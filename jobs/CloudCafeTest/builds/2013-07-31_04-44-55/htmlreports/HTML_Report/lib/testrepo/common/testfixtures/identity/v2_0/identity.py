'''
@summary: Base Classes for Test Suites (Collections of Test Cases)
@note: Correspondes DIRECTLY TO A unittest.TestCase
@see: http://docs.python.org/library/unittest.html#unittest.TestCase
@copyright: Copyright (c) 2012 Rackspace US, Inc.
'''
from testrepo.common.testfixtures.fixtures import BaseTestFixture
from ccengine.providers.identity.v2_0.identity_api \
    import IdentityAPIProvider, IdentityClientTypes
from testrepo.common.testfixtures.rax_signup import\
        RaxSignupAPI_CloudSignupFixture
from ccengine.providers.compute.compute_api import ComputeAPIProvider \
                                                   as _ComputeAPIProvider
from ccengine.providers.atomhopper import AtomHopperProvider
from ccengine.common.resource_manager.resource_pool import ResourcePool
from ccengine.domain.configuration import AuthConfig, MiscConfig, IdentityAPIConfig
from ccengine.common.exception_handler.exception_handler import ExceptionHandler
from ccengine.common.connectors.rest import RestConnector
from ccengine.providers.lbaas.load_balancer_api import LoadBalancersProvider
from ccengine.providers.lbaas.zeus_service import ZeusProvider


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

        # Set up racker client to use Racker credentials
        racker_username = cls.config.identity_api.racker_username
        racker_password = cls.config.identity_api.racker_password
        cls.racker_client = cls.provider.get_client(
            username=racker_username,
            password=racker_password,
            client_type=IdentityClientTypes.RACKER)

        # Set default status error message
        cls.err_msg = 'Response received: {0}; Response expected: {1}'

    def _follow_link(self, link, links, method, method_args=None):
        kwargs = {'url': links[link]['url']}
        return method(method_args, requestslib_kwargs=kwargs)

    def _status_assertion(self, received, expected):
        self.assertEqual(received,
                         expected,
                         msg=self.err_msg.format(received, expected))

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
                apiKey=api_key).entity
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
        admin_auth = cls.public_client.\
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
        ah_dict = {AuthConfig.SECTION_NAME: {'username': api_response.request.entity.contacts[0].user.username, 'api_key': '', 'password': api_response.request.entity.contacts[0].user.password}}
        ah_config = cls.config.mcp_override(ah_dict)
        cls.resources = ResourcePool()
        cls.compute_provider = _ComputeAPIProvider(ah_config, cls.fixture_log)
        cls._set_clients_from_provider()
        cls.flavor_ref = cls.config.compute_api.flavor_ref
        cls.image_ref = cls.config.compute_api.image_ref
        cls.image_ref_alt = cls.config.compute_api.image_ref_alt
        cls.flavor_ref_alt = cls.config.compute_api.flavor_ref_alt
        low_limit_user_auth = {AuthConfig.SECTION_NAME: {'username': cls.config.auth.low_limit_username, 'api_key': cls.config.auth.low_limit_user_password}}
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
                                        'api_key': '', 'password': password}}
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
