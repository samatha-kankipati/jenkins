from testrepo.common.testfixtures.images import BaseImagesFixture
from ccengine.common.decorators import attr
from ccengine.common.exceptions.compute import BadRequest, ItemNotFound


class TestQonosListServersDetailOSSIFilterNegative(BaseImagesFixture):

    @attr('negative')
    def test_list_servers_detail_with_image_schedule_blank(self):
        '''List servers detail with image-schedule set to blank'''

        """
        1) List servers detail with image-schedule set to blank
        2) Verify that a correct validation message is returned
            """

        with self.assertRaises(BadRequest):
            self.images_provider.servers_client. \
                list_servers_with_detail(image_schedule='')

    @attr('negative')
    def test_list_servers_detail_with_image_schedule_does_not_exist(self):
        '''List servers detail with image-schedule set to bad value'''

        """
        1) List servers detail with image-schedule set to value that does not
            exist
        2) Verify that a correct validation message is returned
        """

        with self.assertRaises(BadRequest):
            self.images_provider.servers_client. \
                list_servers_with_detail(image_schedule='DoesNotExist')

    @attr('negative')
    def test_list_servers_detail_with_image_schedule_special_characters(self):
        '''List servers detail with image-schedule containing special
        characters'''

        """
        1) List servers detail with image-schedule containing special
            characters
        2) Verify that a correct validation message is returned
        """

        image_schedule = "*"

        with self.assertRaises(BadRequest):
            self.images_provider.servers_client. \
                list_servers_with_detail(image_schedule=image_schedule)

    @attr('negative')
    def test_list_servers_detail_with_image_schedule_true_including_body(self):
        '''Request including a body with image-schedule set to true'''

        """
        1) Create a valid server instance
        2) List servers using a request with a body and image-schedule filter
        3) Verify that the response code is 400
        """

        with self.assertRaises(ItemNotFound):
            self.images_provider.servers_client. \
                list_servers_with_detail_including_body(image_schedule="True")

    @attr('negative')
    def test_list_servers_detail_w_image_schedule_false_including_body(self):
        '''Request including a body with image-schedule set to false'''

        """
        1) Create a valid server instance
        2) List servers using a request with a body and image-schedule filter
        3) Verify that the response code is 400
        """

        with self.assertRaises(ItemNotFound):
            self.images_provider.servers_client. \
                list_servers_with_detail_including_body(image_schedule="False")
