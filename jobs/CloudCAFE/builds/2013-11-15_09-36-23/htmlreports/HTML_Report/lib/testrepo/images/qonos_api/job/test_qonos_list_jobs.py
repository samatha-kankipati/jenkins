import calendar
import re
import time

import ccengine.common.tools.datagen as datagen
from ccengine.common.constants.images_constants import Constants
from ccengine.common.decorators import attr
from ccengine.domain.types import ScheduledImagesJobStatus
from testrepo.common.testfixtures.images import BaseImagesFixture


class TestQonosListJobs(BaseImagesFixture):

    @classmethod
    def setUpClass(cls):
        """Creates the server instance used for all tests in this class."""

        super(TestQonosListJobs, cls).setUpClass()

        server_name = datagen.random_string(size=10)

        server_obj = cls.images_provider.create_active_server(server_name)

        cls.instance_id = server_obj.entity.id

    @attr('positive')
    def test_happy_path_list_jobs(self):
        """Happy Path - List jobs.

        1) Create a schedule
        2) Create a job from the schedule
        3) List jobs
        4) Verify that the response code is 200
        5) Verify that the length of the jobs is 1
        6) Verify that the job is as expected
        """

        tenant = self.config.images.tenant
        action = self.config.images.alt_action
        id_re = re.compile(Constants.ID_RE)
        count = 1
        marker = None
        retry_count = [0, 1]
        msg = Constants.MESSAGE

        sch_obj = self.images_provider.create_active_schedules(tenant, action)
        self.assertEquals(sch_obj.status_code, 200,
                          msg.format('status_code', 200, sch_obj.status_code))

        sch = sch_obj.entity

        job_obj = self.images_provider.create_active_jobs(sch.id)
        self.assertEquals(job_obj.status_code, 200,
                          msg.format('status_code', 200, job_obj.status_code))

        job = job_obj.entity

        job_hard_timeout_in_sec = \
            calendar.timegm(time.strptime(str(job.hard_timeout),
                                          "%Y-%m-%dT%H:%M:%SZ"))
        job_created_at_in_sec = \
            calendar.timegm(time.strptime(str(job.created_at),
                                          "%Y-%m-%dT%H:%M:%SZ"))
        job_updated_at_in_sec = \
            calendar.timegm(time.strptime(str(job.updated_at),
                                          "%Y-%m-%dT%H:%M:%SZ"))
        job_timeout_in_sec = \
            calendar.timegm(time.strptime(str(job.timeout),
                                          "%Y-%m-%dT%H:%M:%SZ"))

        keys = ["schedule_id", "marker"]
        values = [sch.id, marker]

        listed_jobs = self.images_provider.list_jobs_pagination(keys, values)

        self.assertEqual(len(listed_jobs), count,
                         msg.format("length of the list", count,
                                    len(listed_jobs)))

        listed_job = listed_jobs[0]

        listed_hard_timeout_in_sec = \
            calendar.timegm(time.strptime(str(listed_job.hard_timeout),
                                          "%Y-%m-%dT%H:%M:%SZ"))
        listed_created_at_in_sec = \
            calendar.timegm(time.strptime(str(listed_job.created_at),
                                          "%Y-%m-%dT%H:%M:%SZ"))
        listed_updated_at_in_sec = \
            calendar.timegm(time.strptime(str(listed_job.updated_at),
                                          "%Y-%m-%dT%H:%M:%SZ"))
        listed_timeout_in_sec = \
            calendar.timegm(time.strptime(str(listed_job.timeout),
                                          "%Y-%m-%dT%H:%M:%SZ"))
        hard_timeout_diff_in_sec = \
            abs(listed_hard_timeout_in_sec - job_hard_timeout_in_sec)
        created_at_diff_in_sec = \
            abs(listed_created_at_in_sec - job_created_at_in_sec)
        updated_at_diff_in_sec = \
            abs(listed_updated_at_in_sec - job_updated_at_in_sec)
        timeout_diff_in_sec = \
            abs(listed_timeout_in_sec - job_timeout_in_sec)

        status = listed_job.status

        self.assertTrue(self.images_provider.is_job_status_valid(status),
                        msg.format('status', job.status, status))

        self.assertLessEqual(hard_timeout_diff_in_sec, 10,
                             msg.format('hard_timeout', job.hard_timeout,
                                        listed_job.hard_timeout))
        self.assertEquals(listed_job.tenant, job.tenant,
                          msg.format('tenant', job.tenant,
                                     listed_job.tenant))
        self.assertLessEqual(created_at_diff_in_sec, 10,
                             msg.format('created_at',
                                        job.created_at, listed_job.created_at))
        self.assertLessEqual(updated_at_diff_in_sec, 10,
                             msg.format('updated_at',
                                        job.updated_at, listed_job.updated_at))
        self.assertIn(listed_job.retry_count, retry_count,
                      msg.format('retry_count', '0/1', listed_job.retry_count))
        self.assertEquals(listed_job.schedule_id, job.schedule_id,
                          msg.format('schedule_id', job.schedule_id,
                                     listed_job.schedule_id))
        self.assertLessEqual(timeout_diff_in_sec, 10,
                             msg.format('timeout', job.timeout,
                                        listed_job.timeout))
        self.assertEquals(listed_job.action, job.action,
                          msg.format('action', job.action, listed_job.action))
        self.assertEquals(listed_job.id, job.id,
                          msg.format('id', job.id, listed_job.id))
        self.assertEquals(listed_job.metadata, job.metadata,
                          msg.format('metadata', job.metadata,
                                     listed_job.metadata))
        if listed_job.worker_id is None:
            self.assertEqual(listed_job.worker_id, job.worker_id,
                             msg.format('worker', 'Valid worker id',
                                        listed_job.worker_id))
        elif listed_job.worker_id != job.worker_id:
            self.assertNotEqual(id_re.match(listed_job.worker_id), None,
                                msg.format('worker', 'not None',
                                           listed_job.worker_id))
        else:
            self.fail(msg.format('worker', 'None/Valid worker id',
                                 listed_job.worker_id))

    @attr('positive')
    def test_list_jobs_with_multiple_jobs(self):
        """List jobs with multiple jobs.

        1) Create a schedule
        2) Create a job from the schedule
        3) Create another schedule
        4) Create another job from the second schedule
        5) List jobs
        6) Verify that the response code is 200
        7) Verify that the length of the jobs is 2
        8) Verify that the job is as expected
        """

        tenant = self.config.images.tenant
        action = self.config.images.alt_action
        alt_tenant = self.config.images.alt_tenant
        alt_action = self.config.images.alt_action
        id_re = re.compile(Constants.ID_RE)
        count = 2
        marker = None
        retry_count = [0, 1]
        msg = Constants.MESSAGE
        msg_alt = Constants.MESSAGE_ALT

        sch_obj = self.images_provider.create_active_schedules(tenant, action)
        self.assertEquals(sch_obj.status_code, 200,
                          msg.format('status_code', 200, sch_obj.status_code))

        job_obj = self.images_provider.create_active_jobs(sch_obj.entity.id)
        self.assertEquals(job_obj.status_code, 200,
                          msg.format('status_code', 200, job_obj.status_code))

        job = job_obj.entity

        sch_obj = self.images_provider.create_active_schedules(alt_tenant,
                                                               alt_action)
        self.assertEquals(sch_obj.status_code, 200,
                          msg.format('status_code', 200, sch_obj.status_code))

        alt_job_obj = \
            self.images_provider.create_active_jobs(sch_obj.entity.id)
        self.assertEquals(job_obj.status_code, 200,
                          msg.format('status_code', 200, job_obj.status_code))

        alt_job = alt_job_obj.entity

        keys = ["schedule_id", "marker"]
        values = [job.schedule_id, marker]

        list_jobs = self.images_provider.list_jobs_pagination(keys, values)

        keys = ["schedule_id", "marker"]
        values = [alt_job.schedule_id, marker]

        list_alt_jobs = self.images_provider.list_jobs_pagination(keys, values)

        listed_jobs = list_jobs + list_alt_jobs

        self.assertEqual(len(listed_jobs), count,
                         msg.format("length of the list", count,
                                    len(listed_jobs)))

        for listed_job in listed_jobs:

            if listed_job.id == job.id:
                current_job = job
            elif listed_job.id == alt_job.id:
                current_job = alt_job
            else:
                self.fail(msg_alt.format('job_id', job.job_id, alt_job.job_id,
                                         listed_job.job_id))

            listed_hard_timeout_in_sec = \
                calendar.timegm(time.strptime(str(listed_job.hard_timeout),
                                              "%Y-%m-%dT%H:%M:%SZ"))
            current_hard_timeout_in_sec = \
                calendar.timegm(time.strptime(str(current_job.hard_timeout),
                                              "%Y-%m-%dT%H:%M:%SZ"))
            listed_created_at_in_sec = \
                calendar.timegm(time.strptime(str(listed_job.created_at),
                                              "%Y-%m-%dT%H:%M:%SZ"))
            current_created_at_in_sec = \
                calendar.timegm(time.strptime(str(current_job.created_at),
                                              "%Y-%m-%dT%H:%M:%SZ"))
            listed_updated_at_in_sec = \
                calendar.timegm(time.strptime(str(listed_job.updated_at),
                                              "%Y-%m-%dT%H:%M:%SZ"))
            current_updated_at_in_sec = \
                calendar.timegm(time.strptime(str(current_job.updated_at),
                                              "%Y-%m-%dT%H:%M:%SZ"))
            listed_timeout_in_sec = \
                calendar.timegm(time.strptime(str(listed_job.timeout),
                                              "%Y-%m-%dT%H:%M:%SZ"))
            current_timeout_in_sec = \
                calendar.timegm(time.strptime(str(current_job.timeout),
                                              "%Y-%m-%dT%H:%M:%SZ"))

            hard_timeout_diff_in_sec = \
                abs(listed_hard_timeout_in_sec - current_hard_timeout_in_sec)
            created_at_diff_in_sec = \
                abs(listed_created_at_in_sec - current_created_at_in_sec)
            updated_at_diff_in_sec = \
                abs(listed_updated_at_in_sec - current_updated_at_in_sec)
            timeout_diff_in_sec = \
                abs(listed_timeout_in_sec - current_timeout_in_sec)

            status = current_job.status

            self.assertTrue(self.images_provider.is_job_status_valid(status),
                            msg.format('status', status, listed_job.status))
            self.assertLessEqual(hard_timeout_diff_in_sec, 10,
                                 msg.format('hard_timeout',
                                            current_job.hard_timeout,
                                            listed_job.hard_timeout))
            self.assertEquals(listed_job.tenant, current_job.tenant,
                              msg.format('tenant', current_job.tenant,
                                         listed_job.tenant))
            self.assertLessEqual(created_at_diff_in_sec, 10,
                                 msg.format('created_at',
                                            current_job.created_at,
                                            listed_job.created_at))
            self.assertLessEqual(updated_at_diff_in_sec, 10,
                                 msg.format('updated_at',
                                            current_job.updated_at,
                                            listed_job.updated_at))
            self.assertIn(listed_job.retry_count, retry_count,
                          msg.format('retry_count', '0/1',
                                     listed_job.retry_count))
            self.assertEquals(listed_job.schedule_id, current_job.schedule_id,
                              msg.format('schedule_id',
                                         current_job.schedule_id,
                                         listed_job.schedule_id))
            self.assertLessEqual(timeout_diff_in_sec, 10,
                                 msg.format('timeout', current_job.timeout,
                                            listed_job.timeout))
            self.assertEquals(listed_job.action, current_job.action,
                              msg.format('action', current_job.action,
                                         listed_job.action))
            self.assertEquals(listed_job.metadata, current_job.metadata,
                              msg.format('metadata', current_job.metadata,
                                         listed_job.metadata))
            if listed_job.worker_id is None:
                self.assertEqual(listed_job.worker_id, current_job.worker_id,
                                 msg.format('worker', 'Valid worker id',
                                            listed_job.worker_id))
            elif listed_job.worker_id != current_job.worker_id:
                self.assertNotEqual(id_re.match(listed_job.worker_id), None,
                                    msg.format('worker', 'not None',
                                               listed_job.worker_id))
            else:
                self.fail(msg.format('worker', 'None/Valid worker id',
                                     listed_job.worker_id))

    @attr('positive')
    def test_list_jobs_for_deleted_job(self):
        """List jobs for deleted job.

        1) Create a schedule
        2) Create a job from the schedule
        3) List jobs
        4) Verify that the response code is 200
        5) Verify that the length of the jobs is 1
        6) Delete the job
        7) List jobs
        8) Verify that the response code is 200
        9) Verify that the length of the jobs is 0
        """

        tenant = self.config.images.tenant
        action = self.config.images.action
        count = 1
        msg = Constants.MESSAGE
        marker = None

        sch_obj = self.images_provider.create_active_schedules(tenant, action)
        self.assertEquals(sch_obj.status_code, 200,
                          msg.format('status_code', 200, sch_obj.status_code))

        job_obj = self.images_provider.create_active_jobs(sch_obj.entity.id)
        self.assertEquals(job_obj.status_code, 200,
                          msg.format('status_code', 200, job_obj.status_code))

        job = job_obj.entity

        keys = ["schedule_id", "marker"]
        values = [job.schedule_id, marker]

        listed_jobs = self.images_provider.list_jobs_pagination(keys, values)

        self.assertEqual(len(listed_jobs), count,
                         msg.format("length of the list", count,
                                    len(listed_jobs)))

        del_job_obj = \
            self.images_provider.jobs_client.delete_job(job_obj.entity.id)
        self.assertEquals(del_job_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     del_job_obj.status_code))

        count -= 1

        keys = ["schedule_id", "marker"]
        values = [job.schedule_id, marker]

        listed_jobs = self.images_provider.list_jobs_pagination(keys, values)

        self.assertEqual(len(listed_jobs), count,
                         msg.format("length of the list", count,
                                    len(listed_jobs)))

    @attr('positive')
    def test_list_jobs_after_a_job_completes(self):
        """List jobs after a job completes.

        1) Create a schedule so that a job is created for it within the next 5
            minutes
        2) Create a job from the schedule
        3) List jobs
        4) Verify that the response code is 200
        5) Verify that the length of the jobs is 1
        6) Allow the job to complete
        7) List jobs
        8) Verify that the response code is 200
        9) Verify that the length of the jobs is 1 and the status of the job
            has changed to 'DONE'
        """

        tenant = self.config.images.tenant
        action = self.config.images.action
        count = 1
        key = self.config.images.metadata_key
        instance_id = self.instance_id
        user_name_metadata_key = self.config.images.user_name_metadata_key
        user_name = self.config.images.user_name
        marker = None
        msg = Constants.MESSAGE

        metadata = {key: instance_id, user_name_metadata_key: user_name}

        sch_obj = \
            self.images_provider.create_active_schedules(tenant, action,
                                                         metadata=metadata)
        self.assertEquals(sch_obj.status_code, 200,
                          msg.format('status_code', 200, sch_obj.status_code))

        sch = sch_obj.entity

        job_obj = self.images_provider.create_active_jobs(sch.id)
        self.assertEquals(job_obj.status_code, 200,
                          msg.format('status_code', 200, job_obj.status_code))

        job = job_obj.entity

        keys = ["schedule_id", "marker"]
        values = [job.schedule_id, marker]

        listed_jobs = self.images_provider.list_jobs_pagination(keys, values)

        self.assertEqual(len(listed_jobs), count,
                         msg.format("length of the list", count,
                                    len(listed_jobs)))

        self.images_provider.wait_for_job_status(job.id,
                                                 ScheduledImagesJobStatus.DONE)

        keys = ["schedule_id", "marker"]
        values = [job.schedule_id, marker]

        listed_jobs = self.images_provider.list_jobs_pagination(keys, values)

        self.assertEqual(len(listed_jobs), count,
                         msg.format("length of the list", count,
                                    len(listed_jobs)))

        self.assertEqual(listed_jobs[0].status, ScheduledImagesJobStatus.DONE,
                         msg.format("job status",
                                    ScheduledImagesJobStatus.DONE,
                                    listed_jobs[0].status))
