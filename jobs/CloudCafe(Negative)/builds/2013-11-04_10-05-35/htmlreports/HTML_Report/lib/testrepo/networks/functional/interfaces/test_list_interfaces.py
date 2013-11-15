'''
Created on Nov 12, 2012

@author: leonardo.maycotte@rackspace.com
'''
from testrepo.common.testfixtures.networks import BaseNetworksFixture
from ccengine.common.connectors.ssh import SSHConnector
import ccengine.common.tools.datagen as datagen
from ccengine.common.decorators import attr
from ccengine.domain.types import NovaServerStatusTypes
from ccengine.common.constants.networks_constants import Constants


_OK_STATUS = [200, 202, 204]
_NOT_FOUND = 404


class TestVirtualInterfaceList(BaseNetworksFixture):
    """Test Module for the os_interfacesv2 virtual interface list service"""
    public_id = Constants.PUBLIC_NETWORK_ID
    private_id = Constants.PRIVATE_NETWORK_ID

    @attr('positive')
    def test_server_with_one_isolated_network(self):
        """Testing a server that only has an isolated network"""

        server = self.helper.create_list_servers(1)
        #waiting for the server to be ACTIVE
        wait_req = self.servers_provider.wait_for_server_status(server.id,
                                                NovaServerStatusTypes.ACTIVE)

        interfaces = self.networks_provider.client.list_virtual_interfaces(
                                                                    server.id)
        #check the virtual interface list call was done OK
        self.assertIn(interfaces.status_code, _OK_STATUS, 'Unable to get '
                                                        'Virtual Interfaces')
        #check the virtual interfaces match the number of networks
        self.assertEqual(len(server.net_list), len(interfaces.entity),
                                            'Unexpected interface response')

        #check the virtual interface object params
        self.helper.check_virtual_interface_response(interfaces.entity,
                                                     server.net_list,
                                                     wait_req.entity)

    @attr('positive')
    def test_server_with_one_public_network(self):
        """Testing a server that only has a public network"""

        server = self.helper.create_list_servers(0, [self.public_id])
        #waiting for the server to be ACTIVE
        wait_req = self.servers_provider.wait_for_server_status(server.id,
                                                NovaServerStatusTypes.ACTIVE)

        interfaces = self.networks_provider.client.list_virtual_interfaces(
                                                                    server.id)
        #check the virtual interface list call was done OK
        self.assertIn(interfaces.status_code, _OK_STATUS, 'Unable to get '
                                                        'Virtual Interfaces')
        #check the virtual interfaces match the number of networks
        self.assertEqual(len(server.net_list), len(interfaces.entity),
                                            'Unexpected interface response')

        #check the virtual interface object params
        self.helper.check_virtual_interface_response(interfaces.entity,
                                                     server.net_list,
                                                     wait_req.entity)

    @attr('positive')
    def test_server_with_one_private_network(self):
        """Testing a server that only has a private network"""

        server = self.helper.create_list_servers(0, [self.private_id])
        #waiting for the server to be ACTIVE
        wait_req = self.servers_provider.wait_for_server_status(server.id,
                                                NovaServerStatusTypes.ACTIVE)

        interfaces = self.networks_provider.client.list_virtual_interfaces(
                                                                    server.id)
        #check the virtual interface list call was done OK
        self.assertIn(interfaces.status_code, _OK_STATUS, 'Unable to get '
                                                        'Virtual Interfaces')
        #check the virtual interfaces match the number of networks
        self.assertEqual(len(server.net_list), len(interfaces.entity),
                                            'Unexpected interface response')

        #check the virtual interface object params
        self.helper.check_virtual_interface_response(interfaces.entity,
                                                     server.net_list,
                                                     wait_req.entity)

    @attr('positive')
    def test_server_with_iso_and_public(self):
        """Testing a server with isolated and public networks"""

        server = self.helper.create_list_servers(1, [self.public_id])
        #waiting for the server to be ACTIVE
        wait_req = self.servers_provider.wait_for_server_status(server.id,
                                                NovaServerStatusTypes.ACTIVE)

        interfaces = self.networks_provider.client.list_virtual_interfaces(
                                                                    server.id)
        #check the virtual interface list call was done OK
        self.assertIn(interfaces.status_code, _OK_STATUS, 'Unable to get '
                                                        'Virtual Interfaces')
        #check the virtual interfaces match the number of networks
        self.assertEqual(len(server.net_list), len(interfaces.entity),
                                            'Unexpected interface response')

        #check the virtual interface object params
        self.helper.check_virtual_interface_response(interfaces.entity,
                                                     server.net_list,
                                                     wait_req.entity)

    @attr('positive')
    def test_server_with_iso_and_private(self):
        """Testing a server with isolated and private networks"""

        server = self.helper.create_list_servers(1, [self.private_id])
        #waiting for the server to be ACTIVE
        wait_req = self.servers_provider.wait_for_server_status(server.id,
                                                NovaServerStatusTypes.ACTIVE)

        interfaces = self.networks_provider.client.list_virtual_interfaces(
                                                                    server.id)
        #check the virtual interface list call was done OK
        self.assertIn(interfaces.status_code, _OK_STATUS, 'Unable to get '
                                                        'Virtual Interfaces')
        #check the virtual interfaces match the number of networks
        self.assertEqual(len(server.net_list), len(interfaces.entity),
                                            'Unexpected interface response')

        #check the virtual interface object params
        self.helper.check_virtual_interface_response(interfaces.entity,
                                                     server.net_list,
                                                     wait_req.entity)

    @attr('smoke', 'positive')
    def test_server_with_iso_public_and_private(self):
        """Testing a server with isolated, public and private networks"""

        server = self.helper.create_list_servers(1,
                                            [self.private_id, self.public_id])
        #waiting for the server to be ACTIVE
        wait_req = self.servers_provider.wait_for_server_status(server.id,
                                                NovaServerStatusTypes.ACTIVE)

        interfaces = self.networks_provider.client.list_virtual_interfaces(
                                                                    server.id)
        #check the virtual interface list call was done OK
        self.assertIn(interfaces.status_code, _OK_STATUS, 'Unable to get '
                                                        'Virtual Interfaces')
        #check the virtual interfaces match the number of networks
        self.assertEqual(len(server.net_list), len(interfaces.entity),
                                            'Unexpected interface response')

        #check the virtual interface object params
        self.helper.check_virtual_interface_response(interfaces.entity,
                                                     server.net_list,
                                                     wait_req.entity)

    @attr('positive')
    def test_server_with_public_and_private(self):
        """Testing a server with public and private networks"""

        server = self.helper.create_list_servers(0,
                                            [self.private_id, self.public_id])
        #waiting for the server to be ACTIVE
        wait_req = self.servers_provider.wait_for_server_status(server.id,
                                                NovaServerStatusTypes.ACTIVE)

        interfaces = self.networks_provider.client.list_virtual_interfaces(
                                                                    server.id)
        #check the virtual interface list call was done OK
        self.assertIn(interfaces.status_code, _OK_STATUS, 'Unable to get '
                                                        'Virtual Interfaces')
        #check the virtual interfaces match the number of networks
        self.assertEqual(len(server.net_list), len(interfaces.entity),
                                            'Unexpected interface response')

        #check the virtual interface object params
        self.helper.check_virtual_interface_response(interfaces.entity,
                                                     server.net_list,
                                                     wait_req.entity)

    @attr('positive')
    def test_zserver_with_eight_isolated(self):
        """Testing a server with 8 isolated networks"""

        server = self.helper.create_list_servers(8)
        #waiting for the server to be ACTIVE
        wait_req = self.servers_provider.wait_for_server_status(server.id,
                                                NovaServerStatusTypes.ACTIVE)

        interfaces = self.networks_provider.client.list_virtual_interfaces(
                                                                    server.id)
        #check the virtual interface list call was done OK
        self.assertIn(interfaces.status_code, _OK_STATUS, 'Unable to get '
                                                        'Virtual Interfaces')
        #check the virtual interfaces match the number of networks
        self.assertEqual(len(server.net_list), len(interfaces.entity),
                                            'Unexpected interface response')

        #check the virtual interface object params
        self.helper.check_virtual_interface_response(interfaces.entity,
                                                     server.net_list,
                                                     wait_req.entity)

    @attr('positive')
    def test_server_with_seven_isolated_and_public(self):
        """Testing a server with 7 isolated and public networks"""

        server = self.helper.create_list_servers(7, [self.public_id])
        #waiting for the server to be ACTIVE
        wait_req = self.servers_provider.wait_for_server_status(server.id,
                                                NovaServerStatusTypes.ACTIVE)

        interfaces = self.networks_provider.client.list_virtual_interfaces(
                                                                    server.id)
        #check the virtual interface list call was done OK
        self.assertIn(interfaces.status_code, _OK_STATUS, 'Unable to get '
                                                        'Virtual Interfaces')
        #check the virtual interfaces match the number of networks
        self.assertEqual(len(server.net_list), len(interfaces.entity),
                                            'Unexpected interface response')

        #check the virtual interface object params
        self.helper.check_virtual_interface_response(interfaces.entity,
                                                     server.net_list,
                                                     wait_req.entity)

    @attr('positive')
    def test_server_with_seven_isolated_and_private(self):
        """Testing a server with 7 isolated and private networks"""

        server = self.helper.create_list_servers(7, [self.private_id])
        #waiting for the server to be ACTIVE
        wait_req = self.servers_provider.wait_for_server_status(server.id,
                                                NovaServerStatusTypes.ACTIVE)

        interfaces = self.networks_provider.client.list_virtual_interfaces(
                                                                    server.id)
        #check the virtual interface list call was done OK
        self.assertIn(interfaces.status_code, _OK_STATUS, 'Unable to get '
                                                        'Virtual Interfaces')
        #check the virtual interfaces match the number of networks
        self.assertEqual(len(server.net_list), len(interfaces.entity),
                                            'Unexpected interface response')

        #check the virtual interface object params
        self.helper.check_virtual_interface_response(interfaces.entity,
                                                     server.net_list,
                                                     wait_req.entity)

    @attr('positive')
    def test_server_with_six_iso_public_and_private(self):
        """Testing a server with  isolated, public and private networks"""

        server = self.helper.create_list_servers(6,
                                            [self.private_id, self.public_id])
        #waiting for the server to be ACTIVE
        wait_req = self.servers_provider.wait_for_server_status(server.id,
                                                NovaServerStatusTypes.ACTIVE)

        interfaces = self.networks_provider.client.list_virtual_interfaces(
                                                                    server.id)
        #check the virtual interface list call was done OK
        self.assertIn(interfaces.status_code, _OK_STATUS, 'Unable to get '
                                                        'Virtual Interfaces')
        #check the virtual interfaces match the number of networks
        self.assertEqual(len(server.net_list), len(interfaces.entity),
                                            'Unexpected interface response')

        #check the virtual interface object params
        self.helper.check_virtual_interface_response(interfaces.entity,
                                                     server.net_list,
                                                     wait_req.entity)

    @attr('negative')
    def test_server_without_networks(self):
        """(negative test) Testing on a server without networks"""

        server = self.helper.create_list_servers(0)
        #waiting for the server to be ACTIVE
        wait_req = self.servers_provider.wait_for_server_status(server.id,
                                                NovaServerStatusTypes.ACTIVE)

        interfaces = self.networks_provider.client.list_virtual_interfaces(
                                                                    server.id)
        #check the virtual interface list call was done OK
        self.assertIn(interfaces.status_code, _OK_STATUS, 'Unable to get '
                                                        'Virtual Interfaces')
        #check the virtual interfaces match the number of networks, 0
        self.assertEqual(len(server.net_list), len(interfaces.entity),
                                            'Unexpected interface response')

        #check the virtual interface entity object is an empty list
        self.assertFalse(interfaces.entity)

    @attr('negative')
    def test_server_without_wait(self):
        """(negative test) Testing on a server without waiting for the
        server to be ACTIVE (no data check since it may not be ready)"""

        server = self.helper.create_build_list_server()

        interfaces = self.networks_provider.client.list_virtual_interfaces(
                                                                    server.id)
        #check the virtual interface list call was done OK, 200 status
        self.assertIn(interfaces.status_code, _OK_STATUS, 'Unable to get '
                                                        'Virtual Interfaces')
        server = self.helper.create_build_list_server(1)

        interfaces = self.networks_provider.client.list_virtual_interfaces(
                                                                    server.id)
        #check the call was done OK, 200 status
        self.assertIn(interfaces.status_code, _OK_STATUS, 'Unable to get '
                                                        'Virtual Interfaces')

    @attr('negative')
    def test_inexisting_server(self):
        """(negative test) Testing with a server that does not exists"""
        interfaces = self.networks_provider.client.list_virtual_interfaces(
                                        'inexisting-server-id-8dc3f73ec851')
        self.assertEqual(interfaces.status_code, _NOT_FOUND, 'Unexpected '
                                                'HTTP status code on response')
        self.assertIsNone(interfaces.entity, 'Unexpected entity data')

        #testing with a missing server id
        interfaces = self.networks_provider.client.list_virtual_interfaces('')
        self.assertEqual(interfaces.status_code, _NOT_FOUND, 'Unexpected '
                                                'HTTP status code on response')
        self.assertIsNone(interfaces.entity, 'Unexpected entity data')
