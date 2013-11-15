#from ccengine.common.connectors import rest
from ccengine.clients.base_client import BaseRESTClient
import json


class KeystoneClient(BaseRESTClient):

    def __init__(self, auth_url):
        super(KeystoneClient, self).__init__()
        self.auth_url = auth_url

    def authenticate(self, username, password, tenant_name):
        body = {'auth': {
                'passwordCredentials': {
                    'username': username,
                    'password': password,
                },
                'tenantName': tenant_name
            }
        }
        auth_url = ''.join([self.auth_url, '/v2.0/tokens'])
        headers = {'Content-Type': 'application/json'}
        body = json.dumps(body)
        resp = self.request('POST', auth_url, data=body, headers=headers)

        return resp
