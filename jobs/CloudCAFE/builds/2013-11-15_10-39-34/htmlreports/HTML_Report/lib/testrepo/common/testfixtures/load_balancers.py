'''
@summary: Base Classes for Test Suites (Collections of Test Cases)
@note: Correspondes DIRECTLY TO A unittest.TestCase
@see: http://docs.python.org/library/unittest.html#unittest.TestCase
@copyright: Copyright (c) 2012 Rackspace US, Inc.
'''
import ConfigParser

from ccengine.providers.atomhopper import AtomHopperProvider
from ccengine.providers.lbaas.load_balancer_api import LoadBalancersProvider
from ccengine.providers.lbaas.zeus_service import ZeusProvider
from ccengine.providers.objectstorage.object_storage_provider import \
    ObjectStorageClientProvider
from ccengine.domain.configuration import MiscConfig

from testrepo.common.testfixtures.fixtures import BaseTestFixture, \
    BaseParameterizedTestFixture
from testrepo.lbaas.rbac.helper_lbaas_rbac import LBaasRBACroles


class BaseLoadBalancersFixture(BaseTestFixture):
    '''
    @summary: Fixture for any Load Balancers test..
    '''
    lbs_to_delete = []
    servers_to_delete = []

    @classmethod
    def setUpClass(cls):
        super(BaseLoadBalancersFixture, cls).setUpClass()
        # init provider
        cls.lbaas_provider = LoadBalancersProvider(cls.config,
                                                   cls.fixture_log)
        cls.tenant_id = cls.config.lbaas_api.tenant_id
        cls.client = cls.lbaas_provider.client
        cls.mgmt_client = cls.lbaas_provider.mgmt_client
        cls.default_vip_type = cls.config.lbaas_api.default_vip_type

    @classmethod
    def tearDownClass(cls):
        super(BaseLoadBalancersFixture, cls).tearDownClass()
        for lb_id in cls.lbs_to_delete:
            cls.lbaas_provider.client.delete_load_balancer(lb_id)


class LoadBalancersSmokeFixture(BaseLoadBalancersFixture):

    @classmethod
    def setUpClass(cls):
        super(LoadBalancersSmokeFixture, cls).setUpClass()
        # set up load balancer for smoke tests
        cls.lb = cls.lbaas_provider.global_load_balancer

    @classmethod
    def tearDownClass(cls):
        super(LoadBalancersSmokeFixture, cls).tearDownClass()


class LoadBalancersRBACFixture(BaseLoadBalancersFixture):

    @classmethod
    def setUpClass(cls):
        super(LoadBalancersRBACFixture, cls).setUpClass()

        # Get Role Information and Responses
        cls.roles = LBaasRBACroles(fixture=cls)
        region = cls.config.lbaas_api.rbac_region

        # Create Clients for each role defined
        for role in cls.roles.users_list:
            user = getattr(cls.config.lbaas_api,
                           '{0}_role_user'.format(role))
            pswd = getattr(cls.config.lbaas_api,
                           '{0}_role_password'.format(role))

            cls.fixture_log.info("*** CREATING CLIENT FOR {0} ***".format(role))
            routine = cls.lbaas_provider.new_client(username=user,
                                                    password=pswd,
                                                    region=region)
            setattr(cls, role, routine)
        cls.lbaas_provider.client = cls.user_admin

        # Create the loadbalancer (DUT)
        cls.rbac_lb = cls.lbaas_provider.create_active_load_balancer(
            virtualIps=[{'type': 'SERVICENET'}]
        ).entity
        cls.lbs_to_delete.append(cls.rbac_lb.id)

        # IP Address to use for bogus node
        cls.test_node_address = '192.168.255.128'

    @classmethod
    def tearDownClass(cls):
        cls.lbaas_provider.wait_for_status(cls.rbac_lb.id)
        super(LoadBalancersRBACFixture, cls).tearDownClass()

    def setUp(self):
        super(LoadBalancersRBACFixture, self).setUp()
        self.lbaas_provider.wait_for_status(self.rbac_lb.id)


class LoadBalancersZeusSoapFixture(BaseLoadBalancersFixture):

    @classmethod
    def setUpClass(cls):
        super(LoadBalancersZeusSoapFixture, cls).setUpClass()
        cls.zeus_provider = ZeusProvider(cls.config, cls.fixture_log)
        cls.zeus_vs = cls.zeus_provider.zeus_vs.get_service()
        cls.zeus_tig = cls.zeus_provider.zeus_tig.get_service()
        cls.zeus_pool = cls.zeus_provider.zeus_pool.get_service()
        cls.zeus_ssl = cls.zeus_provider.zeus_ssl.get_service()
        cls.zeus_monitor = cls.zeus_provider.zeus_monitor.get_service()
        cls.zeus_protection = cls.zeus_provider.zeus_protection.get_service()

    @classmethod
    def tearDownClass(cls):
        super(LoadBalancersZeusSoapFixture, cls).tearDownClass()


class LoadBalancersZeusFixture(LoadBalancersZeusSoapFixture):

    @classmethod
    def setUpClass(cls):
        super(LoadBalancersZeusFixture, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        super(LoadBalancersZeusSoapFixture, cls).tearDownClass()


class LoadBalancersGenerateUsageFixture(BaseLoadBalancersFixture):

    @classmethod
    def setUpClass(cls):
        super(LoadBalancersGenerateUsageFixture, cls).setUpClass()
        # init providers
        cls.usage_data = ConfigParser.SafeConfigParser()

    @classmethod
    def tearDownClass(cls):
        super(LoadBalancersGenerateUsageFixture, cls).tearDownClass()


class LoadBalancersAssertUsageFixture(BaseLoadBalancersFixture):
    '''
    @summary: Fixture for any Load Balancers test..
    '''

    @classmethod
    def setUpClass(cls):
        cls.lbs_to_delete = []
        super(LoadBalancersAssertUsageFixture, cls).setUpClass()
        # init providers
        cls.lbaas_provider = LoadBalancersProvider(cls.config,
                                                   cls.fixture_log)
        alt_misc = {MiscConfig.SECTION_NAME:
                    {'serializer': 'xml',
                     'deserializer': 'xml'}}
        alt_conf = cls.config.mcp_override(alt_misc)
        cls.ah_provider = AtomHopperProvider(
            cls.config.lbaas_api.atom_feed_url,
            config=alt_conf,
            username=cls.config.lbaas_api.atom_feed_user,
            password=cls.config.lbaas_api.atom_feed_password)

    @classmethod
    def tearDownClass(cls):
        super(LoadBalancersAssertUsageFixture, cls).tearDownClass()


class LoadBalancersFixtureParameterized(BaseParameterizedTestFixture):
    '''
    @summary: Fixture for any Load Balancers test..
    '''
    lbs_to_delete = []
    servers_to_delete = []

    @classmethod
    def setUpClass(cls):
        super(LoadBalancersFixtureParameterized, cls).setUpClass()
        # init provider
        cls.lbaas_provider = LoadBalancersProvider(cls.config,
                                                   cls.fixture_log)
        cls.client = cls.lbaas_provider.client
        cls.mgmt_client = cls.lbaas_provider.mgmt_client

    @classmethod
    def tearDownClass(cls):
        super(LoadBalancersFixtureParameterized, cls).tearDownClass()
        for lb_id in cls.lbs_to_delete:
            cls.lbaas_provider.client.delete_load_balancer(lb_id)


class LoadBalancersConnectionLogFixture(LoadBalancersZeusFixture):
    '''I am a fixture for logging in load balancers as a service'''

    @classmethod
    def setUpClass(cls):
        super(LoadBalancersConnectionLogFixture, cls).setUpClass()
        cls.files_client = ObjectStorageClientProvider.get_client(
            cls.config.identity_api.username,
            cls.config.object_storage_api.region,
            api_key=cls.config.identity_api.api_key,
            password=cls.config.identity_api.password)

    @classmethod
    def tearDownClass(cls):
        super(LoadBalancersConnectionLogFixture, cls).tearDownClass()
