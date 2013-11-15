from ccengine.common.data_generators.data_generator import DataGenerator
from ccengine.providers.configuration import MasterConfigProvider as _MCP
from ccengine.providers.compute.compute_api import ComputeAPIProvider \
    as _ComputeAPIProvider
from ccengine.common.tools.datagen import rand_name
from random import choice


class ManagedCloudLampNextGenRebuildDataGenerator(DataGenerator):

    def __init__(self):
        config = _MCP()
        servers_created = []
        self.test_records = []
        server_name = "RBLT-{0}-Managed-Lamp-Server".format(
            config.compute_api.region)
        metadata_dict = {'build_config': 'lamp'}
        compute_provider = _ComputeAPIProvider(config)
        servers_client = compute_provider.servers_client
        servers_list = servers_client.list_servers().entity
        images_list = compute_provider.images_client.list_images().entity
        # List of new unsupported images
        ignore_list = ["windows", "image", "vyatta"]
        # Ignore the images in ignore list
        linux_images_list = [
            image for image in images_list if not any(ignored_image in
                                                      image.name.lower()
                                                      for ignored_image in
                                                      ignore_list)]
        for server in servers_list:
            if ("lamp" in server.name.lower()
                    and "linux" not in server.name.lower()):
                servers_created.append(servers_client.rebuild(
                    server_id=server.id,
                    image_ref=choice(linux_images_list).id,
                    flavor_ref=config.managedcloud.flavor_id,
                    name=rand_name(server_name),
                    metadata=metadata_dict).entity)
        for server in servers_created:
            self.test_records.append({
                                     'server_id': server.id,
                                     'server_pass': server.adminPass})
