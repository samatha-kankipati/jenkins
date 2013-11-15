from collections import namedtuple
import time
from ccengine.providers.compute.compute_api import ComputeAPIProvider
from ccengine.providers.nvp.nvp_api import NVPProvider
from ccengine.common.exceptions.compute import ItemNotFound
from ccengine.providers.networks.isolated_networks import \
    IsolatedNetworksProvider
from ccengine.common.tools import datagen
from testrepo.common.testfixtures.fixtures import BaseTestFixture


class RackConnectBaseFixture(BaseTestFixture):
    @classmethod
    def setUpClass(cls):
        super(RackConnectBaseFixture, cls).setUpClass()
        cls.servers_to_delete = []
        cls.servers_provider = ComputeAPIProvider(cls.config, cls.fixture_log)

    @classmethod
    def tearDownClass(cls):
        super(RackConnectBaseFixture, cls).tearDownClass()
        cls.fixture_log.debug('Cleaning servers...')
        cls.servers_provider.delete_servers(cls.servers_to_delete)
        [cls.servers_provider.wait_for_server_to_be_deleted_response_code(
            server_id) for server_id in cls.servers_to_delete]


class RackConnectNetworkFixture(RackConnectBaseFixture):
    @classmethod
    def _network(cls, network_id, label):
        return namedtuple('Network', ['id', 'label'])(network_id, label)

    @classmethod
    def setUpClass(cls):
        super(RackConnectNetworkFixture, cls).setUpClass()
        cls.networks_to_delete = []
        cls.nvp_provider = cls._nvp_provider()
        cls.networks_provider = IsolatedNetworksProvider(cls.config,
                                                         cls.fixture_log)

    @classmethod
    def tearDownClass(cls):
        super(RackConnectNetworkFixture, cls).tearDownClass()
        cls._cleanup_networks()

    @classmethod
    def _create_server(cls, networks):
        networks = [{'uuid': network.id} for network in networks]
        response = cls.servers_provider\
            .create_server_no_wait(
                name=cls.config.rackconnect.rackconnect_initials,
                networks=networks)
        server = response.entity
        cls.servers_to_delete.append(server.id)
        return server

    @classmethod
    def _nvp_provider(cls):
        if cls.config.nvp_api.endpoint:
            return NVPProvider(cls.config, cls.fixture_log)
        return None

    @classmethod
    def list_virtual_interface(cls, server_id):
        time_now = time.time()
        timeout = time_now + cls.config.rackconnect.max_wait
        while time.time() < timeout:
            try:
                response = cls.networks_provider.client\
                    .list_virtual_interfaces(server_id)
                if response is None:
                    raise ItemNotFound
                if len(response.entity) > 0:
                    return response.entity
                time.sleep(cls.config.rackconnect.min_polling_interval)
            except TypeError:
                return
        raise ItemNotFound

    @classmethod
    def _create_isolated_network(cls):
        network_label = datagen.random_string(
            cls.config.rackconnect.rackconnect_initials)
        response = cls.networks_provider.client\
            .create_network(cidr='192.168.0.0/24', label=network_label)
        cls.networks_to_delete.append(response.entity)
        return response.entity

    @classmethod
    def _cleanup_networks(cls):
        [cls.networks_provider.client.delete_network(network.id)
         for network in cls.networks_to_delete]

    def _verify_interface(self, private_interface):
        interfaces = self.list_virtual_interface(self.server.id)
        self.assertEquals(2, len(interfaces))
        self.assertEquals(private_interface.ip_addresses[0].network_id,
                          interfaces[1].ip_addresses[0].network_id)

    def _create_virtual_interface(self, network):
        response = self.networks_provider.client\
            .create_virtual_interface(self.server.id, network.id)
        self.assertEquals(response.status_code, 200)
        return response.entity[0]

    def _verify_network(self, interfaces, network, count):
        ip_addresses = self._filter_networks(interfaces, network)
        self.assertEquals(count, len(ip_addresses))

    def _verify_no_network(self, interfaces, network):
        ip_addresses = self._filter_networks(interfaces, network)
        self.assertEquals(0, len(ip_addresses))

    def _filter_networks(self, interfaces, network):
        filtered_interfaces = [self._filter(interface.ip_addresses, network)
                               for interface in interfaces]
        return reduce(lambda x, y: x+y, filtered_interfaces)

    def _filter(self, addresses, network):
        return [address for address in addresses
                if address.network_id == network.id and
                   address.network_label == network.label]