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


class RBACMetadataTest(RbacComputeFixture):

    @classmethod
    def setUpClass(cls):
        super(RBACMetadataTest, cls).setUpClass()
        # Creation of 1 servers needed for the tests
        active_server_response = cls.compute_provider.create_active_server()
        cls.server = active_server_response.entity
        cls.resources.add(cls.server.id,
                          cls.servers_client.delete_server)

    @classmethod
    def tearDownClass(cls):
        super(RBACMetadataTest, cls).tearDownClass()
    
    def setUp(self):
        self.meta = {'meta_key_1': 'meta_value_1', 'meta_key_2': 'meta_value_2'}
        self.servers_client.set_server_metadata(self.server.id, self.meta)

    @attr(type='smoke', net='no')
    def test_server_metadata_list_with_admin_role(self):
        """List server metadata with admin account should work"""
        message = "Expected {0} to be {1}, was {2}."
        server_response = self.servers_client.list_server_metadata(
            self.server.id)
        self.assertEqual(200, server_response.status_code)
        metadata = server_response.entity
        self.assertEqual('meta_value_1', metadata.meta_key_1,
            msg=message.format('Metadata Item not found on server:', 
                               self.server.id, 'Expected Item Key : ', 
                               'metadata.meta_key_1 with Value : ',
                               'metadata.meta_value_1, but received ',
                               metadata.meta_key_1))
        self.assertEqual('meta_value_2', metadata.meta_key_2,
            msg=message.format('Metadata Item not found on server:', 
                               self.server.id, 'Expected Item Key : ', 
                               'metadata.meta_key_2 with Value : ',
                               'metadata.meta_value_2, but received ',
                               metadata.meta_key_2))

    @attr(type='smoke', net='no')
    def test_server_metadata_list_with_creator_role(self):
        """List server metadata with creator account should work"""
        message = "Expected {0} to be {1}, was {2}."
        server_response = self.creator_servers_client.list_server_metadata(
            self.server.id)
        self.assertEqual(200, server_response.status_code)
        metadata = server_response.entity
        self.assertEqual('meta_value_1', metadata.meta_key_1,
            msg=message.format('Metadata Item not found on server:', 
                               self.server.id, 'Expected Item Key : ', 
                               'metadata.meta_key_1 with Value : ',
                               'metadata.meta_value_1, but received ',
                               metadata.meta_key_1))
        self.assertEqual('meta_value_2', metadata.meta_key_2,
            msg=message.format('Metadata Item not found on server:', 
                               self.server.id, 'Expected Item Key : ', 
                               'metadata.meta_key_2 with Value : ',
                               'metadata.meta_value_2, but received ',
                               metadata.meta_key_2))
    
    @attr(type='smoke', net='no')
    def test_server_metadata_list_with_observer_role(self):
        """List server metadata with observer account should work"""
        message = "Expected {0} to be {1}, was {2}."
        server_response = self.observer_servers_client.list_server_metadata(
            self.server.id)
        self.assertEqual(200, server_response.status_code)
        metadata = server_response.entity
        self.assertEqual('meta_value_1', metadata.meta_key_1,
            msg=message.format('Metadata Item not found on server:', 
                               self.server.id, 'Expected Item Key : ', 
                               'metadata.meta_key_1 with Value : ',
                               'metadata.meta_value_1, but received ',
                               metadata.meta_key_1))
        self.assertEqual('meta_value_2', metadata.meta_key_2,
            msg=message.format('Metadata Item not found on server:', 
                               self.server.id, 'Expected Item Key : ', 
                               'metadata.meta_key_2 with Value : ',
                               'metadata.meta_value_2, but received ',
                               metadata.meta_key_2))
    
    @attr(type='smoke', net='no')
    def test_server_metadata_update_with_admin_role(self):
        """Update server metadata with admin account should work"""
        meta = {'key1': 'alt1', 'key2': 'alt2', 'meta_key_1': 'alt3'}
        server_response = self.servers_client.update_server_metadata(
            self.server.id, meta)
        self.assertEqual(200, server_response.status_code)
        metadata = server_response.entity
        self._assert_update_positive_metadata(metadata)
    
    @attr(type='smoke', net='no')
    def test_server_metadata_update_with_creator_role(self):
        """Update server metadata with creator account should fail"""
        meta = {'falsekey1': 'falsealt1', 'key2': 'alt2', 'meta_key_1': 'alt3'}
        with self.assertRaises(Forbidden):
            self.creator_servers_client.update_server_metadata(
                self.server.id, meta)
        server_response = self.servers_client.list_server_metadata(
            self.server.id)
        metadata = server_response.entity
        self._assert_update_negative_metadata(metadata)
    
    @attr(type='smoke', net='no')
    def test_server_metadata_update_with_observer_role(self):
        """Update server metadata with observer account should fail"""
        meta = {'falsekey1': 'alt1', 'key2': 'alt2', 'meta_key_1': 'falsealt3'}
        with self.assertRaises(Forbidden):
            self.observer_servers_client.update_server_metadata(
                self.server.id, meta)
        server_response = self.servers_client.list_server_metadata(
            self.server.id)
        metadata = server_response.entity
        self._assert_update_negative_metadata(metadata)
    
    def _assert_update_positive_metadata(self, metadata):
        message = "Expected {0} to be {1}, was {2}."
        self.assertEqual('alt1', metadata.key1,
            msg=message.format('Metadata Item not found on server:', 
                               self.server.id, 'Expected Item Key : ', 
                               'metadata.key1 with Value : ',
                               'alt1, but received ',
                               metadata.meta_key_1))
        self.assertEqual('alt2', metadata.key2,
            msg=message.format('Metadata Item not found on server:', 
                               self.server.id, 'Expected Item Key : ', 
                               'metadata.key2 with Value : ',
                               'alt2, but received ',
                               metadata.meta_key_2))
        self.assertEqual('alt3', metadata.meta_key_1,
            msg=message.format('Metadata Item not found on server:', 
                               self.server.id, 'Expected Item Key : ', 
                               'metadata.meta_key_1 with Value : ',
                               'alt3, but received ',
                               metadata.meta_key_1))
        self.assertEqual('meta_value_2', metadata.meta_key_2,
            msg=message.format('Metadata Item not found on server:', 
                               self.server.id, 'Expected Item Key : ', 
                               'metadata.meta_key_2 with Value : ',
                               'metadata.meta_value_2, but received ',
                               metadata.meta_key_2))
    
    def _assert_update_negative_metadata(self, metadata):
        message = "Expected {0} to be {1}, was {2}."
        self.assertNotEqual('falsealt3', metadata.meta_key_1,
            msg=message.format('Metadata Item not found on server:', 
                               self.server.id, 'Expected Item Key : ', 
                               'metadata.key1 with Value : ',
                               'alt1, but received ',
                               metadata.meta_key_1))
    
    @attr(type='smoke', net='no')
    def test_server_metadata_set_with_admin_role(self):
        """Set server metadata with admin account should work"""
        meta = {'meta1': 'data1'}
        server_response = self.servers_client.set_server_metadata(
            self.server.id, meta)
        self.assertEqual(200, server_response.status_code)
        metadata = server_response.entity
        self._assert_set_positive_metadata(metadata)
    
    @attr(type='smoke', net='no')
    def test_server_metadata_set_with_creator_role(self):
        """Set server metadata with creator account should fail"""
        meta = {'meta_key_1': 'data1'}
        with self.assertRaises(Forbidden):
            self.creator_servers_client.set_server_metadata(
                self.server.id, meta)
        server_response = self.servers_client.list_server_metadata(
            self.server.id)
        metadata = server_response.entity
        self._assert_set_negative_metadata(metadata)
    
    @attr(type='smoke', net='no')
    def test_server_metadata_set_with_observer_role(self):
        """Set server metadata with observer account should fail"""
        meta = {'meta_key_1': 'data1'}
        with self.assertRaises(Forbidden):
            self.observer_servers_client.set_server_metadata(
                self.server.id, meta)
        server_response = self.servers_client.list_server_metadata(
            self.server.id)
        metadata = server_response.entity
        self._assert_set_negative_metadata(metadata)
    
    def _assert_set_positive_metadata(self, metadata):
        message = "Expected {0} to be {1}, was {2}."
        self.assertEqual('data1', metadata.meta1,
            msg=message.format('Metadata Item not found on server:', 
                               self.server.id, 'Expected Item Key : ', 
                               'meta1 with Value : ',
                               'data1, but received ',
                               metadata.meta1))
    
    def _assert_set_negative_metadata(self, metadata):
        message = "Expected {0} to be {1}, was {2}."
        self.assertNotEqual('data1', metadata.meta_key_1,
            msg=message.format('Metadata Item not found on server:', 
                               self.server.id, 'Expected Item Key : ', 
                               'metadata.key1 with Value : ',
                               'alt1, but received ',
                               metadata.meta_key_1))
    
    @attr(type='smoke', net='no')
    def test_server_metadata_get_item_with_admin_role(self):
        """Get server metadata with admin account should work"""
        meta = {'meta_key_1': 'getitem1'}
        set_meta_server_response = self.servers_client.set_server_metadata(
            self.server.id, meta)
        self.assertEqual(200, set_meta_server_response.status_code)
        server_response = self.servers_client.get_server_metadata_item(
            self.server.id,
            'meta_key_1')
        self.assertEqual(200, server_response.status_code)
        metadata = server_response.entity
        self._assert_get_item_positive_metadata(metadata)
    
    @attr(type='smoke', net='no')
    def test_server_metadata_get_item_with_creator_role(self):
        """Get server metadata with creator account should work"""
        meta = {'meta_key_1': 'getitem1'}
        set_meta_server_response = self.servers_client.set_server_metadata(
            self.server.id, meta)
        self.assertEqual(200, set_meta_server_response.status_code)
        server_response = self.creator_servers_client.get_server_metadata_item(
            self.server.id,
            'meta_key_1')
        self.assertEqual(200, server_response.status_code)
        metadata = server_response.entity
        self._assert_get_item_positive_metadata(metadata)
    
    @attr(type='smoke', net='no')
    def test_server_metadata_get_item_with_observer_role(self):
        """Get server metadata with observer account should work"""
        meta = {'meta_key_1': 'getitem1'}
        set_meta_server_response = self.servers_client.set_server_metadata(
            self.server.id, meta)
        self.assertEqual(200, set_meta_server_response.status_code)
        server_response = self.observer_servers_client.get_server_metadata_item(
            self.server.id,
            'meta_key_1')
        self.assertEqual(200, server_response.status_code)
        metadata = server_response.entity
        self._assert_get_item_positive_metadata(metadata)
    
    def _assert_get_item_positive_metadata(self, metadata):
        message = "Expected {0} to be {1}, was {2}."
        self.assertEqual('getitem1', metadata.meta_key_1,
            msg=message.format('Metadata Item not found on server:', 
                               self.server.id, 'Expected Item Key : ', 
                               'metadata.key1 with Value : ',
                               'getitem1, but received ',
                               metadata.meta_key_1))
    
    @attr(type='smoke', net='no')
    def test_server_metadata_set_item_with_admin_role(self):
        """Set server metadata item with admin account should work"""
        server_response = self.servers_client.set_server_metadata_item(
            self.server.id,
            'meta_key_2', 'novaitem')
        self.assertEqual(200, server_response.status_code)
        server_response = self.servers_client.list_server_metadata(
            self.server.id)
        metadata = server_response.entity
        message = "Expected {0} to be {1}, was {2}."
        self.assertEqual('novaitem', metadata.meta_key_2,
            msg=message.format('Metadata Item not found on server:', 
                               self.server.id, 'Expected Item Key : ', 
                               'metadata.key2 with Value : ',
                               'novaitem, but received ',
                               metadata.meta_key_2))
    
    @attr(type='smoke', net='no')
    def test_server_metadata_set_item_with_creator_role(self):
        """Set server metadata item with creator account should fail"""
        with self.assertRaises(Forbidden):
            self.creator_servers_client.set_server_metadata_item(
                self.server.id,
                'meta_key_1', 'novaitemneg')
        server_response = self.servers_client.list_server_metadata(
            self.server.id)
        metadata = server_response.entity
        self._assert_set_item_negative_metadata(metadata)
    
    @attr(type='smoke', net='no')
    def test_server_metadata_set_item_with_observer_role(self):
        """Set server metadata item with observer account should fail"""
        with self.assertRaises(Forbidden):
            self.observer_servers_client.set_server_metadata_item(
                self.server.id,
                'meta_key_1', 'novaitemneg')
        server_response = self.servers_client.list_server_metadata(
            self.server.id)
        metadata = server_response.entity
        self._assert_set_item_negative_metadata(metadata)
    
    def _assert_set_item_negative_metadata(self, metadata):
        message = "Expected {0} to be {1}, was {2}."
        self.assertNotEqual('novaitemneg', metadata.meta_key_1,
            msg=message.format('Metadata Item not found on server:', 
                               self.server.id, 'Expected Item Key : ', 
                               'metadata.key1 with Value : ',
                               'getitem1, but received ',
                               metadata.meta_key_1))
    
    @attr(type='smoke', net='no')
    def test_server_metadata_delete_with_admin_role(self):
        """Delete server metadata with admin account should work"""
        meta = {'meta_key_10': 'data1'}
        set_meta_server_response = self.servers_client.set_server_metadata(
            self.server.id, meta)
        self.assertEqual(200, set_meta_server_response.status_code)
        server_response = self.servers_client.delete_server_metadata_item(
            self.server.id,
            'meta_key_10')
        self.assertEqual(204, server_response.status_code)
        server_response = self.servers_client.list_server_metadata(
            self.server.id)
        metadata = server_response.entity
        with self.assertRaises(AttributeError):
            self.assertIsNone(metadata.meta_key_10, msg="Assert metadata is missing")
    
    @attr(type='smoke', net='no')
    def test_server_metadata_delete_with_creator_role(self):
        """Delete server metadata with creator account should fail"""
        meta = {'meta_key_1': 'datanotdel1'}
        set_meta_server_response = self.servers_client.set_server_metadata(
            self.server.id, meta)
        self.assertEqual(200, set_meta_server_response.status_code)
        with self.assertRaises(Forbidden):
            self.creator_servers_client.delete_server_metadata_item(
                self.server.id,
                'meta_key_1')
        server_response = self.servers_client.list_server_metadata(
            self.server.id)
        metadata = server_response.entity
        self._assert_delete_item_failed_metadata(metadata)
    
    @attr(type='smoke', net='no')
    def test_server_metadata_delete_with_observer_role(self):
        """Delete server metadata with observer account should fail"""
        meta = {'meta_key_1': 'datanotdel1'}
        set_meta_server_response = self.servers_client.set_server_metadata(
            self.server.id, meta)
        self.assertEqual(200, set_meta_server_response.status_code)
        with self.assertRaises(Forbidden):
            self.observer_servers_client.delete_server_metadata_item(
                self.server.id,
                'meta_key_1')
        server_response = self.servers_client.list_server_metadata(
            self.server.id)
        metadata = server_response.entity
        self._assert_delete_item_failed_metadata(metadata)
    
    def _assert_delete_item_failed_metadata(self, metadata):
        message = "Expected {0} to be {1}, was {2}."
        self.assertEqual('datanotdel1', metadata.meta_key_1,
            msg=message.format('Metadata Item not found on server:', 
                               self.server.id, 'Expected Item Key : ', 
                               'metadata.key1 with Value : ',
                               'datanotdel1, but received ',
                               metadata.meta_key_1))