from testrepo.common.testfixtures.compute import RbacComputeFixture
from ccengine.common.decorators import attr
from ccengine.common.tools.datagen import rand_name
from ccengine.domain.configuration import AuthConfig
from ccengine.common.exceptions.compute import Forbidden
from ccengine.clients.compute.servers_api import ServerAPIClient
from ccengine.domain.types import NovaImageStatusTypes
from ccengine.domain.types import NovaServerStatusTypes
from ccengine.providers.configuration import MasterConfigProvider as _MCP
from ccengine.providers.compute.compute_api import ComputeAPIProvider \
                                                   as _ComputeAPIProvider


class RBACServerPasswordTest(RbacComputeFixture):

    @classmethod
    def setUpClass(cls):
        super(RBACServerPasswordTest, cls).setUpClass()
        # Creation of 1 servers needed for the tests
        active_server_response = cls.compute_provider.create_active_server()
        cls.server = active_server_response.entity
        cls.resources.add(cls.server.id,
                          cls.servers_client.delete_server)

    @classmethod
    def tearDownClass(cls):
        super(RBACServerPasswordTest, cls).tearDownClass()

    @attr(type='smoke', net='no')
    def test_change_admin_password_with_admin_role(self):
        """Change server password with admin account should work"""
        new_password = "newslice129690TuG72Bgj2"
        password_response = self.servers_client.change_password(
            self.server.id, 
            new_password)
        self.assertEqual(202, password_response.status_code)
    
    @attr(type='smoke', net='no')
    def test_change_admin_password_with_creator_role(self):
        """Change server password with creator account should fail"""
        new_password = "newslice129690TuG72Bgj2"
        with self.assertRaises(Forbidden):
            self.creator_servers_client.change_password(
                self.server.id, 
                new_password)
        
    @attr(type='smoke', net='no')
    def test_change_admin_password_with_observer_role(self):
        """Change server password with observer account should fail"""
        new_password = "newslice129690TuG72Bgj2"
        with self.assertRaises(Forbidden):
            self.observer_servers_client.change_password(
                self.server.id, 
                new_password)
