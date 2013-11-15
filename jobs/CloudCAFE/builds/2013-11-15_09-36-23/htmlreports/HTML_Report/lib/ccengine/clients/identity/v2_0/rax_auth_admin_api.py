from ccengine.clients.identity.v2_0.rax_auth_api import IdentityClient
from ccengine.domain.identity.v2_0.request.role import Role as RequestRole
from ccengine.domain.identity.v2_0.request.credentials \
    import PasswordCredentials as RequestPasswordCredentials, \
        ApiKeyCredentials as RequestApiKeyCredentials
from ccengine.domain.identity.v2_0.request.endpoint_template \
    import EndpointTemplate as RequestEndpointTemplate
from ccengine.domain.identity.v2_0.request.rate_limit \
    import RateLimit as RequestRateLimit
from ccengine.domain.identity.v2_0.request.tenant \
    import Tenant as RequestTenant
from ccengine.domain.identity.v2_0.request.impersonation \
    import Impersonation as RequestImpersonation
from ccengine.domain.identity.v2_0.request.domain \
    import Domain as RequestDomain
from ccengine.domain.identity.v2_0.request.policy \
    import Policy as RequestPolicy
from ccengine.domain.identity.v2_0.request.region_service \
    import DefaultRegionServices as RequestDefaultRegionServices
from ccengine.domain.identity.v2_0.request.capability \
    import Capabilities as RequestCapabilities, Capability as RequestCapability
from ccengine.domain.identity.v2_0.request.group import Group as RequestGroup
from ccengine.domain.identity.v2_0.request.question \
    import Question as RequestQuestion
from ccengine.domain.identity.v2_0.request.secret_qa \
    import SecretQA as RequestSecretQA, UpdateSecretQA
from ccengine.domain.identity.v2_0.response.tenant import Tenants, Tenant \
    as ResponseTenant
from ccengine.domain.identity.v2_0.response.user import Users
from ccengine.domain.identity.v2_0.response.role import Roles, Role
from ccengine.domain.identity.v2_0.response.credentials \
    import ApiKeyCredentials, PasswordCredentials
from ccengine.domain.identity.v2_0.response.secret_qa \
    import SecretQAs, SecretQA
from ccengine.domain.identity.v2_0.response.question import Questions, Question
from ccengine.domain.identity.v2_0.response.endpoint import Endpoints
from ccengine.domain.identity.v2_0.response.endpoint_template \
    import EndpointTemplate as ResponseEndpointTemplate
from ccengine.domain.identity.v2_0.response.domain import Domains, Domain
from ccengine.domain.identity.v2_0.response.policy import Policies, Policy
from ccengine.domain.identity.v2_0.response.rate_limit import RateLimit
from ccengine.domain.identity.v2_0.response.access import Access
from ccengine.domain.identity.v2_0.response.service_api import ServiceAPIs
from ccengine.domain.identity.v2_0.response.capability import Capabilities
from ccengine.domain.identity.v2_0.response.group import Groups, Group
from ccengine.domain.identity.v2_0.response.region_service \
    import DefaultRegionServices
from ccengine.domain.identity.v2_0.response.extension \
    import Extensions, Extension


class IdentityAdminClient(IdentityClient):

    RAX_GRPADM = 'RAX-GRPADM'
    GROUPS = 'groups'
    RAX_KSGRP = 'RAX-KSGRP'
    ENDPOINTS = 'endpoints'
    RAX_KSQA = 'RAX-KSQA'
    SECRETQA = 'secretqa'
    SECRETQAS = 'secretqas'
    QUESTIONS = 'questions'
    IMPERSONATION_TOKENS = 'impersonation-tokens'
    RTADM = 'rtadm'
    DEFAULT_REGION = 'default-region'
    SERVICES = 'services'
    POLICIES = 'policies'
    SERVICE_APIS = 'service-apis'
    CAPABILITIES = 'capabilities'
    BLOB = 'blob_detail'
    EXTENSIONS = 'extensions'
    OS_KSCATALOG = 'OS-KSCATALOG'
    ENDPOINT_TEMPLATES = 'endpointTemplates'

    def list_roles(self, limit=None, marker=None, service_id=None,
                   requestslib_kwargs=None):

        '''
        @summary: List roles
        @return: Global Roles Information
        @rtype: Response Object
        '''

        '''
            GET
            v2.0/OS-KSADM/roles
        '''

        url = '{0}/{1}/{2}'.format(self.base_url, self.OS_KSADM, self.ROLES)
        params = {'limit': limit, 'marker': marker, 'service_id': service_id}

        server_response = self.get(url,
                                   params=params,
                                   response_entity_type=Roles,
                                   requestslib_kwargs=requestslib_kwargs)
        return server_response

    def add_role(self, name, weight=None, propagate=None,
                 description=None, requestslib_kwargs=None):

        '''
        @summary: Add roles
        @param name: The name of the role
        @type name type: String
        @param description: Description of the role
        @type description type: String
        @return: Global Roles Information
        @rtype: Response Object
        '''

        '''
            POST
            v2.0/OS-KSADM/roles
        '''
        auth_request_entity = RequestRole(name=name,
                                          propagate=propagate,
                                          weight=weight,
                                          description=description)
        url = '{0}/{1}/{2}'.format(self.base_url, self.OS_KSADM, self.ROLES)
        server_response = self.post(url,
                                    response_entity_type=Role,
                                    request_entity=auth_request_entity,
                                    requestslib_kwargs=requestslib_kwargs)
        return server_response

    def get_role(self, role_id, requestslib_kwargs=None):

        '''
        @summary: Get role
        @param role_id: The Role ID
        @type userId type: String
        @return: Global Roles Information
        @rtype: Response Object
        '''

        '''
            GET
            v2.0/OS-KSADM/roles/{role_id}
        '''
        url = '{0}/{1}/{2}/{3}'.format(self.base_url, self.OS_KSADM,
                                       self.ROLES, role_id)
        server_response = self.get(url,
                                   response_entity_type=Role,
                                   requestslib_kwargs=requestslib_kwargs)
        return server_response

    def delete_role(self, role_id, requestslib_kwargs=None):

        '''
        @summary: Delete role
        @param role_id: The role id
        @type userId type: String
        @return: Global Roles Information
        @rtype: Response Object
        '''

        '''
            DELETE
            v2.0/OS-KSADM/roles/{role_id}
        '''
        url = '{0}/{1}/{2}/{3}'.format(self.base_url, self.OS_KSADM,
                                       self.ROLES, role_id)
        server_response = self.delete(url,
                                      response_entity_type=Role,
                                      requestslib_kwargs=requestslib_kwargs)
        return server_response



    def get_accessible_domain_endpoints(self, user_id, domain_id,
                                        requestslib_kwargs=None):

        '''
        @summary: Get Accessible Domain Endpoints
        @param user_id: The user id
        @type user_id type: String
        @param domain_id: The domain id
        @type domain_id type: String
        @return: Accessible Domains
        @rtype: Response Object
        '''

        '''
            GET
            v2.0/users/{user_id}/RAX-AUTH/domains/{domain_id}/endpoints
        '''
        url = '{0}/{1}/{2}/{3}/{4}/{5}/{6}'.format(self.base_url, self.USERS,
                                                   user_id, self.RAX_AUTH,
                                                   self.DOMAINS, domain_id,
                                                   self.ENDPOINTS)
        server_response = self.get(url,
                                   response_entity_type=Endpoints,
                                   requestslib_kwargs=requestslib_kwargs)
        return server_response

    def add_user_credentials(self, user_id, username, password,
                             requestslib_kwargs=None):

        '''
        @summary: Add user credentials
        @param username: The username
        @type username type: String
        @return: User Credentials Information
        @rtype: Response Object
        '''

        '''
            POST
            v2.0/users/{user_id}/OS-KSADM/credentials
        '''
        auth_request_entity = RequestPasswordCredentials(username=username,
                                                         password=password)

        url = '{0}/{1}/{2}/{3}/{4}'.format(self.base_url, self.USERS, user_id,
                                           self.OS_KSADM, self.CREDENTIALS)
        server_response = self.post(url,
                                    response_entity_type=PasswordCredentials,
                                    request_entity=auth_request_entity,
                                    requestslib_kwargs=requestslib_kwargs)
        return server_response

    def update_user_credentials(self, user_id, username, api_key,
                                requestslib_kwargs=None):

        '''
        @summary: Update user credentials
        @param username: The username
        @type username type: String
        @return: User Credentials Information
        @rtype: Response Object
        '''

        '''
            POST
            v2.0/users/{user_id}/OS-KSADM/credentials
            /RAX-KSKEY:apiKeyCredentials
        '''
        auth_request_entity = RequestApiKeyCredentials(username=username,
                                                       apiKey=api_key)

        url = '{0}/{1}/{2}/{3}/{4}/{5}'.format(self.base_url, self.USERS, user_id,
                                           self.OS_KSADM, self.CREDENTIALS,
                                           self.RAX_KSKEY_APIKEYCREDENTIALS)
        server_response = self.post(url,
                                    response_entity_type=ApiKeyCredentials,
                                    request_entity=auth_request_entity,
                                    requestslib_kwargs=requestslib_kwargs)
        return server_response

    def update_user_credentials_password(self, user_id, username, password,
                                requestslib_kwargs=None):

        '''
        @summary: Update user credentials
        @param username: The username
        @type username type: String
        @return: User Credentials Information
        @rtype: Response Object
        '''

        '''
            POST
            v2.0/users/{user_id}/OS-KSADM/credentials
            /passwordCredentials
        '''
        auth_request_entity = RequestPasswordCredentials(username=username,
                                                       password=password)

        url = '{0}/{1}/{2}/{3}/{4}/{5}'.format(self.base_url, self.USERS, user_id,
                                           self.OS_KSADM, self.CREDENTIALS,
                                           self.PASSWORD_CREDENTIALS)
        server_response = self.post(url,
                                    response_entity_type=PasswordCredentials,
                                    request_entity=auth_request_entity,
                                    requestslib_kwargs=requestslib_kwargs)
        return server_response

    def get_user_credentials_password(self, user_id, requestslib_kwargs=None):

        '''
        @summary: Get user credentials
        @param username: The username
        @type username type: String
        @return: User Credentials Information
        @rtype: Response Object
        '''

        '''
            POST
            v2.0/users/{user_id}/OS-KSADM/credentials
            /passwordCredentials
        '''
        auth_request_entity = RequestPasswordCredentials()

        url = '{0}/{1}/{2}/{3}/{4}/{5}'.format(self.base_url,
                                               self.USERS,
                                               user_id,
                                               self.OS_KSADM,
                                               self.CREDENTIALS,
                                               self.PASSWORD_CREDENTIALS)
        server_response = self.get(url,
                                   response_entity_type=PasswordCredentials,
                                   requestslib_kwargs=requestslib_kwargs)
        return server_response

    def delete_user_credentials(self, user_id, requestslib_kwargs=None):

        '''
        @summary: Delete user credentials
        @param user_id: The user id
        @type user_id type: String
        @return: Only status code
        @rtype: Response Object entity empty
        '''

        '''
            DELETE
            v2.0/users/{user_id}/OS-KSADM/credentials
            /RAX-KSKEY:apiKeyCredentials
        '''
        url = '{0}/{1}/{2}/{3}/{4}/{5}'.format(
                self.base_url, self.USERS,
                user_id, self.OS_KSADM,
                self.CREDENTIALS,
                self.RAX_KSKEY_APIKEYCREDENTIALS)
        server_response = self.delete(url,
                                      requestslib_kwargs=requestslib_kwargs)
        return server_response

    def get_groups(self, marker=None, limit=None, name=None,
                   requestslib_kwargs=None):

        '''
        @summary: Get groups
        @param marker: The marker param is optional
        @type marker type: String
        @return: Groups
        @rtype: Response Object entity groups
        '''

        '''
            GET
            v2.0/RAX-GRPADM/groups
        '''
        params = {'name': name,
                  'limit': limit,
                  'marker': marker}

        url = '{0}/{1}/{2}'.format(self.base_url, self.RAX_GRPADM, self.GROUPS)
        server_response = self.get(url, params=params,
                                   response_entity_type=Groups,
                                   requestslib_kwargs=requestslib_kwargs)
        return server_response

    def get_group(self, group_id, requestslib_kwargs=None):

        '''
        @summary: Get group
        @param group_id: The group id
        @type userId type: String
        @return: Group
        @rtype: Response Object entity group
        '''

        '''
            GET
            v2.0/RAX-GRPADM/groups/{group_id}
        '''
        url = '{0}/{1}/{2}/{3}'.format(self.base_url, self.RAX_GRPADM,
                                       self.GROUPS, group_id)
        server_response = self.get(url,
                                   response_entity_type=Group,
                                   requestslib_kwargs=requestslib_kwargs)
        return server_response

    def add_group(self, name, description, requestslib_kwargs=None):

        '''
        @summary: Add group
        @param name: The name of the group
        @type name type: String
        @return: Group Information
        @rtype: Response Object
        '''

        '''
            POST
            v2.0/RAX-GRPADM/groups
        '''
        auth_request_entity = RequestGroup(name=name,
                                           description=description)

        url = '{0}/{1}/{2}'.format(self.base_url, self.RAX_GRPADM, self.GROUPS)
        server_response = self.post(url,
                                    response_entity_type=Group,
                                    request_entity=auth_request_entity,
                                    requestslib_kwargs=requestslib_kwargs)
        return server_response

    def update_group(self, group_id, name, description,
                     requestslib_kwargs=None):

        '''
        @summary: Update group
        @param group_id: The id of the group
        @type group_id type: String
        @param name: The name of the group
        @type name type: String
        @return: Group Information
        @rtype: Response Object
        '''

        '''
            PUT
            v2.0/RAX-GRPADM/groups/{group_id}
        '''
        auth_request_entity = RequestGroup(name=name,
                                           description=description)

        url = '{0}/{1}/{2}/{3}'.format(self.base_url, self.RAX_GRPADM,
                                       self.GROUPS, group_id)
        server_response = self.put(url,
                                   response_entity_type=Group,
                                   request_entity=auth_request_entity,
                                   requestslib_kwargs=requestslib_kwargs)
        return server_response

    def delete_group(self, group_id, requestslib_kwargs=None):

        '''
        @summary: Delete group
        @param group_id: The id of the group
        @type group_id type: String
        @return: Group Information
        @rtype: Response Object
        '''

        '''
            DELETE
            v2.0/RAX-GRPADM/groups/{group_id}
        '''
        url = '{0}/{1}/{2}/{3}'.format(self.base_url, self.RAX_GRPADM,
                                       self.GROUPS, group_id)
        server_response = self.delete(url,
                                      requestslib_kwargs=requestslib_kwargs)
        return server_response

    def list_groups_for_user(self, user_id, requestslib_kwargs=None):

        '''
        @summary: List group for users
        @param user_id: The id of the user
        @type user_id type: String
        @return: Group Information
        @rtype: Response Object
        '''

        '''
            GET
            v2.0/users/{user_id}/RAX-KSGRP
        '''
        url = '{0}/{1}/{2}/{3}'.format(self.base_url, self.USERS, user_id,
                                       self.RAX_KSGRP)
        server_response = self.get(url,
                                   response_entity_type=Groups,
                                   requestslib_kwargs=requestslib_kwargs)
        return server_response

    def add_user_to_group(self, group_id, user_id, requestslib_kwargs=None):

        '''
        @summary: Add user to group
        @param group_id: The id of the group
        @type group_id type: String
        @param user_id: The id of the user
        @type user_id type: String
        @return: Group Information
        @rtype: Response Object
        '''

        '''
            PUT
            v2.0/RAX-GRPADM/groups/{group_id}/users/{user_id}
        '''
        url = '{0}/{1}/{2}/{3}/{4}/{5}'.format(self.base_url, self.RAX_GRPADM,
                                               self.GROUPS, group_id,
                                               self.USERS, user_id)
        server_response = self.put(url,
                                   requestslib_kwargs=requestslib_kwargs)
        return server_response

    def remove_user_from_group(self, group_id, user_id, requestslib_kwargs=None):

        '''
        @summary: Remove user from group
        @param group_id: The id of the group
        @type group_id type: String
        @param user_id: The id of the user
        @type user_id type: String
        @return: Group Information
        @rtype: Response Object
        '''

        '''
            DELETE
            v2.0/RAX-GRPADM/groups/{group_id}/users/{user_id}
        '''
        url = '{0}/{1}/{2}/{3}/{4}/{5}'.format(self.base_url, self.RAX_GRPADM,
                                               self.GROUPS, group_id,
                                               self.USERS, user_id)
        server_response = self.delete(url,
                                      requestslib_kwargs=requestslib_kwargs)
        return server_response

    def get_users_for_group(self, group_id, marker=None, limit=None,
                            requestslib_kwargs=None):

        '''
        @summary: Get users for particular group
        @param group_id: The group Id
        @type group_id type: String
        @return: Users
        @rtype: Response Object entity users
        '''

        '''
            GET
            v2.0/RAX-GRPADM/groups/{group_id}/users
        '''
        params = {'limit': limit, 'marker': marker}
        url = '{0}/{1}/{2}/{3}/{4}'.format(self.base_url, self.RAX_GRPADM,
                                           self.GROUPS, group_id, self.USERS)
        server_response = self.get(url, params=params,
                                   response_entity_type=Users,
                                   requestslib_kwargs=requestslib_kwargs)
        return server_response

    def validate_token(self, token_id, belongs_to=None,
                       requestslib_kwargs=None):
        '''
        @summary: Check token information
        @param token_id: The token for check
        @type token_id type: String
        @return: Token info
        @rtype: Response Object entity token
        '''

        '''
            GET
            v2.0/tokens/{token_id}
        '''
        params = {'belongsTo': belongs_to}
        url = '{0}/{1}/{2}'.format(self.base_url, self.TOKENS, token_id)
        server_response = self.get(url, params=params,
                                   response_entity_type=Access,
                                   requestslib_kwargs=requestslib_kwargs)
        return server_response

    def check_token(self, token_id, belongs_to=None,
                    requestslib_kwargs=None):

        '''
        @summary: Check token information
        @param token_id: The token for check
        @type token_id type: String
        @return: Token info
        @rtype: Response Object entity token
        '''

        '''
            HEAD
            v2.0/tokens/{token_id}
        '''
        params = {'belongsTo': belongs_to}
        url = '{0}/{1}/{2}'.format(self.base_url, self.TOKENS, token_id)
        server_response = self.head(url, params=params,
                                    requestslib_kwargs=requestslib_kwargs)
        return server_response

    def revoke_token(self, token_id, requestslib_kwargs=None):
        '''
        @summary: Check token information
        @param token_id: The token for check
        @type token_id type: String
        @return: Token info
        @rtype: Response Object entity token
        '''

        '''
            DELETE
            v2.0/tokens/{token_id}
        '''
        url = '{0}/{1}/{2}'.format(self.base_url, self.TOKENS, token_id)
        server_response = self.delete(url,
                                      requestslib_kwargs=requestslib_kwargs)
        return server_response

    def list_endpoints_for_token(self, token_id, requestslib_kwargs=None):

        '''
        @summary: Get Endpoints
        @param token_id: The token for endpoints
        @type token_id type: String
        @return: Token info
        @rtype: Response Object entity token
        '''

        '''
            GET
            v2.0/tokens/{token_id}/endpoints
        '''
        url = '{0}/{1}/{2}/{3}'.format(self.base_url, self.TOKENS, token_id,
                                       self.ENDPOINTS)
        server_response = self.get(url,
                                   response_entity_type=Endpoints,
                                   requestslib_kwargs=requestslib_kwargs)
        return server_response

    def remove_end_points_for_tenant_id(self, tenant_id, end_point_id,
                                        requestslib_kwargs=None):
        '''
        DELETE
        v2.0/tenants/{tenant_id}/OS-KSCATALOG/endpoints/{endpointId}
        '''
        url = '{0}/{1}/{2}/OS-KSCATALOG/endpoints/{3}'.format(
                self.base_url,
                self.TENANTS,
                tenant_id,
                end_point_id)
        server_response = self.delete(url,
                                      response_entity_type=Endpoints,
                                      requestslib_kwargs=requestslib_kwargs)
        return server_response

    def add_end_point_for_tenant_id(self, tenant_id, requestslib_kwargs=None):
        '''
        POST
        v2.0/tenants/{tenant_id}/OS-KSCATALOG/endpoints/{endpointId}
        '''
        url = '{0}/{1}/{2}/OS-KSCATALOG/endpoints/{3}'.format(
                self.base_url,
                self.TENANTS,
                tenant_id,
                end_point_id)
        server_response = self.post(url,
                                    response_entity_type=Endpoints,
                                    requestslib_kwargs=requestslib_kwargs)
        return server_response

    def get_tenant_by_name(self, name, requestslib_kwargs=None):

        '''
        @summary: Get tenants by name
        @param name: tenant name
        @type name type: String
        @return: Tenants response object containing info for tenants
        @rtype: Response Object
        '''

        '''
            GET
            v2.0/tenants?name=string
        '''
        params = {'name': name}
        url = '{0}/{1}'.format(self.base_url, self.TENANTS)
        server_response = self.get(url, params=params,
                                   response_entity_type=ResponseTenant,
                                   requestslib_kwargs=requestslib_kwargs)
        return server_response

    def get_tenant_by_id(self, tenant_id, requestslib_kwargs=None):

        '''
        @summary: Get tenants by id
        @param name: tenant id
        @type name type: String
        @return: Tenants response object containing info for tenants
        @rtype: Response Object
        '''

        '''
            GET
            v2.0/tenants/{tenant_id}
        '''
        url = '{0}/{1}/{2}'.format(self.base_url, self.TENANTS, tenant_id)
        server_response = self.get(url,
                                    response_entity_type=ResponseTenant,
                                    requestslib_kwargs=requestslib_kwargs)
        return server_response

    def list_roles_for_user_on_tenant(self, tenant_id, user_id,
                                      requestslib_kwargs=None):

        '''
        @summary: List roles for user on tenant
        @param name: tenant id
        @type name type: String
        @return: Tenants response object containing info for tenants
        @rtype: Response Object
        '''

        '''
            GET
            v2.0/tenants/{tenant_id}/users/{user_id}/roles
        '''
        url = '{0}/{1}/{2}/{3}/{4}/{5}'.format(self.base_url, self.TENANTS,
                                               tenant_id, self.USERS, user_id,
                                               self.ROLES)
        server_response = self.get(url,
                                   response_entity_type=Roles,
                                   requestslib_kwargs=requestslib_kwargs)
        return server_response

    def list_users_for_tenant(self, tenant_id, limit=None, marker=None,
                              requestslib_kwargs=None):
        """
            GET
            v2.0/tenants/{tenant_id}/users?limit=string&marker=string
        """
        params = {'limit': limit, 'marker': marker}
        url = '{0}/{1}/{2}/{3}'.format(self.base_url, self.TENANTS, tenant_id,
                                       self.USERS)
        response = self.get(url, params=params, response_entity_type=Users,
                            requestslib_kwargs=requestslib_kwargs)
        return response

    def get_user_secret_qa(self, user_id, requestslib_kwargs=None):

        '''
        @summary: List secret qa
        @param user_id: user id
        @type user_id type: String
        @return: Secret Questions and Answers
        @rtype: Response Object
        '''

        '''
            GET
            v2.0/users/{user_id}/RAX-KSQA/secretqa
        '''
        url = '{0}/{1}/{2}/{3}/{4}'.format(self.base_url, self.USERS, user_id,
                                           self.RAX_KSQA, self.SECRETQA)
        server_response = self.get(url,
                                   response_entity_type=SecretQA,
                                   requestslib_kwargs=requestslib_kwargs)
        return server_response

    def get_user_secret_qa_list(self, user_id, requestslib_kwargs=None):

        '''
        @summary: List secret qa list
        @param user_id: user id
        @type user_id type: String
        @return: Secret Questions and Answers
        @rtype: Response Object
        '''

        '''
            GET
            v2.0/users/{user_id}/RAX-AUTH/secretqas
        '''
        url = '{0}/{1}/{2}/{3}/{4}'.format(self.base_url, self.USERS, user_id,
                                           self.RAX_AUTH, self.SECRETQAS)
        server_response = self.get(url,
                                   response_entity_type=SecretQAs,
                                   requestslib_kwargs=requestslib_kwargs)
        return server_response

    def create_question(self, question, requestslib_kwargs=None):

        '''
        @summary: Creates Question
        @param request body
        @param request body type - question
        @return: Secret Questions and Answers
        @rtype: Response Object
        '''

        '''
            POST
            v2.0/RAX-AUTH/secretqa/questions
        '''
        auth_request_entity = RequestQuestion(question=question)
        url = '{0}/{1}/{2}/{3}'.format(self.base_url, self.RAX_AUTH,
                                        self.SECRETQA, self.QUESTIONS)
        server_response = self.post(url,
                                    request_entity=auth_request_entity,
                                    requestslib_kwargs=requestslib_kwargs)
        return server_response

    def delete_question(self, question_id, requestslib_kwargs=None):

        '''
        @summary: Delete Question
        @param request body
        @param request body type - question
        @return: Secret Questions and Answers
        @rtype: Response Object
        '''

        '''
            DELETE
            v2.0/RAX-AUTH/secretqa/questions/{question_id}
        '''
        url = '{0}/{1}/{2}/{3}/{4}'.format(self.base_url, self.RAX_AUTH,
                                           self.SECRETQA, self.QUESTIONS,
                                           question_id)
        server_response = self.delete(url,
                                      requestslib_kwargs=requestslib_kwargs)
        return server_response

    def update_question(self, question_id, question, requestslib_kwargs=None):

        '''
        @summary: Update Question
        @param request body
        @param request body type - question
        @return: Secret Questions and Answers
        @rtype: Response Object
        '''

        '''
            PUT
            v2.0/RAX-AUTH/secretqa/questions/{question_id}
        '''
        auth_request_entity = RequestQuestion(question=question,
                                              questionId=question_id)
        url = '{0}/{1}/{2}/{3}/{4}'.format(self.base_url, self.RAX_AUTH,
                                           self.SECRETQA, self.QUESTIONS,
                                           question_id)
        server_response = self.put(url,
                                   response_entity_type=Question,
                                   request_entity=auth_request_entity,
                                   requestslib_kwargs=requestslib_kwargs)
        return server_response

    def get_question(self, question_id, requestslib_kwargs=None):

        '''
        @summary: Get Question
        @param question_id: question id
        @type question_id type: String
        @return: Secret Questions and Answers
        @rtype: Response Object
        '''

        '''
            GET
            v2.0/RAX-AUTH/secretqa/questions/{question_id}
        '''
        url = '{0}/{1}/{2}/{3}/{4}'.format(self.base_url, self.RAX_AUTH,
                                           self.SECRETQA, self.QUESTIONS,
                                           question_id)
        server_response = self.get(url,
                                   response_entity_type=Question,
                                   requestslib_kwargs=requestslib_kwargs)
        return server_response

    def get_questions(self, requestslib_kwargs=None):

        '''
        @summary: Get Questions
        @param questionId: question id
        @type questionId type: String
        @return: Secret Questions and Answers
        @rtype: Response Object
        '''

        '''
            GET
            v2.0/RAX-AUTH/secretqa/questions
        '''
        url = '{0}/{1}/{2}/{3}'.format(self.base_url, self.RAX_AUTH,
                                       self.SECRETQA, self.QUESTIONS)
        server_response = self.get(url,
                                   response_entity_type=Questions,
                                   requestslib_kwargs=requestslib_kwargs)
        return server_response

    def create_secret_qa(self, user_id, question_id, answer,
                         requestslib_kwargs=None):

        '''
        @summary: Creates answer to question
        @param request body
        @param request body type - question
        @return: Secret Questions and Answers
        @rtype: Response Object
        '''

        '''
            POST
            v2.0/users/{user_id}/RAX-AUTH/secretqas
        '''
        auth_request_entity = RequestSecretQA(id=question_id, answer=answer)
        url = '{0}/{1}/{2}/{3}/{4}'.format(self.base_url, self.USERS, user_id,
                                           self.RAX_AUTH, self.SECRETQAS)
        server_response = self.post(url,
                                    request_entity=auth_request_entity,
                                    requestslib_kwargs=requestslib_kwargs)
        return server_response

    def update_secret_qa(self, user_id, question, answer,
                         requestslib_kwargs=None):

        '''
        @summary: Updates answer to question
        @param request body
        @param request body type - question
        @return: Secret Questions and Answers
        @rtype: Response Object
        '''

        '''
            PUT
            v2.0/users/{user_id}/RAX-KSQA/secretqa
        '''
        auth_request_entity = UpdateSecretQA(question=question, answer=answer)
        url = '{0}/{1}/{2}/{3}/{4}'.format(self.base_url, self.USERS, user_id,
                                           self.RAX_KSQA, self.SECRETQA)
        server_response = self.put(url,
                                   response_entity_type=SecretQA,
                                   request_entity=auth_request_entity,
                                   requestslib_kwargs=requestslib_kwargs)
        return server_response

    def impersonate_user_expire_in(self,
                                   username,
                                   expire_in_seconds=None,
                                   requestslib_kwargs=None):

        '''
        @summary: Impersonate user
        @param username: the user to impersonate
        @type username: string
        @param expire_in_seconds: the seconds value to be expired
        @type expire_in_seconds type: long
        @return: Impersonation details
        @rtype: Response Object
        '''

        '''
            POST
            v2.0/RAX-AUTH/impersonation-tokens
        '''
        auth_request_entity = \
            RequestImpersonation(username=username,
                                 expire_in_seconds=expire_in_seconds)
        url = '{0}/{1}/{2}'.format(self.base_url, self.RAX_AUTH,
                                   self.IMPERSONATION_TOKENS)
        server_response = self.post(url,
                                    response_entity_type=Access,
                                    request_entity=auth_request_entity,
                                    requestslib_kwargs=requestslib_kwargs)
        return server_response

    def impersonate_user(self, username,
                         requestslib_kwargs=None):
        '''
        @summary: Impersonate user
        @param username: the user to impersonate
        @param username type: string
        @return: Impersonation details
        @rtype: Response Object
        '''

        '''
            POST
            v2.0/RAX-AUTH/impersonation-tokens
        '''
        auth_request_entity = \
            RequestImpersonation(username=username)
        url = '{0}/{1}/{2}'.format(self.base_url, self.RAX_AUTH,
                                   self.IMPERSONATION_TOKENS)
        server_response = self.post(url,
                                    response_entity_type=Access,
                                    request_entity=auth_request_entity,
                                    requestslib_kwargs=requestslib_kwargs)
        return server_response

    def get_user_rate_limit(self, requestslib_kwargs=None):

        '''
        @summary: Get User rate limit
        @param name: None
        @param type: None
        @return: Rate limits details
        @rtype: Response Object
        '''

        '''
            GET
            v2.0/rtadm
        '''
        url = '{0}/{1}'.format(self.base_url, self.RTADM)
        server_response = self.get(url,
                                   response_entity_type=RateLimit,
                                   requestslib_kwargs=requestslib_kwargs)
        return server_response

    def update_user_rate_limits(self, enabled=None, interval=None,
                                threshold=None, allow=None,
                                requestslib_kwargs=None):

        '''
        @summary: Add User rate limit
        @param name: None
        @param type: None
        @return: Rate limits details
        @rtype: Response Object
        '''

        '''
            POST
            v2.0/rtadm
        '''
        auth_request_entity = RequestRateLimit(enabled=enabled,
                                               interval=interval,
                                               threshold=threshold,
                                               allow=allow)
        url = '{0}/{1}'.format(self.base_url, self.RTADM)
        server_response = self.post(url,
                                    response_entity_type=RateLimit,
                                    request_entity=auth_request_entity,
                                    requestslib_kwargs=requestslib_kwargs)
        return server_response

    # TODO: WHITE LIST CRUD CALLS

    def get_domains(self, limit=None, marker=None, requestslib_kwargs=None):
        '''
        @summary: Get Domains
        @return: List of domains
        @rtype: Response Object
        '''

        '''
            GET
            v2.0/RAX-AUTH/domains
        '''
        url = '{0}/{1}/{2}'.format(self.base_url, self.RAX_AUTH, self.DOMAINS)
        params = {'limit': limit, 'marker': marker}
        response = self.get(url,
                            params=params,
                            response_entity_type=Domains,
                            requestslib_kwargs=requestslib_kwargs)
        return response

    def create_domain(self, id, name, description=None, enabled=None,
                      requestslib_kwargs=None):

        '''
        @summary: Add Domain
        @param name: Name of domain
        @param type: String
        @return: Domain details
        @rtype: Response Object
        '''

        '''
            POST
            v2.0/RAX-AUTH/domains
        '''
        auth_request_entity = RequestDomain(id=id, name=name, enabled=enabled,
                                            description=description)
        url = '{0}/{1}/{2}'.format(self.base_url, self.RAX_AUTH, self.DOMAINS)
        server_response = self.post(url,
                                    response_entity_type=Domain,
                                    request_entity=auth_request_entity,
                                    requestslib_kwargs=requestslib_kwargs)
        return server_response

    def delete_domain(self, domain_id, requestslib_kwargs=None):

        '''
        @summary: Delete Domain
        @param domain_id: id of domain
        @param type: String
        @return: Domain details
        @rtype: Response Object
        '''

        '''
            DELETE
            v2.0/RAX-AUTH/domains/{domain_id}
        '''
        url = '{0}/{1}/{2}/{3}'.format(self.base_url, self.RAX_AUTH,
                                       self.DOMAINS, domain_id)
        server_response = self.delete(url,
                                      requestslib_kwargs=requestslib_kwargs)
        return server_response

    def update_domain(self, domain_id, enabled=None, id=None, name=None,
                      description=None, requestslib_kwargs=None):

        '''
        @summary: Update Domain
        @param name: Name of domain
        @param type: String
        @return: Domain details
        @rtype: Response Object
        '''

        '''
            PUT
            v2.0/RAX-AUTH/domains
        '''
        auth_request_entity = RequestDomain(enabled=enabled,
                                            description=description,
                                            id=id,
                                            name=name)
        url = '{0}/{1}/{2}/{3}'.format(self.base_url, self.RAX_AUTH,
                                       self.DOMAINS, domain_id)
        server_response = self.put(url,
                                   response_entity_type=Domain,
                                   request_entity=auth_request_entity,
                                   requestslib_kwargs=requestslib_kwargs)
        return server_response

    def get_domain(self, domain_id, requestslib_kwargs=None):

        '''
        @summary: Get Domain
        @param domain_id: id of domain
        @param type: String
        @return: Domain details
        @rtype: Response Object
        '''

        '''
            GET
            v2.0/RAX-AUTH/domains/{domain_id}
        '''
        url = '{0}/{1}/{2}/{3}'.format(self.base_url, self.RAX_AUTH,
                                       self.DOMAINS, domain_id)
        server_response = self.get(url,
                                   response_entity_type=Domain,
                                   requestslib_kwargs=requestslib_kwargs)
        return server_response

    def get_endpoints_for_domain(self, domain_id, requestslib_kwargs=None):

        '''
        @summary: Get Endpoints for Domain
        @param domain_id: id of domain
        @param type: String
        @return: Domain Endpoints details
        @rtype: Response Object
        '''

        '''
            GET
            v2.0/RAX-AUTH/domains/{domain_id}/endpoints
        '''
        url = '{0}/{1}/{2}/{3}/{4}'.format(self.base_url, self.RAX_AUTH,
                                           self.DOMAINS, domain_id,
                                           self.ENDPOINTS)
        server_response = self.get(url,
                                   response_entity_type=Endpoints,
                                   requestslib_kwargs=requestslib_kwargs)
        return server_response

    def get_users_in_domain(self, domain_id, enabled=None,
                            requestslib_kwargs=None):

        '''
        @summary: Get Users in Domain
        @param domain_id: id of domain
        @param type: String
        @return: Domain details
        @rtype: Response Object
        '''

        '''
            GET
            v2.0/RAX-AUTH/domains/{domain_id}/users?enabled=string
        '''
        params = {'enabled': enabled}
        url = '{0}/{1}/{2}/{3}/{4}'.format(self.base_url, self.RAX_AUTH,
                                           self.DOMAINS, domain_id,
                                           self.USERS)
        server_response = self.get(url, params=params,
                                   response_entity_type=Users,
                                   requestslib_kwargs=requestslib_kwargs)
        return server_response

    def get_tenants_in_domain(self, domain_id, enabled=None,
                              requestslib_kwargs=None):

        '''
        @summary: Get Tenants in Domain
        @param domain_id: id of domain
        @param type: String
        @return: Domain details
        @rtype: Response Object
        '''

        '''
            GET
            v2.0/RAX-AUTH/domains/{domain_id}/tenants?enabled=string
        '''
        params = {'enabled': enabled}
        url = '{0}/{1}/{2}/{3}/{4}'.format(self.base_url, self.RAX_AUTH,
                                           self.DOMAINS, domain_id,
                                           self.TENANTS)
        server_response = self.get(url, params=params,
                                   response_entity_type=Tenants,
                                   requestslib_kwargs=requestslib_kwargs)
        return server_response

    def add_tenant_to_domain(self, domain_id, tenant_id,
                             requestslib_kwargs=None):

        '''
        @summary: Add Tenants in Domain
        @param domain_id: id of domain
        @param type: String
        @param tenant_id: id of tenant
        @param type: String
        @return: Domain details
        @rtype: Response Object
        '''

        '''
            PUT
            v2.0/RAX-AUTH/domains/{domain_id}/tenants/{tenant_id}
        '''
        url = '{0}/{1}/{2}/{3}/{4}/{5}'.format(self.base_url, self.RAX_AUTH,
                                               self.DOMAINS, domain_id,
                                               self.TENANTS, tenant_id)
        server_response = self.put(url, requestslib_kwargs=requestslib_kwargs)
        return server_response

    def add_user_to_domain(self, domain_id, user_id, requestslib_kwargs=None):

        '''
        @summary: Add User in Domain
        @param domain_id: id of domain
        @param type: String
        @param user_id: id of user
        @param type: String
        @return: Domain details
        @rtype: Response Object
        '''

        '''
            PUT
            v2.0/RAX-AUTH/domains/{domain_id}/users/{user_id}
        '''
        url = '{0}/{1}/{2}/{3}/{4}/{5}'.format(self.base_url, self.RAX_AUTH,
                                               self.DOMAINS, domain_id,
                                               self.USERS, user_id)
        server_response = self.put(url, requestslib_kwargs=requestslib_kwargs)
        return server_response

    def get_default_region_services(self, requestslib_kwargs=None):

        '''
        @summary: Get Default Region Services
        @return: Default Region Services details
        @rtype: Response Object
        '''

        '''
            GET
            v2.0/RAX-AUTH/default-region/services
        '''
        url = '{0}/{1}/{2}/{3}'.format(self.base_url, self.RAX_AUTH,
                                       self.DEFAULT_REGION, self.SERVICES)
        server_response = self.get(url,
                                   response_entity_type=DefaultRegionServices,
                                   requestslib_kwargs=requestslib_kwargs)
        return server_response

    def set_default_region_services(self, default_region_services=None,
                                    requestslib_kwargs=None):

        '''
        @summary: Set Default Region Services
        @param default_region_services: list of services
        @param type: List of strings
        @return: Default Region Services details
        @rtype: Response Object
        '''

        '''
            PUT
            v2.0/RAX-AUTH/default-region/services
        '''
        auth_request_entity = RequestDefaultRegionServices(
                defaultRegionServices=default_region_services)
        url = '{0}/{1}/{2}/{3}'.format(self.base_url, self.RAX_AUTH,
                                       self.DEFAULT_REGION, self.SERVICES)
        server_response = self.put(url,
                                   response_entity_type=DefaultRegionServices,
                                   request_entity=auth_request_entity,
                                   requestslib_kwargs=requestslib_kwargs)
        return server_response

    def get_policies(self, requestslib_kwargs=None):

        '''
        @summary: Get Policies
        @return: Policies
        @rtype: Response Object
        '''

        '''
            GET
            v2.0/RAX-AUTH/policies
        '''
        url = '{0}/{1}/{2}'.format(self.base_url, self.RAX_AUTH, self.POLICIES)
        server_response = self.get(url,
                                   response_entity_type=Policies,
                                   requestslib_kwargs=requestslib_kwargs)
        return server_response

    def get_policy(self, policy_id, requestslib_kwargs=None):

        '''
        @summary: Get Policy
        @return: Policy
        @rtype: Response Object
        '''

        '''
            GET
            v2.0/RAX-AUTH/policies/{policy_id}
        '''
        url = '{0}/{1}/{2}/{3}'.format(self.base_url, self.RAX_AUTH,
                                       self.POLICIES, policy_id)
        server_response = self.get(url,
                                   response_entity_type=Policy,
                                   requestslib_kwargs=requestslib_kwargs)
        return server_response

    def create_policy(self, name, blob, type, global_=None, enabled=None,
                      description=None, requestslib_kwargs=None):

        '''
        @summary: Create Policy
        @param name: Name of policy
        @param type: String
        @return: Policy details
        @rtype: Response Object
        '''

        '''
            POST
            v2.0/RAX-AUTH/policies
        '''
        auth_request_entity = RequestPolicy(enabled=enabled,
                                            description=description,
                                            blob=blob,
                                            global_=global_,
                                            type=type,
                                            name=name)
        url = '{0}/{1}/{2}'.format(self.base_url, self.RAX_AUTH, self.POLICIES)
        server_response = self.post(url,
                                    response_entity_type=Policies,
                                    request_entity=auth_request_entity,
                                    requestslib_kwargs=requestslib_kwargs)
        return server_response

    def delete_policy(self, policy_id, requestslib_kwargs=None):

        '''
        @summary: Delete Policy
        @return: Deleted Policy
        @rtype: Response Object
        '''

        '''
            DELETE
            v2.0/RAX-AUTH/policies/{policy_id}
        '''
        url = '{0}/{1}/{2}/{3}'.format(self.base_url, self.RAX_AUTH,
                                       self.POLICIES, policy_id)
        server_response = self.delete(url,
                                      requestslib_kwargs=requestslib_kwargs)
        return server_response

    def update_policy(self, policy_id, name, global_=None, type=None,
                      enabled=None, blob=None, description=None,
                      requestslib_kwargs=None):

        '''
        @summary: Update Policy
        @param name: Name of policy
        @param type: String
        @return: Policy details
        @rtype: Response Object
        '''

        '''
            PUT
            v2.0/RAX-AUTH/policies/{policy_id}
        '''
        auth_request_entity = RequestPolicy(enabled=enabled,
                                            description=description,
                                            blob=blob,
                                            global_=global_,
                                            type=type,
                                            name=name)
        url = '{0}/{1}/{2}/{3}'.format(self.base_url, self.RAX_AUTH,
                                       self.POLICIES, policy_id)
        server_response = self.put(url,
                                   response_entity_type=Policies,
                                   request_entity=auth_request_entity,
                                   requestslib_kwargs=requestslib_kwargs)
        return server_response

    def get_detailed_policy_content(self, policy_id, requestslib_kwargs=None):

        '''
        @summary: Get Detailed Policy Content
        @return: Policy
        @rtype: Response Object
        '''

        '''
            GET
            v2.0/RAX-AUTH/policies/{policy_id}/blob_detail
        '''
        url = '{0}/{1}/{2}/{3}/{4}'.format(self.base_url, self.RAX_AUTH,
                                           self.POLICIES, policy_id, self.BLOB)
        server_response = self.get(url,
                                   response_entity_type=Policy,
                                   requestslib_kwargs=requestslib_kwargs)
        return server_response

    def get_service_apis(self, requestslib_kwargs=None):

        '''
        @summary: Get Service APIs
        @param name: Only X-Auth token
        @param type: String
        @return: Service APIs
        @rtype: Response Object
        '''

        '''
            GET
            v2.0/RAX-AUTH/service-apis
        '''
        url = '{0}/{1}/{2}'.format(self.base_url, self.RAX_AUTH,
                                   self.SERVICE_APIS)
        server_response = self.get(url,
                                   response_entity_type=ServiceAPIs,
                                   requestslib_kwargs=requestslib_kwargs)
        return server_response

    def get_capabilities(self, type, version, requestslib_kwargs=None):

        '''
        @summary: Get Capabilities
        @param typE: Service type
        @param type: String
        @param version: Service version
        @param type: String
        @return: Service APIs Capability
        @rtype: Response Object
        '''

        '''
            GET
            v2.0/RAX-AUTH/service-apis/{type}/{version}/capabilities
        '''
        url = '{0}/{1}/{2}/{3}/{4}/{5}'.format(self.base_url, self.RAX_AUTH,
                                               self.SERVICE_APIS, type,
                                               version, self.CAPABILITIES)
        server_response = self.get(url,
                                   response_entity_type=Capabilities,
                                   requestslib_kwargs=requestslib_kwargs)
        return server_response

    def update_capabilities(self, type, version, capabilities,
                            requestslib_kwargs=None):

        '''
        @summary: Update Capabilities
        @param typE: Service type
        @param type: String
        @param version: Service version
        @param type: String
        @return: Service APIs Updated Capability
        @rtype: Response Object
        '''

        '''
            PUT
            v2.0/RAX-AUTH/service-apis/{type}/{version}/capabilities
        '''
        # TODO: Docs say body not required, is this true?
        capabilities = [RequestCapability(**cap) for cap in capabilities]
        auth_request_entity = RequestCapabilities(capabilities=capabilities)
        url = '{0}/{1}/{2}/{3}/{4}/{5}'.format(self.base_url, self.RAX_AUTH,
                                               self.SERVICE_APIS, type,
                                               version, self.CAPABILITIES)
        server_response = self.put(url,
                                   response_entity_type=Capabilities,
                                   request_entity=auth_request_entity,
                                   requestslib_kwargs=requestslib_kwargs)
        return server_response

    def remove_capabilities(self, type=None, version=None,
                            requestslib_kwargs=None):

        '''
        @summary: Remove Capabilities
        @param typE: Service type
        @param type: String
        @param version: Service version
        @param type: String
        @return: Service APIs Capability Removed from system
        @rtype: Response Object
        '''

        '''
            DELETE
            v2.0/RAX-AUTH/service-apis/{type}/{version}/capabilities
        '''
        url = '{0}/{1}/{2}/{3}/{4}/{5}'.format(self.base_url, self.RAX_AUTH,
                                               self.SERVICE_APIS, type,
                                               version, self.CAPABILITIES)
        server_response = self.delete(url,
                                      requestslib_kwargs=requestslib_kwargs)
        return server_response

    def list_extensions(self, requestslib_kwargs=None):

        '''
        @summary: List extensions
        @params: None
        @params type: None
        @return: List extensions
        @rtype: Response Object
        '''

        '''
            GET
            v2.0/extensions
        '''
        url = '{0}/{1}'.format(self.base_url,
                               self.EXTENSIONS)
        server_response = self.get(url,
                                   response_entity_type=Extensions,
                                   requestslib_kwargs=requestslib_kwargs)
        return server_response

    def get_extension_by_alias(self, alias, requestslib_kwargs=None):

        '''
        @summary: List Extensions
        @param alias: Extension alias
        @param type: String
        @return: Extension
        @rtype: Response Object
        '''

        '''
            GET
            v2.0/extensions/alias
        '''
        url = '{0}/{1}/{2}'.format(self.base_url,
                                   self.EXTENSIONS,
                                   alias)
        server_response = self.get(url,
                                   response_entity_type=Extension,
                                   requestslib_kwargs=requestslib_kwargs)
        return server_response

    def add_tenant(self, name, description=None, enabled=None,
                   requestslib_kwargs=None):
        """
        @summary: Add tenant
        @param name: Name of the tenant
        @type name: String
        @param description: Description of the tenant
        @type description: String
        @param enabled: Specifies if the tenant is enabled or not
        @type enabled: Boolean
        @return: Tenant details
        @rtype: Response Object
        """

        """
            POST
            v2.0/tenants
        """
        tenant_request_entity = RequestTenant(name=name,
                                              description=description,
                                              enabled=enabled)
        url = '{0}/{1}'.format(self.base_url, self.TENANTS)
        response = self.post(
            url,
            response_entity_type=ResponseTenant,
            request_entity=tenant_request_entity,
            requestslib_kwargs=requestslib_kwargs)
        return response

    def delete_tenant(self, tenant_id, requestslib_kwargs=None):

        """
        @summary: Delete tenant
        @param tenant_id: The tenant id
        @type tenant_id: String
        @return: Tenant Removed from system
        @rtype: Response Object
        """

        """
            DELETE
            v2.0/tenants/{tenantId}
        """
        url = '{0}/{1}/{2}'.format(self.base_url, self.TENANTS, tenant_id)
        response = self.delete(
            url,
            response_entity_type=None,
            requestslib_kwargs=requestslib_kwargs)
        return response

    def add_role_to_user_on_tenant(self, tenant_id, user_id, role_id,
                                   requestslib_kwargs=None):
        """
        @summary: Add a specific global role to a user.
        @param tenant_id: The tenant id
        @type tenant_id: String
        @param user_id: The user id
        @type user_id: String
        @param role_id: The role id
        @type role_id: String
        @return: User info with new Global Role
        @rtype: Response Object
        """

        """
            PUT
            v2.0/tenants/{tenant_id}/users/{user_id}/roles/OS-KSADM/{role_id}
        """
        url = '{0}/{1}/{2}/{3}/{4}/{5}/{6}/{7}'.format(
            self.base_url, self.TENANTS, tenant_id, self.USERS, user_id,
            self.ROLES, self.OS_KSADM, role_id)
        response = self.put(
            url,
            response_entity_type=None,
            requestslib_kwargs=requestslib_kwargs)
        return response

    def delete_role_to_user_on_tenant(self, tenant_id, user_id, role_id,
                                      requestslib_kwargs=None):
        """
        @summary: Delete a specific global role to a user.
        @param tenant_id: The tenant id
        @type tenant_id: String
        @param user_id: The user id
        @type user_id: String
        @param role_id: The role id
        @type role_id: String
        @return: User info with new Global Role
        @rtype: Response Object
        """
        """
            DELETE
            v2.0/tenants/{tenant_id}/users/{user_id}/roles/OS-KSADM/{role_id}
        """
        url = ('{base_url}/{tenants}/{tenant_id}/{users}/{user_id}'
               '/{roles}/{os_ksadm}/{role_id}'
               .format(base_url=self.base_url, tenants=self.TENANTS,
                       tenant_id=tenant_id, users=self.USERS, user_id=user_id,
                       roles=self.ROLES, os_ksadm=self.OS_KSADM,
                       role_id=role_id))

        response = self.delete(
            url,
            response_entity_type=None,
            requestslib_kwargs=requestslib_kwargs)
        return response

    def add_endpoint_template(self, id, name, type, region, enabled,
                              public_url=None, internal_url=None,
                              admin_url=None, requestslib_kwargs=None):

        """
        @summary: Add endpoint template
        @param id: The id
        @type id: String
        @param name: Name of the endpoint
        @type name: String
        @param type: Type of the endpoint
        @type type: String
        @param region: Region of the endpoint
        @type region: String
        @param enabled: Specifies if the endpoint is enabled or not
        @type enabled: Boolean
        @param public_url: Public url of the endpoint
        @type public_url: String
        @param internal_url: Internal url of the endpoint
        @type internal_url: String
        @param admin_url: Admin url of the endpoint
        @type admin_url: String
        @return: Endpoint information
        @rtype: Response Object
        """

        """
            POST
            v2.0/OS-KSCATALOG/endpointTemplates
        """
        endpoint_template_request_entity = RequestEndpointTemplate(
            id, name, type, region, public_url, internal_url, admin_url,
            enabled)
        url = '{0}/{1}/{2}'.format(
            self.base_url,
            self.OS_KSCATALOG,
            self.ENDPOINT_TEMPLATES)
        response = self.post(
            url,
            response_entity_type=ResponseEndpointTemplate,
            request_entity=endpoint_template_request_entity,
            requestslib_kwargs=requestslib_kwargs)
        return response

    def get_endpoint_template(self, endpoint_template_id,
                              requestslib_kwargs=None):

        """
        @summary: Get endpoint template
        @param endpoint_template_id: The endpoint template id
        @type endpoint_template_id: String
        @return: Endpoint template
        @rtype: Response Object
        """

        '''
            GET v2.0/OS-KSCATALOG/endpointTemplates/{endpoint_template_id}
        '''
        url = '{0}/{1}/{2}/{3}'.format(
            self.base_url, self.OS_KSCATALOG, self.ENDPOINT_TEMPLATES,
            endpoint_template_id)
        response = self.get(url,
                            response_entity_type=ResponseEndpointTemplate,
                            requestslib_kwargs=requestslib_kwargs)
        return response

    def delete_endpoint_template(self, endpoint_template_id,
                                 requestslib_kwargs=None):

        """
        @summary: Delete endpoint template
        @param endpoint_template_id: The endpoint template id
        @type endpoint_template_id: String
        @return: Delete endpoint template id from the system
        @rtype: Response Object
        """

        """
            DELETE
            v2.0/OS-KSCATALOG/endpointTemplates/{endpoint_template_id}
        """
        url = '{0}/{1}/{2}/{3}'.format(
            self.base_url,
            self.OS_KSCATALOG,
            self.ENDPOINT_TEMPLATES,
            endpoint_template_id)
        response = self.delete(
            url,
            response_entity_type=None,
            requestslib_kwargs=requestslib_kwargs)
        return response

    def add_endpoint_to_tenant(self, id, tenant_id, name=None, type=None,
                               region=None, public_url=None, internal_url=None,
                               admin_url=None, enabled=None,
                               requestslib_kwargs=None):

        """
        @summary: Add endpoint to tenant
        @param id: The endpoint id
        @type id: String
        @param tenant_id: The tenant id
        @type tenant_id: String
        @param name: The name of the endpoint
        @type name: String
        @param type: The type of the endpoint
        @type type: String
        @param region: The region of the endpoint
        @type region: String
        @param public_url: The public url of the endpoint
        @type public_url: String
        @param internal_url: The internal url of the endpoint
        @type internal_url: String
        @param admin_url: The admin url of the endpoint
        @type admin_url: String
        @param enabled: Specifies if the endpoint on the tenant is enabled
        @type enabled: Boolean
        @return: Endpoint added to tenant
        @rtype: Response Object
        """

        """
            POST
            v2.0/tenants/{tenant_id}/OS-KSCATALOG/endpoints
        """
        endpoint_template_request_entity = RequestEndpointTemplate(id)
        url = '{0}/{1}/{2}/{3}/{4}'.format(
            self.base_url,
            self.TENANTS,
            tenant_id,
            self.OS_KSCATALOG,
            self.ENDPOINTS)
        response = self.post(
            url,
            response_entity_type=ResponseEndpointTemplate,
            request_entity=endpoint_template_request_entity,
            requestslib_kwargs=requestslib_kwargs)
        return response

    def delete_endpoint_to_tenant(self, tenant_id, endpoint_id,
                                  requestslib_kwargs=None):

        """
        @summary: Delete endpoint to tenant
        @param id: The endpoint id
        @type id: String
        @param tenant_id: The tenant id
        @type tenant_id: String
        @return: The endpoint on the tenant is deleted
        @rtype: Response Object
        """

        """
            POST
            v2.0/tenants/{tenant_id}/OS-KSCATALOG/endpoints/{endpoint_id}
        """
        url = ('{base_url}/{tenants}/{tenant_id}/{os_kscatalog}/'
               '{endpoints}/{endpoint_id}'
               .format(base_url=self.base_url, tenants=self.TENANTS,
                       tenant_id=tenant_id, os_kscatalog=self.OS_KSCATALOG,
                       endpoints=self.ENDPOINTS, endpoint_id=endpoint_id))
        response = self.delete(
            url,
            request_entity=None,
            requestslib_kwargs=requestslib_kwargs)
        return response
