import ccengine.common.tools.datagen as datagen
from ccengine.common.decorators import attr
from ccengine.domain.types import NovaServerStatusTypes
from testrepo.common.testfixtures.images import RbacImagesFixture


class TestRbacGetScheduledImagesSettingsToggle(RbacImagesFixture):

    @classmethod
    def setUpClass(self):
        """Creates the server instances and snapshots used for all tests in
        this class.
        """

        super(TestRbacGetScheduledImagesSettingsToggle, self).setUpClass()

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

    def _is_get_SI_settings_success(self, provider, instance_id):
        """Verifies that the response and retention are as expected."""

        resp_obj = provider.scheduled_images_client. \
            get_scheduled_images_settings(self.tenant_id, instance_id)
        self.assertEquals(resp_obj.status_code, 200,
                          self.msg.format('status_code', 200,
                                          resp_obj.status_code))

        get_sch_img_settings = resp_obj.entity

        self.assertEquals(int(get_sch_img_settings.retention), self.retention,
                          self.msg.format('retention', self.retention,
                                          get_sch_img_settings.retention))

    @attr('pos', 'rbac')
    def test_rbac_get_scheduled_images_settings_enabled_disabled_enabled(self):
        """Rbac - Get scheduled images settings for a valid server that has
        scheduled images enabled as admin then disabled by admin then enabled
        again by admin.

        1) Create a valid server instance
        2) Enable scheduled images using a valid retention value as admin
        3) Verify that the response code is 200
        4) Disable scheduled images as admin
        5) Verify that the response code is 202
        6) Enable scheduled images using a valid retention value as admin again
        7) Verify that the response code is 200
        8) Get scheduled images settings for the instance as admin
        9) Verify that the response code is 200
        10) Verify that the response contains the entered retention value
        11) Get scheduled images settings for the instance as global admin
        12) Verify that the response code is 200
        13) Verify that the response contains the entered retention value
        14) Get scheduled images settings for the instance as creator
        15) Verify that the response code is 200
        16) Verify that the response contains the entered retention value
        17) Get scheduled images settings for the instance as observer
        18) Verify that the response code is 200
        19) Verify that the response contains the entered retention value
        20) Get scheduled images settings for the instance as global observer
        21) Verify that the response code is 200
        22) Verify that the response contains the entered retention value
        """

        tenant_id = self.tenant_id
        instance_id = self.servers[0].id
        retention = self.retention

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

        sch_img_obj = self.images_provider.scheduled_images_client. \
            enable_scheduled_images(tenant_id, instance_id, retention)
        self.assertEquals(sch_img_obj.status_code, 200,
                          self.msg.format('status_code', 200,
                                          sch_img_obj.status_code))

        # Check admin
        self._is_get_SI_settings_success(self.images_provider, instance_id)

        # Check global admin
        self._is_get_SI_settings_success(self.global_admin_img_prov,
                                         instance_id)

        # Check creator
        self._is_get_SI_settings_success(self.creator_images_provider,
                                         instance_id)

        # Check observer
        self._is_get_SI_settings_success(self.observer_images_provider,
                                         instance_id)

        # Check global observer
        self._is_get_SI_settings_success(self.global_observer_img_prov,
                                         instance_id)

    @attr('pos', 'rbac')
    def test_rbac_get_scheduled_images_settings_en_dis_creator_en(self):
        """Rbac - Get scheduled images settings for a valid server that has
        scheduled images enabled as admin then disabled by admin then enabled
        again by creator.

        1) Create a valid server instance
        2) Enable scheduled images using a valid retention value as admin
        3) Verify that the response code is 200
        4) Disable scheduled images as admin
        5) Verify that the response code is 202
        6) Enable scheduled images using a valid retention value as creator
            again
        7) Verify that the response code is 200
        8) Get scheduled images settings for the instance as admin
        9) Verify that the response code is 200
        10) Verify that the response contains the entered retention value
        11) Get scheduled images settings for the instance as global admin
        12) Verify that the response code is 200
        13) Verify that the response contains the entered retention value
        14) Get scheduled images settings for the instance as creator
        15) Verify that the response code is 200
        16) Verify that the response contains the entered retention value
        17) Get scheduled images settings for the instance as observer
        18) Verify that the response code is 200
        19) Verify that the response contains the entered retention value
        20) Get scheduled images settings for the instance as global observer
        21) Verify that the response code is 200
        22) Verify that the response contains the entered retention value
        """

        tenant_id = self.tenant_id
        instance_id = self.servers[1].id
        retention = self.retention

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

        sch_img_obj = self.creator_images_provider.scheduled_images_client. \
            enable_scheduled_images(tenant_id, instance_id, retention)
        self.assertEquals(sch_img_obj.status_code, 200,
                          self.msg.format('status_code', 200,
                                          sch_img_obj.status_code))

        # Check admin
        self._is_get_SI_settings_success(self.images_provider, instance_id)

        # Check global admin
        self._is_get_SI_settings_success(self.global_admin_img_prov,
                                         instance_id)

        # Check creator
        self._is_get_SI_settings_success(self.creator_images_provider,
                                         instance_id)

        # Check observer
        self._is_get_SI_settings_success(self.observer_images_provider,
                                         instance_id)

        # Check global observer
        self._is_get_SI_settings_success(self.global_observer_img_prov,
                                         instance_id)

    @attr('pos', 'rbac')
    def test_rbac_get_scheduled_images_settings_creator_en_dis_en(self):
        """Rbac - Get scheduled images settings for a valid server that has
        scheduled images enabled as creator then disabled by admin then enabled
        again by admin.

        1) Create a valid server instance
        2) Enable scheduled images using a valid retention value as creator
        3) Verify that the response code is 200
        4) Disable scheduled images as admin
        5) Verify that the response code is 202
        6) Enable scheduled images using a valid retention value as admin again
        7) Verify that the response code is 200
        8) Get scheduled images settings for the instance as admin
        9) Verify that the response code is 200
        10) Verify that the response contains the entered retention value
        11) Get scheduled images settings for the instance as global admin
        12) Verify that the response code is 200
        13) Verify that the response contains the entered retention value
        14) Get scheduled images settings for the instance as creator
        15) Verify that the response code is 200
        16) Verify that the response contains the entered retention value
        17) Get scheduled images settings for the instance as observer
        18) Verify that the response code is 200
        19) Verify that the response contains the entered retention value
        20) Get scheduled images settings for the instance as global observer
        21) Verify that the response code is 200
        22) Verify that the response contains the entered retention value
        """

        tenant_id = self.tenant_id
        instance_id = self.servers[2].id
        retention = self.retention

        sch_img_obj = self.creator_images_provider.scheduled_images_client. \
            enable_scheduled_images(tenant_id, instance_id, retention)
        self.assertEquals(sch_img_obj.status_code, 200,
                          self.msg.format('status_code', 200,
                                          sch_img_obj.status_code))

        dis_sch_img_obj = self.images_provider.scheduled_images_client. \
            disable_scheduled_images(tenant_id, instance_id)
        self.assertEquals(dis_sch_img_obj.status_code, 202,
                          self.msg.format('status_code', 202,
                                          dis_sch_img_obj.status_code))

        sch_img_obj = self.images_provider.scheduled_images_client. \
            enable_scheduled_images(tenant_id, instance_id, retention)
        self.assertEquals(sch_img_obj.status_code, 200,
                          self.msg.format('status_code', 200,
                                          sch_img_obj.status_code))

        # Check admin
        self._is_get_SI_settings_success(self.images_provider, instance_id)

        # Check global admin
        self._is_get_SI_settings_success(self.global_admin_img_prov,
                                         instance_id)

        # Check creator
        self._is_get_SI_settings_success(self.creator_images_provider,
                                         instance_id)

        # Check observer
        self._is_get_SI_settings_success(self.observer_images_provider,
                                         instance_id)

        # Check global observer
        self._is_get_SI_settings_success(self.global_observer_img_prov,
                                         instance_id)

    @attr('pos', 'rbac')
    def test_rbac_get_scheduled_images_setting_creator_en_dis_creator_en(self):
        """Rbac - Get scheduled images settings for a valid server that has
        scheduled images enabled as creator then disabled by admin then enabled
        again by creator.

        1) Create a valid server instance
        2) Enable scheduled images using a valid retention value as creator
        3) Verify that the response code is 200
        4) Disable scheduled images as admin
        5) Verify that the response code is 202
        6) Enable scheduled images using a valid retention value as creator
            again
        7) Verify that the response code is 200
        8) Get scheduled images settings for the instance as admin
        9) Verify that the response code is 200
        10) Verify that the response contains the entered retention value
        11) Get scheduled images settings for the instance as global admin
        12) Verify that the response code is 200
        13) Verify that the response contains the entered retention value
        14) Get scheduled images settings for the instance as creator
        15) Verify that the response code is 200
        16) Verify that the response contains the entered retention value
        17) Get scheduled images settings for the instance as observer
        18) Verify that the response code is 200
        19) Verify that the response contains the entered retention value
        20) Get scheduled images settings for the instance as global observer
        21) Verify that the response code is 200
        22) Verify that the response contains the entered retention value
        """

        tenant_id = self.tenant_id
        instance_id = self.servers[3].id
        retention = self.retention

        sch_img_obj = self.creator_images_provider.scheduled_images_client. \
            enable_scheduled_images(tenant_id, instance_id, retention)
        self.assertEquals(sch_img_obj.status_code, 200,
                          self.msg.format('status_code', 200,
                                          sch_img_obj.status_code))

        dis_sch_img_obj = self.images_provider.scheduled_images_client. \
            disable_scheduled_images(tenant_id, instance_id)
        self.assertEquals(dis_sch_img_obj.status_code, 202,
                          self.msg.format('status_code', 202,
                                          dis_sch_img_obj.status_code))

        sch_img_obj = self.creator_images_provider.scheduled_images_client. \
            enable_scheduled_images(tenant_id, instance_id, retention)
        self.assertEquals(sch_img_obj.status_code, 200,
                          self.msg.format('status_code', 200,
                                          sch_img_obj.status_code))

        # Check admin
        self._is_get_SI_settings_success(self.images_provider, instance_id)

        # Check global admin
        self._is_get_SI_settings_success(self.global_admin_img_prov,
                                         instance_id)

        # Check creator
        self._is_get_SI_settings_success(self.creator_images_provider,
                                         instance_id)

        # Check observer
        self._is_get_SI_settings_success(self.observer_images_provider,
                                         instance_id)

        # Check global observer
        self._is_get_SI_settings_success(self.global_observer_img_prov,
                                         instance_id)

    @attr('pos', 'rbac')
    def test_rbac_get_si_settings_global_admin_enabled_disabled_enabled(self):
        """Rbac - Get scheduled images settings for a valid server that has
        scheduled images enabled as global admin then disabled by global admin
        then enabled again by global admin.

        1) Create a valid server instance
        2) Enable scheduled images using a valid retention value as global
        admin
        3) Verify that the response code is 200
        4) Disable scheduled images as global admin
        5) Verify that the response code is 202
        6) Enable scheduled images using a valid retention value as global
        admin again
        7) Verify that the response code is 200
        8) Get scheduled images settings for the instance as admin
        9) Verify that the response code is 200
        10) Verify that the response contains the entered retention value
        11) Get scheduled images settings for the instance as global admin
        12) Verify that the response code is 200
        13) Verify that the response contains the entered retention value
        14) Get scheduled images settings for the instance as creator
        15) Verify that the response code is 200
        16) Verify that the response contains the entered retention value
        17) Get scheduled images settings for the instance as observer
        18) Verify that the response code is 200
        19) Verify that the response contains the entered retention value
        20) Get scheduled images settings for the instance as global observer
        21) Verify that the response code is 200
        22) Verify that the response contains the entered retention value
        """

        tenant_id = self.tenant_id
        instance_id = self.servers[4].id
        retention = self.retention

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

        sch_img_obj = self.images_provider.scheduled_images_client. \
            enable_scheduled_images(tenant_id, instance_id, retention)
        self.assertEquals(sch_img_obj.status_code, 200,
                          self.msg.format('status_code', 200,
                                          sch_img_obj.status_code))

        # Check admin
        self._is_get_SI_settings_success(self.images_provider, instance_id)

        # Check global admin
        self._is_get_SI_settings_success(self.global_admin_img_prov,
                                         instance_id)

        # Check creator
        self._is_get_SI_settings_success(self.creator_images_provider,
                                         instance_id)

        # Check observer
        self._is_get_SI_settings_success(self.observer_images_provider,
                                         instance_id)

        # Check global observer
        self._is_get_SI_settings_success(self.global_observer_img_prov,
                                         instance_id)
