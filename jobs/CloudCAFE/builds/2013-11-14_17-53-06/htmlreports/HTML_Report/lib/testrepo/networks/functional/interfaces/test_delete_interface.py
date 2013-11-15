'''
Created on Nov 27, 2012

@author: leonardo.maycotte@rackspace.com
'''
from testrepo.common.testfixtures.networks import BaseNetworksFixture
from ccengine.common.decorators import attr
from ccengine.domain.types import NovaServerStatusTypes
from ccengine.common.constants.networks_constants import Constants


_OK_STATUS = [200, 202, 204]
_NOT_FOUND = 404
_SERVER_ERROR = 500


class TestVirtualInterfaceDelete(BaseNetworksFixture):
    """Test Module for the os_interfacesv2 virtual interface delete service"""

    public_id = Constants.PUBLIC_NETWORK_ID
    private_id = Constants.PRIVATE_NETWORK_ID

    @attr('positive')
    def test_server_with_one_isolated_network(self):
        """Testing a server that only has an isolated network"""

        server = self.helper.create_list_servers(1)
        delete_type = 'isolated'
        #waiting for the server to be ACTIVE
        wait_req = self.servers_provider.wait_for_server_status(server.id,
                                                NovaServerStatusTypes.ACTIVE)

        interfaces = self.networks_provider.client.list_virtual_interfaces(
                                                                    server.id)
        #check the virtual interface list call was done OK, 200 status
        self.assertIn(interfaces.status_code, _OK_STATUS, 'Unable to get '
                                                        'Virtual Interfaces')
        #check the virtual interfaces match the number of networks
        self.assertEqual(len(server.net_list), len(interfaces.entity),
                                            'Unexpected Virtual Interfaces')

        #delete the virtual interface
        vi_to_delete = self.helper.get_vi_id(interfaces.entity, delete_type)
        response = self.networks_provider.client.delete_virtual_interface(
                                                    server.id, vi_to_delete)

        #check the virtual interface delete call was done OK, 200 status
        self.assertIn(response.status_code, _OK_STATUS, 'Unable to delete '
                                                        'Virtual Interface')

        self.helper.check_virtual_interface_delete(server.id,
            server.net_list, vi_to_delete)

    @attr('positive')
    def test_server_with_one_public_network(self):
        """Testing a server that only has a public network"""

        server = self.helper.create_list_servers(0, [self.public_id])
        delete_type = 'public'
        #waiting for the server to be ACTIVE
        wait_req = self.servers_provider.wait_for_server_status(server.id,
                                                NovaServerStatusTypes.ACTIVE)

        interfaces = self.networks_provider.client.list_virtual_interfaces(
                                                                    server.id)
        #check the virtual interface list call was done OK, 200 status
        self.assertIn(interfaces.status_code, _OK_STATUS, 'Unable to get '
                                                        'Virtual Interfaces')
        #check the virtual interfaces match the number of networks
        self.assertEqual(len(server.net_list), len(interfaces.entity),
                                            'Unexpected Virtual Interfaces')

        #delete the virtual interface
        vi_to_delete = self.helper.get_vi_id(interfaces.entity, delete_type)
        response = self.networks_provider.client.delete_virtual_interface(
                                                    server.id, vi_to_delete)

        #check the virtual interface delete call was done OK, 200 status
        self.assertIn(response.status_code, _OK_STATUS, 'Unable to delete '
                                                        'Virtual Interface')

        self.helper.check_virtual_interface_delete(server.id,
            server.net_list, vi_to_delete)

    @attr('positive')
    def test_server_with_one_private_network(self):
        """Testing a server that only has a private network"""

        server = self.helper.create_list_servers(0, [self.private_id])
        delete_type = 'private'
        #waiting for the server to be ACTIVE
        wait_req = self.servers_provider.wait_for_server_status(server.id,
                                                NovaServerStatusTypes.ACTIVE)

        interfaces = self.networks_provider.client.list_virtual_interfaces(
                                                                    server.id)
        #check the virtual interface list call was done OK, 200 status
        self.assertIn(interfaces.status_code, _OK_STATUS, 'Unable to get '
                                                        'Virtual Interfaces')
        #check the virtual interfaces match the number of networks
        self.assertEqual(len(server.net_list), len(interfaces.entity),
                                            'Unexpected Virtual Interfaces')

        #delete the virtual interface
        vi_to_delete = self.helper.get_vi_id(interfaces.entity, delete_type)
        response = self.networks_provider.client.delete_virtual_interface(
                                                    server.id, vi_to_delete)

        #check the virtual interface delete call was done OK, 200 status
        self.assertIn(response.status_code, _OK_STATUS, 'Unable to delete '
                                                        'Virtual Interface')

        self.helper.check_virtual_interface_delete(server.id,
            server.net_list, vi_to_delete)

    @attr('positive')
    def test_server_with_iso_and_public(self):
        """Testing a server with isolated and public networks"""

        server = self.helper.create_list_servers(1, [self.public_id])
        delete_type = 'public'
        #waiting for the server to be ACTIVE
        wait_req = self.servers_provider.wait_for_server_status(server.id,
                                                NovaServerStatusTypes.ACTIVE)

        interfaces = self.networks_provider.client.list_virtual_interfaces(
                                                                    server.id)
        #check the virtual interface list call was done OK, 200 status
        self.assertIn(interfaces.status_code, _OK_STATUS, 'Unable to get '
                                                        'Virtual Interfaces')
        #check the virtual interfaces match the number of networks
        self.assertEqual(len(server.net_list), len(interfaces.entity),
                                            'Unexpected Virtual Interfaces')

        #delete the virtual interface
        vi_to_delete = self.helper.get_vi_id(interfaces.entity, delete_type)
        response = self.networks_provider.client.delete_virtual_interface(
                                                    server.id, vi_to_delete)

        #check the virtual interface delete call was done OK, 200 status
        self.assertIn(response.status_code, _OK_STATUS, 'Unable to delete '
                                                        'Virtual Interface')

        self.helper.check_virtual_interface_delete(server.id,
            server.net_list, vi_to_delete)

    @attr('positive')
    def test_server_with_iso_and_public_b(self):
        """Testing a server with isolated and public networks"""

        server = self.helper.create_list_servers(1, [self.public_id])
        delete_type = 'isolated'
        #waiting for the server to be ACTIVE
        wait_req = self.servers_provider.wait_for_server_status(server.id,
                                                NovaServerStatusTypes.ACTIVE)

        interfaces = self.networks_provider.client.list_virtual_interfaces(
                                                                    server.id)
        #check the virtual interface list call was done OK, 200 status
        self.assertIn(interfaces.status_code, _OK_STATUS, 'Unable to get '
                                                        'Virtual Interfaces')
        #check the virtual interfaces match the number of networks
        self.assertEqual(len(server.net_list), len(interfaces.entity),
                                            'Unexpected Virtual Interfaces')

        #delete the virtual interface
        vi_to_delete = self.helper.get_vi_id(interfaces.entity, delete_type)
        response = self.networks_provider.client.delete_virtual_interface(
                                                    server.id, vi_to_delete)

        #check the virtual interface delete call was done OK, 200 status
        self.assertIn(response.status_code, _OK_STATUS, 'Unable to delete '
                                                        'Virtual Interface')

        self.helper.check_virtual_interface_delete(server.id,
            server.net_list, vi_to_delete)

    @attr('positive')
    def test_server_with_iso_and_private(self):
        """Testing a server with isolated and private networks"""

        server = self.helper.create_list_servers(1, [self.private_id])
        delete_type = 'private'
        #waiting for the server to be ACTIVE
        wait_req = self.servers_provider.wait_for_server_status(server.id,
                                                NovaServerStatusTypes.ACTIVE)

        interfaces = self.networks_provider.client.list_virtual_interfaces(
                                                                    server.id)
        #check the virtual interface list call was done OK, 200 status
        self.assertIn(interfaces.status_code, _OK_STATUS, 'Unable to get '
                                                        'Virtual Interfaces')
        #check the virtual interfaces match the number of networks
        self.assertEqual(len(server.net_list), len(interfaces.entity),
                                            'Unexpected Virtual Interfaces')

        #delete the virtual interface
        vi_to_delete = self.helper.get_vi_id(interfaces.entity, delete_type)
        response = self.networks_provider.client.delete_virtual_interface(
                                                    server.id, vi_to_delete)

        #check the virtual interface delete call was done OK, 200 status
        self.assertIn(response.status_code, _OK_STATUS, 'Unable to delete '
                                                        'Virtual Interface')

        self.helper.check_virtual_interface_delete(server.id,
            server.net_list, vi_to_delete)

    @attr('positive')
    def test_server_with_iso_and_private_b(self):
        """Testing a server with isolated and private networks"""

        server = self.helper.create_list_servers(1, [self.private_id])
        delete_type = 'isolated'
        #waiting for the server to be ACTIVE
        wait_req = self.servers_provider.wait_for_server_status(server.id,
                                                NovaServerStatusTypes.ACTIVE)

        interfaces = self.networks_provider.client.list_virtual_interfaces(
                                                                    server.id)
        #check the virtual interface list call was done OK, 200 status
        self.assertIn(interfaces.status_code, _OK_STATUS, 'Unable to get '
                                                        'Virtual Interfaces')
        #check the virtual interfaces match the number of networks
        self.assertEqual(len(server.net_list), len(interfaces.entity),
                                            'Unexpected Virtual Interfaces')

        #delete the virtual interface
        vi_to_delete = self.helper.get_vi_id(interfaces.entity, delete_type)
        response = self.networks_provider.client.delete_virtual_interface(
                                                    server.id, vi_to_delete)

        #check the virtual interface delete call was done OK, 200 status
        self.assertIn(response.status_code, _OK_STATUS, 'Unable to delete '
                                                        'Virtual Interface')

        self.helper.check_virtual_interface_delete(server.id,
            server.net_list, vi_to_delete)

    @attr('smoke', 'positive')
    def test_server_with_iso_public_and_private(self):
        """Testing deleting ServiceNet VIF"""

        server_create = self.helper.create_list_servers(1, [self.private_id,
                                                            self.public_id])
        network_list = server_create.net_list
        delete_type = 'private'

        # Waiting for the server to be ACTIVE, and getting the entity object
        server = self.servers_provider.wait_for_server_status(server_create.id,
            NovaServerStatusTypes.ACTIVE).entity
        server.adminPass = server_create.adminPass
        interfaces = self.networks_provider.client.list_virtual_interfaces(
            server.id)

        # Check the virtual interface list call was done OK, 200 status
        self.assertIn(interfaces.status_code, _OK_STATUS, 'Unable to get '
                      'Virtual Interfaces')

        # Check the virtual interfaces match the number of networks
        self.assertEqual(len(network_list), len(interfaces.entity),
                         'Unexpected Virtual Interfaces')

        # Check the ServiceNet (Private) IPs are in the Server
        ip_list = self.helper.list_interface_ips(server, self.private_network)
        self.helper.assert_ifconfig(server=server, ips=ip_list)

        # Delete the virtual interface
        vi_to_delete = self.helper.get_vi_id(interfaces.entity, delete_type)
        response = self.networks_provider.client.delete_virtual_interface(
            server.id, vi_to_delete)

        # Check the virtual interface delete call was done OK, 200 status
        self.assertIn(response.status_code, _OK_STATUS, 'Unable to delete '
                                                        'Virtual Interface')

        self.helper.check_virtual_interface_delete(server.id, network_list,
                                                   vi_to_delete)

        # Check the ServiceNet (Private) IPs are gone from the Server
        self.helper.assert_ifconfig(server=server, ips=ip_list, find=False)

    @attr('smoke', 'positive')
    def test_server_with_iso_public_and_private_b(self):
        """Testing deleting Public VIF"""

        server_create = self.helper.create_list_servers(1, [self.private_id,
                                                            self.public_id])
        network_list = server_create.net_list
        delete_type = 'public'

        # Waiting for the server to be ACTIVE, and getting the entity object
        server = self.servers_provider.wait_for_server_status(server_create.id,
            NovaServerStatusTypes.ACTIVE).entity
        server.adminPass = server_create.adminPass
        interfaces = self.networks_provider.client.list_virtual_interfaces(
            server.id)

        # Check the virtual interface list call was done OK, 200 status
        self.assertIn(interfaces.status_code, _OK_STATUS, 'Unable to get '
                      'Virtual Interfaces')

        # Check the virtual interfaces match the number of networks
        self.assertEqual(len(network_list), len(interfaces.entity),
                         'Unexpected Virtual Interfaces')

        # Check the Public IPs are in the Server
        ip_list = self.helper.list_interface_ips(server, self.public_network)
        self.helper.assert_ifconfig(server=server, ips=ip_list)

        # Delete the virtual interface
        vi_to_delete = self.helper.get_vi_id(interfaces.entity, delete_type)
        response = self.networks_provider.client.delete_virtual_interface(
            server.id, vi_to_delete)

        # Check the virtual interface delete call was done OK, 200 status
        self.assertIn(response.status_code, _OK_STATUS, 'Unable to delete '
                                                        'Virtual Interface')

        self.helper.check_virtual_interface_delete(server.id, network_list,
                                                   vi_to_delete)

    @attr('smoke', 'positive')
    def test_server_with_iso_public_and_private_c(self):
        """Testing deleting Isolated VIF"""

        server_create = self.helper.create_list_servers(1, [self.private_id,
                                                            self.public_id])
        network_list = server_create.net_list
        delete_type = 'isolated'

        # Waiting for the server to be ACTIVE, and getting the entity object
        server = self.servers_provider.wait_for_server_status(server_create.id,
            NovaServerStatusTypes.ACTIVE).entity
        server.adminPass = server_create.adminPass
        interfaces = self.networks_provider.client.list_virtual_interfaces(
            server.id)

        # Check the virtual interface list call was done OK, 200 status
        self.assertIn(interfaces.status_code, _OK_STATUS, 'Unable to get '
                      'Virtual Interfaces')

        # Check the virtual interfaces match the number of networks
        self.assertEqual(len(network_list), len(interfaces.entity),
                         'Unexpected Virtual Interfaces')

        # Check the Isolated IPs are in the Server
        isolated_network = self.networks_provider.client.get_network(
            network_list[0]).entity
        ip_list = self.helper.list_interface_ips(server, isolated_network)
        self.helper.assert_ifconfig(server=server, ips=ip_list)

        # Delete the virtual interface
        vi_to_delete = self.helper.get_vi_id(interfaces.entity, delete_type)
        response = self.networks_provider.client.delete_virtual_interface(
            server.id, vi_to_delete)

        # Check the virtual interface delete call was done OK, 200 status
        self.assertIn(response.status_code, _OK_STATUS, 'Unable to delete '
                                                        'Virtual Interface')

        self.helper.check_virtual_interface_delete(server.id, network_list,
                                                   vi_to_delete)

        # Check the Isolated IPs are gone from the Server
        self.helper.assert_ifconfig(server=server, ips=ip_list, find=False)

    @attr('positive')
    def test_server_with_public_and_private(self):
        """Testing a server with public and private networks"""

        server = self.helper.create_list_servers(0,
                                            [self.private_id, self.public_id])
        delete_type = 'public'
        #waiting for the server to be ACTIVE
        wait_req = self.servers_provider.wait_for_server_status(server.id,
                                                NovaServerStatusTypes.ACTIVE)

        interfaces = self.networks_provider.client.list_virtual_interfaces(
                                                                    server.id)
        #check the virtual interface list call was done OK, 200 status
        self.assertIn(interfaces.status_code, _OK_STATUS, 'Unable to get '
                                                        'Virtual Interfaces')
        #check the virtual interfaces match the number of networks
        self.assertEqual(len(server.net_list), len(interfaces.entity),
                                            'Unexpected Virtual Interfaces')

        #delete the virtual interface
        vi_to_delete = self.helper.get_vi_id(interfaces.entity, delete_type)
        response = self.networks_provider.client.delete_virtual_interface(
                                                    server.id, vi_to_delete)

        #check the virtual interface delete call was done OK, 200 status
        self.assertIn(response.status_code, _OK_STATUS, 'Unable to delete '
                                                        'Virtual Interface')

        self.helper.check_virtual_interface_delete(server.id,
            server.net_list, vi_to_delete)

    @attr('positive')
    def test_server_with_public_and_private_b(self):
        """Testing a server with public and private networks"""

        server = self.helper.create_list_servers(0,
                                            [self.private_id, self.public_id])
        delete_type = 'private'
        #waiting for the server to be ACTIVE
        wait_req = self.servers_provider.wait_for_server_status(server.id,
                                                NovaServerStatusTypes.ACTIVE)

        interfaces = self.networks_provider.client.list_virtual_interfaces(
                                                                    server.id)
        #check the virtual interface list call was done OK, 200 status
        self.assertIn(interfaces.status_code, _OK_STATUS, 'Unable to get '
                                                        'Virtual Interfaces')
        #check the virtual interfaces match the number of networks
        self.assertEqual(len(server.net_list), len(interfaces.entity),
                                            'Unexpected Virtual Interfaces')

        #delete the virtual interface
        vi_to_delete = self.helper.get_vi_id(interfaces.entity, delete_type)
        response = self.networks_provider.client.delete_virtual_interface(
                                                    server.id, vi_to_delete)

        #check the virtual interface delete call was done OK, 200 status
        self.assertIn(response.status_code, _OK_STATUS, 'Unable to delete '
                                                        'Virtual Interface')

        self.helper.check_virtual_interface_delete(server.id,
            server.net_list, vi_to_delete)

    @attr('positive')
    def test_zserver_with_eight_isolated(self):
        """Testing a server with 8 isolated networks"""

        server = self.helper.create_list_servers(8)
        delete_type = 'isolated'
        #waiting for the server to be ACTIVE
        wait_req = self.servers_provider.wait_for_server_status(server.id,
                                                NovaServerStatusTypes.ACTIVE)

        interfaces = self.networks_provider.client.list_virtual_interfaces(
                                                                    server.id)
        #check the virtual interface list call was done OK, 200 status
        self.assertIn(interfaces.status_code, _OK_STATUS, 'Unable to get '
                                                        'Virtual Interfaces')
        #check the virtual interfaces match the number of networks
        self.assertEqual(len(server.net_list), len(interfaces.entity),
                                            'Unexpected Virtual Interfaces')

        #delete the virtual interface
        vi_to_delete = self.helper.get_vi_id(interfaces.entity, delete_type)
        response = self.networks_provider.client.delete_virtual_interface(
                                                    server.id, vi_to_delete)

        #check the virtual interface delete call was done OK, 200 status
        self.assertIn(response.status_code, _OK_STATUS, 'Unable to delete '
                                                        'Virtual Interface')

        self.helper.check_virtual_interface_delete(server.id,
            server.net_list, vi_to_delete)

    @attr('positive')
    def test_server_with_seven_isolated_and_public(self):
        """Testing a server with 7 isolated and public networks"""

        server = self.helper.create_list_servers(7, [self.public_id])
        delete_type = 'public'
        #waiting for the server to be ACTIVE
        wait_req = self.servers_provider.wait_for_server_status(server.id,
                                                NovaServerStatusTypes.ACTIVE)

        interfaces = self.networks_provider.client.list_virtual_interfaces(
                                                                    server.id)
        #check the virtual interface list call was done OK, 200 status
        self.assertIn(interfaces.status_code, _OK_STATUS, 'Unable to get '
                                                        'Virtual Interfaces')
        #check the virtual interfaces match the number of networks
        self.assertEqual(len(server.net_list), len(interfaces.entity),
                                            'Unexpected Virtual Interfaces')

        #delete the virtual interface
        vi_to_delete = self.helper.get_vi_id(interfaces.entity, delete_type)
        response = self.networks_provider.client.delete_virtual_interface(
                                                    server.id, vi_to_delete)

        #check the virtual interface delete call was done OK, 200 status
        self.assertIn(response.status_code, _OK_STATUS, 'Unable to delete '
                                                        'Virtual Interface')

        self.helper.check_virtual_interface_delete(server.id,
            server.net_list, vi_to_delete)

    @attr('positive')
    def test_server_with_seven_isolated_and_public_b(self):
        """Testing a server with 7 isolated and public networks"""

        server = self.helper.create_list_servers(7, [self.public_id])
        delete_type = 'isolated'
        #waiting for the server to be ACTIVE
        wait_req = self.servers_provider.wait_for_server_status(server.id,
                                                NovaServerStatusTypes.ACTIVE)

        interfaces = self.networks_provider.client.list_virtual_interfaces(
                                                                    server.id)
        #check the virtual interface list call was done OK, 200 status
        self.assertIn(interfaces.status_code, _OK_STATUS, 'Unable to get '
                                                        'Virtual Interfaces')
        #check the virtual interfaces match the number of networks
        self.assertEqual(len(server.net_list), len(interfaces.entity),
                                            'Unexpected Virtual Interfaces')

        #delete the virtual interface
        vi_to_delete = self.helper.get_vi_id(interfaces.entity, delete_type)
        response = self.networks_provider.client.delete_virtual_interface(
                                                    server.id, vi_to_delete)

        #check the virtual interface delete call was done OK, 200 status
        self.assertIn(response.status_code, _OK_STATUS, 'Unable to delete '
                                                        'Virtual Interface')

        self.helper.check_virtual_interface_delete(server.id,
            server.net_list, vi_to_delete)

    @attr('positive')
    def test_server_with_seven_isolated_and_private(self):
        """Testing a server with 7 isolated and private networks"""

        server = self.helper.create_list_servers(7, [self.private_id])
        delete_type = 'private'
        #waiting for the server to be ACTIVE
        wait_req = self.servers_provider.wait_for_server_status(server.id,
                                                NovaServerStatusTypes.ACTIVE)

        interfaces = self.networks_provider.client.list_virtual_interfaces(
                                                                    server.id)
        #check the virtual interface list call was done OK, 200 status
        self.assertIn(interfaces.status_code, _OK_STATUS, 'Unable to get '
                                                        'Virtual Interfaces')
        #check the virtual interfaces match the number of networks
        self.assertEqual(len(server.net_list), len(interfaces.entity),
                                            'Unexpected Virtual Interfaces')

        #delete the virtual interface
        vi_to_delete = self.helper.get_vi_id(interfaces.entity, delete_type)
        response = self.networks_provider.client.delete_virtual_interface(
                                                    server.id, vi_to_delete)

        #check the virtual interface delete call was done OK, 200 status
        self.assertIn(response.status_code, _OK_STATUS, 'Unable to delete '
                                                        'Virtual Interface')

        self.helper.check_virtual_interface_delete(server.id,
            server.net_list, vi_to_delete)

    @attr('positive')
    def test_server_with_seven_isolated_and_private_b(self):
        """Testing a server with 7 isolated and private networks"""

        server = self.helper.create_list_servers(7, [self.private_id])
        delete_type = 'isolated'
        #waiting for the server to be ACTIVE
        wait_req = self.servers_provider.wait_for_server_status(server.id,
                                                NovaServerStatusTypes.ACTIVE)

        interfaces = self.networks_provider.client.list_virtual_interfaces(
                                                                    server.id)
        #check the virtual interface list call was done OK, 200 status
        self.assertIn(interfaces.status_code, _OK_STATUS, 'Unable to get '
                                                        'Virtual Interfaces')
        #check the virtual interfaces match the number of networks
        self.assertEqual(len(server.net_list), len(interfaces.entity),
                                            'Unexpected Virtual Interfaces')

        #delete the virtual interface
        vi_to_delete = self.helper.get_vi_id(interfaces.entity, delete_type)
        response = self.networks_provider.client.delete_virtual_interface(
                                                    server.id, vi_to_delete)

        #check the virtual interface delete call was done OK, 200 status
        self.assertIn(response.status_code, _OK_STATUS, 'Unable to delete '
                                                        'Virtual Interface')

        self.helper.check_virtual_interface_delete(server.id,
            server.net_list, vi_to_delete)

    @attr('positive')
    def test_server_with_six_iso_public_and_private(self):
        """Testing a server with  isolated, public and private networks"""

        server = self.helper.create_list_servers(6,
                                            [self.private_id, self.public_id])
        delete_type = 'public'
        #waiting for the server to be ACTIVE
        wait_req = self.servers_provider.wait_for_server_status(server.id,
                                                NovaServerStatusTypes.ACTIVE)

        interfaces = self.networks_provider.client.list_virtual_interfaces(
                                                                    server.id)
        #check the virtual interface list call was done OK, 200 status
        self.assertIn(interfaces.status_code, _OK_STATUS, 'Unable to get '
                                                        'Virtual Interfaces')
        #check the virtual interfaces match the number of networks
        self.assertEqual(len(server.net_list), len(interfaces.entity),
                                            'Unexpected Virtual Interfaces')

        #delete the virtual interface
        vi_to_delete = self.helper.get_vi_id(interfaces.entity, delete_type)
        response = self.networks_provider.client.delete_virtual_interface(
                                                    server.id, vi_to_delete)

        #check the virtual interface delete call was done OK, 200 status
        self.assertIn(response.status_code, _OK_STATUS, 'Unable to delete '
                                                        'Virtual Interface')

        self.helper.check_virtual_interface_delete(server.id,
            server.net_list, vi_to_delete)

    @attr('positive')
    def test_server_with_six_iso_public_and_private_b(self):
        """Testing a server with  isolated, public and private networks"""

        server = self.helper.create_list_servers(6,
                                            [self.private_id, self.public_id])
        delete_type = 'private'
        #waiting for the server to be ACTIVE
        wait_req = self.servers_provider.wait_for_server_status(server.id,
                                                NovaServerStatusTypes.ACTIVE)

        interfaces = self.networks_provider.client.list_virtual_interfaces(
                                                                    server.id)
        #check the virtual interface list call was done OK, 200 status
        self.assertIn(interfaces.status_code, _OK_STATUS, 'Unable to get '
                                                        'Virtual Interfaces')
        #check the virtual interfaces match the number of networks
        self.assertEqual(len(server.net_list), len(interfaces.entity),
                                            'Unexpected Virtual Interfaces')

        #delete the virtual interface
        vi_to_delete = self.helper.get_vi_id(interfaces.entity, delete_type)
        response = self.networks_provider.client.delete_virtual_interface(
                                                    server.id, vi_to_delete)

        #check the virtual interface delete call was done OK, 200 status
        self.assertIn(response.status_code, _OK_STATUS, 'Unable to delete '
                                                        'Virtual Interface')

        self.helper.check_virtual_interface_delete(server.id,
            server.net_list, vi_to_delete)

    @attr('positive')
    def test_server_with_six_iso_public_and_private_c(self):
        """Testing a server with  isolated, public and private networks"""

        server = self.helper.create_list_servers(6,
                                            [self.private_id, self.public_id])
        delete_type = 'isolated'
        #waiting for the server to be ACTIVE
        wait_req = self.servers_provider.wait_for_server_status(server.id,
                                                NovaServerStatusTypes.ACTIVE)

        interfaces = self.networks_provider.client.list_virtual_interfaces(
                                                                    server.id)
        #check the virtual interface list call was done OK, 200 status
        self.assertIn(interfaces.status_code, _OK_STATUS, 'Unable to get '
                                                        'Virtual Interfaces')
        #check the virtual interfaces match the number of networks
        self.assertEqual(len(server.net_list), len(interfaces.entity),
                                            'Unexpected Virtual Interfaces')

        #delete the virtual interface
        vi_to_delete = self.helper.get_vi_id(interfaces.entity, delete_type)
        response = self.networks_provider.client.delete_virtual_interface(
                                                    server.id, vi_to_delete)

        #check the virtual interface delete call was done OK, 200 status
        self.assertIn(response.status_code, _OK_STATUS, 'Unable to delete '
                                                        'Virtual Interface')

        self.helper.check_virtual_interface_delete(server.id,
            server.net_list, vi_to_delete)

    @attr('negative')
    def test_server_without_networks(self):
        """(negative test) Testing on a server without networks"""

        server = self.helper.create_list_servers(0)
        #waiting for the server to be ACTIVE
        wait_req = self.servers_provider.wait_for_server_status(server.id,
                                                NovaServerStatusTypes.ACTIVE)

        interfaces = self.networks_provider.client.list_virtual_interfaces(
                                                                    server.id)
        #check the virtual interface list call was done OK, 200 status
        self.assertIn(interfaces.status_code, _OK_STATUS, 'Unable to get '
                                                        'Virtual Interfaces')
        #check the virtual interfaces match the number of networks
        self.assertEqual(len(server.net_list), len(interfaces.entity),
                                            'Unexpected Virtual Interfaces')

        #delete the virtual interface
        vi_to_delete = 'inexisting-virtual-interface'
        response = self.networks_provider.client.delete_virtual_interface(
                                                    server.id, vi_to_delete)

        #check the delete call returns an Internal Server Error, 500 status
        self.assertEqual(response.status_code, _SERVER_ERROR, 'Unexpected '
                                                        'HTTP response')

    @attr('negative')
    def test_server_without_wait(self):
        """Testing on a server without waiting for the server to be ACTIVE"""

        server = self.helper.create_build_list_server('withNetworks')
        delete_type = 'isolated'

        interfaces = self.networks_provider.client.list_virtual_interfaces(
                                                                    server.id)
        #check the virtual interface list call was done OK, 200 status
        self.assertIn(interfaces.status_code, _OK_STATUS, 'Unable to get '
                                                        'Virtual Interfaces')

        #unknown since the server might still be in BUILD status without it
        vi_to_delete = 'unknown'
        response = self.networks_provider.client.delete_virtual_interface(
                                                    server.id, vi_to_delete)

        #this test only checks that the call returns a valid HTTP response
        expected_http = []
        expected_http.extend(_OK_STATUS)
        expected_http.append(_SERVER_ERROR)
        expected_http.append(_NOT_FOUND)
        #check the virtual interface delete call was done OK, 200 status
        self.assertIn(response.status_code, expected_http, 'Unexpected '
                                                        'HTTP response')

    @attr('negative')
    def test_inexisting_server(self):
        """(negative test) Testing with a server that does not exists"""
        server_id = 'inexisting-server-id-8dc3f73ec851'
        interfaces = self.networks_provider.client.list_virtual_interfaces(
                                                                    server_id)
        self.assertEqual(interfaces.status_code, _NOT_FOUND, 'Unexpected '
                                                'HTTP status code on response')
        self.assertIsNone(interfaces.entity, 'Unexpected entity data')

        #delete the virtual interface
        vi_to_delete = 'inexisting-virtual-interface'
        response = self.networks_provider.client.delete_virtual_interface(
                                                    server_id, vi_to_delete)

        #check the delete call returns an Internal Server Error, 500 status
        self.assertEqual(response.status_code, _NOT_FOUND, 'Unexpected '
                                                        'HTTP response')

    @attr('negative')
    def test_with_incorrect_data(self):
        """(negative test) Testing with incorrect virtual interface ids"""

        server = self.helper.create_list_servers(8)
        delete_type = 'isolated'
        #waiting for the server to be ACTIVE
        wait_req = self.servers_provider.wait_for_server_status(server.id,
                                                NovaServerStatusTypes.ACTIVE)

        interfaces = self.networks_provider.client.list_virtual_interfaces(
                                                                    server.id)
        #check the virtual interface list call was done OK, 200 status
        self.assertIn(interfaces.status_code, _OK_STATUS, 'Unable to get '
                                                        'Virtual Interfaces')
        #check the virtual interfaces match the number of networks
        self.assertEqual(len(server.net_list), len(interfaces.entity),
                                            'Unexpected Virtual Interfaces')

        #try to delete with network id
        vi_to_delete = server.net_list[0]
        response = self.networks_provider.client.delete_virtual_interface(
                                                    server.id, vi_to_delete)

        #check the delete call returns an Internal Server Error, 500 status
        self.assertEqual(response.status_code, _SERVER_ERROR, 'Unexpected '
                                                        'HTTP response')

        server2 = self.helper.server017
        #waiting for the server to be ACTIVE
        wait_req2 = self.servers_provider.wait_for_server_status(server2.id,
                                                NovaServerStatusTypes.ACTIVE)

        interfaces2 = self.networks_provider.client.list_virtual_interfaces(
                                                                    server2.id)
        #check the virtual interface list call was done OK, 200 status
        self.assertIn(interfaces2.status_code, _OK_STATUS, 'Unable to get '
                                                        'Virtual Interfaces')
 
        #try to delete the virtual interface of server 2 on server 1
        vi_to_delete2 = self.helper.get_vi_id(interfaces2.entity, delete_type)
        response2 = self.networks_provider.client.delete_virtual_interface(
                                                    server.id, vi_to_delete2)
        #check the delete call returns an Internal Server Error, 500 status
        self.assertEqual(response2.status_code, _SERVER_ERROR, 'Unexpected '
                                                        'HTTP response')
