import unittest

from testrepo.common.testfixtures.object_storage_fixture \
        import ObjectStorageTestFixture
from ccengine.providers.objectstorage.object_storage_provider \
        import ObjectStorageClientProvider
from ccengine.clients.objectstorage.object_storage_client \
        import ObjectStorageAPIClient


#these need to be moved to a config
CONTENT_TYPE_TEXT = 'text/plain; charset=UTF-8'


"""4.2 Storage Container Services Smoke Tests"""


class AuthNegativeContainerSmokeTest(ObjectStorageTestFixture):
    @classmethod
    def setUpClass(cls):
        super(AuthNegativeContainerSmokeTest, cls).setUpClass()

        alt_config = cls.config
        v = {
            'identity': {
                'username': cls.config.identity_api.alt_username,
                'api_key': cls.config.identity_api.alt_api_key
            }
        }
        alt_config = alt_config.mcp_override(v)
        cls.alt_client = ObjectStorageClientProvider.get_client(alt_config)

    """4.2.1. List Objects in a Container"""
    def test_objects_list_fails_with_valid_foreign_api_key(self):
        container_name = self.client.generate_unique_container_name()
        self.client.create_container(container_name)
        self.addCleanup(self.client.force_delete_containers,
                        [container_name])

        file_data = 'Test file data'
        content_length = str(len(file_data))
        object_name = self.client.generate_unique_object_name()
        self.client.set_storage_object(
                container_name,
                object_name,
                content_length=content_length,
                content_type=CONTENT_TYPE_TEXT,
                payload=file_data)

        storage_url = self.client.storage_url
        cross_auth_token = self.alt_client.auth_token
        cross_client = ObjectStorageAPIClient(storage_url, cross_auth_token)
        r = cross_client.list_containers()
        self.assertEqual(r.status_code, 401, 'should not list objects')

    """4.2.1.1. Serialized List Output"""

    """4.2.1.2. Controlling a Large List of Objects"""

    """4.2.1.3. Pseudo-Hierarchical Folders/Directories"""

    """4.2.2. Create Container"""
    def test_container_creation_fails_with_valid_foreign_api_key(self):
        container_name = self.client.generate_unique_container_name()

        storage_url = self.client.storage_url
        cross_auth_token = self.alt_client.auth_token
        cross_client = ObjectStorageAPIClient(storage_url, cross_auth_token)
        r = cross_client.create_container(container_name)
        self.assertEqual(r.status_code, 401, 'should not create container')

    def test_container_creation_fails_with_existing_container_and_valid_foreign_api_key(self):
        container_name = self.client.generate_unique_container_name()
        r = self.client.create_container(container_name)
        self.addCleanup(self.client.force_delete_containers,
                        [container_name])
        self.assertEqual(r.status_code, 201, 'should be created')

        storage_url = self.client.storage_url
        cross_auth_token = self.alt_client.auth_token
        cross_client = ObjectStorageAPIClient(storage_url, cross_auth_token)
        r = cross_client.create_container(container_name)
        self.assertEqual(r.status_code, 401, 'should not create container')

    """4.2.3. Delete Container"""
    def test_container_deletion_fails_with_valid_foreign_api_key(self):
        container_name = self.client.generate_unique_container_name()
        r = self.client.create_container(container_name)
        self.addCleanup(self.client.force_delete_containers,
                        [container_name])
        self.assertEqual(r.status_code, 201, 'should be created')

        storage_url = self.client.storage_url
        cross_auth_token = self.alt_client.auth_token
        cross_client = ObjectStorageAPIClient(storage_url, cross_auth_token)
        r = cross_client.delete_container(container_name)
        self.assertEqual(r.status_code, 401, 'should not delete container')

        r = self.client.list_objects(container_name)
        self.assertEqual(r.status_code, 204, 'should still exist')

    """4.2.4. Retrieve Container Metadata"""
    def test_metadata_retrieval_fails_with_valid_foreign_api_key(self):
        container_name = self.client.generate_unique_container_name()
        self.client.create_container(container_name)
        self.addCleanup(self.client.force_delete_containers,
                        [container_name])

        metadata = {'Book-One': 'fight_club',
                    'Book-Two': 'a_clockwork_orange'}
        r = self.client.set_container_metadata(container_name,
                                                           metadata)

        storage_url = self.client.storage_url
        cross_auth_token = self.alt_client.auth_token
        cross_client = ObjectStorageAPIClient(storage_url, cross_auth_token)
        r = cross_client.get_container_metadata(container_name)
        self.assertEqual(r.status_code, 401, 'should not return metadata')

    """4.2.5. Create/Update Container Metadata"""
    def test_metadata_update_fails_with_valid_foreign_api_key(self):
        container_name = self.client.generate_unique_container_name()
        self.client.create_container(container_name)
        self.addCleanup(self.client.force_delete_containers,
                        [container_name])
        metadata = {'Book-One': 'fight_club',
                    'Book-Two': 'a_clockwork_orange'}
        r = self.client.set_container_metadata(container_name,
                                                           metadata)
        self.assertEqual(r.status_code, 204, 'metadata should be added')

        metadata = {'Book-One': 'Fight_Club'}
        storage_url = self.client.storage_url
        cross_auth_token = self.alt_client.auth_token
        cross_client = ObjectStorageAPIClient(storage_url, cross_auth_token)
        r = cross_client.set_container_metadata(container_name,
                                                metadata=metadata)
        self.assertEqual(r.status_code, 401, 'should not update metadata')
