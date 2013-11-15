from ccengine.clients.base_client import BaseMarshallingClient
from ccengine.domain.identity.v2_0.request.auth import Auth as AuthRequest
from ccengine.domain.identity.v2_0.request.credentials \
    import ApiKeyCredentials, PasswordCredentials
from ccengine.domain.identity.v2_0.response.access import\
                                                    Access as AuthResponse


class IdentityClient(BaseMarshallingClient):

    def __init__(self, authentication_endpoint, serialize_format=None,
                    deserialize_format=None):
        '''returns requests object'''
        super(IdentityClient, self).__init__(serialize_format,
                                                deserialize_format)
        self.authentication_endpoint = '%s%s' % (authentication_endpoint,
                                                    '/v2.0/tokens')
        self.default_headers['Content-Type'] = \
                                    'application/%s' % str(serialize_format)
        self.default_headers['Accept'] = \
                                    'application/%s' % str(serialize_format)

    def authenticate_api_key(self, username=None, api_key=None,
                             requestslib_kwargs=None):

        api_creds = ApiKeyCredentials(username=username, apiKey=api_key)
        request_entity = AuthRequest(apiKeyCredentials=api_creds)
        return self.post(self.authentication_endpoint,
                         request_entity=request_entity,
                         response_entity_type=AuthResponse,
                         requestslib_kwargs=requestslib_kwargs)

    def authenticate_password(self, username, password=None,
                                requestslib_kwargs=None):

        pw_creds = PasswordCredentials(username=username, password=password)
        request_entity = AuthRequest(passwordCredentials=pw_creds)
        return self.post(self.authentication_endpoint,
                         response_entity_type=AuthResponse,
                         request_entity=request_entity,
                         requestslib_kwargs=requestslib_kwargs)
