from testrepo.common.testfixtures.images import RbacImagesFixture
from ccengine.common.constants.images_constants import Constants
from ccengine.common.decorators import attr
import ccengine.common.tools.datagen as datagen
from ccengine.common.exceptions.compute import Forbidden, ItemNotFound
from ccengine.domain.types import NovaServerStatusTypes


class TestRbacDisableScheduledImagesToggle(RbacImagesFixture):

    @classmethod
    def setUpClass(self):
        """ Creates the server instances and snapshots used for all tests in
        this class.

        """

        super(TestRbacDisableScheduledImagesToggle, self).setUpClass()

        count = 3
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

    @attr('positive', 'rbac')
    def test_rbac_admin_enable_disable_disable_scheduled_images(self):
        """ Rbac - Enable scheduled images for a valid server as admin then
        disable as admin then disable again.

        """

        """
        1) Create a valid server instance
        2) Enable scheduled images using a valid retention value as admin
        3) Verify that the response code is 200
        4) Disable scheduled images as admin
        5) Verify that the response code is 202
        6) Disable scheduled images as creator again
        7) Verify that the response code is 403
        8) Disable scheduled images as observer again
        9) Verify that the response code is 403
        10) Disable scheduled images as global observer again
        11) Verify that the response code is 403
        12) Disable scheduled images as admin again
        13) Verify that the response code is 404
        14) Disable scheduled images as global admin again
        15) Verify that the response code is 404
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

    @attr('positive', 'rbac')
    def test_rbac_creator_enable_disable_disable_scheduled_images(self):
        """ Rbac - Enable scheduled images for a valid server as creator then
        disable as admin then disable again.

        """

        """
        1) Create a valid server instance
        2) Enable scheduled images using a valid retention value as creator
        3) Verify that the response code is 200
        4) Disable scheduled images as admin
        5) Verify that the response code is 202
        6) Disable scheduled images as creator again
        7) Verify that the response code is 403
        8) Disable scheduled images as observer again
        9) Verify that the response code is 403
        10) Disable scheduled images as observer again
        11) Verify that the response code is 403
        12) Disable scheduled images as admin again
        13) Verify that the response code is 404
        14) Disable scheduled images as global admin again
        15) Verify that the response code is 404
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

    @attr('positive', 'rbac')
    def test_rbac_global_admin_enable_disable_disable_scheduled_images(self):
        """ Rbac - Enable scheduled images for a valid server as global admin
        then disable as global admin then disable again.

        """

        """
        1) Create a valid server instance
        2) Enable scheduled images using a valid retention value as global
        admin
        3) Verify that the response code is 200
        4) Disable scheduled images as global admin
        5) Verify that the response code is 202
        6) Disable scheduled images as creator again
        7) Verify that the response code is 403
        8) Disable scheduled images as observer again
        9) Verify that the response code is 403
        10) Disable scheduled images as global observer again
        11) Verify that the response code is 403
        12) Disable scheduled images as admin again
        13) Verify that the response code is 404
        14) Disable scheduled images as global admin again
        15) Verify that the response code is 404
        """

        tenant_id = self.config.images.tenant_id
        instance_id = self.servers[2].id
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
