from ccengine.common.data_generators.data_generator import DataGenerator
from ccengine.providers.configuration import MasterConfigProvider as _MCP
from ccengine.providers.compute.compute_api import ComputeAPIProvider \
    as _ComputeAPIProvider
from ccengine.common.tools.datagen import rand_name
from random import choice


class ManagedCloudWindowsNextGenRebuildDataGenerator(DataGenerator):

    def __init__(self):
        config = _MCP()
        servers_created = []
        self.test_records = []
        server_name = "RBLT-{0}-Managed-Windows-Server".format(
            config.compute_api.region)
        compute_provider = _ComputeAPIProvider(config)
        servers_client = compute_provider.servers_client
        servers_list = servers_client.list_servers().entity
        images_list = compute_provider.images_client.list_images().entity
        windows_images_list = [
            f for f in images_list if ("windows" in f.name.lower()
                                       and "image" not in f.name.lower())]
        for server in servers_list:
            if ("windows" in server.name.lower()):
                servers_created.append(servers_client.rebuild(
                    server_id=server.id,
                    image_ref=choice(windows_images_list).id,
                    flavor_ref=config.managedcloud.windows_flavor,
                    name=rand_name(server_name)).entity)
        for server in servers_created:
            self.test_records.append({
                                     'server_id': server.id,
                                     'server_pass': server.adminPass})
