from ccengine.common.decorators import attr
from ccengine.common.exceptions.compute import ItemNotFound
from testrepo.common.testfixtures.images import BaseImagesFixture


class TestQonosListWorkersNegative(BaseImagesFixture):

    @attr('negative')
    def test_list_workers_method_mismatch(self):
        """List workers with method mismatch.

        1) Attempt to request the base url of '/workers' using a PUT
            method
        2) Verify that a correct validation message is returned
        """

        method = "PUT"

        with self.assertRaises(ItemNotFound):
            self.images_provider.workers_client. \
                list_workers(requestslib_kwargs={'method': method})

    @attr('negative')
    def test_list_workers_incorrect_url(self):
        """List workers with incorrect url.

        1) Attempt to request the base url of '/workerss'
        2) Verify that a correct validation message is returned
        """

        bad_url = "{0}/workerss".format(self.config.images.url)

        with self.assertRaises(ItemNotFound):
            self.images_provider.workers_client. \
                list_workers(requestslib_kwargs={'url': bad_url})
