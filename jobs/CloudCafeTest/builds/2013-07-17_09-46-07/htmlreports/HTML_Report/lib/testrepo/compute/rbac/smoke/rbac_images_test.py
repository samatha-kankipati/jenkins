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


class RBACImagesTest(RbacComputeFixture):

    @classmethod
    def setUpClass(cls):
        super(RBACImagesTest, cls).setUpClass()
        # Creation of 1 servers needed for the tests
        active_server_response = cls.compute_provider.create_active_server()
        cls.server = active_server_response.entity
        cls.resources.add(cls.server.id,
                          cls.servers_client.delete_server)

    @classmethod
    def tearDownClass(cls):
        super(RBACImagesTest, cls).tearDownClass()

    @attr(type='smoke', net='no')
    def test_image_list_with_admin_role(self):
        """List images with admin account should work"""
        image_response = self.images_client.list_images()
        self.assertEqual(200, image_response.status_code)
    
    @attr(type='smoke', net='no')
    def test_image_list_with_creator_role(self):
        """List images with creator account should work"""
        image_response = self.creator_images_client.list_images()
        self.assertEqual(200, image_response.status_code)
    
    @attr(type='smoke', net='no')
    def test_image_list_with_observer_role(self):
        """List images with observer account should work"""
        image_response = self.observer_images_client.list_images()
        self.assertEqual(200, image_response.status_code)
    
    @attr(type='smoke', net='no')
    def test_image_list_detail_with_admin_role(self):
        """List images detail with admin account should work"""
        image_response = self.images_client.list_images_with_detail()
        self.assertEqual(200, image_response.status_code)
    
    @attr(type='smoke', net='no')
    def test_image_list_detail_with_creator_role(self):
        """List images detail with creator account should work"""
        image_response = self.creator_images_client.list_images_with_detail()
        self.assertEqual(200, image_response.status_code)
    
    @attr(type='smoke', net='no')
    def test_image_list_detail_with_observer_role(self):
        """List images detail with observer account should work"""
        image_response = self.observer_images_client.list_images_with_detail()
        self.assertEqual(200, image_response.status_code)
    
    @attr(type='smoke', net='no')
    def test_image_get_detail_with_admin_role(self):
        """List images detail with admin account should work"""
        image_response = self.images_client.get_image(self.image_ref)
        self.assertEqual(200, image_response.status_code)
    
    @attr(type='smoke', net='no')
    def test_image_get_detail_with_creator_role(self):
        """List images detail with creator account should work"""
        image_response = self.creator_images_client.get_image(self.image_ref)
        self.assertEqual(200, image_response.status_code)
    
    @attr(type='smoke', net='no')
    def test_image_get_detail_with_observer_role(self):
        """List images detail with observer account should work"""
        image_response = self.observer_images_client.get_image(self.image_ref)
        self.assertEqual(200, image_response.status_code)
