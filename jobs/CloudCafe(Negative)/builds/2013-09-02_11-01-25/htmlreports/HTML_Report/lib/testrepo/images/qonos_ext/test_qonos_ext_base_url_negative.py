from testrepo.common.testfixtures.images import BaseImagesFixture
from ccengine.common.decorators import attr
import ccengine.common.tools.datagen as datagen
from ccengine.common.exceptions.compute import ItemNotFound


class TestQonosExtBaseUrlNegative(BaseImagesFixture):

    @classmethod
    def setUpClass(cls):
        '''Creates the server instances and snapshots used for all tests in
        this class'''

        super(TestQonosExtBaseUrlNegative, cls).setUpClass()

        server_name = datagen.random_string(size=10)

        server_obj = cls.images_provider.create_active_server(server_name)

        cls.instance_id = server_obj.entity.id

    @attr('negative')
    def test_qonos_nova_extension_request_incorrect_base_url(self):
        '''Qonos nova extension request incorrect base URL'''

        """
        1) Attempt to request the base url of
            '{tenant_id}/servers/{instance_id}/rax-si-image-schedule-test'
        2) Verify that the response code is 404
        """

        tenant_id = self.config.images.tenant_id
        instance_id = self.instance_id
        url = '-test'

        with self.assertRaises(ItemNotFound):
            self.images_provider.scheduled_images_client. \
                get_incorrect_base_url(tenant_id, instance_id, url)
