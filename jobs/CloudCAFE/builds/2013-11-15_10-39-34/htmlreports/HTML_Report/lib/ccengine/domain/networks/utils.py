#!/usr/bin/env python

# Copyright 2011 OpenStack Foundation
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""Contains utilities for other scripts."""

import ConfigParser
import logging
import logging.handlers
import socket
import subprocess
import struct
import sys
import time
import XenAPI

OVS_OFCTL = '/usr/bin/ovs-ofctl'
OVS_VSCTL = '/usr/bin/ovs-vsctl'
XE = '/opt/xensource/bin/xe'
XENSTORE_READ = '/usr/bin/xenstore-read'
TC = '/sbin/tc'

PUBLICNET = 'publicnet'
SERVICENET = 'servicenet'
ISOLATEDNET = 'isolatednet'
TUNNELNET = 'tunnelnet'
MANAGEMENTNET = 'managementnet'
NVPNET = 'NVP'

COLLAPSED = 'collapsed'
SPLIT = 'split'
BONDED = 'bonded'

INGRESS = 'ingress'
EGRESS = 'egress'

BROADCAST_MAC = struct.pack('BBBBBB', 255, 255, 255, 255, 255, 255)
ARP_HEADER = struct.pack('!HHBBH', 1, 0x0800, 6, 4, 2)
ARP_ETHERNET_TYPE = 0x0806
ARP_TYPE = struct.pack('!H', ARP_ETHERNET_TYPE)

DARK_PATCH = 'dark'
STORMY_PATCH = 'stormy'

LOG = logging.getLogger(__name__)


# note that this decorator ignores **kwargs
def memoize(obj):
    cache = obj.cache = {}

    def memoizer(*args, **kwargs):
        if args not in cache:
            cache[args] = obj(*args, **kwargs)
        return cache[args]

    # note(tr3buchet) and since no functools in 2.4....
    memoizer.__name__ = obj.__name__
    memoizer.__module__ = obj.__module__
    memoizer.__doc__ = obj.__doc__
    memoizer.__dict__.update(obj.__dict__)

    return memoizer


class ClassID(object):
    def __init__(self, classid_string=None, major=None, minor=None):
        if classid_string and ':' in classid_string:
            l = classid_string.split(':')
            self.major = int(l[0], 16)
            self.minor = int(l[1], 16)
        elif major and minor:
            self.major = major
            self.minor = minor
        else:
            msg = 'bad args to create ClassID -> %s %s %s'
            LOG.debug(msg % (classid_string, major, minor))
            raise Exception(msg % (classid_string, major, minor))

    def __str__(self):
        return self.major_str() + ':' + self.minor_str()

    def major_str(self):
        return hex(self.major)[2:]

    def minor_str(self):
        return hex(self.minor)[2:]

    def flow_queue(self):
        """queue that flow tags traffic with to match this class."""
        return self.minor - 1

    def publicnet_classid(self):
        if host_network_flavor() == 'split':
            return ClassID(major=self.major,
                           minor=self.minor)
        else:
            return ClassID(major=self.major,
                           minor=self.minor + 0x1000)

    def servicenet_classid(self):
        if host_network_flavor() == 'split':
            return ClassID(major=self.major,
                           minor=self.minor)
        else:
            return ClassID(major=self.major,
                           minor=self.minor + 0x2000)


class RetryError(Exception):
    pass


class NullHandler(logging.Handler):
    def handle(self, record):
        pass

    def emit(self, record):
        pass

    def createLock(self):
        self.lock = None


class TagFormatter(logging.Formatter):
    def __init__(self, fmt=None, datefmt=None, logtag=None):
        if logtag is not None:
            if fmt is None:
                fmt = '%(message)s'
            fmt = '[%s]' % logtag + ' ' + fmt
        logging.Formatter.__init__(self, fmt, datefmt)


def setup_logging(logtag=None, **kwargs):
    if len(logging.root.handlers) != 0:
        return

    filename = kwargs.get('filename')
    if filename:
        mode = kwargs.get('filemode', 'a')
        maxBytes = int(kwargs.get('maxBytes', 10 ** 7))
        backupCount = int(kwargs.get('backupCount', 5))
        hdlr = logging.handlers.RotatingFileHandler(filename, mode,
                                                    maxBytes=maxBytes,
                                                    backupCount=backupCount)

    stdout = kwargs.get('stdout')
    if stdout:
        stream = kwargs.get("stream")
        hdlr = logging.StreamHandler(stream)

    if not (stdout or filename):
        hdlr = NullHandler()

    fs = kwargs.get("format", '%(asctime)s ' + logging.BASIC_FORMAT)
    dfs = kwargs.get("datefmt", None)

    fmt = TagFormatter(fs, dfs, logtag)
    hdlr.setFormatter(fmt)
    logging.root.addHandler(hdlr)

    level = kwargs.get('level')
    if level:
        logging.root.setLevel(level)


# NOTE(jkoelker) http://code.activestate.com/recipes/578527-retry-loop/
def retryloop(attempts, timeout=None, delay=0, backoff=1, raise_on_fail=False):
    """
    Retry generator for looping.

    Usage:

    for retry in retryloop(10, timeout=30):
        try:
            something
        except SomeException:
            retry()

    for retry in retryloop(10, timeout=30):
        something
        if somecondition:
            retry()

    """
    start = time.time()
    success = set()

    for i in range(attempts):
        success.add(True)
        yield success.clear

        if success:
            return

        duration = time.time() - start

        if timeout is not None and duration > timeout:
            break

        if delay:
            time.sleep(delay)
            delay = delay * backoff

    if not raise_on_fail:
        return

    e = sys.exc_info()[1]

    # No pending exception? Make one
    if e is None:
        try:
            raise RetryError
        except RetryError, e:
            pass

    # Decorate exception with retry information:
    msg = "on attempt {0} of {1} after {2:.3f} seconds"
    e.args = e.args + (msg.format(i, attempts + 1, duration),)

    raise


# NOTE(jkoelker) Ported from 2.7's subprocess, modified for our needs
def check_output(*popenargs, **kwargs):
    popenargs = list(popenargs)
    popenargs[0] = [str(x) for x in popenargs[0]]
    LOG.debug(popenargs)
    kwargs['close_fds'] = kwargs.get('close_fds', True)
    input = kwargs.pop('input', None)

    if input is not None and kwargs.get('stdin') != subprocess.PIPE:
        kwargs['stdin'] = subprocess.PIPE

    process = subprocess.Popen(stdout=subprocess.PIPE, *popenargs, **kwargs)
    output, unused_err = process.communicate(input=input)
    retcode = process.poll()

    return (retcode, output)


def execute(*command, **kwargs):
    """Collect args in tuple for check_output, pass kwargs through."""
    return check_output(command, **kwargs)


def get_return_code(*command, **kwargs):
    return check_output(command, **kwargs)[0]


def get_output(*command, **kwargs):
    return check_output(command, **kwargs)[1].strip()


def raise_for_code(*command, **kwargs):
    expected_codes = kwargs.pop('expected', None)
    r = check_output(command, **kwargs)

    if expected_codes:
        if r[0] in expected_codes:
            return r[1].strip()

    if r[0] != 0:
        msg = 'Err |%s|. output: |%s|' % (r[0], r[1].strip())
        raise Exception(msg)
    else:
        return r[1].strip()


def get_xenapi_session():
    try:
        session = XenAPI.xapi_local()
        session.xenapi.login_with_password('', '')
        return session
    except XenAPI.Failure:
        sys.exit(1)


@memoize
def get_config():
    config = ConfigParser.SafeConfigParser()
    config.read('/opt/rackspace/host.conf')
    if config:
        return config
    raise Exception('config file /opt/rackspace/host.conf not found!')


def host_flavor_class():
    config = get_config()
    value = config.get('DEFAULT', 'flavor_class').lower()
    LOG.debug('config flavor class |%s|' % value)
    return value


def host_network_flavor():
    config = get_config()
    value = config.get('network', 'flavor').lower()
    LOG.debug('config network flavor |%s|' % value)
    return value


def pubnet_qos_percentage():
    config = get_config()
    if config.has_option('network', 'pubnet_qos_percentage'):
        value = config.get('network', 'pubnet_qos_percentage')
    else:
        value = 100
    LOG.debug('config network pubnet_qos_percentage |%s|' % value)
    return int(value)


def qos_bond_factor_percentage():
    config = get_config()
    if config.has_option('network', 'qos_bond_factor_percentage'):
        value = config.get('network', 'qos_bond_factor_percentage')
    else:
        value = 100
    LOG.debug('config network qos_bond_factor_percentage |%s|' % value)
    return int(value)


def flow_bridges():
    config = get_config()
    pflow = config.get('network', 'flow_bridge_publicnet')
    sflow = config.get('network', 'flow_bridge_servicenet')
    r = {PUBLICNET: pflow,
         SERVICENET: sflow,
         ISOLATEDNET: ISOLATEDNET,
         TUNNELNET: TUNNELNET,
         MANAGEMENTNET: MANAGEMENTNET,
         NVPNET: NVPNET}
    LOG.debug('config flow bridges |%s|' % r)
    return r


def patch_ports():
    config = get_config()
    data = {}

    for net in (PUBLICNET, SERVICENET):
        data[net] = {INGRESS: config.get('network', net + '_' + INGRESS),
                     EGRESS: config.get('network', net + '_' + EGRESS)}

    LOG.debug('patch port config |%s|' % data)
    return data


def network_vlans():
    config = get_config()
    r = {PUBLICNET: config.get('network', 'publicnet_vlan'),
         SERVICENET: config.get('network', 'servicenet_vlan'),
         TUNNELNET: config.get('network', 'tunnelnet_vlan')}
    LOG.debug('config vlans |%s|' % r)
    return r


def change_keys(recs, key='uuid', filter_func=None):
    """
    Take a xapi dict, and make the keys the value of recs[ref][key].

    Preserves the ref in rec['ref']

    """
    new_recs = {}

    for ref, rec in recs.iteritems():
        if filter_func is not None and not filter_func(rec):
            continue

        new_recs[rec[key]] = rec
        new_recs[rec[key]]['ref'] = ref

    return new_recs


def expand_reflist(target_recs, refs_key, source_recs, source_key):
    """
    Fill in values from source recs into the ref_key in target_recs.

    e.g. for Tr3buchet

    target_recs = {'uuid': {'refs_key': ['ObjectRef', ...]}}}
    source_recs = {'uuid': {'ref': 'ObjectRef', 'other': 'stuff'}}

    would emit:

    target_recs = {'uuid': {'refs_key': {'source_key':{'ref': 'ObjectRef',
                                                       'other': 'stuff'}}}}

    """
    refs = dict([(r['ref'], r) for r in source_recs.values()])

    for item_key in target_recs:
        item = target_recs[item_key]

        if refs_key not in target_recs[item_key]:
            continue

        if isinstance(target_recs[item_key][refs_key], basestring):
            item[refs_key] = refs[target_recs[item_key][refs_key]]
            continue

        new_value = {}
        for ref in target_recs[item_key][refs_key]:
            new_value[refs[ref][source_key]] = refs[ref]

        item[refs_key] = new_value

    return target_recs


def get_vifs(session):
    """Get vifs from xenserver."""
    recs = session.xenapi.VIF.get_all_records()
    return change_keys(recs, key='uuid')


def get_instances(session):
    is_inst = lambda r: (r['power_state'].lower() == 'running' and
                         not r['is_a_template'] and
                         not r['is_control_domain'] and
                         ('nova_uuid' in r['other_config'] or
                          r['name_label'].startswith('instance-')))
    recs = session.xenapi.VM.get_all_records()
    return change_keys(recs, key='uuid', filter_func=is_inst)


def get_networks(session):
    recs = session.xenapi.network.get_all_records()
    return change_keys(recs, key='uuid')


def get_pifs(session):
    """Get pifs from xenserver."""
    recs = session.xenapi.PIF.get_all_records()
    return change_keys(recs, key='uuid')


def get_compute(session):
    """Get the compute record."""
    ref = session.xenapi.VM.get_by_name_label('compute')
    if not ref:
        return

    rec = session.xenapi.VM.get_record(ref[-1])
    return change_keys({ref[-1]: rec}, key='uuid')


def get_host(session):
    """Get the host record."""
    recs = session.xenapi.host.get_all_records()
    return change_keys(recs, key='uuid')


def send_arp(ifname, mac, ip, vlan=None):
    mac = mac.lower()
    words = mac.split(':')

    int_val = int(''.join(['%.2x' % int(w, 16) for w in words]), 16)
    packed = struct.pack('!HI', int_val >> 32, int_val & 0xffffffff)
    vlan_tag = []

    if vlan is not None:
        vlan_tag.append(struct.pack('!HH', 0x8100, int(vlan)))

    arp = ''.join([ARP_HEADER, packed, socket.inet_aton(ip),
                   packed, socket.inet_aton(ip)])
    frame = ''.join([BROADCAST_MAC, packed] + vlan_tag + [ARP_TYPE, arp])

    try:
        s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW)
        s.bind((ifname, ARP_ETHERNET_TYPE))
        s.send(frame)
        s.close()
    except (socket.error, Exception):
        pass


def get_network_bridges(networks, host, session):
    LOG.debug('Discovering network bridges')

    # NOTE(jkoelker) should we just use defaultdict backport from kitchen?
    bridges = {PUBLICNET: {},
               SERVICENET: {},
               ISOLATEDNET: {},
               TUNNELNET: {},
               MANAGEMENTNET: {},
               NVPNET: {}}

    # NOTE(jkoelker) This is jank
    f = open('/proc/net/route')
    management_br = None
    for line in f.readlines()[1:]:
        cols = line.split('\t')
        if cols[1].strip() == '00000000':
            management_br = cols[0].strip()
            break

    if not management_br:
        LOG.debug('Could not determine managementnet, do you have a '
                  'default route?')

    # NOTE(tr3buchet): make bridges accessible by label
    labeled_bridges = {}
    for network in networks.itervalues():
        labeled_bridges[network['name_label']] = network['bridge']

    # NOTE(jkoelker) Since we're iterating networks here save the bridges
    #                where flows end up
    for network in networks.itervalues():
        if network['name_label'] not in bridges:
            continue

        LOG.debug('Processing network: %s' % network['name_label'])

        LOG.debug('Attemping to magic bridge online')
        session.xenapi.network.attach(network['ref'], host['ref'])
        new_network = session.xenapi.network.get_record(network['ref'])
        network.update(new_network)

        LOG.debug('Discovering ovs bridge for bridge |%s|' % network['bridge'])
        #NOTE(tr3buchet): sorry for this next line
        #                 my mind is a bag of cats at the moment
        ovs_bridge = labeled_bridges[flow_bridges()[network['name_label']]]
        LOG.debug('ovs bridge: |%s|' % ovs_bridge)

        if network['name_label'] in bridges:
            bridges[network['name_label']] = network
            bridges[network['name_label']]['ovs_bridge'] = ovs_bridge

        if network['bridge'] == management_br:
            bridges[MANAGEMENTNET] = network
            bridges[MANAGEMENTNET]['ovs_bridge'] = ovs_bridge

    for name, bridge in bridges.iteritems():
        if not bridge.get('bridge'):
            LOG.error('COULD NOT FIND BRIDGE FOR NETWORK: %s' % name)
            continue

        LOG.debug('Found %s as the %s bridge' % (bridge['bridge'],
                                                 name))
    return bridges
