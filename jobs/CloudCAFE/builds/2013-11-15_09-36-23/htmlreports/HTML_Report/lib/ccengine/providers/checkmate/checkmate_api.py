from ccengine.providers.base_provider import BaseProvider
from ccengine.clients.checkmate.checkmate_api import CheckmateAPIClient
from ccengine.providers.auth.auth_api import AuthProvider as _AuthProvider

class CheckamteProvider(BaseProvider):

    def __init__(self, config, logger):
        '''
        Sets config, sets up client, sets deserializer and serializer based
        on format defined in the config.
        '''
        super(CheckamteProvider, self).__init__()
        self.config = config
        self.auth_provider = _AuthProvider(self.config)
        auth_data = self.auth_provider.authenticate()
        url = config.checkmate.host
        tenant_id = config.checkmate.tenant_id
        self.client = CheckmateAPIClient(url, auth_data.token.id, tenant_id)

