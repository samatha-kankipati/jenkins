from testrepo.common.testfixtures.compute import CreateServerFixture
from ccengine.common.exceptions.compute import ItemNotFound
from ccengine.domain.types import NovaImageStatusTypes
from ccengine.common.decorators import attr


class ImagesTest(CreateServerFixture):

    @classmethod
    def setUpClass(cls):
        super(ImagesTest, cls).setUpClass()
        cls.server = cls.server_response.entity

    @classmethod
    def tearDownClass(cls):
        super(ImagesTest, cls).tearDownClass()

    @attr(type='negative', net='no')
    def test_create_image_invalid_server_id(self):
        """Image creation should fail if the server id does not exist"""
        with self.assertRaises(ItemNotFound):
            self.servers_client.create_image(999, 'test_neg')

    @attr(type='negative', net='no')
    def test_delete_image_invalid_id(self):
        """Image deletion should fail if the image id does not exist"""
        with self.assertRaises(ItemNotFound):
            self.images_client.delete_image(999)

    @attr(type='negative', net='no')
    def test_create_image_invalid_server_name(self):
        """Image creation should fail if the image name is blank"""
        try:
            image_resp = self.servers_client.create_image(self.server.id, '')
        except:
            pass
        else:
            image_id = self.parse_image_id(image_resp)
            self.images_client.wait_for_image_resp_code(image_id, 200)
            self.images_client.wait_for_image_status(image_id,
                                                     NovaImageStatusTypes.ACTIVE)
            self.images_client.delete_image(image_id)
            self.fail('The create request should have failed since the name was blank.')
