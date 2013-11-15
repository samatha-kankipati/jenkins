from testrepo.common.testfixtures.compute import RbacComputeFixture
from ccengine.common.decorators import attr
from ccengine.common.tools.datagen import rand_name
from ccengine.domain.configuration import AuthConfig
from ccengine.clients.compute.servers_api import ServerAPIClient
from ccengine.domain.types import NovaImageStatusTypes
from ccengine.common.exceptions.compute import Forbidden
from ccengine.providers.configuration import MasterConfigProvider as _MCP
from ccengine.providers.compute.compute_api import ComputeAPIProvider \
                                                   as _ComputeAPIProvider


class RBACFlavorTest(RbacComputeFixture):

    @classmethod
    def setUpClass(cls):
        super(RBACFlavorTest, cls).setUpClass()
        # Creation of 1 servers needed for the tests
        active_server_response = cls.compute_provider.create_active_server()
        cls.server = active_server_response.entity
        cls.resources.add(cls.server.id,
                          cls.servers_client.delete_server)

    @classmethod
    def tearDownClass(cls):
        super(RBACFlavorTest, cls).tearDownClass()

    @attr(type='smoke', net='no')
    def test_flavor_list_with_admin_role(self):
        """List flavors with admin account should work"""
        flavor_response = self.flavors_client.list_flavors()
        self.assertEqual(200, flavor_response.status_code)
    
    @attr(type='smoke', net='no')
    def test_flavor_list_with_creator_role(self):
        """List flavors with creator account should work"""
        flavor_response = self.creator_flavors_client.list_flavors()
        self.assertEqual(200, flavor_response.status_code)
    
    @attr(type='smoke', net='no')
    def test_flavor_list_with_observer_role(self):
        """List flavors with observer account should work"""
        flavor_response = self.observer_flavors_client.list_flavors()
        self.assertEqual(200, flavor_response.status_code)
    
    @attr(type='smoke', net='no')
    def test_flavor_list_detail_with_admin_role(self):
        """List flavors with admin account should work"""
        flavor_response = self.flavors_client.list_flavors_with_detail()
        self.assertEqual(200, flavor_response.status_code)
    
    @attr(type='smoke', net='no')
    def test_flavor_list_detail_with_creator_role(self):
        """List flavors with creator account should work"""
        flavor_response = self.creator_flavors_client.list_flavors_with_detail()
        self.assertEqual(200, flavor_response.status_code)
    
    @attr(type='smoke', net='no')
    def test_flavor_list_detail_with_observer_role(self):
        """List flavors with observer account should work"""
        flavor_response = self.observer_flavors_client.list_flavors_with_detail()
        self.assertEqual(200, flavor_response.status_code)
    
    @attr(type='smoke', net='no')
    def test_flavor_get_detail_with_admin_role(self):
        """Get flavors with admin account should work"""
        flavor_response = self.flavors_client.get_flavor_details(
            self.flavor_ref)
        self.assertEqual(200, flavor_response.status_code)
    
    @attr(type='smoke', net='no')
    def test_flavor_get_detail_with_creator_role(self):
        """Get flavors with creator account should work"""
        flavor_response = self.creator_flavors_client.get_flavor_details(
            self.flavor_ref)
        self.assertEqual(200, flavor_response.status_code)
    
    @attr(type='smoke', net='no')
    def test_flavor_get_detail_with_observer_role(self):
        """Get flavors with observer account should work"""
        flavor_response = self.observer_flavors_client.get_flavor_details(
            self.flavor_ref)
        self.assertEqual(200, flavor_response.status_code)
