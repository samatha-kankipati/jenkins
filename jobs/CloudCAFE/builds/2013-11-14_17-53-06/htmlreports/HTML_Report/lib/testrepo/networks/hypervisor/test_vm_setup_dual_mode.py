'''
@summary: Tests at the hypervisor level that the Cloud Networks dual mode
          implementation is setting up correctly the networking for a VM.
@copyright: Copyright (c) 2013 Rackspace US, Inc.
@author: migu6046
'''

import re

from ccengine.common.decorators import attr
from ccengine.domain.networks.dual_mode_flows_table import DualModeFlowsTable
from ccengine.common.tools.datagen import rand_name
from ccengine.providers.hypervisor.hypervisor_api import HypervisorAPIProvider
from testrepo.common.testfixtures.networks import AdminFixture


class TestVMSetUpDualMode(AdminFixture):

    @classmethod
    def setUpClass(cls):
        super(TestVMSetUpDualMode, cls).setUpClass()
        cls.public_network_bridge = \
            cls.config.dual_mode_api.public_network_bridge
        cls.service_network_bridge = \
            cls.config.dual_mode_api.service_network_bridge

        # Create a server with VIFs in public, private
        network_ids = ([cls.public_network.id, cls.private_network.id])
        networks_dict = cls.networks_provider.get_server_network_dd(
            network_ids)
        server_name = rand_name('hypervisor-dual-mode-')
        cls.server = cls.servers_provider.create_active_server(
            name=server_name, networks=networks_dict).entity
        cls.servers_to_delete.append(cls.server.id)

        # Establish a session with the Xen hypervisor hosting the newly created
        # server
        cls.hypervisor_provider = HypervisorAPIProvider(
            cls.server.id,
            cls.admin_provider,
            cls.config,
            cls.fixture_log)

    @attr('smoke', 'positive')
    def test_server_exists_in_hypervisor(self):
        xenapi_vm_rec = \
            self.hypervisor_provider.get_xenapi_vm_record(
                self.server.id)
        self.assertTrue(xenapi_vm_rec)

    @attr('smoke', 'positive')
    def test_server_correct_vifs_bridges_setup(self):
        # get xenapi vif records and confirm server has 2 vifs in xen
        vm_vifs_records = \
            self.hypervisor_provider.get_xenapi_vifs_records(
                self.server.id)
        self.assertEquals(len(vm_vifs_records), 2)

        # get the server vifs and bridges setup in ovs and confirm we see the
        # expected bridges
        vifs_brs = self.hypervisor_provider.get_ovs_vifs_bridges(
            self.server.id)
        expected_bridges = [self.public_network_bridge,
                            self.service_network_bridge]
        expected_bridges.sort()
        found_bridges = vifs_brs.values()
        found_bridges.sort()
        self.assertEquals(expected_bridges, found_bridges)

        # confirm vifs are connected to correct bridges, both from the ovs and
        # xen perspectives
        vifs_ip_details = \
            self.hypervisor_provider.get_vifs_network_details(
                self.server.id)
        for vif, br in vifs_brs.items():
            if vif[-1] == '0':
                self.assertEquals(br, self.public_network_bridge)
                self.assertEquals(vifs_ip_details[vif]['label'], 'public')
            elif vif[-1] == '1':
                self.assertEquals(br, self.service_network_bridge)
                self.assertEquals(vifs_ip_details[vif]['label'], 'private')

    @attr('smoke', 'positive')
    def test_server_correct_mac_setup(self):
        vm_vifs_records = \
            self.hypervisor_provider.get_xenapi_vifs_records(
                self.server.id)

        # get the vifs record from the ovs database and confirm that their mac
        # addresses are the same as seen from xen
        vifs_macs = self.hypervisor_provider.get_ovs_vifs_macs(
            self.server.id)
        vif_fmt = vifs_macs.keys()[0][:-2] + '.%s'
        for vif_rec in vm_vifs_records:
            self.assertEquals(vif_rec['MAC'],
                              vifs_macs[vif_fmt % vif_rec['device']])

    @attr('smoke', 'positive')
    def test_server_correct_flows(self):
        # get the vm data from the hypervisor
        dual_mode_flows_table = DualModeFlowsTable(
            self.config.dual_mode_api.flows_type)
        vifs_flows = self.hypervisor_provider.get_vifs_flows(
            self.server.id, dual_mode_flows_table)
        vifs_net_details = self.hypervisor_provider.get_vifs_network_details(
            self.server.id)

        discrepancies_found = False
        # confirm vif0 and vif1 have the correct flows
        for vif in vifs_net_details:
            match = re.search(r'(\d+).(\d+)', vif)
            vif_id = match.group(2)
            if int(vif_id) < 2:
                # generate the expected flows object for vif
                dom_id = match.group(1)
                xenstore_data = vifs_net_details[vif]
                qos_queue_id = self.hypervisor_provider.get_vm_qos_queue_id(
                    self.server.id, xenstore_data, dual_mode_flows_table)
                expected_flows = dual_mode_flows_table.generate(
                    dom_id, vif_id, qos_queue_id, xenstore_data)
                # compare actual and expected flows and report discrepancies
                not_equal = expected_flows != vifs_flows[vif]
                if not_equal:
                    discrepancies_found = True
                    self.fixture_log.error(
                        'Discrepancies in expected flows for: {}'.format(vif))
                    for fl in not_equal[0]:
                        self.fixture_log.error(fl)
                    self.fixture_log.error(
                        'Discrepancies in actual flows for: {}'.format(vif))
                    for fl in not_equal[1]:
                        self.fixture_log.error(fl)

        if discrepancies_found:
            self.fail()
