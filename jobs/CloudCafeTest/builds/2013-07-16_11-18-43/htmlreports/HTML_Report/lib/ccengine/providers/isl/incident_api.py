import time
from ccengine.providers.base_provider import BaseProvider
from ccengine.clients.isl.incident_api import IncidentAPIClient
from ccengine.providers.auth.auth_api import AuthProvider as _AuthProvider
from ccengine.common.tools.datagen import rand_name

class IncidentAPIProvider(BaseProvider):
    '''
         Proper comments goes here
    '''

    def __init__(self, config, logger=None):
        super(IncidentAPIProvider, self).__init__()
        if config is None:
            self.client_log.warning('empty (=None) config recieved in init')
            ''' Load configuration from default.conf '''
            self.config = _AuthProvider
        else:
            self.config = config

        '''Get Auth Info '''
        self.auth_provider = _AuthProvider(self.config)

        self.auth_data = self.auth_provider.authenticate()
        '''Get Auth Token'''
        self.auth_token = self.auth_data.token.id

        '''setup url'''
        self.base_request_url = self.config.isl.base_request_url

        '''initialize compute api clients'''
        self.incident_client = IncidentAPIClient(self.base_request_url,
                                                 self.auth_token,
                                                 self.config.misc.serializer,
                                                 self.config.misc.deserializer)