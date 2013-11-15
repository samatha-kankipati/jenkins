from ccengine.clients.base_client import BaseRESTClient
from ccengine.domain.identity.v1_0.authenticate_response import AuthResponse

class IdentityClient(BaseRESTClient):

    VERSION = 'v1.0'

    def __init__(self, url):
        super(IdentityClient, self).__init__()
        self.base_url = '{0}/{1}'.format(url, self.VERSION)

    def authenticate(self, x_auth_user, x_auth_key):
        headers = {'X-Auth-User': x_auth_user,
                   'X-Auth-Key': x_auth_key}
        resp = self.get(self.base_url, headers=headers)
        resp.__dict__['entity'] = AuthResponse.load(resp.headers)
        return resp

    def authenticate_storage(self, x_storage_user, x_storage_pass):
        headers = {'X-Storage-User': x_storage_user,
                   'X-Storage-Pass': x_storage_pass}
        resp = self.get(self.base_url, headers=headers)
        resp.__dict__['entity'] = AuthResponse.load(resp.headers)
        return resp
