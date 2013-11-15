from testrepo.common.testfixtures.images import BaseImagesFixture
from ccengine.common.decorators import attr
import ccengine.common.tools.datagen as datagen
from ccengine.common.exceptions.compute \
    import BadRequest, ItemNotFound, Unauthorized
import uuid
from ccengine.common.constants.images_constants import Constants


class TestQonosEnableScheduledImagesNegative(BaseImagesFixture):

    @classmethod
    def setUpClass(cls):
        '''Creates the server instances and snapshots used for all tests in
        this class'''

        super(TestQonosEnableScheduledImagesNegative, cls).setUpClass()

        server_name = datagen.random_string(size=10)

        server_obj = cls.images_provider.create_active_server(server_name)

        cls.instance_id = server_obj.entity.id

    @attr('negative')
    def test_enable_scheduled_images_for_tenant_server_mismatch(self):
        '''Enable scheduled images for a tenant id/server mismatch'''

        """
        1) Create a valid server instance
        2) Enable scheduled images using an incorrect tenant id
        3) Verify that the response code is 400
        4) Enable scheduled images using an incorrect server
        5) Verify that the response code is 404
        """

        tenant_id = self.config.images.tenant_id
        alt_tenant_id = datagen.random_string(size=32)
        instance_id = self.instance_id
        alt_instance_id = uuid.uuid4()
        retention = self.config.images.retention

        with self.assertRaises(Unauthorized):
            self.images_provider.scheduled_images_client. \
                enable_scheduled_images(alt_tenant_id, instance_id, retention)

        with self.assertRaises(ItemNotFound):
            self.images_provider.scheduled_images_client. \
                enable_scheduled_images(tenant_id, alt_instance_id, retention)

    @attr('negative')
    def test_enable_scheduled_images_request_missing_body(self):
        '''Enable scheduled images request missing body'''

        """
        1) Create a valid server instance
        2) Enable scheduled images using a request missing the body
        3) Verify that the response code is 400
        """

        tenant_id = self.config.images.tenant_id
        instance_id = self.instance_id

        with self.assertRaises(BadRequest):
            self.images_provider.scheduled_images_client. \
                enable_sch_images_missing_body(tenant_id, instance_id)

    @attr('negative')
    def test_enable_scheduled_images_with_blank_tenant_id(self):
        '''Enable scheduled images using blank tenant id'''

        """
        1) Create a valid server instance
        2) Enable scheduled images using a blank tenant id
        3) Verify that the response code is 404
        """

        tenant_id = ""
        instance_id = self.instance_id
        retention = self.config.images.retention

        with self.assertRaises(Unauthorized):
            self.images_provider.scheduled_images_client. \
                enable_scheduled_images(tenant_id, instance_id, retention)

    @attr('negative')
    def test_enable_scheduled_images_with_non_existing_tenant_id(self):
        '''Enable scheduled images using non-existing tenant id'''

        """
        1) Create a valid server instance
        2) Enable scheduled images using a non-existing tenant id
        3) Verify that the response code is 404
        """

        tenant_id = datagen.random_string(size=32)
        instance_id = self.instance_id
        retention = self.config.images.retention

        '''TODO: Test will fail when bug #198 is fixed'''
        with self.assertRaises(Unauthorized):
            self.images_provider.scheduled_images_client. \
                enable_scheduled_images(tenant_id, instance_id, retention)

    @attr('negative')
    def test_enable_sch_img_w_special_characters_for_tenant_id(self):
        '''Enable scheduled images using special characters for tenant id'''

        """
        1) Create a valid server instance
        2) Enable scheduled images using special characters for tenant id
        3) Verify that the response code is 400
        """

        tenant_id = "*"
        instance_id = self.instance_id
        retention = self.config.images.retention

        with self.assertRaises(Unauthorized):
            self.images_provider.scheduled_images_client. \
                enable_scheduled_images(tenant_id, instance_id, retention)

    @attr('negative')
    def test_enable_scheduled_images_with_blank_server_id(self):
        '''Enable scheduled images using blank server id'''

        """
        1) Create a valid server instance
        2) Enable scheduled images using a blank server id
        3) Verify that the response code is 404
        """

        tenant_id = self.config.images.tenant_id
        instance_id = ""
        retention = self.config.images.retention

        with self.assertRaises(ItemNotFound):
            self.images_provider.scheduled_images_client. \
                enable_scheduled_images(tenant_id, instance_id, retention)

    @attr('negative')
    def test_enable_scheduled_images_with_non_existing_server_id(self):
        '''Enable scheduled images using non-existing server id'''

        """
        1) Create a valid server instance
        2) Enable scheduled images using a non-existing server id
        3) Verify that the response code is 404
        """

        tenant_id = self.config.images.tenant_id
        instance_id = uuid.uuid4()
        retention = self.config.images.retention

        with self.assertRaises(ItemNotFound):
            self.images_provider.scheduled_images_client. \
                enable_scheduled_images(tenant_id, instance_id, retention)

    @attr('negative')
    def test_enable_sch_img_w_special_characters_for_server_id(self):
        '''Enable scheduled images using special characters for server id'''

        """
        1) Create a valid server instance
        2) Enable scheduled images using special characters for server id
        3) Verify that the response code is 404
        """

        tenant_id = self.config.images.tenant_id
        instance_id = "*"
        retention = self.config.images.retention

        with self.assertRaises(ItemNotFound):
            self.images_provider.scheduled_images_client. \
                enable_scheduled_images(tenant_id, instance_id, retention)

    @attr('negative')
    def test_enable_scheduled_images_with_blank_retention(self):
        '''Enable scheduled images using a blank retention'''

        """
        1) Create a valid server instance
        2) Enable scheduled images using a blank retention
        3) Verify that the response code is 400
        """

        tenant_id = self.config.images.tenant_id
        instance_id = self.instance_id
        retention = ""

        with self.assertRaises(BadRequest):
            self.images_provider.scheduled_images_client. \
                enable_scheduled_images(tenant_id, instance_id, retention)

    @attr('negative')
    def test_enable_scheduled_images_with_zero_retention(self):
        '''Enable scheduled images using zero retention'''

        """
        1) Create a valid server instance
        2) Enable scheduled images using zero retention
        3) Verify that the response code is 400
        """

        tenant_id = self.config.images.tenant_id
        instance_id = self.instance_id
        retention = 0

        with self.assertRaises(BadRequest):
            self.images_provider.scheduled_images_client. \
                enable_scheduled_images(tenant_id, instance_id, retention)

    @attr('negative')
    def test_enable_scheduled_images_with_negative_retention(self):
        '''Enable scheduled images using a negative retention'''

        """
        1) Create a valid server instance
        2) Enable scheduled images using a negative retention
        3) Verify that the response code is 400
        """

        tenant_id = self.config.images.tenant_id
        instance_id = self.instance_id
        retention = -1

        with self.assertRaises(BadRequest):
            self.images_provider.scheduled_images_client. \
                enable_scheduled_images(tenant_id, instance_id, retention)

    @attr('negative')
    def test_enable_scheduled_images_with_letters_for_retention(self):
        '''Enable scheduled images using letters for retention'''

        """
        1) Create a valid server instance
        2) Enable scheduled images using letters for retention
        3) Verify that the response code is 400
        """

        tenant_id = self.config.images.tenant_id
        instance_id = self.instance_id
        retention = "test"

        with self.assertRaises(BadRequest):
            self.images_provider.scheduled_images_client. \
                enable_scheduled_images(tenant_id, instance_id, retention)

    @attr('negative')
    def test_enable_sch_img_w_special_characters_for_retention(self):
        '''Enable scheduled images using letters for retention'''

        """
        1) Create a valid server instance
        2) Enable scheduled images using special characters for retention
        3) Verify that the response code is 400
        """

        tenant_id = self.config.images.tenant_id
        instance_id = self.instance_id
        retention = "*"

        with self.assertRaises(BadRequest):
            self.images_provider.scheduled_images_client. \
                enable_scheduled_images(tenant_id, instance_id, retention)

    @attr('negative')
    def test_enable_scheduled_images_for_a_deleted_server(self):
        '''Enable scheduled images for a server, delete the server, try
        enabling scheduled images again'''

        """
        1) Create a valid server instance
        2) Enable scheduled images using a valid retention value
        3) Verify that the response code is 200
        4) Delete the server
        5) Verify that the response code is 204
        6) Verify that the schedule is deleted
        7) Attempt to enable scheduled images again
        8) Verify that the response code is 404

        Attributes to verify:
        retention
        """

        tenant_id = self.config.images.tenant_id
        server_name = datagen.random_string(size=10)
        retention = self.config.images.retention
        marker = None
        msg = Constants.MESSAGE

        server_obj = self.images_provider.create_active_server(server_name)
        self.assertEquals(server_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     server_obj.status_code))

        instance_id = server_obj.entity.id

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
                        sch_id = s.id

        self.images_provider.delete_active_server(instance_id)

        with self.assertRaises(ItemNotFound):
            self.images_provider.schedules_client.get_schedule(sch_id)

        with self.assertRaises(ItemNotFound):
            self.images_provider.scheduled_images_client. \
                enable_scheduled_images(tenant_id, instance_id, retention)
