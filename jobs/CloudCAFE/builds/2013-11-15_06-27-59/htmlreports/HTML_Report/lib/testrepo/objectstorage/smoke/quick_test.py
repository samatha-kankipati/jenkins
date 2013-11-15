import unittest

from testrepo.common.testfixtures.object_storage_fixture \
        import ObjectStorageTestFixture


#these need to be moved to a config
CONTENT_TYPE_TEXT = 'text/plain; charset=UTF-8'


class QuickTest(ObjectStorageTestFixture):
    def test_object_deletion_with_valid_object(self):
        container_name = self.client.generate_unique_container_name()
        x = self.client.create_container(container_name)
        self.addCleanup(self.client.force_delete_containers, [container_name])
        self.assertEqual(x.status_code, 201, 'container should be created')

        object_name = self.client.generate_unique_object_name()
        object_data = 'Test file data'
        content_length = str(len(object_data))
        x = self.client.set_storage_object(container_name,
                object_name, content_length=content_length,
                content_type=CONTENT_TYPE_TEXT, payload=object_data)

        self.assertEqual(x.status_code, 201, 'should be created')

        x = self.client.delete_storage_object(container_name, object_name)
        self.assertEqual(x.status_code, 204, 'should be deleted')

        x = self.client.get_storage_object(container_name, object_name)
        self.assertEqual(x.status_code, 404,
                'should not be accessible after deletion')
