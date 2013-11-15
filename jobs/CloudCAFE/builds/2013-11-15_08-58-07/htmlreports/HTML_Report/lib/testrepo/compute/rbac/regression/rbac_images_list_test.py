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
        image1_name = rand_name('testimage')
        image1_resp = cls.servers_client.create_image(cls.server.id,
                                                      image1_name)
        assert image1_resp.status_code == 202
        cls.image1_id = cls.parse_image_id(image1_resp)
        cls.compute_provider.wait_for_image_status(cls.image1_id, NovaImageStatusTypes.ACTIVE)

        cls.image_1 = cls.images_client.get_image(cls.image1_id).entity
        cls.resources.add(cls.image1_id, cls.images_client.delete_image)

    @classmethod
    def tearDownClass(cls):
        super(RBACImagesTest, cls).tearDownClass()

    @attr(type='smoke', net='no')
    def test_image_list_with_admin_role(self):
        """List image with admin account should work"""
        image_response = self.images_client.list_images()
        self.assertEqual(200, image_response.status_code)
        images = image_response.entity
        self._assert_image_list(images)
        self._assert_image_list_is_not_dummy(images)
    
    @attr(type='smoke', net='no')
    def test_image_list_with_creator_role(self):
        """List image with creator account should work"""
        image_response = self.creator_images_client.list_images()
        self.assertEqual(200, image_response.status_code)
        images = image_response.entity
        self._assert_image_list(images)
        self._assert_image_list_is_not_dummy(images)
    
    @attr(type='smoke', net='no')
    def test_image_list_with_observer_role(self):
        """List image with observer account should work"""
        image_response = self.observer_images_client.list_images()
        self.assertEqual(200, image_response.status_code)
        images = image_response.entity
        self._assert_image_list(images)
        self._assert_image_list_is_not_dummy(images)
    
    def _assert_image_list(self, images):
        self.assertTrue(len(images) > 0)
        self.assertTrue(images[0].id is not None,
                        msg="id is present")
        self.assertTrue(images[0].name is not None,
                        msg="name is present")
        self.assertTrue(images[0].links is not None,
                        msg="links are present")
    
    def _assert_image_list_is_not_dummy(self, images):
        images = self.images_client.list_images_with_detail()
        images = [image.id for image in images.entity]

        self.assertTrue(self.image_1.id in images,
            msg="Image {0} should be in the list.".format(self.image_1.id))
    
    @attr(type='smoke', net='no')
    def test_image_list_detail_with_admin_role(self):
        """List images detail with admin account should work"""
        image_response = self.images_client.list_images_with_detail()
        self.assertEqual(200, image_response.status_code)
        images = image_response.entity
        self._assert_image_detail(image_list=images)
        self._assert_image_list_is_not_dummy(images)
    
    @attr(type='smoke', net='no')
    def test_image_list_detail_with_creator_role(self):
        """List images detail with creator account should work"""
        image_response = self.creator_images_client.list_images_with_detail()
        self.assertEqual(200, image_response.status_code)
        images = image_response.entity
        self._assert_image_detail(image_list=images)
        self._assert_image_list_is_not_dummy(images)
    
    @attr(type='smoke', net='no')
    def test_image_list_detail_with_observer_role(self):
        """List images detail with observer account should work"""
        image_response = self.observer_images_client.list_images_with_detail()
        self.assertEqual(200, image_response.status_code)
        images = image_response.entity
        self._assert_image_detail(image_list=images)
        self._assert_image_list_is_not_dummy(images)
    
    @attr(type='smoke', net='no')
    def test_image_get_detail_with_admin_role(self):
        """Get images detail with admin account should work"""
        image_response = self.images_client.get_image(self.image_ref)
        self.assertEqual(200, image_response.status_code)
        image = image_response.entity
        self._assert_image_detail(image=image)
    
    @attr(type='smoke', net='no')
    def test_image_get_detail_with_creator_role(self):
        """Get images detail with creator account should work"""
        image_response = self.creator_images_client.get_image(self.image_ref)
        self.assertEqual(200, image_response.status_code)
        image = image_response.entity
        self._assert_image_detail(image=image)
    
    @attr(type='smoke', net='no')
    def test_image_get_detail_with_observer_role(self):
        """Get images detail with observer account should work"""
        image_response = self.observer_images_client.get_image(self.image_ref)
        self.assertEqual(200, image_response.status_code)
        image = image_response.entity
        self._assert_image_detail(image=image)

    def _assert_image_detail(self, image_list=None, image=None):
        message = "Expected {0} to be {1}, was {2}."
        if image_list is not None:
                image = image_list[0]
                image_last = image_list[-1]
                self.assertTrue(image is not None and image_last is not None)
        self.assertTrue(image.id is not None,
                        msg="id is present")
        self.assertTrue(image.name is not None,
                        msg="name is present")
        self.assertTrue(image.links is not None,
                        msg="links are present")
        self.assertTrue(image.diskConfig is not None,
                        msg="diskConfig is present")
        self.assertTrue(image.created is not None,
                        msg="Created field is present")
        self.assertTrue(image.metadata is not None,
                        msg="Metadata field is present")
        self.assertTrue(image.minDisk is not None,
                        msg="minDisk field is present")
        self.assertTrue(image.minRam is not None,
                        msg="minRam field is present")
        self.assertGreaterEqual(image.progress, 0,
                         msg=message.format('image progress', '100',
                                            image.progress))
        self.assertTrue(image.status is not None,
                        msg="Status field is present")
        self.assertTrue(image.updated is not None,
                        msg="Updated field is present")
        self.assertGreaterEqual(image.updated, image.created,
                                msg="Updated >= Created is present")