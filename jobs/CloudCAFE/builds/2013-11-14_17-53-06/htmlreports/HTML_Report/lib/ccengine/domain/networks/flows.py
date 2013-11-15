#!/usr/bin/env python
# vim: tabstop=4 shiftwidth=4 softtabstop=4

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

"""This script is used to configure openvswitch flows on XenServer hosts."""

import argparse
import logging
import netaddr
import simplejson as json
import socket
import struct
import sys

import utils

# This is written to Python 2.4, since that is what is available on XenServer
PRIORITIES = {'drop': 10,
              'normal': 200,
              'multicast': 210,
              'arp': 214,
              'icmp6_nd': 215,
              'tenant': 500,
              'tunnelnet': 1000,
              'compute': 1100,
              'dom0': 1200,
              'cbs': 1300}

TABLE_0 = 0
INTER_VM = 10
SECURITY_GROUP = 20
PORT_SECURITY = 30

# NOTE(jkoelker) Register Values to denote traffic direction
INTER_VM_PORT = 11
INTER_VM_STARBOARD = 16
SECURITY_GROUP_PORT = 21
SECURITY_GROUP_STARBOARD = 26
PORT_SECURITY_PORT = 31
PORT_SECURITY_STARBOARD = 36

# NOTE(jkoelker) Register locations
DIRECTION = 'NXM_NX_REG0[0..7]'

DATA_MARKER = 'cookie'
CBS_NETBLOCKS = ('10.190.128.0/20',)
MANAGEMENT_QUEUE_ID = 1
COMPUTE_QUEUE_ID = 2
CBS_QUEUE_ID = 3

# NOTE(jkoelker) this splits the DATA_MARKER into one 16bit integer for the
#                DOM_ID and one 4bit integer for the VIF_ID.
VIF_ID_MASK = 983040
DOM_ID_MASK = 65535

SENTINEL = object()
LOCAL = 'LOCAL'
NORMAL = 'NORMAL'

LOG = logging.getLogger(__name__)


def get_ipv6_multicast_mac(ip):
    mac_base = 3689292519746568192
    packed_int = socket.inet_pton(socket.AF_INET6, ip)
    int_val = mac_base + struct.unpack('>4I', packed_int)[-1]

    max_word = 2 ** 8 - 1

    words = []
    for _ in range(4):
        word = int_val & max_word
        words.append(int(word))
        int_val >>= 8

    words = words + [51, 51]
    tokens = ['%x' % i for i in reversed(words)]
    return ':'.join(tokens)


def get_ipv6_link_local(mac):
    """Get the link local ipv6 address. Based on code from netaddr."""
    mac = mac.lower()
    words = mac.split(':')
    int_val = 0xfe800000000000000000000000000000

    eui64_tokens = words[0:3] + ['ff', 'fe'] + words[3:6]
    int_val += int(''.join(eui64_tokens), 16)
    int_val ^= 0x00000000000000000200000000000000

    max_word = 2 ** 32 - 1

    _words = []
    for _ in range(4):
        word = int_val & max_word
        _words.append(int(word))
        int_val >>= 32

    packed_int = struct.pack('>4I', *tuple(reversed(_words)))
    return socket.inet_ntop(socket.AF_INET6, packed_int)


def get_snet_gws(ip, routes):
    def str_to_int(addr):
        return struct.unpack('>I', socket.inet_aton(addr))[0]

    ret_set = set()

    ip_int = str_to_int(ip['ip'])
    netmask_int = str_to_int(ip['netmask'])
    network_int = ip_int & netmask_int

    if routes is not None:
        for route in routes:
            gw_int = str_to_int(route['gateway'])
            gw_network_int = gw_int & netmask_int
            if gw_network_int == network_int:
                ret_set.add(route['gateway'])

    if ret_set:
        return tuple(ret_set)

    # NOTE(jkoelker) Fallback to using network address + 1
    gw_int = network_int + 1
    return ('%d.%d.%d.%d' % (gw_int >> 24, (gw_int >> 16) & 0xff,
                            (gw_int >> 8) & 0xff, gw_int & 0xff),)


def get_marker_fragment(dom_id, vif_id):
    dom_id = int(dom_id)
    vif_id = int(vif_id) << 16
    return {DATA_MARKER: '0x%x' % (dom_id + vif_id)}


class OvsFragment(object):
    SEPARATOR = '='

    def __init__(self, key, value=None):
        if isinstance(key, dict):
            if len(key) > 1:
                raise ValueError('Fragment Dictionaries only support one key. '
                                 'Got: %s' % key)

            key, value = key.items()[0]

        self.key = key
        self.value = value

    def __str__(self):
        if self.value is None:
            return str(self.key)
        return str(self.key) + self.SEPARATOR + str(self.value)


class OvsActionFragment(OvsFragment):
    SEPARATOR = ':'


class OvsActionResubmit(object):
    def __init__(self, port, table=None):
        if isinstance(port, dict):
            if len(port) > 1:
                raise ValueError('Fragment Dictionaries only support one key. '
                                 'Got: %s' % port)

            port, table = port.popitem()

        self.port = port
        self.table = table

    def __str__(self):
        if self.table is None:
            return 'resubmit(%s)' % self.port
        return 'resubmit(%s,%s)' % (self.port, self.table)


class OvsFlow(list):
    def add(self, *fragments, **kwargs):
        priority = kwargs.pop('priority', None)
        dom_id = kwargs.pop('dom_id', None)
        vif_id = kwargs.pop('vif_id', 0)

        if priority is not None:
            self.add_fragment({'priority': priority})

        if dom_id is not None:
            self.add_fragment(get_marker_fragment(dom_id, vif_id))

        for fragment in fragments:
            self.add_fragment(fragment)

    def add_fragment(self, fragment, style=OvsFragment):
        """Checking version of self.append(OvsFragment('key', 'value'))."""

        if isinstance(fragment, dict):
            fragment = OvsFragment(fragment)

        if isinstance(fragment, OvsFragment):
            return self.append(fragment)

        if isinstance(style, basestring):
            if style.lower() == 'action':
                style = OvsActionFragment
            else:
                style = OvsFragment

        key = fragment
        value = None

        # NOTE(jkoelker) Parsing is brittle please try to be explicit ;)
        if '=' in fragment:
            key, value = fragment.split('=', 1)
        elif ':' in fragment:
            key, value = fragment.split(':', 1)

        return self.add_fragment(style(key, value), style=style)

    def __str__(self):
        return ','.join([str(fragment) for fragment in self])


class OvsFlowGroup(list):
    def __init__(self, *args, **kwargs):
        self.forced_fragments = tuple(kwargs.pop('forced_fragments', []))
        self.priority = kwargs.pop('priority', None)
        self.dom_id = kwargs.pop('dom_id', None)
        self.vif_id = kwargs.pop('vif_id', 0)

        list.__init__(self, *args, **kwargs)

    def add(self, *fragments, **kwargs):
        flow = OvsFlow()
        priority = kwargs.pop('priority', None)
        dom_id = kwargs.pop('dom_id', SENTINEL)

        if priority is None:
            priority = self.priority

        if priority is not None:
            flow.add_fragment({'priority': priority})

        if dom_id is SENTINEL and self.dom_id is not None:
            flow.add_fragment(get_marker_fragment(self.dom_id, self.vif_id))

        if self.forced_fragments:
            flow.add(*self.forced_fragments)

        flow.add(*fragments, **kwargs)
        self.append(flow)

    def __str__(self):
        return '\n'.join([str(flow) for flow in self])


class OvsFlowList(list):
    def __init__(self, bridge, *args):
        list.__init__(self, *args)
        self._bridge = bridge

    def add(self, flow):
        self.append(flow)

    def _add(self, flow, exe_func=utils.execute):
        return exe_func(utils.OVS_OFCTL, 'add-flow', self._bridge, str(flow))

    def clear_flows(self, dom_id, vif_id, exe_func=utils.execute):
        LOG.debug('Clearing flows for dom_id: %s, vif_id: %s, on bridge: %s' %
                  (dom_id, vif_id, self._bridge))
        fragment = get_marker_fragment(dom_id, vif_id)
        fragment[DATA_MARKER] = '%s/%s' % (fragment[DATA_MARKER],
                                           DOM_ID_MASK | VIF_ID_MASK)
        marker = OvsFragment(fragment)
        return exe_func(utils.OVS_OFCTL, 'del-flows',
                        self._bridge, str(marker))

    def flush(self, exe_func=utils.execute):
        flows = str(self)

        if not flows:
            LOG.debug('No flows for bridge %s' % self._bridge)
            return

        LOG.debug('Flushing flows to bridge: %s' % self._bridge)
        LOG.debug('Flows:\n%s' % flows)
        return exe_func(utils.OVS_OFCTL, 'add-flow', self._bridge, '-',
                        input=flows)

    def __str__(self):
        return '\n'.join([str(flow) for flow in self])


class OvsFlowManager(dict):
    def add(self, flow, bridge):
        if bridge is None:
            LOG.error('Attampted to add flow with None value for bridge. '
                      'dropping (FLOW: %s)' % flow)
            return

        if bridge not in self:
            self[bridge] = OvsFlowList(bridge)

        self[bridge].add(flow)

    def clear_flows(self, dom_id, vif_id, exe_func=utils.execute):
        LOG.debug('Clearing flows for dom_id: %s, vif_id: %s' %
                  (dom_id, vif_id))

        rets = set()
        for bridge in self.itervalues():
            rets.add(bridge.clear_flows(dom_id, vif_id, exe_func=exe_func))
        if len(rets) > 1:
            if exe_func is utils.execute:
                return (1, '')
            elif exe_func is utils.get_output:
                return ''
            else:
                return 1

        return rets.pop()

    def flush(self, exe_func=utils.execute):
        rets = set()
        for bridge in self.itervalues():
            rets.add(bridge.flush(exe_func=exe_func))

        if len(rets) > 1:
            if exe_func is utils.execute:
                return (1, '')
            elif exe_func is utils.get_output:
                return ''
            else:
                return 1

        return rets.pop()

    def __str__(self):
        return '\n'.join(['%s\n%s\n' % item for item in self.iteritems()])


def get_flow_table(table_id, *args, **kwargs):
    table = OvsFlowGroup(forced_fragments=[{'table': table_id}], *args,
                         **kwargs)
    table.add({'actions': 'drop'},
              dom_id=None,
              priority=PRIORITIES['drop'])
    return table


def get_default_drop(*args, **kwargs):
    group = OvsFlowGroup(priority=PRIORITIES['drop'])
    group.add({'actions': 'drop'})
    return group


def get_tunnel_net_flows(tunnelnet):
    group = OvsFlowGroup(priority=PRIORITIES['tunnelnet'], dom_id=0)

    if not tunnelnet or not tunnelnet['PIFs']:
        return group

    pif = get_pif(tunnelnet)
    nw_vlan = int(pif['VLAN'])

    if nw_vlan == -1:
        nw_vlan = None

    tnet_ofport = utils.get_output(utils.OVS_VSCTL, 'get', 'Interface',
                                   tunnelnet['bridge'], 'ofport')

    action = OvsFlow([OvsActionFragment('strip_vlan'),
                      OvsActionFragment('output', tnet_ofport)])

    for port in pif['in_ofports']:
        group.add({'in_port': port},
                  {'dl_vlan': nw_vlan},
                  {'actions': action})
    actions = []
    if nw_vlan is not None:
        actions.append(OvsActionFragment('mod_vlan_vid', nw_vlan))

    if pif['ofport'] == NORMAL:
        # NOTE(jkoelker) In boned mode the tunnelnet bridge needs to be
        #                in vlan_mode=trunk
        utils.execute(utils.OVS_VSCTL, 'set', 'port', tunnelnet['bridge'],
                      'vlan_mode=trunk')
        actions.append(OvsActionFragment(pif['ofport']))

    else:
        actions.append(OvsActionFragment('output', pif['ofport']))

    group.add({'in_port': tnet_ofport},
              {'actions': OvsFlow(actions)})

    return group


def get_cbs_flows(cbs_netblocks, cbs_queue_id):
    group = OvsFlowGroup(priority=PRIORITIES['cbs'], dom_id=0)
    for netblock in cbs_netblocks:
        group.add({'ip': None},
                  {'nw_dst': netblock},
                  {'actions': OvsFlow([OvsActionFragment('set_queue',
                                                         cbs_queue_id),
                                       OvsActionFragment(NORMAL)])})
    return group


def get_dom0_flows(managementnet, management_queue_id):
    group = OvsFlowGroup(priority=PRIORITIES['dom0'], dom_id=0)

    group.add({'in_port': LOCAL},
              {'actions': OvsFlow([OvsActionFragment('set_queue',
                                                     management_queue_id),
                                   OvsActionFragment(NORMAL)])})

    if not managementnet or not managementnet['PIFs']:
        return group

    pif = get_pif(managementnet)

    # NOTE(jkoelker) HIGH-IO management is untagged
    if utils.host_network_flavor() == utils.BONDED:
        for port in pif['in_ofports']:
            group.add({'in_port': port},
                      {'actions': OvsActionFragment(NORMAL)})
        return group

    for port in pif['in_ofports']:
        group.add({'in_port': port},
                  {'vlan_tci': 0},
                  {'actions': OvsActionFragment(NORMAL)})

    return group


def get_compute_flows(compute, compute_queue_id):
    group = OvsFlowGroup(priority=PRIORITIES['compute'])

    if int(compute['domid']) == -1:
        LOG.debug('Compute dom_id is -1, is it running?')
        return group

    for vif in compute['VIFs'].itervalues():
        vif_iface = 'vif%s.%s' % (compute['domid'], vif['device'])
        of_port = utils.get_output(utils.OVS_VSCTL, 'get', 'Interface',
                                   vif_iface, 'ofport')
        group.add({'in_port': of_port},
                  {'actions': OvsFlow([OvsActionFragment('set_queue',
                                                         compute_queue_id),
                                       OvsActionFragment(NORMAL)])},
                  dom_id=compute['domid'], vif_id=vif['device'])

    return group


def get_base_flows(pif):
    table_0 = get_flow_table(TABLE_0, priority=PRIORITIES['normal'])
    inter_vm = get_flow_table(INTER_VM, priority=PRIORITIES['normal'])
    port_security = get_flow_table(PORT_SECURITY,
                                   priority=PRIORITIES['multicast'])

    # NOTE(jkoelker) InterVM Table -> PIF
    table_0.add({'reg0': '0x%x/0xff' % INTER_VM_PORT},
                {'actions': OvsActionFragment('output', pif['ofport'])})

    # NOTE(jkoelker) PIF -> Security Group Table
    actions = [OvsActionFragment('load', '0x%x->%s' % (
        SECURITY_GROUP_STARBOARD,
        DIRECTION)),
        OvsActionResubmit('', SECURITY_GROUP)]

    for port in pif['in_ofports']:
        table_0.add({'reg0': '0x0/0xff'},
                    {'in_port': port},
                    {'actions': OvsFlow(actions)})

    # NOTE(jkoelker) Inter Vm Table -> PIF
    actions = [OvsActionFragment('load', '0x%x->%s' % (INTER_VM_PORT,
                                                       DIRECTION)),
               OvsActionResubmit('', TABLE_0)]
    inter_vm.add({'actions': OvsFlow(actions)})

    port_security.add({'reg0': '0x%x/0xff' % PORT_SECURITY_STARBOARD},
                      {'dl_dst': '01:00:00:00:00:00/01:00:00:00:00:00'},
                      {'actions': 'drop'})

    group = OvsFlowGroup()
    group.append(table_0)
    group.append(inter_vm)
    group.append(port_security)
    return group


def get_rackconnect_security_groups(vm, vif, ips):
    sg = get_flow_table(SECURITY_GROUP,
                        dom_id=vm['domid'],
                        vif_id=vif['device'],
                        priority=PRIORITIES['normal'])

    #          Proto   Port   Network
    allows = (('icmp', None, '10.191.208.0/24'),
              ('tcp', 443, '10.191.208.0/24'),
              ('icmp', None, '10.191.209.0/24'),
              ('tcp', 443, '10.191.209.0/24'),
              ('tcp', 1688, '10.179.63.253'),
              ('tcp', 1688, '10.179.63.254'),
              ('icmp', None, '10.188.0.0/16'),
              ('tcp', None, '10.188.0.0/16'),
              ('udp', None, '10.188.0.0/16'))

    port = [OvsActionFragment('load', '0x%x->%s' % (PORT_SECURITY_STARBOARD,
                                                    DIRECTION)),
            OvsActionResubmit('', PORT_SECURITY)]
    starboard = [OvsActionFragment('load', '0x%x->%s' % (SECURITY_GROUP_PORT,
                                                         DIRECTION)),
                 OvsActionResubmit('', INTER_VM)]

    for ip in ips:
        snet_gws = get_snet_gws(ip, vif['nova'].get('routes'))
        snet_gw_allows = tuple(('icmp', None, snet_gw)
                               for snet_gw in snet_gws)

        for allow in allows + snet_gw_allows:
            # NOTE(jkoelker) Starboard -> Port allow
            fragments = [{allow[0]: None},  # PROTO
                         {'reg0': '0x%x/0xff' % SECURITY_GROUP_STARBOARD},
                         {'dl_dst': vif['MAC']},
                         {'nw_dst': ip['ip']},
                         {'nw_src': allow[2]},
                         {'actions': OvsFlow(port)}]

            if allow[1] is not None:
                fragments.insert(0, {'tp_src': allow[1]})

            sg.add(*fragments)

            # NOTE(jkoelker) Port -> Startboard allow
            fragments = [{allow[0]: None},  # PROTO
                         {'reg0': '0x%x/0xff' % SECURITY_GROUP_PORT},
                         {'nw_src': ip['ip']},
                         {'nw_dst': allow[2]},
                         {'actions': OvsFlow(starboard)}]

            if allow[1] is not None:
                fragments.insert(0, ({'tp_dst': allow[1]}))

            sg.add(*fragments)

            # NOTE(jkoelker) Egress ARP
            sg.add({'arp': None},
                   {'arp_sha': vif['MAC']},
                   {'dl_src': vif['MAC']},
                   {'nw_src': ip['ip']},
                   {'actions': OvsFlow(starboard)})

            # NOTE(jkoelker) Ingress ARP
            sg.add({'arp': None},
                   {'arp_tha': vif['MAC']},
                   {'dl_dst': vif['MAC']},
                   {'actions': OvsFlow(port)})

            # NOTE(jkoelker) Broadcast ARP
            sg.add({'reg0': '0x%x/0xff' % SECURITY_GROUP_STARBOARD},
                   {'arp': None},
                   {'dl_dst': 'ff:ff:ff:ff:ff:ff'},
                   {'nw_dst': ip['ip']},
                   {'actions': OvsFlow(port)},
                   priority=PRIORITIES['arp'])

    return sg


def get_security_group(vm, vif, ips, network):
    if ('rackconnect' in vif['nova'] and
            network['name_label'] == utils.SERVICENET):
        return get_rackconnect_security_groups(vm, vif, ips)

    sg = get_flow_table(SECURITY_GROUP,
                        dom_id=vm['domid'],
                        vif_id=vif['device'],
                        priority=PRIORITIES['normal'])

    # NOTE(jkoelker) Security Group Table -> Port Security Table
    actions = [OvsActionFragment('load', '0x%x->%s' % (
        PORT_SECURITY_STARBOARD,
        DIRECTION)),
        OvsActionResubmit('', PORT_SECURITY)]
    sg.add({'reg0': '0x%x/0xff' % SECURITY_GROUP_STARBOARD},
           {'dl_dst': vif['MAC']},
           {'actions': OvsFlow(actions)})

    for ip in ips:
        # NOTE(jkoelker) Broadcast ARP
        sg.add({'reg0': '0x%x/0xff' % SECURITY_GROUP_STARBOARD},
               {'arp': None},
               {'dl_dst': 'ff:ff:ff:ff:ff:ff'},
               {'nw_dst': ip['ip']},
               {'actions': OvsFlow(actions)},
               priority=PRIORITIES['arp'])

    # NOTE(jkoelker) Security Group Table -> Inter Vm Table
    actions = [OvsActionFragment('load', '0x%x->%s' % (SECURITY_GROUP_PORT,
                                                       DIRECTION)),
               OvsActionResubmit('', INTER_VM)]
    sg.add({'reg0': '0x%x/0xff' % SECURITY_GROUP_PORT},
           {'dl_src': vif['MAC']},
           {'actions': OvsFlow(actions)})

    return sg


def get_tenant_flows(vm, vif, pif, ips, ip6s, network, queue_id):
    vlan = pif['VLAN']

    table_kwargs = dict(dom_id=vm['domid'], vif_id=vif['device'],
                        priority=PRIORITIES['normal'])
    table_0 = get_flow_table(TABLE_0, **table_kwargs)
    port_security = get_flow_table(PORT_SECURITY, **table_kwargs)
    inter_vm = get_flow_table(INTER_VM, **table_kwargs)
    security_groups = get_security_group(vm, vif, ips, network)

    # NOTE(jkoelker) VIF -> Port Security Table
    actions = []
    if vlan is not None:
        actions.append(OvsActionFragment('mod_vlan_vid', vlan))

    if queue_id is not None:
        actions.append(OvsActionFragment('set_queue', queue_id))

    # NOTE(jkoelker) Resubmit *MUST* be the LAST action
    actions.append(OvsActionFragment('load', '0x%x->%s' % (
        PORT_SECURITY_PORT,
        DIRECTION)))
    actions.append(OvsActionResubmit('', PORT_SECURITY))

    table_0.add({'reg0': '0x0/0xff'},
                {'in_port': vif['ofport']},
                {'actions': OvsFlow(actions)})

    # NOTE(jkoelker) Port Security Table -> VIF
    table_0.add({'reg0': '0x%x/0xff' % PORT_SECURITY_STARBOARD},
                {'dl_vlan': vlan},
                {'dl_dst': vif['MAC']},
                {'actions': OvsFlow([OvsActionFragment('strip_vlan'),
                                     OvsActionFragment('output',
                                                       vif['ofport'])])})

    # NOTE(jkoelker) Inter Vm Table -> Security Group Table
    actions = [OvsActionFragment('load', '0x%x->%s' % (
        SECURITY_GROUP_STARBOARD,
        DIRECTION)),
        OvsActionResubmit('', SECURITY_GROUP)]
    inter_vm.add({'dl_dst': vif['MAC']},
                 {'actions': OvsFlow(actions)})

    port = [OvsActionFragment('load', '0x%x->%s' % (SECURITY_GROUP_PORT,
                                                    DIRECTION)),
            OvsActionResubmit('', SECURITY_GROUP)]
    starboard = [OvsActionFragment('load', '0x%x->%s' % (
        PORT_SECURITY_STARBOARD,
        DIRECTION)),
        OvsActionResubmit('', TABLE_0)]

    for ip in ips:
        # NOTE(jkoelker) Port Security Table - > Security Group Table
        port_security.add({'reg0': '0x%x/0xff' % PORT_SECURITY_PORT},
                          {'ip': None},
                          {'dl_src': vif['MAC']},
                          {'nw_src': ip['ip']},
                          {'actions': OvsFlow(port)})

        # NOTE(jkoelker) Port Security Table - > Security Group Table
        port_security.add({'reg0': '0x%x/0xff' % PORT_SECURITY_PORT},
                          {'arp': None},
                          {'arp_sha': vif['MAC']},
                          {'dl_src': vif['MAC']},
                          {'nw_src': ip['ip']},
                          {'actions': OvsFlow(port)})

        # NOTE(jkoelker) Port Security Table -> Table 0 (VIF)
        port_security.add({'reg0': '0x%x/0xff' % PORT_SECURITY_STARBOARD},
                          {'ip': None},
                          {'dl_dst': vif['MAC']},
                          {'nw_dst': ip['ip']},
                          {'actions': OvsFlow(starboard)})

        # NOTE(jkoelker) Port Security Table -> Table 0 (VIF)
        port_security.add({'reg0': '0x%x/0xff' % PORT_SECURITY_STARBOARD},
                          {'arp': None},
                          {'arp_tha': vif['MAC']},
                          {'dl_dst': vif['MAC']},
                          {'actions': OvsFlow(starboard)})

        # NOTE(jkoelker) Port Security Table -> Table 0 (VIF)
        port_security.add({'reg0': '0x%x/0xff' % PORT_SECURITY_STARBOARD},
                          {'arp': None},
                          {'dl_dst': 'ff:ff:ff:ff:ff:ff'},
                          {'nw_dst': ip['ip']},
                          {'actions': OvsFlow(starboard)},
                          priority=PRIORITIES['arp'])

        # NOTE(jkoelker) Table0 -> VIF Broadcast ARP
        table_0.add({'reg0': '0x%x/0xff' % PORT_SECURITY_STARBOARD},
                    {'arp': None},
                    {'dl_dst': 'ff:ff:ff:ff:ff:ff'},
                    {'nw_dst': ip['ip']},
                    {'actions': OvsFlow([OvsActionFragment('strip_vlan'),
                                         OvsActionFragment('output',
                                                           vif['ofport'])])},
                    priority=PRIORITIES['arp'])

    for ip in ip6s:
        ip['ip'] = str(netaddr.IPAddress(ip['ip']))
        # NOTE(jkoelker) Port Security Table - > Security Group Table
        port_security.add({'reg0': '0x%x/0xff' % PORT_SECURITY_PORT},
                          {'ipv6': None},
                          {'dl_src': vif['MAC']},
                          {'ipv6_src': ip['ip']},
                          {'actions': OvsFlow(port)})

        # NOTE(jkoelker) Port Security Table -> Table 0 (VIF)
        port_security.add({'reg0': '0x%x/0xff' % PORT_SECURITY_STARBOARD},
                          {'ipv6': None},
                          {'dl_dst': vif['MAC']},
                          {'ipv6_dst': ip['ip']},
                          {'actions': OvsFlow(starboard)})

        # NOTE(jkoelker) Allow ND Broadcast ingress
        port_security.add({'reg0': '0x%x/0xff' % PORT_SECURITY_STARBOARD},
                          {'icmp6': None},
                          {'icmp_type': 135},
                          {'nd_target': ip['ip']},
                          {'nw_ttl': 255},
                          {'dl_dst': get_ipv6_multicast_mac(ip['ip'])},
                          {'actions': OvsFlow(starboard)},
                          priority=PRIORITIES['icmp6_nd'])

        # NOTE(jkoelker) Allow ND egress
        for icmp_type in (135, 136):
            port_security.add({'reg0': '0x%x/0xff' % PORT_SECURITY_PORT},
                              {'icmp6': None},
                              {'icmp_type': icmp_type},
                              {'dl_src': vif['MAC']},
                              {'ipv6_src': ip['ip']},
                              {'actions': OvsFlow(port)},
                              priority=PRIORITIES['icmp6_nd'])

        # NOTE(jkoelker) Drop all other icmp6
        for icmp_type in (134, 135, 136, 137, 146, 147, 151, 152, 153):
            port_security.add({'reg0': '0x%x/0xff' % PORT_SECURITY_PORT},
                              {'icmp6': None},
                              {'icmp_type': icmp_type},
                              {'actions': 'drop'})

    group = OvsFlowGroup()
    group.append(table_0)
    group.append(port_security)
    group.append(inter_vm)
    group.append(security_groups)
    return group


def get_ovs_flows(ovs, vm, vif, network, queue_id):

    pif = get_pif(network)

    ovs.add(get_base_flows(pif), network.get('ovs_bridge'))

    ips = vif['nova'].get('ips', [])
    ip6s = vif['nova'].get('ip6s', [])

    if ip6s:
        ip6s.append(dict(ip=get_ipv6_link_local(vif['MAC'])))

    ovs.add(get_tenant_flows(vm, vif, pif, ips, ip6s, network, queue_id),
            network.get('ovs_bridge'))

    return ovs


def get_patch_port_names(dom_id, vif_id):
    isolated_port = 'vifp-isolated-%s-%s' % (dom_id, vif_id)
    nvp_port = 'vifp-nvp-%s-%s' % (dom_id, vif_id)
    return isolated_port, nvp_port


def unplug_patch_ports(dom_id, vif_id, networks):
    isolated_port, nvp_port = get_patch_port_names(dom_id, vif_id)

    LOG.debug('Deleteing patch ports')
    utils.execute(utils.OVS_VSCTL, '--if-exist', 'del-port',
                  networks[utils.ISOLATEDNET]['bridge'], isolated_port)
    utils.execute(utils.OVS_VSCTL, '--if-exist', 'del-port',
                  networks[utils.NVPNET]['bridge'], nvp_port)


def plug_patch_ports(ovs, vif, vm, networks, queue_id=None):
    LOG.debug('Vif plugged into IsolatedNet bridge')
    isolated_port, nvp_port = get_patch_port_names(vm['domid'],
                                                   vif['device'])
    isolated = networks[utils.ISOLATEDNET]
    nvp = networks[utils.NVPNET]

    data = {'iface-status': 'active',
            'iface-id': vif['other_config']['nicira-iface-id'],
            'vm-id': vm['uuid'],
            'attached-mac': vif['MAC'].upper()}

    LOG.debug('Creating patch ports')

    utils.get_return_code(utils.OVS_VSCTL, '--may-exist', 'add-port',
                          isolated['bridge'], isolated_port, '--',
                          'set', 'Interface', isolated_port, 'type=patch',
                          'options:peer=%s' % nvp_port)

    external_ids = ['external_ids:%s=%s' % (k, v) for k, v in data.iteritems()]
    utils.get_return_code(utils.OVS_VSCTL, '--may-exist', 'add-port',
                          nvp['bridge'], nvp_port, '--', 'set',
                          'Interface', nvp_port, 'type=patch',
                          'options:peer=%s' % isolated_port, *external_ids)

    LOG.debug('Discovering patch ofport')
    patch_ofport = utils.get_output(utils.OVS_VSCTL, 'get', 'Interface',
                                    isolated_port, 'ofport')
    LOG.debug('Found patch ofport %s' % patch_ofport)

    group = OvsFlowGroup(dom_id=vm['domid'], vif_id=vif['device'],
                         priority=PRIORITIES['normal'])

    actions = []
    if queue_id is not None:
        actions.append(OvsActionFragment('set_queue', queue_id))

    actions.append(OvsActionFragment('output', patch_ofport))

    group.add({'in_port': vif['ofport']},
              {'actions': OvsFlow(actions)})
    group.add({'in_port': patch_ofport},
              {'actions': OvsActionFragment('output', vif['ofport'])})
    ovs.add(group, isolated['bridge'])
    return ovs


def get_instance(session, dom_id):
    vm = None

    for retry in utils.retryloop(10, delay=1):
        instances = utils.get_instances(session)

        for uuid, instance in instances.iteritems():
            if instance['domid'] == dom_id:
                vm = {uuid: instance}
                break

        if not vm:
            LOG.debug('Instance not found via domid (%s), retrying' % dom_id)
            retry()

    return vm


def get_pif(network):
    if network['PIFs']:
        device = network['PIFs'].keys()[0]
        pif = network['PIFs'][device]
    else:
        pif = {}

    if 'ofport' not in pif:
        if (utils.host_network_flavor() == utils.BONDED and
                network['name_label'] in (utils.PUBLICNET,
                                          utils.SERVICENET)):

            patch_ports = utils.patch_ports()
            ingress = patch_ports[network['name_label']][utils.INGRESS]

            pif['ofport'] = utils.get_output(utils.OVS_VSCTL, 'get',
                                             'Interface', ingress,
                                             'ofport')
            pif['in_ofports'] = [utils.get_output(utils.OVS_VSCTL, 'get',
                                                  'Interface', ingress,
                                                  'ofport')]
            pif['device'] = 'bond0'
            network['PIFs'][pif['device']] = pif
        else:
            LOG.debug('Discovering pif ofport')
            pif['ofport'] = utils.get_output(utils.OVS_VSCTL, 'get',
                                             'Interface',
                                             pif['device'], 'ofport')
            pif['in_ofports'] = [pif['ofport']]
            LOG.debug('Found pif ofport %s' % pif['ofport'])

    return pif


def main(command, vif_raw):
    LOG.debug('Running vif script')
    if command == 'add':
        LOG.debug('Add Command: %s' % sys.argv[1:])
        return 0

    LOG.debug('Command requested: %s' % command)
    LOG.debug('Raw VIF data: %s' % vif_raw)

    vif_name, dom_id, vif_id = vif_raw.split('-')
    dom_id = dom_id
    vif_id = vif_id
    vif_iface = '%s%s.%s' % (vif_name, dom_id, vif_id)

    LOG.debug('Connecting to XenAPI')
    session = utils.get_xenapi_session()

    LOG.debug('Discovering host')
    host = utils.get_host(session).values()[-1]

    LOG.debug('Listing Networks')
    networks = utils.get_networks(session)
    networks = utils.get_network_bridges(networks, host, session)

    LOG.debug('Discovering PIFs')
    pifs = utils.get_pifs(session)

    LOG.debug('Exploding PIF refs in networks')
    networks = utils.expand_reflist(networks, 'PIFs', pifs, 'device')

    if not networks[utils.ISOLATEDNET]:
        LOG.debug('Isolated bridge not found')

    LOG.debug('Discovering compute dom_id')
    compute = utils.get_compute(session)

    LOG.debug('Discovering VIFs')
    vifs = utils.get_vifs(session)

    LOG.debug('Exploding VIF refs in compute')
    compute = utils.expand_reflist(compute, 'VIFs', vifs, 'device')

    compute = compute.values()[-1]

    LOG.debug('Found compute with dom_id %s' % compute['domid'])

    LOG.debug('Discovering vif bridge/network')
    bridge = utils.get_output(utils.OVS_VSCTL, 'iface-to-br', vif_iface)
    network = None
    for net in networks.itervalues():
        if net.get('bridge') == bridge:
            network = net
            break

    ovs = OvsFlowManager()

    # NOTE(jkoelker) Always apply base flows
    for net_br in set([net.get('ovs_bridge')
                       for name, net in networks.iteritems()
                       if name != utils.NVPNET]):
        LOG.debug('Adding default drop flows to bridge %s' % net_br)
        ovs.add(get_default_drop(), net_br)

    LOG.debug('Adding tunnelnet flows')
    ovs.add(get_tunnel_net_flows(networks[utils.TUNNELNET]),
            networks[utils.TUNNELNET].get('ovs_bridge'))

    LOG.debug('Adding dom0 flows')
    ovs.add(get_dom0_flows(networks[utils.MANAGEMENTNET],
                           MANAGEMENT_QUEUE_ID),
            networks[utils.MANAGEMENTNET].get('ovs_bridge'))

    # NOTE(jkoelker) HighIO needs this on ManagementNet
    if utils.host_network_flavor() == utils.BONDED:
        cbs_bridge = utils.MANAGEMENTNET
    else:
        cbs_bridge = utils.TUNNELNET

    LOG.debug('Adding cbs flows')
    ovs.add(get_cbs_flows(CBS_NETBLOCKS, CBS_QUEUE_ID),
            networks[cbs_bridge].get('ovs_bridge'))

    LOG.debug('Adding compute flows')
    try:
        ovs.add(get_compute_flows(compute, COMPUTE_QUEUE_ID),
                networks[utils.MANAGEMENTNET].get('ovs_bridge'))
    except ValueError:
        LOG.exception('Compute not found: is it running?')

    # NOTE(jkoelker) If this is a compute vif flush and return
    if compute['domid'] == dom_id:
        LOG.debug('Running for compute vm')
        if command == 'show':
            LOG.debug('Showing flows')
            print str(ovs)
            return 0

        return ovs.flush(exe_func=utils.get_return_code)

    # NOTE(jkoelker) If we are plugged into the NVP integration bridge
    if network == networks[utils.NVPNET]:
        LOG.debug('Vif pluged into NVP integration bridge, take no action')
        return 0

    # NOTE(jkoelker) offline/remove *must* execute prior to the xenstore read
    if command in ('offline', 'remove'):
        LOG.debug('Detected offline event')
        # Make sure to flush out the base flows
        ovs.flush(exe_func=utils.execute)

        if network == networks[utils.ISOLATEDNET]:
            unplug_patch_ports(dom_id, vif_id, networks)

        return ovs.clear_flows(dom_id, vif_id,
                               exe_func=utils.get_return_code)

    # NOTE(jkoelker) fixup the vlan
    LOG.debug('Discovering pif')

    if network is None:
        LOG.error('Totes no network found brah. You sure this hyperwiser '
                  'is setup right? About to crash in 3...')
        LOG.error('2...')
        LOG.error('1...')

    pif = get_pif(network)

    if pif:
        vlans = utils.network_vlans()
        if network['name_label'] in vlans:
            vlan = int(vlans[network['name_label']])
        else:
            vlan = None

        network['PIFs'][pif['device']]['VLAN'] = vlan

    LOG.debug('Vif plugged into %s on network %s' % (bridge,
                                                     network['name_label']))

    LOG.debug('Discovering vm')
    vm = get_instance(session, dom_id)

    if not vm:
        LOG.error('COULD NOT DETERMINE INSTANCE FOR DOMID: %s' % dom_id)
        return 99

    if not network:
        LOG.error('COULD NOT DETERMINE NETWORK FOR BRIDGE: %s' % bridge)
        return 99

    vm = utils.expand_reflist(vm, 'VIFs', vifs, 'device')
    vm_uuid = vm.keys()[-1]
    vm = vm.values()[-1]

    LOG.debug('Found vm %s for domid %s.' % (vm_uuid, dom_id))

    vif = vm['VIFs'][vif_id]
    vif['iface'] = vif_iface

    xenstore_key = 'vm-data/networking/%s' % ''.join(vif['MAC'].split(':'))

    # NOTE(jkoelker) So sometimes we are too fast and xenstore has no datas
    for retry in utils.retryloop(10, delay=1):
        xenstore_data = vm.get('xenstore_data')

        if not xenstore_data or not xenstore_data.get(xenstore_key):
            vm = get_instance(session, dom_id)
            vm = utils.expand_reflist(vm, 'VIFs', vifs, 'device')
            vm_uuid = vm.keys()[-1]
            vm = vm.values()[-1]
            retry()

    vif['nova'] = json.loads(vm['xenstore_data'][xenstore_key])

    LOG.debug('Discovering vif ofport')
    vif['ofport'] = utils.get_output(utils.OVS_VSCTL, 'get', 'Interface',
                                     vif['iface'], 'ofport')
    LOG.debug('Found vif ofport %s' % vif['ofport'])

    # retry to solve race condition
    classid = None
    for retry in utils.retryloop(10, delay=1):
        try:
            classid = utils.ClassID(vm['other_config'].get('qos_queue', ''))
            LOG.debug('qos lookup, vm_uuid |%s| found |%s|' % (vm_uuid,
                                                               classid))
        except:
            LOG.debug('qos lookup, vm_uuid |%s| failed, retrying' % vm_uuid)
            # NOTE(jkoelker) Get a fresher copy of other-config
            new_vm = session.xenapi.VM.get_record(vm['ref'])
            vm['other_config'] = new_vm['other_config']
            retry()

        queue_id = None
        if classid:
            if network == networks[utils.PUBLICNET]:
                queue_id = classid.publicnet_classid().flow_queue()
            elif (network == networks[utils.SERVICENET] or
                  network == networks[utils.ISOLATEDNET]):
                queue_id = classid.servicenet_classid().flow_queue()

    if network == networks[utils.ISOLATEDNET]:
        ovs = plug_patch_ports(ovs, vif, vm, networks, queue_id=queue_id)
    else:
        ovs = get_ovs_flows(ovs, vm, vif, network, queue_id)

    if command in ('online', 'reset'):
        LOG.debug('Detected online event')
        if command == 'reset':
            ovs.clear_flows(dom_id, vif_id, exe_func=utils.get_return_code)

        ret = ovs.flush(exe_func=utils.get_return_code)

        # NOTE(jkoelker) Send out gARP's for all ipv4s
        if network['name_label'] not in (utils.ISOLATEDNET, ):
            # NOTE(jkoelker) Xapi sets the tag field in ovsdb to the value
            #                of the bridge the vif is plugged into. Since
            #                we are handling the vlans ourselves reset it back.
            # TODO(jkoelker) see if there is a way to get Xapi not to do that
            utils.execute(utils.OVS_VSCTL, 'set', 'port', vif['iface'],
                          'vlan_mode=trunk')
            for ip in vif['nova'].get('ips', []):
                utils.send_arp(pif['device'], vif['MAC'], ip['ip'],
                               pif['VLAN'])

        return ret

    print str(ovs)
    return 0


if __name__ == '__main__':
    description = 'Setup flows for vif-<domid>-<deviceid>'
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('command', help='Action [online|offline|reset]')
    parser.add_argument('vif', help='VIF (vif-<domid>-<deviceid>)')
    parser.add_argument('-v', '--verbose', action='store_true',
                        dest='stdout', default=False, help='Log to stdout')
    parser.add_argument('-d', '--debug', default=None, dest='filename',
                        action='store_const',
                        const='/var/log/flow_udev.log',
                        help='Log to logfile')
    args = parser.parse_args()

    utils.setup_logging(filename=args.filename, stdout=args.stdout,
                        level=logging.DEBUG, logtag=args.vif)

    ret = 69
    try:
        ret = main(args.command, args.vif)
    except:
        LOG.exception('BOOM!')
    sys.exit(ret)
