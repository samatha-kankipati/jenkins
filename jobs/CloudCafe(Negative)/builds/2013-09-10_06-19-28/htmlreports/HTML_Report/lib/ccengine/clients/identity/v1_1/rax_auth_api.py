from ccengine.clients.base_client import BaseMarshallingClient
from ccengine.domain.identity.v1_1.request.credentials import Credentials
from ccengine.domain.identity.v1_1.response.auth import Auth
from ccengine.domain.identity.v1_1.response.version import Version


class IdentityClient(BaseMarshallingClient):

    VERSION = 'v1.1'

    def __init__(self, authentication_endpoint, serialize_format=None,
                 deserialize_format=None, auth_token=None):
        self.auth_token = auth_token
        super(IdentityClient, self).__init__(serialize_format,
                                             deserialize_format)
        self.base_url = '{0}/{1}'.format(authentication_endpoint,
                                         self.VERSION)
        self.default_headers['Content-Type'] = \
            'application/{0}'.format(serialize_format)
        if deserialize_format is None:
            deserialize_format = serialize_format
        self.default_headers['Accept'] = 'application/{0}'.\
            format(deserialize_format)

    AUTH = 'auth'

    def get_version_details(self, requestslib_kwargs=None):
        return self.get(self.base_url, response_entity_type=Version,
                        requestslib_kwargs=requestslib_kwargs)

    def authenticate_user(self,
                          username,
                          key,
                          format_extension=None,
                          accept_encoding=None,
                          requestslib_kwargs=None):
        '''
        @summary: Creates authentication using Username and API key.
        @param username: The username of the customer.
        @type username: String
        @param key: The API key.
        @type key: String
        @param format_extension: Format to append to end of url (.json, .xml)
        @type format_extension: String
        @return: Response Object containing auth response
        @rtype: Response Object
        '''
        creds = Credentials(username=username, key=key)

        url = '/'.join([self.base_url, self.AUTH])
        if format_extension:
            url = '{0}{1}'.format(url, format_extension)
        if accept_encoding:
            headers = self.default_headers
            headers['Accept-Encoding'] = accept_encoding
        server_response = self.post(url,
                                    response_entity_type=Auth,
                                    request_entity=creds,
                                    requestslib_kwargs=requestslib_kwargs)
        return server_response
