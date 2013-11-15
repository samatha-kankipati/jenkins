from testrepo.common.testfixtures.images import BaseImagesFixture
from ccengine.common.decorators import attr
import ccengine.common.tools.datagen as datagen
from ccengine.common.exceptions.compute \
    import ItemNotFound, Unauthorized, ServiceUnavailable
import uuid
from ccengine.common.constants.images_constants import Constants


class TestQonosDisableScheduledImagesNegative(BaseImagesFixture):

    @classmethod
    def setUpClass(cls):
        '''Creates the server instances and snapshots used for all tests in
        this class'''

        super(TestQonosDisableScheduledImagesNegative, cls).setUpClass()

        server_name = datagen.random_string(size=10)

        server_obj = cls.images_provider.create_active_server(server_name)

        cls.instance_id = server_obj.entity.id

    @attr('negative')
    def test_disable_scheduled_images_for_tenant_server_mismatch(self):
        '''Disable scheduled images for a tenant id/server mismatch'''

        """
        1) Create a valid server instance
        2) Enable scheduled images for the instance
        3) Disable scheduled images using an incorrect tenant id
        4) Verify that the response code is 400
        5) Disable scheduled images using an incorrect server
        6) Verify that the response code is 404
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
                disable_scheduled_images(alt_tenant_id, instance_id)

        with self.assertRaises(ItemNotFound):
            self.images_provider.scheduled_images_client. \
                disable_scheduled_images(tenant_id, alt_instance_id)

    @attr('negative')
    def test_disable_scheduled_images_request_including_body(self):
        '''Disable scheduled images request including body'''

        """
        1) Create a valid server instance
        2) Enable scheduled images for the instance
        3) Disable scheduled images using a request including a body
        2) Verify that the response code is 400
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

        '''TODO: Test will fail with bug #199 is fixed'''
        with self.assertRaises(ServiceUnavailable):
            self.images_provider.scheduled_images_client. \
                disable_sch_images_including_body(tenant_id, instance_id,
                                                  retention)

    @attr('negative')
    def test_disable_scheduled_images_with_blank_tenant_id(self):
        '''Disable scheduled images using blank tenant id'''

        """
        1) Create a valid server instance
        2) Enable scheduled images
        3) Disable scheduled images using a blank tenant id
        4) Verify that the response code is 404
        """

        tenant_id = self.config.images.tenant_id
        alt_tenant_id = ""
        instance_id = self.instance_id
        retention = self.config.images.retention
        msg = Constants.MESSAGE

        sch_img_obj = self.images_provider.scheduled_images_client. \
            enable_scheduled_images(tenant_id, instance_id, retention)
        self.assertEquals(sch_img_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     sch_img_obj.status_code))

        with self.assertRaises(Unauthorized):
            self.images_provider.scheduled_images_client. \
                disable_scheduled_images(alt_tenant_id, instance_id)

    @attr('negative')
    def test_disable_scheduled_images_with_non_existing_tenant_id(self):
        '''Disable scheduled images using non-existing tenant id'''

        """
        1) Create a valid server instance
        2) Enable scheduled images
        3) Disable scheduled images using a non-existing tenant id
        4) Verify that the response code is 401
        """

        tenant_id = self.config.images.tenant_id
        alt_tenant_id = datagen.random_string(size=32)
        instance_id = self.instance_id
        retention = self.config.images.retention
        msg = Constants.MESSAGE

        sch_img_obj = self.images_provider.scheduled_images_client. \
            enable_scheduled_images(tenant_id, instance_id, retention)
        self.assertEquals(sch_img_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     sch_img_obj.status_code))

        '''TODO: Test will fail when bug #198 is fixed'''
        with self.assertRaises(Unauthorized):
            self.images_provider.scheduled_images_client. \
                disable_scheduled_images(alt_tenant_id, instance_id)

    @attr('negative')
    def test_disable_sch_img_w_special_characters_for_tenant_id(self):
        '''Disable scheduled images using special characters for tenant id'''

        """
        1) Create a valid server instance
        2) Enable scheduled images
        3) Disable scheduled images using special characters for tenant id
        4) Verify that the response code is 400
        """

        tenant_id = self.config.images.tenant_id
        alt_tenant_id = "*"
        instance_id = self.instance_id
        retention = self.config.images.retention
        msg = Constants.MESSAGE

        sch_img_obj = self.images_provider.scheduled_images_client. \
            enable_scheduled_images(tenant_id, instance_id, retention)
        self.assertEquals(sch_img_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     sch_img_obj.status_code))

        with self.assertRaises(Unauthorized):
            self.images_provider.scheduled_images_client. \
                disable_scheduled_images(alt_tenant_id, instance_id)

    @attr('negative')
    def test_disable_scheduled_images_with_blank_server_id(self):
        '''Disable scheduled images using blank server id'''

        """
        1) Create a valid server instance
        2) Enable scheduled images
        3) Disable scheduled images using a blank server id
        4) Verify that the response code is 404
        """

        tenant_id = self.config.images.tenant_id
        instance_id = self.instance_id
        alt_instance_id = ""
        retention = self.config.images.retention
        msg = Constants.MESSAGE

        sch_img_obj = self.images_provider.scheduled_images_client. \
            enable_scheduled_images(tenant_id, instance_id, retention)
        self.assertEquals(sch_img_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     sch_img_obj.status_code))

        with self.assertRaises(ItemNotFound):
            self.images_provider.scheduled_images_client. \
                disable_scheduled_images(tenant_id, alt_instance_id)

    @attr('negative')
    def test_disable_scheduled_images_with_non_existing_server_id(self):
        '''Disable scheduled images using non-existing server id'''

        """
        1) Create a valid server instance
        2) Enable scheduled images
        3) Disable scheduled images using a non-existing server id
        4) Verify that the response code is 404
        """

        tenant_id = self.config.images.tenant_id
        instance_id = self.instance_id
        alt_instance_id = uuid.uuid4()
        retention = self.config.images.retention
        msg = Constants.MESSAGE

        sch_img_obj = self.images_provider.scheduled_images_client. \
            enable_scheduled_images(tenant_id, instance_id, retention)
        self.assertEquals(sch_img_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     sch_img_obj.status_code))

        with self.assertRaises(ItemNotFound):
            self.images_provider.scheduled_images_client. \
                disable_scheduled_images(tenant_id, alt_instance_id)

    @attr('negative')
    def test_disable_sch_img_w_special_characters_for_server_id(self):
        '''Disable scheduled images using special characters for server id'''

        """
        1) Create a valid server instance
        2) Enable scheduled images using
        3) Disable scheduled images special characters for server id
        4) Verify that the response code is 404
        """

        tenant_id = self.config.images.tenant_id
        instance_id = self.instance_id
        alt_instance_id = "*"
        retention = self.config.images.retention
        msg = Constants.MESSAGE

        sch_img_obj = self.images_provider.scheduled_images_client. \
            enable_scheduled_images(tenant_id, instance_id, retention)
        self.assertEquals(sch_img_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     sch_img_obj.status_code))

        with self.assertRaises(ItemNotFound):
            self.images_provider.scheduled_images_client. \
                disable_scheduled_images(tenant_id, alt_instance_id)
