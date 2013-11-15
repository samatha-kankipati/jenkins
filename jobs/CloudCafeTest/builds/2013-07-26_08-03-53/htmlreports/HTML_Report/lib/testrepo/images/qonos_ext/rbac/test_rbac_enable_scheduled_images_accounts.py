from testrepo.common.testfixtures.images import RbacImagesFixture
from ccengine.common.constants.images_constants import Constants
from ccengine.common.decorators import attr
import ccengine.common.tools.datagen as datagen
from ccengine.common.exceptions.compute import Unauthorized
from ccengine.domain.types import NovaServerStatusTypes


class TestRbacEnableScheduledImagesAccounts(RbacImagesFixture):

    @classmethod
    def setUpClass(self):
        """ Creates the server instances and snapshots used for all tests in
        this class.

        """

        super(TestRbacEnableScheduledImagesAccounts, self).setUpClass()

        count = 2
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

    '''TODO: Test will fail when RM bug #774 is fixed'''
    @attr('neg', 'rbac')
    def test_rbac_enable_scheduled_images_diff_account(self):
        """ Rbac - Enable scheduled images for a valid server that belongs to
        a different customer's account.

        """

        """
        1) Create a valid server instance
        2) Enable scheduled images using a valid retention value as admin of
        different account
        3) Verify that the response code is 401
        4) Enable scheduled images using a valid retention value as global
        admin of different account
        5) Verify that the response code is 401
        6) Enable scheduled images using a valid retention value as creator of
        different account
        7) Verify that the response code is 401
        8) Enable scheduled images using a valid retention value as observer of
        different account
        9) Verify that the response code is 401
        10) Enable scheduled images using a valid retention value as global
        observer of different account
        11) Verify that the response code is 401
        """

        tenant_id = self.config.images.tenant_id
        instance_id = self.servers[0].id
        retention = self.config.images.retention

        # Check diff admin
        with self.assertRaises(Unauthorized):
            self.diff_admin_img_prov.scheduled_images_client. \
            enable_scheduled_images(tenant_id, instance_id, retention)

        # Check diff global admin
        with self.assertRaises(Unauthorized):
            self.diff_global_admin_img_prov.scheduled_images_client. \
            enable_scheduled_images(tenant_id, instance_id, retention)

        # Check diff creator
        with self.assertRaises(Unauthorized):
            self.diff_creator_img_prov.scheduled_images_client. \
            enable_scheduled_images(tenant_id, instance_id, retention)

        # Check diff observer
        with self.assertRaises(Unauthorized):
            self.diff_observer_img_prov.scheduled_images_client. \
            enable_scheduled_images(tenant_id, instance_id, retention)

        # Check diff global observer
        with self.assertRaises(Unauthorized):
            self.diff_global_observer_img_prov.scheduled_images_client. \
            enable_scheduled_images(tenant_id, instance_id, retention)

    @attr('pos', 'rbac')
    def test_rbac_enable_scheduled_images_alt_creator_account(self):
        """ Rbac - Enable scheduled images for a valid server that belongs to
        an alternate creator account.

        """

        """
        1) Create a valid server instance
        2) Enable scheduled images using a valid retention value as creator
        3) Verify that the response code is 200
        4) Disable scheduled images
        5) Enable scheduled images using a valid retention value as alternate
            creator
        6) Verify that the response code is 200
        """

        tenant_id = self.config.images.tenant_id
        instance_id = self.servers[1].id
        retention = self.config.images.retention
        msg = Constants.MESSAGE

        # Check creator
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

        # Check alt creator
        sch_img_obj = self.alt_creator_img_prov.scheduled_images_client. \
            enable_scheduled_images(tenant_id, instance_id, retention)
        self.assertEquals(sch_img_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     sch_img_obj.status_code))
