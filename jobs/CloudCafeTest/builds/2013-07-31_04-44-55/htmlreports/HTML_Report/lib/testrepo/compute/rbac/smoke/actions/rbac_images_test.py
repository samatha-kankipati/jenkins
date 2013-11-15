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
        # Creation of 2 servers needed for the tests
        active_server_response = cls.compute_provider.create_active_server()
        cls.server = active_server_response.entity
        cls.resources.add(cls.server.id,
                          cls.servers_client.delete_server)
        sec_active_server_response = cls.compute_provider.create_active_server()
        cls.sec_server = sec_active_server_response.entity
        cls.resources.add(cls.sec_server.id,
                          cls.servers_client.delete_server)

    @classmethod
    def tearDownClass(cls):
        super(RBACServerTest, cls).tearDownClass()
    
    @attr(type='smoke', net='no')
    def test_create_snapshot_admin_user(self):
        """An image is created with admin user should pass"""
        self._test_create_snapshot(role_for_snapshot='admin', 
                                   server_id=self.server.id)
    
    @attr(type='smoke', net='no')
    def test_create_snapshot_creator_user(self):
        """An image is created with creator user should pass"""
        self._test_create_snapshot(role_for_snapshot='creator', 
                                   server_id=self.server.id)
        
    @attr(type='smoke', net='no')
    def test_create_snapshot_observer_user(self):
        """An image is created with observer user should fail"""
        self._test_create_snapshot(role_for_snapshot='observer', 
                                   server_id=self.server.id)
    
    @attr(type='smoke', net='no')
    def test_delete_snapshot_admin_user(self):
        """An image is deleted with admin user should pass"""
        image = self._test_create_snapshot(role_for_snapshot='admin', 
                                           server_id=self.sec_server.id)
        self._test_delete_snapshot(role_for_snapshot='admin', 
                                   image_id=image)
    
    @attr(type='smoke', net='no')
    def test_delete_snapshot_creator_user(self):
        """An image is deleted with creator user should fail"""
        image = self._test_create_snapshot(role_for_snapshot='admin', 
                                           server_id=self.sec_server.id)
        self._test_delete_snapshot(role_for_snapshot='creator', 
                                   image_id=image)
        
    @attr(type='smoke', net='no')
    def test_delete_snapshot_observer_user(self):
        """An image is deleted with observer user should fail"""
        image = self._test_create_snapshot(role_for_snapshot='admin', 
                                           server_id=self.sec_server.id)
        self._test_delete_snapshot(role_for_snapshot='observer', 
                                   image_id=image)
    
    def _test_create_snapshot(self, role_for_snapshot, server_id):
        name = rand_name('testimage')
        if role_for_snapshot.lower() == 'admin':
            image_response = self.servers_client.create_image(
                server_id, 
                name)
            image_id = self.parse_image_id(image_response)
            self.compute_provider.wait_for_image_status(
                                                    image_id,
                                                    NovaImageStatusTypes.ACTIVE)
            self.assertEqual(image_response.status_code, 202)
            return image_id
        if role_for_snapshot.lower() == 'creator':
            with self.assertRaises(Forbidden):
                image_response = self.creator_servers_client.create_image(
                    server_id, 
                    name)
        elif role_for_snapshot.lower() == 'observer':
            with self.assertRaises(Forbidden):
                image_response = self.observer_servers_client.create_image(
                    server_id, 
                    name)
    
    def _test_delete_snapshot(self, role_for_snapshot, image_id):
        if role_for_snapshot.lower() == 'admin':
            image_response = self.images_client.delete_image(
                image_id)
            self.assertEqual(image_response.status_code, 204)
        if role_for_snapshot.lower() == 'creator':
            with self.assertRaises(Forbidden):
                image_response = self.creator_images_client.delete_image(
                image_id)
        elif role_for_snapshot.lower() == 'observer':
            with self.assertRaises(Forbidden):
                image_response = self.observer_images_client.delete_image(
                image_id)
