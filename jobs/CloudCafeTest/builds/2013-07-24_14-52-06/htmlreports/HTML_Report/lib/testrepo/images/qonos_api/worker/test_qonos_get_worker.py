from testrepo.common.testfixtures.images import BaseImagesFixture
from ccengine.common.constants.images_constants import Constants
from ccengine.common.decorators import attr
from ccengine.common.exceptions.compute import ItemNotFound
import ccengine.common.tools.datagen as datagen
import calendar
import time


class TestQonosGetWorker(BaseImagesFixture):

    @attr('positive')
    def test_happy_path_get_worker(self):
        '''Happy Path - Get details of worker'''

        """
        1) Create a worker
        2) Verify that the response code is 200
        3) Get details of the worker
        4) Verify that the auto-generated parameters (id, created-at,
           updated-at) are generated correctly
        5) Verify that the non-auto-generated parameters are created as entered

        Attributes to verify:
            host
            created_at
            updated_at
            id
        """

        host = datagen.random_string(size=10)
        msg = Constants.MESSAGE

        worker_obj = self.images_provider.create_active_workers(host)

        self.assertEquals(worker_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     worker_obj.status_code))

        worker = worker_obj.entity

        get_worker_obj = \
            self.images_provider.workers_client.get_worker(worker.id)

        self.assertEquals(get_worker_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     get_worker_obj.status_code))

        get_worker = get_worker_obj.entity

        worker_created_at_in_sec = \
            calendar.timegm(time.strptime(str(worker.created_at),
                                          "%Y-%m-%dT%H:%M:%SZ"))
        get_created_at_in_sec = \
            calendar.timegm(time.strptime(str(get_worker.created_at),
                                          "%Y-%m-%dT%H:%M:%SZ"))
        worker_updated_at_in_sec = \
            calendar.timegm(time.strptime(str(worker.updated_at),
                                          "%Y-%m-%dT%H:%M:%SZ"))
        get_updated_at_in_sec = \
            calendar.timegm(time.strptime(str(get_worker.updated_at),
                                          "%Y-%m-%dT%H:%M:%SZ"))

        created_at_diff_in_sec = \
            abs(worker_created_at_in_sec - get_created_at_in_sec)
        updated_at_diff_in_sec = \
            abs(worker_updated_at_in_sec - get_updated_at_in_sec)

        self.assertEquals(get_worker.host, worker.host,
                          msg.format('host', worker.host, get_worker.host))
        self.assertTrue(created_at_diff_in_sec <= 10,
                        msg.format('created_at', worker.created_at,
                                   get_worker.created_at))
        self.assertTrue(updated_at_diff_in_sec <= 10,
                        msg.format('updated_at', worker.updated_at,
                                   get_worker.updated_at))
        self.assertEquals(get_worker.id, worker.id,
                          msg.format('id', worker.id, get_worker.id))

    @attr('positive')
    def test_get_deleted_worker_details(self):
        '''Get details of deleted worker'''

        """
        1) Create a worker
        2) Verify that the response code is 200
        3) Delete the worker
        4) Verify that the response code is 200
        5) Get details of the deleted worker
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
