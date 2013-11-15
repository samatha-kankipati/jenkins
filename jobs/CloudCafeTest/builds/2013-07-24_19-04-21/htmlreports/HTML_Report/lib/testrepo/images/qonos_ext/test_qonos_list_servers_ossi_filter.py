from testrepo.common.testfixtures.images import BaseImagesFixture
from ccengine.common.decorators import attr
from ccengine.common.exceptions.compute import ItemNotFound
import ccengine.common.tools.datagen as datagen
from ccengine.domain.types import NovaServerStatusTypes


class TestQonosListServersOSSIFilter(BaseImagesFixture):

    @classmethod
    def setUpClass(cls):
        '''Creates the server instances used for all tests in this class'''

        super(TestQonosListServersOSSIFilter, cls).setUpClass()

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

    @attr('smoke')
    def test_happy_path_list_servers_with_image_schedule(self):
        '''Happy Path - After enabling scheduled images for multiple
        valid servers, list servers with image-schedule set to true'''

        """
        1) Create 2 valid server instances
        2) Enable scheduled images using a valid retention value for 1 server
        3) Verify that the response code is 200
        4) List servers with image-schedule set to true
        5) Verify that the response code is 200
        6) Verify that the response contains the 1 server with image-schedule

        Attributes to verify:
        server id
        scheduled images settings
        retention
        """

        tenant_id = self.tenant_id
        instance_id = self.instance_id
        retention = self.retention
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
            if (s.id == instance_id):
                servers.append(s)
        self.assertEquals(len(servers), 1, self.msg.format('servers', 1,
                          len(servers)))

        server = servers[0]
        self.assertEquals(server.id, instance_id,
                          self.msg.format('server id', instance_id, server.id))
        self.assertFalse(hasattr(server, 'RAX-SI:image_schedule'),
                         self.msg.format('RAX-SI:image_schedule',
                                         'to not be present', 'was present'))

    @attr('positive')
    def test_list_servers_with_image_schedule_server_disabled(self):
        '''List servers with image-schedule set to true for a server that has
        not had scheduled images enabled'''

        """
        1) Create a valid server instance
        2) Enabled scheduled images with a valid retention value
        3) Verify that the response code is 200
        4) Disabled scheduled images for the server
        5) Verify that the response code is 202
        6) List servers with image-schedule set to true
        7) Verify that the response code is 200
        8) Verify that the response does not contain the server

        Attributes to verify:
        scheduled images settings
        retention
        """

        tenant_id = self.config.images.tenant_id
        instance_id = self.instance_id
        retention = self.config.images.retention
        servers = []

        sch_img_obj = self.images_provider.scheduled_images_client. \
            enable_scheduled_images(tenant_id, instance_id, retention)
        self.assertEquals(sch_img_obj.status_code, 200,
                          self.msg.format('status_code', 200,
                                     sch_img_obj.status_code))

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
            if (s.id == instance_id):
                servers.append(s)
        self.assertEquals(len(servers), 0, self.msg.format('servers', 0,
                          len(servers)))

    @attr('positive')
    def test_enable_sch_img_disable_list_servers_w_image_schedule_true(self):
        '''After enabling scheduled images for a server and immediately
        disabling it, list servers with image-schedule set to true'''

        """
        1) Create 2 valid server instances
        2) Enable scheduled images using a valid retention value for each
            server
        3) Verify that the response code is 200
        4) Disable scheduled images for each server
        5) Verify that the response code is 202
        6) List servers with image-schedule set to true
        7) Verify that the response code is 200
        8) Verify that the response contains no servers

        Attributes to verify:
        server id
        scheduled images settings
        retention
        """

        tenant_id = self.tenant_id
        instance_id = self.instance_id
        alt_instance_id = self.alt_instance_id
        retention = self.retention
        servers = []

        sch_img_obj = self.images_provider.scheduled_images_client. \
            enable_scheduled_images(tenant_id, instance_id, retention)
        self.assertEquals(sch_img_obj.status_code, 200,
                          self.msg.format('status_code', 200,
                                     sch_img_obj.status_code))

        sch_img_obj = self.images_provider.scheduled_images_client. \
            enable_scheduled_images(tenant_id, alt_instance_id, retention)
        self.assertEquals(sch_img_obj.status_code, 200,
                          self.msg.format('status_code', 200,
                                     sch_img_obj.status_code))

        dis_sch_img_obj = self.images_provider.scheduled_images_client. \
            disable_scheduled_images(tenant_id, instance_id)
        self.assertEquals(dis_sch_img_obj.status_code, 202,
                          self.msg.format('status_code', 202,
                                     dis_sch_img_obj.status_code))

        dis_sch_img_obj = self.images_provider.scheduled_images_client. \
            disable_scheduled_images(tenant_id, alt_instance_id)
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
        self.assertEquals(len(servers), 0)

    @attr('positive')
    def test_disable_sch_img_lst_srvrs_w_image_schedule_srvr_dis(self):
        '''After disabling scheduled images for a server that doesn't have
        scheduled images enabled, list servers with image-schedule set to
        true'''

        """
        1) Create a valid server instance
        2) Disabled scheduled images for the server
        3) Verify that the response code is 404
        4) List servers with image-schedule set to true
        5) Verify that the response code is 200
        6) Verify that the response does not contain the server
        """

        instance_id = self.new_instance_id
        tenant_id = self.tenant_id
        servers = []

        with self.assertRaises(ItemNotFound):
            self.images_provider.scheduled_images_client. \
                disable_scheduled_images(tenant_id, instance_id)

        list_servers_obj = self.images_provider.servers_client.\
            list_servers(image_schedule=True)
        self.assertEquals(list_servers_obj.status_code, 200,
                          self.msg.format('status_code', 200,
                                     list_servers_obj.status_code))

        list_servers = list_servers_obj.entity
        for s in list_servers:
            if (s.id == instance_id):
                servers.append(s)
        self.assertEquals(len(servers), 0, self.msg.format('servers', 0,
                          len(servers)))

    @attr('positive')
    def test_dis_sch_img_lst_srvrs_w_img_sch_srvr_dis_false(self):
        '''After disabling scheduled images for a server that doesn't have
        scheduled images enabled, list servers with image-schedule set to
        false'''

        """
        1) Create a valid server instance
        2) Disabled scheduled images for the server
        3) Verify that the response code is 404
        4) List servers with image-schedule set to false
        5) Verify that the response code is 200
        6) Verify that the response contains the server
        """

        instance_id = self.new_instance_id
        tenant_id = self.tenant_id
        servers = []

        with self.assertRaises(ItemNotFound):
            self.images_provider.scheduled_images_client. \
                disable_scheduled_images(tenant_id, instance_id)

        list_servers_obj = self.images_provider.servers_client.\
            list_servers(image_schedule=False)
        self.assertEquals(list_servers_obj.status_code, 200,
                          self.msg.format('status_code', 200,
                                     list_servers_obj.status_code))

        list_servers = list_servers_obj.entity
        for s in list_servers:
            if (s.id == instance_id):
                servers.append(s)
        self.assertEquals(len(servers), 1, self.msg.format('servers', 1,
                          len(servers)))
