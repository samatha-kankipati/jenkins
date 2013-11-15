import ConfigParser
import json
import re
import StringIO
import XenAPI

from ccengine.common.connectors.ssh import SSHConnector
from ccengine.domain.networks import utils
from ccengine.providers.base_provider import BaseProvider


class HypervisorAPIProvider(BaseProvider):
    '''
    @summary: Enable users to interact with the hypervisor hosting a nova
              server. The user only needs to provide the server uuid or other
              data readily available from the nova API
    @note: Provides access to data in Xenapi, Open vSwitch (ovs) or other
           components running on the hypervisor
    @note: Should be the primary interface to a test case or external tool.
    @copyright: Copyright (c) 2013 Rackspace US, Inc.
    '''

    def __init__(self, server_id, admin_provider, config, logger=None):
        '''
        @summary: Establishes a session with Xenapi in a hypervisor. It also
                  establishes a ssh session with the same hypervisor
        @param server_id: The nova id of the server hosted by the hypervisors
                          we are establishing a connection with
        @type server_id: String
        @param admin_provider: a CloudCAFE provider for the nova admin API
        @type admin_provider: CloudCAFE provider
        @param config: The configuration oprtions used for this test
        @type config: String
        @param logger: The logger for this tests
        @type logger: String
        '''
        super(HypervisorAPIProvider, self).__init__()

        # Obtain Xenapi end point, Xenapi access credentials and hypervisor ip
        # address
        compute_ip = self._get_compute_ip(server_id, admin_provider, config)
        self.ssh_compute = SSHConnector(compute_ip,
                                        config.admin_api.admin_username,
                                        config.admin_api.admin_password,
                                        port=314)
        cmd_base = 'sudo cat /etc/nova/nova.conf | grep {0}'
        xenapi_url = self.ssh_compute.exec_command(
            cmd_base.format('"xenapi_connection_url"')).strip()
        xenapi_url = xenapi_url[xenapi_url.index('=') + 1:]
        xenapi_username = self.ssh_compute.exec_command(
            cmd_base.format('"xenapi_connection_username"')).strip()
        xenapi_username = xenapi_username[xenapi_username.index('=') + 1:]
        xenapi_password = self.ssh_compute.exec_command(
            cmd_base.format('"xenapi_connection_password"')).strip()
        xenapi_password = xenapi_password[xenapi_password.index('=') + 1:]
        match = re.search(r'\d+.\d+.\d+.\d+', xenapi_url)
        hypervisor_ip = match.group()

        # Create xenapi session and ssh session with hypervisor
        self.xenapi_session = XenAPI.Session(xenapi_url)
        self.xenapi_session.xenapi.login_with_password(xenapi_username,
                                                       xenapi_password)
        self.ssh_hypervisor = SSHConnector(hypervisor_ip, xenapi_username,
                                           xenapi_password)

    def _get_compute_ip(self, server_id, admin_provider, config):
        msg = "object has no attribute 'OS-EXT-SRV-ATTR:host'"
        try:
            compute_ip = \
                admin_provider.get_compute_node_ip_for_server(server_id)
        except AttributeError as e:
            if msg not in e.message:
                raise e
            ssh_scheduler = SSHConnector(
                config.dual_mode_api.nova_scheduler_ip,
                config.admin_api.admin_username,
                config.admin_api.admin_password,
                port=314)
            cmd_base = "cat /var/log/nova/nova-scheduler.log | {0}"
            cmd_base = cmd_base.format("grep --color 'for instance {0}'")
            raw_response = ssh_scheduler.exec_command(
                cmd_base.format(server_id)).strip()
            match = re.search(r'\d+-\d+-\d+-\d+', raw_response)
            compute_ip = re.sub('-', '.', match.group())
        return compute_ip

    def get_xenapi_vm_record(self, server_id):
        '''
        @summary: Retrieves from the Xenapi database the domain data for a
                  given nova server instance
        @server_id: The server instance nova id
        @type compute_ip: String
        @return: The domain data retrived from Xenapi's database
        @type return: Dictionary
        '''
        return self._get_xenapi_vm_record(server_id)[1]

    def _get_xenapi_vm_record(self, server_id):
        all_vms = self.xenapi_session.xenapi.VM.get_all()
        for vm in all_vms:
            record = self.xenapi_session.xenapi.VM.get_record(vm)
            if record['name_label'][len('instance-'):] == server_id:
                    return (vm, record)
        return (None, None)

    def get_xenapi_vifs_records(self, server_id):
        '''
        @summary: Retrieves from the Xenapi database the records for a nova
                  server instance virtual interfaces
        @server_id: The server instance nova id
        @type compute_ip: String
        @return: The the Xenapi virtual interfaces records
        @type return: List
        '''
        vm_opaque_ref, vm_record = self._get_xenapi_vm_record(server_id)
        all_vifs = self.xenapi_session.xenapi.VIF.get_all()
        found_vifs = []
        for vif in all_vifs:
            record = self.xenapi_session.xenapi.VIF.get_record(vif)
            if record['VM'] == vm_opaque_ref:
                found_vifs.append(record)
        return found_vifs

    def get_ovs_vifs_bridges(self, server_id):
        '''
        @summary: Retrieves from openVswitch the bridges where a virtual server
                  instance virtual interfaces are plugged in
        @server_id: The server instance nova id
        @type compute_ip: String
        @return: The virtual interfaces -> bridges associations
        @type return: Dictionary
        '''
        vifs_bridges = {}
        vm_opaque_ref, vm_record = self._get_xenapi_vm_record(server_id)
        # the name of the server vifs, as seen from ovs, should have the format
        # 'vif<domid>.n', where domid is the domain (vm is xen parlance) id
        # and n is the vif's number
        vif_prefix = "vif{0}.".format(vm_record['domid'])
        bridges = self.ssh_hypervisor.exec_command(
            'ovs-vsctl list-br').splitlines()
        for br in bridges:
            vifs = self.ssh_hypervisor.exec_command(
                'ovs-vsctl list-ifaces {0}'.format(br)).splitlines()
            for vif in vifs:
                if vif_prefix in vif:
                    vifs_bridges[vif] = self.ssh_hypervisor.exec_command(
                        'ovs-vsctl br-to-parent {0}'.format(br)).strip()
        return vifs_bridges

    def get_ovs_vifs_macs(self, server_id):
        '''
        @summary: Retrieves from openVswitch the mac addresses assigned to a
                  server virtual interfaces
        @server_id: The server instance nova id
        @type compute_ip: String
        @return: The virtual interfaces -> mac addresses associations
        @type return: Dictionary
        '''
        vifs_bridges = self.get_ovs_vifs_bridges(server_id)
        ovs_cmd = ('ovs-vsctl --columns=external_ids find interface '
                   'name="{0}"')
        mac_hdr = 'attached-mac="'
        mac_fmt = "FF:FF:FF:FF:FF:FF"
        vifs_macs = {}
        for vif in vifs_bridges.keys():
            vif_rec = self.ssh_hypervisor.exec_command(ovs_cmd.format(vif))
            mac_pos = vif_rec.index(mac_hdr) + len(mac_hdr)
            mac_add = vif_rec[mac_pos: mac_pos + len(mac_fmt)]
            vifs_macs[vif] = mac_add
        return vifs_macs

    def _get_config(self):
        contents = self.ssh_hypervisor.exec_command(
            "cat /opt/rackspace/host.conf")
        config = ConfigParser.SafeConfigParser()
        config.readfp(StringIO.StringIO(contents))
        return config

    def get_vifs_network_details(self, server_id):
        '''
        @summary: Retrieves from openVswitch and Xen the details associated
                  with a server virtual interfaces
        @server_id: The server instance nova id
        @type compute_ip: String
        @return: The virtual interfaces details
        @type return: Dictionary
        '''
        vifs_macs = self.get_ovs_vifs_macs(server_id)
        vif0 = vifs_macs.keys()[0]
        dom_id = vif0[3:vif0.index('.')]
        xenstore_cmd = ('xenstore-read '
                        '/local/domain/{0}/vm-data/networking/{1}')
        vif_details = {}
        for vif, mac in vifs_macs.items():
            stripped_mac = ''.join(mac.split(':')).upper()
            ip_details = self.ssh_hypervisor.exec_command(
                xenstore_cmd.format(dom_id, stripped_mac))

            vif_details[vif] = json.loads(ip_details.strip())
            if vif_details[vif]['label'] == 'public':
                label = 'publicnet'
            elif vif_details[vif]['label'] == 'private':
                label = 'servicenet'
            else:
                label = 'NVP'
            if label == 'publicnet' or label == 'servicenet':
                network = self.xenapi_session.xenapi.network.get_by_name_label(
                    label)[0]
                network_record = self.xenapi_session.xenapi.network.get_record(
                    network)
                utils.get_config = self._get_config
                if utils.host_network_flavor() == utils.BONDED:
                    nw_vlan = utils.network_vlans()[label]
                    phys_dev = 'bond0'
                    ingress = utils.patch_ports()[label][utils.INGRESS]
                    cmd = 'ovs-vsctl get Interface {0} ofport'.format(
                        ingress)
                    pif_ofport = self.ssh_hypervisor.exec_command(cmd).strip()
                else:
                    pif = network_record["PIFs"][0]
                    pif_record = self.xenapi_session.xenapi.PIF.get_record(pif)
                    phys_dev = pif_record["device"]
                    nw_vlan = pif_record["VLAN"]
                    pif_ofport = self.ssh_hypervisor.exec_command(
                        'ovs-vsctl get Interface {0} ofport'
                        .format(phys_dev)).strip()
                # nw_vlan == '-1' indicates no vlan tag
                if nw_vlan == '-1':
                    nw_vlan = None
                vif_ofport = self.ssh_hypervisor.exec_command(
                    'ovs-vsctl get Interface {0} ofport'.format(vif)).strip()
                pif_in_ofports = [pif_ofport]
                vif_details[vif]['phys_dev'] = phys_dev
                vif_details[vif]['nw_vlan'] = nw_vlan
                vif_details[vif]['vif_ofport'] = vif_ofport
                vif_details[vif]['pif_ofport'] = pif_ofport
                vif_details[vif]['pif_inofports'] = pif_in_ofports
        return vif_details

    def get_vifs_flows(self, server_id, dual_mode_flows_table):
        '''
        @summary: Retrieves from openVswitch the flows assigned to a server
                  virtual interfaces
        @server_id: The server instance nova id
        @param dual_mode_flows_table: A DualModeFlowsTable instance
        @type dual_mode_flows_table: DualModeFlowsTable instance
        @type compute_ip: String
        @return: The virtual interfaces flows
        @type return: Dictionary
        '''
        vifs_bridges = self.get_ovs_vifs_bridges(server_id)
        vifs_flows = {}
        ofctl_cmd = 'ovs-ofctl dump-flows {0} cookie={1:#x}/-1'
        for vif, br in vifs_bridges.items():
            dom_id = vif[len('vif'):]
            dom_id, vif_id = dom_id.split('.')
            flows_marker = self._get_flows_marker(dom_id, vif_id)
            flows = self.ssh_hypervisor.exec_command(
                ofctl_cmd.format(br, flows_marker))

            flows = flows[flows.index('\n') + 1:]
            flows_type_class = dual_mode_flows_table.get_flows_class()
            vifs_flows[vif] = flows_type_class.deserialize(flows, 'tty')
        return vifs_flows

    def _get_flows_marker(self, dom_id, vif_id):
        dom_id = int(dom_id)
        vif_id = int(vif_id) << 16
        return dom_id + vif_id

    def get_tunnel_net_data(self):
        '''
        @summary: Retrieves from openVswitch and xen the network details
                  associated with a hypervisor tunnel network
        @return: The tunnel network detail for the hypervisor
        @type return: Dictionary
        '''
        network = self.xenapi_session.xenapi.network.get_by_name_label(
            "tunnelnet")[0]
        try:
            network_record = self.xenapi_session.xenapi.network.get_record(
                network)
        except XenAPI.Failure:
            return {'network_uuid': ''}
        network_uuid = network_record["uuid"]
        bridge = network_record["bridge"]
        pif = network_record["PIFs"][0]
        pif_record = self.xenapi_session.xenapi.PIF.get_record(pif)
        phys_dev = pif_record["device"]
        nw_vlan = pif_record["VLAN"]

        pif_ofport = self.ssh_hypervisor.exec_command(
            'ovs-vsctl get Interface {0} ofport'.format(phys_dev)).strip()
        tnet_ofport = self.ssh_hypervisor.exec_command(
            'ovs-vsctl get Interface {0} ofport'.format(bridge)).strip()
        return {'network_uuid': network_uuid,
                'pif_ofport': pif_ofport,
                'nw_vlan': nw_vlan,
                'tnet_ofport': tnet_ofport}

    def get_vm_qos_queue_id(self, server_id, vif_details,
                            dual_mode_flows_table):
        '''
        @summary: Retrieves from openVswitch the quality of service queue id
                  assigned to a server
        @param server_id: The server instance nova id
        @type server_id: String
        @param vif_details: xenstore data for vif
        @type vif_details: Dictionary
        @param dual_mode_flows_table: A DualModeFlowsTable instance
        @type dual_mode_flows_table: DualModeFlowsTable instance
        @return: The queue id
        @type return: Integer
        '''
        _, vm_record = self._get_xenapi_vm_record(server_id)
        try:
            queue_id = vm_record['other_config']['qos_queue']
        except KeyError:
            return None

        if ':' in queue_id:
            queue_id = queue_id.split(':')[-1]
            try:
                queue_id = int(queue_id, 16) - 1
                flows_klass = dual_mode_flows_table.get_flows_class()
                if flows_klass.is_multi_table():
                    if vif_details['label'] == 'public':
                        queue_id += 0x1000
                    elif vif_details['label'] == 'private':
                        queue_id += 0x2000
            except TypeError:
                queue_id = None
        else:
            queue_id = None

        return queue_id

    def get_tc_qdisc(self, phys_dev):
        return self.ssh_hypervisor.exec_command(
            'tc qdisc show dev {0}'.format(phys_dev)).strip()

    def get_tc_class(self, phys_dev):
        return self.ssh_hypervisor.exec_command(
            'tc class show dev {0}'.format(phys_dev)).strip()

    def get_tc_filter(self, phys_dev):
        return self.ssh_hypervisor.exec_command(
            'tc filter show dev {0}'.format(phys_dev)).strip()

    def get_flavor_rxtx_base(self):
        cmd_base = 'sudo cat /etc/nova/nova.conf | grep {0}'
        rxtx_base = self.ssh_compute.exec_command(
            cmd_base.format('"rxtx_base"')).strip()
        if rxtx_base:
            return float(rxtx_base)
        else:
            return 1.0
