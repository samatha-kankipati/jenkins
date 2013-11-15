from testrepo.common.testfixtures.fixtures import BaseTestFixture
from ccengine.providers.dnsaas.domain_api import DomainProvider \
as _DomainProvider
from ccengine.providers.lbaas.load_balancer_api import LoadBalancersProvider
from ccengine.common.tools import datagen
from ccengine.providers.dnsaas.ptr_api import PtrProvider as _PtrProvider
from ccengine.providers.compute.compute_api import ComputeAPIProvider \
as _ComputeAPIProvider
import time
from ccengine.providers.legacyserv.server_api import ServerProvider
from ccengine.common.data_generators.dnsaas.domain_datagen import \
                                                         SmokeData, RecordData
from ccengine.providers.identity.v2_0.identity_api \
    import IdentityAPIProvider, IdentityClientTypes
from ccengine.clients.identity.v2_0.rax_auth_api import IdentityClient
from ccengine.common.tools.datagen import rand_name
from ccengine.clients.dnsaas.domain_api import DnsaasAPIClient
from ccengine.clients.dnsaas.ptr_api import PtrAPIClient


class DomainFixture(BaseTestFixture):
    @classmethod
    def setUpClass(cls):
        super(DomainFixture, cls).setUpClass()
        #init providers
        cls.domain_provider = _DomainProvider(cls.config, cls.fixture_log)
        cls.data = SmokeData()
        cls.name = cls.data.name
        cls.emailAddress = cls.data.emailAddress
        cls.ttl = cls.data.ttl
        cls.comment = cls.data.comment
        cls.name_list = cls.data.name_list
        cls.subname_list = cls.data.subname_list
        cls.type_list = cls.data.type_list
        cls.data_list = cls.data.data_list
        cls.ttl_list = cls.data.ttl_list
        cls.comment_list = cls.data.comment_list

    @classmethod
    def tearDownClass(cls):
        super(DomainFixture, cls).tearDownClass()


class RecordFixture(BaseTestFixture):
    @classmethod
    def setUpClass(cls):
        super(RecordFixture, cls).setUpClass()
        cls.data = RecordData()
        cls.name_domain = cls.data.name
        emailAddress = cls.data.emailAddress
        ttl = cls.data.ttl
        comment = cls.data.comment
        cls.name_list = cls.data.name_list
        cls.type_list = cls.data.type_list
        cls.data_list = cls.data.data_list
        cls.ttl_list = cls.data.ttl_list
        cls.comment_list = cls.data.comment_list
        cls.updated_comment = cls.data.updated_comment
        #init providers
        cls.domain_provider = _DomainProvider(cls.config, cls.fixture_log)
        cls.common_domain = cls.domain_provider.\
                            client.create_domain(name=cls.name_domain,
                emailAddress=emailAddress, ttl=ttl, comment=comment)
        time.sleep(5)
        response = cls.domain_provider.client.\
        list_all_domain()
        cls.domain_id = response.entity[0].id

    @classmethod
    def tearDownClass(cls):
        par = \
        cls.domain_provider.client.delete_domain(cls.domain_id)
        if not par.ok:
            cls.assertClassTeardownFailure('Unable to delete domain in \
            tear down')
        super(RecordFixture, cls).tearDownClass()


class PtrFixture(BaseTestFixture):
    @classmethod
    def setUpClass(cls):
        super(PtrFixture, cls).setUpClass()
        #init providers
        cls.ptr_provider = _PtrProvider(cls.config, cls.fixture_log)
        cls.server_provider = ServerProvider(cls.config, cls.fixture_log)
        cls.common_legacyserv = cls.server_provider.\
                                    create_active_server().entity
        cls.serverid = cls.common_legacyserv.id
        cls.data = cls.common_legacyserv.addresses.public[0]
        print cls.serverid
        print cls.data

    @classmethod
    def tearDownClass(cls):
        super(PtrFixture, cls).tearDownClass()
        par = cls.server_provider.client.delete_server(cls.serverid)


class PtrFixtureLbaas(BaseTestFixture):

    @classmethod
    def setUpClass(cls):

        super(PtrFixtureLbaas, cls).setUpClass()
        #init providers
        cls.ptr_provider = _PtrProvider(cls.config, cls.fixture_log)
        cls.lbaas_provider = LoadBalancersProvider(cls.config,
                                                   cls.fixture_log)
        #create common load balancers to be shared between test cases
        cls.common_lb = cls.lbaas_provider.create_active_load_balancer().entity

        cls.lb_id = cls.common_lb.id
        cls.lb_ipv4 = cls.common_lb.get_public_ipv4_vip().address
        cls.lb_ipv6 = cls.common_lb.get_public_ipv6_vip().address

    @classmethod
    def tearDownClass(cls):
        super(PtrFixtureLbaas, cls).tearDownClass()
        par = cls.lbaas_provider.client.delete_load_balancer(cls.lb_id)
        if not par.ok:
            cls.assertClassTeardownFailure('Unable to delete \
            LoadBalancer in tear down')


class Dnsaas_APIIntegrationFixture(BaseTestFixture):

    @classmethod
    def setUpClass(cls):
        super(Dnsaas_APIIntegrationFixture, cls).setUpClass()
        cls.ptr_provider = _PtrProvider(cls.config, cls.fixture_log)
        cls.compute_api_provider = _ComputeAPIProvider(cls.config)


class Dnsaas_ServerIntegrationFixture(Dnsaas_APIIntegrationFixture):
    '''
    @summary: Foundation for any test requiring a server
              to be built and access to all api's.
    '''
    @classmethod
    def setUpClass(cls):
        super(Dnsaas_ServerIntegrationFixture, cls).setUpClass()

        #Create test server
        cls.fixture_log.info('Creating test server')
        image = cls.config.compute_api.image_ref
        flavor = cls.config.compute_api.flavor_ref
        cls.server_name = datagen.timestamp_string('CinderAPI_VolWriteTest:')
        cls.create_server_response = cls.compute_api_provider.\
            create_active_server(image_ref=image, flavor_ref=flavor,
                                 name=cls.server_name)

        if not cls.create_server_response.ok:
            cls.assertClassSetupFailure('Server Create Failed in setup')

        cls.testserver = cls.create_server_response.entity
        if cls.testserver.status == 'ERROR':
            cls.assertClassSetupFailure('Server Create Failed in setup, \
            server is in Error state')

        cls.fixture_log.debug('%s' % str(cls.testserver))
        cls.server_id = cls.testserver.id
        cls.public_ipv4 = cls.testserver.addresses.public.ipv4
        cls.public_ipv4 = cls.testserver.addresses.public.ipv6
        cls.admin_pass = cls.testserver.adminPass

    @classmethod
    def tearDownClass(cls):
        #delete server
        par = \
        cls.compute_api_provider.servers_client.delete_server(cls.server_id)
        if not par.ok:
            cls.assertClassTeardownFailure('Unable to delete server in \
            tear down')

        #finish local tear down class before doing parent tear down class
        super(Dnsaas_ServerIntegrationFixture, cls).tearDownClass()


class BaseIdentityFixture(BaseTestFixture):
    '''
    Sets up public client and admin clients without tokens.
    '''
    @classmethod
    def setUpClass(cls):
        super(BaseIdentityFixture, cls).setUpClass()

        #Init provider
        cls.provider = IdentityAPIProvider(cls.config)

        #Set up public client without token
        cls.public_client = cls.provider.get_client(
                    client_type=IdentityClientTypes.DEFAULT)

        #Set up admin client without token
        cls.admin_client = cls.provider.get_client()


class IdentityAdminFixture(BaseIdentityFixture):
    '''
    Sets public and admin clients with Identity Admin token.
    '''

    @classmethod
    def setUpClass(cls):
        super(IdentityAdminFixture, cls).setUpClass()
        admin_username = cls.config.identity_api.admin_username
        admin_password = cls.config.identity_api.admin_password
        rel = cls.config.dnsaas.rel
        href = cls.config.dnsaas.href

        auth_data = cls.public_client.\
            authenticate_user_password(username=admin_username,
                                       password=admin_password).entity
        if cls.config.dnsaas.url is not None:
            cls.url = cls.config.dnsaas.url
        else:
            service_name = cls.config.dnsaas.identity_service_name
            service = auth_data.serviceCatalog.get_service(service_name)
            if service is not None:
                cls.url = service.endpoints[0].publicURL

        admin_auth = cls.public_client.\
            authenticate_user_password(username=admin_username,
                                       password=admin_password).entity
        cls.public_client = cls.provider.get_client(
                token=admin_auth.token.id,
                client_type=IdentityClientTypes.DEFAULT)
        cls.admin_client = cls.provider.get_client(
                token=admin_auth.token.id)
        username = cls.config.identity_api.username
        api_key = cls.config.identity_api.api_key
        user_admin_auth = cls.public_client.authenticate_user_apikey(
                username=username, apiKey=api_key).entity
        endpoint = cls.config.identity_api.authentication_endpoint
        serializer = cls.config.misc.serializer
        deserializer = cls.config.misc.deserializer
        cls.user_admin_client = IdentityClient(
                url=endpoint,
                serialize_format=serializer,
                deserialize_format=deserializer,
                auth_token=user_admin_auth.token.id)
        limit = 100
        list_roles = cls.admin_client.list_roles(limit)
        assert list_roles.status_code == 200
        roles = list_roles.entity
        for role in roles:
            if role.name == 'dnsaas:creator':
                cls.createrid = role.id

            elif role.name == 'dnsaas:observer':
                cls.observerid = role.id

            elif role.name == 'dnsaas:admin':
                cls.adminid = role.id

        cls.rolesids = [cls.adminid, cls.createrid, cls.observerid]

        cls.subdomainids = []
        cls.tokens = []
        for i in range(3):
            username = rand_name("dnsqeusersubuser")
            email = username + "@rackspace.com"
            password = "Pass1234"
            create_user = cls.admin_client.add_user(
                    username=username,
                    email=email,
                    password=password)
            cls.subdomainids.append(create_user.entity.id)
            api_key = "56b39aa3492d27aca1d3cbd795294e31"
            auth_subuser_token = cls.public_client.\
            authenticate_user_password(username=username,
                                       password=password).entity.token.id
            cls.tokens.append(auth_subuser_token)

        cls.clientadmin = DnsaasAPIClient(cls.url, cls.tokens[0],
                                      cls.config.misc.serializer,
                                      cls.config.misc.deserializer)
        cls.clientcreator = DnsaasAPIClient(cls.url, cls.tokens[1],
                                      cls.config.misc.serializer,
                                      cls.config.misc.deserializer)
        cls.clientobserver = DnsaasAPIClient(cls.url, cls.tokens[2],
                                      cls.config.misc.serializer,
                                      cls.config.misc.deserializer)

        cls.client_admin_ptr = PtrAPIClient(cls.url, rel, href, cls.tokens[0],
                                      cls.config.misc.serializer,
                                      cls.config.misc.deserializer)

        cls.client_creator_ptr = PtrAPIClient(cls.url, rel, href,
                                              cls.tokens[1],
                                              cls.config.misc.serializer,
                                              cls.config.misc.deserializer)

        cls.client_observer_ptr = PtrAPIClient(cls.url, rel, href,
                                                cls.tokens[2],
                                                cls.config.misc.serializer,
                                                cls.config.misc.deserializer)

        for i in range(len(cls.subdomainids)):
            add_global_role = cls.admin_client.add_role_to_user(
                userId=cls.subdomainids[i],
                roleId=cls.rolesids[i])
