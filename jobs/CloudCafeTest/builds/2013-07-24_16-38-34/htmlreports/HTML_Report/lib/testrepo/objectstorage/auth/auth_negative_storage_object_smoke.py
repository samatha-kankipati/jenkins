import unittest

from testrepo.common.testfixtures.object_storage_fixture \
        import ObjectStorageTestFixture
from ccengine.providers.objectstorage.object_storage_provider \
        import ObjectStorageClientProvider
from ccengine.clients.objectstorage.object_storage_client \
        import ObjectStorageAPIClient


#these need to be moved to a config
CONTENT_TYPE_TEXT = 'text/plain; charset=UTF-8'


"""4.3 Auth Storage Object Services Negative Smoke Tests"""


class AuthNegativeStorageObjectSmokeTest(ObjectStorageTestFixture):
    @classmethod
    def setUpClass(cls):
        super(AuthNegativeStorageObjectSmokeTest, cls).setUpClass()

        alt_config = cls.config
        v = {
            'identity': {
                'username': cls.config.identity_api.alt_username,
                'api_key': cls.config.identity_api.alt_api_key
            }
        }
        alt_config = alt_config.mcp_override(v)

        cls.alt_client = ObjectStorageClientProvider.get_client(alt_config)

    """4.3.1. Retrieve Object"""
    def test_object_retrieval_fails_with_valid_foreign_api_key(self):
        container_name = self.client.generate_unique_container_name()
        self.client.create_container(container_name)
        self.addCleanup(self.client.force_delete_containers,
                        [container_name])

        object_name = self.client.generate_unique_object_name()
        object_data = 'Test file data'
        content_length = str(len(object_data))
        self.client.set_storage_object(
                container_name,
                object_name,
                content_length=content_length,
                content_type=CONTENT_TYPE_TEXT,
                payload=object_data)

        storage_url = self.client.storage_url
        cross_auth_token = self.alt_client.auth_token
        cross_client = ObjectStorageAPIClient(storage_url, cross_auth_token)

        r = cross_client.get_storage_object(container_name, object_name)
        self.assertEqual(r.status_code, 401, 'should not return object.')

    @unittest.skip('This test is not complete')
    def test_object_retrieval_fails_with_missing_api_key(self):
        container_name = self.client.generate_unique_container_name()
        self.client.create_container(container_name)
        self.addCleanup(self.client.force_delete_containers,
                        [container_name])

        object_name = self.client.generate_unique_object_name()
        object_data = 'Test file data'
        content_length = str(len(object_data))
        self.client.set_storage_object(
                container_name,
                object_name,
                content_length=content_length,
                content_type=CONTENT_TYPE_TEXT,
                payload=object_data)

        storage_url = self.client.storage_url
        cross_auth_token = self.alt_client.auth_token
        tokenless_client = ObjectStorageAPIClient(storage_url, None)

        r = tokenless_client.get_storage_object(container_name, object_name)
        self.assertEqual(r.status_code, 401, 'should not return object.')

    """4.3.2. Create/Update Object"""
    def test_object_creation_fails_with_valid_foreign_api_key(self):
        container_name = self.client.generate_unique_container_name()
        self.client.create_container(container_name)
        self.addCleanup(self.client.force_delete_containers,
                        [container_name])

        storage_url = self.client.storage_url
        cross_auth_token = self.alt_client.auth_token
        cross_client = ObjectStorageAPIClient(storage_url, cross_auth_token)

        object_name = self.client.generate_unique_object_name()
        object_data = 'Test file data'
        content_length = str(len(object_data))
        r = cross_client.set_storage_object(container_name,
                                            object_name,
                                            content_length=content_length,
                                            content_type=CONTENT_TYPE_TEXT,
                                            payload=object_data)
        self.assertEqual(r.status_code, 401, 'should not create object.')

    def test_object_update_fails_with_valid_foreign_api_key(self):
        container_name = self.client.generate_unique_container_name()
        self.client.create_container(container_name)
        self.addCleanup(self.client.force_delete_containers,
                        [container_name])

        object_name = self.client.generate_unique_object_name()
        object_data = 'Test file data'
        content_length = str(len(object_data))
        self.client.set_storage_object(
                container_name,
                object_name,
                content_length=content_length,
                content_type=CONTENT_TYPE_TEXT,
                payload=object_data)

        storage_url = self.client.storage_url
        cross_auth_token = self.alt_client.auth_token
        cross_client = ObjectStorageAPIClient(storage_url, cross_auth_token)

        object_data = 'Updated test file data'
        content_length = str(len(object_data))
        x = cross_client.set_storage_object(container_name,
                                            object_name,
                                            content_length=content_length,
                                            content_type=CONTENT_TYPE_TEXT,
                                            payload=object_data)

        self.assertEqual(x.status_code, 401, 'should not update object.')

    """4.3.2.1. Large Object Creation"""

    """4.3.2.2. Chunked Transfer Encoding"""
    """TODO(rich5317): Create negative tests for chunked transfers"""

    """4.3.2.3. Bulk Importing Data"""

    """4.3.2.4. Assigning CORS Headers to Requests"""
    """TODO(rich5317): Create negative tests for CORS Headers"""

    """4.3.2.5. Enabling File Compression with the Content-Encoding Header"""

    """4.3.2.6. Enabling Browser Bypass with the Content-Disposition Header"""

    """4.3.2.7. Expiring Objects with the X-Delete-After and X-Delete-At Headers"""

    """4.3.2.8. Object Versioning"""

    """4.3.3. Copy Object"""
    def test_object_copy_fails_with_valid_foreign_api_key(self):
        container_name = self.client.generate_unique_container_name()
        self.client.create_container(container_name)
        self.addCleanup(self.client.force_delete_containers,
                        [container_name])

        source_object_name = self.client.generate_unique_object_name()
        source_object_data = 'Test file data'
        content_length = str(len(source_object_data))
        self.client.set_storage_object(
                container_name,
                source_object_name,
                content_length=content_length,
                content_type=CONTENT_TYPE_TEXT,
                payload=source_object_data)

        copied_object_name = ''.join([source_object_name, '.new'])

        storage_url = self.client.storage_url
        cross_auth_token = self.alt_client.auth_token
        cross_client = ObjectStorageAPIClient(storage_url, cross_auth_token)
        r = cross_client.copy_storage_object(src_container=container_name,
                                             src_object=source_object_name,
                                             dst_object=copied_object_name)
        self.assertEqual(r.status_code, 401,
                'should not copy an existing object')

    def test_object_copy_fails_with_valid_foreign_api_key_and_x_copy_from_header(self):
        container_name = self.client.generate_unique_container_name()
        self.client.create_container(container_name)
        self.addCleanup(self.client.force_delete_containers,
                        [container_name])

        object_name = self.client.generate_unique_object_name()
        object_data = 'Test file data'
        content_length = str(len(object_data))
        self.client.set_storage_object(
                container_name,
                object_name,
                content_length=content_length,
                content_type=CONTENT_TYPE_TEXT,
                payload=object_data)

        copied_object_name = ''.join([object_name, '.new'])
        source = ''.join([container_name, '/', object_name])
        headers = {'X-Copy-From': source}

        storage_url = self.client.storage_url
        cross_auth_token = self.alt_client.auth_token
        cross_client = ObjectStorageAPIClient(storage_url, cross_auth_token)
        r = cross_client.set_storage_object(container_name,
                                            copied_object_name,
                                            content_length=0,
                                            content_type=CONTENT_TYPE_TEXT,
                                            payload='',
                                            headers=headers)
        self.assertEqual(r.status_code, 401,
                'should not copy an existing object')

    """4.3.4. Delete Object"""
    def test_object_deletion_fails_with_valid_foreign_api_key(self):
        container_name = self.client.generate_unique_container_name()
        self.client.create_container(container_name)
        self.addCleanup(self.client.force_delete_containers,
                        [container_name])

        object_name = self.client.generate_unique_object_name()
        object_data = 'Test file data'
        content_length = str(len(object_data))
        r = self.client.set_storage_object(
                container_name,
                object_name,
                content_length=content_length,
               content_type=CONTENT_TYPE_TEXT,
                payload=object_data)

        storage_url = self.client.storage_url
        cross_auth_token = self.alt_client.auth_token
        cross_client = ObjectStorageAPIClient(storage_url, cross_auth_token)
        r = cross_client.delete_storage_object(container_name,
                                               object_name)
        self.assertEqual(r.status_code, 401, 'should not be deleted')

    """4.3.5. Retrieve Object Metadata"""
    def test_metadata_retrieval_fails_with_valid_foreign_api_key(self):
        container_name = self.client.generate_unique_container_name()
        self.client.create_container(container_name)
        self.addCleanup(self.client.force_delete_containers,
                        [container_name])

        object_name = self.client.generate_unique_object_name()
        object_data = 'Test file data'
        content_length = str(len(object_data))
        headers = {'X-Object-Meta-Grok': 'Drok'}
        self.client.set_storage_object(
                container_name,
                object_name,
                content_length=content_length,
                content_type=CONTENT_TYPE_TEXT,
                payload=object_data,
                headers=headers)

        storage_url = self.client.storage_url
        cross_auth_token = self.alt_client.auth_token
        cross_client = ObjectStorageAPIClient(storage_url, cross_auth_token)
        r = cross_client.get_storage_object_metadata(container_name,
                                                          object_name)
        self.assertEqual(r.status_code, 401, 'should not get metadata')

    """4.3.6. Update Object Metadata"""
    def test_object_update_metadata_fails_with_valid_foreign_api_key(self):
        container_name = self.client.generate_unique_container_name()
        self.client.create_container(container_name)
        self.addCleanup(self.client.force_delete_containers,
                        [container_name])

        object_name = self.client.generate_unique_object_name()
        object_data = 'Test file data'
        content_length = str(len(object_data))
        headers = {'X-Object-Meta-Grok': 'Drok'}
        self.client.set_storage_object(
                container_name,
                object_name,
                content_length=content_length,
                content_type=CONTENT_TYPE_TEXT,
                payload=object_data,
                headers=headers)

        storage_url = self.client.storage_url
        cross_auth_token = self.alt_client.auth_token
        cross_client = ObjectStorageAPIClient(storage_url, cross_auth_token)
        metadata = {'Foo': 'Bar'}
        r = cross_client.set_storage_object_metadata(container_name,
                                                     object_name,
                                                     metadata)
        self.assertEqual(r.status_code, 401, 'should not set metadata')
