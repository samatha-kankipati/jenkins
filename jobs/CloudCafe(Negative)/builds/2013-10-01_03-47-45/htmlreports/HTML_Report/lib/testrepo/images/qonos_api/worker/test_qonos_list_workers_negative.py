from testrepo.common.testfixtures.images import BaseImagesFixture
from ccengine.common.decorators import attr
from ccengine.common.exceptions.compute import ItemNotFound


class TestQonosListWorkersNegative(BaseImagesFixture):

    @attr('negative')
    def test_list_workers_method_mismatch(self):
        '''List workers with method mismatch'''

        """
        1) Attempt to request the base url of '/workers' using a PUT
            method
        2) Verify that a correct validation message is returned
        """

        http_method = "PUT"

        with self.assertRaises(ItemNotFound):
            self.images_provider.workers_client. \
                list_workers(http_method=http_method)

    @attr('negative')
    def test_list_workers_incorrect_url(self):
        '''List workers with incorrect url'''

        """
        1) Attempt to request the base url of '/workerss'
        2) Verify that a correct validation message is returned
        """

        url_addition = 's'

        with self.assertRaises(ItemNotFound):
            self.images_provider.workers_client. \
                list_workers(url_addition=url_addition)
