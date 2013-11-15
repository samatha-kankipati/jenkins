from testrepo.common.testfixtures.images import BaseImagesFixture
from ccengine.common.constants.images_constants import Constants
from ccengine.common.decorators import attr
from ccengine.common.exceptions.compute import ItemNotFound
import ccengine.common.tools.datagen as datagen
import calendar
import time


class TestQonosListWorkers(BaseImagesFixture):

    @attr('positive')
    def test_happy_path_list_workers(self):
        '''Happy Path - List workers'''

        """
        1) List workers
        2) Verify that the response code is 200
        3) Verify that there is at least 1 worker
        4) Verify that the worker is as expected

        Attributes to verify:
            process_id
        """

        count = 1
        msg = Constants.MESSAGE

        list_workers_obj = self.images_provider.workers_client.list_workers()
        self.assertEquals(list_workers_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     list_workers_obj.status_code))
        list_workers = list_workers_obj.entity

        self.assertTrue(len(list_workers) >= count,
                        msg.format("workers list", "At least 1",
                                   len(list_workers)))
        self.assertTrue(list_workers[0].process_id is not None,
                        msg.format("worker", "process id not None",
                                   list_workers[0].process_id))

    @attr('positive')
    def test_list_workers_with_multiple_workers(self):
        '''List workers with multiple workers'''

        """
        1) List workers
        2) Verify that the response code is 200
        3) Verify that there is at least 2 workers
        """

        count = 2
        msg = Constants.MESSAGE

        list_workers_obj = self.images_provider.workers_client.list_workers()
        self.assertEquals(list_workers_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     list_workers_obj.status_code))
        list_workers = list_workers_obj.entity

        self.assertTrue(len(list_workers) >= count,
                        msg.format("workers list", "more than 1",
                                   len(list_workers)))

    @attr('positive')
    def test_list_workers_for_deleted_worker(self):
        '''List workers for deleted worker'''

        """
        1) Create a worker
        2) Delete the worker
        3) List workers
        4) Verify that the response code is 200
        5) Get worker
        5) Verify that the response code is 404
        """

        host = datagen.random_string(size=10)
        msg = Constants.MESSAGE

        worker = self.images_provider.create_active_workers(host)

        self.assertEquals(worker.status_code, 200,
                          msg.format('status_code', 200, worker.status_code))

        del_worker_obj = \
            self.images_provider.workers_client.delete_worker(worker.entity.id)

        self.assertEquals(del_worker_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     del_worker_obj.status_code))

        with self.assertRaises(ItemNotFound):
            self.images_provider.workers_client.get_worker(worker.entity.id)

    @attr('skip')
    def test_happy_path_list_registered_workers(self):
        '''Happy Path - List registered workers'''

        """
        1) Create a worker
        2) List workers
        3) Verify that the response code is 200
        4) Verify that the length of the workers is 1
        5) Verify that the worker is as expected

        Attributes to verify:
            host
            created_at
            updated_at
            id
        """

        host = datagen.random_string(size=10)
        count = 1
        msg = Constants.MESSAGE

        worker_obj = self.images_provider.create_active_workers(host)
        self.assertEquals(worker_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     worker_obj.status_code))

        worker = worker_obj.entity

        list_workers_obj = self.images_provider.workers_client.list_workers()
        self.assertEquals(list_workers_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     list_workers_obj.status_code))

        list_workers = []
        for tmp_worker in list_workers_obj.entity:
            if tmp_worker.host == host:
                list_workers.append(tmp_worker)

        self.assertTrue(len(list_workers) == count,
                        msg.format("length of the list", count,
                                   len(list_workers)))

        listed_worker = list_workers[0]

        worker_created_at_in_sec = \
            calendar.timegm(time.strptime(str(worker.created_at),
                                          "%Y-%m-%dT%H:%M:%SZ"))
        listed_created_at_in_sec = \
            calendar.timegm(time.strptime(str(listed_worker.created_at),
                                          "%Y-%m-%dT%H:%M:%SZ"))
        worker_updated_at_in_sec = \
            calendar.timegm(time.strptime(str(worker.updated_at),
                                          "%Y-%m-%dT%H:%M:%SZ"))
        listed_updated_at_in_sec = \
            calendar.timegm(time.strptime(str(listed_worker.updated_at),
                                          "%Y-%m-%dT%H:%M:%SZ"))

        created_at_diff_in_sec = \
            abs(worker_created_at_in_sec - listed_created_at_in_sec)
        updated_at_diff_in_sec = \
            abs(worker_updated_at_in_sec - listed_updated_at_in_sec)

        self.assertEquals(listed_worker.host, worker.host,
                          msg.format('host', worker.host, listed_worker.host))
        self.assertTrue(created_at_diff_in_sec <= 10,
                        msg.format('created_at', worker.created_at,
                                   listed_worker.created_at))
        self.assertTrue(updated_at_diff_in_sec <= 10,
                        msg.format('updated_at', worker.updated_at,
                                   listed_worker.updated_at))
        self.assertEquals(listed_worker.id, worker.id,
                          msg.format('id', worker.id, listed_worker.id))

    @attr('skip')
    def test_list_workers_with_multiple_registered_workers(self):
        '''List workers with multiple registered workers'''

        """
        1) Create a worker
        2) Create another worker
        3) List workers
        4) Verify that the response code is 200
        5) Verify that the length of the workers is 2
        6) Verify that the worker is as expected

        Attributes to verify:
            host
            created_at
            updated_at
            id
        """

        host = datagen.random_string(size=10)
        alt_host = datagen.random_string(size=10)
        msg = Constants.MESSAGE
        msg_alt = Constants.MESSAGE_ALT
        count = 2

        worker_obj = self.images_provider.create_active_workers(host)

        self.assertEquals(worker_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     worker_obj.status_code))

        worker = worker_obj.entity

        alt_worker_obj = \
            self.images_provider.create_active_workers(alt_host)

        self.assertEquals(alt_worker_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     alt_worker_obj.status_code))

        alt_worker = alt_worker_obj.entity

        list_workers_obj = self.images_provider.workers_client.list_workers()
        self.assertEquals(list_workers_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     list_workers_obj.status_code))

        list_workers = []
        for tmp_worker in list_workers_obj.entity:
            if tmp_worker.host == host or tmp_worker.host == alt_host:
                list_workers.append(tmp_worker)

        self.assertTrue(len(list_workers) == count,
                        msg.format("length of the list", count,
                                   len(list_workers)))

        for l_worker in list_workers:
            if l_worker.host == worker.host:

                worker_created_at_in_sec = \
                    calendar.timegm(time.strptime(str(worker.created_at),
                                                  "%Y-%m-%dT%H:%M:%SZ"))
                listed_created_at_in_sec = \
                    calendar.timegm(time.strptime(str(l_worker.created_at),
                                                  "%Y-%m-%dT%H:%M:%SZ"))
                worker_updated_at_in_sec = \
                    calendar.timegm(time.strptime(str(worker.updated_at),
                                                  "%Y-%m-%dT%H:%M:%SZ"))
                listed_updated_at_in_sec = \
                    calendar.timegm(time.strptime(str(l_worker.updated_at),
                                                  "%Y-%m-%dT%H:%M:%SZ"))

                created_at_diff_in_sec = \
                    abs(worker_created_at_in_sec - listed_created_at_in_sec)
                updated_at_diff_in_sec = \
                    abs(worker_updated_at_in_sec - listed_updated_at_in_sec)

                self.assertTrue(created_at_diff_in_sec <= 10,
                                msg.format('created_at', worker.created_at,
                                           l_worker.created_at))
                self.assertTrue(updated_at_diff_in_sec <= 10,
                                msg.format('updated_at', worker.updated_at,
                                           l_worker.updated_at))
                self.assertEquals(l_worker.id, worker.id,
                                  msg.format('id', worker.id,
                                             l_worker.id))
            elif l_worker.host == alt_worker.host:

                alt_worker_cre_at_in_sec = \
                    calendar.timegm(time.strptime(str(alt_worker.created_at),
                                                  "%Y-%m-%dT%H:%M:%SZ"))
                listed_cre_at_in_sec = \
                    calendar.timegm(time.strptime(str(l_worker.created_at),
                                                  "%Y-%m-%dT%H:%M:%SZ"))
                alt_worker_upd_at_in_sec = \
                    calendar.timegm(time.strptime(str(alt_worker.updated_at),
                                                  "%Y-%m-%dT%H:%M:%SZ"))
                listed_upd_at_in_sec = \
                    calendar.timegm(time.strptime(str(l_worker.updated_at),
                                                  "%Y-%m-%dT%H:%M:%SZ"))

                created_at_diff_in_sec = \
                    abs(alt_worker_cre_at_in_sec - listed_cre_at_in_sec)
                updated_at_diff_in_sec = \
                    abs(alt_worker_upd_at_in_sec - listed_upd_at_in_sec)

                self.assertTrue(created_at_diff_in_sec <= 10,
                                msg.format('created_at',
                                           alt_worker.created_at,
                                           l_worker.created_at))
                self.assertTrue(updated_at_diff_in_sec <= 10,
                                msg.format('updated_at',
                                           alt_worker.updated_at,
                                           l_worker.updated_at))
                self.assertEquals(l_worker.id, alt_worker.id,
                                  msg.format('id', alt_worker.id,
                                             l_worker.id))
            else:
                self.fail(msg_alt.format('host', worker.host, alt_worker.host,
                                     l_worker.host))
