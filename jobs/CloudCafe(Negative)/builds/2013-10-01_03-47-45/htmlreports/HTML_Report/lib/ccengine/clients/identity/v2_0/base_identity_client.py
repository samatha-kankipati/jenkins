from ccengine.clients.base_client import BaseMarshallingClient


class BaseIdentityClient(BaseMarshallingClient):

    def __init__(self, serialize_format, deserialize_format=None):
        super(BaseIdentityClient, self).__init__(serialize_format,
                                                 deserialize_format)

    @property
    def token(self):
        return self.default_headers.get('X-Auth-Token')

    @token.setter
    def token(self, token):
        self.default_headers['X-Auth-Token'] = token

    @token.deleter
    def token(self):
        del self.default_headers['X-Auth-Token']
