import calendar
import re
import time

from ccengine.common.constants.images_constants import Constants
from ccengine.common.decorators import attr
from testrepo.common.testfixtures.images import BaseImagesFixture


class TestQonosCreateSchedule(BaseImagesFixture):

    @attr('positive')
    def test_happy_path_create_schedule(self):
        """Happy Path - Create schedule using valid mandatory parameter tenant
        id, action.

        1) Create a valid schedule with all valid mandatory parameters of
           tenant id and action
        2) Verify the schedule is created
        3) Verify that the response code is 200
        4) Verify that the auto-generated parameters (id, created-at,
           updated-at, next_run, last_scheduled, etc) are generated correctly
        5) Verify that the non-auto-generated parameters (month,
           day_of_week, day_of_month, meta_data, etc) are created as
           entered
        """

        tenant = self.config.images.tenant
        action = self.config.images.action
        secs_in_a_day = (1 * 24 * 3600)
        id_re = re.compile(Constants.ID_RE)
        msg = Constants.MESSAGE

        sch_obj = self.images_provider.create_active_schedules(tenant, action)

        sch_creation_time_in_sec = calendar.timegm(time.gmtime())

        self.assertEquals(sch_obj.status_code, 200,
                          msg.format('status_code', 200, sch_obj.status_code))

        sch = sch_obj.entity

        sch_next_run_time_in_sec = \
            calendar.timegm(time.strptime(str(sch.next_run),
                                          "%Y-%m-%dT%H:%M:%SZ"))

        created_at_in_sec = \
            calendar.timegm(time.strptime(str(sch.created_at),
                                          "%Y-%m-%dT%H:%M:%SZ"))

        offset_in_schedule_next_run = \
            abs(sch_next_run_time_in_sec - created_at_in_sec)

        offset_in_schedule_created_time = \
            abs(created_at_in_sec - sch_creation_time_in_sec)

        updated_at_in_sec = \
            calendar.timegm(time.strptime(str(sch.updated_at),
                                          "%Y-%m-%dT%H:%M:%SZ"))
        offset_in_schedule_updated_time = \
            abs(updated_at_in_sec - sch_creation_time_in_sec)

        self.assertLessEqual(
            offset_in_schedule_next_run, secs_in_a_day, msg.format(
                "next_run", "value less than or equal to {0}".format(
                    secs_in_a_day), offset_in_schedule_next_run))
        self.assertIsNotNone(sch.hour, msg.format('hour', None, sch.hour))
        self.assertEquals(sch.tenant, tenant,
                          msg.format('tenant', tenant, sch.tenant))
        self.assertLessEqual(offset_in_schedule_created_time, 60000,
                             msg.format('created_at',
                                        'value less than or equal to 60000',
                                        offset_in_schedule_created_time))
        self.assertLessEqual(offset_in_schedule_updated_time, 60000,
                             msg.format('updated_at',
                                        'value less than or equal to 60000',
                                        offset_in_schedule_updated_time))
        self.assertIsNone(sch.day_of_week, msg.format('day_of_week', None,
                                                      sch.day_of_week))
        self.assertIsNone(sch.day_of_month, msg.format('day_of_month', None,
                                                       sch.day_of_month))
        self.assertEquals(sch.metadata, {},
                          msg.format('metadata', {}, sch.metadata))
        self.assertIsNone(sch.last_scheduled, msg.format(
            'last_scheduled', None, sch.last_scheduled))
        self.assertEquals(sch.action, action,
                          msg.format('action', action, sch.action))
        self.assertIsNone(sch.month, msg.format('month', None, sch.month))
        self.assertIsNotNone(id_re.match(sch.id),
                             msg.format('id', 'valid schedule id', sch.id))
        self.assertIsNotNone(sch.minute, msg.format('minute', None,
                                                    sch.minute))
