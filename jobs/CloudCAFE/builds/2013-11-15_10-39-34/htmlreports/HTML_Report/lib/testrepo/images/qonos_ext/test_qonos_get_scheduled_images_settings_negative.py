import uuid

import ccengine.common.tools.datagen as datagen
from ccengine.common.constants.images_constants import Constants
from ccengine.common.decorators import attr
from ccengine.common.exceptions.compute import ItemNotFound, Unauthorized
from testrepo.common.testfixtures.images import BaseImagesFixture


class TestQonosGetScheduledImagesSettingsNegative(BaseImagesFixture):

    @classmethod
    def setUpClass(cls):
        """Creates the server instance used for all tests in this class."""

        super(TestQonosGetScheduledImagesSettingsNegative, cls).setUpClass()

        server_name = datagen.random_string(size=10)

        server_obj = cls.images_provider.create_active_server(server_name)

        cls.instance_id = server_obj.entity.id

    @attr('negative')
    def test_get_sch_img_settings_tenant_server_mismatch(self):
        """Get scheduled images settings for a tenant id/server mismatch.

        1) Create a valid server instance
        2) Enable scheduled images for the instance
        3) Verify that the response code is 200
        4) Get scheduled images settings for and incorrect tenant id
        5) Verify that the response code is 400
        6) Get scheduled images settings for and incorrect instance id
        7) Verify that the response code is 404
        """

        tenant_id = self.config.images.tenant_id
        alt_tenant_id = datagen.random_string(size=32)
        instance_id = self.instance_id
        alt_instance_id = uuid.uuid4()
        retention = self.config.images.retention
        msg = Constants.MESSAGE

        sch_img_obj = self.images_provider.scheduled_images_client. \
            enable_scheduled_images(tenant_id, instance_id, retention)
        self.assertEquals(sch_img_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     sch_img_obj.status_code))

        with self.assertRaises(Unauthorized):
            self.images_provider.scheduled_images_client. \
                get_scheduled_images_settings(alt_tenant_id, instance_id)

        with self.assertRaises(ItemNotFound):
            self.images_provider.scheduled_images_client. \
                get_scheduled_images_settings(tenant_id, alt_instance_id)

    @attr('negative')
    def test_get_scheduled_images_settings_with_blank_tenant_id(self):
        """Get scheduled images settings using blank tenant id.

        1) Create a valid server instance
        2) Get scheduled images settings using a blank tenant id
        3) Verify that the response code is 404
        """

        tenant_id = ""
        instance_id = self.instance_id

        with self.assertRaises(Unauthorized):
            self.images_provider.scheduled_images_client. \
                get_scheduled_images_settings(tenant_id, instance_id)

    @attr('negative')
    def test_get_sch_img_settings_non_existing_tenant_id(self):
        """Get scheduled images settings using non-existing tenant id.

        1) Create a valid server instance
        2) Get scheduled images settings using a non-existing tenant id
        3) Verify that the response code is 404
        """

        tenant_id = datagen.random_string(size=32)
        instance_id = self.instance_id

        '''TODO: Test will fail when bug #198 is fixed'''
        with self.assertRaises(Unauthorized):
            self.images_provider.scheduled_images_client. \
                get_scheduled_images_settings(tenant_id, instance_id)

    @attr('negative')
    def test_get_sch_img_settings_special_characters_tenant_id(self):
        """Get scheduled images settings using special characters for tenant
        id.

        1) Create a valid server instance
        2) Get scheduled images settings using special characters for tenant id
        3) Verify that the response code is 400
        """

        tenant_id = "*"
        instance_id = self.instance_id

        with self.assertRaises(Unauthorized):
            self.images_provider.scheduled_images_client. \
                get_scheduled_images_settings(tenant_id, instance_id)

    @attr('negative')
    def test_get_scheduled_images_settings_with_blank_server_id(self):
        """Get scheduled images settings using blank server id.

        1) Create a valid server instance
        2) Get scheduled images settings using a blank server id
        3) Verify that the response code is 404
        """

        tenant_id = self.config.images.tenant_id
        instance_id = ""

        with self.assertRaises(ItemNotFound):
            self.images_provider.scheduled_images_client. \
                get_scheduled_images_settings(tenant_id, instance_id)

    @attr('negative')
    def test_get_sch_img_settings_non_existing_server_id(self):
        """Get scheduled images settings using non-existing server id.

        1) Create a valid server instance
        2) Get scheduled images using a non-existing server id
        3) Verify that the response code is 404
        """

        tenant_id = self.config.images.tenant_id
        instance_id = uuid.uuid4()

        with self.assertRaises(ItemNotFound):
            self.images_provider.scheduled_images_client. \
                get_scheduled_images_settings(tenant_id, instance_id)

    @attr('negative')
    def test_get_sch_img_settings_special_characters_server_id(self):
        """Get scheduled images settings using special characters for server
        id.

        1) Create a valid server instance
        2) Get scheduled images settings using special characters for server id
        3) Verify that the response code is 404
        """

        tenant_id = self.config.images.tenant_id
        instance_id = "*"

        with self.assertRaises(ItemNotFound):
            self.images_provider.scheduled_images_client. \
                get_scheduled_images_settings(tenant_id, instance_id)
