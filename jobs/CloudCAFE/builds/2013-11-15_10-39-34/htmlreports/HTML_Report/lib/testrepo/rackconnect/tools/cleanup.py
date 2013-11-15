from ccengine.providers.compute.compute_api import ComputeAPIProvider
from ccengine.providers.networks.isolated_networks import \
    IsolatedNetworksProvider
from ccengine.common.constants.networks_constants import Constants
from testrepo.common.testfixtures.fixtures import BaseTestFixture


class Cleanup(BaseTestFixture):
    @classmethod
    def setUpClass(cls):
        super(Cleanup, cls).setUpClass()
        cls.servers_provider = ComputeAPIProvider(cls.config, cls.fixture_log)
        cls.networks_provider = IsolatedNetworksProvider(cls.config,
                                                         cls.fixture_log)

    def test_cleanup(self):
        self._cleanup_orphaned_servers()
        self._cleanup_orphaned_networks()

    def _cleanup_orphaned_servers(self):
        self.fixture_log.info("Cleaning up servers.")
        servers = self._find_orphaned_servers()
        if not servers:
            self.fixture_log.info("No servers to clean.")
            return
        self._delete_servers(servers)
        self._wait_for_server_deletion(servers)

    def _find_orphaned_servers(self):
        return self.servers_provider.servers_client\
            .list_servers(self.config.rackconnect.rackconnect_initials).entity

    def _delete_servers(self, servers):
        server_ids = [server.id for server in servers]
        self.fixture_log.info("Cleaning up the following servers.")
        self.fixture_log.info(server_ids)
        self.servers_provider.delete_servers(server_ids)

    def _wait_for_server_deletion(self, servers):
        for server in servers:
            self.servers_provider.wait_for_server_to_be_deleted_response_code(
                server.id)

    def _cleanup_orphaned_networks(self):
        self.fixture_log.info("Cleaning up networks.")
        all_networks = self.networks_provider.client.list_networks().entity
        isolated_networks = self._filter_networks(all_networks)
        if not isolated_networks:
            self.fixture_log.info("No networks to clean.")
            return
        self.fixture_log.info("Cleaning up the following networks.")
        self.fixture_log.info(isolated_networks)
        for network in isolated_networks:
            self.networks_provider.client.delete_network(network.id)

    def _filter_networks(self, networks):
        return [network for network in networks
                if network.id not in (Constants.PUBLIC_NETWORK_ID,
                                      Constants.PRIVATE_NETWORK_ID)]