from testrepo.common.testfixtures.images import BaseImagesFixture
from ccengine.common.decorators import attr
from ccengine.common.exceptions.compute import ItemNotFound


class TestQonosBaseUrlNegative(BaseImagesFixture):

    @attr('negative')
    def test_qonos_api_request_incorrect_base_url(self):
        '''Qonos api request incorrect base URL'''

        """
        1) Attempt to request the base url of '/schedulestest'
        2) Verify that the response code is 404
        """

        bad_url = "{0}/schedulestest".format(self.config.images.url)

        with self.assertRaises(ItemNotFound):
            self.images_provider.schedules_client. \
                list_schedules(requestslib_kwargs={'url': bad_url})
