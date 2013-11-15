"""
Tests Container Quotas:
http://docs.openstack.org/developer/swift/misc.html#module-swift.common.middleware.container_quotas
"""
import hashlib
import math
import os
import re
import tarfile
import time

from ccengine.common.tools.datatools import CLOUDCAFE_DATA_DIRECTORY
from ccengine.common.tools.datatools import CLOUDCAFE_TEMP_DIRECTORY
from testrepo.common.testfixtures.object_storage_fixture \
    import ObjectStorageTestFixture

# TODO(rich5317): This should be set in a config
CONTAINER_TTL = 61


class BulkContainerQuotasSmokeTest(ObjectStorageTestFixture):
    """
    The container_quotas middleware implements simple quotas that can be
    imposed on swift containers by a user with the ability to set container
    metadata
    """

    def test_container_with_quota_bytes_set(self):
        """
        Verify that if a quota in bytes is set, that a user can add exactly
        up to the number of bytes to the container.
        """
        container_name = \
            self.client.generate_unique_container_name('container_quotas')
        headers = {'X-Container-Meta-Quota-Bytes': '16'}
        self.client.create_container(container_name, headers=headers)
        self.addCleanup(self.client.force_delete_containers, [container_name])

        object_name = self.client.generate_unique_object_name()
        object_data = '12345678'
        content_length = str(len(object_data))
        r = self.client.set_storage_object(
            container_name, object_name, content_length=content_length,
            payload=object_data)
        self.assertEqual(r.status_code, 201, 'should create first object.')

        time.sleep(CONTAINER_TTL)

        object_name = self.client.generate_unique_object_name()
        object_data = '12345678'
        content_length = str(len(object_data))
        r = self.client.set_storage_object(
            container_name, object_name, content_length=content_length,
            payload=object_data)
        self.assertEqual(r.status_code, 201, 'should create second object.')

    def test_container_with_quota_bytes_exceeded(self):
        """
        Verify that when the quota in bytes has been exceeded, that it
        prevents further objects from being added.
        """
        container_name = \
            self.client.generate_unique_container_name('container_quotas')
        headers = {'X-Container-Meta-Quota-Bytes': '16'}
        self.client.create_container(container_name, headers=headers)
        self.addCleanup(self.client.force_delete_containers, [container_name])

        object_name = self.client.generate_unique_object_name()
        object_data = '12345678'
        content_length = str(len(object_data))
        r = self.client.set_storage_object(
            container_name, object_name, content_length=content_length,
            payload=object_data)
        self.assertEqual(r.status_code, 201, 'should create first object.')

        object_name = self.client.generate_unique_object_name()
        object_data = '12345678'
        content_length = str(len(object_data))
        r = self.client.set_storage_object(
            container_name, object_name, content_length=content_length,
            payload=object_data)
        self.assertEqual(r.status_code, 201, 'should create second object.')

        time.sleep(CONTAINER_TTL)

        object_name = self.client.generate_unique_object_name()
        object_data = '12345678'
        content_length = str(len(object_data))
        r = self.client.set_storage_object(
            container_name, object_name, content_length=content_length,
            payload=object_data)
        self.assertEqual(
            r.status_code, 413, 'should not create object over quota.')

    def test_container_with_quota_bytes_previously_exceeded(self):
        """
        Verify that a container that previously had its quota in bytes exceeded
        will allow an object to be added.
        """
        container_name = \
            self.client.generate_unique_container_name('container_quotas')
        headers = {'X-Container-Meta-Quota-Bytes': '16'}
        self.client.create_container(container_name, headers=headers)
        self.addCleanup(self.client.force_delete_containers, [container_name])

        object_name = self.client.generate_unique_object_name()
        object_data = '12345678'
        content_length = str(len(object_data))
        r = self.client.set_storage_object(
            container_name, object_name, content_length=content_length,
            payload=object_data)
        self.assertEqual(r.status_code, 201, 'should create first object.')

        object_name = self.client.generate_unique_object_name()
        object_data = '12345678'
        content_length = str(len(object_data))
        r = self.client.set_storage_object(
            container_name, object_name, content_length=content_length,
            payload=object_data)
        self.assertEqual(r.status_code, 201, 'should create second object.')

        object_to_delete = object_name

        time.sleep(CONTAINER_TTL)

        object_name = self.client.generate_unique_object_name()
        object_data = '12345678'
        content_length = str(len(object_data))
        r = self.client.set_storage_object(
            container_name, object_name, content_length=content_length,
            payload=object_data)
        self.assertEqual(
            r.status_code, 413, 'should not create object over quota.')

        r = self.client.delete_storage_object(container_name, object_to_delete)
        self.assertEqual(r.status_code, 204, 'object should be deleted.')

        time.sleep(CONTAINER_TTL)

        object_name = self.client.generate_unique_object_name()
        object_data = '12345678'
        content_length = str(len(object_data))
        r = self.client.set_storage_object(
            container_name, object_name, content_length=content_length,
            payload=object_data)
        self.assertEqual(r.status_code, 201, 'should create third object.')

    def test_container_with_quota_count_set(self):
        """
        Verify that if a quota count is set, that a user can add exactly
        up to the number of bytes to the container.
        """
        quota_count = 10

        container_name = \
            self.client.generate_unique_container_name('container_quotas')
        headers = {'X-Container-Meta-Quota-Count': str(quota_count)}
        self.client.create_container(container_name, headers=headers)
        self.addCleanup(self.client.force_delete_containers, [container_name])

        objects_list = ['object{0}'.format(x) for x in range(
            0, quota_count - 1)]

        self.client.create_bulk_objects(container_name, objects_list)

        time.sleep(CONTAINER_TTL)

        object_name = 'last'
        object_data = 'object data'
        content_length = str(len(object_data))
        r = self.client.set_storage_object(
            container_name, object_name, content_length=content_length,
            payload=object_data)
        self.assertEqual(r.status_code, 201, 'should create second object.')

    def test_container_with_quota_count_exceeded(self):
        """
        Verify that when the quota count has been exceeded, that it
        prevents further objects from being added.
        """
        quota_count = 10

        container_name = \
            self.client.generate_unique_container_name('container_quotas')
        headers = {'X-Container-Meta-Quota-Count': str(quota_count)}
        self.client.create_container(container_name, headers=headers)
        self.addCleanup(self.client.force_delete_containers, [container_name])

        objects_list = ['object{0}'.format(x) for x in range(0, quota_count)]

        self.client.create_bulk_objects(container_name, objects_list)

        time.sleep(CONTAINER_TTL)

        object_name = 'last'
        object_data = 'object data'
        content_length = str(len(object_data))
        r = self.client.set_storage_object(
            container_name, object_name, content_length=content_length,
            payload=object_data)
        self.assertEqual(
            r.status_code, 413, 'should not create object over quota.')

    def test_container_with_quota_count_previously_exceeded(self):
        """
        Verify that a container that previously had its quota count exceeded
        will allow an object to be added.
        """
        quota_count = 10

        container_name = \
            self.client.generate_unique_container_name('container_quotas')
        headers = {'X-Container-Meta-Quota-Count': str(quota_count)}
        self.client.create_container(container_name, headers=headers)
        self.addCleanup(self.client.force_delete_containers, [container_name])

        objects_list = ['object{0}'.format(x) for x in range(0, quota_count)]

        self.client.create_bulk_objects(container_name, objects_list)

        time.sleep(CONTAINER_TTL)

        object_name = 'last'
        object_data = 'object data'
        content_length = str(len(object_data))
        r = self.client.set_storage_object(
            container_name, object_name, content_length=content_length,
            payload=object_data)
        self.assertEqual(
            r.status_code, 413, 'should not create object over quota.')

        r = self.client.delete_storage_object(container_name, objects_list[0])
        self.assertEqual(r.status_code, 204, 'object should be deleted.')

        time.sleep(CONTAINER_TTL)

        object_name = 'last'
        object_data = 'object data'
        content_length = str(len(object_data))
        r = self.client.set_storage_object(
            container_name, object_name, content_length=content_length,
            payload=object_data)
        self.assertEqual(r.status_code, 201, 'should create second object.')
