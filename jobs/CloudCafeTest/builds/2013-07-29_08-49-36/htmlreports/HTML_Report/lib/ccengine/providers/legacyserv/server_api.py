from ccengine.providers.base_provider import BaseProvider
from ccengine.clients.legacyserv.server_api import LegacyServClient
import ccengine.common.tools.datagen as datagen
from ccengine.domain.types import LegacyServerStatusTypes as ServStatus
from ccengine.providers.identity.identity_v2_0_api import IdentityAPIProvider
import time


class ServerProvider(BaseProvider):

    def __init__(self, config, logger):

        super(ServerProvider, self).__init__()
        self.config = config
        self.identity_provider = IdentityAPIProvider(self.config)
        auth_data = self.identity_provider.authenticate().entity
        self.url = config.legacyserv.url
        self.client = LegacyServClient(self.url, auth_data.token.id,
                                       config.misc.serializer,
                                       config.misc.deserializer)

    def wait_for_status(self, server_id, status_to_wait_for=ServStatus.ACTIVE):
        """
        wait for legacy server to be active and exit if its in error state
        """
        responseServer = self.client.list_server_id(server_id)
        time_waited = 0
        interval_time = 3
        timeout = 720
        while (responseServer.entity.status.lower()\
               != status_to_wait_for.lower() and time_waited < timeout):
            time.sleep(interval_time)
            responseServer = self.client.list_server_id(server_id)
            time_waited += interval_time
            if responseServer.entity.status == ServStatus.ERROR:
                break
        return responseServer

    def create_active_server(self, **kwargs):
        """
        Create a legacy server
        """
        name = datagen.random_string('TestServ')
        image_id = 119
        flavor_id = 2

        response = self.client.create_server(name=name,
                                             image_id=image_id,
                                             flavor_id=flavor_id)

        responseServer = self.wait_for_status(response.entity.id)
        if responseServer.entity.status == ServStatus.ERROR:
            responseServer = self.client.create_server(name=name,
                                                       image_id=image_id,
                                                       flavor_id=flavor_id)
        return responseServer
