from testrepo.common.testfixtures.images import BaseImagesFixture
from ccengine.common.constants.images_constants import Constants
from ccengine.common.decorators import attr
import ccengine.common.tools.datagen as datagen
from ccengine.domain.types import ScheduledImagesJobStatus
from datetime import datetime, timedelta
import calendar
import time
import re


class TestQonosCreateJob(BaseImagesFixture):

    @classmethod
    def setUpClass(cls):
        '''Creates the server instances used for all tests in this class'''

        super(TestQonosCreateJob, cls).setUpClass()

        server_name = datagen.random_string(size=10)

        server_obj = cls.images_provider.create_active_server(server_name)

        cls.instance_id = server_obj.entity.id

    @attr('positive')
    def test_happy_path_create_job(self):
        '''Happy Path - Create job from schedule using valid parameters'''

        """
        1) Create a schedule so that a job is created for it within the next 5
            minutes
        2) Create a job from the schedule
        3) Verify that the response code is 200
        4) Verify that the job contains all details as expected

        Attributes to verify:
            status
            hard_timeout
            tenant
            created_at
            updated_at
            retry_count
            schedule_id
            worker_id
            timeout
            action
            id
            metadata
        """

        tenant = self.config.images.tenant
        action = self.config.images.alt_action
        id_re = re.compile(Constants.ID_RE)
        msg = Constants.MESSAGE
        offset = int(self.config.images.hard_timeout_offset)

        sch_obj = self.images_provider.create_active_schedules(tenant, action)
        self.assertEquals(sch_obj.status_code, 200,
                          msg.format('status_code', 200, sch_obj.status_code))

        sch = sch_obj.entity

        job_obj = self.images_provider.create_active_jobs(sch.id)

        job_creation_time_in_sec = calendar.timegm(time.gmtime())

        self.assertEquals(job_obj.status_code, 200,
                          msg.format('status_code', 200, job_obj.status_code))

        job = job_obj.entity

        created_at_in_sec = \
            calendar.timegm(time.strptime(str(job.created_at),
                                          "%Y-%m-%dT%H:%M:%SZ"))

        offset_in_job_created_time = \
            abs(created_at_in_sec - job_creation_time_in_sec)

        updated_at_in_sec = \
            calendar.timegm(time.strptime(str(job.updated_at),
                                          "%Y-%m-%dT%H:%M:%SZ"))
        offset_in_job_updated_time = \
            abs(updated_at_in_sec - job_creation_time_in_sec)

        hard_timeout_in_sec = \
            calendar.timegm(time.strptime(str(job.hard_timeout),
                                          "%Y-%m-%dT%H:%M:%SZ"))
        hard_timeout_diff_in_sec = abs(hard_timeout_in_sec - created_at_in_sec)

        timeout_in_sec = \
            calendar.timegm(time.strptime(str(job.timeout),
                                          "%Y-%m-%dT%H:%M:%SZ"))

        timeout_diff_in_sec = abs(timeout_in_sec - created_at_in_sec)

        self.assertEquals(job.status, 'queued'.upper(),
                          msg.format('status', 'queued', job.status))
        self.assertEquals(hard_timeout_diff_in_sec, int(offset),
                          msg.format('hard_timeout', int(offset),
                                      hard_timeout_diff_in_sec))
        self.assertEquals(job.tenant, sch.tenant,
                          msg.format('tenant', sch.tenant,
                                     job.tenant))
        self.assertTrue(offset_in_job_created_time <= 60000,
                        msg.format('created_at',
                                   'value less than or equal to 60000',
                                   offset_in_job_created_time))
        self.assertTrue(offset_in_job_updated_time <= 60000,
                        msg.format('updated_at',
                                   'value less than or equal to 60000',
                                   offset_in_job_updated_time))
        self.assertTrue(job.retry_count == 0 or job.retry_count == 1,
                        msg.format('retry_count', '0/1', job.retry_count))
        self.assertEquals(job.schedule_id, sch.id,
                          msg.format('schedule_id', sch.id, job.schedule_id))
        self.assertEquals(job.worker_id, None,
                          msg.format('worker_id', None, job.worker_id))
        self.assertEquals(timeout_diff_in_sec, offset,
                          msg.format('timeout', offset,
                                      timeout_diff_in_sec))
        self.assertEquals(job.action, sch.action,
                          msg.format('action', sch.action, job.action))
        self.assertTrue(id_re.match(job.id) != None,
                        msg.format('id', 'valid job id', job.id))
        self.assertEquals(job.metadata, {},
                          msg.format('metadata', {}, job.metadata))

    @attr('positive')
    def test_verify_multiple_jobs_generated(self):
        '''Create job after a job created for it'''

        """
        1) Create a schedule such that a job is created for it in few minutes
        2) Make sure a job is created for that schedule
        3) Wait for few minutes to make sure another new job is created for
            the same schedule
        4) Verify that the schedule has more than one job
        """

        tenant = self.config.images.tenant
        action = self.config.images.action
        msg = Constants.MESSAGE
        key = self.config.images.metadata_key
        instance_id = self.instance_id
        user_name_metadata_key = self.config.images.user_name_metadata_key
        user_name = self.config.images.user_name
        count = 2

        metadata = {key: instance_id, user_name_metadata_key: user_name}

        sch_obj = self.images_provider.\
            create_active_schedules(tenant, action, metadata=metadata)
        self.assertEquals(sch_obj.status_code, 200,
                          msg.format('status_code', 200, sch_obj.status_code))

        sch = sch_obj.entity

        for x in range(count):
            tm = datetime.now() - timedelta(seconds=60)
            next_run_time = tm.strftime('%Y-%m-%d %H:%M:%S')

            upd_sch_obj = \
                self.images_provider.schedules_client.update_schedule(
                    id=sch.id, next_run=next_run_time)
            self.assertEquals(upd_sch_obj.status_code, 200,
                              msg.format('status_code', 200,
                                         upd_sch_obj.status_code))

            if x == 0:
                self.images_provider.wait_for_job_to_create(sch.id)
            elif x == 1:
                self.images_provider.wait_for_job_to_create(sch.id,
                                                            count=(x + 1))

            jobs = self.images_provider.list_jobs_for_schedule(sch.id)

            for job in jobs:
                self.images_provider.wait_for_job_status(job.id,
                                                 ScheduledImagesJobStatus.DONE)

            self.assertEquals(len(jobs), (x + 1), msg.format('total jobs',
                                                             (x + 1),
                                                             len(jobs)))
