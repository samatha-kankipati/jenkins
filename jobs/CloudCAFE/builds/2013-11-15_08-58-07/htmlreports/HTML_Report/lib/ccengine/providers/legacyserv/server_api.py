import time

from ccengine.clients.legacyserv.server_api import LegacyServClient
from ccengine.common.tools.datagen import random_string
from ccengine.domain.types import LegacyServerStatusTypes as ServStatus
from ccengine.providers.base_provider import BaseProvider
from ccengine.providers.identity.identity_v2_0_api import IdentityAPIProvider


class ServerProvider(BaseProvider):

    def __init__(self, config, logger):

        super(ServerProvider, self).__init__()
        self.config = config
        self.identity_provider = IdentityAPIProvider(self.config)
        auth_data = self.identity_provider.authenticate().entity
        if self.config.legacyserv.url:
            self.url = self.config.legacyserv.url
        else:
            self.url = (auth_data.serviceCatalog.get_service(
                self.config.legacyserv.identity_service_name)
                        .endpoints[0].publicURL)
        self.client = LegacyServClient(self.url, auth_data.token.id,
                                       config.misc.serializer,
                                       config.misc.deserializer)

    def wait_for_status(self, server_id, interval_time=None, timeout=None,
                        status_to_wait_for=ServStatus.ACTIVE):
        """
        @summary: Wait for legacy server to be active and exit if
            its in error state.
        @param server_id: The name of the server.
        @type server_id: String
        @param interval_time:  Interval to sleep in seconds.
        @type interval_time: Float
        @param timeout: Max wait time for status to wait for.
        @type timeout: Int
        @param status_to_wait_for: Server status to wait for.
        @type status_to_wait_for: String
        @return: Response Object containing response code and
         the server domain object
        @rtype: Request Response Object
        """
        response_server = self.client.list_server_id(server_id)
        time_waited = 0
        if not interval_time:
            interval_time = self.config.legacyserv.build_interval or 3
        if not timeout:
            timeout = self.config.legacyserv.server_status_timeout or 720
        while (response_server.entity.status.lower() != \
               status_to_wait_for.lower() and time_waited < timeout):
            time.sleep(interval_time)
            response_server = self.client.list_server_id(server_id)
            time_waited += interval_time
            if response_server.entity.status == ServStatus.ERROR:
                break
        if time_waited > timeout:
            raise Exception('Request timed out waiting on Server: '
                            'server entity: {0}\n'
                            'timeout: {1}\n'
                            'status_to_wait_for: {2}\n'
                            .format(response_server.entity,
                                    timeout,
                                    status_to_wait_for))
        return response_server

    def create_active_server(self, name=None, image_ref=None, flavor_ref=None,
                             **kwargs):
        """
        @summary:Creates a legacy server and waits for server to
            reach active status
        @param name: The name of the server.
        @type name: String
        @param image_ref: The reference to the image used to
            build the server.
        @type image_ref: String
        @param flavor_ref: The flavor used to build the server.
        @type flavor_ref: String
        @return: Response Object containing response code and
         the server domain object
        @rtype: Request Response Object
        """
        if not name:
            name = random_string('TestServ')
        if not image_ref:
            image_ref = self.config.legacyserv.image_ref or 119
        if not flavor_ref:
            flavor_id = self.config.legacyserv.flavor_ref or 1

        response = self.client.create_server(name=name,
                                             image_id=image_ref,
                                             flavor_id=flavor_id)

        response_server = self.wait_for_status(response.entity.id)
        if response_server.entity.status == ServStatus.ERROR:
            raise Exception('Build failed. Server entered ERROR status.'
                            '\nserver entity: {0}'
                            .format(response_server.entity))
        return response_server
