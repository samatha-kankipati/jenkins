import unittest
from testrepo.common.testfixtures.object_storage_fixture \
        import ObjectStorageTestFixture


"""4.2 Negative Storage Container Services Smoke Tests"""


class NegativeContainerSmokeTest(ObjectStorageTestFixture):
    def test_container_creation_with_name_containing_null_byte(self):
        container_name = self.client.generate_unique_container_name('%00')
        r = self.client.create_container(container_name)
        self.addCleanup(self.client.force_delete_containers, [container_name])

        self.assertEqual(r.status_code, 412, 'container should not be created')
