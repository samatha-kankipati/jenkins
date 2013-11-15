import json
from ccengine.clients.base_client import BaseMarshallingClient


class ValkyrieClient(BaseMarshallingClient):

    def __init__(self, url, auth_token, serialize_format=None,
                 deserialize_format=None):
        super(ValkyrieClient, self).__init__(serialize_format,
                                             deserialize_format)
        self.url = url
        self.auth_token = auth_token
        self.default_headers['X-Auth-Token'] = auth_token
        self.default_headers['Content-Type'] = 'application/{0}'.format(
                                               self.serialize_format)
        self.default_headers['Accept'] = 'application/{0}'.format(
                                         self.deserialize_format)

    def get_rack_password_for_server(self, server_id):
        '''
        @summary : Returns the rackspassword of the server
        '''
        url = "{0}/{1}/admin_passwords".format(self.url, server_id)
        response = self.request("GET", url)
        json_resp = json.loads(response.text)
        server_password = json_resp['admin_passwords'][0]['admin_password']
        return server_password