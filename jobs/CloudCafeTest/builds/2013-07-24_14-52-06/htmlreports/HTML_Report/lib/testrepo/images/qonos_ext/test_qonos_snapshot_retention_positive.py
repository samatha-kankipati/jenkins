from testrepo.common.testfixtures.images import BaseImagesFixture
from ccengine.common.constants.images_constants import Constants
from ccengine.common.decorators import attr
from ccengine.domain.types import NovaServerStatusTypes
import calendar
import time
import ccengine.common.tools.datagen as datagen
from ccengine.domain.types import NovaImageStatusTypes as status
from datetime import datetime, timedelta


class TestQonosSnapshotRetentionPositive(BaseImagesFixture):

    @classmethod
    def setUpClass(self):
        '''Creates the server instances used for all tests in this class'''

        super(TestQonosSnapshotRetentionPositive, self).setUpClass()

        count = 2
        self.servers = []

        for x in range(count):
            server_name = datagen.random_string(size=10)
            server_obj = \
                self.images_provider.create_server_no_wait(server_name)
            self.servers.append(server_obj.entity)

        for server in self.servers:
            self.images_provider.\
                wait_for_server_status(server.id,
                                       NovaServerStatusTypes.ACTIVE)

    @attr('positive')
    def test_multiple_scheduled_image_retention(self):
        '''Multiple scheduled image retention'''

        """
        1) Create two valid server instances
        2) Enable scheduled images using a value of 2 for the first instance
        3) Verify that the response code is 200
        4) Verify that the response contains the entered retention value
        5) Enable scheduled images using a value of 3 for the second instance
        6) Verify that the response code is 200
        7) Verify that the response contains the entered retention value
        8) List schedules
        9) Verify that the response code is 200
        10) Verify that there is a schedule created for each instance
        11) Update the next_run of the schedule to a minute from now for the
        first instance
        12) After a minute, list images
        13) Verify that the response code is 200
        14) Verify that there is a snapshot created for the first instance
        15) Repeat steps 11-14 for a second snapshot
        16) Verify that the first snapshot is not deleted
        17) Repeat steps 11-14 for a third snapshot
        18) Verify that the first snapshot is deleted
        19) Verify that the second snapshot is not deleted
        20) Update the next_run of the schedule to a minute from now for the
        second instance
        21) After a minute, list images
        22) Verify that the response code is 200
        23) Verify that there is a snapshot created for the second instance
        24) Repeat steps 20-23 for a second snapshot
        25) Verify that the first snapshot is not deleted
        26) Repeat steps 20-23 for a third snapshot
        27) Verify that the first snapshot is not deleted
        28) Verify that the second snapshot is not deleted
        29) Repeat steps 20-23 for a forth snapshot
        30) Verify that the first snapshot is deleted
        31) Verify that the second snapshot is not deleted
        32) Verify that the third snapshot is not deleted
        33) Verify that the first set of snapshots for the first instance are
        not deleted

        Attributes to verify:
        retention
        next_run
        snapshot
        """

        tenant_id = self.config.images.tenant_id
        instance_id = self.servers[0].id
        alt_instance_id = self.servers[1].id
        retention = self.config.images.retention
        alt_retention = self.config.images.alt_retention
        server_daily_count = 3
        alt_server_daily_count = 4
        marker = None
        msg = Constants.MESSAGE

        instance_ids = [instance_id, alt_instance_id]

        for id in instance_ids:
            if id == instance_id:
                ret = retention
            elif id == alt_instance_id:
                ret = alt_retention
            sch_img_obj = self.images_provider.scheduled_images_client. \
                enable_scheduled_images(tenant_id, id, ret)
            self.assertEquals(sch_img_obj.status_code, 200,
                              msg.format('status_code', 200,
                                         sch_img_obj.status_code))

            sch_img = sch_img_obj.entity

            self.assertEquals(sch_img.retention, ret,
                              msg.format('retention', ret,
                                         sch_img.retention))

        keys = ["tenant", "marker"]
        values = [tenant_id, marker]

        list_sch = self.images_provider.list_schedules_pagination(keys, values)

        for s in list_sch:
            for metadata_key, metadata_value in s.metadata.items():
                if metadata_value == instance_id:
                    sch = s
                elif metadata_value == alt_instance_id:
                    alt_sch = s

        # Verify that a first set of snapshots can be taken
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

            self.images_provider. \
                wait_for_new_image_to_be_created(instance_id, next_run_sec,
                                                 sch.id)

            server_daily_list = self.images_provider.\
                get_server_daily_list(instance_id)

            self.assertTrue(len(server_daily_list) > 0,
                            msg.format("length of the daily snapshot",
                                       "More than 1", len(server_daily_list)))
            if x == 0:
                self.assertTrue(len(server_daily_list) == (x + 1),
                                msg.format("length of the list", (x + 1),
                                           len(server_daily_list)))
                first_snapshot = server_daily_list[0]
                self.snapshots_to_delete.append(first_snapshot)
            if x == 1:
                self.assertTrue(len(server_daily_list) == (x + 1),
                                msg.format("length of the list", (x + 1),
                                           len(server_daily_list)))
                second_snapshot = server_daily_list[0]
                self.snapshots_to_delete.append(second_snapshot)
                self.assertTrue(first_snapshot in server_daily_list,
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
                self.assertTrue(len(server_daily_list) == (x),
                                msg.format("length of the list", (x),
                                           len(server_daily_list)))
                self.assertTrue(first_snapshot not in server_daily_list,
                                msg.format("first snapshot not present",
                                           "first snapshot to not be present",
                                           "first snapshot present"))
                self.assertTrue(second_snapshot in server_daily_list,
                                msg.format("second snapshot present",
                                           "second snapshot to be present",
                                           "second snapshot not present"))

        sch = alt_sch

        # Verify that a second set of snapshots can be taken as expected
        for x in range(alt_server_daily_count):
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

            self.images_provider. \
                wait_for_new_image_to_be_created(alt_instance_id, next_run_sec,
                                                 sch.id)

            server_daily_list = self.images_provider.\
                    get_server_daily_list(alt_instance_id)
            self.assertTrue(len(server_daily_list) > 0,
                            msg.format("length of the daily snapshot",
                                       "More than 1", len(server_daily_list)))

            if x == 0:
                self.assertTrue(len(server_daily_list) == (x + 1),
                                msg.format("length of the list", (x + 1),
                                           len(server_daily_list)))
                alt_first_snapshot = server_daily_list[0]
                self.snapshots_to_delete.append(alt_first_snapshot)
            if x == 1:
                self.assertTrue(len(server_daily_list) == (x + 1),
                                msg.format("length of the list", (x + 1),
                                           len(server_daily_list)))
                alt_second_snapshot = server_daily_list[0]
                self.snapshots_to_delete.append(alt_second_snapshot)
                self.assertTrue(alt_first_snapshot in server_daily_list,
                                msg.format("first snapshot present",
                                           "first snapshot to be present",
                                           "first snapshot not present"))
            if x == 2:
                self.assertTrue(len(server_daily_list) == (x + 1),
                                msg.format("length of the list", (x + 1),
                                           len(server_daily_list)))
                alt_third_snapshot = server_daily_list[0]
                self.snapshots_to_delete.append(alt_third_snapshot)
                self.assertTrue(alt_first_snapshot in server_daily_list,
                                msg.format("first snapshot present",
                                           "first snapshot to be present",
                                           "first snapshot not present"))
                self.assertTrue(alt_second_snapshot in server_daily_list,
                                msg.format("second snapshot present",
                                           "second snapshot to be present",
                                           "second snapshot not present"))
            if x == 3:
                alt_forth_snapshot = server_daily_list[0]
                self.snapshots_to_delete.append(alt_forth_snapshot)
                self.images_provider.wait_for_image_status(alt_first_snapshot,
                                                           status.DELETED)
                server_daily_list = self.images_provider.\
                    get_server_daily_list(alt_instance_id)
                self.assertTrue(len(server_daily_list) == (x),
                                msg.format("length of the list", (x),
                                           len(server_daily_list)))
                self.assertTrue(alt_first_snapshot not in server_daily_list,
                                msg.format("first snapshot not present",
                                           "first snapshot to not be present",
                                           "first snapshot present"))
                self.assertTrue(alt_second_snapshot in server_daily_list,
                                msg.format("second snapshot present",
                                           "second snapshot to be present",
                                           "second snapshot not present"))
                self.assertTrue(alt_third_snapshot in server_daily_list,
                                msg.format("third snapshot present",
                                           "third snapshot to be present",
                                           "third snapshot not present"))

            # Verify that the original snapshots still exist
            server_daily_list = self.images_provider.\
                get_server_daily_list(instance_id)

            self.assertTrue(first_snapshot not in server_daily_list,
                                msg.format("first snapshot not present",
                                           "first snapshot to not be present",
                                           "first snapshot present"))
            self.assertTrue(second_snapshot in server_daily_list,
                                msg.format("second snapshot present",
                                           "second snapshot to be present",
                                           "second snapshot not present"))
            self.assertTrue(third_snapshot in server_daily_list,
                                msg.format("third snapshot present",
                                           "third snapshot to be present",
                                           "third snapshot not present"))

        get_sch_img_settings_obj = \
            self.images_provider.scheduled_images_client. \
                get_scheduled_images_settings(tenant_id, instance_id)
        self.assertEquals(get_sch_img_settings_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     get_sch_img_settings_obj.status_code))

        get_sch_img_settings = get_sch_img_settings_obj.entity

        self.assertEquals(get_sch_img_settings.retention, retention,
                          msg.format('Instance-1 retention', retention,
                                     get_sch_img_settings.retention))

        get_sch_img_settings_obj = \
            self.images_provider.scheduled_images_client. \
                get_scheduled_images_settings(tenant_id, alt_instance_id)
        self.assertEquals(get_sch_img_settings_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     get_sch_img_settings_obj.status_code))

        get_sch_img_settings = get_sch_img_settings_obj.entity

        self.assertEquals(get_sch_img_settings.retention, alt_retention,
                          msg.format('Instance-2 retention', alt_retention,
                                     get_sch_img_settings.retention))
