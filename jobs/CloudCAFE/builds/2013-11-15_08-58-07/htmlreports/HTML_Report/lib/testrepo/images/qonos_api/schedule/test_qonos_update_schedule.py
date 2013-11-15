import calendar
import time
from datetime import datetime, timedelta

import ccengine.common.tools.datagen as datagen
from ccengine.common.constants.images_constants import Constants
from ccengine.common.decorators import attr
from ccengine.domain.types import ScheduledImagesJobStatus
from testrepo.common.testfixtures.images import BaseImagesFixture


class TestQonosUpdateSchedule(BaseImagesFixture):

    @classmethod
    def setUpClass(cls):
        """Creates the server instance used for all tests in this class."""

        super(TestQonosUpdateSchedule, cls).setUpClass()

        server_name = datagen.random_string(size=10)

        server_obj = cls.images_provider.create_active_server(server_name)

        cls.instance_id = server_obj.entity.id

    @attr('positive')
    def test_happy_path_update_schedule(self):
        """Happy Path - Update schedule using valid values for all parameter.

        1) Create a schedule
        2) Update the schedule using every parameter with valid values
        3) Verify that the schedule is updated as expected
        4) Verify that the response code is 200
        5) Verify that the auto-generated parameters (id, created-at,
            updated-at, next_run, last_scheduled, etc) are generated correctly
        6) Verify that the non-auto-generated parameters (month, week,
            day_of_week, _day_of_month, meta_data, etc) are updated as entered
        """

        hour = int(self.config.images.hour)
        tenant = self.config.images.tenant
        alt_tenant = self.config.images.alt_tenant
        day_of_week = int(self.config.images.day_of_week)
        day_of_month = int(self.config.images.day_of_month)
        action = self.config.images.action
        alt_action = self.config.images.alt_action
        month = int(self.config.images.month)
        minute = int(self.config.images.minute)
        msg = Constants.MESSAGE

        sch_obj = self.images_provider.create_active_schedules(tenant, action)
        self.assertEquals(sch_obj.status_code, 200,
                          msg.format('status_code', 200, sch_obj.status_code))

        created_sch = sch_obj.entity

        upd_sch_obj = \
            self.images_provider.schedules_client.update_schedule(
                id=created_sch.id, hour=hour, tenant=alt_tenant,
                day_of_week=day_of_week, day_of_month=day_of_month,
                action=alt_action, month=month, minute=minute)
        self.assertEquals(upd_sch_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     upd_sch_obj.status_code))

        upd_sch = upd_sch_obj.entity

        created_sch_created_at_in_sec = \
            calendar.timegm(time.strptime(str(created_sch.created_at),
                                          "%Y-%m-%dT%H:%M:%SZ"))
        updated_created_at_in_sec = \
            calendar.timegm(time.strptime(str(upd_sch.created_at),
                                          "%Y-%m-%dT%H:%M:%SZ"))

        created_at_diff_in_sec = \
            abs(created_sch_created_at_in_sec - updated_created_at_in_sec)

        self.assertEquals(upd_sch.hour, hour,
                          msg.format('hour', hour, upd_sch.hour))
        self.assertEquals(upd_sch.tenant, alt_tenant,
                          msg.format('tenant', alt_tenant,
                                     upd_sch.tenant))
        self.assertLessEqual(created_at_diff_in_sec, 10,
                             msg.format('created_at', created_sch.created_at,
                                        upd_sch.created_at))
        self.assertEquals(upd_sch.day_of_week, day_of_week,
                          msg.format('day_of_week', day_of_week,
                                     upd_sch.day_of_week))
        self.assertEquals(upd_sch.day_of_month, day_of_month,
                          msg.format('day_of_month', day_of_month,
                                     upd_sch.day_of_month))

        ''' @TODO: After github bug #50 fixed, add assertion for metadata '''
        self.assertEquals(upd_sch.action, alt_action,
                          msg.format('action', alt_action, upd_sch.action))
        self.assertEquals(upd_sch.month, month,
                          msg.format('month', month, upd_sch.month))
        self.assertEquals(upd_sch.id, created_sch.id,
                          msg.format('id', created_sch.id, upd_sch.id))
        self.assertEquals(upd_sch.minute, minute,
                          msg.format('minute', minute, upd_sch.minute))

    @attr('positive')
    def test_update_schedule_after_job_created(self):
        """Update schedule after a job created for it.

        1) Create a schedule such that a job is created for it in few minutes
        2) Make sure a job is created for that schedule
        3) Update the schedule with new hour and minute value
        4) Verify that the schedule is updated with hour, minute and next_run
        5) Verify that the currently running job is not affected and
            completes successfully
        """

        tenant = self.config.images.tenant
        action = self.config.images.action
        msg = Constants.MESSAGE
        key = self.config.images.metadata_key
        instance_id = self.instance_id
        hour = int(self.config.images.hour)
        minute = int(self.config.images.minute)
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
        self.assertEquals(upd_sch_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     upd_sch_obj.status_code))

        keys = ["schedule_id", "marker"]
        values = [sch.id, marker]

        self.images_provider.wait_for_job_to_create(sch.id, keys=keys,
                                                    values=values)

        jobs = self.images_provider.list_jobs_for_schedule(sch.id, keys,
                                                           values)

        upd_sch_obj = self.images_provider.schedules_client.\
            update_schedule(id=sch.id, hour=hour, minute=minute)
        self.assertEquals(upd_sch_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     upd_sch_obj.status_code))

        upd_sch = upd_sch_obj.entity

        self.assertEquals(upd_sch.hour, hour,
                          msg.format('hour', hour, upd_sch.hour))
        self.assertEquals(upd_sch.minute, minute,
                          msg.format('minute', minute,
                                     upd_sch.minute))
        self.assertNotEquals(upd_sch.next_run, sch.next_run,
                             msg.format('next_run', "Updated next_run",
                                        upd_sch.next_run))

        job = self.images_provider.jobs_client.get_job(jobs[0].id)

        self.assertEquals(job.status_code, 200,
                          msg.format('status_code', 200, job.status_code))

        status = job.entity.status
        self.assertTrue(self.images_provider.is_job_status_workable(status) or
                        self.images_provider.is_job_status_done(status),
                        msg.format('status', 'workable/done job status',
                                   status))

        self.images_provider.wait_for_job_status(jobs[0].id,
                                                 ScheduledImagesJobStatus.DONE)

        job = self.images_provider.jobs_client.get_job(jobs[0].id)

        self.assertEquals(job.status_code, 200,
                          msg.format('status_code', 200, job.status_code))

        self.assertIsNotNone(job.entity.worker_id, msg.format(
            'worker', 'Not None', job.entity.worker_id))
