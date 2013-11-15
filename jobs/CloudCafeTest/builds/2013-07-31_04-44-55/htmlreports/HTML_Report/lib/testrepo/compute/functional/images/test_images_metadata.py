from testrepo.common.testfixtures.compute import ComputeFixture
from ccengine.common.tools.datagen import rand_name
from ccengine.common.exceptions.compute import ItemNotFound, OverLimit
from ccengine.common.decorators import attr
from ccengine.domain.types import NovaImageStatusTypes
import unittest2 as unittest


class ImagesMetadataTest(ComputeFixture):

    @classmethod
    def setUpClass(cls):
        super(ImagesMetadataTest, cls).setUpClass()
        metadata_limit = cls.limits_client.get_max_image_meta()
        if metadata_limit is None:
            cls.limits_set = False
        else:
            cls.limits_set = True

    def setUp(self):
        self.server_resp = self.compute_provider.create_active_server()
        self.server_id = self.server_resp.entity.id
        self.resources.add(self.server_id, self.servers_client.delete_server)
        meta = {'key1': 'value1', 'key2': 'value2'}
        name = rand_name('testimage')
        image_resp = self.servers_client.create_image(self.server_id, name, meta)
        self.image_id = self.parse_image_id(image_resp)
        self.resources.add(self.image_id, self.images_client.delete_image)
        self.compute_provider.wait_for_image_resp_code(self.image_id, 200)
        self.compute_provider.wait_for_image_status(self.image_id, NovaImageStatusTypes.ACTIVE)
        self.image = self.images_client.get_image(self.image_id)

    @classmethod
    def tearDownClass(cls):
        super(ImagesMetadataTest, cls).tearDownClass()

    @attr(type='negative', net='no')
    def test_delete_nonexistant_image_metadata_item(self):
        """User should not be able to delete a metadata which does not exist"""
        with self.assertRaises(ItemNotFound):
            self.images_client.delete_image_metadata_item(self.image_id,
                                                          'meta_key_5')

    @attr(type='negative', net='no')
    def test_get_nonexistent_image_metadata_item(self):
        """User should not be able to perform a get on an image metadata which does not exist"""
        with self.assertRaises(ItemNotFound):
            self.images_client.get_image_metadata_item(self.image_id,
                                                       'meta_key_5')

    @attr(type='positive', net='no')
    def test_list_image_metadata(self):
        """All metadata key/value pairs for an image should be returned"""
        image_metadata = self.images_client.list_image_metadata(self.image_id)
        self.assertEqual('value1', image_metadata.entity.key1,
                         "The metadata is not same as expected.")
        self.assertEqual('value2', image_metadata.entity.key2,
                         "The metadata is not same as expected.")

    @attr(type='positive', net='no')
    def test_set_image_metadata(self):
        """Test user should be able to set the metadata of an image"""
        meta = {'key3': 'meta3', 'key4': 'meta4'}
        self.images_client.set_image_metadata(self.image_id, meta)

        image_metadata = self.images_client.list_image_metadata(self.image_id)
        self.assertEqual('meta3', image_metadata.entity.key3,
                         "The metadata is not same as expected.")
        self.assertEqual('meta4', image_metadata.entity.key4,
                         "The metadata is not same as expected.")
        self.assertFalse(hasattr(image_metadata.entity, 'key1'))
        self.assertFalse(hasattr(image_metadata.entity, 'key2'))

    @attr(type='positive', net='no')
    def test_create_image_with_max_number_of_metadata_items(self):
        """Create an image with maximum number of metadata allowed"""
        metadata_limit = self.limits_client.get_max_image_meta()
        expected_metadata = {}
        for i in range(int(metadata_limit)):
            expected_metadata['metakey' + str(i)] = 'metavalue' + str(i)

        name = rand_name('testimage')
        image_resp = self.servers_client.create_image(self.server_id,
                                                      name, expected_metadata)
        image_id = self.parse_image_id(image_resp)
        self.compute_provider.wait_for_image_resp_code(image_id, 200)
        self.compute_provider.wait_for_image_status(image_id, NovaImageStatusTypes.ACTIVE)

        metadata_resp = self.images_client.list_image_metadata(image_id)
        metadata_dict = vars(metadata_resp.entity)
        for key, value in expected_metadata.items():
            self.assertEqual(value, metadata_dict[key],
                             "The metadata values do not match.")

    @attr(type='negative', net='no')
    def test_create_image_with_more_than_max_number_of_metadata_items(self):
        """User should not be able to create an image with more then max number of metadata item"""
        metadata_limit = self.limits_client.get_max_image_meta()
        expected_metadata = {}
        for i in range(int(metadata_limit) + 1):
            expected_metadata['metakey' + str(i)] = 'metavalue' + str(i)

        with self.assertRaises(OverLimit):
            name = rand_name('testimage')
            image_resp = self.servers_client.create_image(self.server_id, name,
                                                          expected_metadata)

    @attr(type='positive', net='no')
    @unittest.skip('Bug:lp897807')
    def test_update_image_metadata(self):
        """Verify user should be able to update the metadata"""
        meta = {'key1': 'alt1', 'key2': 'alt2'}
        self.images_client.update_image_metadata(self.image_id, meta)

        metadata_resp = self.images_client.list_image_metadata(self.image_id)
        metadata_dict = vars(metadata_resp.entity)
        self.assertEqual('alt1', metadata_dict['key1'],
                         "The metadata value did not get updated")
        self.assertEqual('alt2', metadata_dict['key2'],
                         "The metadata value did not get updated")

    @attr(type='positive', net='no')
    def test_get_image_metadata_item(self):
        """The value for a specific metadata key should be returned"""
        meta_resp = self.images_client.get_image_metadata_item(self.image_id, 'key2')
        self.assertTrue('value2', meta_resp.text)

    @attr(type='positive', net='no')
    @unittest.skip('Bug:lp897807')
    def test_add_image_metadata_item(self):
        """ The value provided for the given meta
                item should be set for the image"""

        name = rand_name('testimage')
        image_resp = self.servers_client.create_image(self.server_id, name)
        image_id = self.parse_image_id(image_resp)
        self.compute_provider.wait_for_image_resp_code(image_id, 200)
        self.compute_provider.wait_for_image_status(image_id,
                                                    NovaImageStatusTypes.ACTIVE)

        meta = {'nova': 'alt'}
        self.images_client.set_image_metadata_item(image_id, 'nova', meta)
        metadata_resp = self.images_client.list_image_metadata(image_id)
        metadata_dict = vars(metadata_resp.entity)
        self.assertEqual('alt', metadata_dict['nova'],
                         "The metadata did not get added.")

    @attr(type='positive', net='no')
    def test_delete_image_metadata_item(self):
        """The metadata value/key pair should be deleted from the image"""

        self.images_client.delete_image_metadata_item(self.image_id, 'key1')
        metadata_resp = self.images_client.list_image_metadata(self.image_id)
        self.assertFalse(hasattr(metadata_resp.entity, 'key1'),
                         msg="The metadata did not get deleted.")
