import unittest
import os.path

from testrepo.common.testfixtures.object_storage_fixture \
        import ObjectStorageTestFixture


class AccessLogDeliveryTest(ObjectStorageTestFixture):

    def test_access_log_delivery_basic_positive(self):
        container_name = self.client.generate_unique_container_name(
                'autogen_access_log_delivery')
        r = self.client.create_container(container_name)
        # Container can not be deleted or access logs will not be generated
        self.addCleanup(self.client.force_delete_containers,
                        [container_name])
        # Log contianer name
        #self.fixture_log.info(''.join(['Container created for (',
        #        container_name, ')'])
        self.assertTrue(r.status_code == 201 or r.status_code == 202,
                'container creation should return HTTP 201 or 202')

        #Enable Access Log Delivery for Container
        headers = {'X-Container-Meta-Access-Log-Delivery': 'true'}
        r = self.client.update_container(container_name, headers)
        self.assertEqual(r.status_code, 202,
                'enabling log delivery should return HTTP 202')

        #Do things to the container
        #CDN-ENABLE Container
        headers = {'X-CDN-Enabled': 'true'}
        r = self.client.update_container(container_name, headers)
        self.assertTrue(r.status_code == 201 or r.status_code == 202,
                'enabling CDN should return HTTP 202')

        #SET Container Metadata
        headers = {'X-Container-Meta-AccessLogTest': '123'}
        r = self.client.update_container(container_name, headers)
        self.assertEqual(r.status_code, 202,
                'setting container metadata should return HTTP 202')

        #GET Container Metadata
        r = self.client.get_container_metadata(container_name)
        self.assertEqual(r.status_code, 204,
                'getting contianer metadata should return HTTP 204')
        self.assertTrue('x-container-meta-accesslogtest' in r.headers,
                'retrieving container metadata should contain key')
        self.assertEquals(r.headers['x-container-meta-accesslogtest'], '123',
                'retrieving container metadata should be 123')

        #Upload a file to the container
        object_name = 'test_object'
        object_data = 'abcdefghijklmnopqrstuvwxyz'
        content_length = str(len(object_data))
        r = self.client.set_storage_object(
                container_name,
                object_name,
                content_length=content_length,
                payload=object_data)

        # TODO(rich5317): do we need to check for a HTTP 100 here?
        self.assertEqual(r.status_code, 201,
                'creating an object should return a HTTP 201')

        #HEAD Request on test file
        r = self.client.get_storage_object_metadata(container_name,
                object_name)
        self.assertEqual(r.status_code, 200,
                'retrieving object metadata should return HTTP 200')

        #RANGE Request on test file
        headers = {'Range': 'bytes=5-10'}
        r = self.client.get_storage_object(container_name,
                                                       object_name,
                                                       headers=headers)

        self.assertEqual(r.status_code, 206,
                'retriving partial object should return HTTP 206')

        #GET Request Test File
        r = self.client.get_storage_object(container_name,
                                                       object_name)
        self.assertEqual(r.status_code, 200,
                'retrieving object should return HTTP 200')
