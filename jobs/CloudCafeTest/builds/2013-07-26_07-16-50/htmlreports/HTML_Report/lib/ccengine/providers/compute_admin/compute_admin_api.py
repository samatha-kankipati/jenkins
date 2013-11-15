from ccengine.domain.configuration import AuthConfig
from ccengine.providers.base_provider import BaseProvider
from ccengine.clients.compute_admin.admin_api import AdminAPIClient
from ccengine.providers.auth.auth_api import AuthProvider


class ComputeAdminProvider(BaseProvider):

    def __init__(self, config, logger):
        '''Initializes the Compute Admin Client'''
        super(ComputeAdminProvider, self).__init__()
        self.config = config

        # api_key needs to be overwritten to an empty string
        admin_usr = ({AuthConfig.SECTION_NAME:
                {'base_url': self.config.admin_api.admin_auth_url,
                'username': self.config.admin_api.admin_username,
                'password': self.config.admin_api.admin_password,
                'api_key': ''}})

        admin_conf = self.config.mcp_override(admin_usr)
        self.auth_provider = AuthProvider(admin_conf)
        self.auth_data = self.auth_provider.authenticate()
        auth_token = self.auth_data.token.id
        url = self.auth_data.service_catalog[0].endpoints[0].publicURL

        self.client = AdminAPIClient(url, auth_token,
                                     self.config.misc.serializer,
                                     self.config.misc.deserializer)
