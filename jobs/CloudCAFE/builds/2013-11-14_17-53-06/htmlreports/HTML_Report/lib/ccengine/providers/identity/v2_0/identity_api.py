'''
@summary: Provider Module for the AUTH API
@note: Should be the primary interface to a test case or external tool.
@copyright: Copyright (c) 2012 Rackspace US, Inc.
'''
from ccengine.providers.base_provider import BaseProvider, ProviderActionResult
from ccengine.clients.identity.v2_0.rax_auth_service_api \
    import IdentityServiceClient
from ccengine.clients.identity.v2_0.rax_auth_admin_api \
    import IdentityAdminClient
from ccengine.clients.identity.v2_0.rax_auth_admin_api \
    import IdentityClient
from ccengine.clients.identity.v2_0.rax_auth_racker_api \
    import RackerClient


class IdentityClientTypes(object):
    DEFAULT, ADMIN, SERVICE, RACKER = range(4)


class IdentityAPIProvider(BaseProvider):
    '''
    @summary: Provides an interface to Auth providers
    '''

    def __init__(self, config):
        super(IdentityAPIProvider, self).__init__()
        self.config = config
        endpoint = self.config.identity_api.authentication_endpoint
        serializer = self.config.misc.serializer
        deserializer = self.config.misc.deserializer
        self.client = IdentityClient(url=endpoint, serialize_format=serializer,
                                     deserialize_format=deserializer)
        self.racker_client = RackerClient(url=endpoint,
            serialize_format=serializer,
            deserialize_format=deserializer)

    def get_client(self, token=None, username=None, api_key=None,
                   password=None, client_type=IdentityClientTypes.ADMIN):
        '''
        @summary: Creates a client based on credentials passed in. token
        overrides any username/password/api_key combination.  api_key
        overrides any password.  If password, api_key, and token are not
        supplied, a client without any credentials is returned.
        @param token: A token to be used for any calls used with returned
        client
        @type token: String
        @param username: The username of the customer.
        @type name: String
        @param api_key: An API key.
        @type api_key: String
        @param password: A password.
        @type password: String
        @param client_type: Type of client to return. Enumerated options are
        in IdentityClientTypes class
        @type client_type: String
        @return: A client object with identity api methods.
        @rtype: IdentityClient, IdentityAdminClient, or ServiceAdminClient
        '''
        endpoint = self.config.identity_api.authentication_endpoint
        serializer = self.config.misc.serializer
        deserializer = self.config.misc.deserializer
        if client_type == IdentityClientTypes.RACKER:
            auth_token = token or self.racker_token(username, password)
        else:
            auth_token = token or self.get_token(username, api_key, password)
        if client_type == IdentityClientTypes.DEFAULT:
            client = IdentityClient(url=endpoint,
                                    serialize_format=serializer,
                                    deserialize_format=deserializer,
                                    auth_token=auth_token)
        if client_type == IdentityClientTypes.ADMIN:
            client = IdentityAdminClient(url=endpoint,
                                         serialize_format=serializer,
                                         deserialize_format=deserializer,
                                         auth_token=auth_token)
        if client_type == IdentityClientTypes.SERVICE:
            client = IdentityServiceClient(url=endpoint,
                                           serialize_format=serializer,
                                           deserialize_format=deserializer,
                                           auth_token=auth_token)
        if client_type == IdentityClientTypes.RACKER:
            client = RackerClient(url=endpoint,
                                  serialize_format=serializer,
                                  deserialize_format=deserializer,
                                  auth_token=auth_token)
        return client

    def get_token(self, username, api_key=None, password=None):
        '''
        @summary: Attempts to auth with the username and api_key or password
        supplied.  If auth fails, returns None
        @param username: The username of the customer.
        @type name: String
        @param api_key: An API key.
        @type api_key: String
        @param password: A password.
        @type password: String
        @return: A token.
        @rtype: String
        '''
        auth_token = None
        if username is not None:
            if password is not None:
                auth_data = self.client.authenticate_user_password(
                    username=username,
                    password=password)
                if auth_data.entity is not None and \
                        auth_data.entity.token is not None:
                    auth_token = auth_data.entity.token.id
            if api_key is not None:
                auth_data = self.client.authenticate_user_apikey(
                    username=username,
                    api_key=api_key)
                if auth_data.entity is not None and \
                        auth_data.entity.token is not None:
                    auth_token = auth_data.entity.token.id
        return auth_token

    def racker_token(self, username, password):
        '''
            @summary: Attempts to auth with the sso username and sso password
            supplied.  If auth fails, returns None
            @param username: The username of a Racker.
            @type name: String
            @param password: SSO password.
            @type password: String
            @return: A token.
            @rtype: String
        '''
        auth_token = None
        if username is not None:
            if password is not None:
                auth_data = self.racker_client.authenticate_racker(
                    username=username,
                    password=password)
                if auth_data.entity is not None and \
                        auth_data.entity.token is not None:
                    auth_token = auth_data.entity.token.id

        return auth_token

    def authenticate(self):
        '''
            Automatically authenticates given the information in the config
            identity section.
            If both api key and password are present, prefers password.
        '''
        provider_response = ProviderActionResult()
        username = self.config.identity_api.username
        api_key = self.config.identity_api.api_key
        password = self.config.identity_api.password

        if username is None:
            msg1 = 'Username not found in the identity'
            msg2 = 'section of the config object'
            msg = ' '.join([msg1, msg2])
            self.provider_log.critical(msg)
            return None

        if password is None and api_key is None:
            msg1 = 'Neither an api_key nor a password where found in the'
            msg2 = 'identity section of the config object'
            msg = ' '.join([msg1, msg2])
            self.provider_log.critical(msg)
            return None

        if password is not None:
            resp = self.client.authenticate_user_password(username, password)
            provider_response.response = resp
            if resp.ok and (resp.entity is not None):
                provider_response.entity = resp.entity
                return provider_response

        elif api_key is not None:
            resp = self.client.authenticate_user_apikey(username, api_key)
            provider_response.response = resp
            if resp.ok and (resp.entity is not None):
                provider_response.entity = resp.entity
                return provider_response

    def delete_user_permanently(self, user_id, client, service_client):
        """
        Function to delete user permanently from directory using delete_user
        and delete_user_hard functions
        @param user_id: Id of the user
        @param client: Client to make delete_user call
        @param service_client: service client to make delete_user_hard call
        @return: status code
        """
        delete_user = client.delete_user(user_id=user_id)
        if delete_user.status_code == 204:
            delete_user = service_client.delete_user_hard(user_id=user_id)
        return delete_user.status_code
