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
    def test_server_creation_with_admin_role(self):
        """Creation of server with admin account should work"""
        server_response =self.compute_provider.create_active_server()
        self.assertEqual(200, server_response.status_code)
    
    @attr(type='smoke', net='no')
    def test_server_creation_with_creator_role(self):
        """Creation of server with creator account should work"""
        server_response =self.compute_provider_for_creator_user.create_active_server()
        self.assertEqual(200, server_response.status_code)
        
    @attr(type='smoke', net='no')
    def test_server_creation_with_observer_role(self):
        """Creation of server with observer account should not work"""
        with self.assertRaises(Forbidden):
            self.compute_provider_for_observer_user.create_active_server()
        
    @attr(type='smoke', net='no')
    def test_create_server_from_admin_snapshot_admin_user(self):
        """An image is created with admin user"""
        server_response =self.compute_provider.create_active_server()
        self.assertEqual(200, server_response.status_code)
        name = rand_name('testimage')
        server_id = server_response.entity.id
        image_response = self.servers_client.create_image(server_id, name)
        image_id = self.parse_image_id(image_response)
        self.compute_provider.wait_for_image_status(image_id,
                                                    NovaImageStatusTypes.ACTIVE)
        server_response = self.compute_provider.create_active_server(
                                                    image_ref=image_id)
        self.assertEqual(200, server_response.status_code)
        # Delete image and wait for image to be deleted
        self.compute_provider.wait_for_image_to_be_deleted(image_id)
        
    @attr(type='smoke', net='no')
    def test_create_server_from_admin_snapshot_creator_user(self):
        """An image is created with admin user"""
        server_response =self.compute_provider.create_active_server()
        self.assertEqual(200, server_response.status_code)
        name = rand_name('testimage')
        server_id = server_response.entity.id
        image_response = self.servers_client.create_image(server_id, name)
        image_id = self.parse_image_id(image_response)
        self.compute_provider.wait_for_image_status(image_id,
                                                    NovaImageStatusTypes.ACTIVE)
        server_response = self.compute_provider_for_creator_user.create_active_server(
                                                    image_ref=image_id)
        self.assertEqual(200, server_response.status_code)
        # Delete image and wait for image to be deleted
        self.compute_provider.wait_for_image_to_be_deleted(image_id)
        
    @attr(type='smoke', net='no')
    def test_create_server_from_admin_snapshot_observer_user(self):
        """An image is created with admin user"""
        server_response =self.compute_provider.create_active_server()
        self.assertEqual(200, server_response.status_code)
        name = rand_name('testimage')
        server_id = server_response.entity.id
        image_response = self.servers_client.create_image(server_id, name)
        image_id = self.parse_image_id(image_response)
        self.compute_provider.wait_for_image_status(image_id,
                                                    NovaImageStatusTypes.ACTIVE)
        with self.assertRaises(Forbidden):
            self.compute_provider_for_observer_user.create_active_server(
                image_ref=image_id)
        # Delete image and wait for image to be deleted
        self.compute_provider.wait_for_image_to_be_deleted(image_id)
    
    @attr(type='smoke', net='no')
    def test_create_server_from_creator_snapshot_admin_user(self):
        """An image is created with creator user"""
        server_response =self.compute_provider_for_creator_user.create_active_server()
        self.assertEqual(200, server_response.status_code)
        name = rand_name('testimage')
        server_id = server_response.entity.id
        image_response = self.servers_client.create_image(server_id, 
                                                                  name)
        image_id = self.parse_image_id(image_response)
        self.compute_provider.wait_for_image_status(image_id,
                                                    NovaImageStatusTypes.ACTIVE)
        server_response = self.compute_provider.create_active_server(
                                                    image_ref=image_id)
        self.assertEqual(200, server_response.status_code)
        # Delete image and wait for image to be deleted
        self.compute_provider.wait_for_image_to_be_deleted(image_id)
    
    @attr(type='smoke', net='no')
    def test_create_server_from_creator_snapshot_creator_user(self):
        """An image is created with creator user should pass"""
        server_response =self.compute_provider_for_creator_user.create_active_server()
        self.assertEqual(200, server_response.status_code)
        name = rand_name('testimage')
        server_id = server_response.entity.id
        image_response = self.servers_client.create_image(server_id, 
                                                                  name)
        image_id = self.parse_image_id(image_response)
        self.compute_provider.wait_for_image_status(image_id,
                                                    NovaImageStatusTypes.ACTIVE)
        server_response = self.compute_provider_for_creator_user.create_active_server(
                                                    image_ref=image_id)
        self.assertEqual(200, server_response.status_code)
        # Delete image and wait for image to be deleted
        self.compute_provider.wait_for_image_to_be_deleted(image_id)
        
    @attr(type='smoke', net='no')
    def test_create_server_from_creator_snapshot_observer_user(self):
        """An image is created with creator user should fail"""
        server_response =self.compute_provider_for_creator_user.create_active_server()
        self.assertEqual(200, server_response.status_code)
        name = rand_name('testimage')
        server_id = server_response.entity.id
        image_response = self.servers_client.create_image(server_id, 
                                                          name)
        image_id = self.parse_image_id(image_response)
        self.compute_provider.wait_for_image_status(image_id,
                                                    NovaImageStatusTypes.ACTIVE)
        with self.assertRaises(Forbidden):
            self.compute_provider_for_observer_user.create_active_server(
                image_ref=image_id)
        # Delete image and wait for image to be deleted
        self.compute_provider.wait_for_image_to_be_deleted(image_id)