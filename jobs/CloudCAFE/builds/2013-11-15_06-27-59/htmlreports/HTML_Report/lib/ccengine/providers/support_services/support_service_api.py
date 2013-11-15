import time

from ccengine.clients.support_services.support_service_api import\
    SupportServicesAPIGroupsClient, SupportContactClient, SupportTeamsClient
from ccengine.providers.auth.auth_api import AuthProvider as _AuthProvider
from ccengine.providers.base_provider import BaseProvider


class SupportServicesAPIProvider(BaseProvider):

    def __init__(self, config, logger=None):
        super(SupportServicesAPIProvider, self).__init__()

        self.config = config

        #Get Auth Info

        self.auth_provider = _AuthProvider(self.config)
        self.auth_data = self.auth_provider.authenticate()

        #Get Auth Token

        self.auth_token = self.auth_data.token.id

        #setup url

        self.base_request_url = self.config.support_service.base_url

        #initialize ss api clients

        self.support_services_groups_client = SupportServicesAPIGroupsClient(
            self.base_request_url,
            self.auth_token,
            self.config.misc.serializer,
            self.config.misc.deserializer)

        self.support_contact_client = SupportContactClient(
            self.base_request_url,
            self.auth_token,
            self.config.misc.serializer,
            self.config.misc.deserializer)

        self.support_team_client = SupportTeamsClient(
            self.base_request_url,
            self.auth_token,
            self.config.misc.serializer,
            self.config.misc.deserializer)
