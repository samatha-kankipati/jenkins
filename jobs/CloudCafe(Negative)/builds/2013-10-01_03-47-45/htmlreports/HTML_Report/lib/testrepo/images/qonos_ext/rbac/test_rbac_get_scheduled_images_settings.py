from testrepo.common.testfixtures.images import RbacImagesFixture
from ccengine.common.constants.images_constants import Constants
from ccengine.common.decorators import attr
import ccengine.common.tools.datagen as datagen
from ccengine.common.exceptions.compute import ItemNotFound
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
        7) Get scheduled images settings for the instance as creator
        8) Verify that the response code is 200
        9) Verify that the response contains the entered retention value
        10) Get scheduled images settings for the instance as observer
        11) Verify that the response code is 200
        12) Verify that the response contains the entered retention value

        Attributes to verify:
            retention
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

        sch_img = sch_img_obj.entity

        # Check admin
        get_sch_img_settings_obj = \
            self.images_provider.scheduled_images_client. \
                get_scheduled_images_settings(tenant_id, instance_id)
        self.assertEquals(get_sch_img_settings_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     get_sch_img_settings_obj.status_code))

        get_sch_img_settings = get_sch_img_settings_obj.entity

        self.assertEquals(get_sch_img_settings.retention,
                          sch_img.retention,
                          msg.format('retention', sch_img.retention,
                                     get_sch_img_settings.retention))

        # Check creator
        get_sch_img_settings_obj = \
            self.creator_images_provider.scheduled_images_client. \
                get_scheduled_images_settings(tenant_id, instance_id)
        self.assertEquals(get_sch_img_settings_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     get_sch_img_settings_obj.status_code))

        get_sch_img_settings = get_sch_img_settings_obj.entity

        self.assertEquals(get_sch_img_settings.retention,
                          sch_img.retention,
                          msg.format('retention', sch_img.retention,
                                     get_sch_img_settings.retention))

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
        7) Get scheduled images settings for the instance as creator
        8) Verify that the response code is 200
        9) Verify that the response contains the entered retention value
        10) Get scheduled images settings for the instance as observer
        11) Verify that the response code is 200
        12) Verify that the response contains the entered retention value

        Attributes to verify:
            retention
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

        sch_img = sch_img_obj.entity

        # Check admin
        get_sch_img_settings_obj = \
            self.images_provider.scheduled_images_client. \
                get_scheduled_images_settings(tenant_id, instance_id)
        self.assertEquals(get_sch_img_settings_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     get_sch_img_settings_obj.status_code))

        get_sch_img_settings = get_sch_img_settings_obj.entity

        self.assertEquals(get_sch_img_settings.retention,
                          sch_img.retention,
                          msg.format('retention', sch_img.retention,
                                     get_sch_img_settings.retention))

        # Check creator
        get_sch_img_settings_obj = \
            self.creator_images_provider.scheduled_images_client. \
                get_scheduled_images_settings(tenant_id, instance_id)
        self.assertEquals(get_sch_img_settings_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     get_sch_img_settings_obj.status_code))

        get_sch_img_settings = get_sch_img_settings_obj.entity

        self.assertEquals(get_sch_img_settings.retention,
                          sch_img.retention,
                          msg.format('retention', sch_img.retention,
                                     get_sch_img_settings.retention))

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

    @attr('positive', 'rbac')
    def test_rbac_get_scheduled_images_settings_not_enabled(self):
        """ Rbac - Get scheduled images settings for a valid server that does
        not have scheduled images enabled.

        """

        """
        1) Create a valid server instance
        2) Get scheduled images settings for the instance as admin
        3) Verify that the response code is 404
        4) Get scheduled images settings for the instance as creator
        5) Verify that the response code is 404
        6) Get scheduled images settings for the instance as observer
        7) Verify that the response code is 404

        Attributes to verify:
            retention
        """

        tenant_id = self.config.images.tenant_id
        instance_id = self.servers[2].id

        # Check admin
        with self.assertRaises(ItemNotFound):
            self.images_provider.scheduled_images_client. \
                get_scheduled_images_settings(tenant_id, instance_id)

        # Check creator
        with self.assertRaises(ItemNotFound):
            self.creator_images_provider.scheduled_images_client. \
                get_scheduled_images_settings(tenant_id, instance_id)

        # Check observer
        with self.assertRaises(ItemNotFound):
            self.observer_images_provider.scheduled_images_client. \
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
        9) Get scheduled images settings for the instance as creator
        10) Verify that the response code is 200
        11) Verify that the response contains the entered retention value
        12) Get scheduled images settings for the instance as observer
        13) Verify that the response code is 200
        14) Verify that the response contains the entered retention value
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

        dis_sch_img_obj = self.images_provider.scheduled_images_client. \
            disable_scheduled_images(tenant_id, instance_id)
        self.assertEquals(dis_sch_img_obj.status_code, 202,
                          msg.format('status_code', 202,
                                     dis_sch_img_obj.status_code))

        # Check admin
        with self.assertRaises(ItemNotFound):
            self.images_provider.scheduled_images_client. \
                get_scheduled_images_settings(tenant_id, instance_id)

        # Check creator
        with self.assertRaises(ItemNotFound):
            self.creator_images_provider.scheduled_images_client. \
                get_scheduled_images_settings(tenant_id, instance_id)

        # Check observer
        with self.assertRaises(ItemNotFound):
            self.observer_images_provider.scheduled_images_client. \
                get_scheduled_images_settings(tenant_id, instance_id)

    @attr('positive', 'rbac')
    def test_rbac_get_scheduled_images_settings_creator_enabled_disabled(self):
        """ Rbac - Get scheduled images settings for a valid server that has
        scheduled images enabled as creator then disabled by admin.

        """

        """
        1) Create a valid server instance
        2) Enable scheduled images using a valid retention value as creator
        3) Verify that the response code is 200
        4) Disable scheduled images as admin
        5) Verify that the response code is 202
        6) Get scheduled images settings for the instance as admin
        7) Verify that the response code is 200
        8) Verify that the response contains the entered retention value
        9) Get scheduled images settings for the instance as creator
        10) Verify that the response code is 200
        11) Verify that the response contains the entered retention value
        12) Get scheduled images settings for the instance as observer
        13) Verify that the response code is 200
        14) Verify that the response contains the entered retention value
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

        dis_sch_img_obj = self.images_provider.scheduled_images_client. \
            disable_scheduled_images(tenant_id, instance_id)
        self.assertEquals(dis_sch_img_obj.status_code, 202,
                          msg.format('status_code', 202,
                                     dis_sch_img_obj.status_code))

        # Check admin
        with self.assertRaises(ItemNotFound):
            self.images_provider.scheduled_images_client. \
                get_scheduled_images_settings(tenant_id, instance_id)

        # Check creator
        with self.assertRaises(ItemNotFound):
            self.creator_images_provider.scheduled_images_client. \
                get_scheduled_images_settings(tenant_id, instance_id)

        # Check observer
        with self.assertRaises(ItemNotFound):
            self.observer_images_provider.scheduled_images_client. \
                get_scheduled_images_settings(tenant_id, instance_id)
