from testrepo.common.testfixtures.compute import CreateServerFixture
from ccengine.common.tools.datagen import rand_name
from ccengine.domain.types import NovaImageStatusTypes
from ccengine.common.decorators import attr


class ImagesTest(CreateServerFixture):

    @classmethod
    def setUpClass(cls):
        super(ImagesTest, cls).setUpClass()
        cls.name = rand_name('testserver')
        cls.server = cls.server_response.entity

    @classmethod
    def tearDownClass(cls):
        super(ImagesTest, cls).tearDownClass()

    @attr(type='smoke', net='no')
    def test_create_delete_image(self):
        """An image for the provided server should be created"""

        name = rand_name('testimage')
        server_id = self.server.id
        image_response = self.servers_client.create_image(server_id, name)
        image_id = self.parse_image_id(image_response)
        self.compute_provider.wait_for_image_status(image_id,
                                                    NovaImageStatusTypes.ACTIVE)

        # Delete image and wait for image to be deleted
        self.compute_provider.wait_for_image_to_be_deleted(image_id)

    @attr(type='smoke', net='no')
    def test_get_image(self):
        '''The expected image should be returned'''
        image_response = self.images_client.get_image(self.image_ref)
        image = image_response.entity
        self.assertEqual(self.image_ref, image.id,
                         "Could not retrieve the expected image with id %s" %
                         (image.id))
