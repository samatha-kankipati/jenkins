'''
@summary: Base Classes for Test Suites (Collections of Test Cases)
@note: Correspondes DIRECTLY TO A unittest.TestCase
@see: http://docs.python.org/library/unittest.html#unittest.TestCase
@copyright: Copyright (c) 2012 Rackspace US, Inc.
'''
from ccengine.clients.identity.v1_1.rax_auth_admin_api \
    import IdentityAdminClient
from ccengine.common.connectors.rest import RestConnector
from ccengine.common.exception_handler.exception_handler \
    import ExceptionHandler
from ccengine.common.resource_manager.resource_pool import ResourcePool
from ccengine.common.tools.datagen import random_int, rand_name
from ccengine.domain.configuration import AuthConfig, IdentityAPIConfig
from ccengine.providers.compute.compute_api import ComputeAPIProvider \
    as _ComputeAPIProvider
from ccengine.providers.identity.v2_0.identity_api \
    import IdentityAPIProvider, IdentityClientTypes
from ccengine.providers.lbaas.load_balancer_api import LoadBalancersProvider
from testrepo.common.testfixtures.fixtures import BaseTestFixture
from testrepo.common.testfixtures.rax_signup import \
    RaxSignupAPI_CloudSignupFixture


class BaseIdentityFixture(BaseTestFixture):
    '''
    Sets up public client and admin clients without tokens.
    '''

    @classmethod
    def setUpClass(cls):
        super(BaseIdentityFixture, cls).setUpClass()

        # Init provider
        cls.provider = IdentityAPIProvider(cls.config)

        # Set up public client without token
        cls.public_client = cls.provider.get_client(
            client_type=IdentityClientTypes.DEFAULT)

        # Set up admin client without token
        cls.admin_client = cls.provider.get_client()

        # Set up racker client without token
        cls.racker_client = cls.provider.get_client(
            client_type=IdentityClientTypes.RACKER)

        # Set up service client to use Identity Service credentials
        service_username = cls.config.identity_api.service_username
        service_password = cls.config.identity_api.service_password
        cls.service_client = cls.provider.get_client(
            username=service_username,
            password=service_password,
            client_type=IdentityClientTypes.SERVICE)

        # Set up admin client for version 1.1
        endpoint = cls.config.identity_api.authentication_endpoint
        serializer = cls.config.misc.serializer
        cls.admin_user = cls.config.identity_api.admin_username
        cls.admin_password = cls.config.identity_api.admin_password
        cls.admin_client_v11 = IdentityAdminClient(
            url=endpoint,
            user=cls.admin_user,
            password=cls.admin_password,
            serialize_format=serializer)

        # Set default status error message
        cls.err_msg = 'Response received: {0}; Response expected: {1}'

    def _follow_link(self, link, links, method, method_args=None):
        kwargs = {'url': links[link]['url']}
        return method(method_args, requestslib_kwargs=kwargs)

    def _status_assertion(self, received, expected):
        self.assertEqual(received,
                         expected,
                         msg=self.err_msg.format(received, expected))

    @classmethod
    def delete_user_permanently(cls, user_id, client):
        """
        Function to delete user permanently from LDAP using delete_user and
        delete_user_hard functions4
        @param user_id: user ID
        @param client: client to delete user
        @return: response for delete user
        """
        delete_user = client.delete_user(user_id=user_id)
        if delete_user.status_code == 204:
            delete_user = cls.service_client.delete_user_hard(user_id=user_id)
        return delete_user

    @classmethod
    def delete_tenant(cls, tenant_id, client):
        """
        Function to delete tenant from LDAP
        @param domain: domain ID
        @param client: client to delete tenant
        @return: response for delete domain
        """
        delete_tenant = client.delete_tenant(tenant_id=tenant_id)
        return delete_tenant

    @classmethod
    def delete_domain(cls, domain_id, client):
        """
        Function to delete domain permanently from LDAP
        @param domain_id: domain ID
        @param client: client to delete domain
        @return: response for delete domain
        """
        delete_domain = client.delete_domain(domain_id=domain_id)
        return delete_domain

    @classmethod
    def set_client(cls, username, user_type=None, password=None):
        """
        Sets the client with the appropriate token
        """
        # creating a admin client, but token set could be either user admin
        # or a identity user, based on the arguments.  Admin client is created
        # so that it has access to all the api calls
        client = cls.provider.get_client()
        if user_type == IdentityClientTypes.DEFAULT:
            auth_user_adm_resp = cls.public_client.authenticate_user_password(
                username,
                password)
            client.token = auth_user_adm_resp.entity.token.id
        elif user_type == IdentityClientTypes.SERVICE:
            client = cls.service_client
        elif user_type == IdentityClientTypes.ADMIN:
            auth_iden_adm_resp = cls.service_client.authenticate_user_password(
                username,
                password)
            client.token = auth_iden_adm_resp.entity.token.id
        return client

    @classmethod
    def get_test_user_v2_0(cls, client, username, password, default_region=None,
                      domain_id=None, email=None, enabled=True):
        """
        Creates a new user
        """
        email = email or cls.config.identity_api.default_email
        default_region = default_region or (cls.config.identity_api
                                            .default_region)
        created_user_v2_0 = client.add_user(
            default_region=default_region,
            username=username,
            domain_id=domain_id,
            password=password,
            email=email,
            enabled=enabled)
        return created_user_v2_0

    @classmethod
    def get_test_user_v1_1(cls, client, user_id, nast_id=None, api_key=None,
                         mosso_id=None, enabled=True):
        """
        Creates a new user admin in verion 1.1
        """
        created_user_v1_1 = cls.admin_client_v11.create_user(
            id=user_id,
            nast_id=nast_id,
            key=api_key,
            mosso_id=mosso_id,
            enabled=enabled)
        return created_user_v1_1

    @classmethod
    def get_test_tenant(cls, client, name=None, description=None,
                        enabled=True):
        """
        Creates a new tenant
        """
        name = name or ((-1) * random_int(10000, 1000000000))
        description = description or "Test tenant description"
        create_tenant = client.add_tenant(
            name=name,
            description=description,
            enabled=enabled)
        return create_tenant

    @classmethod
    def get_test_role(cls, client, name=None, description=None, weight=None,
                      propagate=True):
        """
        Creates a new role
        """
        role_name = name or rand_name("ccRole")
        description = description or "Test role description"
        create_role = client.add_role(
            name=role_name,
            description=description,
            weight=weight,
            propagate=propagate)
        return create_role

    @classmethod
    def get_test_endpoint_template(cls, client, temp_id=None, name=None,
                                   temp_type=None, region=None,
                                   public_url=None, internal_url=None,
                                   admin_url=None, enabled=True):
        """
        Creates a new endpoint template
        """
        temp_type = temp_type or cls.config.identity_api.type_mosso
        temp_id = temp_id or random_int(10000, 1000000000)
        name = name or rand_name("ccTestEndpoint")
        region = region or cls.config.identity_api.default_region
        public_url = public_url or cls.config.identity_api.public_url
        internal_url = internal_url or cls.config.identity_api.internal_url
        admin_url = admin_url or cls.config.identity_api.admin_url
        create_endpoint_template = (cls.admin_client
                                    .add_endpoint_template(
                                        id=temp_id,
                                        name=name,
                                        type=temp_type,
                                        region=region,
                                        public_url=public_url,
                                        internal_url=internal_url,
                                        admin_url=admin_url,
                                        enabled=enabled))
        return create_endpoint_template


class UserAdminFixture(BaseIdentityFixture):
    '''
    Sets public and admin clients with a User Admin token.
    '''

    @classmethod
    def setUpClass(cls):
        super(UserAdminFixture, cls).setUpClass()
        username = cls.config.identity_api.username
        api_key = cls.config.identity_api.api_key
        user_admin_auth = cls.public_client.authenticate_user_apikey(
            username=username,
            api_key=api_key).entity
        cls.public_client = cls.provider.get_client(
            token=user_admin_auth.token.id,
            client_type=IdentityClientTypes.DEFAULT)
        cls.admin_client = cls.provider.get_client(
            token=user_admin_auth.token.id)


class IdentityAdminFixture(BaseIdentityFixture):
    '''
    Sets public and admin clients with Identity Admin token.
    '''

    @classmethod
    def setUpClass(cls):
        super(IdentityAdminFixture, cls).setUpClass()
        admin_username = cls.config.identity_api.admin_username
        admin_password = cls.config.identity_api.admin_password
        admin_auth = cls.public_client. \
            authenticate_user_password(username=admin_username,
                                       password=admin_password).entity
        cls.public_client = cls.provider.get_client(
            token=admin_auth.token.id,
            client_type=IdentityClientTypes.DEFAULT)
        cls.admin_client = cls.provider.get_client(
            token=admin_auth.token.id)


class IdentityIntegrationFixture(RaxSignupAPI_CloudSignupFixture):
    '''
    TODO
    '''

    @classmethod
    def setUpClass(cls):
        super(IdentityIntegrationFixture, cls).setUpClass()

        metadata = [
            {"key": "cloudSitesPurchased",
             "value": "false"},
            {"key": "cloudFilesPurchased",
             "value": "true"},
            {"key": "cloudServersPurchased",
             "value": "true"},
            {"key": "loadBalancersPurchased",
             "value": "false"},
            {"key": "ipAddress",
             "value": "10.186.932.145"},
            {"key": "rackUID",
             "value": "277298293"},
            {"key": "deviceFingerPrint",
             "value": "134.288-8901"}, ]

        default_order_item = {
            'offering_id': 'CLOUD_SITES',
            'product_id': 'CLOUD_SITES',
            'quantity': '1',
        }

        request_dict = cls.get_signup_request_dict(
            metadata=metadata, default_order_item=default_order_item)

        api_response = cls.client.signup_new_cloud_customer(**request_dict)

        user_id = api_response.entity.id_
        conn = RestConnector()
        body = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns="http://cloud.rackspace.com/account/1.0">
                   <soapenv:Header/>
                   <soapenv:Body>
                      <ns:UpdateAccountStatus>
                         <ns:accountId>{0}</ns:accountId>
                         <ns:accountStatus>ACTIVE</ns:accountStatus>
                      </ns:UpdateAccountStatus>
                   </soapenv:Body>
                </soapenv:Envelope>""".format(user_id)

        conn.post("http://smix.staging.us.ccp.rackspace.net/account/1.0", body)
        ah_dict = {AuthConfig.SECTION_NAME: {
            'username': api_response.request.entity.contacts[0].user.username,
            'api_key': '',
            'password': api_response.request.entity.contacts[0].user.password}}
        ah_config = cls.config.mcp_override(ah_dict)
        cls.resources = ResourcePool()
        cls.compute_provider = _ComputeAPIProvider(ah_config, cls.fixture_log)
        cls._set_clients_from_provider()
        cls.flavor_ref = cls.config.compute_api.flavor_ref
        cls.image_ref = cls.config.compute_api.image_ref
        cls.image_ref_alt = cls.config.compute_api.image_ref_alt
        cls.flavor_ref_alt = cls.config.compute_api.flavor_ref_alt
        low_limit_user_auth = {AuthConfig.SECTION_NAME: {
            'username': cls.config.auth.low_limit_username,
            'api_key': cls.config.auth.low_limit_user_password}}
        cls.low_limit_conf = cls.config.mcp_override(low_limit_user_auth)
        cls.compute_provider_for_low_limits_user = _ComputeAPIProvider(
            cls.low_limit_conf,
            cls.fixture_log)

    @classmethod
    def _set_clients_from_provider(cls, provider=None):
        if provider is None:
            provider = cls.compute_provider
            cls.flavors_client = provider.flavors_client
            cls.flavors_client.add_exception_handler(ExceptionHandler())
            cls.servers_client = provider.servers_client
            cls.images_client = provider.images_client
            cls.limits_client = provider.limits_client
            cls.hosts_client = provider.hosts_client


class IdentityLbaaSIntegrationFixture(RaxSignupAPI_CloudSignupFixture):
    '''
    TODO
    '''

    @classmethod
    def setUpClass(cls):
        super(IdentityLbaaSIntegrationFixture, cls).setUpClass()
        metadata = [
            {"key": "cloudSitesPurchased",
             "value": "false"},
            {"key": "cloudFilesPurchased",
             "value": "true"},
            {"key": "cloudServersPurchased",
             "value": "true"},
            {"key": "loadBalancersPurchased",
             "value": "false"},
            {"key": "ipAddress",
             "value": "10.186.932.145"},
            {"key": "rackUID",
             "value": "277298293"},
            {"key": "deviceFingerPrint",
             "value": "134.288-8901"}, ]

        default_order_item = {
            'offering_id': 'CLOUD_SITES',
            'product_id': 'CLOUD_SITES',
            'quantity': '1',
        }

        request_dict = cls.get_signup_request_dict(
            metadata=metadata, default_order_item=default_order_item)

        api_response = cls.client.signup_new_cloud_customer(**request_dict)
        user_id = api_response.entity.id_
        username = api_response.request.entity.contacts[0].user.username
        password = api_response.request.entity.contacts[0].user.password
        conn = RestConnector()
        body = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns="http://cloud.rackspace.com/account/1.0">
                   <soapenv:Header/>
                   <soapenv:Body>
                      <ns:UpdateAccountStatus>
                         <ns:accountId>{0}</ns:accountId>
                         <ns:accountStatus>ACTIVE</ns:accountStatus>
                      </ns:UpdateAccountStatus>
                   </soapenv:Body>
                </soapenv:Envelope>""".format(user_id)
        conn.post("http://smix.staging.us.ccp.rackspace.net/account/1.0", body)
        ah_dict = {IdentityAPIConfig.SECTION_NAME: {'username': username,
                                                    'api_key': '',
                                                    'password': password}}
        cls.config = cls.config.mcp_override(ah_dict)
        cls.lbaas_provider = LoadBalancersProvider(cls.config,
                                                   cls.fixture_log)
        cls.tenant_id = user_id
        cls.client = cls.lbaas_provider.client
        cls.mgmt_client = cls.lbaas_provider.mgmt_client
        # Don't want to have zeus info in the production configs
        auth_url = cls.config.identity_api.authentication_endpoint
        cls.default_vip_type = cls.config.lbaas_api.default_vip_type
        if 'staging' not in auth_url.lower():
            return
