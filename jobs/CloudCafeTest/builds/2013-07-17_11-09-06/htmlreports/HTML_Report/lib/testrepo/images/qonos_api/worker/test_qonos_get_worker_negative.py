from testrepo.common.testfixtures.images import BaseImagesFixture
from ccengine.common.decorators import attr
from ccengine.common.exceptions.compute import ItemNotFound


class TestQonosGetWorkerNegative(BaseImagesFixture):

    @classmethod
    def setUpClass(self):
        """ Retrieves the worker id used for tests in this class."""

        super(TestQonosGetWorkerNegative, self).setUpClass()

        list_workers_obj = self.images_provider.workers_client.list_workers()

        list_workers = list_workers_obj.entity

        self.worker_id = list_workers[0].id

    @attr('negative')
    def test_get_worker_method_mismatch(self):
        '''Get worker with method mismatch'''

        """
        1) Attempt to request the base url of '/worker/{id}' using a POST
            method
        2) Verify that a correct validation message is returned
        """

        method = "POST"
        worker_id = self.worker_id

        with self.assertRaises(ItemNotFound):
            self.images_provider.workers_client. \
                get_worker(id=worker_id, requestslib_kwargs={'method': method})

    @attr('negative')
    def test_get_worker_incorrect_url(self):
        '''Get worker with incorrect url'''

        """
        1) Attempt to request the base url of '/workers/{id}/work'
        2) Verify that a correct validation message is returned
        """

        worker_id = self.worker_id

        bad_url = "{0}/workers/{1}/work".format(self.config.images.url,
                                               worker_id)

        with self.assertRaises(ItemNotFound):
            self.images_provider.workers_client. \
                get_worker(id=worker_id, requestslib_kwargs={'url': bad_url})

    @attr('negative')
    def test_get_worker_with_blank_worker_id(self):
        '''Get details of worker using blank worker id'''

        """
        1) Get details of the worker using a blank worker id
        2) Verify that no worker is returned and that a correct
            validation message is returned
        """

        worker_id = ""

        with self.assertRaises(ItemNotFound):
            self.images_provider.workers_client.get_worker(worker_id)

    @attr('negative')
    def test_get_worker_for_non_existing_worker_id(self):
        '''Get details of worker for non-existing worker id'''

        """
        1) Get details of the worker using a non-existing worker id
        2) Verify that no worker is returned and that a correct
            validation message is returned
        """

        worker_id = "0"

        with self.assertRaises(ItemNotFound):
            self.images_provider.workers_client.get_worker(worker_id)

    @attr('negative')
    def test_get_worker_using_letters_for_worker_id(self):
        '''Get details of worker using letters for worker id'''

        """
        1) Get details of the worker using letters for worker id
        2) Verify that no worker is returned and that a correct
            validation message is returned
        """

        worker_id = "abcdef"

        with self.assertRaises(ItemNotFound):
            self.images_provider.workers_client.get_worker(worker_id)

    @attr('negative')
    def test_get_worker_using_special_characters_for_worker_id(self):
        '''Get details of worker using special characters for worker id'''

        """
        1) Get details of the worker using special characters for worker id
        2) Verify that no worker is returned and that a correct
            validation message is returned
        """

        worker_id = "<>"

        with self.assertRaises(ItemNotFound):
            self.images_provider.workers_client.get_worker(worker_id)

    @attr('negative')
    def test_get_worker_using_numbers_and_other_special_for_worker_id(self):
        '''Get details of worker using numbers and special characters other
        than - between number sets for worker id'''

        """
        1) Get details of the worker using numbers and special characters other
            than - between number sets for worker id
        2) Verify that no worker is returned and that a correct
            validation message is returned
        """

        worker_id = "055db37b&bdbf&4f95&9d4e&17af201ec75c"

        with self.assertRaises(ItemNotFound):
            self.images_provider.workers_client.get_worker(worker_id)

    @attr('negative')
    def test_get_worker_using_invalid_worker_id_format(self):
        '''Get details of worker using invalid worker id format'''

        """
        1) Get details of the worker using numbers and special characters other
            than - between number sets for worker id
        2) Verify that no worker is returned and that a correct
            validation message is returned
        """

        worker_id = "-{0}-".format(self.worker_id)

        with self.assertRaises(ItemNotFound):
            self.images_provider.workers_client.get_worker(worker_id)
