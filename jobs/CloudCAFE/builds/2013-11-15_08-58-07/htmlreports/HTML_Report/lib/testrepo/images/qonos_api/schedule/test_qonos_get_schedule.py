import calendar
import time
from datetime import datetime, timedelta

import ccengine.common.tools.datagen as datagen
from ccengine.common.constants.images_constants import Constants
from ccengine.common.decorators import attr
from ccengine.common.exceptions.compute import ItemNotFound
from ccengine.domain.types import ScheduledImagesJobStatus
from testrepo.common.testfixtures.images import BaseImagesFixture


class TestQonosGetSchedule(BaseImagesFixture):

    @classmethod
    def setUpClass(cls):
        """Creates the server instance used for all tests in this class."""

        super(TestQonosGetSchedule, cls).setUpClass()

        server_name = datagen.random_string(size=10)

        server_obj = cls.images_provider.create_active_server(server_name)

        cls.instance_id = server_obj.entity.id

    @attr('positive')
    def test_happy_path_get_schedule(self):
        """Happy Path - Get details of schedule using valid parameter.

        1) Create a schedule using valid mandatory parameters
        2) Verify that the response code is 200
        3) Get details of the schedule
        4) Verify that the auto-generated parameters (id, created-at,
           updated-at, next_run, last_scheduled, etc) are generated correctly
        5) Verify that the non-auto-generated parameters (month, week,
           day_of_week, _day_of_month, meta_data, etc) are created as entered
        """

        tenant = self.config.images.tenant
        action = self.config.images.action
        msg = Constants.MESSAGE

        sch_obj = self.images_provider.create_active_schedules(tenant, action)
        self.assertEquals(sch_obj.status_code, 200,
                          msg.format('status_code', 200, sch_obj.status_code))

        created_sch = sch_obj.entity

        get_sch_obj = \
            self.images_provider.schedules_client.get_schedule(created_sch.id)
        self.assertEquals(get_sch_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     get_sch_obj.status_code))

        get_sch = get_sch_obj.entity

        get_next_run_in_sec = \
            calendar.timegm(time.strptime(str(get_sch.next_run),
                                          "%Y-%m-%dT%H:%M:%SZ"))
        created_next_run_in_sec = \
            calendar.timegm(time.strptime(str(created_sch.next_run),
                                          "%Y-%m-%dT%H:%M:%SZ"))
        get_created_at_in_sec = \
            calendar.timegm(time.strptime(str(get_sch.created_at),
                                          "%Y-%m-%dT%H:%M:%SZ"))
        created_created_at_in_sec = \
            calendar.timegm(time.strptime(str(created_sch.created_at),
                                          "%Y-%m-%dT%H:%M:%SZ"))
        get_updated_at_in_sec = \
            calendar.timegm(time.strptime(str(get_sch.updated_at),
                                          "%Y-%m-%dT%H:%M:%SZ"))
        created_updated_at_in_sec = \
            calendar.timegm(time.strptime(str(created_sch.updated_at),
                                          "%Y-%m-%dT%H:%M:%SZ"))

        next_run_diff_in_sec = \
            abs(get_next_run_in_sec - created_next_run_in_sec)
        created_at_diff_in_sec = \
            abs(get_created_at_in_sec - created_created_at_in_sec)
        updated_at_diff_in_sec = \
            abs(get_updated_at_in_sec - created_updated_at_in_sec)

        self.assertLessEqual(next_run_diff_in_sec, 10,
                             msg.format('next_run', created_sch.next_run,
                                        get_sch.next_run))
        self.assertEquals(get_sch.hour, created_sch.hour,
                          msg.format('hour', created_sch.hour, get_sch.hour))
        self.assertEquals(get_sch.tenant, created_sch.tenant,
                          msg.format('tenant', created_sch.tenant,
                                     get_sch.tenant))
        self.assertLessEqual(created_at_diff_in_sec, 10,
                             msg.format('created_at', created_sch.created_at,
                                        get_sch.created_at))
        self.assertLessEqual(updated_at_diff_in_sec, 10,
                             msg.format('updated_at', created_sch.updated_at,
                                        get_sch.updated_at))
        self.assertEquals(get_sch.day_of_week, created_sch.day_of_week,
                          msg.format('day_of_week', created_sch.day_of_week,
                                     get_sch.day_of_week))
        self.assertEquals(get_sch.day_of_month, created_sch.day_of_month,
                          msg.format('day_of_month', created_sch.day_of_month,
                                     get_sch.day_of_month))
        self.assertEquals(get_sch.metadata, created_sch.metadata,
                          msg.format('metadata', created_sch.metadata,
                                     get_sch.metadata))
        self.assertEquals(get_sch.last_scheduled, created_sch.last_scheduled,
                          msg.format('last_scheduled',
                                     created_sch.last_scheduled,
                                     get_sch.last_scheduled))
        self.assertEquals(get_sch.action, created_sch.action,
                          msg.format('action', created_sch.action,
                                     get_sch.action))
        self.assertEquals(get_sch.month, created_sch.month,
                          msg.format('month', created_sch.month,
                                     get_sch.month))
        self.assertEquals(get_sch.id, created_sch.id,
                          msg.format('id', created_sch.id, get_sch.id))
        self.assertEquals(get_sch.minute, created_sch.minute,
                          msg.format('minute', created_sch.minute,
                                     get_sch.minute))

    @attr('positive')
    def test_get_schedule_for_instance_without_scheduled_images_enabled(self):
        """Verify that a schedule is deleted for an instance that does not have
        scheduled images enabled after a job is completed for it.

        1) Create a server instance
        2) Create a schedule for the server instance
        3) Get the server instance
        4) Get the retention value of the server instance
        5) Verify that the retention value is none
        6) Update the schedule so that a job is created for it shortly
        7) Wait for the job to complete
        8) Get the schedule
        9) Verify that the schedule is not deleted
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

        get_server_obj = \
            self.images_provider.servers_client.get_server(instance_id)
        self.assertEquals(get_server_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     get_server_obj.status_code))

        get_server = get_server_obj.entity

        self.assertFalse(hasattr(get_server, 'RAX-SI:image_schedule'),
                         msg.format('RAX-SI:image_schedule',
                                    'to not be present', 'was present'))

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

        for job in jobs:
            self.images_provider.wait_for_job_status(
                job.id, ScheduledImagesJobStatus.DONE)

        with self.assertRaises(ItemNotFound):
            self.images_provider.schedules_client.get_schedule(sch.id)
