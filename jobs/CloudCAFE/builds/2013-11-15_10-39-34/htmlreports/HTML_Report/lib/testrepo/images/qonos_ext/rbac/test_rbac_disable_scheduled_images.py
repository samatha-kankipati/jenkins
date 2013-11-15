import ccengine.common.tools.datagen as datagen
from ccengine.common.constants.images_constants import Constants
from ccengine.common.decorators import attr
from ccengine.common.exceptions.compute import Forbidden, ItemNotFound
from ccengine.domain.types import NovaServerStatusTypes
from testrepo.common.testfixtures.images import RbacImagesFixture


class TestRbacDisableScheduledImages(RbacImagesFixture):

    @classmethod
    def setUpClass(self):
        """Creates the server instances and snapshots used for all tests in
        this class.
        """

        super(TestRbacDisableScheduledImages, self).setUpClass()

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
    def test_rbac_disable_scheduled_images_when_not_enabled(self):
        """Rbac - Disable scheduled images for a valid server when not
        enabled.

        1) Create a valid server instance
        2) Disable scheduled images as creator
        3) Verify that the response code is 403
        4) Disable scheduled images as observer
        5) Verify that the response code is 403
        6) Disable scheduled images as global observer
        7) Verify that the response code is 403
        8) Disable scheduled images as admin
        9) Verify that the response code is 404
        10) Disable scheduled images as global admin
        11) Verify that the response code is 404
        """

        tenant_id = self.config.images.tenant_id
        instance_id = self.servers[0].id

        # Check creator
        with self.assertRaises(Forbidden):
            self.creator_images_provider.scheduled_images_client. \
                disable_scheduled_images(tenant_id, instance_id)

        # Check observer
        with self.assertRaises(Forbidden):
            self.observer_images_provider.scheduled_images_client. \
                disable_scheduled_images(tenant_id, instance_id)

        # Check global observer
        with self.assertRaises(Forbidden):
            self.global_observer_img_prov.scheduled_images_client. \
                disable_scheduled_images(tenant_id, instance_id)

        # Check admin
        with self.assertRaises(ItemNotFound):
            self.images_provider.scheduled_images_client. \
                disable_scheduled_images(tenant_id, instance_id)

        # Check global admin
        with self.assertRaises(ItemNotFound):
            self.global_admin_img_prov.scheduled_images_client. \
                disable_scheduled_images(tenant_id, instance_id)

    @attr('pos', 'rbac')
    def test_rbac_disable_scheduled_images(self):
        """Rbac - Disable scheduled images for a valid server.

        1) Create a valid server instance
        2) Enable scheduled images using a valid retention value as admin
        3) Verify that the response code is 200
        4) Disable scheduled images as creator
        5) Verify that the response code is 403
        6) Disable scheduled images as observer
        7) Verify that the response code is 403
        8) Disable scheduled images as global observer
        9) Verify that the response code is 403
        10) Disable scheduled images as global admin
        11) Verify that the response code is 202
        """

        tenant_id = self.config.images.tenant_id
        instance_id = self.servers[1].id
        retention = self.config.images.retention
        msg = Constants.MESSAGE

        sch_img_obj = self.images_provider.scheduled_images_client. \
            enable_scheduled_images(tenant_id, instance_id, retention)
        self.assertEquals(sch_img_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     sch_img_obj.status_code))

        # Check creator
        with self.assertRaises(Forbidden):
            self.creator_images_provider.scheduled_images_client. \
                disable_scheduled_images(tenant_id, instance_id)

        # Check observer
        with self.assertRaises(Forbidden):
            self.observer_images_provider.scheduled_images_client. \
                disable_scheduled_images(tenant_id, instance_id)

        # Check global observer
        with self.assertRaises(Forbidden):
            self.global_observer_img_prov.scheduled_images_client. \
                disable_scheduled_images(tenant_id, instance_id)

        # Check global admin
        dis_sch_img_obj = self.global_admin_img_prov.scheduled_images_client. \
            disable_scheduled_images(tenant_id, instance_id)
        self.assertEquals(dis_sch_img_obj.status_code, 202,
                          msg.format('status_code', 202,
                                     dis_sch_img_obj.status_code))

    @attr('pos', 'rbac')
    def test_rbac_disable_scheduled_images_enabled_by_creator(self):
        """Rbac - Disable scheduled images for a valid server when enabled by
        creator.

        1) Create a valid server instance
        2) Enable scheduled images using a valid retention value as creator
        3) Verify that the response code is 200
        4) Disable scheduled images as creator
        5) Verify that the response code is 403
        6) Disable scheduled images as observer
        7) Verify that the response code is 403
        8) Disable scheduled images as global observer
        9) Verify that the response code is 403
        10) Disable scheduled images as admin
        11) Verify that the response code is 202
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

        # Check creator
        with self.assertRaises(Forbidden):
            self.creator_images_provider.scheduled_images_client. \
                disable_scheduled_images(tenant_id, instance_id)

        # Check observer
        with self.assertRaises(Forbidden):
            self.observer_images_provider.scheduled_images_client. \
                disable_scheduled_images(tenant_id, instance_id)

        # Check global observer
        with self.assertRaises(Forbidden):
            self.global_observer_img_prov.scheduled_images_client. \
                disable_scheduled_images(tenant_id, instance_id)

        # Check admin
        dis_sch_img_obj = self.images_provider.scheduled_images_client. \
            disable_scheduled_images(tenant_id, instance_id)
        self.assertEquals(dis_sch_img_obj.status_code, 202,
                          msg.format('status_code', 202,
                                     dis_sch_img_obj.status_code))

    @attr('pos', 'rbac')
    def test_rbac_disable_scheduled_images_enabled_by_global_admin(self):
        """Rbac - Disable scheduled images for a valid server when enabled by
        global admin.

        1) Create a valid server instance
        2) Enable scheduled images using a valid retention value as global
        admin
        3) Verify that the response code is 200
        4) Disable scheduled images as creator
        5) Verify that the response code is 403
        6) Disable scheduled images as observer
        7) Verify that the response code is 403
        8) Disable scheduled images as global observer
        9) Verify that the response code is 403
        10) Disable scheduled images as admin
        11) Verify that the response code is 202
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

        # Check creator
        with self.assertRaises(Forbidden):
            self.creator_images_provider.scheduled_images_client. \
                disable_scheduled_images(tenant_id, instance_id)

        # Check observer
        with self.assertRaises(Forbidden):
            self.observer_images_provider.scheduled_images_client. \
                disable_scheduled_images(tenant_id, instance_id)

        # Check global observer
        with self.assertRaises(Forbidden):
            self.global_observer_img_prov.scheduled_images_client. \
                disable_scheduled_images(tenant_id, instance_id)

        # Check admin
        dis_sch_img_obj = self.images_provider.scheduled_images_client. \
            disable_scheduled_images(tenant_id, instance_id)
        self.assertEquals(dis_sch_img_obj.status_code, 202,
                          msg.format('status_code', 202,
                                     dis_sch_img_obj.status_code))
