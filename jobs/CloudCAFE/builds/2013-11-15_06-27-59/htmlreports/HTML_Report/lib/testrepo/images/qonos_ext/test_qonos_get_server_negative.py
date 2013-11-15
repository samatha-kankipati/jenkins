import uuid

import ccengine.common.tools.datagen as datagen
from ccengine.common.constants.images_constants import Constants
from ccengine.common.decorators import attr
from ccengine.common.exceptions.compute import ItemNotFound
from testrepo.common.testfixtures.images import BaseImagesFixture


class TestQonosGetServerNegative(BaseImagesFixture):

    @classmethod
    def setUpClass(cls):
        """Creates the server instance used for all tests in this class."""

        super(TestQonosGetServerNegative, cls).setUpClass()

        server_name = datagen.random_string(size=10)

        server_obj = cls.images_provider.create_active_server(server_name)

        cls.instance_id = server_obj.entity.id

    @attr('negative')
    def test_get_server_request_including_body(self):
        """Get server request including body.

        1) Create a valid server instance
        2) Enable scheduled images using a valid retention value
        3) Verify that the response code is 200
        4) Get server using a request with a body
        5) Verify that the response code is 400
        """

        tenant_id = self.config.images.tenant_id
        instance_id = self.instance_id
        retention = int(self.config.images.retention)
        msg = Constants.MESSAGE

        sch_img_obj = self.images_provider.scheduled_images_client. \
            enable_scheduled_images(tenant_id, instance_id, retention)
        self.assertEquals(sch_img_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     sch_img_obj.status_code))

        '''TODO: Test will fail when bug lp #1160982 is fixed'''
        get_server_obj = self.images_provider.servers_client. \
            get_server_including_body(instance_id)
        self.assertEquals(get_server_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     get_server_obj.status_code))

    @attr('negative')
    def test_get_server_with_blank_server_id(self):
        """Get server with blank server id.

        1) Get server with a blank server id
        2) Verify that the response code is 404
        """

        instance_id = ""

        with self.assertRaises(ItemNotFound):
            self.images_provider.servers_client.get_server(instance_id)

    @attr('negative')
    def test_get_server_with_non_existing_server_id(self):
        """Get server with non-existing server id.

        1) Get server with a non-existing server id
        2) Verify that the response code is 404
        """

        instance_id = uuid.uuid4()

        with self.assertRaises(ItemNotFound):
            self.images_provider.servers_client.get_server(instance_id)

    @attr('negative')
    def test_get_server_with_special_characters_for_server_id(self):
        """Get server with special characters for server id.

        1) Get server with special characters for server id
        2) Verify that the response code is 404
        """

        instance_id = "*"

        with self.assertRaises(ItemNotFound):
            self.images_provider.servers_client.get_server(instance_id)
