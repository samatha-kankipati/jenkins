import base64
from testrepo.common.testfixtures.compute import RbacComputeFixture
from ccengine.common.decorators import attr
from ccengine.common.exceptions.compute import Forbidden
from ccengine.common.tools.datagen import rand_name
from ccengine.domain.configuration import AuthConfig
from ccengine.clients.compute.servers_api import ServerAPIClient
from ccengine.domain.types import NovaImageStatusTypes
from ccengine.domain.types import NovaServerStatusTypes
from ccengine.providers.configuration import MasterConfigProvider as _MCP
from ccengine.providers.compute.compute_api import ComputeAPIProvider \
                                                   as _ComputeAPIProvider


class RBACServerResizeTest(RbacComputeFixture):

    @classmethod
    def setUpClass(cls):
        super(RBACServerResizeTest, cls).setUpClass()
        # Creation of 1 servers needed for the tests
        cls.server_response = cls.compute_provider.create_active_server()
        cls.server_to_resize = cls.server_response.entity
        cls.resources.add(cls.server_to_resize.id, cls.servers_client.delete_server)

    @classmethod
    def tearDownClass(cls):
        super(RBACServerResizeTest, cls).tearDownClass()

    @attr(type='smoke', net='no')
    def test_resize_server_with_observer_role(self):
        """Resize server with observer account should fail"""
        with self.assertRaises(Forbidden):
            self.observer_servers_client.resize(
                self.server_to_resize.id, 
                self.flavor_ref_alt)
        self._assert_server_fail_resize()
    
    @attr(type='smoke', net='no')
    def test_resize_server_with_creator_role(self):
        """Resize server with admin account should fail"""
        with self.assertRaises(Forbidden):
            self.creator_servers_client.resize(
                self.server_to_resize.id, 
                self.flavor_ref_alt)
        self._assert_server_fail_resize()
    
    def _assert_server_fail_resize(self):
        get_server_response = self.servers_client.get_server(self.server_to_resize.id)
        get_server = get_server_response.entity
        message = "Expected {0} to be {1}, was {2}."
        self.assertTrue(get_server.status == 'ACTIVE',
                        msg="Server is not in RESIZE state")
        self.assertEqual(get_server.progress, 100,
                         msg=message.format('server progress', '0',
                                            get_server.progress))
        self.assertTrue(get_server.task_state == None,
                        msg="Server task state should be none")
        self.assertTrue(get_server.id is not None,
                        msg="Server id was not set in the response")
        self.assertTrue(get_server.links is not None,
                        msg="Server links were not set in the response")
        self.assertEquals(get_server.tenant_id,
                          str(self.config.compute_api.tenant_id),
                          msg=message.format('tenant id',
                                             str(self.config.compute_api.tenant_id),
                                             get_server.tenant_id))
        self.assertTrue(get_server.name is not None,
                         msg="Server name was not set in the response")
        self.assertTrue(get_server.hostId is not None,
                        msg='Expected host id to be set.')
        self.assertEqual(self.image_ref, get_server.image.id,
                         msg=message.format('image id', self.image_ref,
                                            get_server.image.id))
        self.assertEqual(get_server.flavor.id, self.flavor_ref,
                         msg=message.format('flavor id', self.flavor_ref,
                                            get_server.flavor.id))
        self.assertTrue(get_server.created is not None,
                        msg="Expected server created date to be set, was null.")
        self.assertTrue(get_server.updated is not None,
                        msg="Expected server updated date to be set, was null.")
        self.assertGreaterEqual(get_server.updated, get_server.created,
                                msg="Expected server updated date to be before the created date.")

        
    @attr(type='smoke', net='no')
    def test_resize_server_with_admin_role(self):
        """Resize server with admin account should pass"""
        active_server_response = self.compute_provider.create_active_server()
        server_personal = active_server_response.entity
        self.resources.add(server_personal.id,
            self.servers_client.delete_server)
        resize_server_response = self.servers_client.resize(
            server_personal.id, 
            self.flavor_ref_alt)
        self.assertEqual(202, resize_server_response.status_code)
        self._assert_server_pass_resize(server_personal)
    
    def _assert_server_pass_resize(self, server_personal):
        get_server_response = self.servers_client.get_server(server_personal.id)
        get_server = get_server_response.entity
        message = "Expected {0} to be {1}, was {2}."
        self.assertTrue(get_server.status == 'RESIZE',
                        msg="Server is not in RESIZE state")
        self.assertTrue(get_server.task_state == 'resize_prep',
                        msg="Server is in resize preparation state")
        self.assertTrue(get_server.id is not None,
                        msg="Server id was not set in the response")
        self.assertTrue(get_server.links is not None,
                        msg="Server links were not set in the response")
        self.assertEqual(get_server.progress, 0,
                         msg=message.format('server progress', '0',
                                            get_server.progress))
        self.assertEquals(get_server.tenant_id,
                          str(self.config.compute_api.tenant_id),
                          msg=message.format('tenant id',
                                             str(self.config.compute_api.tenant_id),
                                             get_server.tenant_id))
        self.assertTrue(get_server.name is not None,
                         msg="Server name was not set in the response")
        self.assertTrue(get_server.hostId is not None,
                        msg='Expected host id to be set.')
        self.assertEqual(self.image_ref, get_server.image.id,
                         msg=message.format('image id', self.image_ref,
                                            get_server.image.id))
        self.assertEqual(get_server.flavor.id, self.flavor_ref,
                         msg=message.format('flavor id', self.flavor_ref,
                                            get_server.flavor.id))
        self.assertTrue(get_server.created is not None,
                        msg="Expected server created date to be set, was null.")
        self.assertTrue(get_server.updated is not None,
                        msg="Expected server updated date to be set, was null.")
        self.assertGreaterEqual(get_server.updated, get_server.created,
                                msg="Expected server updated date to be before the created date.")
    
    @attr(type='smoke', net='no')
    def test_resize_server_confirm_with_observer_role(self):
        """Resize server with observer account should fail"""
        active_server_response = self.compute_provider.create_active_server()
        server_personal = active_server_response.entity
        self.resources.add(server_personal.id,
            self.servers_client.delete_server)
        resize_server_response = self.servers_client.resize(
            server_personal.id, 
            self.flavor_ref_alt)
        self.assertEqual(202, resize_server_response.status_code)
        self.compute_provider.wait_for_server_status(
            server_personal.id,
            NovaServerStatusTypes.VERIFY_RESIZE)
        with self.assertRaises(Forbidden):
            self.observer_servers_client.confirm_resize(
                server_personal.id)
        self._assert_server_fail_confirm_resize(server_personal)
    
    @attr(type='smoke', net='no')
    def test_resize_server_confirm_with_creator_role(self):
        """Resize server confirm with admin account should fail"""
        active_server_response = self.compute_provider.create_active_server()
        server_personal = active_server_response.entity
        self.resources.add(server_personal.id,
            self.servers_client.delete_server)
        resize_server_response = self.servers_client.resize(
            server_personal.id, 
            self.flavor_ref_alt)
        self.assertEqual(202, resize_server_response.status_code)
        self.compute_provider.wait_for_server_status(
            server_personal.id,
            NovaServerStatusTypes.VERIFY_RESIZE)
        with self.assertRaises(Forbidden):      
            self.creator_servers_client.confirm_resize(
                server_personal.id)
        self._assert_server_fail_confirm_resize(server_personal)
    
    def _assert_server_fail_confirm_resize(self, server_personal):
        message = "Expected {0} to be {1}, was {2}."
        self.assertTrue(server_personal.status == 'ACTIVE',
                        msg="Server is not in RESIZE state")
        self.assertEqual(server_personal.progress, 100,
                         msg=message.format('server progress', '0',
                                            server_personal.progress))
        self.assertTrue(server_personal.task_state == None,
                        msg="Server task state should be none not RESIZE CONFIRM")
        self.assertNotEqual(self.flavor_ref_alt, server_personal.flavor.id)
    
    @attr(type='smoke', net='no')
    def test_resize_server_confirm_with_admin_role(self):
        """Resize server confirm with admin account should work"""
        active_server_response = self.compute_provider.create_active_server()
        server_personal = active_server_response.entity
        self.resources.add(server_personal.id,
            self.servers_client.delete_server)
        resize_server_response = self.servers_client.resize(
            server_personal.id, 
            self.flavor_ref_alt)
        self.assertEqual(202, resize_server_response.status_code)
        self.compute_provider.wait_for_server_status(
            server_personal.id,
            NovaServerStatusTypes.VERIFY_RESIZE)
        confirm_resize_response = self.servers_client.confirm_resize(
            server_personal.id)
        self.assertEqual(204, confirm_resize_response.status_code)
        self.compute_provider.wait_for_server_status(server_personal.id,
                                                    NovaServerStatusTypes.ACTIVE)
        resized_server_response = self.servers_client.get_server(server_personal.id)
        resized_server = resized_server_response.entity
        resized_server.adminPass = server_personal.adminPass
        self.assertEqual(self.flavor_ref_alt, resized_server.flavor.id)
        
    @attr(type='smoke', net='no')
    def test_resize_server_revert_with_admin_role(self):
        """Resize server revert with admin account should work"""
        active_server_response = self.compute_provider.create_active_server()
        server_personal = active_server_response.entity
        self.resources.add(server_personal.id,
            self.servers_client.delete_server)
        remote_instance = self.compute_provider.get_remote_instance_client(server_personal)
        file_name = rand_name('file') + '.txt'
        file_content = 'This is a test file'
        file_details = remote_instance.create_file(file_name, file_content)
        resize_server_response = self.servers_client.resize(
            server_personal.id, 
            self.flavor_ref_alt)
        self.assertEqual(202, resize_server_response.status_code)
        resize_server_response = self.compute_provider.wait_for_server_status(
            server_personal.id,
            NovaServerStatusTypes.VERIFY_RESIZE)
        revert_resize_response = self.servers_client.revert_resize(
            server_personal.id)
        self.assertEqual(202, revert_resize_response.status_code)
        reverted_server_response = self.compute_provider.wait_for_server_status(server_personal.id, NovaServerStatusTypes.ACTIVE)
        reverted_server = reverted_server_response.entity
        flavor_response = self.flavors_client.get_flavor_details(self.flavor_ref)
        flavor = flavor_response.entity

        '''Verify that the server resize was reverted '''
        public_address = self.compute_provider.get_public_ip_address(reverted_server)
        reverted_server.adminPass = server_personal.adminPass
        remote_instance = self.compute_provider.get_remote_instance_client(reverted_server, public_address)
        actual_file_content = remote_instance.get_file_details(file_details.name)
        '''Verify that the file content does not change after resize revert'''
        self.assertEqual(actual_file_content, file_details, msg="file changed after resize revert")
        self.assertEqual(self.flavor_ref, reverted_server.flavor.id,
                         msg="Flavor id not reverted")
    
    @attr(type='smoke', net='no')
    def test_resize_server_revert_with_creator_role(self):
        """Resize server revert with creator account should fail"""
        active_server_response = self.compute_provider.create_active_server()
        server_personal = active_server_response.entity
        self.resources.add(server_personal.id,
            self.servers_client.delete_server)
        resize_server_response = self.servers_client.resize(
            server_personal.id, 
            self.flavor_ref_alt)
        self.assertEqual(202, resize_server_response.status_code)
        resize_server_response = self.compute_provider.wait_for_server_status(
            server_personal.id,
            NovaServerStatusTypes.VERIFY_RESIZE)
        with self.assertRaises(Forbidden):  
            self.creator_servers_client.revert_resize(
                server_personal.id)
        server_personal_response = self.servers_client.get_server(server_personal.id)
        server_personal = server_personal_response.entity
        self._assert_server_fail_revert_resize(server_personal)
        
    @attr(type='smoke', net='no')
    def test_resize_server_revert_with_observer_role(self):
        """Resize server revert with creator account should fail"""
        active_server_response = self.compute_provider.create_active_server()
        server_personal = active_server_response.entity
        self.resources.add(server_personal.id,
            self.servers_client.delete_server)
        resize_server_response = self.servers_client.resize(
            server_personal.id, 
            self.flavor_ref_alt)
        self.assertEqual(202, resize_server_response.status_code)
        resize_server_response = self.compute_provider.wait_for_server_status(
            server_personal.id,
            NovaServerStatusTypes.VERIFY_RESIZE)
        with self.assertRaises(Forbidden):
            self.observer_servers_client.revert_resize(
                server_personal.id)
        server_personal_response = self.servers_client.get_server(server_personal.id)
        server_personal = server_personal_response.entity
        self._assert_server_fail_revert_resize(server_personal)
    
    def _assert_server_fail_revert_resize(self, server_personal):
        message = "Expected {0} to be {1}, was {2}."
        self.assertTrue(server_personal.status == 'VERIFY_RESIZE',
                        msg="Server is not in RESIZED state")
        self.assertEqual(server_personal.progress, 100,
                         msg=message.format('server progress', '100',
                                            server_personal.progress))
        self.assertTrue(server_personal.task_state == None,
                        msg="Server task state should be none not RESIZE CONFIRM")
        self.assertEqual(self.flavor_ref_alt, server_personal.flavor.id)
