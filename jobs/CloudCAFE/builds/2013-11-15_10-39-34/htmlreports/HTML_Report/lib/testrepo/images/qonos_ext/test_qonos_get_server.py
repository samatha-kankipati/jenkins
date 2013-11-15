import ccengine.common.tools.datagen as datagen
from ccengine.common.constants.images_constants import Constants
from ccengine.common.decorators import attr
from testrepo.common.testfixtures.images import BaseImagesFixture


class TestQonosGetServer(BaseImagesFixture):

    @classmethod
    def setUpClass(cls):
        """Creates the server instance used for all tests in this class."""

        super(TestQonosGetServer, cls).setUpClass()

        server_name = datagen.random_string(size=10)

        server_obj = cls.images_provider.create_active_server(server_name)

        cls.instance_id = server_obj.entity.id

    @attr('smoke')
    def test_happy_path_after_enable_scheduled_images_get_server(self):
        """Happy Path - After enabling scheduled images for a valid server, get
        server.

        1) Create a valid server instance
        2) Enable scheduled images using a valid retention value
        3) Verify that the response code is 200
        4) Get server
        5) Verify that the response code is 200
        6) Verify that the response contains the scheduled images settings and
            expected retention value
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

        get_server_obj = \
            self.images_provider.servers_client.get_server(instance_id)
        self.assertEquals(get_server_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     get_server_obj.status_code))

        get_server = get_server_obj.entity

        ret = self.images_provider.get_retention(get_server)

        self.assertEquals(ret, retention,
                          msg.format('RAX-SI:image_schedule', retention, ret))
