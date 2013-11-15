from testrepo.common.testfixtures.compute import ComputeFixture

from ccengine.common.exceptions.compute import BadRequest, ItemNotFound
from ccengine.common.decorators import attr
from ccengine.domain.configuration import AuthConfig
from ccengine.clients.compute.servers_api import ServerAPIClient
from ccengine.providers.configuration import MasterConfigProvider as _MCP
from ccengine.providers.compute.compute_api import ComputeAPIProvider \
    as _ComputeAPIProvider
import unittest2 as unittest


class AdminAuthorizationTest(ComputeFixture):

    @classmethod
    def setUpClass(cls):
        super(AdminAuthorizationTest, cls).setUpClass()
        cls.server = cls.compute_provider.create_active_server().entity
        cls.resources.add(cls.server.id, cls.servers_client.delete_server)

    @classmethod
    def tearDownClass(cls):
        super(AdminAuthorizationTest, cls).tearDownClass()

    def test_list_servers_all_tenants_ignored_as_user(self):
        # TODO: This test should really create a second server with a different
        # tenant, and very that server is not returned when the first user
        # attempts to make a request for all tenant servers
        user_servers = self.servers_client.list_servers_with_detail().entity
        all_servers = self.servers_client.list_servers_with_detail(all_tenants=1).entity
        self.assertEquals(len(user_servers), len(all_servers))

    def test_lock_server_fails_as_user(self):
        with self.assertRaises(BadRequest):
            self.servers_client.lock_server(self.server.id)

    def test_unlock_server_fails_as_user(self):
        with self.assertRaises(BadRequest):
            self.servers_client.unlock_server(self.server.id)

    def test_migrate_server_fails_as_user(self):
        with self.assertRaises(BadRequest):
            self.servers_client.migrate_server(self.server.id)

    def test_live_migrate_server_fails_as_user(self):
        with self.assertRaises(BadRequest):
            self.servers_client.live_migrate_server(self.server.id)

    def test_stop_server_fails_as_user(self):
        with self.assertRaises(BadRequest):
            self.servers_client.stop_server(self.server.id)

    def test_start_server_fails_as_user(self):
        with self.assertRaises(BadRequest):
            self.servers_client.start_server(self.server.id)

    def test_suspend_server_fails_as_user(self):
        with self.assertRaises(BadRequest):
            self.servers_client.suspend_server(self.server.id)

    def test_resume_server_fails_as_user(self):
        with self.assertRaises(BadRequest):
            self.servers_client.resume_server(self.server.id)

    def test_pause_server_fails_as_user(self):
        with self.assertRaises(BadRequest):
            self.servers_client.pause_server(self.server.id)

    def test_unpause_server_fails_as_user(self):
        with self.assertRaises(BadRequest):
            self.servers_client.unpause_server(self.server.id)

    def test_reset_server_state_fails_as_user(self):
        with self.assertRaises(BadRequest):
            self.servers_client.reset_state(self.server.id)

    def test_get_server_diagnostics_fails_as_user(self):
        with self.assertRaises(ItemNotFound):
            self.servers_client.get_server_diagnostics(self.server.id)

    def test_list_hosts_fails_as_user(self):
        with self.assertRaises(ItemNotFound):
            self.hosts_client.list_hosts()

