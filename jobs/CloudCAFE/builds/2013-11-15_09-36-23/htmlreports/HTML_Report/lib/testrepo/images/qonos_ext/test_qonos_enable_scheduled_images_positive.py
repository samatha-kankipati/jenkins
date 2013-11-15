from datetime import datetime, timedelta

import ccengine.common.tools.datagen as datagen
from ccengine.common.constants.images_constants import Constants
from ccengine.common.decorators import attr
from ccengine.common.exceptions.compute import BadRequest, ItemNotFound
from ccengine.domain.types import NovaServerStatusTypes
from testrepo.common.testfixtures.images import BaseImagesFixture


class TestQonosEnableScheduledImagesPositive(BaseImagesFixture):

    @classmethod
    def setUpClass(cls):
        """Creates the server instances and snapshots used for all tests in
        this class.
        """

        super(TestQonosEnableScheduledImagesPositive, cls).setUpClass()

        count = 2
        servers = []

        for x in range(count):
            server_name = datagen.random_string(size=10)
            server_obj = cls.images_provider.create_server_no_wait(server_name)
            servers.append(server_obj.entity)

        cls.instance_id = servers[0].id
        cls.alt_instance_id = servers[1].id

        for server in servers:
            cls.images_provider.\
                wait_for_server_status(server.id,
                                       NovaServerStatusTypes.ACTIVE)

    @attr('positive')
    def test_enable_scheduled_images_with_retention_more_than_1(self):
        """Enable scheduled images with a retention of more than 1.

        1) Create a valid server instance
        2) Enable scheduled images using a valid retention value more than 1
        3) Verify that the response code is 200
        4) Verify that the response contains the entered retention value
        """

        tenant_id = self.config.images.tenant_id
        instance_id = self.instance_id
        retention = self.config.images.alt_retention
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

    @attr('positive')
    def test_enable_sch_img_on_more_than_one_server_cust_owns(self):
        """Enable scheduled images on more than one server that the same
        customer owns.

        1) Create 2 valid server instances
        2) Enable scheduled images on both instances
        3) Verify that the response code is 200
        4) List schedules
        5) Verify that the response code is 200
        6) Verify that schedules exist for both instances
        """

        tenant_id = self.config.images.tenant_id
        instance_id = self.instance_id
        alt_instance_id = self.alt_instance_id
        retention = self.config.images.alt_retention
        sch_list = []
        count = 2
        marker = None
        msg = Constants.MESSAGE

        sch_img_obj = self.images_provider.scheduled_images_client. \
            enable_scheduled_images(tenant_id, instance_id, retention)
        self.assertEquals(sch_img_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     sch_img_obj.status_code))

        sch_img_1 = sch_img_obj.entity

        self.assertEquals(sch_img_1.retention, retention,
                          msg.format('retention', retention,
                                     sch_img_1.retention))

        sch_img_obj = self.images_provider.scheduled_images_client. \
            enable_scheduled_images(tenant_id, alt_instance_id, retention)
        self.assertEquals(sch_img_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     sch_img_obj.status_code))

        sch_img_2 = sch_img_obj.entity

        self.assertEquals(sch_img_2.retention, retention,
                          msg.format('retention', retention,
                                     sch_img_2.retention))

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

    @attr('positive')
    def test_enable_scheduled_images_for_a_server_disable_it(self):
        """Enable scheduled images for a server, and immediately disable it.

        1) Create a valid server instance
        2) Enable scheduled images using a valid retention value
        3) Verify that the response code is 200
        4) Disable scheduled images
        5) Verify that the response code is 202
        6) List schedules
        7) Verify that the response code is 200
        8) Verify that the schedule no longer exists
        """

        tenant_id = self.config.images.tenant_id
        instance_id = self.instance_id
        sch_list = []
        count = 0
        retention = self.config.images.retention
        marker = None
        msg = Constants.MESSAGE

        sch_img_obj = self.images_provider.scheduled_images_client. \
            enable_scheduled_images(tenant_id, instance_id, retention)

        self.assertEquals(sch_img_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     sch_img_obj.status_code))

        dis_sch_img_obj = self.images_provider.scheduled_images_client. \
            disable_scheduled_images(tenant_id, instance_id)
        self.assertEquals(dis_sch_img_obj.status_code, 202,
                          msg.format('status_code', 202,
                                     dis_sch_img_obj.status_code))

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

    @attr('positive')
    def test_enable_scheduled_images_server_disable_it_enable_it(self):
        """Enable scheduled images for a server, disable it, enable it again.

        1) Create a valid server instance
        2) Enable scheduled images using a valid retention value
        3) Verify that the response code is 200
        4) Disable scheduled images
        5) Verify that the response code is 202
        6) Enabled scheduled images again using the same retention value
        7) Verify that the response code is 200
        8) Verify that the response contains the entered retention value
        9) List schedules
        10) Verify that the response code is 200
        11) Verify that there is a schedule created for the instance
        """

        tenant_id = self.config.images.tenant_id
        instance_id = self.instance_id
        sch_list = []
        count = 1
        retention = self.config.images.retention
        marker = None
        msg = Constants.MESSAGE

        sch_img_obj = self.images_provider.scheduled_images_client. \
            enable_scheduled_images(tenant_id, instance_id, retention)

        self.assertEquals(sch_img_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     sch_img_obj.status_code))

        dis_sch_img_obj = self.images_provider.scheduled_images_client. \
            disable_scheduled_images(tenant_id, instance_id)
        self.assertEquals(dis_sch_img_obj.status_code, 202,
                          msg.format('status_code', 202,
                                     dis_sch_img_obj.status_code))

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

    @attr('positive')
    def test_enable_scheduled_images_disable_enable_larger_ret(self):
        """Enable schedule images for a server with a retention of 1, disable
        it, enable it again with larger retention.

        1) Create a valid server instance
        2) Enable scheduled images using a valid retention value
        3) Verify that the response code is 200
        4) Disable scheduled images
        5) Verify that the response code is 202
        6) Enabled scheduled images again using a larger retention value
        7) Verify that the response code is 200
        8) Verify that the response contains the entered retention value
        """

        tenant_id = self.config.images.tenant_id
        instance_id = self.instance_id
        retention = self.config.images.retention
        alt_retention = self.config.images.alt_retention
        msg = Constants.MESSAGE

        sch_img_obj = self.images_provider.scheduled_images_client. \
            enable_scheduled_images(tenant_id, instance_id, retention)
        self.assertEquals(sch_img_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     sch_img_obj.status_code))

        dis_sch_img_obj = self.images_provider.scheduled_images_client. \
            disable_scheduled_images(tenant_id, instance_id)
        self.assertEquals(dis_sch_img_obj.status_code, 202,
                          msg.format('status_code', 202,
                                     dis_sch_img_obj.status_code))

        sch_img_obj = self.images_provider.scheduled_images_client. \
            enable_scheduled_images(tenant_id, instance_id, alt_retention)
        self.assertEquals(sch_img_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     sch_img_obj.status_code))

        sch_img = sch_img_obj.entity

        self.assertEquals(sch_img.retention, alt_retention,
                          msg.format('retention', alt_retention,
                                     sch_img.retention))

    @attr('positive')
    def test_enable_scheduled_images_for_server_already_enabled(self):
        """Enable scheduled images for a server that is already enabled, with
        the same retention.

        1) Create a valid server instance
        2) Enable scheduled images using a valid retention value
        3) Verify that the response code is 200
        4) Enabled scheduled images again using the same retention value
        5) Verify that the response code is 200
        6) Verify that the response contains the entered retention value
        7) List schedules
        8) Verify that the response code is 200
        9) Verify that there is a schedule created for the instance
        """

        tenant_id = self.config.images.tenant_id
        instance_id = self.instance_id
        sch_list = []
        count = 1
        retention = self.config.images.retention
        marker = None
        msg = Constants.MESSAGE

        sch_img_obj = self.images_provider.scheduled_images_client. \
            enable_scheduled_images(tenant_id, instance_id, retention)

        self.assertEquals(sch_img_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     sch_img_obj.status_code))

        sch_img_obj = self.images_provider.scheduled_images_client. \
            enable_scheduled_images(tenant_id, instance_id, retention)
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
        self.assertEquals(len(sch_list), count,
                          msg.format("length of the list", count,
                                     len(sch_list)))

        self.assertEquals(sch_img.retention, retention,
                          msg.format('retention', retention,
                                     sch_img.retention))

    @attr('positive')
    def test_enable_scheduled_images_already_enabled_diff_ret(self):
        """Enable scheduled images for a server that is already enabled, with a
        different retention.

        1) Create a valid server instance
        2) Enable scheduled images using a valid retention value
        3) Verify that the response code is 200
        4) Enabled scheduled images again using the different retention value
        5) Verify that the response code is 200
        6) Verify that the response contains the entered retention value
        """

        tenant_id = self.config.images.tenant_id
        instance_id = self.instance_id
        retention = self.config.images.retention
        alt_retention = self.config.images.alt_retention
        msg = Constants.MESSAGE

        sch_img_obj = self.images_provider.scheduled_images_client. \
            enable_scheduled_images(tenant_id, instance_id, retention)
        self.assertEquals(sch_img_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     sch_img_obj.status_code))

        sch_img_obj = self.images_provider.scheduled_images_client. \
            enable_scheduled_images(tenant_id, instance_id, alt_retention)
        self.assertEquals(sch_img_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     sch_img_obj.status_code))

        sch_img = sch_img_obj.entity

        self.assertEquals(sch_img.retention, alt_retention,
                          msg.format('retention', alt_retention,
                                     sch_img.retention))

    @attr('positive')
    def test_enable_sch_images_for_already_enabled_w_invalid_ret(self):
        """Enable scheduled images for a server that is already enabled, with a
        invalid retention value.

        1) Create a valid server instance
        2) Create a faux scheduled image snapshot
        3) Verify that the response code is 202
        4) Enable scheduled images using a valid retention value
        5) Verify that the response code is 200
        6) Enable scheduled images again with an invalid retention value
        7) Verify that the response code 500
        8) Get scheduled images settings
        9) Verify that the response code is 200
        10) Verify that the original retention value remains intact
        11) List images for the account
        12) Verify that the response code is 200
        13) Verify that the scheduled image snapshot is still present
        """

        tenant_id = self.config.images.tenant_id
        instance_id = self.instance_id
        retention = self.config.images.retention
        invalid_retention = 'test'
        snapshot_name = datagen.random_string(size=10)
        metadata = {self.config.images.sch_img_metadata_key:
                    self.config.images.sch_img_metadata_value}
        image_names = []
        msg = Constants.MESSAGE

        faux_sch_img_obj = \
            self.images_provider.create_faux_scheduled_image(instance_id,
                                                             snapshot_name,
                                                             metadata)
        self.assertEquals(faux_sch_img_obj.status_code, 202,
                          msg.format('status_code', 202,
                                     faux_sch_img_obj.status_code))

        sch_img_obj = self.images_provider.scheduled_images_client. \
            enable_scheduled_images(tenant_id, instance_id, retention)
        self.assertEquals(sch_img_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     sch_img_obj.status_code))

        sch_img = sch_img_obj.entity

        with self.assertRaises(BadRequest):
            self.images_provider.scheduled_images_client. \
                enable_scheduled_images(tenant_id, instance_id,
                                        invalid_retention)

        get_sch_img_settings_obj = (self.images_provider.
                                    scheduled_images_client.
                                    get_scheduled_images_settings(tenant_id,
                                                                  instance_id))
        self.assertEquals(get_sch_img_settings_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     get_sch_img_settings_obj.status_code))

        get_sch_img_settings = get_sch_img_settings_obj.entity

        self.assertEquals(get_sch_img_settings.retention, sch_img.retention,
                          msg.format('retention', sch_img.retention,
                                     get_sch_img_settings.retention))

        list_images = self.images_provider.list_images_pagination()

        for image in list_images:
            image_names.append(image.name)

        self.assertIn(snapshot_name, image_names,
                      msg.format('snapshot_name',
                                 'snapshot to be in listed images',
                                 'snapshot not in listed images'))

    @attr('positive')
    def test_enable_sch_images_for_already_enabled_w_ret_of_0(self):
        """Enable scheduled images for a server that is already enabled, and
        then update with a 0 retention value.

        1) Create a valid server instance
        2) Create a faux scheduled image snapshot
        3) Verify that the response code is 202
        4) Enable scheduled images using a valid retention value
        5) Verify that the response code is 200
        6) Enable scheduled images again with a retention value of 0
        7) Verify that the response code 400
        8) Get scheduled images settings
        9) Verify that the response code is 200
        10) Verify that the original retention value remains intact
        11) List images for the account
        12) Verify that the response code is 200
        13) Verify that the scheduled image snapshot is still present
        """

        tenant_id = self.config.images.tenant_id
        instance_id = self.instance_id
        retention = self.config.images.retention
        alt_retention = '0'
        snapshot_name = datagen.random_string(size=10)
        metadata = {self.config.images.sch_img_metadata_key:
                    self.config.images.sch_img_metadata_value}
        image_names = []
        msg = Constants.MESSAGE

        faux_sch_img_obj = \
            self.images_provider.create_faux_scheduled_image(instance_id,
                                                             snapshot_name,
                                                             metadata)
        self.assertEquals(faux_sch_img_obj.status_code, 202,
                          msg.format('status_code', 202,
                                     faux_sch_img_obj.status_code))

        sch_img_obj = self.images_provider.scheduled_images_client. \
            enable_scheduled_images(tenant_id, instance_id, retention)
        self.assertEquals(sch_img_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     sch_img_obj.status_code))

        sch_img = sch_img_obj.entity

        with self.assertRaises(BadRequest):
            self.images_provider.scheduled_images_client. \
                enable_scheduled_images(tenant_id, instance_id,
                                        alt_retention)

        get_sch_img_settings_obj = \
            self.images_provider.scheduled_images_client. \
            get_scheduled_images_settings(tenant_id, instance_id)
        self.assertEquals(get_sch_img_settings_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     get_sch_img_settings_obj.status_code))

        get_sch_img_settings = get_sch_img_settings_obj.entity
        self.assertEquals(get_sch_img_settings.retention, sch_img.retention,
                          msg.format('retention', sch_img.retention,
                                     get_sch_img_settings.retention))

        list_images = self.images_provider.list_images_pagination()

        for image in list_images:
            image_names.append(image.name)

        self.assertIn(snapshot_name, image_names,
                      msg.format('snapshot_name',
                                 'snapshot to be in listed images',
                                 'snapshot not in listed images'))

    @attr('positive')
    def test_worker_deletes_schedule(self):
        """Verify that a schedule is not deleted for a deleted instance until
        the worker attempts to pick up a job for it.

        1) Create a valid server instance
        2) Enable scheduled images using a valid retention value more than 1
        3) Verify that the response code is 200
        4) List schedules
        5) Verify that the response code is 200
        6) Verify that the schedule exists
        7) Delete the server instance
        8) Verify that the response code is 204
        9) Verify that the schedule is not deleted
        10) Update the next_run of the schedule to a minute from now
        11) After a minute, list schedules
        12) Verify that no scheduled image is created
        13) Verify that the schedule is deleted
        """

        tenant_id = self.config.images.tenant_id
        instance_id = self.instance_id
        retention = self.config.images.alt_retention
        count = 1
        sch_list = []
        marker = None
        server_daily_count = 0
        msg = Constants.MESSAGE

        sch_img_obj = self.images_provider.scheduled_images_client. \
            enable_scheduled_images(tenant_id, instance_id, retention)
        self.assertEquals(sch_img_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     sch_img_obj.status_code))

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

        listed_sch = sch_list[0]

        self.images_provider.delete_active_server(instance_id)

        list_sch = self.images_provider.list_schedules_pagination(keys, values)

        sch_list = []

        for s in list_sch:
            for metadata_key, metadata_value in s.metadata.items():
                if metadata_value == instance_id:
                    sch_list.append(s)
        self.assertEquals(listed_sch, sch_list[0],
                          msg.format("schedule", listed_sch, sch_list[0]))

        tm = datetime.now() - timedelta(seconds=60)
        next_run_time = tm.strftime('%Y-%m-%d %H:%M:%S')

        upd_sch_obj = \
            self.images_provider.schedules_client.update_schedule(
                id=listed_sch.id, next_run=next_run_time)
        self.assertEquals(upd_sch_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     upd_sch_obj.status_code))

        server_daily_list = self.images_provider. \
            get_server_daily_list(instance_id)
        self.assertEquals(len(server_daily_list), server_daily_count,
                          msg.format("length of the list", server_daily_count,
                                     len(server_daily_list)))

        self.images_provider.wait_for_schedule_to_delete(listed_sch.id)

        with self.assertRaises(ItemNotFound):
            self.images_provider.schedules_client.get_schedule(listed_sch.id)
