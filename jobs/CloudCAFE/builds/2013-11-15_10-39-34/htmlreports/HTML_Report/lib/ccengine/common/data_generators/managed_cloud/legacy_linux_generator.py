import json

from ccengine.common.data_generators.data_generator import DataGenerator
from ccengine.providers.configuration import MasterConfigProvider as _MCP
from ccengine.providers.legacyserv.server_api import ServerProvider
from ccengine.providers.auth.auth_api import AuthProvider
from ccengine.clients.legacyserv.server_api import LegacyServClient
from ccengine.clients.legacyserv.images_api import ImagesAPIClient
from ccengine.common.tools.datagen import rand_name


class ManagedCloudLegacyLinuxDataGenerator(DataGenerator):

    def __init__(self):
        config = _MCP()
        auth_provider = AuthProvider(config)
        legacy_url = config.legacyserv.url
        customer_id = config.compute_api.tenant_id
        legacy_url = "{0}/{1}".format(legacy_url, customer_id)
        auth_token = auth_provider.authenticate().token.id
        legacy_serv_client = LegacyServClient(legacy_url, auth_token)
        legacy_images_client = ImagesAPIClient(legacy_url, auth_token)
        self.test_records = []
        server_name = "Legacy-Managed-Linux-Server"
        json_resp = json.loads(legacy_images_client.list_images().text)
        server_images_list = json_resp['images']
        for server_image in server_images_list:
            if("windows" not in (server_image['name']).lower()):
                legacy_serv_client.create_server(
                    name=rand_name(server_name),
                    flavor_id=config.managedcloud.legacy_flavor,
                    image_id=server_image['id'])
        json_dict = json.loads(legacy_serv_client.list_server().text)
        for server in json_dict['servers']:
            self.test_records.append({'server_id': server['id']})
