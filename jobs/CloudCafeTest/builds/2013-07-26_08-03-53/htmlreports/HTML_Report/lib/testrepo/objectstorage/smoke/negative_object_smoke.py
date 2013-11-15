import unittest
from testrepo.common.testfixtures.object_storage_fixture \
        import ObjectStorageTestFixture


"""4.3 Negative Storage Object Services Smoke Tests"""


class NegativeObjectSmokeTest(ObjectStorageTestFixture):
    """4.3.2. Create/Update Object"""
    def test_object_creation_with_name_containing_null_byte(self):
        container_name = self.client.generate_unique_container_name()
        self.client.create_container(container_name)
        self.addCleanup(self.client.force_delete_containers, [container_name])

        object_name = self.client.generate_unique_object_name('%00')
        object_data = 'Test file data'
        content_length = str(len(object_data))
        r = self.client.set_storage_object(container_name, object_name,
                content_length=content_length, payload=object_data)
        self.assertEqual(r.status_code, 412, 'object should not be created.')
