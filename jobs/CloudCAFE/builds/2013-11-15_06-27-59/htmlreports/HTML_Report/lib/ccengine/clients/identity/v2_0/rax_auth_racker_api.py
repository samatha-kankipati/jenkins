from ccengine.clients.identity.v2_0.rax_auth_admin_api \
    import IdentityAdminClient
from ccengine.domain.identity.v2_0.request.auth import Auth
from ccengine.domain.identity.v2_0.response.access import Access
from ccengine.domain.identity.v2_0.request.credentials \
    import RackerPasswordCredentials


class RackerClient(IdentityAdminClient):

    VERSION = 'v2.0'
    TOKENS = 'tokens'

    def __init__(self, url, serialize_format, deserialize_format=None,
                 auth_token=None):
        '''returns requests object'''
        super(RackerClient, self).__init__(serialize_format,
                                           deserialize_format)
        self.base_url = '{0}/{1}'.format(url, self.VERSION)
        self.default_headers['Content-Type'] = \
            'application/{0}'.format(serialize_format)
        self.default_headers['Accept'] = \
            'application/{0}'.format(serialize_format)
        if auth_token is not None:
            self.default_headers['X-Auth-Token'] = auth_token

    def authenticate_racker(self, username, password, requestslib_kwargs=None):

        '''
        @summary: Creates authentication using SSO username and password
        @param username: The username of a racker
        @type username: String
        @param password: The password of a racker
        @type password: String
        @return: Response Object containing auth response
        @rtype: Response Object
        '''

        '''
            POST
            v2.0/tokens
        '''
        password_credentials = RackerPasswordCredentials(
            username=username,
            password=password)
        auth_request_entity = Auth(
            rackerPasswordCredentials=password_credentials)
        url = '{0}/{1}'.format(self.base_url, self.TOKENS)
        server_response = self.post(
            url,
            response_entity_type=Access,
            request_entity=auth_request_entity,
            requestslib_kwargs=requestslib_kwargs)
        return server_response
