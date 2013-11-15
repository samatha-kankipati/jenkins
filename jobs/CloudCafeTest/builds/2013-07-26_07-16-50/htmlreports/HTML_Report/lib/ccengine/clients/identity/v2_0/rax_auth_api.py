from ccengine.clients.identity.v2_0.base_identity_client \
    import BaseIdentityClient
from ccengine.domain.identity.v2_0.request.auth import Auth, Token
from ccengine.domain.identity.v2_0.request.credentials \
    import PasswordCredentials as RequestPasswordCredentials, \
    ApiKeyCredentials as RequestApiKeyCredentials
from ccengine.domain.identity.v2_0.request.user import User as RequestUser
from ccengine.domain.identity.v2_0.response.access import Access
from ccengine.domain.identity.v2_0.response.tenant import Tenants
from ccengine.domain.identity.v2_0.response.user import Users, User
from ccengine.domain.identity.v2_0.response.credentials \
    import Credentials, ApiKeyCredentials
from ccengine.domain.identity.v2_0.response.domain import Domains
from ccengine.domain.identity.v2_0.response.role import Roles, Role


class IdentityClient(BaseIdentityClient):
    VERSION = 'v2.0'
    TOKENS = 'tokens'
    TENANTS = 'tenants'
    USERS = 'users'
    RAX_AUTH = 'RAX-AUTH'
    DOMAINS = 'domains'
    OS_KSADM = 'OS-KSADM'
    CREDENTIALS = 'credentials'
    RAX_KSKEY_APIKEYCREDENTIALS = 'RAX-KSKEY:apiKeyCredentials'
    PASSWORD_CREDENTIALS = 'passwordCredentials'
    ROLES = 'roles'
    RESET = 'reset'
    ADMINS = 'admins'

    def __init__(self, url, serialize_format, deserialize_format=None,
                 auth_token=None):
        """returns requests object"""
        super(IdentityClient, self).__init__(serialize_format,
                                             deserialize_format)
        self.base_url = '{0}/{1}'.format(url, self.VERSION)
        self.default_headers['Content-Type'] = \
            'application/{0}'.format(serialize_format)
        self.default_headers['Accept'] = \
            'application/{0}'.format(serialize_format)
        if auth_token is not None:
            self.default_headers['X-Auth-Token'] = auth_token

    def authenticate_user_apikey(self, username, apiKey,
                                 requestslib_kwargs=None):
        """
        @summary: Creates authentication using Username and API key.
        @param username: The username of the customer.
        @type name: String
        @param apiKey: The API key.
        @type apiKey: String
        @return: Response Object containing auth response
        @rtype: Response Object
        """

        """
            POST
            v2.0/tokens
        """
        apiKeyCredentials = RequestApiKeyCredentials(
            username=username,
            apiKey=apiKey)
        auth_request_entity = Auth(
            apiKeyCredentials=apiKeyCredentials)
        url = '{0}/{1}'.format(
            self.base_url,
            self.TOKENS)
        server_response = self.post(
            url,
            response_entity_type=Access,
            request_entity=auth_request_entity,
            requestslib_kwargs=requestslib_kwargs)
        return server_response

    def authenticate_user_apikey_tenant_id(self, username, apiKey, tenantId,
                                           requestslib_kwargs=None):
        """
        @summary: Creates authentication using Username, API key and tenant id.
        @param username: The username of the customer.
        @type username: String
        @param apiKey: The API key.
        @type apiKey: String
        @param tenantId: The tenant id.
        @type tenantId: String
        @return: Response Object containing auth response
        @rtype: Response Object
        """

        """
            POST
            v2.0/tokens
        """
        apiKeyCredentials = RequestApiKeyCredentials(
            username=username,
            apiKey=apiKey)
        auth_request_entity = Auth(
            apiKeyCredentials=apiKeyCredentials,
            tenantId=tenantId)
        url = '{0}/{1}'.format(self.base_url, self.TOKENS)
        server_response = self.post(
            url,
            response_entity_type=Access,
            request_entity=auth_request_entity,
            requestslib_kwargs=requestslib_kwargs)
        return server_response

    def authenticate_user_password(self, username, password,
                                   requestslib_kwargs=None):
        """
        @summary: Creates authentication using Username and password.
        @param username: The username of the customer.
        @type name: String
        @param password: The user password.
        @type password: String
        @return: Response Object containing auth response
        @rtype: Response Object
        """

        """
            POST
            v2.0/tokens
        """
        passwordCredentials = RequestPasswordCredentials(
            username=username,
            password=password)
        auth_request_entity = Auth(passwordCredentials=passwordCredentials)

        url = '{0}/{1}'.format(self.base_url, self.TOKENS)
        server_response = self.post(
            url,
            response_entity_type=Access,
            request_entity=auth_request_entity,
            requestslib_kwargs=requestslib_kwargs)
        return server_response

    def authenticate_user_password_tenant_id(self, username, password,
                                             tenantId,
                                             requestslib_kwargs=None):
        """
        @summary: Authenticates using username, password and tenant id.
        @param username: The username of the customer.
        @type name: String
        @param password: The user password.
        @type password: String
        @param tenantId: The tenant id.
        @type tenantId: String
        @return: Response Object containing auth response
        @rtype: Response Object
        """

        """
            POST
            v2.0/tokens
        """
        passwordCredentials = RequestPasswordCredentials(
            username=username,
            password=password)
        auth_request_entity = Auth(
            passwordCredentials=passwordCredentials,
            tenantId=tenantId)
        url = '{0}/{1}'.format(self.base_url, self.TOKENS)
        server_response = self.post(
            url,
            response_entity_type=Access,
            request_entity=auth_request_entity,
            requestslib_kwargs=requestslib_kwargs)
        return server_response

    def authenticate_tenantid_and_token(self, tenantId, token,
                                        requestslib_kwargs=None):
        """
        @summary: Creates authentication using Tenant id and Token.
        @param tenantName: The Tenant id.
        @type name: String
        @param token: The token of the parent account.
        @type token: String
        @return: Response Object containing auth response
        @rtype: Response Object
        """

        """
            POST
            v2.0/tokens
        """
        token = Token(id=token)
        auth_request_entity = Auth(token=token, tenantId=tenantId)
        url = '{0}/{1}'.format(self.base_url, self.TOKENS)
        server_response = self.post(url, response_entity_type=Access,
                                    request_entity=auth_request_entity,
                                    requestslib_kwargs=requestslib_kwargs)
        return server_response

    def authenticate_tenantname_and_token(self, tenantName, token,
                                          requestslib_kwargs=None):
        """
        @summary: Creates authentication using TenantName and Token.
        @param tenantName: The TenantName which was get from get tenants call.
        @type name: String
        @param token: The token of the parent account.
        @type token: String
        @return: Response Object containing auth response
        @rtype: Response Object
        """

        """
            POST
            v2.0/tokens
        """
        token = Token(id=token)
        auth_request_entity = Auth(token=token, tenantName=tenantName)
        url = '{0}/{1}'.format(self.base_url, self.TOKENS)
        server_response = self.post(
            url,
            response_entity_type=Access,
            request_entity=auth_request_entity,
            requestslib_kwargs=requestslib_kwargs)
        return server_response

    def get_tenants(self, requestslib_kwargs=None):
        """
        @summary: Get tenants for account
        @params: None
        @type name: None
        @return: Tenants response object containing info for tenants
        @rtype: Response Object
        """

        """
            GET
            v2.0/tenants
        """
        url = '{0}/{1}'.format(self.base_url, self.TENANTS)
        server_response = self.get(
            url,
            response_entity_type=Tenants,
            requestslib_kwargs=requestslib_kwargs)
        return server_response

    def list_users(self, marker=None, limit=None, email=None,
                   requestslib_kwargs=None):
        """
        @summary: Get tenants for account
        @params: None
        @type name: None
        @return: Tenants response object containing info for tenants
        @rtype: Response Object
        """

        """
            GET
            v2.0/users
        """
        url = '{0}/{1}'.format(self.base_url, self.USERS)
        params = {'limit': limit, 'marker': marker, 'email': email}
        server_response = self.get(
            url,
            params=params,
            response_entity_type=Users,
            requestslib_kwargs=requestslib_kwargs)
        return server_response

    def get_user_by_name(self, name, requestslib_kwargs=None):
        """
        @summary: Get user by name
        @param name: The user name
        @type name type: String
        @return: User information
        @rtype: Response Object
        """

        """
            GET
            v2.0/users?name=string
        """
        params = {'name': name}
        url = '{0}/{1}'.format(self.base_url, self.USERS)
        server_response = self.get(
            url,
            params=params,
            response_entity_type=User,
            requestslib_kwargs=requestslib_kwargs)
        return server_response

    def get_users_by_email(self, email, requestslib_kwargs=None):
        """
        @summary: Get user by email
        @param email: The user email
        @type email type: String
        @return: User information
        @rtype: Response Object
        """

        """
            GET
            v2.0/users?email=string
        """
        params = {'email': email}
        url = '{0}/{1}'.format(self.base_url, self.USERS)
        server_response = self.get(
            url,
            params=params,
            response_entity_type=Users,
            requestslib_kwargs=requestslib_kwargs)
        return server_response

    def get_user_by_id(self, userId, requestslib_kwargs=None):
        """
        @summary: Get user by id
        @param userId: The user id
        @type userId type: String
        @return: User information
        @rtype: Response Object
        """

        """
            GET
            v2.0/users/{userId}
        """
        url = '{0}/{1}/{2}'.format(self.base_url, self.USERS, userId)
        server_response = self.get(
            url,
            response_entity_type=User,
            requestslib_kwargs=requestslib_kwargs)
        return server_response

    def add_user(self, username, email, enabled=None, password=None,
                 defaultRegion=None, domainId=None, requestslib_kwargs=None):
        """
        @summary: Add user
        @param username: The user name
        @type username type: String
        @return: User information
        @rtype: Response Object
        """

        """
            POST
            v2.0/users
        """
        auth_request_entity = RequestUser(
            username=username,
            email=email,
            enabled=enabled,
            password=password,
            defaultRegion=defaultRegion,
            domainId=domainId)
        url = '{0}/{1}'.format(self.base_url, self.USERS)
        server_response = self.post(
            url,
            response_entity_type=User,
            request_entity=auth_request_entity,
            requestslib_kwargs=requestslib_kwargs)
        return server_response

    def update_user(self, userId, defaultRegion=None, username=None,
                    email=None, enabled=None, password=None,
                    requestslib_kwargs=None):
        """
        @summary: Update user
        @param userId: The user id
        @type userId type: String
        @return: User information
        @rtype: Response Object
        """

        """
            POST
            v2.0/users/{userId}
        """
        auth_request_entity = RequestUser(
            username=username,
            email=email,
            enabled=enabled, password=password,
            defaultRegion=defaultRegion)
        url = '{0}/{1}/{2}'.format(self.base_url, self.USERS, userId)
        server_response = self.post(
            url,
            response_entity_type=User,
            request_entity=auth_request_entity,
            requestslib_kwargs=requestslib_kwargs)
        return server_response

    def delete_user(self, userId, requestslib_kwargs=None):
        """
        @summary: Delete user by id
        @param userId: The user id
        @type userId type: String
        @return: User Delete information
        @rtype: Response Object
        """

        """
            DELETE
            v2.0/users/{userId}
        """
        url = '{0}/{1}/{2}'.format(self.base_url, self.USERS, userId)
        server_response = self.delete(
            url,
            requestslib_kwargs=requestslib_kwargs)
        return server_response

    def get_accessible_domains(self, userId, requestslib_kwargs=None):
        """
        @summary: Get Accessible Domains
        @param userId: The user id
        @type userId type: String
        @return: Accessible Domains
        @rtype: Response Object
        """

        """
            GET
            v2.0/users/{userId}/RAX-AUTH/domains
        """
        url = '{0}/{1}/{2}/{3}/{4}'.format(
            self.base_url,
            self.USERS,
            userId,
            self.RAX_AUTH,
            self.DOMAINS)
        server_response = self.get(
            url,
            response_entity_type=Domains,
            requestslib_kwargs=requestslib_kwargs)
        return server_response

    def list_credentials(self, userId, requestslib_kwargs=None):
        """
        @summary: List user credentials by id
        @param userId: The user id
        @type userId type: String
        @return: User Credentials Information
        @rtype: Response Object
        """

        """
            GET
            v2.0/users/{userId}/OS-KSADM/credentials
        """
        url = '{0}/{1}/{2}/{3}/{4}'.format(
            self.base_url,
            self.USERS,
            userId,
            self.OS_KSADM,
            self.CREDENTIALS)
        server_response = self.get(
            url,
            response_entity_type=Credentials,
            requestslib_kwargs=requestslib_kwargs)
        return server_response

    def get_user_credentials(self, userId, requestslib_kwargs=None):
        """
        @summary: List user credentials by id
        @param userId: The user id
        @type userId type: String
        @return: User Credentials Information
        @rtype: Response Object
        """

        """
        GET
        v2.0/users/{userId}/OS-KSADM/credentials/RAX-KSKEY:apiKeyCredentials
        """
        url = '{0}/{1}/{2}/{3}/{4}/{5}'.format(
            self.base_url,
            self.USERS,
            userId,
            self.OS_KSADM,
            self.CREDENTIALS,
            self.RAX_KSKEY_APIKEYCREDENTIALS)
        server_response = self.get(
            url,
            response_entity_type=ApiKeyCredentials,
            requestslib_kwargs=requestslib_kwargs)
        return server_response

    def list_user_global_roles(self, userId, requestslib_kwargs=None):
        """
        @summary: List user global roles
        @param userId: The user id
        @type userId type: String
        @return: Global Roles Information
        @rtype: Response Object
        """

        """
            GET
            v2.0/users/{userId}/roles
        """
        url = '{0}/{1}/{2}/{3}'.format(
            self.base_url,
            self.USERS,
            userId,
            self.ROLES)
        server_response = self.get(
            url,
            response_entity_type=Roles,
            requestslib_kwargs=requestslib_kwargs)
        return server_response

    def list_users_with_role(self, role_id, limit=None, marker=None,
                             requestslib_kwargs=None):
        """
        @summary: List user with  role
        @param roleId: The role id
        @type roleId type: String
        @return: User List
        @rtype: Response Object
        """

        """
            GET
            v2.0/OS-KSADM/roles/{roleId}/RAX-AUTH/users
        """
        url = "{0}/{1}/{2}/{3}/{4}/{5}".format(
            self.base_url,
            self.OS_KSADM,
            self.ROLES,
            role_id,
            self.RAX_AUTH,
            self.USERS)
        params = {'limit': limit, 'marker': marker}
        server_response = self.get(
            url,
            params=params,
            response_entity_type=Users,
            requestslib_kwargs=requestslib_kwargs)
        return server_response

    def reset_user_api_key(self, userId, requestslib_kwargs=None):
        """
        @summary: Reset user api key
        @param userId: The user id
        @type userId type: String
        @return: Api key
        @rtype: Response Object
        """

        """
            POST
            v2.0/users/{userId}/OS-KSADM/credentials
            /RAX-KSKEY:apiKeyCredentials/RAX-AUTH/reset
        """
        url = '{0}/{1}/{2}/{3}/{4}/{5}/{6}/{7}'.format(
            self.base_url,
            self.USERS,
            userId,
            self.OS_KSADM, self.CREDENTIALS,
            self.RAX_KSKEY_APIKEYCREDENTIALS,
            self.RAX_AUTH, self.RESET)
        api_key = self.post(
            url,
            response_entity_type=Credentials,
            requestslib_kwargs=requestslib_kwargs)
        return api_key

    def show_account_admins(self, userId, requestslib_kwargs=None):
        """
        @summary: Show account admins
        @param userId: The user id
        @type userId type: String
        @return: Global All admins for particular user
        @rtype: Response Object
        """

        """
            GET
            v2.0/users/{userId}/RAX-AUTH/admins
        """
        url = '{0}/{1}/{2}/{3}/{4}'.format(self.base_url, self.USERS, userId,
                                           self.RAX_AUTH, self.ADMINS)
        server_response = self.get(url, response_entity_type=Users,
                                   requestslib_kwargs=requestslib_kwargs)
        return server_response

    def add_role_to_user(self, userId, roleId, requestslib_kwargs=None):
        """
        @summary: Add a specific global role to a user.
        @param userId: The user id
        @type userId type: String
        @param roleId: The role id
        @type roleId type: String
        @return: User info with new Global Role
        @rtype: Response Object
        """

        """
            PUT
            v2.0/users/{userId}/roles/OS-KSADM/{roleId}
        """
        url = '{0}/{1}/{2}/{3}/{4}/{5}'.format(self.base_url, self.USERS,
                                               userId, self.ROLES,
                                               self.OS_KSADM, roleId)
        server_response = self.put(url,
                                   response_entity_type=Role,
                                   requestslib_kwargs=requestslib_kwargs)
        return server_response

    def delete_role_from_user(self, userId, roleId, requestslib_kwargs=None):
        """
        @summary: Delete a specific global role from a user.
        @param userId: The user id
        @type userId type: String
        @param roleId: The role id
        @type roleId type: String
        @return: User without the global role
        @rtype: Response Object
        """

        """
            DELETE
            v2.0/users/{userId}/roles/OS-KSADM/{roleId}
        """
        url = '{0}/{1}/{2}/{3}/{4}/{5}'.format(self.base_url, self.USERS,
                                               userId, self.ROLES,
                                               self.OS_KSADM, roleId)
        server_response = self.delete(url,
                                      requestslib_kwargs=requestslib_kwargs)
        return server_response
