import ccengine.common.tools.datagen as datagen
from ccengine.common.constants.images_constants import Constants
from ccengine.common.decorators import attr
from ccengine.domain.types import NovaServerStatusTypes
from testrepo.common.testfixtures.images import BaseImagesFixture


class TestQonosListServersDetailOSSIFilter(BaseImagesFixture):

    @classmethod
    def setUpClass(cls):
        """Creates the server instances used for all tests in this class."""

        super(TestQonosListServersDetailOSSIFilter, cls).setUpClass()

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
    def test_happy_path_list_servers_detail_with_image_schedule(self):
        """Happy Path - After enabling scheduled images for multiple valid
        servers, list servers detail with image-schedule set to true.

        1) Create 2 valid server instances
        2) Enable scheduled images using a valid retention value for 1 server
        3) Verify that the response code is 200
        4) List servers detail with image-schedule set to true
        5) Verify that the response code is 200
        6) Verify that the response contains the 1 server with image-schedule
        """

        tenant_id = self.config.images.tenant_id
        instance_id = self.instance_id
        retention = int(self.config.images.retention)
        servers = []
        msg = Constants.MESSAGE

        sch_img_obj = self.images_provider.scheduled_images_client. \
            enable_scheduled_images(tenant_id, instance_id, retention)
        self.assertEquals(sch_img_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     sch_img_obj.status_code))

        list_servers_detail_obj = self.images_provider.servers_client.\
            list_servers_with_detail(image_schedule=True)
        self.assertEquals(list_servers_detail_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     list_servers_detail_obj.status_code))

        list_servers_detail = list_servers_detail_obj.entity
        for s in list_servers_detail:
            if (s.id == instance_id):
                servers.append(s)
        self.assertEquals(len(servers), 1, msg.format('servers', 1,
                          len(servers)))

        server = servers[0]
        ret = self.images_provider.get_retention(server)
        self.assertEquals(ret, retention,
                          msg.format('RAX-SI:image_schedule', retention, ret))
