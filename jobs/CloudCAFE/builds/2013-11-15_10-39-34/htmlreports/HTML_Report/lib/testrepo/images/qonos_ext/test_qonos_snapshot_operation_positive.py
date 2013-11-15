import calendar
import time
from datetime import datetime, timedelta

import ccengine.common.tools.datagen as datagen
from ccengine.common.constants.images_constants import Constants
from ccengine.common.decorators import attr
from ccengine.domain.types import NovaServerStatusTypes
from testrepo.common.testfixtures.images import BaseImagesFixture


class TestQonosSnapshotOperationPositive(BaseImagesFixture):

    @classmethod
    def setUpClass(self):
        """Creates the server instances used for all tests in this class."""

        super(TestQonosSnapshotOperationPositive, self).setUpClass()

        count = 3
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
    def test_multiple_scheduled_image_snapshot_operation(self):
        """Multiple scheduled image snapshot operation.

        1) Create two valid server instances
        2) Enable scheduled images using a valid retention value for both
        3) Verify that the response code is 200
        4) Verify that the response contains the entered retention value
        5) List schedules
        6) Verify that the response code is 200
        7) Verify that there is a schedule created for each instance
        8) Update the next_run of the schedule to a minute from now for both
        9) After a minute, list images
        10) Verify that the response code is 200
        11) Verify that there is a snapshot created for each server instance
        """

        tenant_id = self.config.images.tenant_id
        instance_id = self.servers[0].id
        alt_instance_id = self.servers[1].id
        sch_list = []
        count = 2
        retention = self.config.images.retention
        server_daily_count = 1
        marker = None
        msg = Constants.MESSAGE

        instance_ids = [instance_id, alt_instance_id]

        for id in instance_ids:
            sch_img_obj = self.images_provider.scheduled_images_client. \
                enable_scheduled_images(tenant_id, id, retention)
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
                if (metadata_value == instance_id or
                        metadata_value == alt_instance_id):
                    sch_list.append(s)
        self.assertEquals(len(sch_list), count,
                          msg.format("length of the list", count,
                                     len(sch_list)))

        time_in_sec = calendar.timegm(time.gmtime())
        next_run_sec = time_in_sec - 60
        tm = datetime.now() - timedelta(seconds=60)
        next_run_time = tm.strftime('%Y-%m-%d %H:%M:%S')

        for x in range(count):
            sch = sch_list[x]
            upd_sch_obj = \
                self.images_provider.schedules_client.update_schedule(
                    id=sch.id, next_run=next_run_time)
            self.assertEquals(upd_sch_obj.status_code, 200,
                              msg.format('status_code', 200,
                                         upd_sch_obj.status_code))

        keys = ["schedule_id", "marker"]
        values = [sch.id, marker]

        for id in instance_ids:
            self.images_provider. \
                wait_for_image_to_be_created(id, server_daily_count,
                                             next_run_sec, sch.id, keys,
                                             values)

            server_daily_list = self.images_provider.\
                get_server_daily_list(id)

            self.assertEquals(len(server_daily_list), server_daily_count,
                              msg.format("length of the list",
                                         server_daily_count,
                                         len(server_daily_list)))

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

        self.assertEquals(get_sch_img_settings.retention, retention,
                          msg.format('Instance-2 retention', retention,
                                     get_sch_img_settings.retention))

    @attr('positive')
    def test_created_by_attribute_verification(self):
        """Created by attribute verification.

        1) Create a valid server instance
        2) Enable scheduled images using a valid retention value
        3) Verify that the response code is 200
        4) Verify that the response contains the entered retention value
        5) Verify that there is a schedule created for the instance
        6) Update the next_run of the schedule to a minute from now
        7) After a minute, list images
        8) Verify that the response code is 200
        9) Verify that there is a snapshot created for the server instance
        10) Verify that the snapshot contains "created_by:
            scheduled_images_service" in the metadata
        11) Create a second valid server instance from this snapshot
        12) Create an on-demand snapshot of the second server instance
        13) Verify that snapshot does not contain "created_by:
            scheduled_images_service" in the metadata
        14) Enable scheduled images using a retention value of 1 for the
            second server instance
        15) Verify that the response code is 200
        16) Verify that the response contains the entered retention value
        17) Verify that there is a schedule created for the second server
            instance
        18) Update the next_run of the schedule to a minute from now
        19) After a minute, list images
        20) Verify that the response code is 200
        21) Verify that there is a snapshot created for the second server
            instance
        22) Verify that the snapshot contains "created_by:
            scheduled_images_service" in the metadata
        23) Verify that the on-demand snapshot of the second server is not
            deleted
        """

        tenant_id = self.config.images.tenant_id
        instance_id = self.servers[2].id
        sch_list = []
        count = 1
        retention = self.config.images.retention
        alt_retention = '1'
        server_daily_count = 1
        marker = None
        server_name = datagen.random_string(size=10)
        snapshot_name = datagen.random_string(size=10)
        image_count = 2
        msg = Constants.MESSAGE
        msg_alt = Constants.MESSAGE_ALT

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

        time_in_sec = calendar.timegm(time.gmtime())
        next_run_sec = time_in_sec - 60
        tm = datetime.now() - timedelta(seconds=60)
        next_run_time = tm.strftime('%Y-%m-%d %H:%M:%S')

        upd_sch_obj = self.images_provider. \
            schedules_client.update_schedule(id=sch.id, next_run=next_run_time)
        self.assertEquals(upd_sch_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     upd_sch_obj.status_code))

        keys = ["schedule_id", "marker"]
        values = [sch.id, marker]

        self.images_provider.wait_for_image_to_be_created(instance_id,
                                                          server_daily_count,
                                                          next_run_sec,
                                                          sch.id, keys, values)

        server_daily_list = self.images_provider.\
            get_server_daily_list(instance_id)
        self.assertEquals(len(server_daily_list), server_daily_count,
                          msg.format("length of the list", server_daily_count,
                                     len(server_daily_list)))

        first_snapshot_obj = self.images_provider.nova_images_client. \
            get_image(server_daily_list[0])

        created_by = getattr(first_snapshot_obj.entity.metadata,
                             "org.openstack__1__created_by")
        self.assertEquals(created_by, "scheduled_images_service",
                          msg.format('created_by', "scheduled_images_service",
                                     created_by))

        server_obj = self.images_provider. \
            create_active_server(server_name,
                                 image_ref=first_snapshot_obj.entity.id)
        self.assertEquals(server_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     server_obj.status_code))

        created_second_snapshot_id = self.images_provider. \
            create_active_snapshot(server_obj.entity.id,
                                   snapshot_name=snapshot_name)

        second_snapshot_obj = self.images_provider.nova_images_client. \
            get_image(created_second_snapshot_id)

        self.assertFalse(hasattr(second_snapshot_obj.entity.metadata,
                                 "org.openstack__1__created_by"),
                         msg.format("org.openstack__1__created_by",
                                    'to not be present', 'was present'))

        # Repeated from above from here through almost end, minus the kv pairs
        sch_img_obj = self.images_provider.scheduled_images_client. \
            enable_scheduled_images(tenant_id, server_obj.entity.id,
                                    alt_retention)
        self.assertEquals(sch_img_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     sch_img_obj.status_code))

        sch_img = sch_img_obj.entity

        self.assertEquals(sch_img.retention, alt_retention,
                          msg.format('retention', alt_retention,
                                     sch_img.retention))

        keys = ["tenant", "marker"]
        values = [tenant_id, marker]

        list_sch = self.images_provider.list_schedules_pagination(keys, values)

        sch_list = []

        for s in list_sch:
            for metadata_key, metadata_value in s.metadata.items():
                if metadata_value == server_obj.entity.id:
                    sch_list.append(s)
        self.assertEquals(len(sch_list), count,
                          msg.format("length of the list", count,
                                     len(sch_list)))

        sch = sch_list[0]

        time_in_sec = calendar.timegm(time.gmtime())
        next_run_sec = time_in_sec - 60
        tm = datetime.now() - timedelta(seconds=60)
        next_run_time = tm.strftime('%Y-%m-%d %H:%M:%S')

        upd_sch_obj = self.images_provider. \
            schedules_client.update_schedule(id=sch.id, next_run=next_run_time)
        self.assertEquals(upd_sch_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     upd_sch_obj.status_code))

        keys = ["schedule_id", "marker"]
        values = [sch.id, marker]

        self.images_provider.wait_for_image_to_be_created(server_obj.entity.id,
                                                          2, next_run_sec,
                                                          sch.id, keys, values)

        server_daily_list = self.images_provider.\
            get_server_daily_list(server_obj.entity.id)

        self.assertEquals(len(server_daily_list), server_daily_count,
                          msg.format("length of the list", server_daily_count,
                                     len(server_daily_list)))

        third_snapshot_obj = self.images_provider.nova_images_client. \
            get_image(server_daily_list[0])

        third_created_by = getattr(third_snapshot_obj.entity.metadata,
                                   "org.openstack__1__created_by")
        self.assertEquals(third_created_by, "scheduled_images_service",
                          msg.format('created_by', "scheduled_images_service",
                                     third_created_by))

        list_images = self.images_provider.list_images_pagination()

        image_list = [i for i in list_images if hasattr(i, "server")
                      and i.server.id == server_obj.entity.id]
        self.assertEquals(len(image_list), image_count,
                          msg.format("length of the list", image_count,
                                     len(image_list)))

        for i in image_list:
            if i.id == second_snapshot_obj.entity.id:
                self.assertFalse(hasattr(i.metadata,
                                         "org.openstack__1__created_by"),
                                 msg.format("org.openstack__1__created_by",
                                            'to not be present',
                                            'was present'))
            elif i.id == third_snapshot_obj.entity.id:
                created_by = getattr(i.metadata,
                                     "org.openstack__1__created_by")
                self.assertEquals(created_by, "scheduled_images_service",
                                  msg.format('created_by',
                                             "scheduled_images_service",
                                             created_by))
            else:
                self.fail(msg_alt.format('image id',
                                         second_snapshot_obj.entity.id,
                                         third_snapshot_obj.entity.id, i.id))
