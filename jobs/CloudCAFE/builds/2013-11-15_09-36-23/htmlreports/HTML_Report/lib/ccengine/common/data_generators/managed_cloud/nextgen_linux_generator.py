from ccengine.common.data_generators.data_generator import DataGenerator
from ccengine.providers.configuration import MasterConfigProvider as _MCP
from ccengine.providers.compute.compute_api import ComputeAPIProvider \
    as _ComputeAPIProvider
from ccengine.common.tools.datagen import rand_name


class ManagedCloudLinuxNextGenDataGenerator(DataGenerator):

    def __init__(self):
        config = _MCP()
        servers_created = []
        self.test_records = []
        server_name = "{0}-Managed-Linux-Server".format(
            config.compute_api.region)
        compute_provider = _ComputeAPIProvider(config)
        images_list = compute_provider.images_client.list_images().entity
        # List of new unsupported images
        ignore_list = ["windows", "image", "vyatta"]
        # Ignore the images in ignore list
        linux_images_list = [
            image for image in images_list if not any(ignored_image in
                                                      image.name.lower()
                                                      for ignored_image in
                                                      ignore_list)]
        for image in linux_images_list:
            servers_created.append(
                compute_provider.create_server_no_wait(
                    name=rand_name(
                        server_name),
                    imageRef=image.id,
                    flavorRef=config.managedcloud.flavor_id,
                ).entity)
        for server in servers_created:
            self.test_records.append({
                                     'server_id': server.id,
                                     'server_pass': server.adminPass})
