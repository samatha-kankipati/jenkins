import ccengine.common.tools.datagen as datagen
from ccengine.common.decorators import attr
from ccengine.domain.types import NovaServerStatusTypes
from testrepo.common.testfixtures.images import BaseImagesFixture


class TestQonosCleanup(BaseImagesFixture):

    @attr('qonos-data-setup')
    def test_data_setup(self):
        """Data setup by creating many servers and enabling schedules."""

        tenant_id = self.config.images.tenant_id
        image_ref = self.config.compute_api.image_ref
        flavor_ref = self.config.compute_api.flavor_ref
        count = 10

        for i in range(count):
            retention = i + 1
            name = "data_setup_{0}".format(datagen.random_string(size=5))

            server_obj = self.images_provider.servers_client.\
                create_server(name, image_ref, flavor_ref)

            server = server_obj.entity

            self.images_provider.\
                wait_for_server_status(server.id, NovaServerStatusTypes.ACTIVE)

            self.images_provider.scheduled_images_client. \
                enable_scheduled_images(tenant_id, server.id, retention)
