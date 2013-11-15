from testrepo.common.testfixtures.compute import RbacComputeFixture
from ccengine.common.decorators import attr
from ccengine.domain.configuration import AuthConfig
from ccengine.clients.compute.servers_api import ServerAPIClient
from ccengine.providers.configuration import MasterConfigProvider as _MCP
from ccengine.providers.compute.compute_api import ComputeAPIProvider \
                                                   as _ComputeAPIProvider


class RBACServerTest(RbacComputeFixture):

    @classmethod
    def setUpClass(cls):
        super(RBACServerTest, cls).setUpClass()
        # Creation of 1 servers needed for the tests
        active_server_response = cls.compute_provider.create_active_server()
        cls.server = active_server_response.entity
        cls.resources.add(cls.server.id,
                          cls.servers_client.delete_server)

    @classmethod
    def tearDownClass(cls):
        super(RBACServerTest, cls).tearDownClass()

    @attr(type='smoke', net='no')
    def test_list_server_admin_user(self):
        """List server via admin user"""
        server_info_response = self.servers_client.list_servers()
        self.assertEqual(200, server_info_response.status_code)
        
    @attr(type='smoke', net='no')
    def test_list_server_creator_user(self):
        """List server via creator user"""
        server_info_response = self.creator_servers_client.list_servers()
        self.assertEqual(200, server_info_response.status_code)
        
    @attr(type='smoke', net='no')
    def test_list_server_observer_user(self):
        """List server via observer role"""
        server_info_response = self.observer_servers_client.list_servers()
        self.assertEqual(200, server_info_response.status_code)
    
    @attr(type='smoke', net='no')
    def test_list_server_detail_admin_user(self):
        """List server detail via admin user"""
        server_info_response = self.servers_client.list_servers_with_detail()
        self.assertEqual(200, server_info_response.status_code)
        
    @attr(type='smoke', net='no')
    def test_list_server_detail_creator_user(self):
        """List server detail via creator user"""
        server_info_response = self.creator_servers_client.list_servers_with_detail()
        self.assertEqual(200, server_info_response.status_code)
        
    @attr(type='smoke', net='no')
    def test_list_server_detail_observer_user(self):
        """List server detail via observer role"""
        server_info_response = self.observer_servers_client.list_servers_with_detail()
        self.assertEqual(200, server_info_response.status_code)
