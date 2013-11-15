from ccengine.common.data_generators.data_generator import DataGenerator
from ccengine.providers.configuration import MasterConfigProvider as _MCP
from ccengine.providers.compute.compute_api import ComputeAPIProvider\
    as _ComputeAPIProvider
from ccengine.common.tools.datagen import rand_name


class ManagedCloudLampNextGenSnapshotDataGenerator(DataGenerator):

    def __init__(self):
        config = _MCP()
        servers_created = []
        self.test_records = []
        server_name = "SST-{0}-Managed-Lamp-Server".format(
            config.compute_api.region)
        compute_provider = _ComputeAPIProvider(config)
        images_list = compute_provider.images_client.list_images().entity
        linux_images_list = [
            f for f in images_list if ("windows" not in f.name.lower()
                                       and "image" in f.name.lower()
                                       and "lamp" in f.name.lower())]
        for image in linux_images_list:
            servers_created.append(
                compute_provider.create_server_no_wait(
                    name=rand_name(server_name),
                    imageRef=image.id,
                    flavorRef=config.managedcloud.flavor_id,
                ).entity)
        for server in servers_created:
            self.test_records.append({
                                     'server_id': server.id,
                                     'server_pass': server.adminPass})
