import json
from ccengine.clients.base_client import BaseRESTClient


class AuthClient(BaseRESTClient):

    def __init__(self, url, version, username, api_key=None, password=None):
        '''returns requests object'''
        super(AuthClient, self).__init__()
        self.url = url
        self.version = version
        self.username = username
        self.api_key = api_key
        self.password = password

    def auth_2_0(self):
        full_url = ''.join([self.url, '/v2.0/tokens'])
        if self.api_key is None or len(self.api_key) == 0:
            creds = {'auth': {
                        'passwordCredentials': {
                            'username': self.username,
                            'password': self.password
                        }
                      }
                    }
        else:
            creds = {'auth': {
                        'RAX-KSKEY:apiKeyCredentials': {
                            'username': self.username,
                            'apiKey': self.api_key
                            }
                        }
                     }
        try:
            body = json.dumps(creds)
        except:
            print('Error converting auth config options to a serialized '
                   'request body')
            raise

        headers = {'Content-Type': 'application/json',
                   'Accept': 'application/json'}

        return self.request('POST', full_url, data=body, headers=headers)

    def auth_1_1(self):
        '''Authenticates with AuthToken 1.1.'''
        full_url = ''.join([self.url, '/v1.1/auth'])
        creds = {'credentials': {
                    'username': self.username,
                    'key': self.api_key
                    }
                }
        try:
            body = json.dumps(creds)
        except:
            print('Error converting auth config options to a serialized '
                  'request body')
            raise

        headers = {'Content-Type': 'application/json',
                   'Accept': 'application/json'}

        return self.request('POST', full_url, data=body, headers=headers)

    def auth_core(self):
        '''Authentication for Core application'''
        full_url = '{0}/login/{1}'.format(self.url, self.username)
        params = {'password': self.password}
        try:
            body = json.dumps(params)
        except:
            raise Exception('Error converting auth config options\
                             to a serialized request body')
        headers = {'Content-Type': 'application/json',
                   'Accept': 'application/json'}

        auth_token = self.request('POST', full_url, data=body, headers=headers)
        return auth_token

    def auth_2_0_internal(self):
        full_url = ''.join([self.url, '/v2.0/tokens'])
        if self.api_key is None or len(self.api_key) == 0:
            creds = {'auth':
                        {"RAX-AUTH:domain": {
                            "name": "Rackspace"
                        },
                        'passwordCredentials': {
                            'username': self.username,
                            'password': self.password
                        }
                      }
                    }

        try:
            body = json.dumps(creds)
        except:
            print('Error converting auth config options to a serialized '
                   'request body')
            raise

        headers = {'Content-Type': 'application/json',
                   'Accept': 'application/json'}

        return self.request('POST', full_url, data=body, headers=headers)
