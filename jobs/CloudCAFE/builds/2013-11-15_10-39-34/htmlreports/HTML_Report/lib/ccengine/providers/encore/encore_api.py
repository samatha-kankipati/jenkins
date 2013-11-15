from ccengine.clients.encore.device_api import DeviceAPIClient
from ccengine.providers.auth.auth_api import AuthProvider as _AuthProvider
from ccengine.providers.base_provider import BaseProvider


class EncoreAPIProvider(BaseProvider):

    def __init__(self, config, logger=None):
        super(EncoreAPIProvider, self).__init__()
        if config is None:
            self.client_log.warning('empty (=None) config recieved in init')
            # Load configuration from default.conf
            self.config = _AuthProvider
        else:
            self.config = config

        # Get Auth Info
        self.auth_provider = _AuthProvider(self.config)

        # Get Auth Token
        self.auth_token = self.auth_provider.authenticate()

        # setup url
        self.base_request_url = self.config.auth.base_url

        # initialize device api client
        self.encore_client = DeviceAPIClient(self.base_request_url,
                                             self.auth_token,
                                             self.config.misc.serializer,
                                             self.config.misc.deserializer)
