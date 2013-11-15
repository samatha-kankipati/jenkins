from requests.auth import HTTPBasicAuth

from ccengine.clients.zendesk.zendesk_api import ZendeskTicketClient
from ccengine.providers.auth.auth_api import AuthProvider as _AuthProvider
from ccengine.providers.base_provider import BaseProvider


class ZendeskAPIProvider(BaseProvider):

    def __init__(self, config):
        super(ZendeskAPIProvider, self).__init__()
        if config is None:
            self.provider_log.warning('empty (=None) config recieved in init')
            # Load configuration from default.conf
            self.config = _AuthProvider
        else:
            self.config = config
        # Get basic auth
        self.basic_auth = HTTPBasicAuth(self.config.auth.username,
                                        self.config.auth.password)

        self.url = self.config.auth.zendesk_ticket_url

        self.zendesk_client = ZendeskTicketClient(
            self.url, self.basic_auth, self.config.misc.serializer,
            self.config.misc.deserializer)
