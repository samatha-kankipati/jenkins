from testrepo.common.testfixtures.images import BaseImagesFixture
from ccengine.common.constants.images_constants import Constants
from ccengine.common.decorators import attr
from ccengine.common.exceptions.compute import ItemNotFound
import ccengine.common.tools.datagen as datagen
from ccengine.domain.types import NovaServerStatusTypes


class TestQonosDisableScheduledImagesPositive(BaseImagesFixture):

    @classmethod
    def setUpClass(cls):
        '''Creates the server instances used for all tests in this class'''

        super(TestQonosDisableScheduledImagesPositive, cls).setUpClass()

        count = 2
        servers = []

        for x in range(count):
            server_name = datagen.random_string(size=10)
            server_obj = cls.images_provider.create_server_no_wait(server_name)
            servers.append(server_obj.entity)

        cls.instance_id = servers[0].id
        cls.alt_instance_id = servers[1].id

        for server in servers:
            cls.images_provider.\
                wait_for_server_status(server.id,
                                       NovaServerStatusTypes.ACTIVE)

    @attr('positive')
    def test_disable_scheduled_images_for_instance_not_enabled(self):
        '''Disable scheduled images for instance when not enabled'''

        """
        1) Create a valid server instance
        2) Disable scheduled images
        3) Verify that the response code is 404
        4) List schedules
        5) Verify that the response code is 200
        6) Verify that there is no schedule returned for the instance
        """

        tenant_id = self.config.images.tenant_id
        instance_id = self.instance_id
        sch_list = []
        count = 0
        marker = None
        msg = Constants.MESSAGE

        with self.assertRaises(ItemNotFound):
            self.images_provider.scheduled_images_client. \
                disable_scheduled_images(tenant_id, instance_id)

        keys = ["tenant", "marker"]
        values = [tenant_id, marker]

        list_sch = self.images_provider.list_schedules_pagination(keys, values)

        for s in list_sch:
            for metadata_key, metadata_value in s.metadata.items():
                if metadata_value == instance_id:
                    sch_list.append(s)
        self.assertTrue(len(sch_list) == count,
                        msg.format("length of the list", count, len(sch_list)))

    @attr('positive')
    def test_disable_sch_img_single_server_customer_has_many(self):
        '''Disable scheduled images on single server customer has many'''

        """
        1) Create two valid server instances
        2) Enable scheduled images using a valid retention value
        3) Verify that the response code is 200
        4) Enable scheduled images using a valid retention value for second
        instance
        5) Verify that the response code is 200
        6) Disable scheduled images for first instance
        7) Verify that the response code is 202
        8) List schedules
        9) Verify that the response code is 200
        10) Verify that there is a schedule returned for the second instance
        only
        """

        tenant_id = self.config.images.tenant_id
        instance_id = self.instance_id
        alt_instance_id = self.alt_instance_id
        sch_list = []
        count = 1
        retention = self.config.images.retention
        user_name = self.config.images.user_name
        marker = None
        msg = Constants.MESSAGE

        sch_img_obj = self.images_provider.scheduled_images_client. \
            enable_scheduled_images(tenant_id, instance_id, retention)
        self.assertEquals(sch_img_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     sch_img_obj.status_code))

        alt_sch_img_obj = self.images_provider.scheduled_images_client. \
            enable_scheduled_images(tenant_id, alt_instance_id, retention)
        self.assertEquals(alt_sch_img_obj.status_code, 200,
                          msg.format('status_code', 200,
                                     alt_sch_img_obj.status_code))

        dis_sch_img_obj = self.images_provider.scheduled_images_client. \
            disable_scheduled_images(tenant_id, instance_id)
        self.assertEquals(dis_sch_img_obj.status_code, 202,
                          msg.format('status_code', 202,
                                     dis_sch_img_obj.status_code))

        keys = ["tenant", "marker"]
        values = [tenant_id, marker]

        list_sch = self.images_provider.list_schedules_pagination(keys, values)

        for s in list_sch:
            for metadata_key, metadata_value in s.metadata.items():
                if (metadata_value == instance_id
                    or metadata_value == alt_instance_id):
                    sch_list.append(s)
        self.assertTrue(len(sch_list) == count,
                        msg.format("length of the list", count, len(sch_list)))

        listed_sch = sch_list[0]

        self.assertEquals(str(listed_sch.metadata),
                          "{{u'instance_id': u'{0}', u'user_name': u'{1}'}}".\
                          format(alt_instance_id, user_name),
                          msg.format('metadata',
                                     "{{u'instance_id': u'{0}',"
                                     + " u'user_name': u'{1}'}}".\
                                     format(alt_instance_id, user_name),
                                     str(listed_sch.metadata)))

    @attr('positive')
    def test_disable_scheduled_images_server_already_disabled(self):
        '''Disable scheduled images on server that is already disabled'''

        """
        1) Create a valid server instance
        2) Enable scheduled images using a valid retention value
        3) Verify that the response code is 200
        4) Disable scheduled images
        5) Verify that the response code is 202
        6) Disable scheduled images
        7) Verify that the response code is 404
        8) List schedules
        9) Verify that the response code is 200
        10) Verify that there is no schedule returned for the instance
        """

        tenant_id = self.config.images.tenant_id
        instance_id = self.instance_id
        sch_list = []
        count = 0
        retention = self.config.images.retention
        marker = None
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

        with self.assertRaises(ItemNotFound):
            self.images_provider.scheduled_images_client. \
                disable_scheduled_images(tenant_id, instance_id)

        keys = ["tenant", "marker"]
        values = [tenant_id, marker]

        list_sch = self.images_provider.list_schedules_pagination(keys, values)

        for s in list_sch:
            for metadata_key, metadata_value in s.metadata.items():
                if metadata_value == instance_id:
                    sch_list.append(s)
        self.assertTrue(len(sch_list) == count,
                        msg.format("length of the list", count, len(sch_list)))
