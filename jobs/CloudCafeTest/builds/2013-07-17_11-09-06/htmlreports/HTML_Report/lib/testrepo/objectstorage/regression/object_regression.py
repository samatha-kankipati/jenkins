"""
4.3 Storage Object Services Regression Tests
"""
import time
import unittest
import datetime
import time

from testrepo.common.testfixtures.object_storage_fixture \
        import ObjectStorageTestFixture


class ObjectRegressionTest(ObjectStorageTestFixture):
    """4.3.2.7. Expiring Objects with the X-Delete-After
       and X-Delete-At Headers"""

    @unittest.skip('call to sleep in test causes slow execution.')
    def test_object_creation_with_scheduled_expiration(self):
        container_name = self.client.generate_unique_container_name()
        self.client.create_container(container_name)
        self.addCleanup(self.client.force_delete_containers, [container_name])

        """Create an object and set its X-Delete-At header"""
        object_name = self.client.generate_unique_object_name()
        object_data = 'Test data'
        content_length = str(len(object_data))

        delta = datetime.timedelta(minutes=5)
        expire_datetime = datetime.datetime.now() + delta
        expire_timestamp = str(int(time.mktime(expire_datetime.timetuple())))
        headers = {'X-Delete-At': expire_timestamp}
        r = self.client.set_storage_object(container_name, object_name,
                content_length=content_length, payload=object_data,
                headers=headers)
        self.assertEqual(r.status_code, 201,
                'should create an object scheduled to expire')

        """Verify the delete after header is set."""
        r = self.client.get_storage_object_metadata(container_name,
                object_name)
        self.assertTrue(r.ok, 'should return object metadata.')
        self.assertTrue('x-delete-at' in r.headers,
                'headers should contain X-Delete-At.')
        self.assertEqual(r.headers['x-delete-at'], expire_timestamp,
                'X-Delete-At should be set correctly.')

        """Verify the object is accessable."""
        r = self.client.get_storage_object(container_name, object_name)
        self.assertEqual(r.status_code, 200, 'should return object.')

        """Wait till after the object should be expired."""
        time.sleep(delta.seconds)

        """Verify the object was removed."""
        r = self.client.get_storage_object(container_name, object_name)
        self.assertEqual(r.status_code, 404, 'should not return object.')

        """Verify the objects metadata is not returned."""
        r = self.client.get_storage_object_metadata(container_name,
                object_name)
        self.assertEqual(r.status_code, 404,
                'should not return object metadata.')

        """Verify partial objects can not be downloaded."""
        headers = {'Range': 'bytes=5-'}
        r = self.client.get_storage_object(container_name, object_name,
                headers=headers)
        self.assertEqual(r.status_code, 404,
                'should not retrieve a partial object')

        """Verify the object can not be copied (HTTP COPY)."""
        new_object = ''.join([object_name, '_copy'])
        r = self.client.copy_storage_object(container_name, object_name,
                dst_object=new_object)
        self.assertEqual(r.status_code, 404, 'should not copy object')

        """Verify the object can not be copied (X-Copy-From Header)."""
        copied_object_name = ''.join([object_name, '.copy'])
        source = ''.join([container_name, '/', object_name])
        headers = {'X-Copy-From': source}
        r = self.client.set_storage_object(container_name, copied_object_name,
                content_length=0, payload='', headers=headers)
        self.assertEqual(r.status_code, 404,
                'x-copy-from should not copy object using')

        """Verify metadata can not be set for the object"""
        metadata = {'foo': 'bar'}
        r = self.client.set_storage_object_metadata(container_name,
                object_name, metadata)
        self.assertEqual(r.status_code, 404, 'should not set metadata')

    @unittest.skip('call to sleep in test causes slow execution.')
    def test_object_creation_with_delete_after_header(self):
        container_name = self.client.generate_unique_container_name()
        self.client.create_container(container_name)
        self.addCleanup(self.client.force_delete_containers, [container_name])

        """Create an object and set its X-Delete-After header"""
        object_name = self.client.generate_unique_object_name()
        object_data = 'Test data'
        content_length = str(len(object_data))

        delta = datetime.timedelta(minutes=5)
        headers = {'X-Delete-After': str(delta.seconds)}
        r = self.client.set_storage_object(container_name, object_name,
                content_length=content_length, payload=object_data,
                headers=headers)
        self.assertEqual(r.status_code, 201,
                'should create an object scheduled to expire')

        """Verify the delete after header is set."""
        r = self.client.get_storage_object_metadata(container_name,
                object_name)
        self.assertTrue(r.ok, 'should return object metadata.')
        self.assertTrue('x-delete-at' in r.headers,
                'headers should contain X-Delete-At.')
        # TODO(rich5317): Test that X-Delete-At is within some delta of
        #   The time that the HTTP response came back + the time till the
        #   object expires.

        """Verify the object is accessable."""
        r = self.client.get_storage_object(container_name, object_name)
        self.assertEqual(r.status_code, 200, 'should return object.')

        """Wait till after the object should be expired."""
        time.sleep(delta.seconds)

        """Verify the object was removed."""
        r = self.client.get_storage_object(container_name, object_name)
        self.assertEqual(r.status_code, 404, 'should not return object.')

        """Verify the objects metadata is not returned."""
        r = self.client.get_storage_object_metadata(container_name,
                object_name)
        self.assertEqual(r.status_code, 404,
                'should not return object metadata.')

        """Verify partial objects can not be downloaded."""
        headers = {'Range': 'bytes=5-'}
        r = self.client.get_storage_object(container_name, object_name,
                headers=headers)
        self.assertEqual(r.status_code, 404,
                'should not retrieve a partial object')

        """Verify the object can not be copied (HTTP COPY)."""
        new_object = ''.join([object_name, '_copy'])
        r = self.client.copy_storage_object(container_name, object_name,
                dst_object=new_object)
        self.assertEqual(r.status_code, 404, 'should not copy object')

        """Verify the object can not be copied (X-Copy-From Header)."""
        copied_object_name = ''.join([object_name, '.copy'])
        source = ''.join([container_name, '/', object_name])
        headers = {'X-Copy-From': source}
        r = self.client.set_storage_object(container_name, copied_object_name,
                content_length=0, payload='', headers=headers)
        self.assertEqual(r.status_code, 404,
                'x-copy-from should not copy object using')

        """Verify metadata can not be set for the object"""
        metadata = {'foo': 'bar'}
        r = self.client.set_storage_object_metadata(container_name,
                object_name, metadata)
        self.assertEqual(r.status_code, 404, 'should not set metadata')

    @unittest.skip('call to sleep in test causes slow execution.')
    def test_container_listing_with_scheduled_object_expiration(self):
        container_name = self.client.generate_unique_container_name()
        self.client.create_container(container_name)
        self.addCleanup(self.client.force_delete_containers, [container_name])

        """Create an object and set its X-Delete-At header"""
        object_name = self.client.generate_unique_object_name()
        object_data = 'Test data'
        content_length = str(len(object_data))

        delta = datetime.timedelta(minutes=5)
        expire_datetime = datetime.datetime.now() + delta
        expire_timestamp = str(int(time.mktime(expire_datetime.timetuple())))
        headers = {'X-Delete-At': expire_timestamp}
        r = self.client.set_storage_object(container_name, object_name,
                content_length=content_length, payload=object_data,
                headers=headers)
        self.assertEqual(r.status_code, 201,
                'should create an object scheduled to expire')

        """Verify the delete after header is set."""
        r = self.client.get_storage_object_metadata(container_name,
                object_name)
        self.assertTrue(r.ok, 'should return object metadata.')
        self.assertTrue('x-delete-at' in r.headers,
                'headers should contain X-Delete-At.')
        self.assertEqual(r.headers['x-delete-at'], expire_timestamp,
                'X-Delete-At should be set correctly.')

        """Verify the object is accessable."""
        r = self.client.get_storage_object(container_name, object_name)
        self.assertEqual(r.status_code, 200, 'should return object.')

        """Wait till after the object should be expired."""
        time.sleep(delta.seconds)

        """Verify the object was removed from the container listing."""
        timeout = datetime.datetime.now() + datetime.timedelta(hours=1)
        current_time = datetime.datetime.now()
        while current_time < timeout:
            r = self.client.list_objects(container_name)
            if object_name not in r.content:
                self.assertTrue(object_name not in r.content,
                        'should not return object.')
                return

            time.sleep(datetime.timedelta(minutes=5).seconds)
            current_time = datetime.datetime.now()

        self.assertTrue(object_name not in r.content,
                'container listing should not return object.')
