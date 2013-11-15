import base64
from testrepo.common.testfixtures.compute import RbacComputeFixture
from ccengine.common.decorators import attr
from ccengine.common.exceptions.compute import Forbidden
from ccengine.common.tools.datagen import rand_name
from ccengine.domain.configuration import AuthConfig
from ccengine.clients.compute.servers_api import ServerAPIClient
from ccengine.domain.types import NovaImageStatusTypes
from ccengine.domain.types import NovaServerStatusTypes
from ccengine.providers.configuration import MasterConfigProvider as _MCP
from ccengine.providers.compute.compute_api import ComputeAPIProvider \
                                                   as _ComputeAPIProvider


class RBACServerResizeTest(RbacComputeFixture):

    @classmethod
    def setUpClass(cls):
        super(RBACServerResizeTest, cls).setUpClass()
        # Creation of 1 servers needed for the tests
        cls.server_response = cls.compute_provider.create_active_server()
        cls.server_to_resize = cls.server_response.entity
        cls.resources.add(cls.server_to_resize.id, cls.servers_client.delete_server)

    @classmethod
    def tearDownClass(cls):
        super(RBACServerResizeTest, cls).tearDownClass()

    @attr(type='smoke', net='no')
    def test_resize_server_with_observer_role(self):
        """Resize server with observer account should fail"""
        with self.assertRaises(Forbidden):
            self.observer_servers_client.resize(
                self.server_to_resize.id, 
                self.flavor_ref_alt)
    
    @attr(type='smoke', net='no')
    def test_resize_server_with_creator_role(self):
        """Resize server with admin account should fail"""
        with self.assertRaises(Forbidden):
            self.creator_servers_client.resize(
                self.server_to_resize.id, 
                self.flavor_ref_alt)
        
    @attr(type='smoke', net='no')
    def test_resize_server_with_admin_role(self):
        """Resize server with admin account should pass"""
        active_server_response = self.compute_provider.create_active_server()
        server_personal = active_server_response.entity
        self.resources.add(server_personal.id,
            self.servers_client.delete_server)
        resize_server_response = self.servers_client.resize(
            server_personal.id, 
            self.flavor_ref_alt)
        self.assertEqual(202, resize_server_response.status_code)
    
    @attr(type='smoke', net='no')
    def test_resize_server_confirm_with_observer_role(self):
        """Resize server with observer account should fail"""
        active_server_response = self.compute_provider.create_active_server()
        server_personal = active_server_response.entity
        self.resources.add(server_personal.id,
            self.servers_client.delete_server)
        resize_server_response = self.servers_client.resize(
            server_personal.id, 
            self.flavor_ref_alt)
        self.assertEqual(202, resize_server_response.status_code)
        self.compute_provider.wait_for_server_status(
            server_personal.id,
            NovaServerStatusTypes.VERIFY_RESIZE)
        with self.assertRaises(Forbidden):
            self.observer_servers_client.confirm_resize(
                server_personal.id)
    
    @attr(type='smoke', net='no')
    def test_resize_server_confirm_with_creator_role(self):
        """Resize server confirm with admin account should fail"""
        active_server_response = self.compute_provider.create_active_server()
        server_personal = active_server_response.entity
        self.resources.add(server_personal.id,
            self.servers_client.delete_server)
        resize_server_response = self.servers_client.resize(
            server_personal.id, 
            self.flavor_ref_alt)
        self.assertEqual(202, resize_server_response.status_code)
        self.compute_provider.wait_for_server_status(
            server_personal.id,
            NovaServerStatusTypes.VERIFY_RESIZE)
        with self.assertRaises(Forbidden):      
            self.creator_servers_client.confirm_resize(
                server_personal.id)
    
    @attr(type='smoke', net='no')
    def test_resize_server_confirm_with_admin_role(self):
        """Resize server confirm with admin account should work"""
        active_server_response = self.compute_provider.create_active_server()
        server_personal = active_server_response.entity
        self.resources.add(server_personal.id,
            self.servers_client.delete_server)
        resize_server_response = self.servers_client.resize(
            server_personal.id, 
            self.flavor_ref_alt)
        self.assertEqual(202, resize_server_response.status_code)
        self.compute_provider.wait_for_server_status(
            server_personal.id,
            NovaServerStatusTypes.VERIFY_RESIZE)
        confirm_resize_response = self.servers_client.confirm_resize(
            server_personal.id)
        self.assertEqual(204, confirm_resize_response.status_code)
        
    @attr(type='smoke', net='no')
    def test_resize_server_revert_with_admin_role(self):
        """Resize server revert with admin account should work"""
        active_server_response = self.compute_provider.create_active_server()
        server_personal = active_server_response.entity
        self.resources.add(server_personal.id,
            self.servers_client.delete_server)
        resize_server_response = self.servers_client.resize(
            server_personal.id, 
            self.flavor_ref_alt)
        self.assertEqual(202, resize_server_response.status_code)
        resize_server_response = self.compute_provider.wait_for_server_status(
            server_personal.id,
            NovaServerStatusTypes.VERIFY_RESIZE)
        revert_resize_response = self.servers_client.revert_resize(
            server_personal.id)
        self.assertEqual(202, revert_resize_response.status_code)
    
    @attr(type='smoke', net='no')
    def test_resize_server_revert_with_creator_role(self):
        """Resize server revert with creator account should fail"""
        active_server_response = self.compute_provider.create_active_server()
        server_personal = active_server_response.entity
        self.resources.add(server_personal.id,
            self.servers_client.delete_server)
        resize_server_response = self.servers_client.resize(
            server_personal.id, 
            self.flavor_ref_alt)
        self.assertEqual(202, resize_server_response.status_code)
        resize_server_response = self.compute_provider.wait_for_server_status(
            server_personal.id,
            NovaServerStatusTypes.VERIFY_RESIZE)
        with self.assertRaises(Forbidden):  
            self.creator_servers_client.revert_resize(
                server_personal.id)
        
    @attr(type='smoke', net='no')
    def test_resize_server_revert_with_observer_role(self):
        """Resize server revert with creator account should fail"""
        active_server_response = self.compute_provider.create_active_server()
        server_personal = active_server_response.entity
        self.resources.add(server_personal.id,
            self.servers_client.delete_server)
        resize_server_response = self.servers_client.resize(
            server_personal.id, 
            self.flavor_ref_alt)
        self.assertEqual(202, resize_server_response.status_code)
        resize_server_response = self.compute_provider.wait_for_server_status(
            server_personal.id,
            NovaServerStatusTypes.VERIFY_RESIZE)
        with self.assertRaises(Forbidden):
            self.observer_servers_client.revert_resize(
                server_personal.id)
