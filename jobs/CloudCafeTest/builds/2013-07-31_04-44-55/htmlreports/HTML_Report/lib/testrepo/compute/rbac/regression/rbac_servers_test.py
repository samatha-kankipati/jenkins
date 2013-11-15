from testrepo.common.testfixtures.compute import RbacComputeFixture
from ccengine.common.decorators import attr
from ccengine.common.tools.datagen import rand_name
from ccengine.domain.configuration import AuthConfig
from ccengine.clients.compute.servers_api import ServerAPIClient
from ccengine.domain.types import NovaImageStatusTypes
from ccengine.common.exceptions.compute import Forbidden
from ccengine.providers.configuration import MasterConfigProvider as _MCP
from ccengine.providers.compute.compute_api import ComputeAPIProvider \
                                                   as _ComputeAPIProvider


class RBACServerTest(RbacComputeFixture):

    @classmethod
    def setUpClass(cls):
        super(RBACServerTest, cls).setUpClass()
        # Creation of 1 servers needed for the tests
        active_server_response = cls.compute_provider.create_active_server()
        cls.server = active_server_response.entity
        cls.resources.add(cls.server.id,
                          cls.servers_client.delete_server)

    @classmethod
    def tearDownClass(cls):
        super(RBACServerTest, cls).tearDownClass()
    
    @attr(type='smoke', net='no')
    def test_create_server_from_creator_snapshot_admin_user(self):
        """An image is created with creator user should pass"""
        self._test_create_server_from_creator_snapshot(role='admin')
    
    @attr(type='smoke', net='no')
    def test_create_server_from_creator_snapshot_creator_user(self):
        """An image is created with creator user should pass"""
        self._test_create_server_from_creator_snapshot(role='creator')
        
    @attr(type='smoke', net='no')
    def test_create_server_from_creator_snapshot_observer_user(self):
        """An image is created with creator user should fail"""
        self._test_create_server_from_creator_snapshot(role='observer')
    
    @attr(type='smoke', net='no')
    def test_create_server_from_admin_snapshot_admin_user(self):
        """An image is created with admin user"""
        self._test_create_server_from_admin_snapshot(role='admin')
        
    @attr(type='smoke', net='no')
    def test_create_server_from_admin_snapshot_creator_user(self):
        """An image is created with creator user"""
        self._test_create_server_from_admin_snapshot(role='creator')
        
    @attr(type='smoke', net='no')
    def test_create_server_from_admin_snapshot_observer_user(self):
        """An image is created with observer user"""
        self._test_create_server_from_admin_snapshot(role='observer')
    
    @attr(type='smoke', net='no')
    def test_server_creation_with_admin_role(self):
        """Creation of server with admin account should work"""
        self._test_server_creation(role='admin')
    
    @attr(type='smoke', net='no')
    def test_server_creation_with_creator_role(self):
        """Creation of server with creator account should work"""
        self._test_server_creation(role='creator')
        
    @attr(type='smoke', net='no')
    def test_server_creation_with_observer_role(self):
        """Creation of server with observer account should not work"""
        self._test_server_creation(role='observer')
    
    def _test_create_server_snapshot(self, role_for_server):
        if role_for_server.lower() == 'admin':
            base_server_response = self.compute_provider.create_active_server()
        
        if role_for_server.lower() == 'creator':
            base_server_response = self.compute_provider_for_creator_user.create_active_server()
        self.assertEqual(200, base_server_response.status_code) 
        name = rand_name('testimage')
        server_id = base_server_response.entity.id
        image_response = self.servers_client.create_image(server_id, name)
        image_id = self.parse_image_id(image_response)
        self.compute_provider.wait_for_image_status(image_id,
                                                    NovaImageStatusTypes.ACTIVE)
        return image_id, base_server_response
    
    def _test_create_server_from_admin_snapshot(self, role):
        '''Image creatoion with admin user'''
        image_id, base_server_response = self._test_create_server_snapshot(
            role_for_server='admin')
        self._test_create_server_from_snapshot_general_procedure(role=role,
            image_id=image_id,
            base_server_response=base_server_response)
    
    def _test_create_server_from_creator_snapshot(self, role):
        '''Image creatoion with creator user'''
        image_id, base_server_response = self._test_create_server_snapshot(
            role_for_server='creator')
        self._test_create_server_from_snapshot_general_procedure(role=role,
            image_id=image_id,
            base_server_response=base_server_response)
    
    def _test_create_server_from_snapshot_general_procedure(self, role,
                                                            image_id,
                                                            base_server_response):
        server_info_response = self.servers_client.list_servers()
        num_servers_before = len(server_info_response.entity)
        class Empty: pass
        server_from_image_response = Empty()
        server_from_image_response.entity = 'Data'
        if role.lower() == 'admin':
            server_from_image_response = self.compute_provider.create_active_server(
                                                    image_ref=image_id)
        if role.lower() == 'creator':
            server_from_image_response = self.compute_provider_for_creator_user.create_active_server(
                                                    image_ref=image_id)
        elif role.lower() == 'observer':
            with self.assertRaises(Forbidden):
                self.compute_provider_for_observer_user.create_active_server(
                    image_ref=image_id)
        base_server = base_server_response.entity
        server_from_image = server_from_image_response.entity
        self._check_server_response(role=role, image_id=image_id,
                                   num_servers_before=num_servers_before,
                                   base_server=base_server,
                                   server_from_image=server_from_image)
        # Delete image and wait for image to be deleted
        self.compute_provider.wait_for_image_to_be_deleted(image_id)
    
    def _check_server_response(self, role, num_servers_before=None,
                              base_server=None, server_from_image=None,
                              image_id=None, only_server_creation=None):
        if role.lower() == 'observer':
            server_info_response = self.servers_client.list_servers()
            num_servers_present = len(server_info_response.entity)
            self.assertEqual(num_servers_before, num_servers_present,
                             msg='Server stay the same number')
        else:
            message = "Expected {0} to be {1}, was {2}."
            self.assertTrue(server_from_image.id is not None,
                            msg="Server id was not set in the response")
            if only_server_creation is not True:
                self.assertNotEqual(base_server.adminPass, server_from_image.adminPass,
                                    msg="Admin password should be diferent in the response")
                self.assertNotEqual(base_server.links, server_from_image.links,
                                    msg="Server links should be diferent in the response")
                self.assertEqual(server_from_image.image.id, image_id,
                             msg=message.format('image id', image_id,
                                                server_from_image.image.id))
            self.assertEqual(server_from_image.progress, 100,
                             msg=message.format('server progress', '100',
                                                server_from_image.progress))
            self.assertEquals(server_from_image.tenant_id,
                              base_server.tenant_id,
                              msg=message.format('tenant id equals',
                                                 server_from_image.tenant_id,
                                                 base_server.tenant_id))
            self.assertTrue(server_from_image.name is not None,
                            msg="Server name was not set in the response")
            self.assertTrue(server_from_image.hostId is not None,
                            msg='Expected host id to be set.')
            self.assertEqual(server_from_image.flavor.id, self.flavor_ref,
                             msg=message.format('flavor id', self.flavor_ref,
                                                server_from_image.flavor.id))
            self.assertTrue(server_from_image.created is not None,
                            msg="Expected server created date to be set, was null.")
            self.assertTrue(server_from_image.updated is not None,
                            msg="Expected server updated date to be set, was null.")
            self.assertGreaterEqual(server_from_image.created, base_server.created,
                                    msg="Exp. server created date is after the base server created date.")
    
    def _test_server_creation(self, role):
        only_server_creation = True
        server_info_response = self.servers_client.list_servers()
        num_servers_before = len(server_info_response.entity)
        class Empty: pass
        server_response = Empty()
        server_response.entity = 'Data'
        if role.lower() == 'admin':
            server_response = self.compute_provider.create_active_server()
        if role.lower() == 'creator':
            server_response = self.compute_provider_for_creator_user.create_active_server()
        elif role.lower() == 'observer':
            with self.assertRaises(Forbidden):
                self.compute_provider_for_observer_user.create_active_server()
        server = server_response.entity
        self._check_server_response(role=role,
                                    num_servers_before=num_servers_before,
                                    base_server=server,
                                    server_from_image=server,
                                    only_server_creation=only_server_creation)
    