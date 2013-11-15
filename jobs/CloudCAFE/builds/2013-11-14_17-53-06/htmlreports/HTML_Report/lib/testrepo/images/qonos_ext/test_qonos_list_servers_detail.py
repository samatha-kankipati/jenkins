import ccengine.common.tools.datagen as datagen
from ccengine.common.decorators import attr
from ccengine.domain.types import NovaServerStatusTypes
from testrepo.common.testfixtures.images import BaseImagesFixture


class TestQonosListServersDetail(BaseImagesFixture):

    @classmethod
    def setUpClass(cls):
        """Creates the server instances used for all tests in this class."""

        super(TestQonosListServersDetail, cls).setUpClass()

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
    def test_happy_path_enable_multiple_sch_images_list_servers(self):
        """Happy Path - After enabling scheduled images for multiple valid
        servers, list servers detail.

        1) Create 2 valid server instances
        2) Enable scheduled images using a valid retention value for each -
            values of 1 and 3
        3) Verify that the response code is 200
        4) List servers detail
        5) Verify that the response code is 200
        6) Verify that the response contains the scheduled images settings and
            expected retention value for both servers
        """

        tenant_id = self.tenant_id
        instance_id = self.instance_id
        alt_instance_id = self.alt_instance_id
        retention = self.retention
        alt_retention = self.alt_retention
        servers = []
        msg = self.msg

        sch_img_obj = self.images_provider.scheduled_images_client. \
            enable_scheduled_images(tenant_id, instance_id, retention)
        self.assertEquals(sch_img_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     sch_img_obj.status_code))

        sch_img_obj = self.images_provider.scheduled_images_client. \
            enable_scheduled_images(tenant_id, alt_instance_id, alt_retention)
        self.assertEquals(sch_img_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     sch_img_obj.status_code))

        list_servers_obj = \
            self.images_provider.servers_client.list_servers_with_detail()
        self.assertEquals(list_servers_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     list_servers_obj.status_code))

        list_servers = list_servers_obj.entity

        for server in list_servers:
            if (server.id == instance_id or server.id == alt_instance_id):
                servers.append(server)

        for server in servers:
            ret = self.images_provider.get_retention(server)
            if (server.id == instance_id):
                self.assertEquals(ret, retention,
                                  msg.format('RAX-SI:image_schedule',
                                             retention, ret))
            elif (server.id == alt_instance_id):
                self.assertEquals(ret, alt_retention,
                                  msg.format('RAX-SI:image_schedule',
                                             alt_retention,
                                             ret))
            else:
                self.fail('Unexpected server id in list')
