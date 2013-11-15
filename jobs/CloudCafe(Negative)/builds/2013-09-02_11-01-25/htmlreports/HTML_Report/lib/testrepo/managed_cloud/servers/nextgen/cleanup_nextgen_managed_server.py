import json
from testrepo.common.testfixtures.compute import ComputeFixture
from ccengine.common.decorators import attr


class CleanUpManagedServersTest(ComputeFixture):
    def test_delete_all_server_on_account(self):
        list_servers_response = self.servers_client.list_servers()
        list_servers = list_servers_response.entity
        if (len(list_servers) > 0):
            for server in list_servers:
                self.deleted_server = self.servers_client.delete_server(
                    server.id)
                self.assertEqual(204, self.deleted_server.status_code,
                                 'The delete call #response was: {0}'.format(
                                     self.deleted_server.status_code))

    def test_delete_all_images_on_account(self):
        list_images_response = self.images_client.list_images()
        list_images = list_images_response.entity
        if (len(list_images) > 0):
            for image in list_images:
                if ("image" in image.name.lower()):
                    self.deleted_image = self.images_client.delete_image(
                        image_id=image.id)
                    self.assertEqual(204, self.deleted_image.status_code,
                                     'The delete call #response was: {0}'.format(
                                         self.deleted_image.status_code))
