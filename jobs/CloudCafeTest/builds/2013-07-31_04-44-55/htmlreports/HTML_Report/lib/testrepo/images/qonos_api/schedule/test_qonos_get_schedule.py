from testrepo.common.testfixtures.images import BaseImagesFixture
from ccengine.common.constants.images_constants import Constants
from ccengine.common.decorators import attr
import calendar
import time


class TestQonosGetSchedule(BaseImagesFixture):

    @attr('positive')
    def test_happy_path_get_schedule(self):
        '''Happy Path - Get details of schedule using valid parameter'''

        """
        1) Create a schedule using valid mandatory parameters
        2) Verify that the response code is 200
        3) Get details of the schedule
        4) Verify that the auto-generated parameters (id, created-at,
           updated-at, next_run, last_scheduled, etc) are generated correctly
        5) Verify that the non-auto-generated parameters (month, week,
           day_of_week, _day_of_month, meta_data, etc) are created as entered

        Attributes to verify:
            next_run
            hour
            tenant
            created_at
            updated_at
            day_of_week
            day_of_month
            metadata
            last_scheduled
            action
            month
            id
            minute
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

        self.assertTrue(next_run_diff_in_sec <= 10,
                        msg.format('next_run', created_sch.next_run,
                                   get_sch.next_run))
        self.assertEquals(get_sch.hour, created_sch.hour,
                          msg.format('hour', created_sch.hour, get_sch.hour))
        self.assertEquals(get_sch.tenant, created_sch.tenant,
                          msg.format('tenant', created_sch.tenant,
                                     get_sch.tenant))
        self.assertTrue(created_at_diff_in_sec <= 10,
                        msg.format('created_at', created_sch.created_at,
                                   get_sch.created_at))
        self.assertTrue(updated_at_diff_in_sec <= 10,
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
