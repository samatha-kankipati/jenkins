import calendar
import time
from datetime import datetime, timedelta

import ccengine.common.tools.datagen as datagen
from ccengine.common.constants.images_constants import Constants
from ccengine.common.decorators import attr
from ccengine.domain.types import NovaImageStatusTypes as status
from testrepo.common.testfixtures.images import BaseImagesFixture


class TestQonosSnapshotRetention(BaseImagesFixture):

    @classmethod
    def setUpClass(self):
        """Creates the server instance used for all tests in this class."""

        super(TestQonosSnapshotRetention, self).setUpClass()

        server_name = datagen.random_string(size=10)

        server_obj = self.images_provider.create_active_server(server_name)

        self.instance_id = server_obj.entity.id

    @attr('positive')
    def test_happy_path_scheduled_image_snapshot_retention(self):
        """Happy Path - Scheduled image snapshot retention.

        1) Create a valid server instance
        2) Enable scheduled images using a retention value of 2
        3) Verify that the response code is 200
        4) Verify that the response contains the entered retention value
        5) List schedules
        6) Verify that the response code is 200
        7) Verify that there is a schedule created for the instance
        8) Update the next_run of the schedule to a minute from now
        9) After a minute, list images
        10) Verify that the response code is 200
        11) Verify that there is a snapshot created for the server instance
        12) Repeat steps 8-11 for a second snapshot
        13) Verify that the first snapshot is not deleted
        14) Repeat steps 8-11 for a third snapshot
        15) Verify that the first snapshot is deleted
        16) Verify that the second snapshot is not deleted
        """

        tenant_id = self.config.images.tenant_id
        instance_id = self.instance_id
        sch_list = []
        count = 1
        retention = self.config.images.retention
        server_daily_count = 3
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
        self.assertEquals(len(sch_list), count,
                          msg.format("length of the list", count,
                                     len(sch_list)))

        sch = sch_list[0]

        for x in range(server_daily_count):
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

            keys = ["schedule_id", "marker"]
            values = [sch.id, marker]

            self.images_provider.wait_for_new_image_to_be_created(instance_id,
                                                                  next_run_sec,
                                                                  sch.id, keys,
                                                                  values)

            server_daily_list = self.images_provider.\
                get_server_daily_list(instance_id)

            self.assertGreater(len(server_daily_list), 0,
                               msg.format("length of the daily snapshot",
                                          "More than 1",
                                          len(server_daily_list)))

            if x == 0:
                self.assertEquals(len(server_daily_list), x + 1,
                                  msg.format("length of the list", x + 1,
                                             len(server_daily_list)))
                first_snapshot = server_daily_list[0]
                self.snapshots_to_delete.append(first_snapshot)
            if x == 1:
                self.assertEquals(len(server_daily_list), x + 1,
                                  msg.format("length of the list", x + 1,
                                             len(server_daily_list)))
                second_snapshot = server_daily_list[0]
                self.snapshots_to_delete.append(second_snapshot)
                self.assertIn(first_snapshot, server_daily_list,
                              msg.format("first snapshot present",
                                         "first snapshot to be present",
                                         "first snapshot not present"))
            if x == 2:
                third_snapshot = server_daily_list[0]
                self.snapshots_to_delete.append(third_snapshot)
                self.images_provider.wait_for_image_status(first_snapshot,
                                                           status.DELETED)
                server_daily_list = self.images_provider.\
                    get_server_daily_list(instance_id)
                self.assertEquals(len(server_daily_list), x,
                                  msg.format("length of the list", x,
                                             len(server_daily_list)))
                self.assertNotIn(first_snapshot, server_daily_list,
                                 msg.format("first snapshot not present",
                                            "first snapshot to not be present",
                                            "first snapshot present"))
                self.assertIn(second_snapshot, server_daily_list,
                              msg.format("second snapshot present",
                                         "second snapshot to be present",
                                         "second snapshot not present"))

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
