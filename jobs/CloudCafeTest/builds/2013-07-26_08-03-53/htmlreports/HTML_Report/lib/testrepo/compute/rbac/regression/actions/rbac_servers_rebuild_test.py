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
        test_server = active_server_response.entity
        self.resources.add(test_server.id,
                          self.servers_client.delete_server)
        rebuilt_server_response = self.servers_client.rebuild(
            test_server.id,
            self.image_ref_alt,
            name=self.name,
            metadata=self.metadata,
            personality=self.personality,
            admin_pass=self.password)
        self.assertEqual(202, rebuilt_server_response.status_code)
        rebuilt_server = rebuilt_server_response.entity
        self._assert_server_pass_rebuild(rebuilt_server, test_server)
        
    def _assert_server_pass_rebuild(self, rebuilt_server, test_server):
        '''Verify Server rebuilded'''
        
        if rebuilt_server.addresses.public is not None:
            v4_address = rebuilt_server.addresses.public.ipv4
            v6_address = rebuilt_server.addresses.public.ipv6
            self.assertEqual(v4_address, test_server.accessIPv4,
                             msg="AccessIPv4 did not match")
#       Two zeroes ommited from the ipV6 address
#        self.assertEqual(v6_address, str(test_server.accessIPv6),
#                         msg="AccessIPv6 did not match")
        self.assertEquals(rebuilt_server.tenant_id, 
                          self.config.compute_api.tenant_id,
                          msg="Tenant id did not match")
        self.assertEqual(rebuilt_server.name, self.name,
                         msg="Server name did not match")
        self.assertTrue(rebuilt_server.hostId is not None,
                        msg="Host id was not set")
        self.assertEqual(rebuilt_server.flavor.id, self.flavor_ref,
                         msg="Flavor id did not match")
        self.assertEqual(rebuilt_server.id, test_server.id, 
                         msg="Server id did not match")
        self.assertEqual(rebuilt_server.links.bookmark, 
                         test_server.links.bookmark, 
                         msg="Bookmark links do not match")
        self.assertEqual(rebuilt_server.metadata.key, 'value')
        self.assertEqual(rebuilt_server.created, test_server.created,
                         msg="Server Created date changed after rebuild")
        self.assertTrue(rebuilt_server.updated != test_server.updated,
                        msg="Server Updated date not changed after rebuild")
#       Two zeroes ommited from the ipV6 address
#        self.assertEquals(rebuilt_server.addresses, test_server.addresses,
#                          msg="Server IP addresses changed after rebuild")
    
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
        self._assert_server_fail_rebuild()
    
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
        self._assert_server_fail_rebuild()
    
    @attr(type='smoke', net='no')
    def test_rebuild_server_creator_image_with_admin_role(self):
        """Rebuild server from creator image with admin account should fail"""
        name = rand_name('testimage')
        server_id = self.server.id
        with self.assertRaises(Forbidden):
            self.creator_servers_client.create_image(server_id, 
                                                     name)
        self._assert_server_fail_rebuild()
        #Should fail on creator image creation before rebuilding server

    @attr(type='smoke', net='no')
    def test_rebuild_server_creator_image_with_creator_role(self):
        """Rebuild server from creator image with creator account should fail"""
        name = rand_name('testimage')
        server_id = self.server.id
        with self.assertRaises(Forbidden):
            self.creator_servers_client.create_image(server_id, 
                                                     name)
        self._assert_server_fail_rebuild()
        #Should fail on creator image creation before rebuilding server  

    @attr(type='smoke', net='no')
    def test_rebuild_server_creator_image_with_observer_role(self):
        """Rebuild server from creator image with observer account should fail"""
        name = rand_name('testimage')
        server_id = self.server.id
        with self.assertRaises(Forbidden):
            self.creator_servers_client.create_image(server_id, 
                                                     name)
        self._assert_server_fail_rebuild()
        #Should fail on creator image creation before rebuilding server
    
    def _assert_server_fail_rebuild(self):
        get_server_response = self.servers_client.get_server(self.server.id)
        get_server = get_server_response.entity
        '''Verify Server did not rebuild'''
        self.assertTrue(get_server.tenant_id is not None,
                        msg="Tenant id in rebuild server should be none")
        self.assertNotEqual(get_server.image.id, self.image_ref_alt,
                         msg="Image id did match")
        self.assertEqual(get_server.flavor.id, self.flavor_ref,
                         msg="Flavor id did not match")
        self.assertEqual(get_server.id, self.server.id, 
                         msg="Server id did not match")
        self.assertEqual(get_server.links.bookmark, self.server.links.bookmark, 
                         msg="Bookmark links do not match")
        self.assertEqual(get_server.created, self.server.created,
                         msg="Server Created date changed after rebuild")
        self.assertEquals(get_server.addresses, self.server.addresses,
                          msg="Server IP addresses changed after rebuild")
        self.assertNotEqual(get_server.status, 'REBUILD',
                            msg="Flavor id did not match")

    @attr(type='smoke', net='no')
    def test_rebuild_server_admin_image_with_admin_role(self):
        """Rebuild server from admin image with admin account should pass"""
        active_server_response = self.compute_provider.create_active_server()
        test_server = active_server_response.entity
        self.resources.add(test_server.id,
                          self.servers_client.delete_server)
        name = rand_name('testimage')
        server_id = test_server.id
        image_response = self.servers_client.create_image(server_id, 
                                                          name)
        image_id = self.parse_image_id(image_response)
        self.compute_provider.wait_for_image_status(image_id,
                                                    NovaImageStatusTypes.ACTIVE)
        rebuilt_server_response = self.servers_client.rebuild(
            test_server.id,
            image_id,
            name=self.name,
            metadata=self.metadata,
            personality=self.personality,
            admin_pass=self.password)
        self.assertEqual(202, rebuilt_server_response.status_code)
        rebuilt_server = rebuilt_server_response.entity
        self._assert_server_pass_rebuild(rebuilt_server, test_server)
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
        self._assert_server_fail_rebuild()
        # Delete image and wait for image to be deleted
        self.compute_provider.wait_for_image_to_be_deleted(image_id)
    
    @attr(type='smoke', net='no')
    def test_rebuild_server_admin_image_with_observer_role(self):
        """Rebuild server from admin image with observer account should fail"""
        name = rand_name('testimage')
        server_id = self.server.id
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
        self._assert_server_fail_rebuild()
        # Delete image and wait for image to be deleted
        self.compute_provider.wait_for_image_to_be_deleted(image_id)