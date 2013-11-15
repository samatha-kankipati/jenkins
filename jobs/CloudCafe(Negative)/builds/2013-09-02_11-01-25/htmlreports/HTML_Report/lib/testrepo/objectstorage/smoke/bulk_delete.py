"""
Tests Swfit Bulk Delete Operations:
http://docs.openstack.org/developer/swift/misc.html#module-swift.common.middleware.bulk
"""
import re

from testrepo.common.testfixtures.object_storage_fixture \
    import ObjectStorageTestFixture

BULK_DELETE_MAX_COUNT = 1000


class BulkDeleteSmokeTest(ObjectStorageTestFixture):
    """
    Will delete multiple objects or containers from their account with a
    single request.
    """

    def test_bulk_deletion_of_multiple_objects(self):
        """
        Bulk Delete Test Scenarios
        Verify user can delete multiple objects from a container
        """
        container_name = \
            self.client.generate_unique_container_name('bulk_delete')
        self.client.create_container(container_name)
        self.addCleanup(self.client.force_delete_containers, [container_name])

        objects_to_remain = [
            'object10',
            'object20',
            'object30',
            'object40']

        objects_to_delete = [
            'object1',
            'object2',
            'object3',
            'object4']

        self.client.create_bulk_objects(
            container_name, objects_to_remain + objects_to_delete)

        targets = [
            '{0}/{1}'.format(container_name, x) for x in objects_to_delete]

        r = self.client.bulk_delete(targets)
        self.assertTrue(r.ok, 'should return report.')

        self.assertTrue(
            re.search('Number Deleted:', r.content),
            'should contain "Number Deleted" in the report returned.')

        number_deleted = \
            int(re.findall('Number Deleted: (\d+)', r.content)[0])
        self.assertEqual(
            number_deleted, len(objects_to_delete),
            'should delete objects in the deletion list.')

        self.assertTrue(
            re.search('Number Not Found:', r.content),
            'should contain "Number Not Found" in the report returned.')

        not_found_count = \
            int(re.findall('Number Not Found: (\d+)', r.content)[0])
        self.assertEqual(
            not_found_count, 0,
            'should have found all objects to be removed.')

        c = self.client.get_object_count(container_name)
        self.assertEqual(
            c, len(objects_to_remain),
            'should not remove objects with similar names.')

    def test_bulk_deletion_of_all_objects(self):
        """
        Verify user can delete all objects in a container then the newly empty
        container
        """
        container_name = \
            self.client.generate_unique_container_name('bulk_delete')
        self.client.create_container(container_name)
        self.addCleanup(self.client.force_delete_containers, [container_name])

        objects_list = ['object{0}'.format(x) for x in range(1, 10)]

        self.client.create_bulk_objects(container_name, objects_list)

        targets = [
            '{0}/{1}'.format(container_name, x) for x in objects_list]

        targets = targets + [container_name]

        r = self.client.bulk_delete(targets)
        self.assertTrue(r.ok, 'should return report.')

        self.assertTrue(
            re.search('Number Deleted:', r.content),
            'should contain "Number Deleted" in the report returned.')

        number_deleted = \
            int(re.findall('Number Deleted: (\d+)', r.content)[0])
        self.assertEqual(
            number_deleted, len(targets),
            'should delete objects in the deletion list.')

        self.assertTrue(
            re.search('Number Not Found:', r.content),
            'should contain "Number Not Found" in the report returned.')

        not_found_count = \
            int(re.findall('Number Not Found: (\d+)', r.content)[0])
        self.assertEqual(
            not_found_count, 0,
            'should have found all objects to be removed.')

        r = self.client.list_objects(container_name)
        self.assertEqual(
            r.status_code, 404,
            'container and all objects should have been deleted.')

    def test_bulk_delete_max_count(self):
        """
        Verify user can delete the max count
        """
        container_name = \
            self.client.generate_unique_container_name('bulk_delete')
        self.client.create_container(container_name)
        self.addCleanup(self.client.force_delete_containers, [container_name])

        max_objects = ['object{0}'.format(x + 1) for x in range(
            0, BULK_DELETE_MAX_COUNT)]

        self.client.create_bulk_objects(container_name, max_objects)

        targets = [
            '{0}/{1}'.format(container_name, x) for x in max_objects]

        targets = targets

        r = self.client.bulk_delete(targets)
        self.assertTrue(r.ok, 'should return report.')

        self.assertTrue(
            re.search('Number Deleted:', r.content),
            'should contain "Number Deleted" in the report returned.')

        number_deleted = \
            int(re.findall('Number Deleted: (\d+)', r.content)[0])
        self.assertEqual(
            number_deleted, len(targets),
            'should delete objects in the deletion list.')

        self.assertTrue(
            re.search('Number Not Found:', r.content),
            'should contain "Number Not Found" in the report returned.')

        not_found_count = \
            int(re.findall('Number Not Found: (\d+)', r.content)[0])
        self.assertEqual(
            not_found_count, 0,
            'should have found all objects to be removed.')

    def test_cant_bulk_delete_above_max_count(self):
        """
        """
        container_name = \
            self.client.generate_unique_container_name('bulk_delete')
        self.client.create_container(container_name)
        self.addCleanup(self.client.force_delete_containers, [container_name])

        total_objects = ['object{0}'.format(x) for x in range(
            0, BULK_DELETE_MAX_COUNT + 1)]
        self.client.create_bulk_objects(container_name, total_objects)

        targets = [
            '{0}/{1}'.format(container_name, x) for x in total_objects]

        r = self.client.bulk_delete(targets)
        self.assertEqual(
            r.status_code, 413, 'should not delete objects over max count.')

    def test_bulk_deletion_empty_list(self):
        """
        Verify recieve an error when an empty list is sent.
        """
        container_name = \
            self.client.generate_unique_container_name('bulk_delete')
        self.client.create_container(container_name)
        self.addCleanup(self.client.force_delete_containers, [container_name])

        max_objects = ['object{0}'.format(x + 1) for x in range(0, 10)]
        total_objects = max_objects + ['extra_object']

        self.client.create_bulk_objects(container_name, total_objects)

        targets = ''

        r = self.client.bulk_delete(targets)
        self.assertEqual(r.status_code, 400, 'should return error.')
