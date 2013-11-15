from testrepo.common.testfixtures.images import BaseImagesFixture
from ccengine.common.constants.images_constants import Constants
from ccengine.common.decorators import attr
import calendar
import time
import re
import ccengine.common.tools.datagen as datagen


class TestQonosEnableScheduledImages(BaseImagesFixture):

    @classmethod
    def setUpClass(cls):
        '''Creates the server instances and snapshots used for all tests in
        this class'''

        super(TestQonosEnableScheduledImages, cls).setUpClass()

        server_name = datagen.random_string(size=10)

        server_obj = cls.images_provider.create_active_server(server_name)

        cls.instance_id = server_obj.entity.id

    @attr('smoke')
    def test_happy_path_enable_scheduled_images(self):
        '''Happy Path - Enable scheduled images for a valid server'''

        """
        1) Create a valid server instance
        2) Enable scheduled images using a valid retention value
        3) Verify that the response code is 200
        4) Verify that the response contains the entered retention value
        5) List schedules
        6) Verify that the response code is 200
        7) Verify that there is a schedule created for the instance
        8) Verify that the auto-generated parameters (id, created-at,
        updated-at, next_run, last_scheduled, etc) are generated correctly
        9) Verify that the non-auto-generated parameters (month,
        day_of_week, day_of_month, meta_data, etc) are created as
        entered

        Attributes to verify:
        retention
        next_run
        hour
        tenant
        created_at
        updated_at
        day_of_week
        day_of_month
        schedule_metadata
        last_scheduled
        action
        month
        id
        minute
        """

        tenant_id = self.config.images.tenant_id
        tenant = self.config.images.tenant
        user_name = self.config.images.user_name
        instance_id = self.instance_id
        secs_in_a_day = (1 * 24 * 3600)
        sch_list = []
        count = 1
        id_re = re.compile(Constants.ID_RE)
        retention = self.config.images.retention
        marker = None
        msg = Constants.MESSAGE

        sch_img_obj = self.images_provider.scheduled_images_client. \
            enable_scheduled_images(tenant_id, instance_id, retention)

        sch_img_creation_time_in_sec = calendar.timegm(time.gmtime())

        self.assertEquals(sch_img_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     sch_img_obj.status_code))

        sch_img = sch_img_obj.entity

        keys = ["tenant", "marker"]
        values = [tenant_id, marker]

        list_sch = self.images_provider.list_schedules_pagination(keys, values)

        for s in list_sch:
            for metadata_key, metadata_value in s.metadata.items():
                if metadata_value == instance_id:
                    sch_list.append(s)
        self.assertTrue(len(sch_list) == count,
                        msg.format("length of the list", count, len(sch_list)))

        listed_sch = sch_list[0]

        sch_next_run_time_in_sec = \
            calendar.timegm(time.strptime(str(listed_sch.next_run),
                                          "%Y-%m-%dT%H:%M:%SZ"))

        created_at_in_sec = \
            calendar.timegm(time.strptime(str(listed_sch.created_at),
                                          "%Y-%m-%dT%H:%M:%SZ"))

        offset_in_schedule_next_run = \
            abs(sch_next_run_time_in_sec - created_at_in_sec)

        offset_in_schedule_created_time = \
            abs(created_at_in_sec - sch_img_creation_time_in_sec)

        updated_at_in_sec = \
            calendar.timegm(time.strptime(str(listed_sch.updated_at),
                                          "%Y-%m-%dT%H:%M:%SZ"))
        offset_in_schedule_updated_time = \
            abs(updated_at_in_sec - sch_img_creation_time_in_sec)

        self.assertEquals(sch_img.retention, retention,
                          msg.format('retention', retention,
                                     sch_img.retention))
        self.assertTrue(offset_in_schedule_next_run <= secs_in_a_day,
                        msg.format('next_run', "value less than or equal to %s"
                                   % (secs_in_a_day),
                                   offset_in_schedule_next_run))

        self.assertNotEquals(listed_sch.hour, None,
                        msg.format('hour', None, listed_sch.hour))
        self.assertEquals(listed_sch.tenant, tenant,
                          msg.format('tenant', tenant, listed_sch.tenant))
        self.assertTrue(offset_in_schedule_created_time <= 60000,
                        msg.format('created_at',
                                   'value less than or equal to 60000',
                                   offset_in_schedule_created_time))
        self.assertTrue(offset_in_schedule_updated_time <= 60000,
                        msg.format('updated_at',
                                   'value less than or equal to 60000',
                                   offset_in_schedule_updated_time))
        self.assertEquals(listed_sch.day_of_week, None,
                          msg.format('day_of_week', None,
                                     listed_sch.day_of_week))
        self.assertEquals(listed_sch.day_of_month, None,
                          msg.format('day_of_month', None,
                                     listed_sch.day_of_month))
        self.assertEquals(str(listed_sch.metadata),
                          "{{u'instance_id': u'{0}', u'user_name': u'{1}'}}".\
                          format(instance_id, user_name),
                          msg.format('metadata',
                                     "{{u'instance_id': u'{0}',"
                                     + " u'user_name': u'{1}'}}".\
                                     format(instance_id, user_name),
                                     str(listed_sch.metadata)))
        self.assertEquals(listed_sch.last_scheduled, None,
                          msg.format('last_scheduled', None,
                                     listed_sch.last_scheduled))
        self.assertEquals(listed_sch.action, self.config.images.action,
                          msg.format('action', self.config.images.action,
                                     listed_sch.action))
        self.assertEquals(listed_sch.month, None,
                          msg.format('month', None, listed_sch.month))
        self.assertTrue(id_re.match(listed_sch.id) != None,
                        msg.format('id', 'valid schedule id', listed_sch.id))
        self.assertNotEquals(listed_sch.minute, None,
                          msg.format('minute', None,
                                     listed_sch.minute))
