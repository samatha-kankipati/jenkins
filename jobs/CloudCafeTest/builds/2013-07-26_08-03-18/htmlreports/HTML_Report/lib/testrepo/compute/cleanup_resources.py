from ccengine.common.decorators import attr
from testrepo.common.testfixtures.compute import ComputeFixture


class CleanupResource(ComputeFixture):

    @attr(type='cleanup')
    def test_cleanup_delete_servers(self):
        try:
            servers = self.servers_client.list_servers_with_detail()
            self.fixture_log.debug("\n Total number of servers found: "
                                   "{0}".format(len(servers.entity)))

            for server in servers.entity:
                self.servers_client.delete_server(server.id)
                self.fixture_log.debug("\n deleting server: "
                                       "{0}".format(server.id))
        except Exception, e:
            self.fixture_log.error(e)
            pass

    @attr(type='cleanup')
    def test_cleanup_delete_images(self):
        images = self.images_client.list_images_with_detail()

        for image in images.entity:
            if hasattr(image.metadata, "instance_uuid"):
                self.images_client.delete_image(image.id)
                self.fixture_log.debug("\n deleting image: "
                                       "{0}".format(image.id))
