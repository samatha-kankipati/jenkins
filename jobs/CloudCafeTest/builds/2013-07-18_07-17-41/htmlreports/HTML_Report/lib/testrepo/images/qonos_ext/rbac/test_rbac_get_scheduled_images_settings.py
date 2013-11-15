from testrepo.common.testfixtures.images import RbacImagesFixture
from ccengine.common.decorators import attr
import ccengine.common.tools.datagen as datagen
from ccengine.common.exceptions.compute import Forbidden, ItemNotFound
from ccengine.domain.types import NovaServerStatusTypes


class TestRbacGetScheduledImagesSettings(RbacImagesFixture):

    @classmethod
    def setUpClass(self):
        """ Creates the server instances and snapshots used for all tests in
        this class.

        """

        super(TestRbacGetScheduledImagesSettings, self).setUpClass()

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

    @attr('positive', 'rbac')
    def test_rbac_get_scheduled_images_settings(self):
        """ Rbac - Get scheduled images settings for a valid server that has
        scheduled images enabled as admin.

        """

        """
        1) Create a valid server instance
        2) Enable scheduled images using a valid retention value as admin
        3) Verify that the response code is 200
        4) Get scheduled images settings for the instance as admin
        5) Verify that the response code is 200
        6) Verify that the response contains the entered retention value
        7) Get scheduled images settings for the instance as global admin
        8) Verify that the response code is 200
        9) Verify that the response contains the entered retention value
        10) Get scheduled images settings for the instance as creator
        11) Verify that the response code is 200
        12) Verify that the response contains the entered retention value
        13) Get scheduled images settings for the instance as observer
        14) Verify that the response code is 200
        15) Verify that the response contains the entered retention value
        16) Get scheduled images settings for the instance as global observer
        17) Verify that the response code is 200
        18) Verify that the response contains the entered retention value

        Attributes to verify:
            retention
        """

        tenant_id = self.tenant_id
        instance_id = self.servers[0].id
        retention = self.retention

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

        # this check fails when global observer is available in staging
        # Check global observer
        with self.assertRaises(Forbidden):
            self.global_observer_img_prov.scheduled_images_client. \
                get_scheduled_images_settings(tenant_id, instance_id)

    @attr('positive', 'rbac')
    def test_rbac_get_scheduled_images_settings_creator(self):
        """ Rbac - Get scheduled images settings for a valid server that has
        scheduled images enabled as creator.

        """

        """
        1) Create a valid server instance
        2) Enable scheduled images using a valid retention value as creator
        3) Verify that the response code is 200
        4) Get scheduled images settings for the instance as admin
        5) Verify that the response code is 200
        6) Verify that the response contains the entered retention value
        7) Get scheduled images settings for the instance as global admin
        8) Verify that the response code is 200
        9) Verify that the response contains the entered retention value
        10) Get scheduled images settings for the instance as creator
        11) Verify that the response code is 200
        12) Verify that the response contains the entered retention value
        13) Get scheduled images settings for the instance as observer
        14) Verify that the response code is 200
        15) Verify that the response contains the entered retention value
        16) Get scheduled images settings for the instance as global observer
        17) Verify that the response code is 200
        18) Verify that the response contains the entered retention value

        Attributes to verify:
            retention
        """

        tenant_id = self.tenant_id
        instance_id = self.servers[1].id
        retention = self.retention

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

        # this check fails when global observer is available in staging
        # Check global observer
        with self.assertRaises(Forbidden):
            self.global_observer_img_prov.scheduled_images_client. \
                get_scheduled_images_settings(tenant_id, instance_id)

    @attr('positive', 'rbac')
    def test_rbac_get_scheduled_images_settings_global_admin(self):
        """ Rbac - Get scheduled images settings for a valid server that has
        scheduled images enabled as global admin.

        """

        """
        1) Create a valid server instance
        2) Enable scheduled images using a valid retention value as global
        admin
        3) Verify that the response code is 200
        4) Get scheduled images settings for the instance as admin
        5) Verify that the response code is 200
        6) Verify that the response contains the entered retention value
        7) Get scheduled images settings for the instance as global admin
        8) Verify that the response code is 200
        9) Verify that the response contains the entered retention value
        10) Get scheduled images settings for the instance as creator
        11) Verify that the response code is 200
        12) Verify that the response contains the entered retention value
        13) Get scheduled images settings for the instance as observer
        14) Verify that the response code is 200
        15) Verify that the response contains the entered retention value
        16) Get scheduled images settings for the instance as global observer
        17) Verify that the response code is 200
        18) Verify that the response contains the entered retention value

        Attributes to verify:
            retention
        """

        tenant_id = self.tenant_id
        instance_id = self.servers[2].id
        retention = self.retention

        sch_img_obj = self.global_admin_img_prov.scheduled_images_client. \
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

        # this check fails when global observer is available in staging
        # Check global observer
        with self.assertRaises(Forbidden):
            self.global_observer_img_prov.scheduled_images_client. \
                get_scheduled_images_settings(tenant_id, instance_id)

    @attr('positive', 'rbac')
    def test_rbac_get_scheduled_images_settings_not_enabled(self):
        """ Rbac - Get scheduled images settings for a valid server that does
        not have scheduled images enabled.

        """

        """
        1) Create a valid server instance
        2) Get scheduled images settings for the instance as admin
        3) Verify that the response code is 404
        4) Get scheduled images settings for the instance as global admin
        5) Verify that the response code is 404
        6) Get scheduled images settings for the instance as creator
        7) Verify that the response code is 404
        8) Get scheduled images settings for the instance as observer
        9) Verify that the response code is 404
        10) Get scheduled images settings for the instance as global observer
        11) Verify that the response code is 404

        Attributes to verify:
            retention
        """

        tenant_id = self.tenant_id
        instance_id = self.servers[3].id

        # Check admin
        with self.assertRaises(ItemNotFound):
            self.images_provider.scheduled_images_client. \
                get_scheduled_images_settings(tenant_id, instance_id)

        # Check global admin
        with self.assertRaises(ItemNotFound):
            self.global_admin_img_prov.scheduled_images_client. \
                get_scheduled_images_settings(tenant_id, instance_id)

        # Check creator
        with self.assertRaises(ItemNotFound):
            self.creator_images_provider.scheduled_images_client. \
                get_scheduled_images_settings(tenant_id, instance_id)

        # Check observer
        with self.assertRaises(ItemNotFound):
            self.observer_images_provider.scheduled_images_client. \
                get_scheduled_images_settings(tenant_id, instance_id)

        # this check fails when global observer is available in staging
        # Check global observer
        with self.assertRaises(Forbidden):
            self.global_observer_img_prov.scheduled_images_client. \
                get_scheduled_images_settings(tenant_id, instance_id)

    @attr('positive', 'rbac')
    def test_rbac_get_scheduled_images_settings_enabled_disabled(self):
        """ Rbac - Get scheduled images settings for a valid server that has
        scheduled images enabled as admin then disabled by admin.

        """

        """
        1) Create a valid server instance
        2) Enable scheduled images using a valid retention value as admin
        3) Verify that the response code is 200
        4) Disable scheduled images as admin
        5) Verify that the response code is 202
        6) Get scheduled images settings for the instance as admin
        7) Verify that the response code is 200
        8) Verify that the response contains the entered retention value
        9) Get scheduled images settings for the instance as global admin
        10) Verify that the response code is 200
        11) Verify that the response contains the entered retention value
        12) Get scheduled images settings for the instance as creator
        13) Verify that the response code is 200
        14) Verify that the response contains the entered retention value
        15) Get scheduled images settings for the instance as observer
        16) Verify that the response code is 200
        17) Verify that the response contains the entered retention value
        18) Get scheduled images settings for the instance as global observer
        19) Verify that the response code is 200
        20) Verify that the response contains the entered retention value
        """

        tenant_id = self.tenant_id
        instance_id = self.servers[3].id
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

        # Check admin
        with self.assertRaises(ItemNotFound):
            self.images_provider.scheduled_images_client. \
                get_scheduled_images_settings(tenant_id, instance_id)

        # Check global admin
        with self.assertRaises(ItemNotFound):
            self.global_admin_img_prov.scheduled_images_client. \
                get_scheduled_images_settings(tenant_id, instance_id)

        # Check creator
        with self.assertRaises(ItemNotFound):
            self.creator_images_provider.scheduled_images_client. \
                get_scheduled_images_settings(tenant_id, instance_id)

        # Check observer
        with self.assertRaises(ItemNotFound):
            self.observer_images_provider.scheduled_images_client. \
                get_scheduled_images_settings(tenant_id, instance_id)

        # this check fails when global observer is available in staging
        # Check global observer
        with self.assertRaises(Forbidden):
            self.global_observer_img_prov.scheduled_images_client. \
                get_scheduled_images_settings(tenant_id, instance_id)

    @attr('positive', 'rbac')
    def test_rbac_get_scheduled_images_settings_creator_enabled_disabled(self):
        """ Rbac - Get scheduled images settings for a valid server that has
        scheduled images enabled as creator then disabled by global admin.

        """

        """
        1) Create a valid server instance
        2) Enable scheduled images using a valid retention value as creator
        3) Verify that the response code is 200
        4) Disable scheduled images as global admin
        5) Verify that the response code is 202
        6) Get scheduled images settings for the instance as admin
        7) Verify that the response code is 200
        8) Verify that the response contains the entered retention value
        9) Get scheduled images settings for the instance as global admin
        10) Verify that the response code is 200
        11) Verify that the response contains the entered retention value
        12) Get scheduled images settings for the instance as creator
        13) Verify that the response code is 200
        14) Verify that the response contains the entered retention value
        15) Get scheduled images settings for the instance as observer
        16) Verify that the response code is 200
        17) Verify that the response contains the entered retention value
        18) Get scheduled images settings for the instance as global observer
        19) Verify that the response code is 200
        20) Verify that the response contains the entered retention value
        """

        tenant_id = self.tenant_id
        instance_id = self.servers[4].id
        retention = self.retention

        sch_img_obj = self.creator_images_provider.scheduled_images_client. \
            enable_scheduled_images(tenant_id, instance_id, retention)
        self.assertEquals(sch_img_obj.status_code, 200,
                          self.msg.format('status_code', 200,
                                          sch_img_obj.status_code))

        dis_sch_img_obj = self.global_admin_img_prov. \
            scheduled_images_client.disable_scheduled_images(tenant_id,
                                                             instance_id)
        self.assertEquals(dis_sch_img_obj.status_code, 202,
                          self.msg.format('status_code', 202,
                                          dis_sch_img_obj.status_code))

        # Check admin
        with self.assertRaises(ItemNotFound):
            self.images_provider.scheduled_images_client. \
                get_scheduled_images_settings(tenant_id, instance_id)

        # Check global admin
        with self.assertRaises(ItemNotFound):
            self.global_admin_img_prov.scheduled_images_client. \
                get_scheduled_images_settings(tenant_id, instance_id)

        # Check creator
        with self.assertRaises(ItemNotFound):
            self.creator_images_provider.scheduled_images_client. \
                get_scheduled_images_settings(tenant_id, instance_id)

        # Check observer
        with self.assertRaises(ItemNotFound):
            self.observer_images_provider.scheduled_images_client. \
                get_scheduled_images_settings(tenant_id, instance_id)

        # this check fails when global observer is available in staging
        # Check global observer
        with self.assertRaises(Forbidden):
            self.global_observer_img_prov.scheduled_images_client. \
                get_scheduled_images_settings(tenant_id, instance_id)

    def _is_get_SI_settings_success(self, provider, instance_id):

        resp_obj = provider.scheduled_images_client. \
            get_scheduled_images_settings(self.tenant_id, instance_id)

        self.assertEquals(resp_obj.status_code, 200,
                          self.msg.format('status_code', 200,
                                          resp_obj.status_code))

        get_sch_img_resp = resp_obj.entity

        self.assertEquals(int(get_sch_img_resp.retention),
                          self.retention,
                          self.msg.format('retention', self.retention,
                                          get_sch_img_resp.retention))
