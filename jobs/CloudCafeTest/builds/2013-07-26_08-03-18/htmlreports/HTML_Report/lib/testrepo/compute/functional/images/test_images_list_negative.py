from testrepo.common.testfixtures.compute import ComputeFixture
from ccengine.common.exceptions.compute import BadRequest
from ccengine.common.decorators import attr


class ImagesListTestNegative(ComputeFixture):

    @attr(type='negative', net='no')
    def test_list_images_filter_by_nonexistent_server_id(self):
        """Negative Test: Images should not get listed with invalid server ID"""
        server_id = 'sjlfdlkjfldjlkdjfldjf'
        images = self.images_client.list_images(server_ref=server_id)
        self.assertEqual(200, images.status_code,
                         "The response code is not 200")
        self.assertEqual(0, len(images.entity),
                         "The list of images is not empty.")

    @attr(type='negative', net='no')
    def test_list_images_filter_by_nonexistent_image_name(self):
        """Images should not get listed when filtered with invalid image name"""
        image_name = 'aljsdjfsjkljlkjdfkjs999'
        images = self.images_client.list_images(image_name=image_name)
        self.assertEqual(200, images.status_code,
                         "The response code is not 200.")
        self.assertEqual(0, len(images.entity),
                         "The list of images is not empty.")

    @attr(type='negative', net='no')
    def test_list_images_filter_by_invalid_image_status(self):
        """Images should not get listed when filtered with invalid status"""
        image_status = 'INVALID'
        images = self.images_client.list_images(status=image_status)
        self.assertEqual(200, images.status_code,
                         "The response code is not 200.")
        self.assertEqual(0, len(images.entity),
                         "The list of images is not empty.")

    @attr(type='negative', net='no')
    def test_list_images_filter_by_invalid_marker(self):
        """Images should not get listed when filtered with invalid marker"""
        marker = 999
        with self.assertRaises(BadRequest):
            self.images_client.list_images(marker=marker)

    @attr(type='negative', net='no')
    def test_list_images_filter_by_invalid_type(self):
        """Images should not get listed when filtered with invalid type"""
        type = 'INVALID'
        images = self.images_client.list_images(image_type=type)
        self.assertEqual(200, images.status_code,
                         "The response code is not 200.")
        self.assertEqual(0, len(images.entity),
                         "The list of images is not empty")

    @attr(type='negative', net='no')
    def test_list_images_filter_by_invalid_changes_since(self):
        """Images should not get listed with invalid changes since"""
        changes_since = '2012-02-22T'
        with self.assertRaises(BadRequest):
            self.images_client.list_images(changes_since=changes_since)

    @attr(type='negative', net='no')
    def test_list_images_filter_by_invalid_limit(self):
        """Images should not get listed with invalid limit"""
        limit = -3
        with self.assertRaises(BadRequest):
            self.images_client.list_images(limit=limit)
