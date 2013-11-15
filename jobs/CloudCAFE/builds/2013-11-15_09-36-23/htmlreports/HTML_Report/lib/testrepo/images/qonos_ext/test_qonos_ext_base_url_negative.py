import ccengine.common.tools.datagen as datagen
from ccengine.common.decorators import attr
from ccengine.common.exceptions.compute import ItemNotFound
from testrepo.common.testfixtures.images import BaseImagesFixture


class TestQonosExtBaseUrlNegative(BaseImagesFixture):

    @classmethod
    def setUpClass(cls):
        """Creates the server instance used for all tests in this class."""

        super(TestQonosExtBaseUrlNegative, cls).setUpClass()

        server_name = datagen.random_string(size=10)

        server_obj = cls.images_provider.create_active_server(server_name)

        cls.instance_id = server_obj.entity.id

    @attr('negative')
    def test_qonos_nova_extension_request_incorrect_base_url(self):
        """Qonos nova extension request incorrect base URL.

        1) Attempt to request the base url of
            '{tenant_id}/servers/{instance_id}/rax-si-image-schedule-test'
        2) Verify that the response code is 404
        """

        tenant_id = self.config.images.tenant_id
        instance_id = self.instance_id
        base_url = self.config.images.url

        url = \
            "{0}/{1}/servers/{2}/rax-si-image-schedules".format(base_url,
                                                                tenant_id,
                                                                instance_id)

        with self.assertRaises(ItemNotFound):
            self.images_provider.scheduled_images_client. \
                get_scheduled_images_settings(tenant_id, instance_id,
                                              requestslib_kwargs={'url': url})
