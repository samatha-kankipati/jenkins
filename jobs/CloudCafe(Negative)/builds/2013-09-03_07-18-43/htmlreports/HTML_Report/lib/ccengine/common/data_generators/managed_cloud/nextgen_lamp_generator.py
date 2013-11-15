from ccengine.common.data_generators.data_generator import DataGenerator
from ccengine.providers.configuration import MasterConfigProvider as _MCP
from ccengine.providers.compute.compute_api import ComputeAPIProvider \
    as _ComputeAPIProvider
from ccengine.common.tools.datagen import rand_name


class ManagedCloudLinuxNextGenLampDataGenerator(DataGenerator):

    def __init__(self):
        config = _MCP()
        servers_created = []
        self.test_records = []
        server_name = "{0}-Managed-Lamp-Server".format(
            config.compute_api.region)
        compute_provider = _ComputeAPIProvider(config)
        servers_client = compute_provider.servers_client
        images_list = compute_provider.images_client.list_images().entity
        metadata_dict = {'build_config': 'lamp'}
        linux_images_list = [
            f for f in images_list if ("windows" not in f.name.lower()
                                       and "image" not in f.name.lower())]
        for image in linux_images_list:
            servers_created.append(
                servers_client.create_server(
                    name=rand_name(
                        server_name),
                    image_ref=image.id,
                    flavor_ref=3,
                    metadata=metadata_dict
                ).entity)
        for server in servers_created:
            self.test_records.append({
                                     'server_id': server.id,
                                     'server_pass': server.adminPass})
