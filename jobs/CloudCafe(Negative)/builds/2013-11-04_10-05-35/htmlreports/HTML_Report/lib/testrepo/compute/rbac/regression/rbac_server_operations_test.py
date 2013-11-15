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
        expected_upd_name ='upd_server'
        expected_accessIPv4 = '67.23.10.132'
        expected_accessIPv6 = '::babe:4317:a84'
        updated_server_response = self.servers_client.update_server(
            self.server.id,
            name=expected_upd_name,
            accessIPv4=expected_accessIPv4,
            accessIPv6=expected_accessIPv6)
        self.assertEqual(200, updated_server_response.status_code)
    
        updated_server = updated_server_response.entity
        updated_server_details_response = self.servers_client.get_server(
            self.server.id)
        updated_server_details = updated_server_details_response.entity
        self.compute_provider.wait_for_server_status(self.server.id,
            NovaServerStatusTypes.ACTIVE)
        # Verify the name and access IPs of the server have changed
        self._assert_success_updated_server_details(self.server, expected_upd_name,
            expected_accessIPv4, expected_accessIPv6,updated_server,
            updated_server_details)
        
    @attr(type='smoke', net='no')
    def test_update_server_with_creator_role(self):
        """Update of server with creator account should work"""
        expected_upd_name ='updated_server'
        expected_accessIPv4 = '67.23.10.131'
        expected_accessIPv6 = '::babe:67.23.10.131'
        with self.assertRaises(Forbidden):
            updated_server_response = self.creator_servers_client.update_server(
                self.server.id,
                name=expected_upd_name,
                accessIPv4=expected_accessIPv4,
                accessIPv6=expected_accessIPv6)
        updated_server_details_response = self.servers_client.get_server(
            self.server.id)
        updated_server_details = updated_server_details_response.entity
        # Verify the name and access IPs of the server have not changed
        self._assert_false_updated_server_details(self.server, expected_upd_name,
            expected_accessIPv4, expected_accessIPv6,
            updated_server_details)
    
    @attr(type='smoke', net='no')
    def test_update_server_with_observer_role(self):
        """Update of server with observer account should not work"""
        expected_upd_name ='updated_server'
        expected_accessIPv4 = '67.23.10.131'
        expected_accessIPv6 = '::babe:67.23.10.131'
        with self.assertRaises(Forbidden):
            self.observer_servers_client.update_server(
                self.server.id,
                name=expected_upd_name,
                accessIPv4=expected_accessIPv4,
                accessIPv6=expected_accessIPv6)
        updated_server_details_response = self.servers_client.get_server(
            self.server.id)
        updated_server_details = updated_server_details_response.entity
        # Verify the name and access IPs of the server have not changed
        self._assert_false_updated_server_details(self.server, expected_upd_name,
            expected_accessIPv4, expected_accessIPv6,
            updated_server_details)
    
    @attr(type='smoke', net='no')
    def test_update_server_with_observer_role_get_details(self):
        """Update of server with observer account should not work"""
        expected_upd_name ='updated_server'
        expected_accessIPv4 = '67.23.10.131'
        expected_accessIPv6 = '::babe:67.23.10.131'
        with self.assertRaises(Forbidden):
            self.observer_servers_client.update_server(
                self.server.id,
                name=expected_upd_name,
                accessIPv4=expected_accessIPv4,
                accessIPv6=expected_accessIPv6)
        updated_server_details_response = self.servers_client.get_server(
            self.server.id)
        updated_server_details = updated_server_details_response.entity
        # Verify the name and access IPs of the server have not changed
        self._assert_false_updated_server_details(self.server, expected_upd_name,
            expected_accessIPv4, expected_accessIPv6,
            updated_server_details)
    
    def _assert_success_updated_server_details(self, server, expected_upd_name,
                               expected_accessIPv4, expected_accessIPv6,
                               updated_server, updated_server_details):
        self.assertEqual(expected_upd_name, updated_server.name,
            msg="The name was not updated")
        self.assertEqual(expected_accessIPv4, updated_server.accessIPv4,
            msg="AccessIPv4 was not updated")
        self.assertEqual(expected_accessIPv6, updated_server.accessIPv6,
            msg="AccessIPv6 was not updated")
        self.assertEqual(server.created, updated_server.created,
            msg="The creation date was updated")
        # Verify details changed on get updated server call
        self.assertEqual(expected_upd_name, updated_server_details.name,
            msg="The name was not updated")
        self.assertEqual(expected_accessIPv4, updated_server_details.accessIPv4,
            msg="AccessIPv4 was not updated")
        self.assertEqual(expected_accessIPv6, updated_server_details.accessIPv6,
            msg="AccessIPv6 was not updated")
        self.assertEqual(self.server.created, updated_server_details.created,
            msg="The creation date was updated")
        self.assertNotEqual(server.updated, updated_server_details.updated,
            msg="Server %s updated time did not change after a + \
            modification to the server." % updated_server_details.id)
    
    def _assert_false_updated_server_details(self, server, expected_upd_name,
                               expected_accessIPv4, expected_accessIPv6,
                               updated_server_details):
        # Verify details are not changed on get updated server call
        self.assertNotEqual(expected_upd_name, updated_server_details.name,
            msg="The name was not updated")
        self.assertNotEqual(expected_accessIPv4, updated_server_details.accessIPv4,
            msg="AccessIPv4 was not updated")
        self.assertNotEqual(expected_accessIPv6, updated_server_details.accessIPv6,
            msg="AccessIPv6 was not updated")
        self.assertEqual(self.server.created, updated_server_details.created,
            msg="The creation date was updated")
        
    @attr(type='smoke', net='no')
    def test_get_server_admin_user(self):
        """Get server via admin user"""
        server_info_response = self.servers_client.get_server(self.server.id)
        self.assertEqual(200, server_info_response.status_code)
        server = server_info_response.entity
        # Verify the get elements in the api call
        self._assert_get_server_details(server)
    
    @attr(type='smoke', net='no')
    def test_get_server_creator_user(self):
        """Get server via creator user"""
        server_info_response = self.creator_servers_client.get_server(
            self.server.id)
        self.assertEqual(200, server_info_response.status_code)
        server = server_info_response.entity
        # Verify the get elements in the api call
        self._assert_get_server_details(server)
    
    @attr(type='smoke', net='no')
    def test_get_server_observer_user(self):
        """Get server via observer user"""
        server_info_response = self.observer_servers_client.get_server(
            self.server.id)
        self.assertEqual(200, server_info_response.status_code)
        server = server_info_response.entity
        # Verify the get elements in the api call
        self._assert_get_server_details(server)
    
    def _assert_get_server_details(self, server):
        message = "Expected {0} to be {1}, was {2}."
        self.assertEqual(server.progress, 100,
                         msg=message.format('server progress', '100',
                                            server.progress))
        self.assertEquals(server.tenant_id,
                          str(self.config.compute_api.tenant_id),
                          msg=message.format('tenant id',
                                             str(self.config.compute_api.tenant_id),
                                             server.tenant_id))
        self.assertTrue(server.name is not None,
                         msg='Server name is empty')
        self.assertTrue(self.server.hostId is not None,
                        msg='Expected host id to be set.')
        self.assertEqual(self.image_ref, server.image.id,
                         msg=message.format('image id', self.image_ref,
                                            server.image.id))
        self.assertEqual(server.flavor.id, self.flavor_ref,
                         msg=message.format('flavor id', self.flavor_ref,
                                            server.flavor.id))
        self.assertTrue(server.created is not None,
                        msg="Expected server created date to be set, was null.")
        self.assertTrue(server.updated is not None,
                        msg="Expected server updated date to be set, was null.")
        self.assertGreaterEqual(server.updated, server.created,
                                msg="Expected server updated date to be before the created date.")
    
    @attr(type='smoke', net='no')
    def test_delete_server_admin_user(self):
        """Delete server via admin user"""
        active_server_response = self.compute_provider.create_active_server()
        active_server = active_server_response.entity
        deleted_server_response = self.servers_client.delete_server(active_server.id)
        self.assertEqual(204, deleted_server_response.status_code,
                         msg='The delete call response was: %s'
                         % (deleted_server_response.status_code))
        self.compute_provider.wait_for_server_status(active_server.id,
                                                     NovaServerStatusTypes.DELETED)
        # Verify the server is now in deleted status
        parameter = str(active_server.created)
        list_servers = self.servers_client.list_servers_with_detail(changes_since=parameter)
        found = False
        for server in list_servers.entity:
            if server.id == active_server.id:
                deleted_server = server
                found = True

        self.assertTrue(found,
                        msg="The server which was deleted was not found in the server list")
        self.assertEqual('DELETED', deleted_server.status,
                         msg="The server which was deleted was not in DELETED status")
    
    @attr(type='smoke', net='no')
    def test_delete_server_creator_user(self):
        """Delete server via creator user should fail"""
        active_server_response = (
            self.compute_provider_for_creator_user.create_active_server())
        active_server = active_server_response.entity
        with self.assertRaises(Forbidden):
            self.creator_servers_client.delete_server(
                active_server.id)
        # Verify the server was not deleted
        self._assert_server_not_deleted_details(active_server)
    
    @attr(type='smoke', net='no')
    def test_delete_server_observer_user(self):
        """Delete server via observer user should fail"""
        active_server_response = (
            self.compute_provider_for_creator_user.create_active_server())
        active_server = active_server_response.entity
        with self.assertRaises(Forbidden):
            self.observer_servers_client.delete_server(
                active_server.id)
        # Verify the server was not deleted
        self._assert_server_not_deleted_details(active_server)
    
    def _assert_server_not_deleted_details(self, active_server):
        # Verify the server is now in deleted status
        parameter = str(active_server.created)
        list_servers = self.servers_client.list_servers_with_detail(changes_since=parameter)
        found = False
        for server in list_servers.entity:
            if server.id == active_server.id:
                deleted_server = server
                found = True

        self.assertTrue(found,
                        msg="The server which was deleted was not found in the server list")
        self.assertNotEqual('DELETED', deleted_server.status,
                         msg="The server which was deleted was not in DELETED status")
    
    @attr(type='smoke', net='yes')
    def test_list_addresses_admin_user(self):
        """List Server IPs with admin user"""
        expected_addresses = self.server.addresses
        addr_list = self.servers_client.list_addresses(self.server.id)
        actual_addresses = addr_list.entity
        self.assertTrue(actual_addresses is not None,
                        "List addresses did not return any addresses")
        self.assertEqual(200, addr_list.status_code)
        # Verify listed addresses
        self._assert_list_addresses(actual_addresses, expected_addresses)
        
    @attr(type='smoke', net='yes')
    def test_list_addresses_creator_user(self):
        """List Server IPs with creator user"""
        expected_addresses = self.server.addresses
        addr_list = self.creator_servers_client.list_addresses(self.server.id)
        actual_addresses = addr_list.entity
        self.assertTrue(actual_addresses is not None,
                        "List addresses did not return any addresses")
        self.assertEqual(200, addr_list.status_code)
        # Verify listed addresses
        self._assert_list_addresses(actual_addresses, expected_addresses)
    
    @attr(type='smoke', net='yes')
    def test_list_addresses_observer_user(self):
        """List Server IPs with observer user"""
        expected_addresses = self.server.addresses
        addr_list = self.observer_servers_client.list_addresses(self.server.id)
        actual_addresses = addr_list.entity
        self.assertTrue(actual_addresses is not None,
                        "List addresses did not return any addresses")
        self.assertEqual(200, addr_list.status_code)
        # Verify listed addresses
        self._assert_list_addresses(actual_addresses, expected_addresses)
    
    def _assert_list_addresses(self, actual_addresses, expected_addresses):
        self.assertTrue(actual_addresses is not None,
                        "List addresses did not return any addresses")
        self.assertEqual(expected_addresses, actual_addresses,
                         '''Addresses returned by List addresses request is not 
                         same as the addresses returned in Get server request''')
        if len(actual_addresses.public.addresses) > 0:
            remote_client = self.compute_provider.get_remote_instance_client(self.server)
            self.assertTrue(remote_client.can_connect_to_public_ip(),
                            "Cannot connect to server using public ip")
        if len(actual_addresses.private.addresses) > 0:
            self._assert_private_addresses(actual_addresses.private.addresses)

    def _assert_private_addresses(self, private_addresses):
        remote_client = self.compute_provider.get_remote_instance_client(self.server)
        self.assertTrue(remote_client.can_remote_ping_private_ip(private_addresses),
                        "Cannot access the server using private address")
        
    @attr(type='smoke', net='yes')
    def test_list_addresses_by_network_admin_user(self):
        """List Server IPs with admin user should pass"""
        expected_addresses = self.server.addresses
        addr_list = self.servers_client.list_addresses_by_network(
            self.server.id,
            'public')
        self.assertEqual(200, addr_list.status_code)
        actual_addresses = addr_list.entity
        # Verify listed addresses public
        self._assert_list_network_addresses_public(actual_addresses, expected_addresses)
        
        addr_list = self.servers_client.list_addresses_by_network(
            self.server.id,
            'private')
        self.assertEqual(200, addr_list.status_code)
        actual_addresses = addr_list.entity
        # Verify listed addresses private
        self._assert_list_network_addresses_private(actual_addresses, expected_addresses)
        
    @attr(type='smoke', net='yes')
    def test_list_addresses_by_network_creator_user(self):
        """List Server IPs with creator user should pass"""
        expected_addresses = self.server.addresses
        addr_list = self.creator_servers_client.list_addresses_by_network(
            self.server.id,
            'public')
        self.assertEqual(200, addr_list.status_code)
        actual_addresses = addr_list.entity
        # Verify listed addresses public
        self._assert_list_network_addresses_public(actual_addresses, expected_addresses)
        
        addr_list = self.creator_servers_client.list_addresses_by_network(
            self.server.id,
            'private')
        self.assertEqual(200, addr_list.status_code)
        actual_addresses = addr_list.entity
        # Verify listed addresses private
        self._assert_list_network_addresses_private(actual_addresses, expected_addresses)
        
    @attr(type='smoke', net='yes')
    def test_list_addresses_by_network_observer_user(self):
        """List Server IPs with observer user should pass"""
        expected_addresses = self.server.addresses
        addr_list = self.observer_servers_client.list_addresses_by_network(
            self.server.id,
            'public')
        self.assertEqual(200, addr_list.status_code)
        actual_addresses = addr_list.entity
        # Verify listed addresses public
        self._assert_list_network_addresses_public(actual_addresses, expected_addresses)
        
        addr_list = self.observer_servers_client.list_addresses_by_network(
            self.server.id,
            'private')
        self.assertEqual(200, addr_list.status_code)
        actual_addresses = addr_list.entity
        # Verify listed addresses private
        self._assert_list_network_addresses_private(actual_addresses, expected_addresses)
    
    def _assert_list_network_addresses_public(self, actual_addresses, expected_addresses):
        self.assertTrue(actual_addresses is not None,
                        "List addresses did not return any addresses")
        public_addresses = actual_addresses
        self.assertEqual(expected_addresses.public, public_addresses.public,
                         '''Addresses returned by List addresses by public type
                         did not match addresses returned by get server''')
        if len(public_addresses.public.addresses) > 0:
            remote_client = self.compute_provider.get_remote_instance_client(self.server)
            self.assertTrue(remote_client.can_ping_public_ip(public_addresses.public.addresses,
                            self.config.compute_api.ip_address_version_for_ssh),
                            "Cannot connect to server using public ip")
        
    def _assert_list_network_addresses_private(self, actual_addresses, expected_addresses):
        self.assertTrue(actual_addresses is not None,
                        "List addresses did not return any addresses")     
        private_addresses = actual_addresses
        self.assertEqual(expected_addresses.private, private_addresses.private,
                         '''Addresses returned by List addresses by private type 
                         did not match addresses returned by get server''')
        if len(private_addresses.private.addresses) > 0:
            self._assert_private_addresses(private_addresses.private.addresses)