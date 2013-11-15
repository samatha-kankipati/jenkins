import os.path
import unittest

from testrepo.common.testfixtures.object_storage_fixture \
        import ObjectStorageTestFixture


#these need to be moved to a config
CONTENT_TYPE_TEXT = 'text/plain; charset=UTF-8'


"""4.2 Storage Container Services Smoke Tests"""


class ContainerSmokeTest(ObjectStorageTestFixture):
    """4.2.1. List Objects in a Container"""
    def test_objects_list_with_non_empty_container(self):
        container_name = self.client.generate_unique_container_name()
        self.client.create_container(container_name)
        self.addCleanup(self.client.force_delete_containers,
                        [container_name])

        file_data = 'Test file data'
        content_length = str(len(file_data))
        object_name = self.client.generate_unique_object_name()
        self.client.set_storage_object(
                container_name,
                object_name,
                content_length=content_length,
                content_type=CONTENT_TYPE_TEXT,
                payload=file_data)

        r = self.client.list_objects(container_name)
        self.assertEqual(r.status_code, 200, 'should list object')

    """4.2.1.1. Serialized List Output"""
    def test_objects_list_with_format_json_query_parameter(self):
        container_name = self.client.generate_unique_container_name()
        self.client.create_container(container_name)
        self.addCleanup(self.client.force_delete_containers,
                        [container_name])

        file_data = 'Test file data'
        content_length = str(len(file_data))
        object_name = self.client.generate_unique_object_name()
        self.client.set_storage_object(
                container_name,
                object_name,
                content_length=content_length,
                content_type=CONTENT_TYPE_TEXT,
                payload=file_data)

        format = {'format': 'json'}
        r = self.client.list_objects(container_name, params=format)
        self.assertEqual(r.status_code, 200,
                'should list object using content-type json')

    def test_objects_list_with_format_xml_query_parameter(self):
        container_name = self.client.generate_unique_container_name()
        self.client.create_container(container_name)
        self.addCleanup(self.client.force_delete_containers,
                        [container_name])

        file_data = 'Test file data'
        content_length = str(len(file_data))
        object_name = self.client.generate_unique_object_name()
        self.client.set_storage_object(
                container_name,
                object_name,
                content_length=content_length,
                content_type=CONTENT_TYPE_TEXT,
                payload=file_data)

        format = {'format': 'xml'}
        r = self.client.list_objects(container_name, params=format)
        self.assertEqual(r.status_code, 200,
                'should list object using content-type xml')

    def test_object_list_with_accept_header(self):
        container_name = self.client.generate_unique_container_name()
        self.client.create_container(container_name)
        self.addCleanup(self.client.force_delete_containers,
                        [container_name])

        file_data = 'Test file data'
        content_length = str(len(file_data))
        object_name = self.client.generate_unique_object_name()
        self.client.set_storage_object(
                container_name,
                object_name,
                content_length=content_length,
                content_type=CONTENT_TYPE_TEXT,
                payload=file_data)

        headers = {'Accept': '*/*'}
        r = self.client.list_objects(container_name,
                                                 headers=headers)
        self.assertEqual(r.status_code, 200,
                'should list objects using content-type text/plain')

    def test_object_list_with_text_accept_header(self):
        container_name = self.client.generate_unique_container_name()
        self.client.create_container(container_name)
        self.addCleanup(self.client.force_delete_containers,
                        [container_name])

        file_data = 'Test file data'
        content_length = str(len(file_data))
        object_name = self.client.generate_unique_object_name()
        self.client.set_storage_object(
                container_name,
                object_name,
                content_length=content_length,
                content_type=CONTENT_TYPE_TEXT,
                payload=file_data)

        headers = {'Accept': 'text/plain'}
        r = self.client.list_objects(container_name,
                                                 headers=headers)
        self.assertEqual(r.status_code, 200,
                'should list objects using content-type text/plain')

    def test_object_list_with_json_accept_header(self):
        container_name = self.client.generate_unique_container_name()
        self.client.create_container(container_name)
        self.addCleanup(self.client.force_delete_containers,
                        [container_name])

        file_data = 'Test file data'
        content_length = str(len(file_data))
        object_name = self.client.generate_unique_object_name()
        self.client.set_storage_object(
                container_name,
                object_name,
                content_length=content_length,
                content_type=CONTENT_TYPE_TEXT,
                payload=file_data)

        headers = {'Accept': 'application/json'}
        r = self.client.list_objects(container_name,
                                                 headers=headers)
        self.assertEqual(r.status_code, 200,
                'should list objects using content-type application/json')

    def test_object_list_with_xml_accept_header(self):
        container_name = self.client.generate_unique_container_name()
        self.client.create_container(container_name)
        self.addCleanup(self.client.force_delete_containers,
                        [container_name])

        file_data = 'Test file data'
        content_length = str(len(file_data))
        object_name = self.client.generate_unique_object_name()
        self.client.set_storage_object(
                container_name,
                object_name,
                content_length=content_length,
                content_type=CONTENT_TYPE_TEXT,
                payload=file_data)

        headers = {'Accept': 'application/xml'}
        r = self.client.list_objects(container_name,
                                                 headers=headers)
        self.assertEqual(r.status_code, 200,
                'should list objects using content-type application/xml')

        headers = {'Accept': 'text/xml'}
        r = self.client.list_objects(container_name,
                                                 headers=headers)
        self.assertEqual(r.status_code, 200,
                'should list objects using content-type text/xml')

    """4.2.1.2. Controlling a Large List of Objects"""
    def test_objects_list_with_limit_query_parameter(self):
        container_name = self.client.generate_unique_container_name()
        self.client.create_container(container_name)
        self.addCleanup(self.client.force_delete_containers,
                        [container_name])

        file_data = 'Test file data'
        content_length = str(len(file_data))
        object_name = self.client.generate_unique_object_name()
        self.client.set_storage_object(
                container_name,
                object_name,
                content_length=content_length,
                content_type=CONTENT_TYPE_TEXT,
                payload=file_data)

        limit = {'limit': '3'}
        r = self.client.list_objects(container_name, params=limit)
        self.assertEqual(r.status_code, 200, 'should list object')

    def test_objects_list_with_marker_query_parameter(self):
        container_name = self.client.generate_unique_container_name()
        self.client.create_container(container_name)
        self.addCleanup(self.client.force_delete_containers,
                        [container_name])

        file_data = 'Test file data'
        content_length = str(len(file_data))
        object_name = self.client.generate_unique_object_name()
        self.client.set_storage_object(
                container_name,
                object_name,
                content_length=content_length,
                content_type=CONTENT_TYPE_TEXT,
                payload=file_data)

        marker = {'marker': container_name}
        r = self.client.list_objects(container_name, params=marker)
        self.assertEqual(r.status_code, 200, 'should list object')

    """4.2.1.3. Pseudo-Hierarchical Folders/Directories"""
    def test_objects_list_with_prefix_query_parameter(self):
        container_name = self.client.generate_unique_container_name()
        self.client.create_container(container_name)
        self.addCleanup(self.client.force_delete_containers,
                        [container_name])

        file_data = 'Test file data'
        content_length = str(len(file_data))
        object_name = self.client.generate_unique_object_name()
        self.client.set_storage_object(
                container_name,
                object_name,
                content_length=content_length,
                content_type=CONTENT_TYPE_TEXT,
                payload=file_data)

        prefix = {'prefix': container_name[0:3]}
        r = self.client.list_objects(container_name, params=prefix)
        self.assertEqual(r.status_code, 200, 'should list object')

    """
    This is a depricated feature that has little documentation.
    The following things need to be done for the path parameter to work.
      1. For every 'directory' a 'directory marker' must be added as a object.
         The directory marker does not need to contain data, and thus can have
         a length of 0.
         Example: If you want a directory 'foo/bar/', you would upload a
                  object named 'foo/bar/' to your container.

      2. You must upload your objects, prefixed with the 'directory' path.
         Example: If you wanted to create an object in 'foo/' and another in
                  'foo/bar/', you would have to name the objects as follows:
                    foo/object1.txt
                    foo/bar/object2.txt

      3. Once this has been done, you can use the path query string parameter
         to list the objects in the simulated directory structure.
         Example: Using the above examples, setting path to 'foo/' should list
                  the following:
                    foo/objet1.txt
                    foo/bar/
    """
    def test_objects_list_with_path_query_parameter(self):
        container_name = self.client.generate_unique_container_name()
        self.client.create_container(container_name)
        self.addCleanup(self.client.force_delete_containers,
                        [container_name])

        dir_marker = 'path_test/'
        self.client.set_storage_object(
                container_name,
                dir_marker,
                content_length=0,
                content_type=CONTENT_TYPE_TEXT,
                payload='')

        dir_marker = 'path_test/nested_dir/'
        self.client.set_storage_object(
                container_name,
                dir_marker,
                content_length=0,
                content_type=CONTENT_TYPE_TEXT,
                payload='')

        file_data = 'Test file data'
        content_length = str(len(file_data))
        object_name_prefix = 'path_test/nested_dir/'
        object_name_postfix = self.client.generate_unique_object_name()
        object_name = ''.join([object_name_prefix, object_name_postfix])
        self.client.set_storage_object(
                container_name,
                object_name,
                content_length=content_length,
                content_type=CONTENT_TYPE_TEXT,
                payload=file_data)

        params = {'path': 'path_test/'}
        r = self.client.list_objects(container_name, params=params)
        self.assertEqual(r.status_code, 200,
                'should list the simulated directory')

        params = {'path': 'path_test/nested_dir/'}
        r = self.client.list_objects(container_name, params=params)
        self.assertEqual(r.status_code, 200,
                'should list the object in the simulated directory')

    def test_objects_list_with_delimiter_query_parameter(self):
        container_name = self.client.generate_unique_container_name()
        self.client.create_container(container_name)
        self.addCleanup(self.client.force_delete_containers,
                        [container_name])

        file_data = 'Test file data'
        content_length = str(len(file_data))
        object_name_prefix = 'delimiter_test/'
        object_name_postfix = self.client.generate_unique_object_name()
        object_name = ''.join([object_name_prefix, object_name_postfix])
        self.client.set_storage_object(
                container_name,
                object_name,
                content_length=content_length,
                content_type=CONTENT_TYPE_TEXT,
                payload=file_data)

        params = {'delimiter': '/'}
        r = self.client.list_objects(container_name, params=params)
        self.assertEqual(r.status_code, 200,
                'should list the simulated directory')

        params = {'prefix': object_name_prefix, 'delimiter': '/'}
        r = self.client.list_objects(container_name, params=params)
        self.assertEqual(r.status_code, 200,
                'should list the object in the simulated directory')

    """4.2.2. Create Container"""
    def test_container_creation_with_valid_container_name(self):
        container_name = self.client.generate_unique_container_name()
        r = self.client.create_container(container_name)
        self.addCleanup(self.client.force_delete_containers,
                        [container_name])

        self.assertEqual(r.status_code, 201, 'should be created')

    def test_container_creation_with_existing_container_name(self):
        container_name = self.client.generate_unique_container_name()
        r = self.client.create_container(container_name)
        self.addCleanup(self.client.force_delete_containers,
                        [container_name])
        self.assertEqual(r.status_code, 201, 'should be created')

        r = self.client.create_container(container_name)
        self.assertEqual(r.status_code, 202, 'should be successful')

    def test_container_creation_with_metadata(self):
        container_name = self.client.generate_unique_container_name()
        metadata = {'Book-One': 'fight_club',
                    'Book-Two': 'a_clockwork_orange'}
        r = self.client.create_container(container_name,
                                                     metadata=metadata)
        self.addCleanup(self.client.force_delete_containers,
                        [container_name])
        self.assertEqual(r.status_code, 201, 'should be created')

    """4.2.3. Delete Container"""
    def test_container_deletion_with_existing_empty_container(self):
        container_name = self.client.generate_unique_container_name()
        r = self.client.create_container(container_name)
        self.addCleanup(self.client.force_delete_containers,
                        [container_name])
        self.assertEqual(r.status_code, 201, 'should be created')

        r = self.client.delete_container(container_name)
        self.assertEqual(r.status_code, 204, 'should be deleted')

        r = self.client.list_objects(container_name)
        self.assertEqual(r.status_code, 404,
                'should not exist after deletion')

    """4.2.4. Retrieve Container Metadata"""
    def test_metadata_retrieval_with_newly_created_container(self):
        container_name = self.client.generate_unique_container_name()
        metadata = {'Book-One': 'fight_club',
                    'Book-Two': 'a_clockwork_orange'}
        r = self.client.create_container(container_name, metadata)
        self.addCleanup(self.client.force_delete_containers,
                        [container_name])
        self.assertEqual(r.status_code, 201, 'should be created')

        r = self.client.get_container_metadata(container_name)
        self.assertEqual(r.status_code, 204,
                'new container should return metadata')

    def test_metadata_retrieval_with_container_possessing_metadata(self):
        container_name = self.client.generate_unique_container_name()
        self.client.create_container(container_name)
        self.addCleanup(self.client.force_delete_containers,
                        [container_name])

        metadata = {'Book-One': 'fight_club',
                    'Book-Two': 'a_clockwork_orange'}
        r = self.client.set_container_metadata(container_name,
                                                           metadata)

        r = self.client.get_container_metadata(container_name)
        self.assertEqual(r.status_code, 204,
                'container should return metadata')

    """4.2.5. Create/Update Container Metadata"""
    def test_metadata_update_with_container_possessing_metadata(self):
        container_name = self.client.generate_unique_container_name()
        x = self.client.create_container(container_name)
        self.addCleanup(self.client.force_delete_containers,
                        [container_name])
        metadata = {'Book-One': 'fight_club',
                    'Book-Two': 'a_clockwork_orange'}
        r = self.client.set_container_metadata(container_name,
                                                           metadata)
        self.assertEqual(r.status_code, 204, 'metadata should be added')

        metadata = {'Book-One': 'Fight_Club'}
        r = self.client.set_container_metadata(container_name,
                                                           metadata)
        self.assertEqual(r.status_code, 204, 'metadata should be updated')
