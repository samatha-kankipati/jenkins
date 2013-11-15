from testrepo.common.testfixtures.compute import RbacComputeFixture
from ccengine.common.decorators import attr
from ccengine.common.tools.datagen import rand_name
from ccengine.domain.configuration import AuthConfig
from ccengine.common.exceptions.compute import Forbidden
from ccengine.domain.types import NovaServerStatusTypes, NovaServerRebootTypes
from ccengine.clients.compute.servers_api import ServerAPIClient
from ccengine.domain.types import NovaImageStatusTypes
from ccengine.domain.types import NovaServerStatusTypes
from ccengine.providers.configuration import MasterConfigProvider as _MCP
from ccengine.providers.compute.compute_api import ComputeAPIProvider \
                                                   as _ComputeAPIProvider


class RBACServerRescueTest(RbacComputeFixture):

    @classmethod
    def setUpClass(cls):
        super(RBACServerRescueTest, cls).setUpClass()
        # Creation of 1 servers needed for the tests
        active_server_response = cls.compute_provider.create_active_server()
        cls.server = active_server_response.entity
        cls.resources.add(cls.server.id,
                          cls.servers_client.delete_server)

    @classmethod
    def tearDownClass(cls):
        super(RBACServerRescueTest, cls).tearDownClass()

    @attr(type='smoke', net='no')
    def test_rescue_server_with_admin_role(self):
        """Rescue server with admin account should work"""
        active_server_response = self.compute_provider.create_active_server()
        server_personal = active_server_response.entity
        self.resources.add(server_personal.id,
                          self.servers_client.delete_server)
        rescue_response = self.servers_client.rescue(server_personal.id)
        self.assertEqual(200, rescue_response.status_code)
    
    @attr(type='smoke', net='no')
    def test_rescue_server_with_creator_role(self):
        """Rescue server with creator account should fail"""
        with self.assertRaises(Forbidden):
            self.creator_servers_client.rescue(self.server.id)
    
    @attr(type='smoke', net='no')
    def test_rescue_server_with_observer_role(self):
        """Rescue server with observer account should fail"""
        with self.assertRaises(Forbidden):
            self.observer_servers_client.rescue(self.server.id)
    
    @attr(type='smoke', net='no')
    def test_unrescue_server_with_admin_role(self):
        """Unrescue server with admin account should work"""
        active_server_response = self.compute_provider.create_active_server()
        server_personal = active_server_response.entity
        self.resources.add(server_personal.id,
            self.servers_client.delete_server)
        rescue_response = self.servers_client.rescue(server_personal.id)
        self.assertEqual(200, rescue_response.status_code)
        rescue_server_response = self.compute_provider.wait_for_server_status(
            server_personal.id, 'RESCUE')
        unrescue_response = self.servers_client.unrescue(server_personal.id)
        self.assertEqual(202, unrescue_response.status_code)
    
    @attr(type='smoke', net='no')
    def test_unrescue_server_with_creator_role(self):
        """Unrescue server with creator account should fail"""
        active_server_response = self.compute_provider.create_active_server()
        server_personal = active_server_response.entity
        self.resources.add(server_personal.id,
            self.servers_client.delete_server)
        rescue_response = self.servers_client.rescue(server_personal.id)
        self.assertEqual(200, rescue_response.status_code)
        rescue_server_response = self.compute_provider.wait_for_server_status(
            server_personal.id, 'RESCUE')
        with self.assertRaises(Forbidden):
            self.creator_servers_client.unrescue(self.server.id)
    
    @attr(type='smoke', net='no')
    def test_unrescue_server_with_observer_role(self):
        """Unrescue server with observer account should fail"""
        active_server_response = self.compute_provider.create_active_server()
        server_personal = active_server_response.entity
        self.resources.add(server_personal.id,
            self.servers_client.delete_server)
        rescue_response = self.servers_client.rescue(server_personal.id)
        self.assertEqual(200, rescue_response.status_code)
        rescue_server_response = self.compute_provider.wait_for_server_status(
            server_personal.id, 'RESCUE')
        with self.assertRaises(Forbidden):
            self.observer_servers_client.unrescue(self.server.id)
