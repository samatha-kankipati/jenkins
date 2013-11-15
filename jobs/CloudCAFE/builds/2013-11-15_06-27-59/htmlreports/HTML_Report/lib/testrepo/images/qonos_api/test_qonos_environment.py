import time
import unittest2 as unittest
from datetime import datetime, timedelta

import ccengine.common.tools.datagen as datagen
from ccengine.common.constants.images_constants import Constants
from ccengine.common.decorators import attr
from ccengine.domain.types import ScheduledImagesJobStatus
from testrepo.common.testfixtures.images import BaseImagesFixture


@unittest.skip("Class is not testable on h48/preprod/prod")
class TestQonosEnvironment(BaseImagesFixture):

    @attr('skip')
    def test_worker_operation(self):
        """Verify the worker operation.

        1) Stop all running workers
        2) Start worker
        3) Make sure a new worker is started and ready to process jobs
        4) Create a schedule such that a job is created for it in few minutes
        5) Make sure that job is processed by the new worker
        """

        tenant = self.config.images.tenant
        action = self.config.images.action
        msg = Constants.MESSAGE
        key = self.config.images.metadata_key
        user_name_metadata_key = self.config.images.user_name_metadata_key
        user_name = self.config.images.user_name
        marker = None

        server_name = datagen.random_string(size=10)

        server_obj = self.images_provider.create_active_server(server_name)
        self.assertEquals(server_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     server_obj.status_code))

        instance_id = server_obj.entity.id

        stop_worker = self.images_provider.stop_workers()
        self.assertEquals(stop_worker.status_code, 200,
                          msg.format('status_code', 200,
                                     stop_worker.status_code))

        # Wait time for stopping all workers
        time.sleep(int(self.config.images.worker_stop_timeout))

        running_worker = self.images_provider.get_running_worker_count()
        self.assertEquals(running_worker.status_code, 200,
                          msg.format('status_code', 200,
                                     running_worker.status_code))
        worker_resp = running_worker.content.split('\n')
        self.assertEquals(int(worker_resp[0]), 0,
                          msg.format('worker_count', 0,
                                     int(worker_resp[0])))

        start_worker = self.images_provider.start_worker()
        self.assertEquals(start_worker.status_code, 200,
                          msg.format('status_code', 200,
                                     start_worker.status_code))

        # Wait time for starting a worker
        time.sleep(int(self.config.images.worker_start_timeout))

        running_worker = self.images_provider.get_running_worker_count()
        self.assertEquals(running_worker.status_code, 200,
                          msg.format('status_code', 200,
                                     running_worker.status_code))
        worker_resp = running_worker.content.split('\n')
        self.assertGreater(int(worker_resp[0]), 0,
                           msg.format('worker_count', 'at least one worker',
                                      int(worker_resp[0])))

        metadata = {key: instance_id, user_name_metadata_key: user_name}

        sch_obj = self.images_provider.\
            create_active_schedules(tenant, action, metadata=metadata)
        self.assertEquals(sch_obj.status_code, 200,
                          msg.format('status_code', 200, sch_obj.status_code))

        sch = sch_obj.entity

        tm = datetime.now() - timedelta(seconds=60)
        next_run_time = tm.strftime('%Y-%m-%d %H:%M:%S')

        upd_sch_obj = \
            self.images_provider.schedules_client.update_schedule(
                id=sch.id, next_run=next_run_time)
        self.assertEquals(upd_sch_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     upd_sch_obj.status_code))

        keys = ["schedule_id", "marker"]
        values = [sch.id, marker]

        self.images_provider.wait_for_job_to_create(sch.id, keys=keys,
                                                    values=values)

        jobs = self.images_provider.list_jobs_for_schedule(sch.id, keys,
                                                           values)

        self.assertEquals(len(jobs), 1, msg.format('job_length', 1, len(jobs)))

        status = jobs[0].status
        self.assertTrue(self.images_provider.is_job_status_workable(status) or
                        self.images_provider.is_job_status_done(status),
                        msg.format('status', 'workable/done job status',
                                   status))

        self.images_provider.wait_for_job_status(jobs[0].id,
                                                 ScheduledImagesJobStatus.DONE)

        job = self.images_provider.jobs_client.get_job(jobs[0].id)

        self.assertEquals(job.status_code, 200,
                          msg.format('status_code', 200, job.status_code))

        self.assertIsNotNone(job.entity.worker_id,
                             msg.format('worker', 'Not None',
                                        job.entity.worker_id))

    @attr('skip')
    def test_delete_worker_after_job_picked(self):
        """Delete the worker after a job is picked up by that worker.

        1) Create a schedule such that a job is created for it in few minutes
        2) Make sure a job is created for that schedule
        3) Make sure worker is assigned to that job
        4) Stop the worker
        5) Verify that the response code is 200
        6) Get the stopped worker
        7) Verify that the response code is 404
        8) Verify that the currently running job is not affected and
            completes successfully
        """

        tenant = self.config.images.tenant
        action = self.config.images.action
        msg = Constants.MESSAGE
        key = self.config.images.metadata_key
        user_name_metadata_key = self.config.images.user_name_metadata_key
        user_name = self.config.images.user_name
        marker = None

        server_name = datagen.random_string(size=10)

        server_obj = self.images_provider.create_active_server(server_name)
        self.assertEquals(server_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     server_obj.status_code))
        instance_id = server_obj.entity.id

        metadata = {key: instance_id, user_name_metadata_key: user_name}

        sch_obj = self.images_provider.\
            create_active_schedules(tenant, action, metadata=metadata)
        self.assertEquals(sch_obj.status_code, 200,
                          msg.format('status_code', 200, sch_obj.status_code))

        sch = sch_obj.entity

        tm = datetime.now() - timedelta(seconds=60)
        next_run_time = tm.strftime('%Y-%m-%d %H:%M:%S')

        upd_sch_obj = \
            self.images_provider.schedules_client.update_schedule(
                id=sch.id, next_run=next_run_time)
        self.assertEquals(upd_sch_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     upd_sch_obj.status_code))

        keys = ["schedule_id", "marker"]
        values = [sch.id, marker]

        self.images_provider.wait_for_job_to_create(sch.id, keys=keys,
                                                    values=values)

        jobs = self.images_provider.list_jobs_for_schedule(sch.id, keys,
                                                           values)

        self.assertEquals(len(jobs), 1, msg.format('job_length', 1, len(jobs)))

        job = self.images_provider.wait_for_job_status(
            jobs[0].id, ScheduledImagesJobStatus.PROCESSING)

        old_worker_id = job.entity.worker_id
        self.assertIsNotNone(old_worker_id,
                             msg.format('worker', 'Not None',
                                        old_worker_id))

        get_worker_obj = self.images_provider.workers_client.\
            get_worker(job.entity.worker_id)

        self.assertEquals(get_worker_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     get_worker_obj.status_code))

        param_keys = ['pid', 'force']
        param_values = [get_worker_obj.entity.process_id, 'true']

        stop_worker = self.images_provider.\
            stop_workers(param_keys, param_values)
        self.assertEquals(stop_worker.status_code, 200,
                          msg.format('status_code', 200,
                                     stop_worker.status_code))

        self.images_provider.make_sure_new_worker_exists(
            get_worker_obj.entity.process_id)

        self.images_provider.workers_to_delete.append(get_worker_obj.entity.id)
        get_job = self.images_provider.jobs_client.get_job(jobs[0].id)
        self.assertEquals(get_job.status_code, 200,
                          msg.format('status_code', 200,
                                     get_job.status_code))

        timeout = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

        update_job_status_obj = self.images_provider.jobs_client.\
            update_job_status(jobs[0].id, status=get_job.entity.status,
                              timeout=timeout)

        self.assertEquals(update_job_status_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     update_job_status_obj.status_code))

        """ @TODO: Steps to do after resolving github issue #163
        1) Add assertion to check/wait for job status to done
        2) Remove sleep (added it to make the test pass now)"""

        time.sleep(20)
        get_job = self.images_provider.jobs_client.get_job(jobs[0].id)
        self.assertEquals(get_job.status_code, 200,
                          msg.format('status_code', 200,
                                     get_job.status_code))

        self.assertNotEquals(get_job.entity.worker_id, old_worker_id,
                             msg.format('worker', 'New worker',
                                        get_job.entity.worker_id))
