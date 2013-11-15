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

"""
This script is used to configure openvswitch flows on XenServer hosts.

This copy of the script is maintained in CloudCAFE to enable the testing of
dual mode flows in test cases.
"""

from netaddr import EUI, IPAddress
import os
import re
import socket
import subprocess
import struct
import sys

from ccengine.domain.base_domain import BaseMarshallingDomain
from ccengine.domain.networks import flows


# This is written to Python 2.4, since that is what is available on XenServer
OVS_OFCTL = '/usr/bin/ovs-ofctl'
OVS_VSCTL = '/usr/bin/ovs-vsctl'
XE = '/opt/xensource/bin/xe'
XENSTORE_READ = '/usr/bin/xenstore-read'
XENSTORE_LIST = '/usr/bin/xenstore-list'

PUBLICNET = 'publicnet'
SERVICENET = 'servicenet'

PRIORITIES = {'drop': 10,
              'tenant': 500,
              'tunnelnet': 1000,
              'compute': 1100,
              'dom0': 1200, }

DATA_MARKER = 'cookie'

# NOTE(jkoelker) this splits the DATA_MARKER into one 16bit integer for the
#                DOM_ID and one 4bit integer for the VIF_ID.
VIF_ID_MASK = 983040
DOM_ID_MASK = 65535

BROADCAST_MAC = struct.pack('BBBBBB', 255, 255, 255, 255, 255, 255)
ARP_HEADER = struct.pack('!HHBBH', 1, 0x0800, 6, 4, 2)
ARP_ETHERNET_TYPE = 0x0806
ARP_TYPE = struct.pack('!H', ARP_ETHERNET_TYPE)


def _send_arp(ifname, mac, ip, vlan=None):
    mac = mac.lower()
    words = mac.split(':')

    int_val = int(''.join(['%.2x' % int(w, 16) for w in words]), 16)
    packed = struct.pack('!HI', int_val >> 32, int_val & 0xffffffff)
    vlan_tag = []

    if vlan is not None:
        vlan_tag.append(struct.pack('!HH', 0x8100, int(vlan)))

    try:
        s = socket.socket(socket.AF_PACKET, socket.SOCK_RAW)
        s.bind((ifname, ARP_ETHERNET_TYPE))
        arp = ''.join([ARP_HEADER, packed, socket.inet_aton(ip),
                       packed, socket.inet_aton(ip)])
        frame = ''.join([BROADCAST_MAC, packed] + vlan_tag + [ARP_TYPE, arp])
        s.send(frame)
        s.close()
    except (socket.error, Exception):
        pass


# NOTE(jkoelker) Ported from 2.7's subprocess, modified for our needs
def check_output(*popenargs, **kwargs):
    kwargs['close_fds'] = kwargs.get('close_fds', True)
    input = kwargs.pop('input', None)

    if input is not None and kwargs.get('stdin') != subprocess.PIPE:
        kwargs['stdin'] = subprocess.PIPE

    process = subprocess.Popen(stdout=subprocess.PIPE, *popenargs, **kwargs)
    output, unused_err = process.communicate(input=input)
    retcode = process.poll()

    return (retcode, output)


def execute(*command, **kwargs):
    """Collect args in tuple for check_output, pass kwargs through"""
    return check_output(command, **kwargs)


def get_return_code(*command, **kwargs):
    return check_output(command, **kwargs)[0]


def get_output(*command, **kwargs):
    return check_output(command, **kwargs)[1].strip()


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
    """Get the link local ipv6 address. Based on code from netaddr"""
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
    return {DATA_MARKER: dom_id + vif_id}


class OvsFragment(object):
    SEPARATOR = '='

    def __init__(self, key, value=None):
        if isinstance(key, dict):
            if len(key) > 1:
                raise ValueError('Fragment Dictionaries only support one key. '
                                 'Got: %s' % key)

            key, value = key.popitem()

        self.key = key
        self.value = value

    def __str__(self):
        if self.value is None:
            return str(self.key)
        if self.key == DATA_MARKER and not isinstance(self.value, basestring):
            str_value = hex(self.value)
        else:
            str_value = str(self.value)
        return str(self.key) + self.SEPARATOR + str_value


class OvsActionFragment(OvsFragment):
    SEPARATOR = ':'


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
        """Checking version of self.append(OvsFragment('key', 'value'))"""

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

    def __eq__(self, other):
        if not isinstance(other, OvsFlow):
            return NotImplemented
        if len(self) != len(other):
            return False
        self_fragments = {}
        for fragment in self:
            self_fragments[fragment.key] = fragment.value
        for fragment in other:
            self_frg_value = self._get_fragment_value(fragment.key,
                                                      self_fragments)
            if self_frg_value != 'not found':
                if self_frg_value != fragment.value:
                    return False
            else:
                return False
        return True

    keys_equivalences = {
        'nw_dst': 'arp_tpa',
        'nw_src': 'arp_spa',
        'arp_tpa': 'nw_dst',
        'arp_spa': 'nw_src', }

    def _get_fragment_value(self, key, fragments_dict):
        if key in fragments_dict:
            return fragments_dict[key]
        elif key in self.keys_equivalences and (self.keys_equivalences[key] in
                                                fragments_dict):
            return fragments_dict[self.keys_equivalences[key]]
        else:
            return 'not found'

    def __ne__(self, other):
        result = self.__eq__(other)
        if result is NotImplemented:
            return result
        return not result


class OvsFlowGroup(list):
    def __init__(self, *args, **kwargs):
        self.forced_fragments = tuple(kwargs.pop('forced_fragments', []))
        self.priority = kwargs.pop('priority', None)
        self.dom_id = kwargs.pop('dom_id', None)
        self.vif_id = kwargs.pop('vif_id', 0)

        list.__init__(self, *args, **kwargs)

    def add(self, *fragments, **kwargs):
        flow = OvsFlow()
        if self.priority is not None:
            flow.add_fragment({'priority': self.priority})

        if self.dom_id is not None:
            flow.add_fragment(get_marker_fragment(self.dom_id, self.vif_id))

        flow.add(*(self.forced_fragments + fragments), **kwargs)
        self.append(flow)

    def __str__(self):
        return '\n'.join([str(flow) for flow in self])


class OvsFlowManager(list):
    def add(self, flow):
        self.append(flow)

    def _add(self, flow, bridge, exe_func=execute):
        return exe_func(OVS_OFCTL, 'add-flow', bridge, str(flow))

    def clear_flows(self, bridge, dom_id, vif_id, exe_func=execute):
        fragment = get_marker_fragment(dom_id, vif_id)
        fragment[DATA_MARKER] = '%s/%s' % (fragment[DATA_MARKER],
                                           DOM_ID_MASK | VIF_ID_MASK)
        marker = OvsFragment(fragment)
        return exe_func(OVS_OFCTL, 'del-flows', bridge, str(marker))

    def flush(self, bridge, exe_func=execute):
        return exe_func(OVS_OFCTL, 'add-flow', bridge, '-', input=str(self))

    def __str__(self):
        return '\n'.join([str(flow) for flow in self])


def get_default_drop(*args, **kwargs):
    group = OvsFlowGroup(priority=PRIORITIES['drop'])
    group.add({'actions': 'drop'})
    return group


def get_tunnel_net_flows(*args, **kwargs):
    group = OvsFlowGroup(priority=PRIORITIES['tunnelnet'], dom_id=0)
    network_uuid = get_output(XE, 'network-list',
                              'name-label=tunnelnet', '--minimal')
    network_uuid = kwargs['network_uuid']
    if not network_uuid:
        return group

    bridge = get_output(XE, 'network-param-get', 'param-name=bridge',
                        'uuid=%s' % network_uuid)
    pif_uuid = get_output(XE, 'network-param-get', 'param-name=PIF-uuids',
                          'uuid=%s' % network_uuid)
    phys_dev = get_output(XE, 'pif-param-get', 'param-name=device',
                          'uuid=%s' % pif_uuid)
    nw_vlan = get_output(XE, 'pif-param-get', 'param-name=VLAN',
                         'uuid=%s' % pif_uuid)
    pif_ofport = get_output(OVS_VSCTL, 'get', 'Interface', phys_dev,
                            'ofport')
    tnet_ofport = get_output(OVS_VSCTL, 'get', 'Interface', bridge,
                             'ofport')

    pif_ofport = kwargs['pif_ofport']
    nw_vlan = kwargs['nw_vlan']
    tnet_ofport = kwargs['tnet_ofport']
    group.add({'in_port': pif_ofport},
              {'dl_vlan': nw_vlan},
              {'actions': OvsFlow([OvsActionFragment('strip_vlan'),
                                   OvsActionFragment('output',
                                                     tnet_ofport)])})
    group.add({'in_port': tnet_ofport},
              {'actions': OvsFlow([OvsActionFragment('mod_vlan_vid', nw_vlan),
                                   OvsActionFragment('output', pif_ofport)])})

    return group


def get_dom0_flows(*args, **kwargs):
    group = OvsFlowGroup(priority=PRIORITIES['dom0'], dom_id=0)
    group.add({'in_port': 'LOCAL'}, {'actions': 'normal'})
    return group


def get_compute_flows(compute_dom_id):
    vifs = get_output(XENSTORE_LIST,
                      '/local/domain/%s/device/vif' % compute_dom_id)
    vifs = [vif.strip() for vif in vifs.split()]

    group = OvsFlowGroup(priority=PRIORITIES['compute'])

    for vif_id in vifs:
        vif = 'vif%s.%s' % (compute_dom_id, vif_id)
        of_port = get_output(OVS_VSCTL, 'get', 'Interface', vif, 'ofport')
        group.add({'in_port': of_port},
                  {'actions': 'normal'},
                  dom_id=compute_dom_id, vif_id=vif_id)

        xenstore_key = '/xapi/%s/private/vif/%s/bridge' % (compute_dom_id,
                                                           vif_id)
        bridge = get_output(XENSTORE_READ, xenstore_key)
        bridge = get_output(OVS_VSCTL, 'br-to-parent', bridge)

        network_uuid = get_output(XE, 'network-list', 'bridge=%s' % bridge,
                                  '--minimal')
        pif_uuid = get_output(XE, 'network-param-get', 'param-name=PIF-uuids',
                              'uuid=%s' % network_uuid)
        phys_dev = get_output(XE, 'pif-param-get', 'uuid=%s' % pif_uuid,
                              'param-name=device')
        pif_ofport = get_output(OVS_VSCTL, 'get', 'Interface', phys_dev,
                                'ofport')

        group.add({'in_port': pif_ofport},
                  {'vlan_tci': 0},
                  {'actions': 'normal'},
                  dom_id=compute_dom_id)

    return group


def get_tenant_ipv4_flows(dom_id, vif_id, pif_ofport, vif_mac, ip,
                          vif_ofport, queue_id=None, nw_vlan=None):
    '''
    @summary: Calculates the flows to handle ipv4 traffic for a Xen domain
              virtual interface
    @param dom_id: The domain's (VM) id assigned by Xen
    @type dom_id: String
    @param vif_id: The virtual interface id assigned by Xen
    @type vif_id: String
    @param pif_ofport: The openflow port number assigned openVswitch to the
                       physical interface that handles the traffic of the
                       virtual interface
    @type pif_ofport: String
    @param vif_mac: The MAC address assigned by Xen the the virtual interface
    @type vif_mac: String
    @param ip: The version 4 ip address assigned to the virtual interface
    @type ip: String
    @param vif_ofport: The openflow port number assigned in openVswitch to the
                       virtual interface
    @type vif_ofport: String
    @param queue_id: The id of the HTB class assigned to manage the quality of
                     service characteristics of the virtual interface
    @type queue_id: String
    @param nw_vlan: The id of the virtual lan carrying the virtual interface
                    traffic
    @type nw_vlan: String
    @return: flows for the virtual interface
    @type return: String
    '''
    priority = PRIORITIES['tenant']
    group = OvsFlowGroup(dom_id=dom_id, vif_id=vif_id)

    # NOTE(jkoelker) arp ingress
    fragments = [{'dl_dst': vif_mac},
                 {'actions': OvsFlow([OvsActionFragment('strip_vlan'),
                                      OvsActionFragment('output',
                                                        vif_ofport)])}]

    group.add(priority=priority + 5, *fragments)

    # NOTE(jkoelker) allow address pair ip traffic vif egress
    #                actions are order specific
    actions = []
    if nw_vlan is not None:
        actions.append(OvsActionFragment('mod_vlan_vid', nw_vlan))

    if queue_id is not None:
        actions.append(OvsActionFragment('set_queue', queue_id))

    actions.append(OvsActionFragment('output', pif_ofport))

    group.add({'ip': None},
              {'in_port': vif_ofport},
              {'dl_src': vif_mac},
              {'nw_src': ip},
              {'actions': OvsFlow(actions)},
              priority=priority)

    # NOTE(jkoelker) allow arp from mac vm vif egress from address pair
    #                Reuses the actions from above
    group.add({'arp': None},
              {'in_port': vif_ofport},
              {'dl_src': vif_mac},
              {'arp_sha': vif_mac},
              {'nw_src': ip},
              {'actions': OvsFlow(actions)},
              priority=priority + 2)

    # NOTE(jkoelker) arp broadcast from pif
    fragments = [{'arp': None},
                 {'dl_dst': 'ff:ff:ff:ff:ff:ff'},
                 {'nw_dst': ip},
                 {'actions': OvsFlow([OvsActionFragment('strip_vlan'),
                                      OvsActionFragment('output',
                                                        vif_ofport)])}]

    group.add(priority=priority + 2, *fragments)
    return group


def get_broadcast_multicast_flows(dom_id, vif_id, vif_ofport):
    '''
    @summary: Calculates the flows to handle broadcast and multicast for a Xen
              domain virtual interface
    @param dom_id: The domain's (VM) id assigned by Xen
    @type dom_id: String
    @param vif_id: The virtual interface id assigned by Xen
    @type vif_id: String
    @param vif_ofport: The openflow port number assigned in openVswitch to the
                       virtual interface
    @type vif_ofport: String
    @return: flows for the virtual interface
    @type return: String
    '''
    priority = PRIORITIES['tenant']
    group = OvsFlowGroup(dom_id=dom_id, vif_id=vif_id)

    # NOTE(jkoelker) Block broadcast/mulitcast
    group.add({'in_port': vif_ofport},
              {'dl_dst': '01:00:00:00:00:00/01:00:00:00:00:00'},
              {'actions': 'drop'},
              priority=priority + 1)

    return group


def get_tenant_ipv6_flows(dom_id, vif_id, pif_ofport, vif_mac, ip6,
                          vif_ofport, queue_id=None, nw_vlan=None):
    '''
    @summary: Calculates the flows to handle ipv6 traffic for a Xen domain
              virtual interface
    @param dom_id: The domain's (VM) id assigned by Xen
    @type dom_id: String
    @param vif_id: The virtual interface id assigned by Xen
    @type vif_id: String
    @param pif_ofport: The openflow port number assigned openVswitch to the
                       physical interface that handles the traffic of the
                       virtual interface
    @type pif_ofport: String
    @param vif_mac: The MAC address assigned by Xen the the virtual interface
    @type vif_mac: String
    @param ip6: The version 6 ip address assigned to the virtual interface
    @type ip6: String
    @param vif_ofport: The openflow port number assigned in openVswitch to the
                       virtual interface
    @type vif_ofport: String
    @param queue_id: The id of the HTB class assigned to manage the quality of
                     service characteristics of the virtual interface
    @type queue_id: String
    @param nw_vlan: The id of the virtual lan carrying the virtual interface
                    traffic
    @type nw_vlan: String
    @return: flows for the virtual interface
    @type return: String
    '''
    priority = PRIORITIES['tenant']
    group = OvsFlowGroup(dom_id=dom_id, vif_id=vif_id)

    # NOTE(jkoelker) ND broadcast ingress
    fragments = [{'icmp6': None},
                 {'icmp_type': 135},
                 {'nd_target': ip6},
                 {'nw_ttl': 255},
                 {'dl_dst': get_ipv6_multicast_mac(ip6)},
                 {'actions': OvsFlow([OvsActionFragment('strip_vlan'),
                                      OvsActionFragment('output',
                                                        vif_ofport)])}]

    group.add(priority=priority + 5, *fragments)

    # NOTE(jkoelker) allow address pair ipv6 traffic vif egres
    #                actions are order specific
    actions = []
    if nw_vlan is not None:
        actions.append(OvsActionFragment('mod_vlan_vid', nw_vlan))

    if queue_id is not None:
        actions.append(OvsActionFragment('set_queue', queue_id))

    actions.append(OvsActionFragment('output', pif_ofport))

    group.add({'ipv6': None},
              {'in_port': vif_ofport},
              {'dl_src': vif_mac},
              {'ipv6_src': ip6},
              {'actions': OvsFlow(actions)},
              priority=priority)

    # NOTE(jkoelker) Allow NDP. Reuses the actions from above
    for icmp_type in (135, 136):
        group.add({'icmp6': None},
                  {'icmp_type': icmp_type},
                  {'in_port': vif_ofport},
                  {'dl_src': vif_mac},
                  {'ipv6_src': ip6},
                  {'actions': OvsFlow(actions)},
                  priority=priority + 11)

    # NOTE(jkoelker) Drop all other icmp6
    for icmp_type in (134, 135, 136, 137, 146, 147, 151, 152, 153):
        group.add({'icmp6': None},
                  {'icmp_type': icmp_type},
                  {'in_port': vif_ofport},
                  {'actions': 'drop'},
                  priority=priority + 10)

    return group


class VMFlowsBase(BaseMarshallingDomain):
    def __init__(self, table):
        self.flows_table = table

    @classmethod
    def is_multi_table(cls):
        return False

    @classmethod
    def generate(cls, dom_id, vif_id, queue_id, xenstore_data):
        '''
        @summary: Computes a virtual interface flows using the same code that
                  nova uses when a server is spinned up
        @param dom_id: the id assigned by Xen to the server
        @type dom_id: String
        @param vif_id: the id assigned by Xen to the virtual interface
        @type vif_id: String
        @param xenstore_data: data describing the hypervisor level environment
                              to which the virtual interface is plugged in,
                              such as MAC address, physical interface, etc
        @type xenstore_data: dictionary
        @return: a VMFlowsSingeTable object containing a virtual interface
                 flows
        @type image_ref: VMFlowsSingleTable
        '''
        flows_table_str = cls.main(dom_id, vif_id, queue_id, xenstore_data)
        return cls._tty_to_obj(flows_table_str)

    @classmethod
    def _tty_to_obj(cls, terminal_str):
        '''
        @summary: Deserializes a virtual interface flows obtained as output
                  from CLI commands such as ovs-ofctl
        @param terminal_str: flows obtained at the CLI level
        @type terminal_str: String
        @return: a VMFlowsBase instance containing a virtual interface
                 flows
        @type return: VMFlowsBase instance
        '''
        segment_exp = re.compile(r'(\w+)=?([\w:./-]+)?')
        action_exp = re.compile(r',(\w+):([\w:.-]+)')
        terminal_lines = terminal_str.splitlines()
        group = OvsFlowGroup()

        for line in terminal_lines:
            # add one flow from a line of input
            fragments = segment_exp.findall(line)
            action_fragments = action_exp.findall(line)
            flow = []
            actions = []
            for fragment in fragments:
                if not fragment[1]:
                    flow.append({fragment[0]: None})
                elif fragment[0] in ['duration', 'n_packets', 'n_bytes',
                                     'hard_age', 'idle_age', 'table']:
                    continue
                elif fragment[0] == 'actions':
                    key_value_list = fragment[1].split(':')
                    actions.append(OvsActionFragment(*key_value_list))
                    break
                else:
                    value = cls._normalize_address(fragment)
                    flow.append({fragment[0]: value})
            for fragment in action_fragments:
                actions.append(OvsActionFragment(*fragment))
            flow.append({'actions': OvsFlow(actions)})

            # we have all the fragments for this flow
            group.add(*flow)

        # we have all the flows for this interface
        return cls(group)

    @classmethod
    def _normalize_address(cls, fragment):
        '''
        @summary: Converts ipv4, ipv6 and mac addresses to a common format so
                  they can be compared reliably
        @param fragment: An open flow fragment that might contain ipv4, ipv6 or
                         mac address
        @type fragment: OvsFragment
        @return: an ipv4, ipv6 or mac address in the format provided by netaddr
        @type return: String
        '''
        if fragment[0] not in ['ipv6_src', 'dl_dst', 'nd_target']:
            return fragment[1]
        if fragment[0] == 'dl_dst':
            if '/' in fragment[1]:
                return fragment[1]
            else:
                return str(EUI(fragment[1]))
        return str(IPAddress(fragment[1]))

    def __str__(self):
        return '\n'.join([str(flow) for flow in self.flows_table])

    def __eq__(self, other):
        raise NotImplementedError()

    def __ne__(self, other):
        if not isinstance(other, VMFlowsBase):
            return NotImplemented
        self_copy = self._cleanup_duplicates(self.flows_table)
        other_copy = self._cleanup_duplicates(other.flows_table)
        self_ptr = 0
        while self_ptr < len(self_copy) and len(other_copy) > 0:
            for other_ptr in xrange(len(other_copy)):
                if self_copy[self_ptr] == other_copy[other_ptr]:
                    other_copy.pop(other_ptr)
                    self_copy.pop(self_ptr)
                    break
            else:
                self_ptr += 1
        if not self_copy and not other_copy:
            return ()
        else:
            return (self_copy, other_copy)

    def _cleanup_duplicates(self, flows_table):
        clean = []
        for flow in flows_table:
            for c in clean:
                if flow == c:
                    break
            else:
                clean.append(flow)
        return clean


class VMFlowsSingleTable(VMFlowsBase):
    @classmethod
    def main(cls, dom_id, vif_id, queue_id, xenstore_data):
        '''
        @summary: Calculates the flows for a Xen domain virtual interface
        @param dom_id: The domain's (VM) id assigned by Xen
        @type dom_id: String
        @param vif_id: The virtual interface id assigned by Xen
        @type vif_id: String
        @param queue_id: The id for the HTB queueing discipline to be used to
        control the quality of service for the virtual interface
        @type queue_id: String
        @param xenstore_data: Data from the domain Xen record that is used to
        calculate the flows
        @type xenstore_data: Dictionary
        @return: flows for the virtual interface
        @type return: String
        '''
        ovs = OvsFlowManager()
        mac = xenstore_data['mac'].lower()
        nw_vlan = xenstore_data['nw_vlan']
        vif_ofport = xenstore_data['vif_ofport']
        pif_ofport = xenstore_data['pif_ofport']
        ovs.add(get_broadcast_multicast_flows(dom_id, vif_id, vif_ofport))

        # if net_type in ('ipv4', 'all') and 'ips' in xenstore_data:
        if 'ips' in xenstore_data:
            for ip in xenstore_data['ips']:
                ovs.add(get_tenant_ipv4_flows(dom_id, vif_id, pif_ofport,
                                              mac, ip['ip'], vif_ofport,
                                              queue_id, nw_vlan))

        # if net_type in ('ipv6', 'all') and 'ip6s' in xenstore_data:
        if 'ip6s' in xenstore_data:
            link_local = get_ipv6_link_local(mac)
            ovs.add(get_tenant_ipv6_flows(dom_id, vif_id, pif_ofport,
                                          mac, link_local,
                                          vif_ofport, queue_id, nw_vlan))
            for ip in xenstore_data['ip6s']:
                ovs.add(get_tenant_ipv6_flows(dom_id, vif_id, pif_ofport,
                                              mac, ip['ip'], vif_ofport,
                                              queue_id, nw_vlan))

        return str(ovs)


class VMFlowsMultiTable(VMFlowsBase):
    @classmethod
    def is_multi_table(cls):
        return True

    @classmethod
    def main(cls, dom_id, vif_id, queue_id, xenstore_data):
        ovs = flows.OvsFlowManager()
        vm = dict(domid=dom_id)
        vif = dict(nova=dict(ips=xenstore_data.get('ips', []),
                             ip6s=xenstore_data.get('ip6s', [])),
                   MAC=xenstore_data['mac'].lower(),
                   device=vif_id,
                   ofport=xenstore_data['vif_ofport'])
        network = dict(ovs_bridge='dummy-variable')

        flows.get_pif = lambda *args: dict(
            ofport=xenstore_data['pif_ofport'],
            VLAN=xenstore_data['nw_vlan'],
            in_ofports=xenstore_data['pif_inofports'])
        flows_obj = flows.get_ovs_flows(ovs, vm, vif, network, queue_id)
        ret = str(flows_obj['dummy-variable'])

        # evict flows without cookies
        newret = ''
        for line in ret.split('\n'):
            if 'cookie' in line:
                newret += line + '\n'

        return newret


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print ' '.join(['usage: %s' % os.path.basename(sys.argv[0]),
                        '[online|offline|reset]',
                        'vif-domid-idx',
                        '[ipv4|ipv6|all]'])
        sys.exit(1)
    else:
        command, vif_raw, net_type = sys.argv[1:4]
        sys.exit(VMFlowsSingleTable.main(command, vif_raw, net_type))
