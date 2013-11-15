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
        servers = server_info_response.entity
        self._assert_server_list(servers)
        self.assertTrue(self.server.min_details() in
            servers, msg="Server id {0} was not found".format(self.server.id))
        
    @attr(type='smoke', net='no')
    def test_list_server_creator_user(self):
        """List server via creator user"""
        server_info_response = self.creator_servers_client.list_servers()
        self.assertEqual(200, server_info_response.status_code)
        servers = server_info_response.entity
        self._assert_server_list(servers)
        self.assertTrue(self.server.min_details() in
            servers, msg="Server id {0} was not found".format(self.server.id))
        
    @attr(type='smoke', net='no')
    def test_list_server_observer_user(self):
        """List server via observer role"""
        server_info_response = self.observer_servers_client.list_servers()
        self.assertEqual(200, server_info_response.status_code)
        servers = server_info_response.entity
        self._assert_server_list(servers)
        self.assertTrue(self.server.min_details() in
            servers, msg="Server id {0} was not found".format(self.server.id))
    
    def _assert_server_list(self, servers):
        self.assertTrue(len(servers) > 0)
        self.assertTrue(servers[0].id is not None,
                        msg="id is present")
        self.assertTrue(servers[0].name is not None,
                        msg="name is present")
        self.assertTrue(servers[0].links is not None,
                        msg="links are present")
    
    @attr(type='smoke', net='no')
    def test_list_server_detail_admin_user(self):
        """List server detail via admin user"""
        server_info_response = self.servers_client.list_servers_with_detail()
        self.assertEqual(200, server_info_response.status_code)
        servers = server_info_response.entity
        self._assert_server_list_detail(servers)
        self.assertTrue(self.server.min_details() in
            servers, msg="Server id {0} was not found".format(self.server.id))
        
    @attr(type='smoke', net='no')
    def test_list_server_detail_creator_user(self):
        """List server detail via creator user"""
        server_info_response = self.creator_servers_client.list_servers_with_detail()
        self.assertEqual(200, server_info_response.status_code)
        servers = server_info_response.entity
        self._assert_server_list_detail(servers)
        self.assertTrue(self.server.min_details() in
            servers, msg="Server id {0} was not found".format(self.server.id))
        
    @attr(type='smoke', net='no')
    def test_list_server_detail_observer_user(self):
        """List server detail via observer role"""
        server_info_response = self.observer_servers_client.list_servers_with_detail()
        self.assertEqual(200, server_info_response.status_code)
        servers = server_info_response.entity
        self._assert_server_list_detail(servers)
        self.assertTrue(self.server.min_details() in
            servers, msg="Server id {0} was not found".format(self.server.id))

    def _assert_server_list_detail(self, servers):
        message = "Expected {0} to be {1}, was {2}."
        self.assertTrue(len(servers) > 0)
        self.assertTrue(servers[0].id is not None,
                        msg="id is present")
        self.assertTrue(servers[0].name is not None,
                        msg="name is present")
        self.assertTrue(servers[0].links is not None,
                        msg="links are present")
        self.assertTrue(servers[0].accessIPv4 is not None,
                        msg="accessIPv4 are present")
        self.assertTrue(servers[0].accessIPv6 is not None,
                        msg="accessIPv6 are present")
        self.assertTrue(servers[0].addresses.public.ipv4 is not None,
                        msg="IPv4 public is present")
        self.assertTrue(servers[0].addresses.public.ipv6 is not None,
                        msg="IPv6 public is present")
        self.assertTrue(servers[0].addresses.private.ipv4 is not None,
                        msg="IPv4 public is present")
        self.assertTrue(servers[0].created is not None,
                        msg="created field present")
        self.assertTrue(servers[0].diskConfig is not None,
                        msg="diskConfig field present")
        self.assertTrue(servers[0].flavor.id is not None,
                        msg="Flavor id field present")
        self.assertTrue(servers[0].hostId is not None,
                        msg="host id field present")
        self.assertTrue(servers[0].image.id is not None,
                        msg="image id field present")
        self.assertTrue(servers[0].metadata is not None,
                        msg="metadata field present")
        self.assertTrue(servers[0].power_state is not None,
                        msg="power_state field present")
        self.assertTrue(servers[0].progress >=0,
                         msg=message.format('server progress', 'should be int',
                                            servers[0].progress))
        self.assertTrue(servers[0].status is not None,
                        msg="status field present")
        self.assertEquals(servers[0].tenant_id,
                          str(self.config.compute_api.tenant_id),
                          msg=message.format('tenant id',
                                str(self.config.compute_api.tenant_id),
                                servers[0].tenant_id))
        self.assertTrue(servers[0].updated is not None,
                        msg="updated field present")
        self.assertTrue(servers[0].user_id is not None,
                        msg="user id field present")
        self.assertTrue(servers[0].vm_state is not None,
                        msg="vm state field present")
        