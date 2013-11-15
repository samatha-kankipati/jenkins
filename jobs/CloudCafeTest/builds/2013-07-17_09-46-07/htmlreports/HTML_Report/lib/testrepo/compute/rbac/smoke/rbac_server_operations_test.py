from testrepo.common.testfixtures.compute import RbacComputeFixture
from ccengine.common.decorators import attr
from ccengine.common.tools.datagen import rand_name
from ccengine.domain.configuration import AuthConfig
from ccengine.clients.compute.servers_api import ServerAPIClient
from ccengine.domain.types import NovaImageStatusTypes
from ccengine.common.exceptions.compute import Forbidden
from ccengine.domain.types import NovaServerStatusTypes
from ccengine.providers.configuration import MasterConfigProvider as _MCP
from ccengine.providers.compute.compute_api import ComputeAPIProvider \
                                                   as _ComputeAPIProvider


class RBACServerOperationsTest(RbacComputeFixture):

    @classmethod
    def setUpClass(cls):
        super(RBACServerOperationsTest, cls).setUpClass()
        # Creation of 1 servers needed for the tests
        active_server_response = cls.compute_provider.create_active_server()
        cls.server = active_server_response.entity
        cls.resources.add(cls.server.id,
                          cls.servers_client.delete_server)

    @classmethod
    def tearDownClass(cls):
        super(RBACServerOperationsTest, cls).tearDownClass()

    @attr(type='smoke', net='no')
    def test_update_server_with_admin_role(self):
        """Update of server with admin account should work"""
        updated_server_response = self.servers_client.update_server(
            self.server.id,
            name='upd_server',
            accessIPv4='67.23.10.132',
            accessIPv6='::babe:67.23.10.132')
        self.assertEqual(200, updated_server_response.status_code)
        
    @attr(type='smoke', net='no')
    def test_update_server_with_creator_role(self):
        """Update of server with creator account should work"""
        with self.assertRaises(Forbidden):
            updated_server_response = self.creator_servers_client.update_server(
                self.server.id,
                name='updated_server',
                accessIPv4='67.23.10.132',
                accessIPv6='::babe:67.23.10.132')
    
    @attr(type='smoke', net='no')
    def test_update_server_with_observer_role(self):
        """Update of server with observer account should not work"""
        with self.assertRaises(Forbidden):
            self.observer_servers_client.update_server(
                self.server.id,
                name='upd_server',
                accessIPv4='67.23.10.132',
                accessIPv6='::babe:67.23.10.132')
    
    @attr(type='smoke', net='no')
    def test_update_server_with_observer_role_get_details(self):
        """Update of server with observer account should not work"""
        with self.assertRaises(Forbidden):
            self.observer_servers_client.update_server(
                self.server.id,
                name='upd_server',
                accessIPv4='67.23.10.132',
                accessIPv6='::babe:67.23.10.132')
        
    @attr(type='smoke', net='no')
    def test_get_server_admin_user(self):
        """Get server via admin user"""
        server_info_response = self.servers_client.get_server(self.server.id)
        self.assertEqual(200, server_info_response.status_code)
    
    @attr(type='smoke', net='no')
    def test_get_server_creator_user(self):
        """Get server via creator user"""
        server_info_response = self.creator_servers_client.get_server(
            self.server.id)
        self.assertEqual(200, server_info_response.status_code)
    
    @attr(type='smoke', net='no')
    def test_get_server_observer_user(self):
        """Get server via observer user"""
        server_info_response = self.observer_servers_client.get_server(
            self.server.id)
        self.assertEqual(200, server_info_response.status_code)
    
    @attr(type='smoke', net='no')
    def test_delete_server_admin_user(self):
        """Delete server via admin user"""
        active_server_response = self.compute_provider.create_active_server()
        active_server = active_server_response.entity
        deleted_server_response = self.servers_client.delete_server(active_server.id)
        self.assertEqual(204, deleted_server_response.status_code,
                         msg='The delete call response was: %s'
                         % (deleted_server_response.status_code))
    
    @attr(type='smoke', net='no')
    def test_delete_server_creator_user(self):
        """Delete server via creator user should fail"""
        active_server_response = (
            self.compute_provider_for_creator_user.create_active_server())
        active_server = active_server_response.entity
        with self.assertRaises(Forbidden):
            self.creator_servers_client.delete_server(
                active_server.id)
    
    @attr(type='smoke', net='no')
    def test_delete_server_observer_user(self):
        """Delete server via observer user should fail"""
        active_server_response = (
            self.compute_provider_for_creator_user.create_active_server())
        active_server = active_server_response.entity
        with self.assertRaises(Forbidden):
            self.observer_servers_client.delete_server(
                active_server.id)
    
    @attr(type='smoke', net='yes')
    def test_list_addresses_admin_user(self):
        """List Server IPs with admin user"""
        addr_list = self.servers_client.list_addresses(self.server.id)
        actual_addresses = addr_list.entity
        self.assertTrue(actual_addresses is not None,
                        "List addresses did not return any addresses")
        self.assertEqual(200, addr_list.status_code)
        
    @attr(type='smoke', net='yes')
    def test_list_addresses_creator_user(self):
        """List Server IPs with creator user"""
        addr_list = self.creator_servers_client.list_addresses(self.server.id)
        actual_addresses = addr_list.entity
        self.assertTrue(actual_addresses is not None,
                        "List addresses did not return any addresses")
        self.assertEqual(200, addr_list.status_code)
    
    @attr(type='smoke', net='yes')
    def test_list_addresses_observer_user(self):
        """List Server IPs with observer user"""
        addr_list = self.observer_servers_client.list_addresses(self.server.id)
        actual_addresses = addr_list.entity
        self.assertTrue(actual_addresses is not None,
                        "List addresses did not return any addresses")
        self.assertEqual(200, addr_list.status_code)
        
    @attr(type='smoke', net='yes')
    def test_list_addresses_by_network_admin_user(self):
        """List Server IPs with admin user should pass"""
        addr_list = self.servers_client.list_addresses_by_network(
            self.server.id,
            'public')
        actual_addresses = addr_list.entity
        self.assertTrue(actual_addresses is not None,
                        "List addresses did not return any addresses")
        self.assertEqual(200, addr_list.status_code)
        
    @attr(type='smoke', net='yes')
    def test_list_addresses_by_network_creator_user(self):
        """List Server IPs with creator user should pass"""
        addr_list = self.creator_servers_client.list_addresses_by_network(
            self.server.id,
            'public')
        actual_addresses = addr_list.entity
        self.assertTrue(actual_addresses is not None,
                        "List addresses did not return any addresses")
        self.assertEqual(200, addr_list.status_code)
        
    @attr(type='smoke', net='yes')
    def test_list_addresses_by_network_observer_user(self):
        """List Server IPs with observer user should pass"""
        addr_list = self.observer_servers_client.list_addresses_by_network(
            self.server.id,
            'public')
        actual_addresses = addr_list.entity
        self.assertTrue(actual_addresses is not None,
                        "List addresses did not return any addresses")
        self.assertEqual(200, addr_list.status_code)