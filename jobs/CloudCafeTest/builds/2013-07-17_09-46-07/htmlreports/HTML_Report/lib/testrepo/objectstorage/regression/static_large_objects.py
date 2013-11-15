"""
Swfit Static Large Object Tests

http://docs.openstack.org/developer/swift/misc.html#module-swift.common.middleware.slo
"""
import time
import json
import unittest

from ccengine.common.tools.filetools import get_md5_hash
from testrepo.common.testfixtures.object_storage_fixture \
    import ObjectStorageTestFixture
from ccengine.common.data_generators.objectstorage.object_generators \
    import generate_static_large_object
from ccengine.common.data_generators.objectstorage.object_generators \
    import generate_data_from_pattern
from ccengine.common.data_generators.objectstorage.object_generators \
    import generate_md5sum_from_pattern
from ccengine.common.decorators import attr

from ccengine.common.data_generators.objectstorage.object_generators \
    import SWIFT_CONTENT_TYPE_TEXT
from ccengine.common.data_generators.objectstorage.object_generators \
    import SWIFT_CONTENT_TYPE_JSON
from ccengine.common.data_generators.objectstorage.object_generators \
    import SWIFT_CONTENT_TYPE_HTML


class StaticLargeObjectsRegressionTest(ObjectStorageTestFixture):
    """
    Allows the user to upload many objects concurrently and afterwards
    download them as a single object.  Static large objects differ from
    dynamic large objects in that a manifest file is uploaded which defines
    the segments to be combined to form the static large object.
    """

    @attr('regression', type='positive')
    def test_slo_creation_with_valid_slo(self):
        """
        Scenario:
            Create a SLO where the manifest and each segment are in their
            own unique containers.

        Expected Results:
            The SLO should be created.
        """
        min_segment_size = self.config.object_storage_api.slo_min_segment_size
        containers = []

        container_name = self.client.generate_unique_container_name('slo')
        containers.append(container_name)
        object_name = 'object'

        manifest = []
        for x in range(0, 3):
            segment_container_name = '{0}_{1}'.format(container_name, x)
            containers.append(segment_container_name)
            manifest.append({
                'container_name': segment_container_name,
                'name': '{0}.{1}'.format(object_name, x),
                'size_bytes': min_segment_size,
                'data_pattern': str(x)})

        self.addCleanup(self.client.force_delete_containers, containers)

        (seg_results, slo_results) = generate_static_large_object(
            self.client, container_name, object_name, manifest)

        for segment in manifest:
            key = '{0}/{1}'.format(segment['container_name'], segment['name'])
            self.assertTrue(
                key in seg_results,
                'segment should be captured in responses.')
            self.assertTrue(
                seg_results[key]['container_response'].ok,
                'should create "segment {0}" container.'.format(
                    segment['container_name']))
            self.assertTrue(
                seg_results[key]['object_response'].ok,
                'should create "segment {0}".'.format(
                    segment['name']))

        # NOTE: r.headers['etag'] will not match the md5sum of the manifest
        #   sent since the manifest stored is generated from the one
        #   uploaded.
        self.assertEqual(
            slo_results['container_response'].status_code, 201,
            'should create container for SLO.')
        self.assertTrue(
            slo_results['object_response'].ok,
            'should create SLO.')
        self.assertEqual(
            slo_results['object_response'].headers['content-length'], '0',
            'should recieve correct content-length.')
        self.assertNotIn(
            slo_results['object_response'].headers['content-type'],
            'swift_size',
            'content-type should not have swift_size field.')
        self.assertEqual(
            slo_results['object_response'].headers['content-type'],
            SWIFT_CONTENT_TYPE_HTML, 'should recieve correct content-type.')

    def test_slo_retrieval_with_valid_slo(self):
        """
        Scenario:
            Retrive a SLO.

        Expected Results:
            The SLO retrieved should be identical to the original data the
            SLO was created from.

        Notes:
            The ETag of the SLO is not the MD5 hash of the assembled object's
            segments, but will be the MD5 hash of the concatination of each
            segment's MD5 hash.
            When retrieving a SLO, the content type should not list the
            internal 'swift_size' field.
        """
        min_segment_size = self.config.object_storage_api.slo_min_segment_size
        containers = []

        container_name = self.client.generate_unique_container_name('slo')
        containers.append(container_name)
        object_name = 'object'

        manifest = []
        for x in range(0, 3):
            segment_container_name = '{0}_{1}'.format(container_name, x)
            containers.append(segment_container_name)
            manifest.append({
                'container_name': segment_container_name,
                'name': '{0}.{1}'.format(object_name, x),
                'size_bytes': min_segment_size,
                'data_pattern': str(x)})

        self.addCleanup(self.client.force_delete_containers, containers)

        (seg_results, slo_results) = generate_static_large_object(
            self.client, container_name, object_name, manifest)

        etags = []

        for segment in manifest:
            key = '{0}/{1}'.format(segment['container_name'], segment['name'])
            self.assertTrue(
                key in seg_results,
                'segment should be captured in responses.')
            etags.append(generate_md5sum_from_pattern(
                segment['data_pattern'], segment['size_bytes']))
            self.assertTrue(
                seg_results[key]['container_response'].ok,
                'should create "segment {0}" container.'.format(
                    segment['container_name']))
        self.assertEqual(
            slo_results['container_response'].status_code, 201,
            'should create container for SLO.')

        # Retrieve the static large object.
        r = self.client.get_storage_object(
            container_name, object_name)

        #expected_slo_content_md5sum = get_md5_hash(expected_slo_content)
        expected_slo_etag = get_md5_hash(''.join(etags))
        expected_slo_quoted_etag = '"{0}"'.format(expected_slo_etag)

        self.assertEqual(
            r.status_code, 200, 'should return static large object')
        self.assertTrue(
            r.headers['x-static-large-object'],
            'SLO "x-static-large-object" header should be correct.')
        self.assertEqual(
            r.headers['etag'], expected_slo_quoted_etag,
            'SLO "etag" header should be correct.')
        self.assertNotIn(
            r.headers['content-type'], 'swift_size',
            'content-type should not have swift_size field.')
        self.assertEqual(
            r.headers['content-type'], SWIFT_CONTENT_TYPE_TEXT,
            'SLO "content-type" header should be correct.')
        #self.assertEqual(
        #    get_md5_hash(r.content), expected_slo_content_md5sum,
        #    'SLO content should be correct.')

    @attr('regression', type='positive')
    def test_slo_manifest_retrieval_with_valid_slo(self):
        """
        Scenario:
            Retrive a SLO manifest.

        Expected Results:
            The SLO manifest should be returned.
        """
        min_segment_size = self.config.object_storage_api.slo_min_segment_size
        containers = []

        container_name = self.client.generate_unique_container_name('slo')
        containers.append(container_name)
        object_name = 'object'

        manifest = []
        expected_segments = {}
        for x in range(0, 3):
            segment_container_name = '{0}_{1}'.format(container_name, x)
            segment_object_name = '{0}.{1}'.format(object_name, x)
            segment_key = '/{0}/{1}'.format(
                segment_container_name, segment_object_name)

            containers.append(segment_container_name)
            segment_pattern = str(x)
            segment_size = min_segment_size
            expected_segment_data = generate_data_from_pattern(
                segment_pattern, segment_size)
            expected_segment_etag = get_md5_hash(expected_segment_data)

            segment = {
                'container_name': segment_container_name,
                'name': segment_object_name,
                'size_bytes': segment_size,
                'data_pattern': segment_pattern}
            manifest.append(segment)

            expected_segments[segment_key] = {
                'bytes': segment_size,
                'content_type': 'application/octet-stream',
                'hash': expected_segment_etag}

        self.addCleanup(self.client.force_delete_containers, containers)

        (seg_results, slo_results) = generate_static_large_object(
            self.client, container_name, object_name, manifest)

        self.assertEqual(
            slo_results['object_response'].status_code, 201,
            'should create static large object.')

        # Retrieve the static large object.
        # NOTE: r.headers['etag'] will not match the md5sum of the manifest
        #   sent since the manifest stored is generated from the one
        #   uploaded.
        params = {'multipart-manifest': 'get'}
        r = self.client.get_storage_object(
            container_name, object_name, params=params)
        self.assertEqual(
            r.status_code, 200, 'should return SLO manifest.')
        self.assertTrue(
            r.headers['x-static-large-object'],
            'SLO manifest "x-static-large-object" header should correct.')
        self.assertTrue(
            'content-type' in r.headers,
            '"content-type" should be in headers.')
        self.assertEqual(
            r.headers['content-type'], SWIFT_CONTENT_TYPE_JSON,
            '"content-type" header should be json.')

        # NOTE: The manifest genrated from our manifest will look similar to
        #   the following:
        #
        #   [{"hash": "7202826a7791073fe2787f0c94603278",
        #    "last_modified": "2013-03-22T14:40:53.000000",
        #    "bytes": 1048576,
        #    "name": "/slo_a_2013-3-22-9-40_cf_qe_container_bd10b6de/A",
        #    "content_type": "application/octet-stream"}, ...]
        manifest = json.loads(r.content)
        for segment in manifest:
            self.assertTrue(
                'name' in segment,
                'manifest segment should contain a "name" field.')
            key = segment['name']
            self.assertTrue(
                'hash' in segment,
                'manifest segment should contain a "hash" field.')
            self.assertEqual(
                segment['hash'], expected_segments[key]['hash'],
                'hash should match etag for "{0}".'.format(key))
            self.assertTrue(
                'last_modified' in segment,
                'manifest segment should contain a "last_modified" field.')
            self.assertEqual(
                segment['bytes'], expected_segments[key]['bytes'],
                'bytes should match size_bytes for "{0}".'.format(key))
            self.assertEqual(
                segment['content_type'],
                expected_segments[key]['content_type'],
                'content-type should match for "{0}".'.format(key))

    @attr('regression', type='positive')
    def test_slo_creation_with_slo_header(self):
        """
        Scenario:
            Create a SLO while sending the 'X-Static-Large-Object' header.

        Expected Results:
            The SLO should be created.  Regardless of the value sent with the
            header, 'True' should be the value set after the SLO is created.

        Notes:
            The header 'X-Static-Large-Ojbect' is a server only header, and
            should not be settable by the end user.
        """
        min_segment_size = self.config.object_storage_api.slo_min_segment_size
        containers = []

        container_name = self.client.generate_unique_container_name('slo')
        containers.append(container_name)
        object_name = 'object'

        expected_segment_data = []
        manifest = []
        for x in range(0, 3):
            segment_container_name = '{0}_{1}'.format(container_name, x)
            containers.append(segment_container_name)
            manifest.append({
                'container_name': segment_container_name,
                'name': '{0}.{1}'.format(object_name, x),
                'size_bytes': min_segment_size,
                'data_pattern': str(x)})
            expected_segment_data.append(generate_data_from_pattern(
                str(x), min_segment_size))

        headers = {'X-Static-Large-Object': 'False'}
        self.addCleanup(self.client.force_delete_containers, containers)

        (seg_results, slo_results) = generate_static_large_object(
            self.client, container_name, object_name, manifest,
            slo_headers=headers)
        r = slo_results['object_response']

        self.assertEqual(r.status_code, 201, 'should create manifest object.')

        expected_content = ''.join(expected_segment_data)
        r = self.client.get_storage_object(container_name, object_name)
        self.assertEqual(
            r.status_code, 200, 'should return static large object')
        self.assertTrue(
            r.headers['x-static-large-object'], 'should set SLO header.')
        self.assertEqual(
            get_md5_hash(r.content), get_md5_hash(expected_content),
            'original data and slo md5sums should match.')

    @attr('regression', type='positive')
    def test_copy_slo_with_valid_combined_segment_size(self):
        """
        Scenario:
            Copy (HTTP COPY) a SLO.  The summation of all the SLOs segments
            should be less than the max allowed object size.

        Expected Results:
            A non SLO object should be created which contains all the user
            set metadata from the source SLO being copied.  The content for
            the new object should be the summation of all the SLO's segments.

        Notes:
            TODO (rich5317): Verify this is the case.
            The ETag for the newly copied object should be the MD5 hash for
            its content?
        """
        min_segment_size = self.config.object_storage_api.slo_min_segment_size

        # Create the container to house segment 'a'
        segment_a_container_name = \
            self.client.generate_unique_container_name('slo_a')
        r = self.client.create_container(segment_a_container_name)
        self.addCleanup(
            self.client.force_delete_containers, [segment_a_container_name])
        self.assertTrue(r.ok, 'should create "segment a" container.')

        # Create segment 'a' for the static large object
        segment_a_name = 'A'
        segment_a_data = 'a' * min_segment_size
        segment_a_etag = get_md5_hash(segment_a_data)
        segment_a_size = str(len(segment_a_data))
        r = self.client.set_storage_object(
            segment_a_container_name, segment_a_name,
            content_length=segment_a_size, payload=segment_a_data)
        self.assertEqual(
            r.status_code, 201, 'should create "a" segment object.')

        # Create the container to house segment 'b'
        segment_b_container_name = \
            self.client.generate_unique_container_name('slo_b')
        r = self.client.create_container(segment_b_container_name)
        self.addCleanup(
            self.client.force_delete_containers, [segment_b_container_name])
        self.assertTrue(r.ok, 'should create "segment b" container.')

        # Create segment 'b' for the static large object
        segment_b_name = 'B'
        segment_b_data = 'b' * min_segment_size
        segment_b_etag = get_md5_hash(segment_b_data)
        segment_b_size = str(len(segment_b_data))
        r = self.client.set_storage_object(
            segment_b_container_name, segment_b_name,
            content_length=segment_b_size, payload=segment_b_data)
        self.assertEqual(
            r.status_code, 201, 'should create "b" segment object.')

        slo_container_name = \
            self.client.generate_unique_container_name('slo')
        r = self.client.create_container(slo_container_name)
        self.addCleanup(
            self.client.force_delete_containers, [slo_container_name])
        self.assertTrue(r.ok, 'should create "slo" container.')

        # Create the manifest for the static large object
        slo_name = 'slo_object'
        slo_manifest = '[{{"path": "{0}/{1}",' \
            '"etag": "{2}",' \
            '"size_bytes": {3}}},' \
            '{{"path": "{4}/{5}",' \
            '"etag": "{6}",' \
            '"size_bytes": {7}}}]'.format(
                segment_a_container_name, segment_a_name,
                segment_a_etag,
                segment_a_size,
                segment_b_container_name, segment_b_name,
                segment_b_etag,
                segment_b_size)
        slo_manifest_size = str(len(slo_manifest))
        slo_custom_header = 'x-object-meta-foo'
        slo_custom_header_value = 'bar'
        slo_headers = {
            'Content-Type': 'text/plain',
            slo_custom_header: slo_custom_header_value}
        slo_params = {'multipart-manifest': 'put'}

        # Send the static large object manifest
        # NOTE: The manifest sent will not be the manifest stored.  The system
        #   will take the manifest, parse it, and generate a new manifest to
        #   store.
        r = self.client.set_storage_object(
            slo_container_name, slo_name,
            content_length=slo_manifest_size, payload=slo_manifest,
            headers=slo_headers, params=slo_params)

        # NOTE: r.headers['etag'] will not match the md5sum of the manifest
        #   sent since the manifest stored is generated from the one
        #   uploaded.
        self.assertEqual(
            r.status_code, 201, 'should create manifest object.')

        copy_container_name = \
            self.client.generate_unique_container_name('slo_copy')
        r = self.client.create_container(copy_container_name)
        self.addCleanup(
            self.client.force_delete_containers, [copy_container_name])
        self.assertTrue(r.ok, 'should create "slo_copy" container.')

        copy_name = '{0}.copy'.format(slo_name)
        r = self.client.copy_storage_object(
            slo_container_name, slo_name,
            dst_container=copy_container_name, dst_object=copy_name)
        self.assertEqual(
            r.status_code, 201, 'should copy the SLO.')

        r = self.client.get_storage_object(copy_container_name, copy_name)
        self.assertTrue(
            r.ok, 'should return the copied object.')
        slo_content = '{0}{1}'.format(
            ('a' * min_segment_size), ('b' * min_segment_size))
        slo_content_md5sum = get_md5_hash(slo_content)
        copy_object_md5sum = get_md5_hash(r.content)
        self.assertEqual(
            copy_object_md5sum, slo_content_md5sum,
            'should return the copied object.')
        self.assertFalse(
            'x-static-large-object' in r.headers,
            'should not contain the "x-static-large-object" header.')
        self.assertEqual(
            r.headers[slo_custom_header], slo_custom_header_value,
            'custom headers should be copied to the object.')

    @attr('regression', type='positive')
    def test_copyput_slo_with_valid_combined_segment_size(self):
        """
        Scenario:
            Copy (HTTP PUT) a SLO.  The summation of all the SLOs segments
            should be less than the max allowed object size.

        Expected Results:
            A non SLO object should be created which contains all the user
            set metadata from the source SLO being copied.  The content for
            the new object should be the summation of all the SLO's segments.
        """
        min_segment_size = self.config.object_storage_api.slo_min_segment_size

        # Create the container to house segment 'a'
        segment_a_container_name = \
            self.client.generate_unique_container_name('slo_a')
        r = self.client.create_container(segment_a_container_name)
        self.addCleanup(
            self.client.force_delete_containers, [segment_a_container_name])
        self.assertTrue(r.ok, 'should create "segment a" container.')

        # Create segment 'a' for the static large object
        segment_a_name = 'A'
        segment_a_data = 'a' * min_segment_size
        segment_a_etag = get_md5_hash(segment_a_data)
        segment_a_size = str(len(segment_a_data))
        r = self.client.set_storage_object(
            segment_a_container_name, segment_a_name,
            content_length=segment_a_size, payload=segment_a_data)
        self.assertEqual(
            r.status_code, 201, 'should create "a" segment object.')

        # Create the container to house segment 'b'
        segment_b_container_name = \
            self.client.generate_unique_container_name('slo_b')
        r = self.client.create_container(segment_b_container_name)
        self.addCleanup(
            self.client.force_delete_containers, [segment_b_container_name])
        self.assertTrue(r.ok, 'should create "segment b" container.')

        # Create segment 'b' for the static large object
        segment_b_name = 'B'
        segment_b_data = 'b' * min_segment_size
        segment_b_etag = get_md5_hash(segment_b_data)
        segment_b_size = str(len(segment_b_data))
        r = self.client.set_storage_object(
            segment_b_container_name, segment_b_name,
            content_length=segment_b_size, payload=segment_b_data)
        self.assertEqual(
            r.status_code, 201, 'should create "b" segment object.')

        slo_container_name = \
            self.client.generate_unique_container_name('slo')
        r = self.client.create_container(slo_container_name)
        self.addCleanup(
            self.client.force_delete_containers, [slo_container_name])
        self.assertTrue(r.ok, 'should create "slo" container.')

        # Create the manifest for the static large object
        slo_name = 'slo_object'
        slo_manifest = '[{{"path": "{0}/{1}",' \
            '"etag": "{2}",' \
            '"size_bytes": {3}}},' \
            '{{"path": "{4}/{5}",' \
            '"etag": "{6}",' \
            '"size_bytes": {7}}}]'.format(
                segment_a_container_name, segment_a_name,
                segment_a_etag,
                segment_a_size,
                segment_b_container_name, segment_b_name,
                segment_b_etag,
                segment_b_size)
        slo_manifest_size = str(len(slo_manifest))
        slo_custom_header = 'x-object-meta-foo'
        slo_custom_header_value = 'bar'
        slo_headers = {
            'Content-Type': 'text/plain',
            slo_custom_header: slo_custom_header_value}
        slo_params = {'multipart-manifest': 'put'}

        # Send the static large object manifest
        # NOTE: The manifest sent will not be the manifest stored.  The system
        #   will take the manifest, parse it, and generate a new manifest to
        #   store.
        r = self.client.set_storage_object(
            slo_container_name, slo_name,
            content_length=slo_manifest_size, payload=slo_manifest,
            headers=slo_headers, params=slo_params)

        # NOTE: r.headers['etag'] will not match the md5sum of the manifest
        #   sent since the manifest stored is generated from the one
        #   uploaded.
        self.assertEqual(
            r.status_code, 201, 'should create manifest object.')

        copy_container_name = \
            self.client.generate_unique_container_name('slo_copy')
        r = self.client.create_container(copy_container_name)
        self.addCleanup(
            self.client.force_delete_containers, [copy_container_name])
        self.assertTrue(r.ok, 'should create "slo_copy" container.')

        copy_name = '{0}.copy'.format(slo_name)

        r = self.client.putcopy_storage_object(
            slo_container_name, slo_name,
            dst_container=copy_container_name, dst_object=copy_name)
        self.assertEqual(
            r.status_code, 201, 'should copy the SLO.')

        r = self.client.get_storage_object(copy_container_name, copy_name)
        self.assertTrue(
            r.ok, 'should return the copied object.')
        slo_content = '{0}{1}'.format(
            ('a' * min_segment_size), ('b' * min_segment_size))
        slo_content_md5sum = get_md5_hash(slo_content)
        copy_object_md5sum = get_md5_hash(r.content)
        self.assertEqual(
            copy_object_md5sum, slo_content_md5sum,
            'should return the copied object.')
        self.assertFalse(
            'x-static-large-object' in r.headers,
            'should not contain the "x-static-large-object" header.')
        self.assertEqual(
            r.headers[slo_custom_header], slo_custom_header_value,
            'custom headers should be copied to the object.')

    @attr('regression', type='negative')
    @unittest.skip('This test is too slow and takes up too much memory.')
    def test_copy_slo_with_exceeded_combined_segment_size(self):
        """
        Scenario:
            Copy (HTTP PUT) a SLO.  The summation of all the SLOs segments
            should be greater than the max allowed object size.

        Expected Results:
            An error should be returned immediatly.
        """
        min_segment_size = self.config.object_storage_api.slo_min_segment_size
        max_object_size = self.config.object_storage_api.object_max_size

        # Create the container to house segment 'a'
        segment_a_container_name = \
            self.client.generate_unique_container_name('slo_a')
        r = self.client.create_container(segment_a_container_name)
        self.addCleanup(
            self.client.force_delete_containers, [segment_a_container_name])
        self.assertTrue(r.ok, 'should create "segment a" container.')

        # Create segment 'a' for the static large object
        segment_a_name = 'A'
        segment_a_data = 'a' * max_object_size
        segment_a_etag = get_md5_hash(segment_a_data)
        segment_a_size = str(len(segment_a_data))
        r = self.client.set_storage_object(
            segment_a_container_name, segment_a_name,
            content_length=segment_a_size, payload=segment_a_data)
        self.assertEqual(
            r.status_code, 201, 'should create "a" segment object.')

        # Create the container to house segment 'b'
        segment_b_container_name = \
            self.client.generate_unique_container_name('slo_b')
        r = self.client.create_container(segment_b_container_name)
        self.addCleanup(
            self.client.force_delete_containers, [segment_b_container_name])
        self.assertTrue(r.ok, 'should create "segment b" container.')

        # Create segment 'b' for the static large object
        segment_b_name = 'B'
        segment_b_data = 'b' * min_segment_size
        segment_b_etag = get_md5_hash(segment_b_data)
        segment_b_size = str(len(segment_b_data))
        r = self.client.set_storage_object(
            segment_b_container_name, segment_b_name,
            content_length=segment_b_size, payload=segment_b_data)
        self.assertEqual(
            r.status_code, 201, 'should create "b" segment object.')

        slo_container_name = \
            self.client.generate_unique_container_name('slo')
        r = self.client.create_container(slo_container_name)
        self.addCleanup(
            self.client.force_delete_containers, [slo_container_name])
        self.assertTrue(r.ok, 'should create "slo" container.')

        # Create the manifest for the static large object
        slo_name = 'slo_object'
        slo_manifest = '[{{"path": "{0}/{1}",' \
            '"etag": "{2}",' \
            '"size_bytes": {3}}},' \
            '{{"path": "{4}/{5}",' \
            '"etag": "{6}",' \
            '"size_bytes": {7}}}]'.format(
                segment_a_container_name, segment_a_name,
                segment_a_etag,
                segment_a_size,
                segment_b_container_name, segment_b_name,
                segment_b_etag,
                segment_b_size)
        slo_manifest_size = str(len(slo_manifest))
        slo_custom_header = 'x-object-meta-foo'
        slo_custom_header_value = 'bar'
        slo_headers = {
            'Content-Type': 'text/plain',
            slo_custom_header: slo_custom_header_value}
        slo_params = {'multipart-manifest': 'put'}

        # Send the static large object manifest
        # NOTE: The manifest sent will not be the manifest stored.  The system
        #   will take the manifest, parse it, and generate a new manifest to
        #   store.
        r = self.client.set_storage_object(
            slo_container_name, slo_name,
            content_length=slo_manifest_size, payload=slo_manifest,
            headers=slo_headers, params=slo_params)

        # NOTE: r.headers['etag'] will not match the md5sum of the manifest
        #   sent since the manifest stored is generated from the one
        #   uploaded.
        self.assertEqual(
            r.status_code, 201, 'should create manifest object.')

        copy_container_name = \
            self.client.generate_unique_container_name('slo_copy')
        r = self.client.create_container(copy_container_name)
        self.addCleanup(
            self.client.force_delete_containers, [copy_container_name])
        self.assertTrue(r.ok, 'should create "slo_copy" container.')

        copy_name = '{0}.copy'.format(slo_name)

        r = self.client.copy_storage_object(
            slo_container_name, slo_name,
            dst_container=copy_container_name, dst_object=copy_name)
        self.assertEqual(
            r.status_code, 201, 'should copy the SLO.')

        r = self.client.get_storage_object(copy_container_name, copy_name)
        self.assertTrue(
            r.ok, 'should return the copied object.')
        slo_content = '{0}{1}'.format(
            ('a' * min_segment_size), ('b' * min_segment_size))
        slo_content_md5sum = get_md5_hash(slo_content)
        copy_object_md5sum = get_md5_hash(r.content)
        self.assertEqual(
            copy_object_md5sum, slo_content_md5sum,
            'should return the copied object.')
        self.assertFalse(
            'x-static-large-object' in r.headers,
            'should not contain the "x-static-large-object" header.')
        self.assertEqual(
            r.headers[slo_custom_header], slo_custom_header_value,
            'custom headers should be copied to the object.')

    @attr('regression', type='negative')
    def test_putcopy_slo_with_exceeded_combined_segment_size(self):
        """
        Scenario:
            Copy (HTTP PUT) a SLO.  The summation of all the SLOs segments
            should be greater than the max allowed object size.

        Expected Results:
            An error should be returned immediatly indicating that the SLO
            is too large to be copied to a non SLO object.
        """

    # HTTP method vs multipart-manifest method matrix

    @attr('regression', type='positive')
    def test_add_metadata_with_valid_slo(self):
        """
        Scenario:
            Create a SLO, once created, add metadata to the SLO (copy/POST).

        Expected Results:
            After metadata is added, the object should continue to be a valid
            SLO.
        """

    @attr('regression', type='positive')
    def test_copyput_slo_manifest_with_slo(self):
        """
        Scenario:
            Create a SLO, once created, copy the manifest.

        Expected Results:
            Verify the copy is a valid SLO.
        """
        min_segment_size = self.config.object_storage_api.slo_min_segment_size
        containers = []

        container_name = self.client.generate_unique_container_name('slo')
        containers.append(container_name)
        object_name = 'object'

        manifest = []
        for x in range(0, 3):
            segment_container_name = '{0}_{1}'.format(container_name, x)
            containers.append(segment_container_name)
            manifest.append({
                'container_name': segment_container_name,
                'name': '{0}.{1}'.format(object_name, x),
                'size_bytes': min_segment_size,
                'data_pattern': str(x)})

        self.addCleanup(self.client.force_delete_containers, containers)

        headers = {'Content-Type': 'text/plain'}
        (seg_results, slo_results) = generate_static_large_object(
            self.client, container_name, object_name, manifest,
            slo_headers=headers)
        self.assertEqual(
            slo_results['object_response'].status_code, 201,
            'should create the SLO.')

        # Ensure last modified should be different.
        time.sleep(2)

        src = '{0}/{1}'.format(container_name, object_name)
        headers = {'x-copy-from': src}
        params = {'multipart-manifest': 'get'}
        copy_name = '{0}.copy'.format(object_name)
        r = self.client.set_storage_object(
            container_name, copy_name, headers=headers, params=params)

        # Validate the manifests
        params = {'multipart-manifest': 'get'}
        r = self.client.get_storage_object(
            container_name, object_name, params=params)
        self.assertTrue(r.ok, 'should return src manifest.')
        src_manifest = r.content
        src_manifest_md5 = get_md5_hash(src_manifest)
        src_headers = r.headers

        params = {'multipart-manifest': 'get'}
        r = self.client.get_storage_object(
            container_name, copy_name, params=params)
        self.assertEqual(
            r.status_code, 200, 'should return copy of manifest.')
        copy_manifest = r.content
        copy_manifest_md5 = get_md5_hash(copy_manifest)
        copy_headers = r.headers

        self.assertEqual(
            copy_manifest, src_manifest,
            'copy of manifest data should match the original.')
        self.assertEqual(
            copy_headers['content-length'], src_headers['content-length'],
            'manifest copies content-length header should match original.')
        self.assertEqual(
            copy_headers['etag'], src_headers['etag'],
            'manifest copies etag header should match original.')
        self.assertNotEqual(
            copy_headers['last-modified'], src_headers['last-modified'],
            'manifest copies last-modified header should not match original.')
        self.assertEqual(
            copy_headers['x-static-large-object'],
            src_headers['x-static-large-object'],
            'manifest copies x-static-large-object header should match '
            'original.')
        self.assertEqual(
            copy_headers['content-type'], src_headers['content-type'],
            'manifest copies content-type header should match original.')

        r = self.client.get_storage_object(container_name, object_name)
        self.assertTrue(r.ok, 'should return src object.')
        src_object = r.content
        src_object_md5 = get_md5_hash(src_object)
        src_headers = r.headers

        r = self.client.get_storage_object(container_name, copy_name)
        self.assertEqual(
            r.status_code, 200, 'should return copy of manifest.')
        copy_object = r.content
        copy_object_md5 = get_md5_hash(copy_object)
        copy_headers = r.headers

        self.assertEqual(
            copy_object_md5, src_object_md5,
            'copy object md5 should match the src data md5.')
        self.assertEqual(
            copy_headers['content-length'], src_headers['content-length'],
            'copy object content-length header should match src.')
        self.assertEqual(
            copy_headers['etag'], src_headers['etag'],
            'copy object etag header should match src.')
        self.assertEqual(
            copy_headers['last-modified'], src_headers['last-modified'],
            'copy object last-modified header should match src.')
        self.assertEqual(
            copy_headers['x-static-large-object'],
            src_headers['x-static-large-object'],
            'copy object x-static-large-object header should match src.')
        self.assertEqual(
            copy_headers['content-type'], src_headers['content-type'],
            'copy object content-type header should match src.')

    @attr('regression', type='positive')
    def test_slo_creation_with_last_segment_less_than_min_size(self):
        """
        Scenario:
            Create a SLO, where the last segment's size is less than the
            min allowed segment size.

        Expected Results:
            Verify that the SLO is created.

        Notes:
            The min segment size does not apply to the last segment in a SLO.
        """
        min_segment_size = self.config.object_storage_api.slo_min_segment_size
        containers = []

        container_name = self.client.generate_unique_container_name('slo')
        containers.append(container_name)
        object_name = 'object'

        manifest = []
        for x in range(0, 3):
            segment_container_name = '{0}_{1}'.format(container_name, x)
            containers.append(segment_container_name)
            manifest.append({
                'container_name': segment_container_name,
                'name': '{0}.{1}'.format(object_name, x),
                'size_bytes': min_segment_size,
                'data_pattern': str(x)})

        segment_container_name = '{0}_{1}'.format(container_name, 'last')
        containers.append(segment_container_name)
        manifest.append({
            'container_name': segment_container_name,
            'name': '{0}.{1}'.format(object_name, 'last'),
            'size_bytes': 1,
            'data_pattern': 'a'})
        self.addCleanup(self.client.force_delete_containers, containers)

        (seg_results, slo_results) = generate_static_large_object(
            self.client, container_name, object_name, manifest)

        for segment in manifest:
            key = '{0}/{1}'.format(segment['container_name'], segment['name'])
            self.assertTrue(
                key in seg_results,
                'segment should be captured in responses.')
            self.assertTrue(
                seg_results[key]['container_response'].ok,
                'should create "segment {0}" container.'.format(
                    segment['container_name']))
            self.assertTrue(
                seg_results[key]['object_response'].ok,
                'should create "segment {0}".'.format(
                    segment['name']))

        self.assertEqual(
            slo_results['container_response'].status_code, 201,
            'should create container for SLO.')
        self.assertTrue(
            slo_results['object_response'].ok,
            'should create SLO.')
        self.assertEqual(
            slo_results['object_response'].headers['content-length'], '0',
            'should recieve correct content-length.')
        self.assertEqual(
            slo_results['object_response'].headers['content-type'],
            SWIFT_CONTENT_TYPE_HTML, 'should recieve correct content-type.')

    @attr('regression', type='positive')
    def test_slo_creation_fails_with_middle_segment_less_than_min_size(self):
        """
        Scenario:
            Create a SLO, where a middle segment's size is less than the
            min allowed segment size.

        Expected Results:
            An error should be returned indicating that the segment's size is
            too small.
        """
        min_segment_size = self.config.object_storage_api.slo_min_segment_size
        containers = []

        container_name = self.client.generate_unique_container_name('slo')
        containers.append(container_name)
        object_name = 'object'

        manifest = []

        segment_container_name = '{0}_{1}'.format(container_name, 'first')
        containers.append(segment_container_name)
        manifest.append({
            'container_name': segment_container_name,
            'name': '{0}.{1}'.format(object_name, 'first'),
            'size_bytes': min_segment_size,
            'data_pattern': 'first'})

        segment_container_name = '{0}_{1}'.format(container_name, 'middle')
        containers.append(segment_container_name)
        manifest.append({
            'container_name': segment_container_name,
            'name': '{0}.{1}'.format(object_name, 'middle'),
            'size_bytes': (min_segment_size - 1),
            'data_pattern': 'middle'})

        segment_container_name = '{0}_{1}'.format(container_name, 'last')
        containers.append(segment_container_name)
        manifest.append({
            'container_name': segment_container_name,
            'name': '{0}.{1}'.format(object_name, 'last'),
            'size_bytes': min_segment_size,
            'data_pattern': 'last'})

        self.addCleanup(self.client.force_delete_containers, containers)

        (seg_results, slo_results) = generate_static_large_object(
            self.client, container_name, object_name, manifest)

        r = slo_results['object_response']
        self.assertEqual(
            r.status_code, 400,
            'should return status code inidicating an error.')

        self.assertEqual(
            r.content,
            'Each segment, except the last, must be larger than {0} bytes.'
            .format(min_segment_size),
            'should return error indicating segment is too small.')

    @attr('regression', type='positive')
    def test_create_slo_manifest_with_slo_as_segment(self):
        """
        Scenario:
            Create a SLO where one of the segments is a SLO.

        Expected Results:
            An error should be returned indicating that this is not allowed.
        Note:
            This will be fixed in a future release.
        """
        min_segment_size = self.config.object_storage_api.slo_min_segment_size
        containers = []

        slo_container_name = self.client.generate_unique_container_name('slo')
        containers.append(slo_container_name)
        slo_object_name = 'object'
        slo_object_size = 0

        manifest = []
        for x in range(0, 3):
            segment_container_name = '{0}_{1}'.format(slo_container_name, x)
            containers.append(segment_container_name)
            segment_size = min_segment_size
            slo_object_size += segment_size
            manifest.append({
                'container_name': segment_container_name,
                'name': '{0}.{1}'.format(slo_object_name, x),
                'size_bytes': segment_size,
                'data_pattern': str(x)})

        self.addCleanup(self.client.force_delete_containers, containers)

        (seg_results, slo_results) = generate_static_large_object(
            self.client, slo_container_name, slo_object_name, manifest)
        self.assertTrue(
            slo_results['object_response'].ok, 'should create first slo.')

        r = self.client.get_storage_object_metadata(
            slo_container_name, slo_object_name)
        slo_etag = r.headers['etag'].replace('"', '')

        containers = []
        manifest = []

        container_name = self.client.generate_unique_container_name('slo2')
        containers.append(container_name)
        object_name = 'object2'

        r = self.client.create_container(container_name)

        segment_container_name = '{0}_{1}'.format(container_name, x)
        r = self.client.create_container(segment_container_name)
        containers.append(segment_container_name)

        segment_name = '{0}.{1}'.format(object_name, x)
        segment_data = generate_data_from_pattern('1', min_segment_size)
        segment_etag = get_md5_hash(segment_data)
        segment_size = len(segment_data)
        r = self.client.set_storage_object(
            segment_container_name, segment_name, content_length=segment_size,
            payload=segment_data)
        self.assertTrue(r.ok, 'should create slo2 segment.')

        manifest.append({
            'path': '/{0}/{1}'.format(segment_container_name, segment_name),
            'etag': segment_etag,
            'size_bytes': segment_size})

        manifest.append({
            'path': '/{0}/{1}'.format(slo_container_name, slo_object_name),
            'etag': slo_etag,
            'size_bytes': slo_object_size})

        slo_params = {'multipart-manifest': 'put'}
        slo_data = json.dumps(manifest)
        slo_size = len(slo_data)

        r = self.client.set_storage_object(
            container_name, object_name, content_length=slo_size,
            params=slo_params, payload=slo_data)
        self.assertEqual(
            r.status_code, 400, 'second SLO should not be created.')
        # TODO(rich5317): once this is fixed, check the message returned.

    @attr('regression', type='positive')
    def test_create_slo_manifest_with_dlo(self):
        """
        Scenario:
            Create a SLO where one of the segments is a DLO.

        Expected Results:
            Unknown, verify the system does not 500.
        """
        self.assertTrue(False, 'Write Test')

    @attr('regression', type='negative')
    def test_slo_creation_fails_with_invaild_manifest_json(self):
        """
        Scenario:
            Attempt to create a SLO where the manifest is composed of invalid
            JSON.

        Expected Results:
            An error should be returned indicating that invalid JSON was
            provided.
        """
        min_segment_size = self.config.object_storage_api.slo_min_segment_size
        containers = []
        manifest = []

        container_name = self.client.generate_unique_container_name('slo')
        containers.append(container_name)
        object_name = 'object2'

        r = self.client.create_container(container_name)

        segment_container_name = '{0}_1'.format(container_name)
        r = self.client.create_container(segment_container_name)
        containers.append(segment_container_name)

        segment_name = '{0}.1'.format(object_name)
        segment_data = generate_data_from_pattern('1', min_segment_size)
        segment_etag = get_md5_hash(segment_data)
        segment_size = len(segment_data)
        r = self.client.set_storage_object(
            segment_container_name, segment_name, content_length=segment_size,
            payload=segment_data)
        self.assertTrue(r.ok, 'should create slo2 segment.')

        manifest.append({
            'path': '/{0}/{1}'.format(segment_container_name, segment_name),
            'etag': segment_etag,
            'size_bytes': segment_size})

        slo_params = {'multipart-manifest': 'put'}
        invalid_json = '[{0}'.format(json.dumps(manifest))
        slo_size = len(invalid_json)

        r = self.client.set_storage_object(
            container_name, object_name, content_length=slo_size,
            params=slo_params, payload=invalid_json)
        self.assertEqual(
            r.status_code, 400, 'second SLO should not be created.')
        self.assertEqual(
            r.content, 'Manifest must be valid json.',
            'content should reflect invalid json.')

    @attr('regression', type='negative')
    def test_slo_creation_fails_with_invaild_manifest_missing_objects(self):
        """
        Scenario:
            Attempt to create a SLO where the manifest that contains no
            segments.

        Expected Results:
            An error should be returned indicating that objects are required.
        """
        min_segment_size = self.config.object_storage_api.slo_min_segment_size
        containers = []
        manifest = []

        container_name = self.client.generate_unique_container_name('slo')
        containers.append(container_name)
        object_name = 'object2'

        r = self.client.create_container(container_name)

        segment_container_name = '{0}_1'.format(container_name)
        r = self.client.create_container(segment_container_name)
        containers.append(segment_container_name)

        segment_name = '{0}.1'.format(object_name)
        segment_data = generate_data_from_pattern('1', min_segment_size)
        segment_etag = get_md5_hash(segment_data)
        segment_size = len(segment_data)

        # Never actually uplaod the segment.

        manifest.append({
            'path': '/{0}/{1}'.format(segment_container_name, segment_name),
            'etag': segment_etag,
            'size_bytes': segment_size})

        slo_params = {'multipart-manifest': 'put'}
        slo_data = json.dumps(manifest)
        slo_size = len(slo_data)

        r = self.client.set_storage_object(
            container_name, object_name, content_length=slo_size,
            params=slo_params, payload=slo_data)
        self.assertEqual(
            r.status_code, 400, 'second SLO should not be created.')

        error_message = '/{0}/{1}, 404 Not Found'.format(
            segment_container_name, segment_name)

        self.assertIn(
            error_message, r.content,
            'content should reflect a non-existant segment.')

    @attr('regression', type='negative')
    def test_slo_creation_fails_with_invaild_manifest_incorrect_etag(self):
        """
        Scenario:
            Attempt to create a SLO where the manifest that references a
             segment that does not exist.

        Expected Results:
            An error should be returned indicating that segment does not
            exist.
        """
        min_segment_size = self.config.object_storage_api.slo_min_segment_size
        containers = []
        manifest = []

        container_name = self.client.generate_unique_container_name('slo')
        containers.append(container_name)
        object_name = 'object2'

        r = self.client.create_container(container_name)

        segment_container_name = '{0}_1'.format(container_name)
        r = self.client.create_container(segment_container_name)
        containers.append(segment_container_name)

        segment_name = '{0}.1'.format(object_name)
        segment_data = generate_data_from_pattern('1', min_segment_size)
        segment_etag = get_md5_hash(segment_data)
        segment_size = len(segment_data)
        r = self.client.set_storage_object(
            segment_container_name, segment_name, content_length=segment_size,
            payload=segment_data)
        self.assertTrue(r.ok, 'should create slo2 segment.')

        invalid_etag = get_md5_hash(segment_size)
        manifest.append({
            'path': '/{0}/{1}'.format(segment_container_name, segment_name),
            'etag': invalid_etag,
            'size_bytes': segment_size})

        slo_params = {'multipart-manifest': 'put'}
        slo_data = json.dumps(manifest)
        slo_size = len(slo_data)

        r = self.client.set_storage_object(
            container_name, object_name, content_length=slo_size,
            params=slo_params, payload=slo_data)
        self.assertEqual(
            r.status_code, 400, 'second SLO should not be created.')

        error_message = '/{0}/{1}, Etag Mismatch'.format(
            segment_container_name, segment_name)
        self.assertIn(
            error_message, r.content,
            'content should reflect incorrect segment etag.')

    @attr('regression', type='negative')
    def test_slo_creation_fails_with_invaild_manifest_incorrect_size(self):
        """
        Scenario:
            Attempt to create a SLO where the manifest where a segment's size
            is incorrect.

        Expected Results:
            An error should be returned indicating that segment's size is
            incorrect.
        """
        min_segment_size = self.config.object_storage_api.slo_min_segment_size
        containers = []
        manifest = []

        container_name = self.client.generate_unique_container_name('slo')
        containers.append(container_name)
        object_name = 'object2'

        r = self.client.create_container(container_name)

        segment_container_name = '{0}_1'.format(container_name)
        r = self.client.create_container(segment_container_name)
        containers.append(segment_container_name)

        segment_name = '{0}.1'.format(object_name)
        segment_data = generate_data_from_pattern('1', min_segment_size)
        segment_etag = get_md5_hash(segment_data)
        segment_size = len(segment_data)
        r = self.client.set_storage_object(
            segment_container_name, segment_name, content_length=segment_size,
            payload=segment_data)
        self.assertTrue(r.ok, 'should create slo2 segment.')

        invalid_size = segment_size + 10
        manifest.append({
            'path': '/{0}/{1}'.format(segment_container_name, segment_name),
            'etag': segment_etag,
            'size_bytes': invalid_size})

        slo_params = {'multipart-manifest': 'put'}
        slo_data = json.dumps(manifest)
        slo_size = len(slo_data)

        r = self.client.set_storage_object(
            container_name, object_name, content_length=slo_size,
            params=slo_params, payload=slo_data)
        self.assertEqual(
            r.status_code, 400, 'second SLO should not be created.')

        error_message = '/{0}/{1}, Size Mismatch'.format(
            segment_container_name, segment_name)
        self.assertIn(
            error_message, r.content,
            'content should reflect incorrect segment size.')

    @attr('regression', type='positive', features='object_versioning')
    def test_slo_with_object_versioning(self):
        """
        Scenario:
            Create a SLO where container where the manifest/segments are
            created, has object versioning enabled.

        Expected Results:
            Unknown: might work. verify the system does not 500.
        """
        self.assertTrue(False, 'Write Test')

    @attr('regression', type='positive', features='cdn')
    def test_slo_retrieval_with_cdn_url(self):
        """
        Scenario:
            Retrieve a SLO over the CDN URL.

        Expected Results:
            Should retrive an exact copy of the SLO.

        Notes:
            The container for the manifest should be CDN enabled, but the
            containers for the segments should not be.
        """
        self.assertTrue(False, 'Write Test')

    @attr('regression', type='positive', features='cdn')
    def test_slo_retrieval_with_cdn_ssl(self):
        """
        Scenario:
            Retrieve a SLO over the CDN SSL URL.

        Expected Results:
            Should retrive an exact copy of the SLO.

        Notes:
            The container for the manifest should be CDN enabled, but the
            containers for the segments should not be.
        """
        self.assertTrue(False, 'Write Test')

    @attr('regression', type='positive', features='cdn')
    def test_slo_retrieval_with_cdn_streaming(self):
        """
        Scenario:
            Retrieve a SLO over the CDN streaming URL.

        Expected Results:
            Should retrive a copy slightly larger than the original SLO due
            to overhead associated with streaming.

        Notes:
            The container for the manifest should be CDN enabled, but the
            containers for the segments should not be.
        """
        self.assertTrue(False, 'Write Test')

    @attr('regression', type='positive', features='cdn')
    def test_slo_retrieval_with_cdn_ios_streaming(self):
        """
        Scenario:
            Retrieve a SLO over the CDN iOS streaming URL.

        Expected Results:
            Should retrive a copy slightly larger than the original SLO due
            to overhead associated with iOS streaming.

        Notes:
            The container for the manifest should be CDN enabled, but the
            containers for the segments should not be.
        """
        self.assertTrue(False, 'Write Test')

    @attr('regression', type='positive', features='cdn')
    def test_log_delivery_with_slo(self):
        """
        Scenario:
            Retrieve a SLO living in a container with log delivery enabled
            using a TempURL.

        Expected Results:
            Log lines should be generated reflecting the transaction.
        """
        self.assertTrue(False, 'Write Test')

    @attr('regression', type='positive', features='cdn')
    def test_log_delivery_with_cdn_url(self):
        """
        Scenario:
            Retrieve a SLO living in a container with CDN log delivery enabled
            using the CDN URL.

        Expected Results:
            Log lines should be generated reflecting the transaction.
            Enable log delivery on segment containers as well and verify what
            happens.
        """
        self.assertTrue(False, 'Write Test')

    @attr('regression', type='positive', features='cdn')
    def test_log_delivery_with_cdn_ssl(self):
        """
        Scenario:
            Retrieve a SLO living in a container with CDN log delivery enabled
            using the CDN SSL URL.

        Expected Results:
            Log lines should be generated reflecting the transaction.
            Enable log delivery on segment containers as well and verify what
            happens.
        """
        self.assertTrue(False, 'Write Test')

    @attr('regression', type='positive', features='cdn')
    def test_log_delivery_with_cdn_streaming(self):
        """
        Scenario:
            Retrieve a SLO living in a container with CDN log delivery enabled
            using the CDN Streaming URL.

        Expected Results:
            Log lines should be generated reflecting the transaction.
            Enable log delivery on segment containers as well and verify what
            happens.
        """
        self.assertTrue(False, 'Write Test')

    @attr('regression', type='positive', features='cdn')
    def test_log_delviery_with_cdn_ios_streaming(self):
        """
        Scenario:
            Retrieve a SLO living in a container with CDN log delivery enabled
            using the CDN iOS Streaming URL.

        Expected Results:
            Log lines should be generated reflecting the transaction.
            Enable log delivery on segment containers as well and verify what
            happens.
        """
        self.assertTrue(False, 'Write Test')

    @attr('regression', type='negative')
    def test_create_slo_manifest_with_large_content_length(self):
        """
        Scenario:
            Create a SLO manifest where the content length is larger than the
            content.

        Expected Results:
            Should return a 408.
        """
        self.assertTrue(False, 'Write Test')
