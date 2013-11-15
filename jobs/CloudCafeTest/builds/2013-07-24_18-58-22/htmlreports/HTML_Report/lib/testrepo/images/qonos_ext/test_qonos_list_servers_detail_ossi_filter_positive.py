from testrepo.common.testfixtures.images import BaseImagesFixture
from ccengine.common.decorators import attr
from ccengine.common.exceptions.compute import ItemNotFound
import ccengine.common.tools.datagen as datagen
from ccengine.domain.types import NovaServerStatusTypes


class TestQonosListServersDetailOSSIFilterPositive(BaseImagesFixture):

    @classmethod
    def setUpClass(cls):
        '''Creates the server instances used for all tests in this class'''

        super(TestQonosListServersDetailOSSIFilterPositive, cls).setUpClass()

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

    @attr('positive')
    def test_list_servers_detail_with_image_schedule_false(self):
        """After enabling scheduled images for multiple
        valid servers, list servers detail with image-schedule set to false

        1) Create 2 valid server instances
        2) Enable scheduled images using a valid retention value for 1 server
        3) Verify that the response code is 200
        4) List servers_detail with image-schedule set to false
        5) Verify that the response code is 200
        6) Verify that the response contains the 1 server without
            image-schedule

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
        msg = self.msg

        sch_img_obj = self.images_provider.scheduled_images_client. \
            enable_scheduled_images(tenant_id, instance_id, retention)
        self.assertEquals(sch_img_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     sch_img_obj.status_code))

        list_servers_detail_obj = self.images_provider.servers_client.\
            list_servers_with_detail(image_schedule=False)
        self.assertEquals(list_servers_detail_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     list_servers_detail_obj.status_code))

        list_servers_detail = list_servers_detail_obj.entity
        for s in list_servers_detail:
            if (s.id == alt_instance_id):
                servers.append(s)
        self.assertEquals(len(servers), 1, msg.format('servers', 1,
                          len(servers)))

    @attr('positive')
    def test_list_servers_detail_with_image_schedule_server_not_enabled(self):
        """List servers detail with image-schedule set to true for a server
        that has not had scheduled images enabled

        1) Create a valid server instance
        2) List servers detail with image-schedule set to true
        3) Verify that the response code is 200
        4) Verify that the response does not contain the server

        Attributes to verify:
        scheduled images settings
        retention
        """

        instance_id = self.alt_instance_id
        servers = []
        msg = self.msg

        list_servers_detail_obj = self.images_provider.servers_client.\
            list_servers_with_detail(image_schedule=True)
        self.assertEquals(list_servers_detail_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     list_servers_detail_obj.status_code))

        list_servers_detail = list_servers_detail_obj.entity
        for s in list_servers_detail:
            if (s.id == instance_id):
                servers.append(s)
        self.assertEquals(len(servers), 0, msg.format('servers', 0,
                          len(servers)))

    @attr('positive')
    def test_lst_srvrs_detail_w_image_schedule_false_server_not_enabled(self):
        """List servers detail with image-schedule set to false for a server
        that has not had scheduled images enabled

        1) Create a valid server instance
        2) List servers detail with image-schedule set to false
        3) Verify that the response code is 200
        4) Verify that the response does contain the server

        Attributes to verify:
        scheduled images settings
        retention
        """

        instance_id = self.alt_instance_id
        servers = []
        msg = self.msg

        list_servers_detail_obj = self.images_provider.servers_client.\
            list_servers_with_detail(image_schedule=False)
        self.assertEquals(list_servers_detail_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     list_servers_detail_obj.status_code))

        list_servers_detail = list_servers_detail_obj.entity
        for s in list_servers_detail:
            if (s.id == instance_id):
                servers.append(s)
        self.assertEquals(len(servers), 1, msg.format('servers', 1,
                          len(servers)))

    @attr('positive')
    def test_list_servers_detail_with_image_schedule_server_disabled(self):
        """List servers detail with image-schedule set to true for a server
        that has scheduled images disabled

        1) Create a valid server instance
        2) Enabled scheduled images with a valid retention value
        3) Verify that the response code is 200
        4) Disabled scheduled images for the server
        5) Verify that the response code is 202
        6) List servers detail with image-schedule set to true
        7) Verify that the response code is 200
        8) Verify that the response does not contain the server

        Attributes to verify:
        scheduled images settings
        retention
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

        list_servers_detail_obj = self.images_provider.servers_client.\
            list_servers_with_detail(image_schedule=True)
        self.assertEquals(list_servers_detail_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     list_servers_detail_obj.status_code))

        list_servers_detail = list_servers_detail_obj.entity
        for s in list_servers_detail:
            if (s.id == instance_id):
                servers.append(s)
        self.assertEquals(len(servers), 0, msg.format('servers', 0,
                          len(servers)))

    @attr('positive')
    def test_list_servers_detail_w_image_schedule_false_server_disabled(self):
        """List servers detail with image-schedule set to false for a server
        that has scheduled images disabled
        1) Create a valid server instance
        2) Enabled scheduled images with a valid retention value
        3) Verify that the response code is 200
        4) Disabled scheduled images for the server
        5) Verify that the response code is 202
        6) List servers detail with image-schedule set to false
        7) Verify that the response code is 200
        8) Verify that the response contains does contain the server

        Attributes to verify:
        scheduled images settings
        retention
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

        list_servers_detail_obj = self.images_provider.servers_client.\
            list_servers_with_detail(image_schedule=False)
        self.assertEquals(list_servers_detail_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     list_servers_detail_obj.status_code))

        list_servers_detail = list_servers_detail_obj.entity
        for s in list_servers_detail:
            if (s.id == instance_id):
                servers.append(s)
        self.assertEquals(len(servers), 1, msg.format('servers', 1,
                          len(servers)))

    @attr('positive')
    def test_list_servers_detail_w_image_schedule_with_ret_more_than_1(self):
        """After enabling scheduled images with a retention of more than 1,
        list servers detail with image-schedule set to true

        1) Create 2 valid server instances
        2) Enable scheduled images using a valid retention value of more than 1
            for both instances
        3) Verify that the response code is 200
        4) List servers detail with image-schedule set to true
        5) Verify that the response code is 200
        6) Verify that the response contains both servers with image-schedule
            and expected retentions

        Attributes to verify:
        scheduled images settings
        retention
        """

        tenant_id = self.tenant_id
        instance_id = self.instance_id
        multi_ret_instance_id = self.multi_ret_instance_id
        alt_retention = self.alt_retention
        servers = []
        msg = self.msg
        sch_img_obj = self.images_provider.scheduled_images_client. \
            enable_scheduled_images(tenant_id, instance_id, alt_retention)
        self.assertEquals(sch_img_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     sch_img_obj.status_code))

        sch_img_obj = self.images_provider.scheduled_images_client. \
            enable_scheduled_images(tenant_id, multi_ret_instance_id,
                                    alt_retention)
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
            if (s.id == instance_id or s.id == multi_ret_instance_id):
                servers.append(s)
        self.assertEquals(len(servers), 2, msg.format('servers', 2,
                          len(servers)))

        for server in servers:
            ret = self.images_provider.get_retention(server)
            self.assertEquals(ret, alt_retention,
                              msg.format('RAX-SI:image_schedule',
                                         alt_retention, ret))

    @attr('positive')
    def test_enable_sch_img_disable_list_servers_detail_w_img_sch_true(self):
        """After enabling scheduled images for a server and immediately
        disabling it, list servers detail with image-schedule set to true

        1) Create 2 valid server instances
        2) Enable scheduled images using a valid retention value for each
            server
        3) Verify that the response code is 200
        4) Disable scheduled images for each server
        5) Verify that the response code is 202
        6) List servers detail with image-schedule set to true
        7) Verify that the response code is 200
        8) Verify that the response contains no servers

        Attributes to verify:
        server id
        scheduled images settings
        retention
        """

        tenant_id = self.tenant_id
        instance_id = self.instance_id
        multi_ret_instance_id = self.multi_ret_instance_id
        retention = self.retention
        servers = []
        msg = self.msg

        sch_img_obj = self.images_provider.scheduled_images_client. \
            enable_scheduled_images(tenant_id, instance_id, retention)
        self.assertEquals(sch_img_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     sch_img_obj.status_code))

        sch_img_obj = self.images_provider.scheduled_images_client. \
            enable_scheduled_images(tenant_id, multi_ret_instance_id,
                                    retention)
        self.assertEquals(sch_img_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     sch_img_obj.status_code))

        dis_sch_img_obj = self.images_provider.scheduled_images_client. \
            disable_scheduled_images(tenant_id, instance_id)
        self.assertEquals(dis_sch_img_obj.status_code, 202,
                          msg.format('status_code', 202,
                                     dis_sch_img_obj.status_code))

        dis_sch_img_obj = self.images_provider.scheduled_images_client. \
            disable_scheduled_images(tenant_id, multi_ret_instance_id)
        self.assertEquals(dis_sch_img_obj.status_code, 202,
                          msg.format('status_code', 202,
                                     dis_sch_img_obj.status_code))

        list_servers_detail_obj = self.images_provider.servers_client.\
            list_servers_with_detail(image_schedule=True)
        self.assertEquals(list_servers_detail_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     list_servers_detail_obj.status_code))

        list_servers_detail = list_servers_detail_obj.entity

        for s in list_servers_detail:
            if (s.id == instance_id or s.id == multi_ret_instance_id):
                servers.append(s)
        self.assertEquals(len(servers), 0)

    @attr('positive')
    def test_enable_disable_enable_sch_images_list_servers_detail(self):
        """After enabling scheduled images for a server, disable it and
        enable it again, list servers detail with image-schedule set to true

        1) Create 2 valid server instances
        2) Enable scheduled images using a valid retention value for a server
        3) Verify that the response code is 200
        4) List servers detail with image-schedule set to true
        5) Verify that the response code is 200
        6) Verify that the response contains the 1 server with image-schedule
        7) Disable scheduled images using a valid retention value for a server
        8) Verify that the response code is 200
        9) List servers detail with image-schedule set to true
        10) Verify that the response code is 200
        11) Verify that the response contains no server
        12) Enable scheduled images using a valid retention value for a server
        13) Verify that the response code is 200
        14) List servers detail with image-schedule set to true
        15) Verify that the response code is 200
        16) Verify that the response contains the 1 server with image-schedule

        Attributes to verify:
        server id
        scheduled images settings
        retention
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

        dis_sch_img_obj = self.images_provider.scheduled_images_client. \
            disable_scheduled_images(tenant_id, instance_id)
        self.assertEquals(dis_sch_img_obj.status_code, 202,
                          msg.format('status_code', 202,
                                     dis_sch_img_obj.status_code))

        list_servers_detail_obj = self.images_provider.servers_client.\
            list_servers_with_detail(image_schedule=True)
        self.assertEquals(list_servers_detail_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     list_servers_detail_obj.status_code))

        list_servers_detail = list_servers_detail_obj.entity
        servers.pop()
        for s in list_servers_detail:
            if (s.id == instance_id):
                servers.append(s)
        self.assertEquals(len(servers), 0)

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

    @attr('positive')
    def test_enable_disabled_sch_img_w_larger_ret_list_server_details(self):
        """After enabling schedule images for a server with a retention of 1,
        disable it, enable it again with larger retention, list servers detail
        with image-schedule set to true

        1) Create 2 valid server instances
        2) Enable scheduled images using a valid retention value for a server
        3) Verify that the response code is 200
        4) List servers detail with image-schedule set to true
        5) Verify that the response code is 200
        6) Verify that the response contains the 1 server with image-schedule
        7) Disable scheduled images using a valid retention value for a server
        8) Verify that the response code is 200
        9) List servers detail with image-schedule set to true
        10) Verify that the response code is 200
        11) Verify that the response contains no server
        12) Enable scheduled images using a larger retention value for a server
        13) Verify that the response code is 200
        14) List servers detail with image-schedule set to true
        15) Verify that the response code is 200
        16) Verify that the response contains the 1 server with image-schedule
            having larger retention

        Attributes to verify:
        server id
        scheduled images settings
        retention
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

        dis_sch_img_obj = self.images_provider.scheduled_images_client. \
            disable_scheduled_images(tenant_id, instance_id)
        self.assertEquals(dis_sch_img_obj.status_code, 202,
                          msg.format('status_code', 202,
                                     dis_sch_img_obj.status_code))

        list_servers_detail_obj = self.images_provider.servers_client.\
            list_servers_with_detail(image_schedule=True)
        self.assertEquals(list_servers_detail_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     list_servers_detail_obj.status_code))

        list_servers_detail = list_servers_detail_obj.entity
        servers.pop()
        for s in list_servers_detail:
            if (s.id == instance_id):
                servers.append(s)
        self.assertEquals(len(servers), 0)

        sch_img_obj = self.images_provider.scheduled_images_client. \
            enable_scheduled_images(tenant_id, instance_id, alt_retention)
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
        self.assertEquals(ret, alt_retention,
                          msg.format('RAX-SI:image_schedule',
                                     alt_retention, ret))

    @attr('positive')
    def test_enable_disable_enable_ret_sch_images_list_servers_detail(self):
        """After enabling scheduled images for a server, disable it and
        enable it again, list servers detail with image-schedule set to true

        1) Create 2 valid server instances
        2) Enable scheduled images using a valid retention value for a server
        3) Verify that the response code is 200
        4) List servers detail with image-schedule set to true
        5) Verify that the response code is 200
        6) Verify that the response contains the 1 server with image-schedule
        7) Disable scheduled images using a valid retention value for a server
        8) Verify that the response code is 200
        9) List servers detail with image-schedule set to true
        10) Verify that the response code is 200
        11) Verify that the response contains no server
        12) Enable scheduled images using a larger retention value for a server
        13) Verify that the response code is 200
        14) List servers detail with image-schedule set to true
        15) Verify that the response code is 200
        16) Verify that the response contains the 1 server with image-schedule
            having larger retention

        Attributes to verify:
        server id
        scheduled images settings
        retention
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

        dis_sch_img_obj = self.images_provider.scheduled_images_client. \
            disable_scheduled_images(tenant_id, instance_id)
        self.assertEquals(dis_sch_img_obj.status_code, 202,
                          msg.format('status_code', 202,
                                     dis_sch_img_obj.status_code))

        list_servers_detail_obj = self.images_provider.servers_client.\
            list_servers_with_detail(image_schedule=True)
        self.assertEquals(list_servers_detail_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     list_servers_detail_obj.status_code))

        list_servers_detail = list_servers_detail_obj.entity
        servers.pop()
        for s in list_servers_detail:
            if (s.id == instance_id):
                servers.append(s)
        self.assertEquals(len(servers), 0, msg.format('servers', 0,
                          len(servers)))

        sch_img_obj = self.images_provider.scheduled_images_client. \
            enable_scheduled_images(tenant_id, instance_id, alt_retention)
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
        self.assertEquals(ret, alt_retention,
                          msg.format('RAX-SI:image_schedule',
                                     alt_retention, ret))

    @attr('positive')
    def test_enable_enable_sch_images_list_servers_detail(self):
        """After enabling scheduled images for a server that is already
        enabled with same retention, list servers detail with image-schedule
        set to true

        1) Create 2 valid server instances
        2) Enable scheduled images using a valid retention value for 1 server
        3) Verify that the response code is 200
        4) List servers detail with image-schedule set to true
        5) Verify that the response code is 200
        6) Verify that the response contains the 1 server with image-schedule
        7) Enable scheduled images using same retention value for the server
        8) Verify that the response code is 200
        9) List servers detail with image-schedule set to true
        10) Verify that the response code is 200
        11) Verify that the response contains the 1 server with image-schedule

        Attributes to verify:
        server id
        scheduled images settings
        retention
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
        servers.pop()
        for s in list_servers_detail:
            if (s.id == instance_id):
                servers.append(s)
        self.assertEquals(len(servers), 1, msg.format('servers', 1,
                          len(servers)))

        server = servers[0]
        ret = self.images_provider.get_retention(server)
        self.assertEquals(ret, retention,
                          msg.format('RAX-SI:image_schedule', retention, ret))

    @attr('positive')
    def test_enable_enable_different_ret_sch_images_list_servers_detail(self):
        """After enabling scheduled images for a server that is already
        enabled with same retention, list servers detail with image-schedule
        set to true

        1) Create 2 valid server instances
        2) Enable scheduled images using a valid retention value for 1 server
        3) Verify that the response code is 200
        4) List servers detail with image-schedule set to true
        5) Verify that the response code is 200
        6) Verify that the response contains the 1 server with image-schedule
        7) Enable scheduled images using different retention value for the
            server
        8) Verify that the response code is 200
        9) List servers detail with image-schedule set to true
        10) Verify that the response code is 200
        11) Verify that the response contains the 1 server with image-schedule
            having different retention

        Attributes to verify:
        server id
        scheduled images settings
        retention
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
                          msg.format('image_schedule', retention, ret))

        sch_img_obj = self.images_provider.scheduled_images_client. \
            enable_scheduled_images(tenant_id, instance_id, alt_retention)
        self.assertEquals(sch_img_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     sch_img_obj.status_code))

        list_servers_detail_obj = self.images_provider.servers_client.\
            list_servers_with_detail(image_schedule=True)
        self.assertEquals(list_servers_detail_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     list_servers_detail_obj.status_code))

        list_servers_detail = list_servers_detail_obj.entity
        servers.pop()
        for s in list_servers_detail:
            if (s.id == instance_id):
                servers.append(s)
        self.assertEquals(len(servers), 1, msg.format('servers', 1,
                          len(servers)))

        server = servers[0]
        ret = self.images_provider.get_retention(server)
        self.assertEquals(ret, alt_retention,
                          msg.format('image_schedule', alt_retention, ret))

    @attr('positive')
    def test_disable_sch_img_lst_srvrs_detail_w_image_schedule_srvr_dis(self):
        """After disabling scheduled images for a server that doesn't have
        scheduled images enabled, list servers detail with image-schedule set
        to true

        1) Create a valid server instance
        2) Disabled scheduled images for the server
        3) Verify that the response code is 404
        4) List servers detail with image-schedule set to true
        5) Verify that the response code is 200
        6) Verify that the response does not contain the server
        """

        instance_id = self.alt_instance_id
        tenant_id = self.tenant_id
        servers = []
        msg = self.msg

        with self.assertRaises(ItemNotFound):
            self.images_provider.scheduled_images_client. \
                disable_scheduled_images(tenant_id, instance_id)

        list_servers_detail_obj = self.images_provider.servers_client.\
            list_servers_with_detail(image_schedule=True)
        self.assertEquals(list_servers_detail_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     list_servers_detail_obj.status_code))

        list_servers_detail = list_servers_detail_obj.entity
        for s in list_servers_detail:
            if (s.id == instance_id):
                servers.append(s)
        self.assertEquals(len(servers), 0, msg.format('servers', 0,
                          len(servers)))

    @attr('positive')
    def test_dis_sch_img_lst_srvrs_detail_w_img_sch_srvr_dis_false(self):
        """After disabling scheduled images for a server that doesn't have
        scheduled images enabled, list servers detail with image-schedule set
        to false

        1) Create a valid server instance
        2) Disabled scheduled images for the server
        3) Verify that the response code is 404
        4) List servers detail with image-schedule set to false
        5) Verify that the response code is 200
        6) Verify that the response contains the server
        """

        instance_id = self.alt_instance_id
        tenant_id = self.tenant_id
        servers = []
        msg = self.msg

        with self.assertRaises(ItemNotFound):
            self.images_provider.scheduled_images_client. \
                disable_scheduled_images(tenant_id, instance_id)

        list_servers_detail_obj = self.images_provider.servers_client.\
            list_servers_with_detail(image_schedule=False)
        self.assertEquals(list_servers_detail_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     list_servers_detail_obj.status_code))

        list_servers_detail = list_servers_detail_obj.entity
        for s in list_servers_detail:
            if (s.id == instance_id):
                servers.append(s)
        self.assertEquals(len(servers), 1, msg.format('servers', 1,
                          len(servers)))
