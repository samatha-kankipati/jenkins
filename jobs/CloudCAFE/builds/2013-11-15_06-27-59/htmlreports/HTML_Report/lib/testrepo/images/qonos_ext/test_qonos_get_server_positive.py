import ccengine.common.tools.datagen as datagen
from ccengine.common.decorators import attr
from ccengine.common.exceptions.compute import ItemNotFound
from ccengine.domain.types import NovaServerStatusTypes
from testrepo.common.testfixtures.images import BaseImagesFixture


class TestQonosGetServerPositive(BaseImagesFixture):

    @classmethod
    def setUpClass(cls):
        """Creates the server instances used for all tests in this class."""

        super(TestQonosGetServerPositive, cls).setUpClass()

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
    def test_after_enable_sch_images_ret_more_than_1_get_server(self):
        """After enabling scheduled images with a retention of more than 1, get
        server.

        1) Create a valid server instance
        2) Enable scheduled images using a valid retention value of more than 1
        3) Verify that the response code is 200
        4) Get server
        5) Verify that the response code is 200
        6) Verify that the response contains the scheduled images settings and
            expected retention value
        """

        tenant_id = self.tenant_id
        instance_id = self.instance_id
        retention = self.retention
        msg = self.msg

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

    @attr('positive')
    def test_after_enable_scheduled_images_disable_get_server(self):
        """After enabling scheduled images for a server and immediately
        disabling it, get server.

        1) Create a valid server instance
        2) Enable scheduled images using a valid retention value
        3) Verify that the response code is 200
        4) Disable scheduled images
        5) Verify that the response code is 202
        6) Get server
        7) Verify that the response code is 200
        8) Verify that the response does not contain the scheduled images
            settings
        """

        tenant_id = self.tenant_id
        instance_id = self.instance_id
        retention = self.retention
        ext_deserializer = self.ext_deserializer
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

        get_server_obj = \
            self.images_provider.servers_client.get_server(instance_id)
        self.assertEquals(get_server_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     get_server_obj.status_code))

        get_server = get_server_obj.entity

        if ext_deserializer == 'json':
            self.assertFalse(hasattr(get_server, 'RAX-SI:image_schedule'),
                             msg.format('RAX-SI:image_schedule',
                                        'to not be present', 'was present'))
        else:
            self.assertFalse(hasattr(get_server, 'image_schedule'),
                             msg.format('RAX-SI:image_schedule',
                                        'to not be present', 'was present'))

    @attr('positive')
    def test_after_enable_sch_images_disable_enable_get_server(self):
        """After enabling scheduled images for a server, disable it and enabled
        it again, get server.

        1) Create a valid server instance
        2) Enable scheduled images using a valid retention value
        3) Verify that the response code is 200
        4) Disable scheduled images
        5) Verify that the response code is 202
        6) Enable scheduled images using a valid retention value
        7) Verify that the response code is 200
        8) Get server
        9) Verify that the response code is 200
        10) Verify that the response contains the scheduled images settings and
            expected retention value
        """

        tenant_id = self.tenant_id
        instance_id = self.instance_id
        retention = self.retention
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

        get_server_obj = \
            self.images_provider.servers_client.get_server(instance_id)
        self.assertEquals(get_server_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     get_server_obj.status_code))

        get_server = get_server_obj.entity

        ret = self.images_provider.get_retention(get_server)

        self.assertEquals(ret, retention,
                          msg.format('RAX-SI:image_schedule', retention, ret))

    @attr('positive')
    def test_after_enable_disable_enable_ret_more_than_1(self):
        """After enabling schedule images for a server with a retention of 1,
        disable it, enable it again with larger retention, get server.

        1) Create a valid server instance
        2) Enable scheduled images using a valid retention value of 1
        3) Verify that the response code is 200
        4) Disable scheduled images
        5) Verify that the response code is 202
        6) Enable scheduled images using a valid retention value greater than 1
        7) Verify that the response code is 200
        8) Get server
        9) Verify that the response code is 200
        10) Verify that the response contains the scheduled images settings and
            expected retention value
        """

        tenant_id = self.tenant_id
        instance_id = self.instance_id
        retention = self.retention
        alt_retention = self.alt_retention
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

        get_server_obj = \
            self.images_provider.servers_client.get_server(instance_id)
        self.assertEquals(get_server_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     get_server_obj.status_code))

        get_server = get_server_obj.entity

        ret = self.images_provider.get_retention(get_server)

        self.assertEquals(ret, alt_retention,
                          msg.format('RAX-SI:image_schedule', alt_retention,
                                     ret))

    @attr('positive')
    def test_after_enable_enabled_sch_images_same_ret_get_server(self):
        """After enabling scheduled images for a server that is already enabled
        with the same retention, get server.

        1) Create a valid server instance
        2) Enable scheduled images using a valid retention value
        3) Verify that the response code is 200
        4) Enable scheduled images using a same retention value
        5) Verify that the response code is 200
        6) Get server
        7) Verify that the response code is 200
        8) Verify that the response contains the scheduled images settings and
            expected retention value
        """

        tenant_id = self.tenant_id
        instance_id = self.instance_id
        retention = self.retention
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

        get_server_obj = \
            self.images_provider.servers_client.get_server(instance_id)
        self.assertEquals(get_server_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     get_server_obj.status_code))

        get_server = get_server_obj.entity

        ret = self.images_provider.get_retention(get_server)

        self.assertEquals(ret, retention,
                          msg.format('RAX-SI:image_schedule', retention, ret))

    @attr('positive')
    def test_after_enable_enabled_sch_images_diff_ret_get_server(self):
        """After enabling scheduled images for a server that is already enabled
        with a different retention, get server.

        1) Create a valid server instance
        2) Enable scheduled images using a valid retention value
        3) Verify that the response code is 200
        4) Enable scheduled images using a different retention value
        5) Verify that the response code is 200
        6) Get server
        7) Verify that the response code is 200
        8) Verify that the response contains the scheduled images settings and
            expected retention value
        """

        tenant_id = self.tenant_id
        instance_id = self.instance_id
        retention = self.retention
        alt_retention = self.alt_retention
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

        get_server_obj = \
            self.images_provider.servers_client.get_server(instance_id)
        self.assertEquals(get_server_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     get_server_obj.status_code))

        get_server = get_server_obj.entity

        ret = self.images_provider.get_retention(get_server)

        self.assertEquals(ret, alt_retention,
                          msg.format('RAX-SI:image_schedule', alt_retention,
                                     ret))

    @attr('positive')
    def test_after_disable_not_enabled_sch_images_get_server(self):
        """After disabling scheduled images for a server that doesn't have
        scheduled images enabled, get server.

        1) Create a valid server instance
        2) Disable scheduled images
        3) Verify that the response code is 404
        4) Get server
        5) Verify that the response code is 200
        6) Verify that the response does not contain scheduled images settings
            or retention value
        """

        tenant_id = self.tenant_id
        instance_id = self.alt_instance_id
        ext_deserializer = self.ext_deserializer
        msg = self.msg

        with self.assertRaises(ItemNotFound):
            self.images_provider.scheduled_images_client. \
                disable_scheduled_images(tenant_id, instance_id)

        get_server_obj = \
            self.images_provider.servers_client.get_server(instance_id)
        self.assertEquals(get_server_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     get_server_obj.status_code))

        get_server = get_server_obj.entity

        if ext_deserializer == 'json':
            self.assertFalse(hasattr(get_server, 'RAX-SI:image_schedule'),
                             msg.format('RAX-SI:image_schedule',
                                        'to not be present', 'was present'))
        else:
            self.assertFalse(hasattr(get_server, 'image_schedule'),
                             msg.format('RAX-SI:image_schedule',
                                        'to not be present', 'was present'))
