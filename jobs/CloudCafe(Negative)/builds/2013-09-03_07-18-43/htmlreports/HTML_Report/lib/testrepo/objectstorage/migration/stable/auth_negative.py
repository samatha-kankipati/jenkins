import unittest
import os.path
from calendar import timegm
import time

from testrepo.common.testfixtures.object_storage_fixture \
        import ObjectStorageTestFixture
from ccengine.providers.objectstorage.object_storage_provider import \
        ObjectStorageClientProvider
from ccengine.clients.objectstorage.object_storage_client import \
        ObjectStorageAPIClient


class AuthNegativeTest(ObjectStorageTestFixture):
    @classmethod
    def setUpClass(cls):
        super(AuthNegativeTest, cls).setUpClass()

        alt_config = cls.config
        v = {
            'identity': {
                'username': cls.config.identity_api.alt_username,
                'api_key': cls.config.identity_api.alt_api_key
            }
        }
        alt_config = alt_config.mcp_override(v)

        cls.alt_client = ObjectStorageClientProvider.get_client(alt_config)
        cls.valid_expired_token = 'f642682de507145169fdc0bd5a97050f'
        cls.bad_token = 'bad_token'

    def test_auth_create_container(self):
        container_name = self.client.generate_unique_container_name()
        self.addCleanup(self.client.force_delete_containers,
                        [container_name])

        storage_url = self.client.storage_url

        auth_token = self.valid_expired_token
        alt_client = ObjectStorageAPIClient(storage_url, auth_token)
        r = alt_client.create_container(container_name)
        self.assertEqual(r.status_code, 401,
                'should not create container with expired token')

        auth_token = self.bad_token
        alt_client = ObjectStorageAPIClient(storage_url, auth_token)
        r = alt_client.create_container(container_name)
        self.assertEqual(r.status_code, 401,
                'should not create container with bad token')

        auth_token = self.alt_client.auth_token
        alt_client = ObjectStorageAPIClient(storage_url, auth_token)
        r = alt_client.create_container(container_name)
        self.assertEqual(r.status_code, 401,
                'should not create container with cross token')

    def test_auth_container_delete(self):
        container_name = self.client.generate_unique_container_name()
        r = self.client.create_container(container_name)
        self.addCleanup(self.client.force_delete_containers,
                        [container_name])
        self.assertEqual(r.status_code, 201,
                'container should be created.')

        storage_url = self.client.storage_url

        auth_token = self.valid_expired_token
        alt_client = ObjectStorageAPIClient(storage_url, auth_token)
        r = alt_client.delete_container(container_name)
        self.assertEqual(r.status_code, 401,
                'should not delete container with expired token')

        auth_token = self.bad_token
        alt_client = ObjectStorageAPIClient(storage_url, auth_token)
        r = alt_client.delete_container(container_name)
        self.assertEqual(r.status_code, 401,
                'should not delete container with bad token')

        auth_token = self.alt_client.auth_token
        alt_client = ObjectStorageAPIClient(storage_url, auth_token)
        r = alt_client.delete_container(container_name)
        self.assertEqual(r.status_code, 401,
                'should not delete container with cross token')

    def test_auth_container_list(self):
        container_name = self.client.generate_unique_container_name()
        r = self.client.create_container(container_name)
        self.addCleanup(self.client.force_delete_containers,
                        [container_name])
        self.assertEqual(r.status_code, 201,
                'container should be created.')

        object_name = self.client.generate_unique_object_name()
        object_data = 'Test object data'
        content_length = str(len(object_data))
        r = self.client.set_storage_object(
                container_name,
                object_name,
                content_length=content_length,
                payload=object_data)

        self.assertEqual(r.status_code, 201, 'object should be created.')

        storage_url = self.client.storage_url

        auth_token = self.valid_expired_token
        alt_client = ObjectStorageAPIClient(storage_url, auth_token)
        r = alt_client.list_objects(container_name)
        self.assertEqual(r.status_code, 401,
                'should not list objects with expired token')

        auth_token = self.bad_token
        alt_client = ObjectStorageAPIClient(storage_url, auth_token)
        r = alt_client.list_objects(container_name)
        self.assertEqual(r.status_code, 401,
                'should not list objects with bad token')

        auth_token = self.alt_client.auth_token
        alt_client = ObjectStorageAPIClient(storage_url, auth_token)
        r = alt_client.list_objects(container_name)
        self.assertEqual(r.status_code, 401,
                'should not list objects with cross token')

    def test_auth_container_obj_count(self):
        container_name = self.client.generate_unique_container_name()
        r = self.client.create_container(container_name)
        self.addCleanup(self.client.force_delete_containers,
                        [container_name])
        self.assertEqual(r.status_code, 201,
                'container should be created.')

        object_name = self.client.generate_unique_object_name()
        object_data = 'Test object data'
        content_length = str(len(object_data))
        r = self.client.set_storage_object(
                container_name,
                object_name,
                content_length=content_length,
                payload=object_data)

        self.assertEqual(r.status_code, 201, 'object should be created.')

        storage_url = self.client.storage_url

        # TODO(rich5317): Ensure that the header keys are lowercase
        auth_token = self.valid_expired_token
        alt_client = ObjectStorageAPIClient(storage_url, auth_token)
        r = alt_client.get_container_metadata(container_name)
        self.assertEqual(r.status_code, 401,
                'should not return metadata with expired token')
        self.assertEquals('x-container-object-count' in r.headers, False,
                'should not contian Object-Count header expired token')

        auth_token = self.bad_token
        alt_client = ObjectStorageAPIClient(storage_url, auth_token)
        r = alt_client.get_container_metadata(container_name)
        self.assertEqual(r.status_code, 401,
                'should not return metadata with bad token')
        self.assertEquals('x-container-object-count' in r.headers, False,
                'should not contian Object-Count header with bad token')

        auth_token = self.alt_client.auth_token
        alt_client = ObjectStorageAPIClient(storage_url, auth_token)
        r = alt_client.get_container_metadata(container_name)
        self.assertEqual(r.status_code, 401,
                'should not return metadata with cross token')
        self.assertEquals('x-container-object-count' in r.headers, False,
                'should not contian Object-Count header with cross token')

    def test_auth_container_bytes_used(self):
        container_name = self.client.generate_unique_container_name()
        r = self.client.create_container(container_name)
        self.addCleanup(self.client.force_delete_containers,
                        [container_name])
        self.assertEqual(r.status_code, 201,
                'container should be created.')

        object_name = self.client.generate_unique_object_name()
        object_data = 'Test object data'
        content_length = str(len(object_data))
        r = self.client.set_storage_object(
                container_name,
                object_name,
                content_length=content_length,
                payload=object_data)

        self.assertEqual(r.status_code, 201, 'object should be created.')

        storage_url = self.client.storage_url

        # TODO(rich5317): Ensure that the header keys are lowercase
        auth_token = self.valid_expired_token
        alt_client = ObjectStorageAPIClient(storage_url, auth_token)
        r = alt_client.get_container_metadata(container_name)
        self.assertEqual(r.status_code, 401,
                'should not return metadata with expired token')
        self.assertEquals('x-container-bytes-used' in r.headers, False,
                'should not contian Object-Count header expired token')

        auth_token = self.bad_token
        alt_client = ObjectStorageAPIClient(storage_url, auth_token)
        r = alt_client.get_container_metadata(container_name)
        self.assertEqual(r.status_code, 401,
                'should not return metadata with bad token')
        self.assertEquals('x-container-bytes-used' in r.headers, False,
                'should not contian Object-Count header with bad token')

        auth_token = self.alt_client.auth_token
        alt_client = ObjectStorageAPIClient(storage_url, auth_token)
        r = alt_client.get_container_metadata(container_name)
        self.assertEqual(r.status_code, 401,
                'should not return metadata with cross token')
        self.assertEquals('x-container-bytes-used' in r.headers, False,
                'should not contian Object-Count header with cross token')

    def test_auth_container_acl(self):
        container_name = self.client.generate_unique_container_name()
        r = self.client.create_container(container_name)
        self.addCleanup(self.client.force_delete_containers,
                        [container_name])
        self.assertEqual(r.status_code, 201,
                'container should be created.')

        object_name = self.client.generate_unique_object_name()
        object_data = 'Test object data'
        content_length = str(len(object_data))
        r = self.client.set_storage_object(
                container_name,
                object_name,
                content_length=content_length,
                payload=object_data)

        self.assertEqual(r.status_code, 201, 'object should be created.')

        storage_url = self.client.storage_url
        headers = {'X-Container-Meta-Read': 'acl'}
        # TODO(rich5317): We should probably read metadata values with the
        #       valid account, just to ensure that it is in fact not set.

        auth_token = self.valid_expired_token
        alt_client = ObjectStorageAPIClient(storage_url, auth_token)
        r = alt_client.update_container(container_name, headers=headers)
        self.assertEqual(r.status_code, 401,
                'should not set acl metadata with expired token')

        auth_token = self.bad_token
        alt_client = ObjectStorageAPIClient(storage_url, auth_token)
        r = alt_client.update_container(container_name, headers=headers)
        self.assertEqual(r.status_code, 401,
                'should not set acl metadata with bad token')

        auth_token = self.alt_client.auth_token
        alt_client = ObjectStorageAPIClient(storage_url, auth_token)
        r = alt_client.update_container(container_name, headers=headers)
        self.assertEqual(r.status_code, 401,
                'should not set acl metadata with cross token')

    def test_auth_container_enable_access_logging(self):
        container_name = self.client.generate_unique_container_name()
        r = self.client.create_container(container_name)
        self.addCleanup(self.client.force_delete_containers,
                        [container_name])
        self.assertEqual(r.status_code, 201,
                'container should be created.')

        object_name = self.client.generate_unique_object_name()
        object_data = 'Test object data'
        content_length = str(len(object_data))
        r = self.client.set_storage_object(
                container_name,
                object_name,
                content_length=content_length,
                payload=object_data)

        self.assertEqual(r.status_code, 201, 'object should be created.')

        storage_url = self.client.storage_url
        headers = {'X-Container-Meta-Log-Delivery': 'TRUE'}
        # TODO(rich5317): We should probably read metadata values with the
        #       valid account, just to ensure that it is in fact not set.

        auth_token = self.valid_expired_token
        alt_client = ObjectStorageAPIClient(storage_url, auth_token)
        r = alt_client.update_container(container_name, headers=headers)
        self.assertEqual(r.status_code, 401,
                'should not enable logging with expired token')

        auth_token = self.bad_token
        alt_client = ObjectStorageAPIClient(storage_url, auth_token)
        r = alt_client.update_container(container_name, headers=headers)
        self.assertEqual(r.status_code, 401,
                'should not enable logging with bad token')

        auth_token = self.alt_client.auth_token
        alt_client = ObjectStorageAPIClient(storage_url, auth_token)
        r = alt_client.update_container(container_name, headers=headers)
        self.assertEqual(r.status_code, 401,
                'should not enable logging with cross token')

    def test_auth_container_disable_access_logging(self):
        container_name = self.client.generate_unique_container_name()
        headers = {'X-Container-Meta-Log-Delivery': 'TRUE'}
        r = self.client.create_container(container_name,
                headers=headers)
        self.addCleanup(self.client.force_delete_containers,
                        [container_name])
        self.assertEqual(r.status_code, 201,
                'container should be created.')

        object_name = self.client.generate_unique_object_name()
        object_data = 'Test object data'
        content_length = str(len(object_data))
        r = self.client.set_storage_object(
                container_name,
                object_name,
                content_length=content_length,
                payload=object_data)

        self.assertEqual(r.status_code, 201, 'object should be created.')

        storage_url = self.client.storage_url
        headers = {'X-Container-Meta-Log-Delivery': 'FALSE'}
        # TODO(rich5317): We should probably read metadata values with the
        #       valid account, just to ensure that it is in fact not set.

        auth_token = self.valid_expired_token
        alt_client = ObjectStorageAPIClient(storage_url, auth_token)
        r = alt_client.update_container(container_name, headers=headers)
        self.assertEqual(r.status_code, 401,
                'should not disable logging with expired token')

        auth_token = self.bad_token
        alt_client = ObjectStorageAPIClient(storage_url, auth_token)
        r = alt_client.update_container(container_name, headers=headers)
        self.assertEqual(r.status_code, 401,
                'should not disable logging with bad token')

        auth_token = self.alt_client.auth_token
        alt_client = ObjectStorageAPIClient(storage_url, auth_token)
        r = alt_client.update_container(container_name, headers=headers)
        self.assertEqual(r.status_code, 401,
                'should not disable logging with cross token')

    def test_auth_container_get_meta(self):
        container_name = self.client.generate_unique_container_name()
        r = self.client.create_container(container_name)
        self.addCleanup(self.client.force_delete_containers,
                        [container_name])
        self.assertEqual(r.status_code, 201,
                'container should be created.')

        object_name = self.client.generate_unique_object_name()
        object_data = 'Test object data'
        content_length = str(len(object_data))
        r = self.client.set_storage_object(
                container_name,
                object_name,
                content_length=content_length,
                payload=object_data)

        self.assertEqual(r.status_code, 201, 'object should be created.')

        storage_url = self.client.storage_url

        alt_client = ObjectStorageAPIClient(storage_url,
                self.valid_expired_token)
        r = alt_client.get_container_metadata(container_name)
        self.assertEqual(r.status_code, 401,
                'should return HTTP 401 with expired token')
        for key in r.headers:
            self.assertEqual(key.startswith('x-container-meta'), False,
                    'should not return container metadata with expired token.')

        alt_client = ObjectStorageAPIClient(storage_url, self.bad_token)
        r = alt_client.get_container_metadata(container_name)
        self.assertEqual(r.status_code, 401,
                'should return HTTP 401 with bad token')
        for key in r.headers:
            self.assertEqual(key.startswith('x-container-meta'), False,
                    'should not return container metadata with bad token.')

        alt_client = ObjectStorageAPIClient(storage_url,
                self.alt_client.auth_token)
        r = alt_client.get_container_metadata(container_name)
        self.assertEqual(r.status_code, 401,
                'should return HTTP 401 with cross token')
        for key in r.headers:
            self.assertEqual(key.startswith('x-container-meta'), False,
                    'should not return container metadata with cross token.')

    def test_auth_container_set_meta(self):
        container_name = self.client.generate_unique_container_name()
        r = self.client.create_container(container_name)
        self.addCleanup(self.client.force_delete_containers,
                        [container_name])
        self.assertEqual(r.status_code, 201,
                'container should be created.')

        storage_url = self.client.storage_url
        headers = {'X-Container-Meta-hurf': 'durf'}
        # TODO(rich5317): We should probably read metadata values with the
        #       valid account, just to ensure that it is in fact not set.

        auth_token = self.valid_expired_token
        alt_client = ObjectStorageAPIClient(storage_url, auth_token)
        r = alt_client.update_container(container_name, headers=headers)
        self.assertEqual(r.status_code, 401,
                'should not set metadata with expired token')

        auth_token = self.bad_token
        alt_client = ObjectStorageAPIClient(storage_url, auth_token)
        r = alt_client.update_container(container_name, headers=headers)
        self.assertEqual(r.status_code, 401,
                'should not set metadata with bad token')

        auth_token = self.alt_client.auth_token
        alt_client = ObjectStorageAPIClient(storage_url, auth_token)
        r = alt_client.update_container(container_name, headers=headers)
        self.assertEqual(r.status_code, 401,
                'should not set metadata with cross token')

    def test_auth_obj_create(self):
        container_name = self.client.generate_unique_container_name()
        r = self.client.create_container(container_name)
        self.addCleanup(self.client.force_delete_containers,
                        [container_name])
        self.assertEqual(r.status_code, 201,
                'container should be created.')

        storage_url = self.client.storage_url
        object_name = self.client.generate_unique_object_name()
        object_data = 'Test object data'
        content_length = str(len(object_data))

        # TODO(rich5317): We should probably list objects with the
        #       valid account, just to ensure that it is in fact not created.

        alt_client = ObjectStorageAPIClient(storage_url,
                self.valid_expired_token)
        r = alt_client.set_storage_object(container_name,
                object_name,
                content_length=content_length,
                payload=object_data)
        self.assertEqual(r.status_code, 401,
                'should not create object with expired token')

        alt_client = ObjectStorageAPIClient(storage_url, self.bad_token)
        r = alt_client.set_storage_object(container_name,
                object_name,
                content_length=content_length,
                payload=object_data)
        self.assertEqual(r.status_code, 401,
                'should not create object with bad token')

        alt_client = ObjectStorageAPIClient(storage_url,
                self.alt_client.auth_token)
        r = alt_client.set_storage_object(container_name,
                object_name,
                content_length=content_length,
                payload=object_data)
        self.assertEqual(r.status_code, 401,
                'should not create object with cross token')

    def test_auth_obj_delete(self):
        container_name = self.client.generate_unique_container_name()
        r = self.client.create_container(container_name)
        self.addCleanup(self.client.force_delete_containers,
                        [container_name])
        self.assertEqual(r.status_code, 201,
                'container should be created.')

        object_name = self.client.generate_unique_object_name()
        object_data = 'Test object data'
        content_length = str(len(object_data))
        r = self.client.set_storage_object(
                container_name,
                object_name,
                content_length=content_length,
                payload=object_data)

        self.assertEqual(r.status_code, 201, 'object should be created.')

        storage_url = self.client.storage_url

        alt_client = ObjectStorageAPIClient(storage_url,
                self.valid_expired_token)
        r = alt_client.delete_storage_object(container_name, object_name)
        self.assertEqual(r.status_code, 401,
                'should not delete object with expired token')

        alt_client = ObjectStorageAPIClient(storage_url, self.bad_token)
        r = alt_client.delete_storage_object(container_name, object_name)
        self.assertEqual(r.status_code, 401,
                'should not delete object with bad token')

        alt_client = ObjectStorageAPIClient(storage_url,
                self.alt_client.auth_token)
        r = alt_client.delete_storage_object(container_name, object_name)
        self.assertEqual(r.status_code, 401,
                'should not create object with cross token')

    def test_auth_obj_copy(self):
        container_name = self.client.generate_unique_container_name()
        container_one = ''.join([container_name, '1'])
        container_two = ''.join([container_name, '2'])
        self.addCleanup(self.client.force_delete_containers,
                        [container_one, container_two])
        r = self.client.create_container(container_one)
        self.assertEqual(r.status_code, 201,
                'container one should be created.')
        r = self.client.create_container(container_two)
        self.assertEqual(r.status_code, 201,
                'container two should be created.')

        object_name = self.client.generate_unique_object_name()
        object_data = 'Test object data'
        content_length = str(len(object_data))
        r = self.client.set_storage_object(
                container_one,
                object_name,
                content_length=content_length,
                payload=object_data)
        self.assertEqual(r.status_code, 201,
                'object should be created.')

        storage_url = self.client.storage_url

        alt_client = ObjectStorageAPIClient(storage_url,
                self.valid_expired_token)
        r = alt_client.copy_storage_object(src_container=container_one,
                src_object=object_name, dst_container=container_two)
        self.assertEqual(r.status_code, 401,
                'should not copy object with expired token')

        alt_client = ObjectStorageAPIClient(storage_url, self.bad_token)
        r = alt_client.copy_storage_object(src_container=container_one,
                src_object=object_name, dst_container=container_two)
        self.assertEqual(r.status_code, 401,
                'should not copy object with bad token')

        alt_client = ObjectStorageAPIClient(storage_url,
                self.alt_client.auth_token)
        r = alt_client.copy_storage_object(src_container=container_one,
                src_object=object_name, dst_container=container_two)
        self.assertEqual(r.status_code, 401,
                'should not copy object with cross token')

    def test_auth_obj_get(self):
        container_name = self.client.generate_unique_container_name()
        self.addCleanup(self.client.force_delete_containers,
                        [container_name])
        r = self.client.create_container(container_name)
        self.assertEqual(r.status_code, 201,
                'container should be created.')

        object_name = self.client.generate_unique_object_name()
        object_data = 'Test object data'
        content_length = str(len(object_data))
        r = self.client.set_storage_object(
                container_name,
                object_name,
                content_length=content_length,
                payload=object_data)
        self.assertEqual(r.status_code, 201,
                'object should be created.')

        storage_url = self.client.storage_url

        alt_client = ObjectStorageAPIClient(storage_url,
                self.valid_expired_token)
        r = alt_client.get_storage_object(container_name, object_name)
        self.assertEqual(r.status_code, 401,
                'should not get object with expired token')

        alt_client = ObjectStorageAPIClient(storage_url, self.bad_token)
        r = alt_client.get_storage_object(container_name, object_name)
        self.assertEqual(r.status_code, 401,
                'should not get object with bad token')

        alt_client = ObjectStorageAPIClient(storage_url,
                self.alt_client.auth_token)
        r = alt_client.get_storage_object(container_name, object_name)
        self.assertEqual(r.status_code, 401,
                'should not get object with cross token')

    def test_auth_obj_get_meta(self):
        container_name = self.client.generate_unique_container_name()
        self.addCleanup(self.client.force_delete_containers,
                        [container_name])
        r = self.client.create_container(container_name)
        self.assertEqual(r.status_code, 201,
                'container should be created.')

        object_name = self.client.generate_unique_object_name()
        object_data = 'Test object data'
        content_length = str(len(object_data))
        r = self.client.set_storage_object(
                container_name,
                object_name,
                content_length=content_length,
                payload=object_data)
        self.assertEqual(r.status_code, 201,
                'object should be created.')

        storage_url = self.client.storage_url

        alt_client = ObjectStorageAPIClient(storage_url,
                self.valid_expired_token)

        r = alt_client.get_storage_object_metadata(container_name, object_name)
        self.assertEqual(r.status_code, 401,
                'should not get object metadata with expired token')
        for key in r.headers:
            self.assertEqual(key.startswith('x-object-meta'), False,
                    'should not return object metadata with expired token.')

        alt_client = ObjectStorageAPIClient(storage_url, self.bad_token)
        r = alt_client.get_storage_object_metadata(container_name, object_name)
        self.assertEqual(r.status_code, 401,
                'should not get object metadata with bad token')
        for key in r.headers:
            self.assertEqual(key.startswith('x-object-meta'), False,
                    'should not return object metadata with bad token.')

        alt_client = ObjectStorageAPIClient(storage_url,
                self.alt_client.auth_token)
        r = alt_client.get_storage_object_metadata(container_name, object_name)
        self.assertEqual(r.status_code, 401,
                'should not get object metadata with cross token')
        for key in r.headers:
            self.assertEqual(key.startswith('x-object-meta'), False,
                    'should not return object metadata with cross token.')

    def test_auth_obj_range(self):
        container_name = self.client.generate_unique_container_name()
        self.addCleanup(self.client.force_delete_containers,
                        [container_name])
        r = self.client.create_container(container_name)
        self.assertEqual(r.status_code, 201,
                'container should be created.')

        object_name = self.client.generate_unique_object_name()
        object_data = 'Test object data'
        content_length = str(len(object_data))
        r = self.client.set_storage_object(
                container_name,
                object_name,
                content_length=content_length,
                payload=object_data)
        self.assertEqual(r.status_code, 201,
                'object should be created.')

        storage_url = self.client.storage_url
        headers = {'Range': 'bytes=5-6'}

        alt_client = ObjectStorageAPIClient(storage_url,
                self.valid_expired_token)
        r = alt_client.get_storage_object_metadata(container_name, object_name,
                headers=headers)
        self.assertEqual(r.status_code, 401,
                'should not get partial object with expired token')

        alt_client = ObjectStorageAPIClient(storage_url, self.bad_token)
        r = alt_client.get_storage_object_metadata(container_name, object_name,
                headers=headers)
        self.assertEqual(r.status_code, 401,
                'should not get partial object with bad token')

        alt_client = ObjectStorageAPIClient(storage_url,
                self.alt_client.auth_token)
        r = alt_client.get_storage_object_metadata(container_name, object_name,
                headers=headers)
        self.assertEqual(r.status_code, 401,
                'should not get partial object with cross token')

    def test_auth_obj_etag(self):
        container_name = self.client.generate_unique_container_name()
        self.addCleanup(self.client.force_delete_containers,
                        [container_name])
        r = self.client.create_container(container_name)
        self.assertEqual(r.status_code, 201,
                'container should be created.')

        object_name = self.client.generate_unique_object_name()
        object_data = 'Test object data'
        content_length = str(len(object_data))
        r = self.client.set_storage_object(
                container_name,
                object_name,
                content_length=content_length,
                payload=object_data)
        self.assertEqual(r.status_code, 201,
                'object should be created.')

        storage_url = self.client.storage_url

        alt_client = ObjectStorageAPIClient(storage_url,
                self.valid_expired_token)
        r = alt_client.get_storage_object_metadata(container_name, object_name)
        self.assertEqual(r.status_code, 401,
                'should not get object metadata with expired token')
        self.assertEquals('etag' in r.headers, False,
                'should not contian etag header with expired token')

        alt_client = ObjectStorageAPIClient(storage_url, self.bad_token)
        r = alt_client.get_storage_object_metadata(container_name, object_name)
        self.assertEqual(r.status_code, 401,
                'should not get object metadata with bad token')
        self.assertEquals('etag' in r.headers, False,
                'should not contian etag header with bad token')

        alt_client = ObjectStorageAPIClient(storage_url,
                self.alt_client.auth_token)
        r = alt_client.get_storage_object_metadata(container_name, object_name)
        self.assertEqual(r.status_code, 401,
                'should not get object metadata with cross token')
        self.assertEquals('etag' in r.headers, False,
                'should not contian etag header with cross token')

    def test_auth_obj_del_after_x_seconds(self):
        container_name = self.client.generate_unique_container_name()
        self.addCleanup(self.client.force_delete_containers,
                        [container_name])
        r = self.client.create_container(container_name)
        self.assertEqual(r.status_code, 201,
                'container should be created.')

        object_name = self.client.generate_unique_object_name()
        object_data = 'Test object data'
        content_length = str(len(object_data))
        r = self.client.set_storage_object(
                container_name,
                object_name,
                content_length=content_length,
                payload=object_data)

        storage_url = self.client.storage_url

        headers = {'X-Delete-After': '10'}

        alt_client = ObjectStorageAPIClient(storage_url,
                self.valid_expired_token)
        r = alt_client.get_storage_object_metadata(container_name, object_name,
                headers=headers)
        self.assertEqual(r.status_code, 401,
                'should not set delete after with expired token')

        alt_client = ObjectStorageAPIClient(storage_url, self.bad_token)
        r = alt_client.get_storage_object_metadata(container_name, object_name,
                headers=headers)
        self.assertEqual(r.status_code, 401,
                'should not set delete after with bad token')

        alt_client = ObjectStorageAPIClient(storage_url,
                self.alt_client.auth_token)
        r = alt_client.get_storage_object_metadata(container_name, object_name,
                headers=headers)
        self.assertEqual(r.status_code, 401,
                'should not set delete after with cross token')

        t = timegm(time.gmtime())
        headers = {'X-Delete-At': str(t + 100)}

        alt_client = ObjectStorageAPIClient(storage_url,
                self.valid_expired_token)
        r = alt_client.get_storage_object_metadata(container_name, object_name,
                headers=headers)
        self.assertEqual(r.status_code, 401,
                'should not set delete at with expired token')

        alt_client = ObjectStorageAPIClient(storage_url, self.bad_token)
        r = alt_client.get_storage_object_metadata(container_name, object_name,
                headers=headers)
        self.assertEqual(r.status_code, 401,
                'should not set delete at with bad token')

        alt_client = ObjectStorageAPIClient(storage_url,
                self.alt_client.auth_token)
        r = alt_client.get_storage_object_metadata(container_name, object_name,
                headers=headers)
        self.assertEqual(r.status_code, 401,
                'should not set delete at with cross token')

    def test_auth_obj_update(self):
        container_name = self.client.generate_unique_container_name()
        self.addCleanup(self.client.force_delete_containers,
                        [container_name])
        r = self.client.create_container(container_name)
        self.assertEqual(r.status_code, 201,
                'container should be created.')

        object_name = self.client.generate_unique_object_name()
        object_data = 'Test object data'
        content_length = str(len(object_data))
        r = self.client.set_storage_object(
                container_name,
                object_name,
                content_length=content_length,
                payload=object_data)

        storage_url = self.client.storage_url

        object_data = 'New File Data'
        content_length = str(len(object_data))

        alt_client = ObjectStorageAPIClient(storage_url,
                self.valid_expired_token)
        r = alt_client.set_storage_object(container_name,
                object_name,
                content_length=content_length,
                payload=object_data)
        self.assertEqual(r.status_code, 401,
                'should not update storage object with expired token')

        alt_client = ObjectStorageAPIClient(storage_url, self.bad_token)
        r = alt_client.set_storage_object(container_name,
                object_name,
                content_length=content_length,
                payload=object_data)
        self.assertEqual(r.status_code, 401,
                'should not update storage object with bad token')

        alt_client = ObjectStorageAPIClient(storage_url,
                self.alt_client.auth_token)
        r = alt_client.set_storage_object(container_name,
                object_name,
                content_length=content_length,
                payload=object_data)
        self.assertEqual(r.status_code, 401,
                'should not update storage object with cross token')

    def test_auth_obj_update_meta(self):
        container_name = self.client.generate_unique_container_name()
        r = self.client.create_container(container_name)
        self.addCleanup(self.client.force_delete_containers,
                        [container_name])
        self.assertEqual(r.status_code, 201,
                'container should be created.')

        object_name = self.client.generate_unique_object_name()
        object_data = 'Test object data'
        content_length = str(len(object_data))
        r = self.client.set_storage_object(
                container_name,
                object_name,
                content_length=content_length,
                payload=object_data)

        storage_url = self.client.storage_url
        headers = {'X-Container-Meta-hurf': 'durf'}
        # TODO(rich5317): We should probably read metadata values with the
        #       valid account, just to ensure that it is in fact not set.

        alt_client = ObjectStorageAPIClient(storage_url,
                self.valid_expired_token)
        r = alt_client.set_storage_object(container_name,
                object_name, headers=headers)
        self.assertEqual(r.status_code, 401,
                'should not update object metadata with expired token')

        alt_client = ObjectStorageAPIClient(storage_url, self.bad_token)
        r = alt_client.set_storage_object(container_name,
                object_name, headers=headers)
        self.assertEqual(r.status_code, 401,
                'should not update object metadata with bad token')

        alt_client = ObjectStorageAPIClient(storage_url,
                self.alt_client.auth_token)
        r = alt_client.set_storage_object(container_name,
                object_name, headers=headers)
        self.assertEqual(r.status_code, 401,
                'should not update object metadata with cross token')

    def test_auth_container_static_web_index_file(self):
        container_name = self.client.generate_unique_container_name()
        r = self.client.create_container(container_name)
        self.addCleanup(self.client.force_delete_containers,
                        [container_name])
        self.assertEqual(r.status_code, 201,
                'container should be created.')

        storage_url = self.client.storage_url
        headers = {'X-Container-Meta-Web-Index': 'index.html'}
        # TODO(rich5317): We should probably read metadata values with the
        #       valid account, just to ensure that it is in fact not set.

        alt_client = ObjectStorageAPIClient(storage_url,
                self.valid_expired_token)
        r = alt_client.update_container(container_name, headers=headers)
        self.assertEqual(r.status_code, 401,
                'should not set web index with expired token')

        alt_client = ObjectStorageAPIClient(storage_url, self.bad_token)
        r = alt_client.update_container(container_name, headers=headers)
        self.assertEqual(r.status_code, 401,
                'should not set web index with bad token')

        alt_client = ObjectStorageAPIClient(storage_url,
                self.alt_client.auth_token)
        r = alt_client.update_container(container_name, headers=headers)
        self.assertEqual(r.status_code, 401,
                'should not set web index with cross token')

    def test_auth_container_static_web_error_file(self):
        container_name = self.client.generate_unique_container_name()
        r = self.client.create_container(container_name)
        self.addCleanup(self.client.force_delete_containers,
                        [container_name])
        self.assertEqual(r.status_code, 201,
                'container should be created.')

        storage_url = self.client.storage_url
        headers = {'X-Container-Meta-Web-Error': 'error.html'}
        # TODO(rich5317): We should probably read metadata values with the
        #       valid account, just to ensure that it is in fact not set.

        alt_client = ObjectStorageAPIClient(storage_url,
                self.valid_expired_token)
        r = alt_client.update_container(container_name, headers=headers)
        self.assertEqual(r.status_code, 401,
                'should not set error file with expired token')

        alt_client = ObjectStorageAPIClient(storage_url, self.bad_token)
        r = alt_client.update_container(container_name, headers=headers)
        self.assertEqual(r.status_code, 401,
                'should not set error file with bad token')

        alt_client = ObjectStorageAPIClient(storage_url,
                self.alt_client.auth_token)
        r = alt_client.update_container(container_name, headers=headers)
        self.assertEqual(r.status_code, 401,
                'should not set error file with cross token')

    def test_auth_container_static_web_css_file(self):
        container_name = self.client.generate_unique_container_name()
        r = self.client.create_container(container_name)
        self.addCleanup(self.client.force_delete_containers,
                        [container_name])
        self.assertEqual(r.status_code, 201,
                'container should be created.')

        storage_url = self.client.storage_url
        headers = {'X-Container-Meta-Web-Listings-CSS': 'default.css'}
        # TODO(rich5317): We should probably read metadata values with the
        #       valid account, just to ensure that it is in fact not set.

        alt_client = ObjectStorageAPIClient(storage_url,
                self.valid_expired_token)
        r = alt_client.update_container(container_name, headers=headers)
        self.assertEqual(r.status_code, 401,
                'should not set css file with expired token')

        alt_client = ObjectStorageAPIClient(storage_url, self.bad_token)
        r = alt_client.update_container(container_name, headers=headers)
        self.assertEqual(r.status_code, 401,
                'should not set css file with bad token')

        alt_client = ObjectStorageAPIClient(storage_url,
                self.alt_client.auth_token)
        r = alt_client.update_container(container_name, headers=headers)
        self.assertEqual(r.status_code, 401,
                'should not set css file with cross token')

    def test_auth_container_enable_static_web_listings(self):
        container_name = self.client.generate_unique_container_name()
        r = self.client.create_container(container_name)
        self.addCleanup(self.client.force_delete_containers,
                        [container_name])
        self.assertEqual(r.status_code, 201,
                'container should be created.')

        storage_url = self.client.storage_url
        headers = {'X-Container-Meta-Web-Listings': 'true'}
        # TODO(rich5317): We should probably read metadata values with the
        #       valid account, just to ensure that it is in fact not set.

        alt_client = ObjectStorageAPIClient(storage_url,
                self.valid_expired_token)
        r = alt_client.update_container(container_name, headers=headers)
        self.assertEqual(r.status_code, 401,
                'should not enable listings with expired token')

        alt_client = ObjectStorageAPIClient(storage_url, self.bad_token)
        r = alt_client.update_container(container_name, headers=headers)
        self.assertEqual(r.status_code, 401,
                'should not enable listings with bad token')

        alt_client = ObjectStorageAPIClient(storage_url,
                self.alt_client.auth_token)
        r = alt_client.update_container(container_name, headers=headers)
        self.assertEqual(r.status_code, 401,
                'should not enable listings with cross token')

    def test_auth_container_disable_static_web_listing(self):
        container_name = self.client.generate_unique_container_name()
        r = self.client.create_container(container_name)
        self.addCleanup(self.client.force_delete_containers,
                        [container_name])
        self.assertEqual(r.status_code, 201,
                'container should be created.')

        storage_url = self.client.storage_url
        headers = {'X-Container-Meta-Web-Listings': 'false'}
        # TODO(rich5317): We should probably read metadata values with the
        #       valid account, just to ensure that it is in fact not set.

        alt_client = ObjectStorageAPIClient(storage_url,
                self.valid_expired_token)
        r = alt_client.update_container(container_name, headers=headers)
        self.assertEqual(r.status_code, 401,
                'should not disable listings with expired token')

        alt_client = ObjectStorageAPIClient(storage_url, self.bad_token)
        r = alt_client.update_container(container_name, headers=headers)
        self.assertEqual(r.status_code, 401,
                'should not disable listings with bad token')

        alt_client = ObjectStorageAPIClient(storage_url,
                self.alt_client.auth_token)
        r = alt_client.update_container(container_name, headers=headers)
        self.assertEqual(r.status_code, 401,
                'should not disable listings with cross token')

    def test_auth_container_enable_static_web_anon_request(self):
        container_name = self.client.generate_unique_container_name()
        r = self.client.create_container(container_name)
        self.addCleanup(self.client.force_delete_containers,
                        [container_name])
        self.assertEqual(r.status_code, 201,
                'container should be created.')

        storage_url = self.client.storage_url
        headers = {'X-Container-Meta-Web-Mode': 'true'}
        # TODO(rich5317): We should probably read metadata values with the
        #       valid account, just to ensure that it is in fact not set.

        alt_client = ObjectStorageAPIClient(storage_url,
                self.valid_expired_token)
        r = alt_client.update_container(container_name, headers=headers)
        self.assertEqual(r.status_code, 401,
                'should not enable anon with expired token')

        alt_client = ObjectStorageAPIClient(storage_url, self.bad_token)
        r = alt_client.update_container(container_name, headers=headers)
        self.assertEqual(r.status_code, 401,
                'should not enable anon with bad token')

        alt_client = ObjectStorageAPIClient(storage_url,
                self.alt_client.auth_token)
        r = alt_client.update_container(container_name, headers=headers)
        self.assertEqual(r.status_code, 401,
                'should not enable anon with cross token')

    def test_auth_container_disable_static_web_anon_request(self):
        container_name = self.client.generate_unique_container_name()
        r = self.client.create_container(container_name)
        self.addCleanup(self.client.force_delete_containers,
                        [container_name])
        self.assertEqual(r.status_code, 201,
                'container should be created.')

        storage_url = self.client.storage_url
        headers = {'X-Container-Meta-Web-Mode': 'false'}
        # TODO(rich5317): We should probably read metadata values with the
        #       valid account, just to ensure that it is in fact not set.

        alt_client = ObjectStorageAPIClient(storage_url,
                self.valid_expired_token)
        r = alt_client.update_container(container_name, headers=headers)
        self.assertEqual(r.status_code, 401,
                'should not disable anon with expired token')

        alt_client = ObjectStorageAPIClient(storage_url, self.bad_token)
        r = alt_client.update_container(container_name, headers=headers)
        self.assertEqual(r.status_code, 401,
                'should not disable anon with bad token')

        alt_client = ObjectStorageAPIClient(storage_url,
                self.alt_client.auth_token)
        r = alt_client.update_container(container_name, headers=headers)
        self.assertEqual(r.status_code, 401,
                'should not disable anon with cross token')
