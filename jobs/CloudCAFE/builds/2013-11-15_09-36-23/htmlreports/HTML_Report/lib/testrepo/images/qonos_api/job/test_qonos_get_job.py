import calendar
import re
import time
from datetime import datetime, timedelta

import ccengine.common.tools.datagen as datagen
from ccengine.common.constants.images_constants import Constants
from ccengine.common.decorators import attr
from ccengine.domain.types import ScheduledImagesJobStatus
from testrepo.common.testfixtures.images import BaseImagesFixture


class TestQonosGetJob(BaseImagesFixture):

    @classmethod
    def setUpClass(cls):
        """Creates the server instance used for all tests in this class."""

        super(TestQonosGetJob, cls).setUpClass()

        server_name = datagen.random_string(size=10)

        server_obj = cls.images_provider.create_active_server(server_name)

        cls.instance_id = server_obj.entity.id

    @attr('positive')
    def test_happy_path_get_job(self):
        """Happy Path - Get job.

        1) Create a schedule so that a job is created for it within the next 5
            minutes
        2) Create a job from the schedule
        3) Get the job
        4) Verify that the response code is 200
        5) Verify that the job is as expected
        """

        tenant = self.config.images.tenant
        action = self.config.images.alt_action
        msg = Constants.MESSAGE
        id_re = re.compile(Constants.ID_RE)

        sch_obj = self.images_provider.create_active_schedules(tenant, action)
        self.assertEquals(sch_obj.status_code, 200,
                          msg.format('status_code', 200, sch_obj.status_code))

        sch = sch_obj.entity

        job_obj = self.images_provider.create_active_jobs(sch.id)
        self.assertEquals(job_obj.status_code, 200,
                          msg.format('status_code', 200, job_obj.status_code))

        job = job_obj.entity

        get_job_obj = self.images_provider.jobs_client.get_job(job.id)
        self.assertEquals(get_job_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     get_job_obj.status_code))

        get_job = get_job_obj.entity

        get_hard_timeout_in_sec = \
            calendar.timegm(time.strptime(str(get_job.hard_timeout),
                                          "%Y-%m-%dT%H:%M:%SZ"))
        job_hard_timeout_in_sec = \
            calendar.timegm(time.strptime(str(job.hard_timeout),
                                          "%Y-%m-%dT%H:%M:%SZ"))
        get_created_at_in_sec = \
            calendar.timegm(time.strptime(str(get_job.created_at),
                                          "%Y-%m-%dT%H:%M:%SZ"))
        job_created_at_in_sec = \
            calendar.timegm(time.strptime(str(job.created_at),
                                          "%Y-%m-%dT%H:%M:%SZ"))
        get_updated_at_in_sec = \
            calendar.timegm(time.strptime(str(get_job.updated_at),
                                          "%Y-%m-%dT%H:%M:%SZ"))
        job_updated_at_in_sec = \
            calendar.timegm(time.strptime(str(job.updated_at),
                                          "%Y-%m-%dT%H:%M:%SZ"))
        get_timeout_in_sec = \
            calendar.timegm(time.strptime(str(get_job.timeout),
                                          "%Y-%m-%dT%H:%M:%SZ"))
        job_timeout_in_sec = \
            calendar.timegm(time.strptime(str(job.timeout),
                                          "%Y-%m-%dT%H:%M:%SZ"))

        hard_timeout_diff_in_sec = \
            abs(get_hard_timeout_in_sec - job_hard_timeout_in_sec)
        created_at_diff_in_sec = \
            abs(get_created_at_in_sec - job_created_at_in_sec)
        updated_at_diff_in_sec = \
            abs(get_updated_at_in_sec - job_updated_at_in_sec)
        timeout_diff_in_sec = \
            abs(get_timeout_in_sec - job_timeout_in_sec)

        status = get_job.status

        self.assertTrue(self.images_provider.is_job_status_valid(status),
                        msg.format('status', job.status, status))
        self.assertLessEqual(hard_timeout_diff_in_sec, 10,
                             msg.format('hard_timeout', job.hard_timeout,
                                        get_job.hard_timeout))
        self.assertEquals(get_job.tenant, job.tenant,
                          msg.format('tenant', job.tenant, get_job.tenant))
        self.assertLessEqual(
            created_at_diff_in_sec, 10,
            msg.format('created_at', job.created_at, get_job.created_at))
        self.assertLessEqual(
            updated_at_diff_in_sec, 10,
            msg.format('updated_at', job.updated_at, get_job.updated_at))
        self.assertIsNotNone(
            get_job.retry_count,
            msg.format('retry_count', 'valid integer', get_job.retry_count))
        self.assertEquals(
            get_job.schedule_id, job.schedule_id,
            msg.format('schedule_id', job.schedule_id, get_job.schedule_id))
        self.assertLessEqual(
            timeout_diff_in_sec, 10,
            msg.format('timeout', job.timeout, get_job.timeout))
        self.assertEquals(get_job.action, job.action,
                          msg.format('action', job.action, get_job.action))
        self.assertEquals(get_job.id, job.id,
                          msg.format('id', job.id, get_job.id))
        self.assertEquals(
            get_job.metadata, job.metadata,
            msg.format('metadata', job.metadata, get_job.metadata))
        if get_job.worker_id is None:
            self.assertEqual(
                get_job.worker_id, job.worker_id,
                msg.format('worker', 'Valid worker id', get_job.worker_id))
        elif get_job.worker_id != job.worker_id:
            self.assertNotEqual(
                id_re.match(get_job.worker_id), None,
                msg.format('worker', 'not None', get_job.worker_id))
        else:
            self.fail(msg.format('worker', 'None/Valid worker id',
                                 get_job.worker_id))

    @attr('positive')
    def test_happy_path_get_job_status(self):
        """Happy Path - Get job status.

        1) Create a schedule so that a job is created for it within the
            next 5 minutes
        2) List the jobs
        3) Verify that the response code is 200
        4) Make sure a job is created from the schedule
        5) Verify job is assigned with worker id
        6) Wait for the job status to change from 'queued' to 'processing'
            to 'done'
        """

        tenant = self.config.images.tenant
        action = self.config.images.action
        msg = Constants.MESSAGE
        key = self.config.images.metadata_key
        instance_id = self.instance_id
        user_name_metadata_key = self.config.images.user_name_metadata_key
        user_name = self.config.images.user_name
        marker = None

        sch_obj = self.images_provider.create_active_schedules(tenant, action)
        self.assertEquals(sch_obj.status_code, 200,
                          msg.format('status_code', 200, sch_obj.status_code))

        sch = sch_obj.entity

        keys = [key, user_name_metadata_key]
        values = [instance_id, user_name]

        sch_metadata_obj = self.images_provider.schedules_client.\
            set_schedule_metadata(sch.id, keys, values)

        self.assertEquals(
            sch_metadata_obj.status_code, 200,
            msg.format('status_code', 200, sch_metadata_obj.status_code))

        tm = datetime.now() - timedelta(seconds=60)
        next_run_time = tm.strftime('%Y-%m-%d %H:%M:%S')

        upd_sch_obj = \
            self.images_provider.schedules_client.update_schedule(
                id=sch.id, next_run=next_run_time)
        self.assertEquals(
            upd_sch_obj.status_code, 200,
            msg.format('status_code', 200, upd_sch_obj.status_code))

        keys = ["schedule_id", "marker"]
        values = [sch.id, marker]

        self.images_provider.wait_for_job_to_create(sch.id, keys=keys,
                                                    values=values)

        jobs = self.images_provider.list_jobs_for_schedule(sch.id, keys,
                                                           values)

        self.assertEquals(len(jobs), 1, msg.format('job_length', 1, len(jobs)))

        status = jobs[0].status
        self.assertTrue(
            self.images_provider.is_job_status_workable(status) or
            self.images_provider.is_job_status_done(status),
            msg.format('status', 'workable/done job status', status))

        self.images_provider.wait_for_job_status(jobs[0].id,
                                                 ScheduledImagesJobStatus.DONE)

        job = self.images_provider.jobs_client.get_job(jobs[0].id)

        self.assertEquals(job.status_code, 200,
                          msg.format('status_code', 200, job.status_code))

        self.assertIsNotNone(
            job.entity.worker_id,
            msg.format('worker', 'Not None', job.entity.worker_id))

    @attr('positive')
    def test_get_job_after_worker_picks_it_up(self):
        """Get job after worker picks it up for processing.

        1) Create a schedule with metadata such that a job is created for it
            in few minutes
        2) Make sure a job is created for that schedule
        3) Get the job
        4) Verify that the response code is 200
        5) Verify that the job is assigned with worker id and its status is
            valid
        6) After the job is processed by a worker, get the job
        7) Verify that the response code is 200
        8) Verify that the status of the job has changed to 'done'
        """

        tenant = self.config.images.tenant
        action = self.config.images.action
        msg = Constants.MESSAGE
        key = self.config.images.metadata_key
        instance_id = self.instance_id
        user_name_metadata_key = self.config.images.user_name_metadata_key
        user_name = self.config.images.user_name
        marker = None

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
        self.assertEquals(
            upd_sch_obj.status_code, 200,
            msg.format('status_code', 200, upd_sch_obj.status_code))

        keys = ["schedule_id", "marker"]
        values = [sch.id, marker]

        self.images_provider.wait_for_job_to_create(sch.id, keys=keys,
                                                    values=values)

        jobs = self.images_provider.list_jobs_for_schedule(sch.id, keys,
                                                           values)

        job = self.images_provider.jobs_client.get_job(jobs[0].id)

        self.assertEquals(job.status_code, 200,
                          msg.format('status_code', 200, job.status_code))

        status = job.entity.status
        self.assertTrue(
            self.images_provider.is_job_status_workable(status) or
            self.images_provider.is_job_status_done(status),
            msg.format('status', 'workable/done job status', status))

        self.images_provider.wait_for_job_status(jobs[0].id,
                                                 ScheduledImagesJobStatus.DONE)

        job = self.images_provider.jobs_client.get_job(jobs[0].id)

        self.assertEquals(job.status_code, 200,
                          msg.format('status_code', 200, job.status_code))

        self.assertIsNotNone(
            job.entity.worker_id,
            msg.format('worker', 'Not None', job.entity.worker_id))
