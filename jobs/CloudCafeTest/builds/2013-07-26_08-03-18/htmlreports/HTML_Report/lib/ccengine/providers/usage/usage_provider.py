'''
@summary: Provider Module for the AUTH API
@note: Should be the primary interface to a test case or external tool.
@copyright: Copyright (c) 2012 Rackspace US, Inc.
'''
from ccengine.providers.base_provider import BaseProvider
from ccengine.providers.rax_signup.rax_signup_api import RaxSignupProvider
from ccengine.providers.identity.v2_0.identity_api import IdentityAPIProvider
from ccengine.clients.servicemix.service_mix_client import ServiceMixAPIClient
from ccengine.domain.configuration import IdentityAPIConfig


class UsageIntegrationProvider(BaseProvider):

    def __init__(self, config):
        self.config = config
        self.signup_provider = RaxSignupProvider(self.config)
        self.identity_provider = IdentityAPIProvider(self.config)
        self.smix_client = ServiceMixAPIClient(self.config.service_mix.base_url)

    def create_active_cloud_account(self):
        resp = self.signup_provider.create_new_cloud_account()
        account_id = resp.entity.id_
        username = resp.request.entity.contacts[0].user.username
        password = resp.request.entity.contacts[0].user.password

        resp = self.smix_client.set_account_status(account_id, 'ACTIVE')
        assert resp.ok, 'Unable to set new user to ACTIVE state'
        new_user_config_info = {
            IdentityAPIConfig.SECTION_NAME: {
                'username': username,
                'api_key': '',
                'password': password}}

        user_config = self.config.mcp_override(new_user_config_info)
        return account_id
