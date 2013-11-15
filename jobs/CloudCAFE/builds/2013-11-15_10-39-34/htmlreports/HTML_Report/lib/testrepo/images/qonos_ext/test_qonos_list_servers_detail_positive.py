import ccengine.common.tools.datagen as datagen
from ccengine.common.decorators import attr
from ccengine.common.exceptions.compute import ItemNotFound
from ccengine.domain.types import NovaServerStatusTypes
from testrepo.common.testfixtures.images import BaseImagesFixture


class TestQonosListServersDetailPositive(BaseImagesFixture):

    @classmethod
    def setUpClass(cls):
        """Creates the server instances used for all tests in this class."""

        super(TestQonosListServersDetailPositive, cls).setUpClass()

        count = 3
        servers = []

        for x in range(count):
            server_name = datagen.random_string(size=10)
            server_obj = cls.images_provider.create_server_no_wait(server_name)
            servers.append(server_obj.entity)

        cls.instance_id = servers[0].id
        cls.alt_instance_id = servers[1].id
        cls.new_instance_id = servers[2].id

        for server in servers:
            cls.images_provider.\
                wait_for_server_status(server.id,
                                       NovaServerStatusTypes.ACTIVE)

    @attr('positive')
    def test_enable_scheduled_images_disable_list_servers_detail(self):
        """After enabling scheduled images for multiple servers and immediately
        disabling it, list servers details.

        1) Create 2 valid server instances
        2) Enable scheduled images using a valid retention value for each
        3) Verify that the response code is 200
        4) Disable scheduled images for each
        5) Verify that the response code is 202
        6) List servers detail
        7) Verify that the response code is 200
        8) Verify that the response does not contain the scheduled images
            settings for both server instances
        """

        tenant_id = self.tenant_id
        instance_id = self.instance_id
        alt_instance_id = self.alt_instance_id
        retention = self.retention
        servers = []
        ext_deserializer = self.ext_deserializer
        msg = self.msg

        sch_img_obj = self.images_provider.scheduled_images_client. \
            enable_scheduled_images(tenant_id, instance_id, retention)
        self.assertEquals(sch_img_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     sch_img_obj.status_code))

        sch_img_obj = self.images_provider.scheduled_images_client. \
            enable_scheduled_images(tenant_id, alt_instance_id, retention)
        self.assertEquals(sch_img_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     sch_img_obj.status_code))

        dis_sch_img_obj = self.images_provider.scheduled_images_client. \
            disable_scheduled_images(tenant_id, instance_id)
        self.assertEquals(dis_sch_img_obj.status_code, 202,
                          msg.format('status_code', 202,
                                     dis_sch_img_obj.status_code))

        dis_sch_img_obj = self.images_provider.scheduled_images_client. \
            disable_scheduled_images(tenant_id, alt_instance_id)
        self.assertEquals(dis_sch_img_obj.status_code, 202,
                          msg.format('status_code', 202,
                                     dis_sch_img_obj.status_code))

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
            if ext_deserializer == 'json':
                self.assertFalse(hasattr(server, 'RAX-SI:image_schedule'),
                                 msg.format('RAX-SI:image_schedule',
                                            'to not be present',
                                            'was present'))
            else:
                self.assertFalse(hasattr(server, 'image_schedule'),
                                 msg.format('RAX-SI:image_schedule',
                                            'to not be present',
                                            'was present'))

    @attr('positive')
    def test_disable_enabled_sch_images_enable_list_servers(self):
        """After enabling scheduled images with a retention of more than 1,
        list servers detail.

        1) Create valid server instance
        2) Enable scheduled images using a valid retention value
        3) Verify that the response code is 200
        4) Disable scheduled images
        5) Verify that the response code is 202
        6) Enable scheduled images using a valid retention value
        7) Verify that the response code is 200
        8) List servers detail
        9) Verify that the response code is 200
        10) Verify that the response contains the scheduled images settings and
            expected retention value
        """

        tenant_id = self.tenant_id
        instance_id = self.instance_id
        retention = self.retention
        servers = []
        msg = self.msg

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

        list_servers_obj = \
            self.images_provider.servers_client.list_servers_with_detail()
        self.assertEquals(list_servers_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     list_servers_obj.status_code))

        list_servers = list_servers_obj.entity

        for server in list_servers:
            if (server.id == instance_id):
                servers.append(server)

        for server in servers:
            if (server.id == instance_id):
                ret = self.images_provider.get_retention(server)
                self.assertEquals(ret, retention,
                                  msg.format('RAX-SI:image_schedule',
                                             retention, ret))
            else:
                self.fail('Unexpected server id in list')

    @attr('positive')
    def test_disable_enabled_sch_img_enable_w_diff_ret_lst_srvrs(self):
        """After enabling scheduled images for a server, disable it and enabled
        it again, list servers detail.

        1) Create valid server instance
        2) Enable scheduled images using a valid retention value
        3) Verify that the response code is 200
        4) Disable scheduled images
        5) Verify that the response code is 202
        6) Enable scheduled images using a different valid retention value
        7) Verify that the response code is 200
        8) List servers detail
        9) Verify that the response code is 200
        10) Verify that the response contains the scheduled images settings and
            expected retention value
        """

        tenant_id = self.tenant_id
        instance_id = self.instance_id
        retention = self.retention
        alt_retention = self.alt_retention
        servers = []
        msg = self.msg

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

        list_servers_obj = \
            self.images_provider.servers_client.list_servers_with_detail()
        self.assertEquals(list_servers_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     list_servers_obj.status_code))

        list_servers = list_servers_obj.entity

        for server in list_servers:
            if (server.id == instance_id):
                servers.append(server)

        for server in servers:
            if (server.id == instance_id):
                ret = self.images_provider.get_retention(server)
                self.assertEquals(ret, alt_retention,
                                  msg.format('RAX-SI:image_schedule',
                                             alt_retention, ret))
            else:
                self.fail('Unexpected server id in list')

    @attr('positive')
    def test_enable_enabled_sch_img_with_same_ret_list_servers(self):
        """After enabling scheduled images for a server that is already enabled
        with the same retention, list servers detail.

        1) Create valid server instance
        2) Enable scheduled images using a valid retention value
        3) Verify that the response code is 200
        4) Enable scheduled images using the same valid retention value
        5) Verify that the response code is 200
        6) List servers detail
        7) Verify that the response code is 200
        8) Verify that the response contains the scheduled images settings and
            expected retention value
        """

        tenant_id = self.tenant_id
        instance_id = self.instance_id
        retention = self.retention
        servers = []
        msg = self.msg

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

        list_servers_obj = \
            self.images_provider.servers_client.list_servers_with_detail()
        self.assertEquals(list_servers_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     list_servers_obj.status_code))

        list_servers = list_servers_obj.entity

        for server in list_servers:
            if (server.id == instance_id):
                servers.append(server)

        for server in servers:
            if (server.id == instance_id):
                ret = self.images_provider.get_retention(server)
                self.assertEquals(ret, retention,
                                  msg.format('RAX-SI:image_schedule',
                                             retention, ret))
            else:
                self.fail('Unexpected server id in list')

    @attr('positive')
    def test_enable_enabled_sch_img_with_diff_ret_list_servers(self):
        """After enabling scheduled images for a server that is already enabled
        with a different retention, list servers detail.

        1) Create valid server instance
        2) Enable scheduled images using a valid retention value
        3) Verify that the response code is 200
        4) Enable scheduled images using a different valid retention value
        5) Verify that the response code is 200
        6) List servers detail
        7) Verify that the response code is 200
        8) Verify that the response contains the scheduled images settings and
            expected retention value
        """

        tenant_id = self.tenant_id
        instance_id = self.instance_id
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
            enable_scheduled_images(tenant_id, instance_id, alt_retention)
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
            if (server.id == instance_id):
                servers.append(server)

        for server in servers:
            if (server.id == instance_id):
                ret = self.images_provider.get_retention(server)
                self.assertEquals(ret, alt_retention,
                                  msg.format('RAX-SI:image_schedule',
                                             alt_retention, ret))
            else:
                self.fail('Unexpected server id in list')

    @attr('positive')
    def test_disable_not_enabled_sch_img_list_servers(self):
        """After disabling scheduled images for a server that doesn't have
        scheduled images enabled, list servers detail.

        1) Create valid server instance
        2) Enable scheduled images using a valid retention value
        3) Verify that the response code is 200
        4) Enable scheduled images using a different valid retention value
        5) Verify that the response code is 200
        6) List servers detail
        7) Verify that the response code is 200
        8) Verify that the response contains the scheduled images settings and
            expected retention value
        """

        tenant_id = self.tenant_id
        instance_id = self.new_instance_id
        servers = []
        ext_deserializer = self.ext_deserializer
        msg = self.msg

        with self.assertRaises(ItemNotFound):
            self.images_provider.scheduled_images_client. \
                disable_scheduled_images(tenant_id, instance_id)

        list_servers_obj = \
            self.images_provider.servers_client.list_servers_with_detail()
        self.assertEquals(list_servers_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     list_servers_obj.status_code))

        list_servers = list_servers_obj.entity

        for server in list_servers:
            if (server.id == instance_id):
                servers.append(server)

        for server in servers:
            if (server.id == instance_id):
                if ext_deserializer == 'json':
                    self.assertFalse(hasattr(server, 'RAX-SI:image_schedule'),
                                     msg.format('RAX-SI:image_schedule',
                                                'to not be present',
                                                'was present'))
                else:
                    self.assertFalse(hasattr(server, 'image_schedule'),
                                     msg.format('RAX-SI:image_schedule',
                                                'to not be present',
                                                'was present'))
            else:
                self.fail('Unexpected server id in list')
