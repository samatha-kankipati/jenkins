import ccengine.common.tools.datagen as datagen
from ccengine.common.constants.images_constants import Constants
from ccengine.common.decorators import attr
from ccengine.common.exceptions.compute import ItemNotFound
from ccengine.domain.types import NovaServerStatusTypes
from testrepo.common.testfixtures.images import BaseImagesFixture


class TestQonosGetScheduledImagesSettings(BaseImagesFixture):

    @classmethod
    def setUpClass(cls):
        """Creates the server instances used for all tests in this class."""

        super(TestQonosGetScheduledImagesSettings, cls).setUpClass()

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

    @attr('smoke')
    def test_happy_path_get_scheduled_images_settings(self):
        """Happy Path - Get scheduled images settings for a valid server that
        has scheduled images enabled.

        1) Create a valid server instance
        2) Enable scheduled images using a valid retention value
        3) Verify that the response code is 200
        4) Get scheduled images settings for the instance
        5) Verify that the response code is 200
        6) Verify that the response contains the entered retention value
        """

        tenant_id = self.config.images.tenant_id
        instance_id = self.instance_id
        retention = self.config.images.retention
        msg = Constants.MESSAGE

        sch_img_obj = self.images_provider.scheduled_images_client. \
            enable_scheduled_images(tenant_id, instance_id, retention)
        self.assertEquals(sch_img_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     sch_img_obj.status_code))

        sch_img = sch_img_obj.entity

        get_sch_img_settings_obj = \
            self.images_provider.scheduled_images_client. \
            get_scheduled_images_settings(tenant_id, instance_id)
        self.assertEquals(get_sch_img_settings_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     get_sch_img_settings_obj.status_code))

        get_sch_img_settings = get_sch_img_settings_obj.entity

        self.assertEquals(get_sch_img_settings.retention,
                          sch_img.retention,
                          msg.format('retention', sch_img.retention,
                                     get_sch_img_settings.retention))

    @attr('positive')
    def test_get_scheduled_images_settings_for_enabled_disabled_instance(self):
        """Get schedule images settings for a valid server that has scheduled
        images enabled and then disabled.

        1) Create a valid server instance
        2) Enable scheduled images using a valid retention value
        3) Verify that the response code is 200
        4) Disable scheduled images for the instance
        5) Verify that the response code is 202
        6) Get scheduled images settings for the instance
        7) Verify that the response code is 404
        """

        tenant_id = self.config.images.tenant_id
        instance_id = self.instance_id
        retention = self.config.images.retention
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

        with self.assertRaises(ItemNotFound):
            self.images_provider.scheduled_images_client. \
                get_scheduled_images_settings(tenant_id, instance_id)

    @attr('positive')
    def test_get_scheduled_images_settings_for_instance_not_enabled(self):
        """Get scheduled images settings for a valid server that has not
        enabled for scheduled images.

        1) Create a valid server instance
        2) Get scheduled images settings for the instance
        3) Verify that the response code is 404
        """

        tenant_id = self.config.images.tenant_id
        instance_id = self.alt_instance_id

        with self.assertRaises(ItemNotFound):
            self.images_provider.scheduled_images_client. \
                get_scheduled_images_settings(tenant_id, instance_id)
