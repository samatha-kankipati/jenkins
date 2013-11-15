'''
@summary: Base Classes for Test Suites (Collections of Test Cases)
@note: Correspondes DIRECTLY TO A unittest.TestCase
@see: http://docs.python.org/library/unittest.html#unittest.TestCase
@copyright: Copyright (c) 2012 Rackspace US, Inc.
'''
import time
from ccengine.clients.compute.servers_api import ServerAPIClient
from ccengine.common.constants.networks_constants import Constants
from ccengine.common.constants.networks_constants import HTTPResponseCodes
from ccengine.common.exceptions.compute import ItemNotFound
from ccengine.common.tools import datagen
from ccengine.domain.configuration import AuthConfig
from ccengine.domain.types import NovaImageStatusTypes, NovaServerStatusTypes
from ccengine.providers.compute.compute_api import ComputeAPIProvider
from ccengine.providers.compute_admin.compute_admin_api \
    import ComputeAdminProvider
from ccengine.providers.networks.isolated_networks \
    import IsolatedNetworksProvider
from ccengine.providers.nvp.nvp_api import NVPProvider
from ccengine.providers.quantum.quantum_api import QuantumProvider
from testrepo.common.testfixtures.fixtures import BaseTestFixture
from testrepo.networks.helper import Helper


class BaseNetworksFixture(BaseTestFixture):
    """Basic networks fixture without alternate users or providers"""
    @classmethod
    def setUpClass(cls):
        super(BaseNetworksFixture, cls).setUpClass()
        cls.networks_to_delete = []
        cls.servers_to_delete = []
        cls.images_to_delete = []

        #init providers
        cls.networks_provider = IsolatedNetworksProvider(cls.config,
                                                         cls.fixture_log)
        cls.servers_provider = ComputeAPIProvider(cls.config, cls.fixture_log)

        if cls.config.nvp_api.endpoint:
            cls.nvp_provider = NVPProvider(cls.config, cls.fixture_log)
        else:
            cls.nvp_provider = None

        # flag for NVP checks in Preprod
        cls.run_nvp = cls.config.isolated_networks_api.run_nvp

        # flag for ifconfig eth IP addresses order check when adding fixed IPs
        cls.ifconfig_order_check = cls.config.isolated_networks_api.\
            ifconfig_order_check

        # set up Public and ServiceNet network objects
        cls.public_network = cls.networks_provider.get_public_network()
        cls.private_network = cls.networks_provider.get_private_network()

        # set up helper instance
        cls.helper = Helper(cls.networks_provider, cls.servers_provider,
                            cls.nvp_provider, cls.servers_to_delete,
                            cls.networks_to_delete, cls.run_nvp)

    @classmethod
    def tearDownClass(cls):
        super(BaseNetworksFixture, cls).tearDownClass()
        cls.fixture_log.debug('Cleaning up servers and networks')
        cleanup_servers_and_networks(cls.servers_provider,
                                     cls.servers_to_delete,
                                     cls.networks_provider,
                                     cls.networks_to_delete)


class AdminFixture(BaseNetworksFixture):
    """Admin user fixture for the add and remove fixed ip calls"""
    @classmethod
    def setUpClass(cls):
        super(AdminFixture, cls).setUpClass()
        cls.admin_provider = ComputeAdminProvider(cls.config, cls.fixture_log)

    @classmethod
    def tearDownClass(cls):
        super(AdminFixture, cls).tearDownClass()
        pass


class QuantumFixture(BaseTestFixture):
    """Quantum Networks Test Fixture"""
    @classmethod
    def setUpClass(cls):
        super(QuantumFixture, cls).setUpClass()
        cls.tenant_id = cls.config.auth.tenant_id
        cls.q_networks_to_delete = []
        cls.quantum_provider = QuantumProvider(cls.config, cls.fixture_log)

    @classmethod
    def tearDownClass(cls):
        super(QuantumFixture, cls).tearDownClass()
        cls.fixture_log.debug('Cleaning up quantum networks')
        r = cls.quantum_provider.delete_network_list(cls.q_networks_to_delete)
        if r:
            cls.fixture_log.debug(
                            'Unable to delete quantum networks {0}'.format(r))


class NetworksRBACFixture(BaseNetworksFixture):
    """RBAC Fixture for admin, creator and observer users"""
    @classmethod
    def setUpClass(cls):
        super(NetworksRBACFixture, cls).setUpClass()
        cls.admin_networks_to_delete = []
        cls.admin_servers_to_delete = []
        cls.creator_networks_to_delete = []
        cls.creator_servers_to_delete = []
        cls.observer_networks_to_delete = []
        cls.observer_servers_to_delete = []

        cls.create_msg = 'Unable to create {0} network: {1} {2} {3}'
        cls.get_msg = 'Unable to get network: {0} {1} {2}'
        cls.list_msg = 'Unable to list networks: {0} {1} {2}'
        cls.delete_msg = 'Unable to delete {0} network: {1} {2} {3}'
        cls.nvp_msg = 'NVP switch NOT found for Network {0}'
        cls.nvpf_msg = 'NVP switch found for deleted Network {0}'
        cls.ucreate_msg = 'Unexpected, able to create {0} network: {1} {2} {3}'
        cls.uadelete_msg = ('Unexpected, able to delete {0} network: {1} {2} '
                            '{3}')
        cls.udelete_msg = ('Unexpected, able to get deleted network: '
                           '{0} {1} {2}')
        cls.ucidr_msg = 'Unexpected {0} network cidr, expected: {1}'
        cls.uname_msg = 'Unexpected {0} network name, expected: {1}'
        cls.ulist_msg = ('Unexpected network list, network {0} should {1} '
                         'be in list')
        cls.unvp_msg = ('Unexpected NVP Switch display name: {0}, '
                    'expected network name: {1}')
        cls.setup_msg = 'setUp failure: unable to create {0} network'

        # set up admin user and providers
        cls.admin_servers_provider, cls.admin_networks_provider, \
            cls.admin_nvp_provider = set_up_user_providers(
                config=cls.config, fixture_log=cls.fixture_log, role='admin')

        cls.admin_helper = Helper(cls.admin_networks_provider,
            cls.admin_servers_provider, cls.admin_nvp_provider,
            cls.admin_servers_to_delete, cls.admin_networks_to_delete)

        # set up creator user and providers
        cls.creator_servers_provider, cls.creator_networks_provider, \
            cls.creator_nvp_provider = set_up_user_providers(
                config=cls.config, fixture_log=cls.fixture_log, role='creator')

        cls.creator_helper = Helper(cls.creator_networks_provider,
            cls.creator_servers_provider, cls.creator_nvp_provider,
            cls.creator_servers_to_delete, cls.creator_networks_to_delete)

        # set up observer user and providers
        cls.observer_servers_provider, cls.observer_networks_provider, \
            cls.observer_nvp_provider = set_up_user_providers(
                config=cls.config, fixture_log=cls.fixture_log,
                role='observer')

        cls.observer_helper = Helper(cls.observer_networks_provider,
            cls.observer_servers_provider, cls.observer_nvp_provider,
            cls.observer_servers_to_delete, cls.observer_networks_to_delete)

        # IPv4 test networks created by admin and creator
        network_name = datagen.rand_name('test_admin_net')
        prefix = '171.*.*.0'
        suffix = '24'
        cidr = datagen.random_cidr(ip_pattern=prefix, mask=suffix)
        cls.admin_helper.assert_ip_version(ips=cidr, version=4)
        resp = cls.admin_networks_provider.client.create_network(cidr=cidr,
            label=network_name)
        cls.assertResponse(resp, HTTPResponseCodes.CREATE_NETWORK,
                           cls.setup_msg.format('IPv4 Admin'))
        cls.admin_networks_to_delete.append(resp.entity.id)
        cls.admin_network = resp.entity

        network_ipv6_name = datagen.rand_name('test_admin_ipv6_net')
        cidr = '2001:db8::/32'
        cls.admin_helper.assert_ip_version(ips=cidr, version=6)
        resp = cls.admin_networks_provider.client.create_network(cidr=cidr,
            label=network_ipv6_name)
        cls.assertResponse(resp, HTTPResponseCodes.CREATE_NETWORK,
                           cls.setup_msg.format('IPv6 Admin'))
        cls.admin_networks_to_delete.append(resp.entity.id)
        cls.admin_ipv6_network = resp.entity


#    BUG 778: creator role getting a 503 when creating a network using admin
#    network for now

        cls.creator_network = cls.admin_network

#        network_name = datagen.rand_name('test_creator_net')
#        prefix = '171.*.*.0'
#        suffix = '24'
#        cidr = datagen.random_cidr(ip_pattern=prefix, mask=suffix)
#        cls.creator_helper.assert_ip_version(ips=cidr, version=4)
#        resp = cls.creator_networks_provider.client.create_network(cidr=cidr,
#            label=network_name)
#        cls.assertResponse(resp, HTTPResponseCodes.CREATE_NETWORK,
#                           cls.setup_msg.format('IPv4 Creator'))
#        cls.admin_networks_to_delete.append(resp.entity.id)
#        cls.creator_network = resp.entity
#        print cls.creator_network
#
#
#        network_ipv6_name = datagen.rand_name('test_creator_ipv6_net')
#        cidr = '2000:db8::/32'
#        cls.creator_helper.assert_ip_version(ips=cidr, version=6)
#        resp = cls.creator_networks_provider.client.create_network(cidr=cidr,
#            label=network_ipv6_name)
#        cls.assertResponse(resp, HTTPResponseCodes.CREATE_NETWORK,
#                           cls.setup_msg.format('IPv6 Creator'))
#        cls.admin_networks_to_delete.append(resp.entity.id)
#        cls.creator_ipv6_network = resp.entity
#        print cls.creator_ipv6_network


        # expected forbidden or unallowed http response
        cls.unallowed_status = HTTPResponseCodes.FORBIDDEN

    @classmethod
    def create_rbac_server(cls, networks, role):
        """
        @summary: Create an RBAC server
        @param networks: network ids to provision the server with
        @type: list
        @param role: user role, for ex. admin, creator or observer
        @type: str
        """
        networks_dict = cls.admin_networks_provider.get_server_network_dd(
            networks)

        servers_role = '{0}_servers_provider'.format(role)
        if hasattr(cls, servers_role):
            servers_provider = getattr(cls, servers_role)
        else:
            cls.assertClassSetupFailure('{0} unavailable'.format(servers_role))

        resp = servers_provider.create_server_no_wait(networks=networks_dict)
        msg = 'Unable to create {0} server with networks: {1}. {2} {3} {4}'\
            .format(role, networks, resp.status_code, resp.reason,
                    resp.content)
        cls.assertResponse(resp, HTTPResponseCodes.CREATE_SERVER, msg)
        cls.admin_servers_to_delete.append(resp.entity.id)
        return resp.entity

    @classmethod
    def wait_for_rbac_server(cls, server_id, role):
        """
        @summary: Wait for an Active RBAC server
        @param server_id: server ids to wait for to be active
        @type: str
        @param role: user role, for ex. admin, creator or observer
        @type: str
        """
        servers_role = '{0}_servers_provider'.format(role)
        if hasattr(cls, servers_role):
            servers_provider = getattr(cls, servers_role)
        else:
            cls.assertClassSetupFailure('{0} unavailable'.format(servers_role))

        resp = servers_provider.wait_for_server_status(server_id,
            NovaServerStatusTypes.ACTIVE)
        msg = 'Unable to get {0} active {1} server: {2} {3} {4}'.format(
            role, server_id, resp.status_code, resp.reason, resp.content)
        cls.assertResponse(resp, HTTPResponseCodes.GET_SERVER, msg)
        return resp.entity

    @classmethod
    def assertResponse(cls, resp, http_resp, msg):
        """
        @summary: Assert the HTTP Response Code
        @param resp: API response
        @type: requests.models.Response object
        @param http_resp: HTTP Response Code
        @type: int
        @param msg: Error message
        @type: str
        """
        try:
            assert resp.status_code == http_resp
        except AssertionError:
            cls.tearDownClass()
            cls.assertClassSetupFailure(msg)

    @classmethod
    def tearDownClass(cls):
        super(NetworksRBACFixture, cls).tearDownClass()

        # admin user clean up
        cls.fixture_log.debug('Cleaning up admin servers and networks')
        cleanup_servers_and_networks(cls.admin_servers_provider,
                                     cls.admin_servers_to_delete,
                                     cls.admin_networks_provider,
                                     cls.admin_networks_to_delete)

        # creator user clean up
        cls.fixture_log.debug('Cleaning up creator servers and networks')
        cleanup_servers_and_networks(cls.creator_servers_provider,
                                     cls.creator_servers_to_delete,
                                     cls.creator_networks_provider,
                                     cls.creator_networks_to_delete)

        # observer user clean up
        cls.fixture_log.debug('Cleaning up observer servers and networks')
        cleanup_servers_and_networks(cls.observer_servers_provider,
                                     cls.observer_servers_to_delete,
                                     cls.observer_networks_provider,
                                     cls.observer_networks_to_delete)


class NetworksAltUserFixture(BaseNetworksFixture):
    """Original Base Networks Fixture"""
    @classmethod
    def setUpClass(cls):
        super(NetworksAltUserFixture, cls).setUpClass()
        cls.alt_networks_to_delete = []
        cls.alt_servers_to_delete = []

        #set up alt user and providers
        alt_user = ({AuthConfig.SECTION_NAME:
                    {'username': cls.config.auth.alt_username,
                    'api_key': cls.config.auth.alt_api_key,
                    'password': cls.config.auth.alt_password}})
        alt_conf = cls.config.mcp_override(alt_user)
        cls.alt_networks_provider = IsolatedNetworksProvider(alt_conf,
                                                             cls.fixture_log)
        cls.alt_servers_provider = ComputeAPIProvider(alt_conf,
                                                      cls.fixture_log)

    @classmethod
    def tearDownClass(cls):
        super(NetworksAltUserFixture, cls).tearDownClass()
        cls.fixture_log.debug('Cleaning up alt user servers and networks')
        cleanup_servers_and_networks(cls.alt_servers_provider,
                                     cls.alt_servers_to_delete,
                                     cls.alt_networks_provider,
                                     cls.alt_networks_to_delete)


class NetworksMDIFixture(BaseNetworksFixture):
    """MDI Networks Test Fixture"""
    @classmethod
    def setUpClass(cls):
        super(NetworksMDIFixture, cls).setUpClass()

        cls.tenant_id = cls.config.auth.tenant_id
        #NVP clients for Cell0001 and Cell0002
        cls.cell_01 = cls.nvp_provider.aic_client
        cls.cell_02 = cls.nvp_provider.aic_client2
        assert cls.cell_01, 'NVP Client unavailable'
        assert cls.cell_02, 'NVP Client unavailable'

        #Relations to be used in NVP queries
        cls.switch_relation = 'LogicalSwitchStatus'
        cls.port_relation = ['LogicalSwitchConfig', 'LogicalPortAttachment']

        #where vif switch ports are expected by default
        cls.primary = 'cell_02'

        #set up server providers for both Cells
        cell_url = 'http://nova-api01.{0}.netdev-ord.ohthree.com:8774/v2/{1}'

        cls.servers_provider_01 = ComputeAPIProvider(cls.config,
                                                     cls.fixture_log)

        client_01 = ServerAPIClient(cell_url.format('c0001', cls.tenant_id),
                            cls.servers_provider_01.auth_token,
                            cls.servers_provider_01.config.misc.serializer,
                            cls.servers_provider_01.config.misc.deserializer)

        cls.servers_provider_01.servers_client = client_01

        cls.servers_provider_02 = ComputeAPIProvider(cls.config,
                                                     cls.fixture_log)

        client_02 = ServerAPIClient(cell_url.format('c0002', cls.tenant_id),
                            cls.servers_provider_02.auth_token,
                            cls.servers_provider_02.config.misc.serializer,
                            cls.servers_provider_02.config.misc.deserializer)

        cls.servers_provider_02.servers_client = client_02

        #set up helper instances for both Cells
        cls.helper_01 = Helper(cls.networks_provider, cls.servers_provider_01,
                            cls.nvp_provider, cls.servers_to_delete,
                            cls.networks_to_delete)
        cls.helper_02 = Helper(cls.networks_provider, cls.servers_provider_02,
                            cls.nvp_provider, cls.servers_to_delete,
                            cls.networks_to_delete)

    @classmethod
    def tearDownClass(cls):
        super(NetworksMDIFixture, cls).tearDownClass()


class NetworksTestFixture(NetworksAltUserFixture):

    @classmethod
    def setUpClass(cls):
        super(NetworksTestFixture, cls).setUpClass()

        #init global network and gateway server
        cidr = '172.16.99.0/24'
        network_label = datagen.random_string('shared_network')
        r = cls.networks_provider.client.create_network(cidr=cidr,
                                                        label=network_label)
        cls.shared_network = r.entity
        cls.networks_to_delete.append(cls.shared_network.id)

    @classmethod
    def tearDownClass(cls):
        super(NetworksTestFixture, cls).tearDownClass()


class NetworksGatewayServerFixture(NetworksAltUserFixture):
    '''
    @summary: Fixture for any Isolated Networks test..
    '''
    @classmethod
    def setUpClass(cls):
        super(NetworksGatewayServerFixture, cls).setUpClass()

        #init global network and gateway server
        cidr = '172.16.99.0/24'
        network_label = datagen.random_string('shared_network')
        cls.fixture_log.debug('Creating shared network.')
        r = cls.networks_provider.client.create_network(cidr=cidr,
                                                        label=network_label)
        cls.shared_network = r.entity
        cls.networks_to_delete.append(cls.shared_network.id)

        server_name = datagen.random_string('gateway_server')
        network_list = [{'uuid': cls.shared_network.id},
                    {'uuid': cls.networks_provider.get_public_network().id}]
        cls.fixture_log.debug('Creating gatway server and wait for ACTIVE.')
        r = cls.servers_provider.create_active_server(name=server_name,
                                                      networks=network_list)
        cls.gateway_server = r.entity
        cls.servers_to_delete.append(cls.gateway_server.id)
        assert cls.gateway_server.status == NovaServerStatusTypes.ACTIVE, \
               'Shared server BUILD timeout.'
        admin_pass_gateway = cls.gateway_server.adminPass
        r = cls.servers_provider.servers_client.get_server(
                                                        cls.gateway_server.id)
        cls.gateway_server = r.entity
        cls.gateway_server.adminPass = admin_pass_gateway
        assert cls.gateway_server.addresses.public is not None, \
              'Public network was not assigned to this server.'
        assert cls.gateway_server.addresses.public.ipv4 is not None, \
              'Public IPv4 address was not assigned to this server.'
        cls.gateway_ip = cls.gateway_server.addresses.public.ipv4

    @classmethod
    def tearDownClass(cls):
        super(NetworksGatewayServerFixture, cls).tearDownClass()


class NetworksServerActionsFixture(NetworksAltUserFixture):

    @classmethod
    def setUpClass(cls):
        super(NetworksServerActionsFixture, cls).setUpClass()

        #init global network and gateway server
        cidr = '172.16.99.0/24'
        network_label = datagen.random_string('shared_network')
        cls.fixture_log.debug('Creating shared network.')
        r = cls.networks_provider.client.create_network(cidr=cidr,
                                                        label=network_label)
        cls.shared_network = r.entity
        cls.networks_to_delete.append(cls.shared_network.id)

        server_name = datagen.random_string('actions_shared_server')
        network_list = [{'uuid': cls.shared_network.id},
                    {'uuid': cls.networks_provider.get_public_network().id}]
        cls.fixture_log.debug('Creating shared server and wait for ACTIVE.')
        r = cls.servers_provider.create_active_server(name=server_name,
                                                      networks=network_list)
        cls.shared_server = r.entity
        cls.servers_to_delete.append(cls.shared_server.id)
        assert cls.shared_server.status == NovaServerStatusTypes.ACTIVE, \
               'Shared server BUILD timeout.'
        admin_pass_shared = cls.shared_server.adminPass
        r = cls.servers_provider.servers_client.get_server(
                                                        cls.shared_server.id)
        cls.shared_server = r.entity
        cls.shared_server.adminPass = admin_pass_shared
        assert cls.shared_server.addresses.public is not None, \
              'Public network was not assigned to this server.'
        assert cls.shared_server.addresses.public.ipv4 is not None, \
              'Public IPv4 address was not assigned to this server.'
        cls.shared_ip = cls.shared_server.accessIPv4
        image_name = datagen.random_string('test_networks_image')
        cls.fixture_log.debug('Creating image of shared server.')
        r = cls.servers_provider.servers_client.create_image(
                                                      cls.shared_server.id,
                                                      name=image_name)
        image_loc_split = r.headers['Location'].split('/')
        image_id = image_loc_split[len(image_loc_split) - 1]
        cls.fixture_log.debug('Waiting for image %s to become active'
                              % image_id)
        r = cls.servers_provider.wait_for_image_status(image_id,
                                                 NovaImageStatusTypes.ACTIVE)
        cls.shared_image = r.entity
        cls.images_to_delete.append(cls.shared_image.id)

    @classmethod
    def tearDownClass(cls):
        super(NetworksServerActionsFixture, cls).tearDownClass()


class NetworksManagedRackConnectUsersFixture(NetworksAltUserFixture):

    @classmethod
    def setUpClass(cls):
        super(NetworksManagedRackConnectUsersFixture, cls).setUpClass()
        cls.public_network = cls.networks_provider.get_public_network()
        cls.private_network = cls.networks_provider.get_private_network()
        cls.managed_networks_to_delete = []
        cls.managed_servers_to_delete = []
        cls.rackconnect_networks_to_delete = []
        cls.rackconnect_servers_to_delete = []

        # Get Public and ServiceNet network IDs
        cls.public_id = cls.public_network.id
        cls.private_id = cls.private_network.id
        cls.public_label = cls.public_network.label
        cls.private_label = cls.private_network.label

        # set up managed user and providers
        cls.managed_servers_provider, cls.managed_networks_provider, \
            cls.managed_nvp_provider = set_up_user_providers(
                config=cls.config, fixture_log=cls.fixture_log, role='managed')

        # set up helper instance
        cls.managed_helper = Helper(cls.managed_networks_provider,
            cls.managed_servers_provider, cls.managed_nvp_provider,
            cls.managed_servers_to_delete, cls.managed_networks_to_delete)

        # set up rackconnect user and providers
        cls.rackconnect_servers_provider, cls.rackconnect_networks_provider, \
            cls.rackconnect_nvp_provider = set_up_user_providers(
                config=cls.config, fixture_log=cls.fixture_log,
                role='rackconnect')

        # set up helper instance
        cls.rackconnect_helper = Helper(cls.rackconnect_networks_provider,
            cls.rackconnect_servers_provider, cls.rackconnect_nvp_provider,
            cls.rackconnect_servers_to_delete,
            cls.rackconnect_networks_to_delete)

        # Set isolated networks data for Managed and Rackconnect
        prefix = '188.*.*.0'
        suffix = '24'
        cidr_m = datagen.random_cidr(ip_pattern=prefix, mask=suffix)
        cidr_r = datagen.random_cidr(ip_pattern=prefix, mask=suffix)
        name_m = datagen.rand_name('n_network_managed')
        name_r = datagen.rand_name('n_network_rackconnect')

        # Create isolated networks for Managed and Rackconnect users
        req_m = cls.managed_networks_provider.client.create_network(
            cidr=cidr_m, label=name_m)
        assert req_m.status_code == HTTPResponseCodes.CREATE_NETWORK, \
            'Networks create failed: {0}'.format(req_m.content)
        cls.managed_networks_to_delete.append(req_m.entity.id)
        cls.managed_network_id = req_m.entity.id
        cls.managed_network_label = req_m.entity.label
        req_r = cls.rackconnect_networks_provider.client.create_network(
            cidr=cidr_r, label=name_r)
        assert req_r.status_code == HTTPResponseCodes.CREATE_NETWORK, \
            'Networks create failed: {0}'.format(req_m.content)
        cls.rackconnect_networks_to_delete.append(req_r.entity.id)
        cls.rackconnect_network_id = req_r.entity.id
        cls.rackconnect_network_label = req_r.entity.label

    @classmethod
    def tearDownClass(cls):
        super(NetworksManagedRackConnectUsersFixture, cls).tearDownClass()
        cls.fixture_log.debug('Cleaning up managed user servers and networks')
        cleanup_servers_and_networks(cls.managed_servers_provider,
                                     cls.managed_servers_to_delete,
                                     cls.managed_networks_provider,
                                     cls.managed_networks_to_delete)

        cls.fixture_log.debug('Cleaning up rackconnect user servers and '
                              'networks')
        cleanup_servers_and_networks(cls.rackconnect_servers_provider,
                                     cls.rackconnect_servers_to_delete,
                                     cls.rackconnect_networks_provider,
                                     cls.rackconnect_networks_to_delete)


class NetworksPerformanceFixture(NetworksAltUserFixture):

    @classmethod
    def setUpClass(cls):
        super(NetworksPerformanceFixture, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        super(NetworksPerformanceFixture, cls).tearDownClass()
        cls.fixture_log.debug('Cleaning up performance servers.')
        for server_id in cls.servers_to_delete:
            cls.servers_provider.servers_client.delete_server(server_id)
        time.sleep(5)
        cls.fixture_log.debug('Cleaning up performance networks.')
        for network_id in cls.networks_to_delete:
            cls.networks_provider.client.delete_network(network_id)


def set_up_user_providers(config, fixture_log, role):
    """
    @summary: Create providers for a given user
    @param config: User config object
    @type: ConfigParser.SafeConfigParser instance
    @param fixture_log: Fixture log
    @type: logging.Logger object
    @param role: User role, for ex. admin, creator, observer, managed, etc.
    @type: str
    """
    user_path = '{0}_username'.format(role)
    api_key_path = '{0}_api_key'.format(role)
    pass_path = '{0}_password'.format(role)

    if hasattr(config.isolated_networks_api, user_path):
        username = getattr(config.isolated_networks_api, user_path)
    else:
        username = None

    if hasattr(config.isolated_networks_api, api_key_path):
        api_key = getattr(config.isolated_networks_api, api_key_path)
    else:
        api_key = None

    if hasattr(config.isolated_networks_api, pass_path):
        password = getattr(config.isolated_networks_api, pass_path)
    else:
        password = None

    user = {AuthConfig.SECTION_NAME:
        {'username': username, 'api_key': api_key, 'password': password}}
    conf = config.mcp_override(user)
    networks_provider = IsolatedNetworksProvider(conf, fixture_log)
    servers_provider = ComputeAPIProvider(conf, fixture_log)
    if config.nvp_api.endpoint:
        nvp_provider = NVPProvider(conf, fixture_log)
    else:
        nvp_provider = None

    return servers_provider, networks_provider, nvp_provider


def cleanup_servers_and_networks(servers_provider, servers_to_delete,
                                 networks_provider, networks_to_delete):
    """
    @summary: Delete test servers and networks
    @param servers_provider: Server Provider
    @type: ComputeAPIProvider object
    @param servers_to_delete: Servers to delete ids
    @type: list
    @param networks_provider: Networks Provider
    @type: IsolatedNetworksProvider object
    @param networks_to_delete: Networks to delete ids
    @type: list
    """
    for server_id in servers_to_delete:
        servers_provider.servers_client.delete_server(server_id)
    for server_id in servers_to_delete:
        time_count = 0
        while True:
            try:
                resp = servers_provider.servers_client.get_server(server_id)
                if (resp.status_code == HTTPResponseCodes.NOT_FOUND or
                    time_count > Constants.DELETE_SERVER_TIMEOUT):
                    break
            except ItemNotFound:
                break
            finally:
                time.sleep(1)
                time_count += 1
    for network_id in networks_to_delete:
        networks_provider.client.delete_network(network_id)
