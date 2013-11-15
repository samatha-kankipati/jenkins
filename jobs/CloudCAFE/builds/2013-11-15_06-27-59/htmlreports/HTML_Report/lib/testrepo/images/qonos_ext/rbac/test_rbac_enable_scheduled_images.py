import ccengine.common.tools.datagen as datagen
from ccengine.common.constants.images_constants import Constants
from ccengine.common.decorators import attr
from ccengine.common.exceptions.compute import Forbidden
from ccengine.domain.types import NovaServerStatusTypes
from testrepo.common.testfixtures.images import RbacImagesFixture


class TestRbacEnableScheduledImages(RbacImagesFixture):

    @classmethod
    def setUpClass(self):
        """Creates the server instances and snapshots used for all tests in
        this class.
        """

        super(TestRbacEnableScheduledImages, self).setUpClass()

        count = 5
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
    def test_rbac_admin_enable_scheduled_images(self):
        """Rbac - Enable scheduled images for a valid server as admin.

        1) Create a valid server instance
        2) Enable scheduled images using a valid retention value as admin
        3) Verify that the response code is 200
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

    @attr('pos', 'rbac')
    def test_rbac_creator_enable_scheduled_images(self):
        """Rbac - Enable scheduled images for a valid server as creator.

        1) Create a valid server instance
        2) Enable scheduled images using a valid retention value as creator
        3) Verify that the response code is 200
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

    @attr('neg', 'rbac')
    def test_rbac_observer_enable_scheduled_images(self):
        """Rbac - Enable scheduled images for a valid server as observer.

        1) Create a valid server instance
        2) Enable scheduled images using a valid retention value as observer
        3) Verify that the response code is 403
        """

        tenant_id = self.config.images.tenant_id
        instance_id = self.servers[2].id
        retention = self.config.images.retention

        with self.assertRaises(Forbidden):
            self.observer_images_provider.scheduled_images_client. \
                enable_scheduled_images(tenant_id, instance_id, retention)

    @attr('pos', 'rbac')
    def test_rbac_global_admin_enable_scheduled_images(self):
        """Rbac - Enable scheduled images for a valid server as global
        admin.

        1) Create a valid server instance
        2) Enable scheduled images using a valid retention value as global
        admin
        3) Verify that the response code is 200
        """

        tenant_id = self.config.images.tenant_id
        instance_id = self.servers[0].id
        retention = self.config.images.retention

        sch_img_obj = self.global_admin_img_prov.scheduled_images_client. \
            enable_scheduled_images(tenant_id, instance_id, retention)
        self.assertEquals(sch_img_obj.status_code, 200,
                          self.msg.format('status_code', 200,
                                          sch_img_obj.status_code))

    @attr('neg', 'rbac')
    def test_rbac_global_observer_enable_scheduled_images(self):
        """Rbac - Enable scheduled images for a valid server as
        global observer.

        1) Create a valid server instance
        2) Enable scheduled images using a valid retention value as global
        observer
        3) Verify that the response code is 403
        """

        tenant_id = self.config.images.tenant_id
        instance_id = self.servers[2].id
        retention = self.config.images.retention

        with self.assertRaises(Forbidden):
            self.global_observer_img_prov.scheduled_images_client. \
                enable_scheduled_images(tenant_id, instance_id, retention)

    @attr('pos', 'rbac')
    def test_rbac_enable_scheduled_images_already_admin(self):
        """Rbac - Enable scheduled images for a valid server when already
        enabled by admin.

        1) Create a valid server instance
        2) Enable scheduled images using a valid retention value as admin
        3) Verify that the response code is 200
        4) Enable scheduled images using a valid retention value as observer
        5) Verify that the response code is 403
        6) Enable scheduled images using a valid retention value as global
        observer
        7) Verify that the response code is 403
        8) Enable scheduled images using a valid retention value as creator
        9) Verify that the response code is 200
        10) Enable scheduled images using a valid retention value as admin
        11) Verify that the response code is 200
        12) Enable scheduled images using a valid retention value as global
        admin
        13) Verify that the response code is 200
        """

        tenant_id = self.config.images.tenant_id
        instance_id = self.servers[3].id
        retention = self.config.images.retention
        msg = Constants.MESSAGE

        sch_img_obj = self.images_provider.scheduled_images_client. \
            enable_scheduled_images(tenant_id, instance_id, retention)
        self.assertEquals(sch_img_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     sch_img_obj.status_code))

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

        # Check global admin
        sch_img_obj = self.global_admin_img_prov.scheduled_images_client. \
            enable_scheduled_images(tenant_id, instance_id, retention)
        self.assertEquals(sch_img_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     sch_img_obj.status_code))

    @attr('pos', 'rbac')
    def test_rbac_enable_scheduled_images_already_creator(self):
        """Rbac - Enable scheduled images for a valid server when already
        enabled by creator.

        1) Create a valid server instance
        2) Enable scheduled images using a valid retention value as creator
        3) Verify that the response code is 200
        4) Enable scheduled images using a valid retention value as observer
        5) Verify that the response code is 403
        6) Enable scheduled images using a valid retention value as global
        observer
        7) Verify that the response code is 403
        8) Enable scheduled images using a valid retention value as creator
        9) Verify that the response code is 200
        10) Enable scheduled images using a valid retention value as admin
        11) Verify that the response code is 200
        12) Enable scheduled images using a valid retention value as global
        admin
        13) Verify that the response code is 200
        """

        tenant_id = self.config.images.tenant_id
        instance_id = self.servers[4].id
        retention = self.config.images.retention
        msg = Constants.MESSAGE

        sch_img_obj = self.creator_images_provider.scheduled_images_client. \
            enable_scheduled_images(tenant_id, instance_id, retention)
        self.assertEquals(sch_img_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     sch_img_obj.status_code))

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

        # Check global admin
        sch_img_obj = self.global_admin_img_prov.scheduled_images_client. \
            enable_scheduled_images(tenant_id, instance_id, retention)
        self.assertEquals(sch_img_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     sch_img_obj.status_code))

    @attr('pos', 'rbac')
    def test_rbac_enable_scheduled_images_already_global_admin(self):
        """Rbac - Enable scheduled images for a valid server when already
        enabled by global admin.

        1) Create a valid server instance
        2) Enable scheduled images using a valid retention value as global
        admin
        3) Verify that the response code is 200
        4) Enable scheduled images using a valid retention value as observer
        5) Verify that the response code is 403
        6) Enable scheduled images using a valid retention value as global
        observer
        7) Verify that the response code is 403
        8) Enable scheduled images using a valid retention value as admin
        9) Verify that the response code is 200
        10) Enable scheduled images using a valid retention value as global
        admin
        11) Verify that the response code is 200
        12) Enable scheduled images using a valid retention value as creator
        13) Verify that the response code is 200
        """

        tenant_id = self.config.images.tenant_id
        instance_id = self.servers[4].id
        retention = self.config.images.retention
        msg = Constants.MESSAGE

        sch_img_obj = self.global_admin_img_prov.scheduled_images_client. \
            enable_scheduled_images(tenant_id, instance_id, retention)
        self.assertEquals(sch_img_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     sch_img_obj.status_code))

        # Check observer
        with self.assertRaises(Forbidden):
            self.observer_images_provider.scheduled_images_client. \
                enable_scheduled_images(tenant_id, instance_id, retention)

        # Check global observer
        with self.assertRaises(Forbidden):
            self.global_observer_img_prov.scheduled_images_client. \
                enable_scheduled_images(tenant_id, instance_id, retention)

        # Check admin
        sch_img_obj = self.images_provider.scheduled_images_client. \
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

        # Check creator
        sch_img_obj = self.creator_images_provider.scheduled_images_client. \
            enable_scheduled_images(tenant_id, instance_id, retention)
        self.assertEquals(sch_img_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     sch_img_obj.status_code))
