from testrepo.common.testfixtures.images import BaseImagesFixture
from ccengine.common.constants.images_constants import Constants
from ccengine.common.decorators import attr
import unittest2 as unittest
from ccengine.common.exceptions.compute import ItemNotFound
import ccengine.common.tools.datagen as datagen


@unittest.skip("Class is not testable on h48/preprod/prod")
class TestQonosDeleteWorker(BaseImagesFixture):

    @attr('skip')
    def test_happy_path_delete_worker(self):
        '''Happy Path - Delete a valid worker'''

        """
        1) Create a worker
        2) Verify that the response code is 200
        3) Delete the worker
        4) Verify that the response code is 200
        5) Get the deleted worker
        6) Verify that the response code is 404
        """

        host = datagen.random_string(size=10)
        msg = Constants.MESSAGE

        worker_obj = self.images_provider.create_active_workers(host)

        self.assertEquals(worker_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     worker_obj.status_code))

        worker = worker_obj.entity

        del_worker_obj = \
            self.images_provider.workers_client.delete_worker(worker.id)

        self.assertEquals(del_worker_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     del_worker_obj.status_code))

        with self.assertRaises(ItemNotFound):
            self.images_provider.workers_client.get_worker(worker.id)

    @attr('skip')
    def test_delete_a_deleted_worker(self):
        '''Delete a deleted worker'''

        """
        1) Create a worker
        2) Verify that the response code is 200
        3) Delete the worker
        4) Verify that the response code is 200
        3) Delete the worker again
        4) Verify that the response code is 404
        5) Get the deleted worker
        6) Verify that the response code is 404
        """

        host = datagen.random_string(size=10)
        msg = Constants.MESSAGE

        worker_obj = self.images_provider.create_active_workers(host)

        self.assertEquals(worker_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     worker_obj.status_code))

        worker = worker_obj.entity

        del_worker_obj = \
            self.images_provider.workers_client.delete_worker(worker.id)

        self.assertEquals(del_worker_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     del_worker_obj.status_code))

        with self.assertRaises(ItemNotFound):
            self.images_provider.workers_client.delete_worker(worker.id)

        with self.assertRaises(ItemNotFound):
            self.images_provider.workers_client.get_worker(worker.id)
