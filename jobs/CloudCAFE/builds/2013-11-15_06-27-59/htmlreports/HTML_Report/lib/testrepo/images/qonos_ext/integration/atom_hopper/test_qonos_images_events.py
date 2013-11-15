import calendar
from datetime import datetime, timedelta
import time

from ccengine.common.decorators import attr
import ccengine.common.tools.datagen as datagen
from ccengine.domain.types import NovaImageStatusTypes as status
from testrepo.common.testfixtures.atomhopper_events_validator\
    .events_validator import EventsValidator
from testrepo.common.testfixtures.images import ImagesEventsFixture


class TestQonosImagesEvents(ImagesEventsFixture, EventsValidator):

    @classmethod
    def setUpClass(self):
        """Creates the server instances used for all tests in this class."""

        super(TestQonosImagesEvents, self).setUpClass()

        server_name = datagen.random_string(size=10)

        server_obj = self.images_provider.create_active_server(server_name)
        self.instance_id = server_obj.entity.id

        self.date_break = datetime.utcnow() - timedelta(hours=1)

    @attr('images_events')
    def test_create_delete_image_events_by_qonos(self):
        """Create and Delete image events triggered by scheduled images.

        1) Create a valid server instance
        2) Create an on-demand snap for that server
        3) Enable scheduled images with retention value of 2
        4) Update next_run of the schedule to current time and
        hence scheduled image is created
        5) Once first image is active, make sure image.activate event
        is emitted for that.
        6) Update next_run of the schedule again to current time and
        make sure second image is created
        7) Once second image is active, make sure image.activate event
        is emitted for that.
        8) Update next_run of the schedule again to current time and
        make sure third image is created
        9) Once third image is active, make sure image.activate event
        is emitted for third image
        10) Verify first image is deleted and on-demand snap is active
        11) Verify image.delete event is emitted for first scheduled image and
        not for on-demand snapshot
        12) Delete second image through nova api and
        make sure image.delete event is emitted for that
        """

        snapshot_name = datagen.random_string(size=10)
        server_daily_count = 3
        marker = None
        sch_list = []
        count = 1

        on_demand_snap = self.images_provider. \
            create_active_snapshot(self.instance_id,
                                   snapshot_name=snapshot_name)

        sch_img_obj = self.images_provider.scheduled_images_client. \
            enable_scheduled_images(self.tenant_id, self.instance_id,
                                    self.retention)
        self.assertEqual(sch_img_obj.status_code, 200,
                         self.msg.format('status_code', 200,
                                         sch_img_obj.status_code))

        keys = ["tenant", "marker"]
        values = [self.tenant_id, marker]

        list_sch = self.images_provider.list_schedules_pagination(keys, values)

        for s in list_sch:
            for metadata_key, metadata_value in s.metadata.items():
                if metadata_value == self.instance_id:
                    sch_list.append(s)
        self.assertEqual(len(sch_list), count,
                         self.msg.format("length of the list", count,
                                         len(sch_list)))

        sch = sch_list[0]

        for no_of_daily_img in range(1, server_daily_count + 1):
            time_in_sec = calendar.timegm(time.gmtime())
            next_run_sec = time_in_sec - 60
            tm = datetime.now() - timedelta(seconds=60)
            next_run = tm.strftime('%Y-%m-%d %H:%M:%S')

            upd_sch_obj = self.images_provider. \
                schedules_client.update_schedule(id=sch.id, next_run=next_run)
            self.assertEqual(upd_sch_obj.status_code, 200,
                             self.msg.format('status_code', 200,
                                             upd_sch_obj.status_code))

            created_at = datetime.utcnow()

            self.images_provider. \
                wait_for_new_image_to_be_created(self.instance_id,
                                                 next_run_sec, sch.id)

            server_daily_list = self.images_provider.\
                get_server_daily_list(self.instance_id)

            if no_of_daily_img == 1:
                self.assertEqual(len(server_daily_list), no_of_daily_img,
                                 self.msg.format("length of the list",
                                                 no_of_daily_img,
                                                 len(server_daily_list)))
                first_snapshot = server_daily_list[0]
                self.snapshots_to_delete.append(first_snapshot)
            if no_of_daily_img == 2:
                self.assertEqual(len(server_daily_list), no_of_daily_img,
                                 self.msg.format("length of the list",
                                                 no_of_daily_img,
                                                 len(server_daily_list)))
                second_snapshot = server_daily_list[0]
                self.assertListEqual(server_daily_list,
                                     [second_snapshot, first_snapshot],
                                     self.msg.format(
                                         "Server daily list",
                                         "2nd and 1st snap",
                                         "2nd and 1st snap not present"))
                self.snapshots_to_delete.append(second_snapshot)

            if no_of_daily_img == 3:
                # deleted_at of first snapshot is third snap created_at time
                deleted_at = datetime.utcnow()
                self.assertEqual(len(server_daily_list), self.retention,
                                 self.msg.format("length of the list",
                                                 self.retention,
                                                 len(server_daily_list)))
                third_snapshot = server_daily_list[0]
                self.assertListEqual(server_daily_list,
                                     [third_snapshot, second_snapshot],
                                     self.msg.format(
                                         "Server daily list",
                                         "3rd and 2nd snap",
                                         "3rd and 2nd snap not present"))

                self.snapshots_to_delete.append(third_snapshot)
                self.assertNotEqual(second_snapshot, third_snapshot,
                                    self.msg.format("snapshot id",
                                                    "Different snapshot id",
                                                    "Same snapshot id"))

            si_image_obj = self.images_provider.nova_images_client. \
                get_image(server_daily_list[0])

            self.glance_atomhopper_provider.\
                wait_for_atomhopper_timestamp(created_at)

            # Get expected data for verification
            expected_data = {'image': si_image_obj.entity,
                             'image_created_at':
                             created_at.strftime("%Y-%m-%dT%H:%M:%S")}
            expected_event_types = ["image.update", "image.update",
                                    "image.activate", "image.upload",
                                    "image.prepare", "image.create"]
            self.get_and_verify_ah_events(
                wait_for_timestamp=created_at,
                date_break=self.date_break,
                expected_data=expected_data,
                expected_event_types=expected_event_types)

        self.images_provider.wait_for_image_status(first_snapshot,
                                                   status.DELETED)
        on_demand_snap_obj = self.images_provider.nova_images_client. \
            get_image(on_demand_snap)
        self.assertEqual(on_demand_snap_obj.entity.status, status.ACTIVE,
                         self.msg.format("Image Status", "Active",
                                         on_demand_snap_obj.entity.status))

        si_image_obj = self.images_provider.nova_images_client. \
            get_image(first_snapshot)

        self.glance_atomhopper_provider.\
            wait_for_atomhopper_timestamp(deleted_at)

        # Get expected data for verification
        expected_data = {'image': si_image_obj.entity,
                         'image_deleted_at':
                         deleted_at.strftime("%Y-%m-%dT%H:%M:%S")}
        # Check event counts in order
        expected_event_types = ["image.delete", "image.update", "image.update",
                                "image.activate", "image.upload",
                                "image.prepare", "image.create"]

        self.get_and_verify_ah_events(
            wait_for_timestamp=deleted_at,
            date_break=self.date_break,
            expected_data=expected_data,
            expected_event_types=expected_event_types)

        # Delete second image through nova api and verify image.delete event
        # RM#2338
        second_snap_deleted_at = datetime.utcnow()

        self.images_provider.nova_images_client.delete_image(second_snapshot)

        si_image_obj = self.images_provider.nova_images_client. \
            get_image(second_snapshot)

        self.glance_atomhopper_provider.\
            wait_for_atomhopper_timestamp(second_snap_deleted_at)

        # Get expected data for verification
        expected_data = {'image': si_image_obj.entity,
                         'image_deleted_at':
                         second_snap_deleted_at.strftime("%Y-%m-%dT%H:%M:%S")}
        # Check event counts in order
        expected_event_types = ["image.delete", "image.update", "image.update",
                                "image.activate", "image.upload",
                                "image.prepare", "image.create"]

        self.get_and_verify_ah_events(
            wait_for_timestamp=second_snap_deleted_at,
            date_break=self.date_break,
            expected_data=expected_data,
            expected_event_types=expected_event_types)
