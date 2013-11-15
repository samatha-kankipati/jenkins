from testrepo.common.testfixtures.images import BaseImagesFixture
from ccengine.common.decorators import attr
import ccengine.common.tools.datagen as datagen
from ccengine.domain.types import NovaServerStatusTypes


class TestQonosListServersOSSIFilterPositive(BaseImagesFixture):

    @classmethod
    def setUpClass(cls):
        '''Creates the server instances used for all tests in this class'''

        super(TestQonosListServersOSSIFilterPositive, cls).setUpClass()

        count = 3
        servers = []

        for x in range(count):
            server_name = datagen.random_string(size=10)
            server_obj = cls.images_provider.create_server_no_wait(server_name)
            servers.append(server_obj.entity)

        cls.instance_id = servers[0].id
        cls.alt_instance_id = servers[1].id
        cls.multi_ret_instance_id = servers[2].id
        for server in servers:
            cls.images_provider.\
                wait_for_server_status(server.id,
                                       NovaServerStatusTypes.ACTIVE)

        cls.images_provider.scheduled_images_client. \
            enable_scheduled_images(cls.tenant_id, cls.instance_id,
                                    cls.retention)

        cls.images_provider.scheduled_images_client. \
            enable_scheduled_images(cls.tenant_id, cls.multi_ret_instance_id,
                                    cls.alt_retention)

    @attr('positive')
    def test_list_servers_with_image_schedule(self):
        """List servers with image-schedule set to true

        1) Create required valid server instance as part of setup class
        2) List servers with image-schedule set to true
        3) Verify that the response code is 200
        4) Verify that the response contain only the server enabled with SI

        Attributes to verify:
        scheduled images settings
        """

        instance_id = self.instance_id
        alt_instance_id = self.alt_instance_id
        multi_ret_instance_id = self.multi_ret_instance_id
        enabled_servers = []
        servers = []

        list_servers_obj = self.images_provider.servers_client.\
            list_servers(image_schedule=True)
        self.assertEquals(list_servers_obj.status_code, 200,
                          self.msg.format('status_code', 200,
                                     list_servers_obj.status_code))

        list_servers = list_servers_obj.entity
        for s in list_servers:
            if (s.id == alt_instance_id):
                servers.append(s)
            if (s.id == instance_id or s.id == multi_ret_instance_id):
                enabled_servers.append(s)

        self.assertEquals(len(enabled_servers), 2,
                          self.msg.format('Enabled servers', 2,
                                          len(enabled_servers)))
        self.assertEquals(len(servers), 0,
                          self.msg.format('Disabled servers', 0,
                          len(servers)))

    @attr('positive')
    def test_list_servers_with_image_schedule_false(self):
        """List servers with image-schedule set to false

        1) Create required valid server instance as part of setup class
        2) List servers with image-schedule set to false
        3) Verify that the response code is 200
        4) Verify that the response contain only the server not enabled with SI

        Attributes to verify:
        scheduled images settings
        """

        instance_id = self.instance_id
        alt_instance_id = self.alt_instance_id
        multi_ret_instance_id = self.multi_ret_instance_id
        disabled_servers = []
        servers = []

        list_servers_obj = self.images_provider.servers_client.\
            list_servers(image_schedule=False)
        self.assertEquals(list_servers_obj.status_code, 200,
                          self.msg.format('status_code', 200,
                                     list_servers_obj.status_code))

        list_servers = list_servers_obj.entity
        for s in list_servers:
            if (s.id == alt_instance_id):
                disabled_servers.append(s)
            if (s.id == instance_id or s.id == multi_ret_instance_id):
                servers.append(s)

        self.assertEquals(len(disabled_servers), 1,
                          self.msg.format('Disabled servers', 1,
                                          len(disabled_servers)))
        self.assertEquals(len(servers), 0,
                          self.msg.format('Enabled servers', 0,
                          len(servers)))

    @attr('positive')
    def test_enable_enable_sch_images_list_servers(self):
        """After enabling scheduled images for a server that is already
        enabled with same retention, list servers with image-schedule
        set to true

        1) Create required valid server instance as part of setup class
        2) Enable scheduled images using a valid retention value for 1 server
        3) Verify that the response code is 200
        4) List servers with image-schedule set to true
        5) Verify that the response code is 200
        6) Verify that the response contains enabled server with image-schedule

        Attributes to verify:
        server id
        scheduled images settings
        retention
        """

        tenant_id = self.tenant_id
        instance_id = self.instance_id
        retention = self.retention
        alt_instance_id = self.alt_instance_id
        multi_ret_instance_id = self.multi_ret_instance_id
        enabled_servers = []
        servers = []

        sch_img_obj = self.images_provider.scheduled_images_client. \
            enable_scheduled_images(tenant_id, instance_id, retention)
        self.assertEquals(sch_img_obj.status_code, 200,
                          self.msg.format('status_code', 200,
                                     sch_img_obj.status_code))

        list_servers_obj = self.images_provider.servers_client.\
            list_servers(image_schedule=True)
        self.assertEquals(list_servers_obj.status_code, 200,
                          self.msg.format('status_code', 200,
                                     list_servers_obj.status_code))

        list_servers = list_servers_obj.entity
        for s in list_servers:
            if (s.id == alt_instance_id):
                servers.append(s)
            if (s.id == instance_id):
                enabled_servers.append(s)
                server = s
            if (s.id == multi_ret_instance_id):
                enabled_servers.append(s)

        self.assertEquals(len(enabled_servers), 2,
                          self.msg.format('Enabled servers', 2,
                                          len(enabled_servers)))
        self.assertEquals(len(servers), 0,
                          self.msg.format('Disabled servers', 0,
                          len(servers)))

        self.assertFalse(hasattr(server, 'RAX-SI:image_schedule'),
                         self.msg.format('RAX-SI:image_schedule',
                                         'to not be present', 'was present'))

    @attr('positive')
    def test_enable_enable_different_retention_sch_images_list_servers(self):
        """After enabling scheduled images for a server that is already
        enabled with different retention, list servers with image-schedule
        set to true

        1) Create required valid server instance as part of setup class
        2) Enable scheduled images using different retention value for 1 server
        3) Verify that the response code is 200
        4) List servers with image-schedule set to true
        5) Verify that the response code is 200
        6) Verify that the response contains enabled server with image-schedule

        Attributes to verify:
        server id
        scheduled images settings
        retention
        """
        tenant_id = self.tenant_id
        instance_id = self.instance_id
        alt_retention = self.alt_retention
        alt_instance_id = self.alt_instance_id
        multi_ret_instance_id = self.multi_ret_instance_id
        enabled_servers = []
        servers = []

        sch_img_obj = self.images_provider.scheduled_images_client. \
            enable_scheduled_images(tenant_id, instance_id, alt_retention)
        self.assertEquals(sch_img_obj.status_code, 200,
                          self.msg.format('status_code', 200,
                                     sch_img_obj.status_code))

        list_servers_obj = self.images_provider.servers_client.\
            list_servers(image_schedule=True)
        self.assertEquals(list_servers_obj.status_code, 200,
                          self.msg.format('status_code', 200,
                                     list_servers_obj.status_code))

        list_servers = list_servers_obj.entity
        for s in list_servers:
            if (s.id == alt_instance_id):
                servers.append(s)
            if (s.id == instance_id):
                enabled_servers.append(s)
                server = s
            if (s.id == multi_ret_instance_id):
                enabled_servers.append(s)

        self.assertEquals(len(enabled_servers), 2,
                          self.msg.format('Enabled servers', 2,
                                          len(enabled_servers)))
        self.assertEquals(len(servers), 0,
                          self.msg.format('Disabled servers', 0,
                          len(servers)))

        self.assertFalse(hasattr(server, 'RAX-SI:image_schedule'),
                         self.msg.format('RAX-SI:image_schedule',
                                         'to not be present', 'was present'))

    @attr('positive')
    def test_enable_disabled_scheduled_images_w_larger_ret_list_server(self):
        """After enabling schedule images for a server with a retention of 1,
        disable it, enable it again with larger retention, list servers with
        image-schedule set to true

        1) Create required valid server instance as part of setup class
        2) Disable scheduled images
        3) List servers with image-schedule set to true
        4) Verify that the response code is 200
        5) Verify that the response doesn't have disabled server
        3) Enable scheduled images using larger retention value for 1 server
        4) Verify that the response code is 200
        5) List servers with image-schedule set to true
        6) Verify that the response code is 200
        7) Verify that the response contains enabled server with image-schedule

        Attributes to verify:
        server id
        scheduled images settings
        retention
        """
        tenant_id = self.tenant_id
        instance_id = self.instance_id
        alt_retention = self.alt_retention
        alt_instance_id = self.alt_instance_id
        multi_ret_instance_id = self.multi_ret_instance_id
        enabled_servers = []
        servers = []

        dis_sch_img_obj = self.images_provider.scheduled_images_client. \
            disable_scheduled_images(tenant_id, instance_id)
        self.assertEquals(dis_sch_img_obj.status_code, 202,
                          self.msg.format('status_code', 202,
                                     dis_sch_img_obj.status_code))

        list_servers_obj = self.images_provider.servers_client.\
            list_servers(image_schedule=True)
        self.assertEquals(list_servers_obj.status_code, 200,
                          self.msg.format('status_code', 200,
                                     list_servers_obj.status_code))

        list_servers = list_servers_obj.entity
        for s in list_servers:
            if (s.id == instance_id or s.id == alt_instance_id):
                servers.append(s)
            if (s.id == multi_ret_instance_id):
                enabled_servers.append(s)

        self.assertEquals(len(enabled_servers), 1,
                          self.msg.format('Enabled servers', 1,
                                          len(enabled_servers)))
        self.assertEquals(len(servers), 0,
                          self.msg.format('Disabled servers', 0,
                          len(servers)))

        sch_img_obj = self.images_provider.scheduled_images_client. \
            enable_scheduled_images(tenant_id, instance_id, alt_retention)
        self.assertEquals(sch_img_obj.status_code, 200,
                          self.msg.format('status_code', 200,
                                     sch_img_obj.status_code))

        list_servers_obj = self.images_provider.servers_client.\
            list_servers(image_schedule=True)
        self.assertEquals(list_servers_obj.status_code, 200,
                          self.msg.format('status_code', 200,
                                     list_servers_obj.status_code))

        list_servers = list_servers_obj.entity
        enabled_servers = []
        for s in list_servers:
            if (s.id == alt_instance_id):
                servers.append(s)
            if (s.id == instance_id):
                enabled_servers.append(s)
                server = s
            if (s.id == multi_ret_instance_id):
                enabled_servers.append(s)

        self.assertEquals(len(enabled_servers), 2,
                          self.msg.format('Enabled servers', 2,
                                          len(enabled_servers)))
        self.assertEquals(len(servers), 0,
                          self.msg.format('Disabled servers', 0,
                          len(servers)))

        self.assertFalse(hasattr(server, 'RAX-SI:image_schedule'),
                         self.msg.format('RAX-SI:image_schedule',
                                         'to not be present', 'was present'))

    @attr('positive')
    def test_enable_disable_enable_sch_images_list_servers(self):
        """After enabling scheduled images for a server, disable it and
        enable it again, list servers with image-schedule set to true

        1) Create required valid server instance as part of setup class
        2) Disable scheduled images
        3) List servers with image-schedule set to true
        4) Verify that the response code is 200
        5) Verify that the response doesn't have disabled server
        3) Enable scheduled images using valid retention value for 1 server
        4) Verify that the response code is 200
        5) List servers with image-schedule set to true
        6) Verify that the response code is 200
        7) Verify that the response contains enabled server with image-schedule

        Attributes to verify:
        server id
        scheduled images settings
        retention
        """
        tenant_id = self.tenant_id
        instance_id = self.instance_id
        retention = self.retention
        alt_instance_id = self.alt_instance_id
        multi_ret_instance_id = self.multi_ret_instance_id
        enabled_servers = []
        servers = []

        dis_sch_img_obj = self.images_provider.scheduled_images_client. \
            disable_scheduled_images(tenant_id, instance_id)
        self.assertEquals(dis_sch_img_obj.status_code, 202,
                          self.msg.format('status_code', 202,
                                     dis_sch_img_obj.status_code))

        list_servers_obj = self.images_provider.servers_client.\
            list_servers(image_schedule=True)
        self.assertEquals(list_servers_obj.status_code, 200,
                          self.msg.format('status_code', 200,
                                     list_servers_obj.status_code))

        list_servers = list_servers_obj.entity
        for s in list_servers:
            if (s.id == instance_id or s.id == alt_instance_id):
                servers.append(s)
            if (s.id == multi_ret_instance_id):
                enabled_servers.append(s)

        self.assertEquals(len(enabled_servers), 1,
                          self.msg.format('Enabled servers', 1,
                                          len(enabled_servers)))
        self.assertEquals(len(servers), 0,
                          self.msg.format('Disabled servers', 0,
                          len(servers)))

        sch_img_obj = self.images_provider.scheduled_images_client. \
            enable_scheduled_images(tenant_id, instance_id, retention)
        self.assertEquals(sch_img_obj.status_code, 200,
                          self.msg.format('status_code', 200,
                                     sch_img_obj.status_code))

        list_servers_obj = self.images_provider.servers_client.\
            list_servers(image_schedule=True)
        self.assertEquals(list_servers_obj.status_code, 200,
                          self.msg.format('status_code', 200,
                                     list_servers_obj.status_code))

        list_servers = list_servers_obj.entity
        enabled_servers = []
        for s in list_servers:
            if (s.id == alt_instance_id):
                servers.append(s)
            if (s.id == instance_id):
                enabled_servers.append(s)
                server = s
            if (s.id == multi_ret_instance_id):
                enabled_servers.append(s)

        self.assertEquals(len(enabled_servers), 2,
                          self.msg.format('Enabled servers', 2,
                                          len(enabled_servers)))
        self.assertEquals(len(servers), 0,
                          self.msg.format('Disabled servers', 0,
                          len(servers)))

        self.assertFalse(hasattr(server, 'RAX-SI:image_schedule'),
                         self.msg.format('RAX-SI:image_schedule',
                                         'to not be present', 'was present'))
