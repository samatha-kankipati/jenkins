from testrepo.common.testfixtures.images import BaseImagesFixture
from ccengine.common.constants.images_constants import Constants
from ccengine.common.decorators import attr
import ccengine.common.tools.datagen as datagen
import unittest2 as unittest
import calendar
import time
import re


@unittest.skip("Class is not testable on h48/preprod/prod")
class TestQonosCreateWorker(BaseImagesFixture):

    @attr('skip')
    def test_happy_path_create_worker(self):
        '''Happy Path - Create and register valid worker'''

        """
        1) Create a worker using valid parameters
        2) Verify that the response code is 200
        3) Get the worker
        4) Verify that the worker contains the passed parameters with auto
            generated attributes and values

        Attributes to verify:
            host
            created_at
            updated_at
            id
        """

        host = datagen.random_string(size=10)
        id_re = re.compile(Constants.ID_RE)
        msg = Constants.MESSAGE

        worker_obj = self.images_provider.create_active_workers(host)

        worker_creation_time_in_sec = calendar.timegm(time.gmtime())

        self.assertEquals(worker_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     worker_obj.status_code))

        worker = worker_obj.entity

        created_at_in_sec = \
            calendar.timegm(time.strptime(str(worker.created_at),
                                          "%Y-%m-%dT%H:%M:%SZ"))

        offset_in_worker_created_time = \
            abs(created_at_in_sec - worker_creation_time_in_sec)

        updated_at_in_sec = \
            calendar.timegm(time.strptime(str(worker.updated_at),
                                          "%Y-%m-%dT%H:%M:%SZ"))
        offset_in_worker_updated_time = \
            abs(updated_at_in_sec - worker_creation_time_in_sec)

        self.assertEquals(worker.host, host,
                          msg.format('host', host, worker.host))
        self.assertTrue(offset_in_worker_created_time <= 60000,
                        msg.format('created_at',
                                   'value less than or equal to 60000',
                                   offset_in_worker_created_time))
        self.assertTrue(offset_in_worker_updated_time <= 60000,
                        msg.format('updated_at',
                                   'value less than or equal to 60000',
                                   offset_in_worker_updated_time))
        self.assertTrue(id_re.match(worker.id) != None,
                        msg.format('id', 'valid worker id', worker.id))

    @attr('skip')
    def test_create_multiple_workers_on_different_hosts(self):
        '''Create multiple workers on different hosts'''

        """
        1) Create a worker using valid host
        2) Verify that the response code is 200
        3) Create another worker using different host
        4) Verify that the list workers contains both workers with
            auto generated attributes and values

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

    @attr('skip')
    def test_create_multiple_workers_on_same_host(self):
        '''Create multiple workers on same host'''

        """
        1) Create a worker using valid host
        2) Verify that the response code is 200
        3) Create another worker using same host
        4) Verify that the list workers contains both workers with
            auto generated attributes and values

        Attributes to verify:
            host
            created_at
            updated_at
            process_id
            id
        """

        host = datagen.random_string(size=10)
        msg = Constants.MESSAGE
        msg_alt = Constants.MESSAGE_ALT
        count = 2

        worker_obj = self.images_provider.create_active_workers(host)

        self.assertEquals(worker_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     worker_obj.status_code))

        worker = worker_obj.entity

        alt_worker_obj = self.images_provider.create_active_workers(host)

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
            if tmp_worker.host == host:
                list_workers.append(tmp_worker)

        self.assertTrue(len(list_workers) == count,
                        msg.format("length of the list", count,
                                   len(list_workers)))

        for l_worker in list_workers:
            if l_worker.id == worker.id:

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
                self.assertEquals(l_worker.process_id, worker.process_id,
                                  msg.format('process_id', worker.process_id,
                                             l_worker.process_id))
                self.assertEquals(l_worker.host, worker.host,
                                  msg.format('host', worker.host,
                                             l_worker.host))
            elif l_worker.id == alt_worker.id:

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
                                msg.format('created_at',
                                           alt_worker.created_at,
                                           l_worker.created_at))
                self.assertTrue(updated_at_diff_in_sec <= 10,
                                msg.format('updated_at',
                                           alt_worker.updated_at,
                                           l_worker.updated_at))
                self.assertEquals(l_worker.process_id, worker.process_id,
                                  msg.format('process_id', worker.process_id,
                                             l_worker.process_id))
                self.assertEquals(l_worker.host, alt_worker.host,
                                  msg.format('host', alt_worker.host,
                                             l_worker.host))
            else:
                self.fail(msg_alt.format('id', worker.id, alt_worker.id,
                                         l_worker.id))
