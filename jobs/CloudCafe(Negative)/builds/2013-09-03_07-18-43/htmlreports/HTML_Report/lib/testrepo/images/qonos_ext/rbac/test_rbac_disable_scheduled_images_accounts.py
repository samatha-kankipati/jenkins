from testrepo.common.testfixtures.images import RbacImagesFixture
from ccengine.common.constants.images_constants import Constants
from ccengine.common.decorators import attr
import ccengine.common.tools.datagen as datagen
from ccengine.common.exceptions.compute import Unauthorized
from ccengine.domain.types import NovaServerStatusTypes


class TestRbacDisableScheduledImagesAccounts(RbacImagesFixture):

    @classmethod
    def setUpClass(self):
        """ Creates the server instances and snapshots used for all tests in
        this class.

        """

        super(TestRbacDisableScheduledImagesAccounts, self).setUpClass()

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

    '''TODO: Test will fail when RM bug #774 is fixed'''
    @attr('negative', 'rbac')
    def test_rbac_disable_scheduled_images_diff_account(self):
        """ Rbac - Disable scheduled images for a valid server that belongs to
        a different customer's account.

        """

        """
        1) Create a valid server instance
        2) Enable scheduled images using a valid retention value as admin
        3) Verify that the response code is 200
        4) Disable scheduled images using a valid retention value as admin of
            different account
        5) Verify that the response code is 401
        6) Disable scheduled images using a valid retention value as creator of
            different account
        7) Verify that the response code is 401
        8) Disable scheduled images using a valid retention value as observer of
            different account
        9) Verify that the response code is 401
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

        # Check diff admin
        with self.assertRaises(Unauthorized):
            self.diff_admin_img_prov.scheduled_images_client. \
            disable_scheduled_images(tenant_id, instance_id)

        # Check diff creator
        with self.assertRaises(Unauthorized):
            self.diff_creator_img_prov.scheduled_images_client. \
            disable_scheduled_images(tenant_id, instance_id)

        # Check diff observer
        with self.assertRaises(Unauthorized):
            self.diff_observer_img_prov.scheduled_images_client. \
            disable_scheduled_images(tenant_id, instance_id)

    @attr('postive', 'rbac')
    def test_rbac_disable_enable_disable_scheduled_images_alt_account(self):
        """ Rbac - Enable scheduled images for a valid server as admin then
        disable as an alternate admin of the same account then enable again as
        the first admin.

        """

        """
        1) Create a valid server instance
        2) Enable scheduled images using a valid retention value as admin
        3) Verify that the response code is 200
        4) Disable scheduled images using a valid retention value as alternate
            admin
        5) Verify that the response code is 202
        6) Enable scheduled images using a valid retention value as primary
            admin again
        7) Verify that the response code is 200
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

        dis_sch_img_obj = self.alt_admin_img_prov.scheduled_images_client. \
            disable_scheduled_images(tenant_id, instance_id)
        self.assertEquals(dis_sch_img_obj.status_code, 202,
                          msg.format('status_code', 202,
                                     dis_sch_img_obj.status_code))

        sch_img_obj = self.images_provider.scheduled_images_client. \
            enable_scheduled_images(tenant_id, instance_id, retention)
        self.assertEquals(sch_img_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     sch_img_obj.status_code))

    @attr('postive', 'rbac')
    def test_rbac_disable_enable_disable_scheduled_images_alt_account_2(self):
        """ Rbac - Enable scheduled images for a valid server as admin then
        disable as an alternate admin of the same account then enable again as
        the alternate admin.

        """

        """
        1) Create a valid server instance
        2) Enable scheduled images using a valid retention value as admin
        3) Verify that the response code is 200
        4) Disable scheduled images using a valid retention value as alternate
            admin
        5) Verify that the response code is 202
        6) Enable scheduled images using a valid retention value as alternate
            admin again
        7) Verify that the response code is 200
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

        dis_sch_img_obj = self.alt_admin_img_prov.scheduled_images_client. \
            disable_scheduled_images(tenant_id, instance_id)
        self.assertEquals(dis_sch_img_obj.status_code, 202,
                          msg.format('status_code', 202,
                                     dis_sch_img_obj.status_code))

        sch_img_obj = self.alt_admin_img_prov.scheduled_images_client. \
            enable_scheduled_images(tenant_id, instance_id, retention)
        self.assertEquals(sch_img_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     sch_img_obj.status_code))
