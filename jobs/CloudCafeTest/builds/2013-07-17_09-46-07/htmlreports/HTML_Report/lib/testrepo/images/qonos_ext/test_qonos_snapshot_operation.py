import calendar
import time
from datetime import datetime, timedelta
import ccengine.common.tools.datagen as datagen
from ccengine.common.constants.images_constants import Constants
from ccengine.common.decorators import attr
from testrepo.common.testfixtures.images import BaseImagesFixture


class TestQonosSnapshotOperation(BaseImagesFixture):

    @classmethod
    def setUpClass(self):
        '''Creates the server instances used for all tests in this class'''

        super(TestQonosSnapshotOperation, self).setUpClass()

        server_name = datagen.random_string(size=10)

        server_obj = self.images_provider.create_active_server(server_name)

        self.instance_id = server_obj.entity.id

    @attr('smoke')
    def test_happy_path_scheduled_image_snapshot_operation(self):
        '''Happy Path - Scheduled image snapshot operation'''

        """
        1) Create a valid server instance
        2) Enable scheduled images using a valid retention value
        3) Verify that the response code is 200
        4) Verify that the response contains the entered retention value
        5) List schedules
        6) Verify that the response code is 200
        7) Verify that there is a schedule created for the instance
        8) Update the next_run of the schedule to a minute from now
        9) After a minute, list images
        10) Verify that the response code is 200
        11) Verify that there is a snapshot created for the server instance

        Attributes to verify:
        retention
        next_run
        snapshot
        """

        tenant_id = self.config.images.tenant_id
        instance_id = self.instance_id
        sch_list = []
        count = 1
        retention = self.config.images.retention
        server_daily_count = 1
        marker = None
        msg = Constants.MESSAGE

        sch_img_obj = self.images_provider.scheduled_images_client. \
            enable_scheduled_images(tenant_id, instance_id, retention)
        self.assertEquals(sch_img_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     sch_img_obj.status_code))

        sch_img = sch_img_obj.entity

        self.assertEquals(sch_img.retention, retention,
                          msg.format('retention', retention,
                                     sch_img.retention))

        keys = ["tenant", "marker"]
        values = [tenant_id, marker]

        list_sch = self.images_provider.list_schedules_pagination(keys, values)

        for s in list_sch:
            for metadata_key, metadata_value in s.metadata.items():
                if metadata_value == instance_id:
                    sch_list.append(s)
        self.assertTrue(len(sch_list) == count,
                        msg.format("length of the list", count, len(sch_list)))

        sch = sch_list[0]

        time_in_sec = calendar.timegm(time.gmtime())
        next_run_sec = time_in_sec - 60
        tm = datetime.now() - timedelta(seconds=60)
        next_run_time = tm.strftime('%Y-%m-%d %H:%M:%S')

        upd_sch_obj = \
            self.images_provider.schedules_client.update_schedule(
                id=sch.id, next_run=next_run_time)
        self.assertEquals(upd_sch_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     upd_sch_obj.status_code))

        self.images_provider.wait_for_image_to_be_created(instance_id,
                                                          server_daily_count,
                                                          next_run_sec,
                                                          sch.id)

        server_daily_list = self.images_provider.\
            get_server_daily_list(instance_id)

        self.assertTrue(len(server_daily_list) == server_daily_count,
                        msg.format("length of the list", server_daily_count,
                                   len(server_daily_list)))

        get_sch_img_settings_obj = \
            self.images_provider.scheduled_images_client. \
                get_scheduled_images_settings(tenant_id, instance_id)
        self.assertEquals(get_sch_img_settings_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     get_sch_img_settings_obj.status_code))

        get_sch_img_settings = get_sch_img_settings_obj.entity

        self.assertEquals(get_sch_img_settings.retention, retention,
                          msg.format('retention', retention,
                                     get_sch_img_settings.retention))
