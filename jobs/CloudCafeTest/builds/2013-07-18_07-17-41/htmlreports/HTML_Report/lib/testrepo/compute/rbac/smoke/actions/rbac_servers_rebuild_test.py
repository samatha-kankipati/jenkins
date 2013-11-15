import base64
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


class RBACServerRebuildTest(RbacComputeFixture):

    @classmethod
    def setUpClass(cls):
        super(RBACServerRebuildTest, cls).setUpClass()
        # Creation of 1 servers needed for the tests
        active_server_response = cls.compute_provider.create_active_server()
        cls.server = active_server_response.entity
        cls.resources.add(cls.server.id,
                          cls.servers_client.delete_server)
        cls.metadata = {'key': 'value'}
        cls.name = rand_name('testserver')
        file_contents = 'Test server rebuild.'
        cls.personality = [{'path': '/etc/rebuild.txt',
                       'contents': base64.b64encode(file_contents)}]
        cls.password = 'rebuild'

    @classmethod
    def tearDownClass(cls):
        super(RBACServerRebuildTest, cls).tearDownClass()

    @attr(type='smoke', net='no')
    def test_rebuild_server_base_image_with_admin_role(self):
        """Rebuild server from base image with admin account should work"""
        active_server_response = self.compute_provider.create_active_server()
        server_personal = active_server_response.entity
        self.resources.add(server_personal.id,
                          self.servers_client.delete_server)
        rebuilt_server_response = self.servers_client.rebuild(
            self.server.id,
            self.image_ref_alt,
            name=self.name,
            metadata=self.metadata,
            personality=self.personality,
            admin_pass=self.password)
        self.assertEqual(202, rebuilt_server_response.status_code)
        
    @attr(type='smoke', net='no')
    def test_rebuild_server_base_image_with_creator_role(self):
        """Rebuild server from base image with creator account should fail"""
        with self.assertRaises(Forbidden):
            self.creator_servers_client.rebuild(
                self.server.id,
                self.image_ref_alt,
                name=self.name,
                metadata=self.metadata,
                personality=self.personality,
                admin_pass=self.password)
    
    @attr(type='smoke', net='no')
    def test_rebuild_server_base_image_with_observer_role(self):
        """Rebuild server from base image with observer account should fail"""
        with self.assertRaises(Forbidden):
            self.observer_servers_client.rebuild(
                self.server.id,
                self.image_ref_alt,
                name=self.name,
                metadata=self.metadata,
                personality=self.personality,
                admin_pass=self.password)
    
    @attr(type='smoke', net='no')
    def test_rebuild_server_creator_image_with_admin_role(self):
        """Rebuild server from creator image with admin account should fail"""
        name = rand_name('testimage')
        server_id = self.server.id
        with self.assertRaises(Forbidden):
            self.creator_servers_client.create_image(server_id, 
                                                     name)
        #Should fail on creator image creation before rebuilding server

    @attr(type='smoke', net='no')
    def test_rebuild_server_creator_image_with_creator_role(self):
        """Rebuild server from creator image with creator account should fail"""
        name = rand_name('testimage')
        server_id = self.server.id
        with self.assertRaises(Forbidden):
            self.creator_servers_client.create_image(server_id, 
                                                     name)
        #Should fail on creator image creation before rebuilding server  

    @attr(type='smoke', net='no')
    def test_rebuild_server_creator_image_with_observer_role(self):
        """Rebuild server from creator image with observer account should fail"""
        name = rand_name('testimage')
        server_id = self.server.id
        with self.assertRaises(Forbidden):
            self.creator_servers_client.create_image(server_id, 
                                                     name)
        #Should fail on creator image creation before rebuilding server

    @attr(type='smoke', net='no')
    def test_rebuild_server_admin_image_with_admin_role(self):
        """Rebuild server from admin image with admin account should pass"""
        active_server_response = self.compute_provider.create_active_server()
        server_personal = active_server_response.entity
        self.resources.add(server_personal.id,
                          self.servers_client.delete_server)
        name = rand_name('testimage')
        server_id = server_personal.id
        image_response = self.servers_client.create_image(server_id, 
                                                          name)
        image_id = self.parse_image_id(image_response)
        self.compute_provider.wait_for_image_status(image_id,
                                                    NovaImageStatusTypes.ACTIVE)
        rebuilt_server_response = self.servers_client.rebuild(
            server_personal.id,
            image_id,
            name=self.name,
            metadata=self.metadata,
            personality=self.personality,
            admin_pass=self.password)
        self.assertEqual(202, rebuilt_server_response.status_code)
        # Delete image and wait for image to be deleted
        self.compute_provider.wait_for_image_to_be_deleted(image_id)
    
    @attr(type='smoke', net='no')
    def test_rebuild_server_admin_image_with_creator_role(self):
        """Rebuild server from admin image with creator account should fail"""
        name = rand_name('testimage')
        server_id = self.server.id
        image_response = self.servers_client.create_image(server_id, 
                                                          name)
        image_id = self.parse_image_id(image_response)
        self.compute_provider.wait_for_image_status(image_id,
                                                    NovaImageStatusTypes.ACTIVE)
        with self.assertRaises(Forbidden):
            self.creator_servers_client.rebuild(
                self.server.id,
                image_id,
                name=self.name,
                metadata=self.metadata,
                personality=self.personality,
                admin_pass=self.password)
        # Delete image and wait for image to be deleted
        self.compute_provider.wait_for_image_to_be_deleted(image_id)
    
    @attr(type='smoke', net='no')
    def test_rebuild_server_admin_image_with_observer_role(self):
        """Rebuild server from admin image with observer account should fail"""
        active_server_response = self.compute_provider.create_active_server()
        server_personal = active_server_response.entity
        self.resources.add(server_personal.id,
                          self.servers_client.delete_server)
        name = rand_name('testimage')
        server_id = server_personal.id
        image_response = self.servers_client.create_image(server_id, 
                                                          name)
        image_id = self.parse_image_id(image_response)
        self.compute_provider.wait_for_image_status(image_id,
                                                    NovaImageStatusTypes.ACTIVE)
        with self.assertRaises(Forbidden):
            self.observer_servers_client.rebuild(
                self.server.id,
                image_id,
                name=self.name,
                metadata=self.metadata,
                personality=self.personality,
                admin_pass=self.password)
        # Delete image and wait for image to be deleted
        self.compute_provider.wait_for_image_to_be_deleted(image_id)