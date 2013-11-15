from ccengine.providers.base_provider import BaseProvider
from ccengine.providers.identity.identity_v2_0_api import IdentityAPIProvider
from ccengine.clients.rax_signup.rax_signup_api import RaxSignupAPIClient


class RaxSignupProvider(BaseProvider):
    '''
    Provides constructors for different client configurations.
    '''

    def __init__(self, config):
        self.config = config
        self.identity_provider = IdentityAPIProvider(self.config)

    def get_default_client(
            self, base_url=None, auth_token=None, serialize_format=None,
            deserialize_format=None, ah_endpoint=None, identity_endpoint=None):

        auth_token = self.get_token()

        if deserialize_format is None:
            deserialize_format = self.config.misc.deserializer

        return RaxSignupAPIClient(
            base_url=self.config.rax_signup.base_url,
            auth_token=auth_token,
            serialize_format=self.config.misc.serializer,
            deserialize_format=deserialize_format,
            ah_endpoint=self.config.atom_hopper_events.ah_endpoint,
            identity_endpoint=self.config.user_identity.identity_endpoint)

    def get_token(self):
        par = self.identity_provider.authenticate()
        auth_token = par.response.entity.token.id
        assert auth_token is not None,\
                "Could not locate an auth token"
        return auth_token
