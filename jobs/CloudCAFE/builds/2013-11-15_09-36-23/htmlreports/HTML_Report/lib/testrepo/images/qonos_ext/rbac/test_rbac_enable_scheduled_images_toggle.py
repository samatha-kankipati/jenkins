import ccengine.common.tools.datagen as datagen
from ccengine.common.constants.images_constants import Constants
from ccengine.common.decorators import attr
from ccengine.common.exceptions.compute import Forbidden
from ccengine.domain.types import NovaServerStatusTypes
from testrepo.common.testfixtures.images import RbacImagesFixture


class TestRbacEnableScheduledImagesToggle(RbacImagesFixture):

    @classmethod
    def setUpClass(self):
        """Creates the server instances and snapshots used for all tests in
        this class.
        """

        super(TestRbacEnableScheduledImagesToggle, self).setUpClass()

        count = 4
        self.servers = []

        for x in range(count):
            server_name = datagen.random_string(size=10)
            server_obj = \
                self.images_provider.create_server_no_wait(server_name)
            self.servers.append(server_obj.entity)

        for server in self.servers:
            self.images_provider.\
                wait_for_server_status(server.id,
                                       NovaServerStatusTypes.ACTIVE)

    @attr('pos', 'rbac')
    def test_rbac_admin_enable_disable_enable_scheduled_images(self):
        """Rbac - Enable scheduled images for a valid server as admin then
        disabled by admin then enable again by admin.

        1) Create a valid server instance
        2) Enable scheduled images using a valid retention value as admin
        3) Verify that the response code is 200
        4) Disable scheduled images as admin
        5) Verify that the response code is 202
        6) Enable scheduled images using a valid retention value as admin again
        7) Verify that the response code is 200
        """

        tenant_id = self.config.images.tenant_id
        instance_id = self.servers[0].id
        retention = self.config.images.retention
        msg = Constants.MESSAGE

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

    @attr('pos', 'rbac')
    def test_rbac_admin_enable_disable_others_enable_scheduled_images(self):
        """Rbac - Enable scheduled images for a valid server as admin then
        disabled by admin then enable again by observer, global observer,
        creator and global admin.

        1) Create a valid server instance
        2) Enable scheduled images using a valid retention value as admin
        3) Verify that the response code is 200
        4) Disable scheduled images as admin
        5) Verify that the response code is 202
        6) Enable scheduled images using a valid retention value as observer
        again
        7) Verify that the response code is 403
        8) Enable scheduled images using a valid retention value as global
        observer again
        9) Verify that the response code is 403
        10) Enable scheduled images using a valid retention value as creator
        again
        11) Verify that the response code is 200
        12) Enable scheduled images using a valid retention value as global
        admin again
        13) Verify that the response code is 200
        """

        tenant_id = self.config.images.tenant_id
        instance_id = self.servers[0].id
        retention = self.config.images.retention
        msg = Constants.MESSAGE

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

        # Check observer
        with self.assertRaises(Forbidden):
            self.observer_images_provider.scheduled_images_client. \
                enable_scheduled_images(tenant_id, instance_id, retention)

        # Check global observer
        with self.assertRaises(Forbidden):
            self.global_observer_img_prov.scheduled_images_client. \
                enable_scheduled_images(tenant_id, instance_id, retention)

        # Check creator
        sch_img_obj = self.creator_images_provider.scheduled_images_client. \
            enable_scheduled_images(tenant_id, instance_id, retention)
        self.assertEquals(sch_img_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     sch_img_obj.status_code))

        # Check global admin
        sch_img_obj = self.global_admin_img_prov.scheduled_images_client. \
            enable_scheduled_images(tenant_id, instance_id, retention)
        self.assertEquals(sch_img_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     sch_img_obj.status_code))

    @attr('pos', 'rbac')
    def test_rbac_creator_enable_admin_disable_enable_scheduled_images(self):
        """Rbac - Enable scheduled images for a valid server as creator then
        disabled by admin then enable again by admin.

        1) Create a valid server instance
        2) Enable scheduled images using a valid retention value as creator
        3) Verify that the response code is 200
        4) Disable scheduled images as admin
        5) Verify that the response code is 202
        6) Enable scheduled images using a valid retention value as admin again
        7) Verify that the response code is 200
        """

        tenant_id = self.config.images.tenant_id
        instance_id = self.servers[1].id
        retention = self.config.images.retention
        msg = Constants.MESSAGE

        sch_img_obj = self.creator_images_provider.scheduled_images_client. \
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

    @attr('pos', 'rbac')
    def test_rbac_creator_en_admin_dis_others_en_scheduled_images(self):
        """Rbac - Enable scheduled images for a valid server as creator then
        disabled by admin then enable again by observer, global observer,
        creator and global admin.

        1) Create a valid server instance
        2) Enable scheduled images using a valid retention value as creator
        3) Verify that the response code is 200
        4) Disable scheduled images as admin
        5) Verify that the response code is 202
        6) Enable scheduled images using a valid retention value as observer
        again
        7) Verify that the response code is 403
        8) Enable scheduled images using a valid retention value as global
        observer again
        9) Verify that the response code is 403
        10) Enable scheduled images using a valid retention value as creator
        again
        11) Verify that the response code is 200
        12) Enable scheduled images using a valid retention value as global
        admin again
        13) Verify that the response code is 200
        """

        tenant_id = self.config.images.tenant_id
        instance_id = self.servers[2].id
        retention = self.config.images.retention
        msg = Constants.MESSAGE

        sch_img_obj = self.creator_images_provider.scheduled_images_client. \
            enable_scheduled_images(tenant_id, instance_id, retention)
        self.assertEquals(sch_img_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     sch_img_obj.status_code))

        dis_sch_img_obj = self.images_provider.scheduled_images_client. \
            disable_scheduled_images(tenant_id, instance_id)
        self.assertEquals(dis_sch_img_obj.status_code, 202,
                          msg.format('status_code', 202,
                                     dis_sch_img_obj.status_code))

        # Check observer
        with self.assertRaises(Forbidden):
            self.observer_images_provider.scheduled_images_client. \
                enable_scheduled_images(tenant_id, instance_id, retention)

        # Check global observer
        with self.assertRaises(Forbidden):
            self.global_observer_img_prov.scheduled_images_client. \
                enable_scheduled_images(tenant_id, instance_id, retention)

        # Check creator
        sch_img_obj = self.creator_images_provider.scheduled_images_client. \
            enable_scheduled_images(tenant_id, instance_id, retention)
        self.assertEquals(sch_img_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     sch_img_obj.status_code))

        # Check global admin
        sch_img_obj = self.global_admin_img_prov.scheduled_images_client. \
            enable_scheduled_images(tenant_id, instance_id, retention)
        self.assertEquals(sch_img_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     sch_img_obj.status_code))

    @attr('pos', 'rbac')
    def test_rbac_global_admin_enable_disable_enable_scheduled_images(self):
        """Rbac - Enable scheduled images for a valid server as global admin
        then disabled by global admin then enable again by global admin.

        1) Create a valid server instance
        2) Enable scheduled images using a valid retention value as global
        admin
        3) Verify that the response code is 200
        4) Disable scheduled images as global admin
        5) Verify that the response code is 202
        6) Enable scheduled images using a valid retention value as global
        admin again
        7) Verify that the response code is 200
        """

        tenant_id = self.config.images.tenant_id
        instance_id = self.servers[3].id
        retention = self.config.images.retention
        msg = Constants.MESSAGE

        sch_img_obj = self.global_admin_img_prov.scheduled_images_client. \
            enable_scheduled_images(tenant_id, instance_id, retention)
        self.assertEquals(sch_img_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     sch_img_obj.status_code))

        dis_sch_img_obj = self.global_admin_img_prov.scheduled_images_client. \
            disable_scheduled_images(tenant_id, instance_id)
        self.assertEquals(dis_sch_img_obj.status_code, 202,
                          msg.format('status_code', 202,
                                     dis_sch_img_obj.status_code))

        sch_img_obj = self.global_admin_img_prov.scheduled_images_client. \
            enable_scheduled_images(tenant_id, instance_id, retention)
        self.assertEquals(sch_img_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     sch_img_obj.status_code))

    @attr('pos', 'rbac')
    def test_rbac_global_admin_enable_then_disable_others_enable_sch_img(self):
        """Rbac - Enable scheduled images for a valid server as global admin
        then disabled by global admin then enable again by observer, global
        observer, creator and admin.

        1) Create a valid server instance
        2) Enable scheduled images using a valid retention value as global
        admin
        3) Verify that the response code is 200
        4) Disable scheduled images as global admin
        5) Verify that the response code is 202
        6) Enable scheduled images using a valid retention value as observer
        again
        7) Verify that the response code is 403
        8) Enable scheduled images using a valid retention value as global
        observer again
        9) Verify that the response code is 403
        10) Enable scheduled images using a valid retention value as creator
        again
        11) Verify that the response code is 200
        12) Enable scheduled images using a valid retention value as
        admin again
        13) Verify that the response code is 200
        """

        tenant_id = self.config.images.tenant_id
        instance_id = self.servers[3].id
        retention = self.config.images.retention
        msg = Constants.MESSAGE

        sch_img_obj = self.global_admin_img_prov.scheduled_images_client. \
            enable_scheduled_images(tenant_id, instance_id, retention)
        self.assertEquals(sch_img_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     sch_img_obj.status_code))

        dis_sch_img_obj = self.global_admin_img_prov.scheduled_images_client. \
            disable_scheduled_images(tenant_id, instance_id)
        self.assertEquals(dis_sch_img_obj.status_code, 202,
                          msg.format('status_code', 202,
                                     dis_sch_img_obj.status_code))

        # Check observer
        with self.assertRaises(Forbidden):
            self.observer_images_provider.scheduled_images_client. \
                enable_scheduled_images(tenant_id, instance_id, retention)

        # Check global observer
        with self.assertRaises(Forbidden):
            self.global_observer_img_prov.scheduled_images_client. \
                enable_scheduled_images(tenant_id, instance_id, retention)

        # Check creator
        sch_img_obj = self.creator_images_provider.scheduled_images_client. \
            enable_scheduled_images(tenant_id, instance_id, retention)
        self.assertEquals(sch_img_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     sch_img_obj.status_code))

        # Check admin
        sch_img_obj = self.images_provider.scheduled_images_client. \
            enable_scheduled_images(tenant_id, instance_id, retention)
        self.assertEquals(sch_img_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     sch_img_obj.status_code))
