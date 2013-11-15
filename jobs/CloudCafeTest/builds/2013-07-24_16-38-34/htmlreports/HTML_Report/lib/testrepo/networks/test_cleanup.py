from testrepo.common.testfixtures.networks import NetworksTestFixture, \
                                         NetworksManagedRackConnectUsersFixture
from ccengine.common.decorators import attr
import time


class TestCleanup(NetworksTestFixture):

    @attr('cleanup')
    def test_standard_cleanup(self):
        self._cleanup_servers()
        time.sleep(30)
        self._cleanup_images()
        self._cleanup_networks()

    def _cleanup_servers(self):
        servers = self.servers_provider.servers_client.list_servers().entity
        for server in servers:
            r = self.servers_provider.servers_client.delete_server(server.id)
            if not r.ok:
                print r.content
            time.sleep(1)

    def _cleanup_networks(self):
        networks = self.networks_provider.client.list_networks().entity
        for network in networks:
            if network.label != 'public' and network.label != 'private':
                r = self.networks_provider.client.delete_network(network.id)
                if not r.ok:
                    print r.content

    def _cleanup_images(self):
        all_images = self.servers_provider.images_client.list_images().entity
        for ai in all_images:
            if ai.name.find('test_') != -1:
                self.servers_provider.images_client.delete_image(ai.id)


class TestCleanupManagedRackConnect(NetworksManagedRackConnectUsersFixture):

    @attr('cleanup_managed')
    def test_managed_rackconnect_cleanup(self):
        self._cleanup_servers()
        time.sleep(30)
        self._cleanup_networks()

    def _cleanup_servers(self):
        man_servers = self.managed_servers_provider.servers_client.list_servers().entity
        rc_servers = self.rackconnect_servers_provider.servers_client.list_servers().entity
        for server in man_servers:
            r = self.managed_servers_provider.servers_client.delete_server(server.id)
            if not r.ok:
                print r.content
            time.sleep(1)
        for server in rc_servers:
            r = self.rackconnect_servers_provider.servers_client.delete_server(server.id)
            if not r.ok:
                print r.content
            time.sleep(1)

    def _cleanup_networks(self):
        man_networks = self.managed_networks_provider.client.list_networks().entity
        rc_networks = self.rackconnect_networks_provider.client.list_networks().entity
        for network in man_networks:
            if network.label != 'public' and network.label != 'private':
                r = self.managed_networks_provider.client.delete_network(network.id)
                if not r.ok:
                    print r.content
        for network in rc_networks:
            if network.label != 'public' and network.label != 'private':
                r = self.rackconnect_networks_provider.client.delete_network(network.id)
                if not r.ok:
                    print r.content
