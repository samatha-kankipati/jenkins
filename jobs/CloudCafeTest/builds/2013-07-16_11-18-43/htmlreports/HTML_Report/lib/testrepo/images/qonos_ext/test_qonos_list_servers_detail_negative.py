from testrepo.common.testfixtures.images import BaseImagesFixture
from ccengine.common.decorators import attr
from ccengine.common.exceptions.compute import ItemNotFound


class TestQonosListServersDetailNegative(BaseImagesFixture):

    @attr('negative')
    def test_list_servers_detail_request_including_body(self):
        '''List servers detail request including body'''

        """
        1) List servers detail using a request with a body
        2) Verify that the response code is 400
        """

        with self.assertRaises(ItemNotFound):
            self.images_provider.servers_client. \
                list_servers_with_detail_including_body()
