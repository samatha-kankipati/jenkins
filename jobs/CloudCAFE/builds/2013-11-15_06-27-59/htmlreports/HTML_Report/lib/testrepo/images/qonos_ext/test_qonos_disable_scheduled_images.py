import ccengine.common.tools.datagen as datagen
from ccengine.common.constants.images_constants import Constants
from ccengine.common.decorators import attr
from testrepo.common.testfixtures.images import BaseImagesFixture


class TestQonosDisableScheduledImages(BaseImagesFixture):

    @classmethod
    def setUpClass(cls):
        """Creates the server instances used for all tests in this class."""

        super(TestQonosDisableScheduledImages, cls).setUpClass()

        server_name = datagen.random_string(size=10)

        server_obj = cls.images_provider.create_active_server(server_name)

        cls.instance_id = server_obj.entity.id

    @attr('smoke')
    def test_happy_path_disable_scheduled_images(self):
        """Happy Path - Disable scheduled images for a valid server.

        1) Create a valid server instance
        2) Enable scheduled images using a valid retention value
        3) Verify that the response code is 200
        4) Disable scheduled images
        5) Verify that the response code is 202
        6) List schedules
        7) Verify that the response code is 200
        8) Verify that there is no schedule returned for the instance
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

        keys = ["tenant", "marker"]
        values = [tenant_id, marker]

        list_sch = self.images_provider.list_schedules_pagination(keys, values)

        for s in list_sch:
            for metadata_key, metadata_value in s.metadata.items():
                if metadata_value == self.instance_id:
                    sch_list.append(s)
        self.assertEquals(len(sch_list), count,
                          msg.format("length of the list", count,
                                     len(sch_list)))
