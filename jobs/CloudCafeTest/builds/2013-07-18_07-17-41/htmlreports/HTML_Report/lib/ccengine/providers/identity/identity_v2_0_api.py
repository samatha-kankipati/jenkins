'''
@summary: Provider Module for the AUTH API
@note: Should be the primary interface to a test case or external tool.
@copyright: Copyright (c) 2012 Rackspace US, Inc.
'''
from ccengine.providers.base_provider import BaseProvider, ProviderActionResult
from ccengine.clients.identity.identity_api_v2_0 import IdentityClient


class IdentityAPIProvider(BaseProvider):
    '''
    @summary: Provides an interface to Auth providers
    '''

    def __init__(self, config):
        super(IdentityAPIProvider, self).__init__()
        self.config = config
        self.identity_client = None
        if self.config.identity_api.version == '2.0':
            self.identity_client = IdentityClient(
                            self.config.identity_api.authentication_endpoint,
                            serialize_format='json',
                            deserialize_format='json')
                            #self.config.misc.serializer,
                            #self.config.misc.deserializer)
        else:
            msg = 'Does not support versions of identity older than 2.0'
            raise NotImplementedError(msg)

    def authenticate(self):
        '''
            Automatically authenticates given the information in the config
            identity section.
            If both api key and password are present, prefers api_key.
            NOTE:  Currently only supports Rax Auth.
        '''
        provider_response = ProviderActionResult()
        username = self.config.identity_api.username
        api_key = self.config.identity_api.api_key
        password = self.config.identity_api.password

        if not username:
            msg1 = 'Username not found in the identity'
            msg2 = 'section of the config object'
            msg = ' '.join([msg1, msg2])
            self.provider_log.critical(msg)
            return None

        if not password and not api_key:
            msg1 = 'Neither an api_key nor a password where found in the'
            msg2 = 'identity section of the config object'
            msg = ' '.join([msg1, msg2])
            self.provider_log.critical(msg)
            return None

        if api_key:
            resp = self.identity_client.authenticate_api_key(username, api_key)
            provider_response.response = resp
            if resp.ok and (resp.entity is not None):
                provider_response.entity = resp.entity
                return provider_response

        elif password:
            resp = self.identity_client.authenticate_password(username,
                                                                password)
            provider_response.response = resp
            if resp.ok and (resp.entity is not None):
                provider_response.entity = resp.entity
                return provider_response
