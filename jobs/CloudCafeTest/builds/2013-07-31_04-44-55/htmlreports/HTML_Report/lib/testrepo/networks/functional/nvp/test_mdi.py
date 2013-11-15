'''
Created on Jan 23, 2013

@author: leon0944
'''
import time
import collections
from ccengine.common.tools import datatools
from testrepo.common.testfixtures.networks import NetworksMDIFixture
from ccengine.common.decorators import attr
from ccengine.domain.types import NovaServerStatusTypes


class TestMDI(NetworksMDIFixture):
    """Test Module for verifying MDI network data in NVP (MDI functionality
    only available in the new networks environment for now"""

    @attr('mdi')
    def test_switch(self):
        """Testing NVP switch with MDI functionality"""
        networks = self.helper.create_n_networks(2)
        self.assertEqual(len(networks), 2, 'Unable to create test networks')

        # get networks data cidr, id, label
        net01 = self.networks_provider.client.get_network(networks[0]).entity
        self.assertIsNotNone(net01, 'Unable to get network data')
        self.assertEqual(net01.id, networks[0], 'Unexpected Network ID')
        net02 = self.networks_provider.client.get_network(networks[1]).entity
        self.assertIsNotNone(net02, 'Unable to get network data')
        self.assertEqual(net02.id, networks[1], 'Unexpected Network ID')

        self.assert_switches(net01)
        self.assert_switches(net02)

    @attr('mdi')
    def test_switch_port(self):
        """Testing the MDI switch port"""
        servers, networks = self.helper.create_network_with_n_servers(1)
        # wait for server to be active for vif
        self.servers_provider.wait_for_server_status(servers[0],
                                                NovaServerStatusTypes.ACTIVE)

        net01 = self.networks_provider.client.get_network(networks[0]).entity
        interface = self.networks_provider.get_interface(servers[0],
                                                         networks[0])

        # Get switch id for switch port query
        switch_01 = self.cell_01.list_lswitches(tag=networks[0])
        switch_02 = self.cell_02.list_lswitches(tag=networks[0])
        switch_01_id = switch_01['results'][0]['uuid']
        switch_02_id = switch_02['results'][0]['uuid']

        # Get the switch ports, wait a little for the inter connection
        ports_01 = self.cell_01.list_lswitch_ports(switch_01_id,
                                                   relation=self.port_relation)
        ports_02 = self.cell_02.list_lswitch_ports(switch_02_id,
                                                   relation=self.port_relation)

        # VIF switch port by default is expected to be in Cell0002
        if self.primary == 'cell_01':
            self.assert_switches(net01, 2, 1)
            self.assertEqual(ports_01['result_count'], 2, 'Unexpected switch '
                                                          'count in Cell 0001')
            self.assertEqual(ports_02['result_count'], 1, 'Unexpected switch '
                                                          'count in Cell 0002')
            # expected virtual interface port
            vif = ports_01['results'][1]
            vif_switch = switch_01
        else:
            self.assert_switches(net01, 1, 2)
            self.assertEqual(ports_01['result_count'], 1, 'Unexpected switch '
                                                          'count in Cell 0001')
            self.assertEqual(ports_02['result_count'], 2, 'Unexpected switch '
                                                          'count in Cell 0002')
            # expected virtual interface port
            vif = ports_02['results'][1]
            vif_switch = switch_02

        # Check mdi ports in each switch, expected as portno 1 and first item
        mdi_01 = ports_01['results'][0]
        mdi_02 = ports_02['results'][0]

        # The Interconnect Context ID of the Multi-Domain Gateway Service
        # should be the same in both cell switches
        if 'LogicalPortAttachment' in self.port_relation:
            msg = '{0} MDI Switch Port not set in expected time, missing '\
                  'Interconnect Context ID'

            icc_set_01 = 'interconnect_context_id' in mdi_01['_relations']\
                                                      ['LogicalPortAttachment']
            icc_set_02 = 'interconnect_context_id' in mdi_02['_relations']\
                                                      ['LogicalPortAttachment']
            self.assertTrue(icc_set_01, msg.format('cell0001'))
            self.assertTrue(icc_set_02, msg.format('cell0002'))

            if icc_set_01:
                icc_id_01 = mdi_01['_relations']['LogicalPortAttachment']\
                                                    ['interconnect_context_id']
            else:
                icc_id_01 = msg.format('cell0001')
            if icc_set_02:
                icc_id_02 = mdi_02['_relations']['LogicalPortAttachment']\
                                                    ['interconnect_context_id']
            else:
                icc_id_02 = msg.format('cell0002')
            self.assertEqual(icc_id_01, icc_id_02)

        self.assert_mdi_port(mdi_01, switch_01, net01)
        self.assert_mdi_port(mdi_02, switch_02, net01)

        # Check vif port
        self.assert_vif_port(vif, vif_switch, net01, interface)

    def assert_vif_port(self, vif, switch, network, interface):
        """Asserts MDI Switch Port in a Switch"""
        switch_id = switch['results'][0]['uuid']
        zone_uuid = switch['results'][0]['transport_zones'][0]['zone_uuid']
        port_id = vif['uuid']
        vif_uuid = interface.id

        port_type = 'VifAttachment'
        port_num = 2

        nvp_data = datatools.convert_unicode_to_str(vif)

        switch_config = dict(tenant_id=self.tenant_id, switch_id=switch_id,
                        network_id=network.id, network_label=network.label,
                        zone_uuid=zone_uuid)

        att_config = dict(switch_id=switch_id, port_id=port_id, type=port_type,
                     vif_uuid=vif_uuid)

        port_data = self.nvp_provider.PortData(port_id, switch_id, port_num,
                    self.port_relation, switch_config, att_config)
        tags = self.nvp_provider.Tag('os_tid', self.tenant_id)
        port_data.tags = [tags.get_dict()]
        vif_data = port_data.get_dict()

        for key in vif_data.keys():
            if isinstance(vif_data[key], collections.Iterable):
                self.assertItemsEqual(vif_data[key], nvp_data[key], \
                    'Unexpected switch data; expected: %s, received: %s' \
                    % (vif_data[key], nvp_data[key]))
            else:
                self.assertEqual(vif_data[key], nvp_data[key], \
                    'Unexpected switch data; expected: %s, received: %s' \
                    % (vif_data[key], nvp_data[key]))

    def assert_mdi_port(self, mdi, switch, network):
        """Asserts MDI Switch Port in a Switch"""
        switch_id = switch['results'][0]['uuid']
        zone_uuid = switch['results'][0]['transport_zones'][0]['zone_uuid']
        port_id = mdi['uuid']
        interconnect_context_id = mdi['_relations']['LogicalPortAttachment']\
                                                    ['interconnect_context_id']
        domain_gateway_service_uuid = mdi['_relations']\
                       ['LogicalPortAttachment']['domain_gateway_service_uuid']
        port_type = 'DomainGatewayAttachment'
        port_num = 1

        nvp_data = datatools.convert_unicode_to_str(mdi)

        switch_config = dict(tenant_id=self.tenant_id, switch_id=switch_id,
                        network_id=network.id, network_label=network.label,
                        zone_uuid=zone_uuid)

        att_config = dict(switch_id=switch_id, port_id=port_id, type=port_type,
                     domain_gateway_service_uuid=domain_gateway_service_uuid,
                     interconnect_context_id=interconnect_context_id)

        mdi_data = self.nvp_provider.PortData(port_id, switch_id, port_num,
                    self.port_relation, switch_config, att_config).get_dict()

        for key in mdi_data.keys():
            if isinstance(mdi_data[key], collections.Iterable):
                self.assertItemsEqual(mdi_data[key], nvp_data[key], \
                    'Unexpected switch data; expected: %s, received: %s' \
                    % (mdi_data[key], nvp_data[key]))
            else:
                self.assertEqual(mdi_data[key], nvp_data[key], \
                    'Unexpected switch data; expected: %s, received: %s' \
                    % (mdi_data[key], nvp_data[key]))

    def assert_switches(self, network, cell_one_ports=0, cell_two_ports=0):
        """Asserts Network NVP Switches in both Cells"""

        # Get switch data from Cell 1 & 2
        switch_01 = self.cell_01.list_lswitches(tag=network.id, \
                                               relation=self.switch_relation)
        switch_02 = self.cell_02.list_lswitches(tag=network.id, \
                                               relation=self.switch_relation)

        # verify there is only one switch per cell
        self.assertEqual(switch_01['result_count'], 1, 'Unexpected switch '
                                                        'count in Cell 0001')
        self.assertEqual(switch_02['result_count'], 1, 'Unexpected switch '
                                                        'count in Cell 0002')

        # NVP switch data
        nvp_data_01 = datatools.convert_unicode_to_str(switch_01['results'][0])
        nvp_data_02 = datatools.convert_unicode_to_str(switch_02['results'][0])

        # expected - dynamic switch data in both cells
        switch_01_id = nvp_data_01['uuid']
        switch_02_id = nvp_data_02['uuid']

        # switch id expected to be different from network id and unique by cell
        self.assertNotEqual(switch_01_id, switch_02_id)
        self.assertNotEqual(switch_01_id, network.id)
        self.assertNotEqual(switch_02_id, network.id)

        zone_uuid_01 = nvp_data_01['transport_zones'][0]['zone_uuid']
        zone_uuid_02 = nvp_data_02['transport_zones'][0]['zone_uuid']

        cell01_data = self.nvp_provider.SwitchData(self.tenant_id,
                                                   switch_01_id, network.id,
                                                   network.label, zone_uuid_01,
                                                   self.switch_relation)

        cell02_data = self.nvp_provider.SwitchData(self.tenant_id,
                                                   switch_02_id, network.id,
                                                   network.label, zone_uuid_02,
                                                   self.switch_relation)
        # creating expected switch data objects
        if cell_one_ports != 0:
            rel = self.nvp_provider.Relations(switch_01_id,
                                              self.switch_relation)
            lss = self.nvp_provider.LogicalSwitchStatus(switch_01_id)
            lss.lport_count = cell_one_ports
            lss.lport_fabric_up_count = cell_one_ports
            lss.lport_admin_up_count = cell_one_ports
            lss.lport_link_up_count = cell_one_ports
            rel.LogicalSwitchStatus = lss.get_dict()
            cell01_data._relations = rel.get_dict()

        if cell_two_ports != 0:
            rel = self.nvp_provider.Relations(switch_02_id,
                                              self.switch_relation)
            lss = self.nvp_provider.LogicalSwitchStatus(switch_02_id)
            lss.lport_count = cell_two_ports
            lss.lport_fabric_up_count = cell_two_ports
            lss.lport_admin_up_count = cell_two_ports
            lss.lport_link_up_count = cell_two_ports
            rel.LogicalSwitchStatus = lss.get_dict()
            cell02_data._relations = rel.get_dict()

        expected_data_01 = cell01_data.get_dict()
        expected_data_02 = cell02_data.get_dict()

        for key in expected_data_01.keys():
            if isinstance(expected_data_01[key], collections.Iterable):
                self.assertItemsEqual(expected_data_01[key], nvp_data_01[key],
                    'Unexpected switch data; expected: %s, received: %s' \
                    % (expected_data_01[key], nvp_data_01[key]))
            else:
                self.assertEqual(expected_data_01[key], nvp_data_01[key],
                    'Unexpected switch data; expected: %s, received: %s' \
                    % (expected_data_01[key], nvp_data_01[key]))

        for key in expected_data_02.keys():
            if isinstance(expected_data_02[key], collections.Iterable):
                self.assertItemsEqual(expected_data_02[key], nvp_data_02[key],
                    'Unexpected switch data; expected: %s, received: %s' \
                    % (expected_data_02[key], nvp_data_02[key]))
            else:
                self.assertEqual(expected_data_02[key], nvp_data_02[key],
                    'Unexpected switch data; expected: %s, received: %s' \
                    % (expected_data_02[key], nvp_data_02[key]))
