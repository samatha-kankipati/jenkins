import calendar
import datetime
import hashlib
import os.path
import time
import unittest
import zlib

from testrepo.common.testfixtures.object_storage_fixture \
        import ObjectStorageTestFixture


#these need to be moved to a config
CONTENT_TYPE_TEXT = 'text/plain; charset=UTF-8'


"""4.3 Storage Object Services Smoke Tests"""


class LogDeliveryObjectSmokeTest(ObjectStorageTestFixture):
    @classmethod
    def setUpClass(cls):
        super(LogDeliveryObjectSmokeTest, cls).setUpClass()

        cls.container_name = cls.client.generate_unique_container_name(
                '_log_delivery_object_smoke_tests')
        metadata = {'Access-Log-Delivery': 'True'}
        cls.client.create_container(cls.container_name,
                metadata=metadata)
        cls.fixture_log.info('Container created for object smoke log ' \
                'delivery tests(%s)' % cls.container_name)

    # Containers can not be deleted or access logs will not be generated

    """4.3.1. Retrieve Object"""
    def test_object_retrieval_with_valid_object_name(self):
        container_name = self.container_name

        object_name = self.client.generate_unique_object_name()
        object_data = 'Test file data'
        content_length = str(len(object_data))
        self.client.set_storage_object(
                container_name,
                object_name,
                content_length=content_length,
                content_type=CONTENT_TYPE_TEXT,
                payload=object_data)

        r = self.client.get_storage_object(container_name,
                object_name)
        self.assertEqual(r.status_code, 200, 'should return object.')

    def test_object_retrieval_with_if_match_header(self):
        container_name = self.container_name

        object_name = self.client.generate_unique_object_name()
        object_data = 'Test file data'
        content_length = str(len(object_data))
        etag = self.filetools.get_md5_hash(object_data)
        headers = {'Etag': etag}
        self.client.set_storage_object(
                container_name,
                object_name,
                content_length=content_length,
                content_type=CONTENT_TYPE_TEXT,
                payload=object_data,
                headers=headers)

        headers = {'If-Match': etag}
        r = self.client.get_storage_object(container_name, object_name,
                headers=headers)
        self.assertEqual(r.status_code, 200, 'should retrieve object')

    def test_object_retrieval_with_if_none_match_header(self):
        container_name = self.container_name

        object_name = self.client.generate_unique_object_name()
        object_data = 'Test file data'
        content_length = str(len(object_data))
        etag = self.filetools.get_md5_hash(object_data)
        headers = {'Etag': etag}
        self.client.set_storage_object(
                container_name,
                object_name,
                content_length=content_length,
                content_type=CONTENT_TYPE_TEXT,
                payload=object_data,
                headers=headers)

        headers = {'If-None-Match': 'grok'}
        r = self.client.get_storage_object(container_name, object_name,
                headers=headers)
        self.assertEqual(r.status_code, 200, 'should retrieve object')

    def test_object_retrieval_with_if_modified_since_header(self):
        container_name = self.container_name

        object_name = self.client.generate_unique_object_name()
        object_data = 'Test file data'
        content_length = str(len(object_data))
        self.client.set_storage_object(
                container_name,
                object_name,
                content_length=content_length,
                content_type=CONTENT_TYPE_TEXT,
                payload=object_data)

        headers = {'If-Unmodified-Since': 'Fri, 17 Aug 3000 18:44:42 GMT'}
        r = self.client.get_storage_object(container_name,
                object_name,
                headers=headers)
        self.assertEqual(r.status_code, 200, 'should retrieve object')

    def test_object_retrieval_with_if_unmodified_since_header(self):
        container_name = self.container_name

        object_name = self.client.generate_unique_object_name()
        object_data = 'Test file data'
        content_length = str(len(object_data))
        self.client.set_storage_object(
                container_name,
                object_name,
                content_length=content_length,
                content_type=CONTENT_TYPE_TEXT,
                payload=object_data)

        headers = {'If-Modified-Since': 'Fri, 17 Aug 2001 18:44:42 GMT'}
        r = self.client.get_storage_object(container_name, object_name,
                headers=headers)
        self.assertEqual(r.status_code, 200, 'should retrieve object')

    def test_partial_object_retrieval_with_start_range(self):
        container_name = self.container_name

        object_name = self.client.generate_unique_object_name()
        object_data = 'Test file data'
        content_length = str(len(object_data))
        self.client.set_storage_object(
                container_name,
                object_name,
                content_length=content_length,
                content_type=CONTENT_TYPE_TEXT,
                payload=object_data)

        headers = {'Range': 'bytes=5-'}
        r = self.client.get_storage_object(container_name,
                object_name,
                headers=headers)
        self.assertEqual(r.status_code, 206,
                'should retrieve a partial object from the middle to the end')

    def test_partial_object_retrieval_with_end_range(self):
        container_name = self.container_name

        object_name = self.client.generate_unique_object_name()
        object_data = 'Test file data'
        content_length = str(len(object_data))
        self.client.set_storage_object(
                container_name,
                object_name,
                content_length=content_length,
                content_type=CONTENT_TYPE_TEXT,
                payload=object_data)

        headers = {'Range': 'bytes=-4'}
        r = self.client.get_storage_object(container_name, object_name,
                headers=headers)
        self.assertEqual(r.status_code, 206,
                'should retrieve a partial object from the end to the middle')

    def test_partial_object_retrieval_with_range(self):
        container_name = self.container_name

        object_name = self.client.generate_unique_object_name()
        object_data = 'Test file data'
        content_length = str(len(object_data))
        self.client.set_storage_object(
                container_name,
                object_name,
                content_length=content_length,
                content_type=CONTENT_TYPE_TEXT,
                payload=object_data)

        headers = {'Range': 'bytes=5-8'}
        r = self.client.get_storage_object(container_name,
                object_name,
                headers=headers)
        self.assertEqual(r.status_code, 206,
                'should retrieve a partial object from the middle to the ' \
                'middle')

    def test_partial_object_retrieval_with_complete_range(self):
        container_name = self.container_name

        object_name = self.client.generate_unique_object_name()
        object_data = 'Test file data'
        content_length = str(len(object_data))
        self.client.set_storage_object(
                container_name,
                object_name,
                content_length=content_length,
                content_type=CONTENT_TYPE_TEXT,
                payload=object_data)

        headers = {'Range': 'bytes=99-0'}
        r = self.client.get_storage_object(container_name, object_name,
                headers=headers)
        self.assertEqual(r.status_code, 200, 'should retrieve complete object')

    """4.3.2. Create/Update Object"""
    def test_object_creation_with_valid_object_name(self):
        container_name = self.container_name

        object_name = self.client.generate_unique_object_name()
        object_data = 'Test file data'
        content_length = str(len(object_data))
        r = self.client.set_storage_object(
                container_name,
                object_name,
                content_length=content_length,
                content_type=CONTENT_TYPE_TEXT,
                payload=object_data)
        self.assertEqual(r.status_code, 201, 'should create object.')

    def test_object_update_with_valid_object_name(self):
        container_name = self.container_name

        object_name = self.client.generate_unique_object_name()
        object_data = 'Test file data'
        content_length = str(len(object_data))
        self.client.set_storage_object(
                container_name,
                object_name,
                content_length=content_length,
                content_type=CONTENT_TYPE_TEXT,
                payload=object_data)

        object_data = 'Updated test file data'
        content_length = str(len(object_data))
        x = self.client.set_storage_object(
                container_name,
                object_name,
                content_length=content_length,
                content_type=CONTENT_TYPE_TEXT,
                payload=object_data)

        self.assertEqual(x.status_code, 201, 'should update object.')

    def test_object_creation_with_etag_header(self):
        container_name = self.container_name

        object_name = self.client.generate_unique_object_name()
        object_data = 'Test file data'
        content_length = str(len(object_data))
        headers = {'Etag': self.filetools.get_md5_hash(object_data)}
        r = self.client.set_storage_object(
                container_name,
                object_name,
                content_length=content_length,
                content_type=CONTENT_TYPE_TEXT,
                payload=object_data,
                headers=headers)
        self.assertEqual(r.status_code, 201, 'should create object')

    def test_object_creation_with_metadata(self):
        container_name = self.container_name

        object_name = self.client.generate_unique_object_name()
        object_data = 'Test file data'
        content_length = str(len(object_data))
        headers = {'X-Object-Meta-Grok': 'Drok'}
        r = self.client.set_storage_object(
                container_name,
                object_name,
                content_length=content_length,
                content_type=CONTENT_TYPE_TEXT,
                payload=object_data,
                headers=headers)
        self.assertEqual(r.status_code, 201,
                'should create object with metadata')

    """4.3.2.1. Large Object Creation"""
    def test_object_creation_with_large_object(self):
        container_name = self.container_name

        object_name = self.client.generate_unique_object_name()

        segment_name = ''.join([object_name, '.1'])
        segment_data = 'Segment 1'
        content_length = str(len(segment_data))
        r = self.client.set_storage_object(
                container_name,
                segment_name,
                content_length=content_length,
                content_type=CONTENT_TYPE_TEXT,
                payload=segment_data)
        self.assertEqual(r.status_code, 201,
                'should create object representing segment 1')

        segment_name = ''.join([object_name, '.2'])
        segment_data = 'Segment 2'
        content_length = str(len(segment_data))
        r = self.client.set_storage_object(
                container_name,
                segment_name,
                content_length=content_length,
                content_type=CONTENT_TYPE_TEXT,
                payload=segment_data)
        self.assertEqual(r.status_code, 201,
                'should create object representing segment 2')

        large_object_common_prefix = ''.join([container_name, '/',
                object_name])
        headers = {'X-Object-Manifest': large_object_common_prefix}
        r = self.client.set_storage_object(
                container_name,
                object_name,
                content_length=0,
                content_type=CONTENT_TYPE_TEXT,
                payload='',
                headers=headers)
        self.assertEqual(r.status_code, 201,
                'should create large object manifest')

        r = self.client.get_storage_object(container_name,
                                                       object_name)
        self.assertEqual(r.status_code, 200,
                'should retrieve assembled large file')

    """4.3.2.2. Chunked Transfer Encoding"""
    def test_object_creation_with_chunked_transfer(self):
        container_name = self.container_name
        """TODO(rich5317): implement creation of smoke test for chunked
           transfers"""
        #x = self.client.create_container(self.base_container_name)
        #self.assertEqual(x.status_code, 201)

        #chunks = ['this', 'is', 'a', 'series', 'of', 'chunks!!!', '0']

        #x = self.client.chunked_transfer(self.base_container_name,
        #                                    self.base_object_name,
        #                                    payload=chunks)
        #self.assertEqual(x.status_code, 201)

        #x = self.client.retrieve_storage_object(self.base_container_name,
        #        self.base_object_name)
        #self.assertEqual(x.status_code, 200)
        #self.assertEqual(x.content, 'thisisaseriesofchunks!!!')

        #x = self.client.delete_storage_object(self.base_container_name,
        #        self.base_object_name)
        #self.assertEqual(x.status_code, 204)

        #x = self.client.delete_container(self.base_container_name)
        #self.assertEqual(x.status_code, 204)

    """4.3.2.3. Bulk Importing Data"""
    """TODO(rich5317): investigate process for this to see if there is anything
                       that can be done to test it."""

    """4.3.2.4. Assigning CORS Headers to Requests"""
    def test_object_creation_with_cors_allow_credentials_header(self):
        container_name = self.container_name

        object_name = self.client.generate_unique_object_name()
        object_data = 'Test file data'
        content_length = str(len(object_data))
        headers = {'Access-Control-Allow-Credentials': 'true'}
        self.client.set_storage_object(
                container_name,
                object_name,
                content_length=content_length,
                content_type=CONTENT_TYPE_TEXT,
                payload=object_data,
                headers=headers)

        r = self.client.get_storage_object(container_name,
                object_name)
        self.assertEqual(r.status_code, 200, 'should retrieve object')

    def test_object_creation_with_cors_allow_credentials_header(self):
        container_name = self.container_name

        object_name = self.client.generate_unique_object_name()
        object_data = 'Test file data'
        content_length = str(len(object_data))
        headers = {'Access-Control-Allow-Methods': 'GET, POST, OPTIONS'}
        self.client.set_storage_object(
                container_name,
                object_name,
                content_length=content_length,
                content_type=CONTENT_TYPE_TEXT,
                payload=object_data,
                headers=headers)

        r = self.client.get_storage_object(container_name,
                object_name)
        self.assertEqual(r.status_code, 200, 'should retrieve object')

    def test_object_creation_with_cors_allow_origin_header(self):
        container_name = self.container_name

        object_name = self.client.generate_unique_object_name()
        object_data = 'Test file data'
        content_length = str(len(object_data))
        headers = {'Access-Control-Allow-Origin': 'http://foobar.org'}
        self.client.set_storage_object(
                container_name,
                object_name,
                content_length=content_length,
                content_type=CONTENT_TYPE_TEXT,
                payload=object_data,
                headers=headers)

        r = self.client.get_storage_object(container_name,
                object_name)
        self.assertEqual(r.status_code, 200, 'should retrieve object')

    def test_object_creation_with_cors_expose_headers_header(self):
        container_name = self.container_name

        object_name = self.client.generate_unique_object_name()
        object_data = 'Test file data'
        content_length = str(len(object_data))
        headers = {'Access-Control-Expose-Headers': 'X-Foobar-Header'}
        self.client.set_storage_object(
                container_name,
                object_name,
                content_length=content_length,
                content_type=CONTENT_TYPE_TEXT,
                payload=object_data,
                headers=headers)

        r = self.client.get_storage_object(container_name,
                object_name)
        self.assertEqual(r.status_code, 200, 'should retrieve object')

    def test_object_creation_with_cors_max_age_header(self):
        container_name = self.container_name

        object_name = self.client.generate_unique_object_name()
        object_data = 'Test file data'
        content_length = str(len(object_data))
        headers = {'Access-Control-Max-Age': '5'}
        self.client.set_storage_object(
                container_name,
                object_name,
                content_length=content_length,
                content_type=CONTENT_TYPE_TEXT,
                payload=object_data,
                headers=headers)

        r = self.client.get_storage_object(container_name,
                object_name)
        self.assertEqual(r.status_code, 200, 'should retrieve object')

    def test_object_creation_with_cors_request_headers_header(self):
        container_name = self.container_name

        object_name = self.client.generate_unique_object_name()
        object_data = 'Test file data'
        content_length = str(len(object_data))
        headers = {'Access-Control-Request-Headers': 'x-requested-with'}
        self.client.set_storage_object(
                container_name,
                object_name,
                content_length=content_length,
                content_type=CONTENT_TYPE_TEXT,
                payload=object_data,
                headers=headers)

        r = self.client.get_storage_object(container_name,
                object_name)
        self.assertEqual(r.status_code, 200, 'should retrieve object')

    def test_object_creation_with_cors_request_method_header(self):
        container_name = self.container_name

        object_name = self.client.generate_unique_object_name()
        object_data = 'Test file data'
        content_length = str(len(object_data))
        headers = {'Access-Control-Request-Method': 'GET'}
        self.client.set_storage_object(
                container_name,
                object_name,
                content_length=content_length,
                content_type=CONTENT_TYPE_TEXT,
                payload=object_data,
                headers=headers)

        r = self.client.get_storage_object(container_name,
                object_name)
        self.assertEqual(r.status_code, 200, 'should retrieve object')

    def test_object_creation_with_cors_origin_header(self):
        container_name = self.container_name

        object_name = self.client.generate_unique_object_name()
        object_data = 'Test file data'
        content_length = str(len(object_data))
        headers = {'Origin': 'http://foobar.org'}
        self.client.set_storage_object(
                container_name,
                object_name,
                content_length=content_length,
                content_type=CONTENT_TYPE_TEXT,
                payload=object_data,
                headers=headers)

        r = self.client.get_storage_object(container_name,
                object_name)
        self.assertEqual(r.status_code, 200, 'should retrieve object')

    """4.3.2.5. Enabling File Compression with the Content-Encoding Header"""
    def test_object_retrieval_with_file_compression(self):
        container_name = self.container_name

        object_name = self.client.generate_unique_object_name()
        object_data = 'Uncompressed test file data'
        compressed_object_data = zlib.compress(object_data)
        content_length = str(len(compressed_object_data))
        headers = {'Content-Encoding': 'gzip'}
        self.client.set_storage_object(
                container_name,
                object_name,
                content_length=content_length,
                content_type=CONTENT_TYPE_TEXT,
                payload=compressed_object_data,
                headers=headers)

        r = self.client.get_storage_object(container_name,
                object_name)
        self.assertEqual(r.status_code, 200,
                'should retrieve a compressed object')

    """4.3.2.6. Enabling Browser Bypass with the Content-Disposition Header"""
    def test_object_retrieval_with_browser_bypase(self):
        container_name = self.container_name

        object_name = self.client.generate_unique_object_name()
        object_data = 'Test file data'
        content_length = str(len(object_data))
        headers = {'Content-Disposition': 'attachment; filename=testdata.txt'}
        self.client.set_storage_object(
                container_name,
                object_name,
                content_length=content_length,
                content_type=CONTENT_TYPE_TEXT,
                payload=object_data,
                headers=headers)

        r = self.client.get_storage_object(container_name,
                                                       object_name)
        self.assertEqual(r.status_code, 200,
                'should retrieve object')

    """4.3.2.7. Expiring Objects with the X-Delete-After and X-Delete-At Headers"""
    def test_object_creation_with_scheduled_expiration(self):
        container_name = self.container_name

        object_name = self.client.generate_unique_object_name()
        object_data = 'Test file data'
        content_length = str(len(object_data))
        start_time = calendar.timegm(time.gmtime())
        future_time = str(int(start_time + 60))
        headers = {'X-Delete-At': future_time}
        r = self.client.set_storage_object(
                container_name,
                object_name,
                content_length=content_length,
                content_type=CONTENT_TYPE_TEXT,
                payload=object_data,
                headers=headers)
        self.assertEqual(r.status_code, 201,
                'should create an object scheduled to expire')

    def test_object_creation_with_delete_after_header(self):
        container_name = self.container_name

        object_name = self.client.generate_unique_object_name()
        object_data = 'Test file data'
        content_length = str(len(object_data))
        start_time = calendar.timegm(time.gmtime())
        future_time = str(int(start_time + 60))
        headers = {'X-Delete-After': '60'}
        r = self.client.set_storage_object(
                container_name,
                object_name,
                content_length=content_length,
                content_type=CONTENT_TYPE_TEXT,
                payload=object_data,
                headers=headers)
        self.assertEqual(r.status_code, 201,
                'should create an object scheduled to expire')

    """4.3.2.8. Object Versioning"""
    def test_versioned_contaner_creation_with_valid_data(self):
        # Since the we are creating containers in this test, we won't use
        #   the common container.  Instead we will create a new container using
        #   the common test container's name appended them with
        #   '_versioned_non_current' and '_versioned_current'
        common_container_name = self.container_name
        """Create a container for 'non-current' object storage"""
        non_current_version_container_name = ''.join([common_container_name,
                '_versioned_non_current'])
        metadata = {'Access-Log-Delivery': 'True'}
        self.client.create_container(
                non_current_version_container_name,
                metadata=metadata)
        # Containers can not be deleted or access logs will not be generated
        self.fixture_log.info('Container created for object smoke log ' \
                'delivery tests(%s)' % non_current_version_container_name)

        """Create a container for 'current' object storage"""
        current_version_container_name = ''.join([common_container_name,
                                                 '_versioned_current'])
        current_version_container_headers = \
                {'X-Versions-Location': non_current_version_container_name}
        metadata = {'Access-Log-Delivery': 'True'}
        self.client.create_container(
                current_version_container_name,
                headers=current_version_container_headers,
                metadata=metadata)
        # Containers can not be deleted or access logs will not be generated
        self.fixture_log.info('Container created for object smoke log ' \
                'delivery tests(%s)' % current_version_container_name)

        """Create an object (version 1)"""
        object_name = self.client.generate_unique_object_name()
        object_data = 'Version 1'
        content_length = str(len(object_data))
        r = self.client.set_storage_object(
                current_version_container_name,
                object_name,
                content_length=content_length,
                content_type=CONTENT_TYPE_TEXT,
                payload=object_data)
        self.assertEqual(r.status_code, 201, 'should create versioned object')

        r = self.client.list_objects(
                non_current_version_container_name)
        self.assertEqual(r.status_code, 204, 'should be empty')

        """Update an object (version 2)"""
        object_data = 'Version 2'
        content_length = str(len(object_data))
        r = self.client.set_storage_object(
                current_version_container_name,
                object_name,
                content_length=content_length,
                content_type=CONTENT_TYPE_TEXT,
                payload=object_data)
        self.assertEqual(r.status_code, 201, 'should update versioned object')

        r = self.client.list_objects(
                non_current_version_container_name)
        self.assertEqual(r.status_code, 200, 'should have files')

    """4.3.3. Copy Object"""
    def test_object_copy_with_valid_object_name(self):
        container_name = self.container_name

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
        r = self.client.copy_storage_object(
                src_container=container_name,
                src_object=source_object_name,
                dst_object=copied_object_name)
        self.assertEqual(r.status_code, 201,
                'should copy an existing object')

        r = self.client.get_storage_object(container_name, copied_object_name)
        self.assertEqual(r.status_code, 200,
                'should be accessible after copy')

    def test_object_copy_with_x_copy_from_header(self):
        container_name = self.container_name

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
        r = self.client.set_storage_object(
                container_name,
                copied_object_name,
                content_length=0,
                content_type=CONTENT_TYPE_TEXT,
                payload='',
                headers=headers)
        self.assertEqual(r.status_code, 201,
                'should copy an existing object')

        r = self.client.get_storage_object(container_name, copied_object_name)
        self.assertEqual(r.status_code, 200,
                'should be accessible after copy')

    """4.3.4. Delete Object"""
    def test_object_deletion_with_valid_object(self):
        container_name = self.container_name

        object_name = self.client.generate_unique_object_name()
        object_data = 'Test file data'
        content_length = str(len(object_data))
        r = self.client.set_storage_object(
                container_name,
                object_name,
                content_length=content_length,
                content_type=CONTENT_TYPE_TEXT,
                payload=object_data)
        self.assertEqual(r.status_code, 201, 'should be created')

        r = self.client.delete_storage_object(container_name, object_name)
        self.assertEqual(r.status_code, 204, 'should be deleted')

        r = self.client.get_storage_object(container_name,
                                                       object_name)
        self.assertEqual(r.status_code, 404,
                'should not be accessible after deletion')

    """4.3.5. Retrieve Object Metadata"""
    def test_metadata_retrieval_with_newly_created_object(self):
        container_name = self.container_name

        object_name = self.client.generate_unique_object_name()
        object_data = 'Test file data'
        content_length = str(len(object_data))
        headers = {'X-Object-Meta-Grok': 'Drok'}
        r = self.client.set_storage_object(
                container_name,
                object_name,
                content_length=content_length,
                content_type=CONTENT_TYPE_TEXT,
                payload=object_data,
                headers=headers)
        self.assertEqual(r.status_code, 201, 'should be created')

        r = self.client.get_storage_object_metadata(container_name,
                object_name)
        self.assertEqual(r.status_code, 200,
                'should be accessible after creation')

    def test_metadata_retrieval_with_object_possessing_metadata(self):
        container_name = self.container_name

        object_name = self.client.generate_unique_object_name()
        object_data = 'Test file data'
        content_length = str(len(object_data))
        self.client.set_storage_object(
                container_name,
                object_name,
                content_length=content_length,
                content_type=CONTENT_TYPE_TEXT,
                payload=object_data)

        metadata = {'Grok': 'Drok'}
        r = self.client.set_storage_object_metadata(container_name,
                object_name,
                metadata)
        self.assertEqual(r.status_code, 202, 'should set metadata')

    """4.3.6. Update Object Metadata"""
    def test_object_update_with_metadata(self):
        container_name = self.container_name

        object_name = self.client.generate_unique_object_name()
        object_data = 'Test file data'
        content_length = str(len(object_data))
        self.client.set_storage_object(
                container_name,
                object_name,
                content_length=content_length,
                content_type=CONTENT_TYPE_TEXT,
                payload=object_data)

        metadata = {'Grok': 'Drok'}
        r = self.client.set_storage_object_metadata(container_name,
                object_name,
                metadata)
        self.assertEqual(r.status_code, 202, 'should set metadata')

        r = self.client.get_storage_object_metadata(container_name,
                object_name)
        self.assertEqual(r.status_code, 200,
                'should be accessible after update')
