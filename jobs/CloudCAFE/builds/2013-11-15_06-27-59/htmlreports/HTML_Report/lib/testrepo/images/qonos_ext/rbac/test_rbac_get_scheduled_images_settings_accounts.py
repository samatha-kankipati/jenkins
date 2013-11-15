import ccengine.common.tools.datagen as datagen
from ccengine.common.constants.images_constants import Constants
from ccengine.common.decorators import attr
from ccengine.common.exceptions.compute import Unauthorized
from ccengine.domain.types import NovaServerStatusTypes
from testrepo.common.testfixtures.images import RbacImagesFixture


class TestRbacGetScheduledImagesSettingsAccounts(RbacImagesFixture):

    @classmethod
    def setUpClass(self):
        """Creates the server instances and snapshots used for all tests in
        this class.
        """

        super(TestRbacGetScheduledImagesSettingsAccounts, self).setUpClass()

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
    def test_rbac_get_scheduled_images_settings_diff_account(self):
        """Rbac - Get scheduled images settings for a valid server that
        belongs to a different customer's account.

        1) Create a valid server instance
        2) Enable scheduled images using a valid retention value as admin
        3) Verify that the response code is 200
        4) Get scheduled images settings for the instance as admin of different
            account
        5) Verify that the response code is 401
        6) Get scheduled images settings for the instance as global admin of
        different account
        7) Verify that the response code is 401
        8) Get scheduled images settings for the instance as creator of
            different account
        9) Verify that the response code is 401
        10) Get scheduled images settings for the instance as observer of
            different account
        11) Verify that the response code is 401
        12) Get scheduled images settings for the instance as global observer
        of different account
        13) Verify that the response code is 401
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
                get_scheduled_images_settings(tenant_id, instance_id)

        # Check diff global admin
        with self.assertRaises(Unauthorized):
            self.diff_global_admin_img_prov.scheduled_images_client. \
                get_scheduled_images_settings(tenant_id, instance_id)

        # Check diff creator
        with self.assertRaises(Unauthorized):
            self.diff_creator_img_prov.scheduled_images_client. \
                get_scheduled_images_settings(tenant_id, instance_id)

        # Check diff observer
        with self.assertRaises(Unauthorized):
            self.diff_observer_img_prov.scheduled_images_client. \
                get_scheduled_images_settings(tenant_id, instance_id)

        # Check diff global observer
        with self.assertRaises(Unauthorized):
            self.diff_glbl_obsrvr_img_prov.scheduled_images_client. \
                get_scheduled_images_settings(tenant_id, instance_id)

    @attr('pos', 'rbac')
    def test_rbac_get_scheduled_images_settings_alt_observer_account(self):
        """Rbac - Get scheduled images settings for a valid server as an
        alternate observer account.

        1) Create a valid server instance
        2) Enable scheduled images using a valid retention value as admin
        3) Verify that the response code is 200
        4) Get scheduled images settings for the instance as observer
        5) Verify that the response code is 200
        6) Verify that the response contains the entered retention value
        7) Get scheduled images settings for the instance as alternate observer
        8) Verify that the response code is 200
        9) Verify that the response contains the entered retention value
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

        sch_img = sch_img_obj.entity

        # Check observer
        get_sch_img_settings_obj = \
            self.observer_images_provider.scheduled_images_client. \
            get_scheduled_images_settings(tenant_id, instance_id)
        self.assertEquals(get_sch_img_settings_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     get_sch_img_settings_obj.status_code))

        get_sch_img_settings = get_sch_img_settings_obj.entity

        self.assertEquals(get_sch_img_settings.retention,
                          sch_img.retention,
                          msg.format('retention', sch_img.retention,
                                     get_sch_img_settings.retention))

        # Check alt observer
        get_sch_img_settings_obj = \
            self.alt_observer_img_prov.scheduled_images_client. \
            get_scheduled_images_settings(tenant_id, instance_id)
        self.assertEquals(get_sch_img_settings_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     get_sch_img_settings_obj.status_code))

        get_sch_img_settings = get_sch_img_settings_obj.entity

        self.assertEquals(get_sch_img_settings.retention,
                          sch_img.retention,
                          msg.format('retention', sch_img.retention,
                                     get_sch_img_settings.retention))
