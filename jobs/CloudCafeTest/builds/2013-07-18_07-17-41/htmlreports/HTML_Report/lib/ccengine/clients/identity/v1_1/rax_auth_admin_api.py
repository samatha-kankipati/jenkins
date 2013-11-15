import base64
from ccengine.clients.base_client import BaseMarshallingClient
from ccengine.domain.identity.v1_1.request.credentials \
    import MossoCredentials, NastCredentials, PasswordCredentials
from ccengine.domain.identity.v1_1.response.auth import Auth, ServiceCatalog
from ccengine.domain.identity.v1_1.response.token import Token
from ccengine.domain.identity.v1_1.request.user import User as RequestUser
from ccengine.domain.identity.v1_1.response.user import User as ResponseUser
from ccengine.domain.identity.v1_1.response.group import Groups
from ccengine.domain.identity.v1_1.response.base_url import BaseURLs, \
    BaseURL as ResponseBaseURL, BaseURLRefs, BaseURLRef as ResponseBaseURLRef
from ccengine.domain.identity.v1_1.request.base_url \
    import BaseURLRef as RequestBaseURLRef
from ccengine.domain.identity.v1_1.request.base_url \
    import BaseURL as RequestBaseURL
from ccengine.domain.identity.v1_1.response.extension import Extensions


class IdentityAdminClient(BaseMarshallingClient):

    VERSION = 'v1.1'
    #Using auth redirects to auth-admin.  Requests changes the method from POST
    #to GET when this redirect happens.
    #AUTH = 'auth'
    AUTH = 'auth-admin'
    TOKEN = 'token'
    USERS = 'users'
    ENABLED = 'enabled'
    GROUPS = 'groups'
    SERVICE_CATALOG = 'serviceCatalog'
    KEY = 'key'
    NAST = 'nast'
    MOSSO = 'mosso'
    BASE_URLS = 'baseURLs'
    BASE_URL_REFS = 'baseURLRefs'
    EXTENSIONS = 'extensions'

    def __init__(self, url, user, password, serialize_format=None,
                 deserialize_format=None, auth_token=None):
        super(IdentityAdminClient, self).__init__(serialize_format,
                                                  deserialize_format)
        self.base_url = '{0}/{1}'.format(url, self.VERSION)
        encrypted_password = \
            base64.encodestring('{0}:{1}'.format(user, password))[:-1]
        self.default_headers['Authorization'] = \
            'Basic {0}'.format(encrypted_password)
        content_type = 'application/{0}'.format(self.serialize_format)
        accept = 'application/{0}'.format(self.deserialize_format)
        self.default_headers['Content-Type'] = content_type
        self.default_headers['Accept'] = accept

    def authenticate_mosso(self, mossoId, key, requestslib_kwargs=None):
        url = '{0}/{1}'.format(self.base_url, self.AUTH)
        mosso_creds = MossoCredentials(mossoId=mossoId, key=key)
        return self.post(url,
                         request_entity=mosso_creds,
                         response_entity_type=Auth,
                         requestslib_kwargs=requestslib_kwargs)

    def authenticate_nast(self, nastId, key, requestslib_kwargs=None):
        url = '{0}/{1}'.format(self.base_url, self.AUTH)
        nast_creds = NastCredentials(nastId=nastId, key=key)
        return self.post(url,
                         request_entity=nast_creds,
                         response_entity_type=Auth,
                         requestslib_kwargs=requestslib_kwargs)

    def authenticate_password(self, username, password,
                              requestslib_kwargs=None):
        url = '{0}/{1}'.format(self.base_url, self.AUTH)
        pw_creds = PasswordCredentials(username=username, password=password)
        return self.post(url,
                         request_entity=pw_creds,
                         response_entity_type=Auth,
                         requestslib_kwargs=requestslib_kwargs)

    def get_token(self, tokenId, requestslib_kwargs=None):
        url = '{0}/{1}/{2}'.format(self.base_url, self.TOKEN, tokenId)
        return self.get(url,
                        response_entity_type=Token,
                        requestslib_kwargs=requestslib_kwargs)

    def validate_token(self, tokenId, belongsTo=None, type=None,
                       requestslib_kwargs=None):
        params = {}
        if belongsTo:
            params['belongsTo'] = belongsTo
        if type:
            params['type'] = type
        url = '{0}/{1}/{2}'.format(self.base_url, self.TOKEN, tokenId)
        return self.get(url,
                        params=params,
                        response_entity_type=Token,
                        requestslib_kwargs=requestslib_kwargs)

    def revoke_token(self, tokenId, requestslib_kwargs=None):
        url = '{0}/{1}/{2}'.format(self.base_url, self.TOKEN, tokenId)
        return self.delete(url, requestslib_kwargs=requestslib_kwargs)

    def create_user(self, id, key, mossoId, enabled, nastId=None,
                    requestslib_kwargs=None):
        url = '{0}/{1}'.format(self.base_url, self.USERS)
        user = RequestUser(id=id, key=key, mossoId=mossoId, nastId=nastId,
                           enabled=enabled)
        return self.post(url,
                         request_entity=user,
                         response_entity_type=ResponseUser,
                         requestslib_kwargs=requestslib_kwargs)

    def get_user(self, userId, requestslib_kwargs=None):
        url = '{0}/{1}/{2}'.format(self.base_url, self.USERS, userId)
        return self.get(url,
                        response_entity_type=ResponseUser,
                        requestslib_kwargs=requestslib_kwargs)

    def get_user_enabled(self, userId, requestslib_kwargs=None):
        url = '{0}/{1}/{2}/{3}'.format(self.base_url, self.USERS, userId,
                                       self.ENABLED)
        return self.get(url,
                        response_entity_type=ResponseUser,
                        requestslib_kwargs=requestslib_kwargs)

    def get_user_groups(self, userId, requestslib_kwargs=None):
        url = '{0}/{1}/{2}/{3}'.format(self.base_url, self.USERS, userId,
                                       self.GROUPS)
        return self.get(url,
                        response_entity_type=Groups,
                        requestslib_kwargs=requestslib_kwargs)

    def get_user_service_catalog(self, userId, requestslib_kwargs=None):
        url = '{0}/{1}/{2}/{3}'.format(self.base_url, self.USERS, userId,
                                       self.SERVICE_CATALOG)
        return self.get(url,
                        response_entity_type=ServiceCatalog,
                        requestslib_kwargs=requestslib_kwargs)

    def update_user(self, userId, id=None, key=None, mossoId=None, nastId=None,
                    enabled=None, requestslib_kwargs=None):
        url = '{0}/{1}/{2}'.format(self.base_url, self.USERS, userId)
        user = RequestUser(id=id, key=key, mossoId=mossoId, nastId=nastId,
                           enabled=enabled)
        return self.put(url,
                        request_entity=user,
                        response_entity_type=ResponseUser,
                        requestslib_kwargs=requestslib_kwargs)

    def update_user_enabled(self, userId, enabled=None,
                            requestslib_kwargs=None):
        url = '{0}/{1}/{2}/{3}'.format(self.base_url, self.USERS, userId,
                                       self.ENABLED)
        user = RequestUser(enabled=enabled)
        return self.put(url,
                        request_entity=user,
                        response_entity_type=ResponseUser,
                        requestslib_kwargs=requestslib_kwargs)

    def delete_user(self, userId, requestslib_kwargs=None):
        url = '{0}/{1}/{2}'.format(self.base_url, self.USERS, userId)
        return self.delete(url, requestslib_kwargs=requestslib_kwargs)

    def get_user_key(self, userId, requestslib_kwargs=None):
        url = '{0}/{1}/{2}/{3}'.format(self.base_url, self.USERS, userId,
                                       self.KEY)
        return self.get(url,
                        response_entity_type=ResponseUser,
                        requestslib_kwargs=requestslib_kwargs)

    def set_user_key(self, userId, key, requestslib_kwargs=None):
        url = '{0}/{1}/{2}/{3}'.format(self.base_url, self.USERS, userId,
                                       self.KEY)
        user = RequestUser(key=key)
        return self.put(url,
                        request_entity=user,
                        response_entity_type=ResponseUser,
                        requestslib_kwargs=requestslib_kwargs)

    def get_user_by_nast_id(self, nastId, requestslib_kwargs=None):
        url = '{0}/{1}/{2}'.format(self.base_url, self.NAST, nastId)
        return self.get(url,
                        response_entity_type=ResponseUser,
                        requestslib_kwargs=requestslib_kwargs)

    def get_user_by_mosso_id(self, mossoId, requestslib_kwargs=None):
        url = '{0}/{1}/{2}'.format(self.base_url, self.MOSSO, mossoId)
        return self.get(url,
                        response_entity_type=ResponseUser,
                        requestslib_kwargs=requestslib_kwargs)

    def list_base_urls_enabled(self, serviceName=None,
                               requestslib_kwargs=None):
        params = {}
        if serviceName:
            params['serviceName'] = serviceName
        url = '{0}/{1}/{2}'.format(self.base_url, self.BASE_URLS, self.ENABLED)
        return self.get(url, params=params,
                        response_entity_type=BaseURLs,
                        requestslib_kwargs=requestslib_kwargs)

    def list_base_urls(self, serviceName=None, requestslib_kwargs=None):
        params = {}
        if serviceName:
            params['serviceName'] = serviceName
        url = '{0}/{1}'.format(self.base_url, self.BASE_URLS)
        return self.get(url, params=params,
                        response_entity_type=BaseURLs,
                        requestslib_kwargs=requestslib_kwargs)

    def get_base_url(self, baseURLId, requestslib_kwargs=None):
        url = '{0}/{1}/{2}'.format(self.base_url, self.BASE_URLS, baseURLId)
        return self.get(url,
                        response_entity_type=ResponseBaseURL,
                        requestslib_kwargs=requestslib_kwargs)

    def get_user_base_urls(self, userId, requestslib_kwargs=None):
        url = '{0}/{1}/{2}/{3}'.format(self.base_url, self.USERS, userId,
                                       self.BASE_URL_REFS)
        return self.get(url,
                        response_entity_type=BaseURLRefs,
                        requestslib_kwargs=requestslib_kwargs)

    def add_user_base_url(self, userId, id, v1Default,
                          requestslib_kwargs=None):
        url = '{0}/{1}/{2}/{3}'.format(self.base_url, self.USERS, userId,
                                       self.BASE_URL_REFS)
        base_url = RequestBaseURLRef(id=id, v1Default=v1Default)
        return self.post(url,
                         request_entity=base_url,
                         response_entity_type=ResponseBaseURLRef,
                         requestslib_kwargs=requestslib_kwargs)

    def delete_user_base_url(self, userId, baseURLId,
                             requestslib_kwargs=None):
        url = '{0}/{1}/{2}/{3}/{4}'.format(self.base_url, self.USERS, userId,
                                           self.BASE_URL_REFS, baseURLId)
        return self.delete(url, requestslib_kwargs=requestslib_kwargs)

    def list_extensions(self, requestslib_kwargs=None):
        url = '{0}/{1}'.format(self.base_url, self.EXTENSIONS)
        return self.get(url,
                        response_entity_type=Extensions,
                        requestslib_kwargs=requestslib_kwargs)

    def list_extensions_by_alias(self, alias, requestslib_kwargs=None):
        url = '{0}/{1}/{2}'.format(self.base_url, self.EXTENSIONS, alias)
        return self.get(url, response_entity_type=Extensions,
                        requestslib_kwargs=requestslib_kwargs)

    def add_base_url(self, id, userType, region, serviceName, 
            publicURL, internalURL, adminURL, default, enabled, 
            requestslib_kwargs=None):
        url = '{0}/{1}'.format(self.base_url, self.BASE_URLS)

        baseUrlRequest = RequestBaseURL(id=id, userType=userType, region=region,
                serviceName=serviceName, publicURL=publicURL, 
                internalURL=internalURL, adminURL=adminURL,
                default=default, enabled=enabled)
        return self.post(url, 
                request_entity=baseUrlRequest,
                response_entity_type=None,
                requestslib_kwargs=requestslib_kwargs)
