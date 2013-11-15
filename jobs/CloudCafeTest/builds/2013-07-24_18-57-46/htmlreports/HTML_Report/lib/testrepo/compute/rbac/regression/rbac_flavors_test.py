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
        flavors_response = self.flavors_client.list_flavors()
        self.assertEqual(200, flavors_response.status_code)
        flavors = flavors_response.entity
        self._assert_flavor_list(flavors)
        self._assert_flavor_list_is_not_dummy(flavors)
    
    def _assert_flavor_list(self, flavors):
        self.assertTrue(len(flavors) > 0)
        self.assertTrue(flavors[0].id is not None,
                        msg="id is present")
        self.assertTrue(flavors[0].name is not None,
                        msg="name is present")
        self.assertTrue(flavors[0].links is not None,
                        msg="links are present")
    
    def _assert_flavor_list_is_not_dummy(self, flavors):
        response = self.flavors_client.get_flavor_details(self.flavor_ref)
        flavor = response.entity
        for each in flavors:
            if flavor.id == each.id:
                return
        self.fail("The exp. flavor {0} not found in the fl. list.".format(flavor.id))
        
    
    @attr(type='smoke', net='no')
    def test_flavor_list_with_creator_role(self):
        """List flavors with creator account should work"""
        flavors_response = self.creator_flavors_client.list_flavors()
        self.assertEqual(200, flavors_response.status_code)
        flavors = flavors_response.entity
        self._assert_flavor_list(flavors)
        self._assert_flavor_list_is_not_dummy(flavors)
    
    @attr(type='smoke', net='no')
    def test_flavor_list_with_observer_role(self):
        """List flavors with observer account should work"""
        flavors_response = self.observer_flavors_client.list_flavors()
        self.assertEqual(200, flavors_response.status_code)
        flavors = flavors_response.entity
        self._assert_flavor_list(flavors)
        self._assert_flavor_list_is_not_dummy(flavors)
    
    @attr(type='smoke', net='no')
    def test_flavor_list_detail_with_admin_role(self):
        """List flavors with admin account should work"""
        flavors_detail_response = self.flavors_client.list_flavors_with_detail()
        self.assertEqual(200, flavors_detail_response.status_code)
        flavors = flavors_detail_response.entity
        self._assert_flavor_detail(flavor_list=flavors)
        self._assert_flavor_list_is_not_dummy(flavors)
    
    @attr(type='smoke', net='no')
    def test_flavor_list_detail_with_creator_role(self):
        """List flavors with creator account should work"""
        flavors_detail_response = self.creator_flavors_client.list_flavors_with_detail()
        self.assertEqual(200, flavors_detail_response.status_code)
        flavors = flavors_detail_response.entity
        self._assert_flavor_detail(flavor_list=flavors)
        self._assert_flavor_list_is_not_dummy(flavors)
    
    @attr(type='smoke', net='no')
    def test_flavor_list_detail_with_observer_role(self):
        """List flavors with observer account should work"""
        flavors_detail_response = self.observer_flavors_client.list_flavors_with_detail()
        self.assertEqual(200, flavors_detail_response.status_code)
        flavors = flavors_detail_response.entity
        self._assert_flavor_detail(flavor_list=flavors)
        self._assert_flavor_list_is_not_dummy(flavors)
    
    @attr(type='smoke', net='no')
    def test_flavor_get_detail_with_admin_role(self):
        """Get flavors with admin account should work"""
        flavor_detail_response = self.flavors_client.get_flavor_details(
            self.flavor_ref)
        self.assertEqual(200, flavor_detail_response.status_code)
        flavor = flavor_detail_response.entity
        self._assert_flavor_detail(flavor=flavor)
    
    def _assert_flavor_detail(self, flavor_list=None, flavor=None):
        if flavor_list is not None:
            self.assertTrue(len(flavor_list) > 0)
            flavor = flavor_list[0]
        self.assertTrue(flavor.id is not None,
                        msg="id is present")
        self.assertTrue(flavor.name is not None,
                        msg="name is present")
        self.assertTrue(flavor.links is not None,
                        msg="links are present")
        self.assertTrue(flavor.disk is not None,
                        msg="disk parameter is present")
        self.assertTrue(flavor.ram is not None,
                        msg="ram parameter is present")
        self.assertTrue(flavor.rxtx_factor is not None,
                        msg="rxtx_factor parameter is present")
        self.assertTrue(flavor.swap is not None,
                        msg="swap parameter is present")
        self.assertTrue(flavor.vcpus is not None,
                        msg="vcpus parameter is present")
    
    @attr(type='smoke', net='no')
    def test_flavor_get_detail_with_creator_role(self):
        """Get flavors with creator account should work"""
        flavor_detail_response = self.creator_flavors_client.get_flavor_details(
            self.flavor_ref)
        self.assertEqual(200, flavor_detail_response.status_code)
        flavor = flavor_detail_response.entity
        self._assert_flavor_detail(flavor=flavor)
    
    @attr(type='smoke', net='no')
    def test_flavor_get_detail_with_observer_role(self):
        """Get flavors with observer account should work"""
        flavor_detail_response = self.observer_flavors_client.get_flavor_details(
            self.flavor_ref)
        self.assertEqual(200, flavor_detail_response.status_code)
        flavor = flavor_detail_response.entity
        self._assert_flavor_detail(flavor=flavor)
