from testrepo.common.testfixtures.compute import ComputeFixture
from ccengine.common.exceptions.compute import ItemNotFound
from ccengine.common.decorators import attr


class ImagesMetadataNegativeTest(ComputeFixture):

    @attr(type='negative', net='no')
    def test_list_image_metadata_for_nonexistent_image(self):
        """List on nonexistent image metadata should fail"""
        with self.assertRaises(ItemNotFound):
            self.images_client.list_image_metadata(999)

    @attr(type='negative', net='no')
    def test_get_image_metadata_item_for_nonexistent_image(self):
        """Get metadata of a nonexistent image should fail"""
        with self.assertRaises(ItemNotFound):
            self.images_client.get_image_metadata_item(999, 'key2')

    @attr(type='negative', net='no')
    def test_set_image_metadata_item_for_nonexistent_image(self):
        """"Metadata item should not be set for a nonexistent image"""
        meta = {'meta_key_1': 'meta_value_1'}
        with self.assertRaises(ItemNotFound):
                self.images_client.set_image_metadata_item(999, 'meta_key_1',
                                                           'meta_value_1')

    @attr(type='negative', net='no')
    def test_delete_image_metadata_item_for_nonexistent_image(self):
        """Should not be able to delete metadata item of nonexistent image"""
        try:
            self.images_client.delete_image_metadata_item(999, 'key1')
            self.fail("No exception thrown for delete image metadata for non existent image")
        except:
            pass
