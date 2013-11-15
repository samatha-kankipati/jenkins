'''
Created on Jan 15, 2013

@author: leon0944
'''
import aiclib
from testrepo.common.testfixtures.networks import BaseNetworksFixture
from ccengine.common.decorators import attr
from ccengine.domain.types import NovaServerStatusTypes
from ccengine.common.constants.networks_constants import HTTPResponseCodes


class TestNVPData(BaseNetworksFixture):
    """Test Module for verifying network data in NVP"""

    @classmethod
    def setUpClass(cls):
        """Setting the nvp client to be used and number of servers"""
        super(TestNVPData, cls).setUpClass()
        cls.servers_num = 3
        if cls.nvp_provider:
            cls.nvp_client = cls.nvp_provider.aic_client
        else:
            cls.nvp_client = None

    @attr('smoke', 'positive', 'bug_fix')
    def test_network_delete(self):
        """Testing a network with no servers can be deleted and verifying
        the switch and switch ports are deleted from NVP"""

        servers, networks = self.helper.create_network_with_n_servers(
                                                            self.servers_num)
        #isolated network is the first element (then public and private)
        isolated_network = networks[0]

        #verify the expected virtual interfaces and switch ports were created
        for s in servers:
            interfaces = self.networks_provider.client.list_virtual_interfaces(
                                                                             s)
            self.assertEqual(interfaces.status_code,
                                        HTTPResponseCodes.LIST_INTERFACES,
                                        'Unable to get Virtual Interfaces')

            active_server = self.servers_provider.wait_for_server_status(s,
                                                NovaServerStatusTypes.ACTIVE)
            self.helper.check_virtual_interface_response(interfaces.entity,
                                                networks, active_server.entity)

        #double check switch and switch port data from nvp
        if self.run_nvp:
            lswitch = self.nvp_client.get_lswitch(isolated_network)
            lswitch_ports = self.nvp_client.list_lswitch_ports(
                isolated_network)
            self.assertEqual(lswitch['uuid'], isolated_network,
                'Unexpected switch uuid')
            self.assertEquals(len(lswitch_ports['results']), self.servers_num,
                'Switch ports should match the number of servers')
            self.assertEquals(lswitch_ports['result_count'], self.servers_num,
                'Unexpected switch ports result count')

        #delete servers
        not_deleted = self.servers_provider.delete_servers(servers)
        self.assertFalse(not_deleted, 'Unable to delete servers')

        #verify the servers and their switch ports were deleted
        if self.run_nvp:
            deleted_ports = self.nvp_client.list_lswitch_ports(
                isolated_network)
            self.assertFalse(deleted_ports['results'], 'Ports still present')
            self.assertEqual(deleted_ports['result_count'], 0,
                'Unexpected ports')

        #delete network and verify the switch is deleted from nvp
        delete_network = self.networks_provider.client.delete_network(
            isolated_network)
        self.assertEqual(delete_network.status_code,
            HTTPResponseCodes.DELETE_NETWORK, 'Unable to delete network')

        if self.run_nvp:
            self.assertRaises(aiclib.nvp.ResourceNotFound,
                self.nvp_client.get_lswitch, isolated_network)
