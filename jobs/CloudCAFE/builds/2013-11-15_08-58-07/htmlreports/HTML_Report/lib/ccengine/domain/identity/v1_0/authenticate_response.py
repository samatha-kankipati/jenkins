from ccengine.domain.base_domain import BaseDomain


class AuthResponse(BaseDomain):

    def __init__(self, x_powered_by=None, x_storage_token=None,
                 x_storage_url=None, x_server_management_url=None,
                 x_cdn_management_url=None, x_auth_token=None):
        super(AuthResponse, self).__init__()
        self.x_powered_by = x_powered_by
        self.x_storage_token = x_storage_token
        self.x_storage_url = x_storage_url
        self.x_server_management_url = x_server_management_url
        self.x_cdn_management_url = x_cdn_management_url
        self.x_auth_token = x_auth_token

    @classmethod
    def load(cls, headers):
        return AuthResponse(
                x_powered_by=headers.get('X-Powered-By'),
                x_storage_token=headers.get('X-Storage-Token'),
                x_storage_url=headers.get('X-Storage-Url'),
                x_server_management_url=headers.get('X-Server-Management-Url'),
                x_cdn_management_url=headers.get('X-CDN-Management-Url'),
                x_auth_token=headers.get('X-Auth-Token'))
