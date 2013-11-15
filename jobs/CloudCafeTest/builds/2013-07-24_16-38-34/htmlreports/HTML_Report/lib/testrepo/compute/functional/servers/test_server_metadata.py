from ccengine.common.tools.datagen import rand_name
from ccengine.common.exceptions.compute import ItemNotFound, OverLimit
from testrepo.common.testfixtures.compute import ComputeFixture
from ccengine.common.decorators import attr
from ccengine.domain.types import NovaServerStatusTypes
import unittest2 as unittest


class ServerMetadataTest(ComputeFixture):
    limits_set = False

    @classmethod
    def setUpClass(cls):
        super(ServerMetadataTest, cls).setUpClass()
        server_response = cls.compute_provider.create_active_server()
        cls.server = server_response.entity
        cls.resources.add(cls.server.id, cls.servers_client.delete_server)
        metadata_limit = cls.limits_client.get_max_server_meta()
        if metadata_limit is not None:
            cls.limits_set = True

    @classmethod
    def tearDownClass(cls):
        super(ServerMetadataTest, cls).tearDownClass()

    def setUp(self):
        self.meta = {'meta_key_1': 'meta_value_1', 'meta_key_2': 'meta_value_2'}
        self.servers_client.set_server_metadata(self.server.id, self.meta)

    @attr(type='positive', net='no')
    def test_list_server_metadata(self):
        """All metadata key/value pairs for a server should be returned"""
        metadata_response = self.servers_client.list_server_metadata(self.server.id)
        metadata = metadata_response.entity
        self.assertEqual(200, metadata_response.status_code,
                         "List server metadata call response was: %s" % (metadata_response.status_code))
        self.assertEqual('meta_value_1', metadata.meta_key_1,
                         "Metadata Item not found on server %s. Expected Item Key : meta_key_1, Value : meta_value_1" % self.server.id)
        self.assertEqual('meta_value_2', metadata.meta_key_2,
                         "Metadata Item not found on server %s. Expected Item Key : meta_key_2, Value : meta_value_2" % self.server.id)

    @attr(type='positive', net='no')
    def test_set_server_metadata(self):
        """The server's metadata should be replaced with the provided values"""
        meta = {'meta1': 'data1'}
        server_response = self.compute_provider.create_active_server(metadata=meta)
        server = server_response.entity
        self.resources.add(server.id, self.servers_client.delete_server)

        new_meta = {'meta2': 'data2', 'meta3': 'data3'}
        metadata_response = self.servers_client.set_server_metadata(server.id,
                                                                    new_meta)
        metadata = metadata_response.entity
        self.assertEqual(200, metadata_response.status_code,
                         "Set server metadata call response was: %s" % (metadata_response.status_code))
        self.assertEqual('data2', metadata.meta2,
                         "Metadata Item not found on server %s. Expected Item Key : meta2, Value : data2" % server.id)
        self.assertEqual('data3', metadata.meta3,
                         "Metadata Item not found on server %s. Expected Item Key : meta3, Value : data3" % server.id)
        self.assertFalse(hasattr(metadata, 'meta1'),
                         "The already existing metadata(Key : meta1) is not removed during Set metadata")

        actual_metadata_response = self.servers_client.list_server_metadata(server.id)
        actual_metadata = actual_metadata_response.entity
        self.assertEqual('data2', actual_metadata.meta2,
                         "Metadata Item not found on server %s. Expected Item Key : meta2, Value : data2" % server.id)
        self.assertEqual('data3', actual_metadata.meta3,
                         "Metadata Item not found on server %s. Expected Item Key : meta3, Value : data3" % server.id)
        self.assertFalse(hasattr(actual_metadata, 'meta1'),
                         "The already existing metadata(Key : meta1) is not removed during Set metadata")

    @attr(type='positive', net='no')
    def test_update_server_metadata(self):
        """The server's metadata values should be updated to the provided values"""
        meta = {'key1': 'alt1', 'key2': 'alt2', 'meta_key_1': 'alt3'}
        metadata_response = self.servers_client.update_server_metadata(self.server.id, meta)
        metadata = metadata_response.entity
        self.assertEqual(200, metadata_response.status_code,
                         "Update server metadata call response was: %s" % (metadata_response.status_code))
        self.assertEqual('alt1', metadata.key1,
                         "Metadata Item not found on server %s. Expected Item Key : key1, Value : alt1" % self.server.id)
        self.assertEqual('alt2', metadata.key2,
                         "Metadata Item not found on server %s. Expected Item Key : key2, Value : alt2" % self.server.id)
        self.assertEqual('alt3', metadata.meta_key_1,
                         "Metadata Item not found on server %s. Expected Item Key : meta_key_1, Value : alt3" % self.server.id)
        self.assertEqual('meta_value_2', metadata.meta_key_2,
                         "Metadata Item not found on server %s. Expected Item Key : meta_key_2, Value : meta_value_2" % self.server.id)

        #Verify the values have been updated to the proper values
        actual_metadata_response = self.servers_client.list_server_metadata(self.server.id)
        actual_metadata = actual_metadata_response.entity
        self.assertEqual('alt1', actual_metadata.key1,
                         "Metadata Item not found on server %s. Expected Item Key : key1, Value : alt1" % self.server.id)
        self.assertEqual('alt2', actual_metadata.key2,
                         "Metadata Item not found on server %s. Expected Item Key : key2, Value : alt2" % self.server.id)
        self.assertEqual('alt3', actual_metadata.meta_key_1,
                         "Metadata Item not found on server %s. Expected Item Key : meta_key_1, Value : alt3" % self.server.id)
        self.assertEqual('meta_value_2', actual_metadata.meta_key_2,
                         "Metadata Item not found on server %s. Expected Item Key : meta_key_2, Value : meta_value_2" % self.server.id)

    @attr(type='positive', net='no')
    def test_get_server_metadata_item(self):
        """The value for a specific metadata key should be returned"""
        metadata_response = self.servers_client.get_server_metadata_item(self.server.id,
                                                                         'meta_key_1')
        metadata = metadata_response.entity
        self.assertEqual('meta_value_1', metadata.meta_key_1,
                         msg="Metadata Item not found on server %s. Expected Item Key : meta_key_1, Value : meta_value_1" % self.server.id)

    @attr(type='positive', net='no')
    def test_set_server_metadata_item(self):
        """The value provided for the given meta item should be set for the server"""
        meta = {'meta_key_2': 'nova'}
        metadata_response = self.servers_client.set_server_metadata_item(self.server.id,
                                                                         'meta_key_2', 'nova')
        metadata = metadata_response.entity
        self.assertEqual(200, metadata_response.status_code,
                         "Set server metadata item call response was: %s" % (metadata_response.status_code))
        self.assertEqual('nova', metadata.meta_key_2,
                         "Metadata Item not found on server %s. Expected Item Key : meta_key_2, Value : nova" % self.server.id)

        actual_metadata_response = self.servers_client.list_server_metadata(self.server.id)
        actual_metadata = actual_metadata_response.entity
        self.assertEqual('nova', actual_metadata.meta_key_2,
                         "Metadata Item not found on server %s. Expected Item Key : meta_key_2, Value : nova" % self.server.id)
        self.assertEqual('meta_value_1', actual_metadata.meta_key_1,
                         "Metadata Item not found on server %s. Expected Item Key : meta_key_1, Value : meta_value_1" % self.server.id)

    @attr(type='positive', net='no')
    def test_add_new_server_metadata_item(self):
        """ The metadata item should be added to the server"""
        meta = {'meta_key_3': 'meta_value_3'}
        metadata_response = self.servers_client.set_server_metadata_item(self.server.id,
                                                                         'meta_key_3', 'meta_value_3')
        metadata = metadata_response.entity
        self.assertEqual(200, metadata_response.status_code, "Add server metadata item call response was: %s" % (metadata_response.status_code))
        self.assertEqual('meta_value_3', metadata.meta_key_3,
                         "Metadata Item not found on server %s. Expected Item Key : meta_key_3, Value : meta_value_3" % self.server.id)

        actual_metadata_response = self.servers_client.list_server_metadata(self.server.id)
        actual_metadata = actual_metadata_response.entity
        self.assertEqual('meta_value_3', actual_metadata.meta_key_3,
                         "Metadata Item not found on server %s. Expected Item Key : meta_key_3, Value : meta_value_3" % self.server.id)
        self.assertEqual('meta_value_2', actual_metadata.meta_key_2,
                         "Metadata Item not found on server %s. Expected Item Key : meta_key_2, Value : meta_value_2" % self.server.id)
        self.assertEqual('meta_value_1', actual_metadata.meta_key_1,
                         "Metadata Item not found on server %s. Expected Item Key : meta_key_1, Value : meta_value_1" % self.server.id)

    @attr(type='positive', net='no')
    def test_delete_server_metadata_item(self):
        """The metadata value/key pair should be deleted from the server"""

        response = self.servers_client.delete_server_metadata_item(self.server.id,
                                                                   'meta_key_1')
        self.assertEqual(204, response.status_code, "Delete server metadata item call response was: %s" % (response.status_code))
        metadata_response = self.servers_client.list_server_metadata(self.server.id)
        metadata = metadata_response.entity
        self.assertFalse(hasattr(metadata, 'meta_key_1'), "The server\
                            metadata item (Key: meta_key_1) is not deleted")

    @attr(type='negative', net='no')
    def test_delete_nonexistent_server_metadata_item(self):
            with self.assertRaises(ItemNotFound):
                self.servers_client.delete_server_metadata_item(self.server.id,
                                                                'meta_key_5')

    @attr(type='negative', net='no')
    def test_get_nonexistent_server_metadata_item(self):
        with self.assertRaises(ItemNotFound):
            self.servers_client.get_server_metadata_item(self.server.id,
                                                         'meta_key_5')

    @attr(type='negative', net='no')
    def test_set_blank_metadata_value(self):
        meta = {'meta_key': ''}
        create_server_response = self.servers_client.create_server(rand_name('testserver'),
                                                                   self.image_ref,
                                                                   self.flavor_ref,
                                                                   metadata=meta)
        metadata_response = self.servers_client.list_server_metadata(create_server_response.entity.id)
        metadata = metadata_response.entity
        self.assertEqual(None or '', metadata.meta_key)

    @attr(type='negative', net='no')
    @unittest.skip('Failing, under review')
    def test_set_blank_metadata_dict(self):
        blank_meta = {'': ''}
        create_server_response = self.servers_client.create_server(rand_name('testserver'), self.image_ref, self.flavor_ref, metadata=blank_meta)
        server_response = self.servers_client.get_server(create_server_response.entity.id)
        server = server_response.entity
        self.assertEqual("", server.metadata[''])

    @attr(type='positive', net='no')
    def test_create_server_with_max_metadata_items(self):
        metadata_limit = self.limits_client.get_max_server_meta()
        expected_metadata = {}
        if self.config.misc.serializer == "xml":
            for i in range(int(metadata_limit)):
                expected_metadata['metakey' + str(i)] = 'metavalue' + str(i)
        else:
            for i in range(metadata_limit):
                expected_metadata['metakey' + str(i)] = 'metavalue' + str(i)
        name = rand_name('testserver')

        server_response = self.servers_client.create_server(name, self.image_ref,
                                                            self.flavor_ref, metadata=expected_metadata)
        server = server_response.entity
        self.resources.add(server.id, self.servers_client.delete_server)

        self.assertEqual(202, server_response.status_code)
        active_server_response = self.compute_provider.wait_for_server_status(server.id, NovaServerStatusTypes.ACTIVE)
        active_server = active_server_response.entity

        for key, value in expected_metadata.items():
            self.assertEqual(value, getattr(active_server.metadata, key),
                             "Metadata Item not found on server %s. Expected Item Key : %s, Value : %s" % (self.server.id, key, value))

    @attr(type='negative', net='no')
    def test_create_server_with_number_of_metadata_items_more_than_max_metadata_items(self):
        """Try to create server with the number of meta data, more than maximum number of metadata allowed"""
        metadata_limit = self.limits_client.get_max_server_meta()
        expected_metadata = {}
        # Set the number of meta data more than maximum allowed
        if self.config.misc.serializer == "xml":
            for i in range(int(metadata_limit) + 1):
                expected_metadata['metakey' + str(i)] = 'metavalue' + str(i)
        else:
            for i in range(metadata_limit + 1):
                expected_metadata['metakey' + str(i)] = 'metavalue' + str(i)

        with self.assertRaises(OverLimit):
            name = rand_name('testserver')
            server_response = self.servers_client.create_server(name, self.image_ref,
                                                                self.flavor_ref,
                                                                metadata=expected_metadata)
            self.resources.add(server_response.entity.id,
                               self.servers_client.delete_server)
