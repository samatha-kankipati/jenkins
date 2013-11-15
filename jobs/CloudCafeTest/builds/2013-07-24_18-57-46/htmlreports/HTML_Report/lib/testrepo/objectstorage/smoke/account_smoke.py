import unittest

from testrepo.common.testfixtures.object_storage_fixture \
        import ObjectStorageTestFixture


# TODO: fix the tests to account for 200 or 204 empty and non empty


"""4.1 Storage Account Services Smoke Tests"""


class AccountSmokeTest(ObjectStorageTestFixture):

    """4.1.1. List Containers"""
    def test_container_list_with_non_empty_account(self):
        r = self.client.list_containers()
        self.assertEqual(r.status_code, 200, 'should list containers')

    """4.1.1.1. Serialized List Output"""
    def test_container_list_with_format_json_query_parameter(self):
        format = {'format': 'json'}
        r = self.client.list_containers(params=format)
        self.assertEqual(r.status_code, 200,
                'should list containers using content-type json')

    def test_container_list_with_format_xml_query_parameter(self):
        format = {'format': 'xml'}
        r = self.client.list_containers(params=format)
        self.assertEqual(r.status_code, 200,
                'should list containers using content-type xml')

    def test_container_list_with_accept_header(self):
        headers = {'Accept': '*/*'}
        r = self.client.list_containers(headers=headers)
        self.assertEqual(r.status_code, 200,
                'should list containers using content-type text/plain')

    def test_container_list_with_text_accept_header(self):
        headers = {'Accept': 'text/plain'}
        r = self.client.list_containers(headers=headers)
        self.assertEqual(r.status_code, 200,
                'should list containers using content-type text/plain')

    def test_container_list_with_json_accept_header(self):
        headers = {'Accept': 'application/json'}
        r = self.client.list_containers(headers=headers)
        self.assertEqual(r.status_code, 200,
                'should list containers using content-type application/json')

    def test_container_list_with_xml_accept_header(self):
        headers = {'Accept': 'application/xml'}
        r = self.client.list_containers(headers=headers)
        self.assertEqual(r.status_code, 200,
                'should list containers using content-type application/xml')

        headers = {'Accept': 'text/xml'}
        r = self.client.list_containers(headers=headers)
        self.assertEqual(r.status_code, 200,
                'should list containers using content-type text/xml')

    """4.1.1.2. Controlling a Large List of Containers"""
    def test_container_list_with_limit_query_parameter(self):
        limit = {'limit': '10'}
        r = self.client.list_containers(params=limit)
        self.assertEqual(r.status_code, 200, 'should list containers')

    def test_container_list_with_marker_query_parameter(self):
        marker = {'marker': 'a'}
        r = self.client.list_containers(params=marker)
        self.assertEqual(r.status_code, 200, 'should list containers')

    def test_container_list_with_limit_and_marker_query_parameters(self):
        limit_marker = {'limit': '3', 'marker': 'a'}
        r = self.client.list_containers(params=limit_marker)
        self.assertEqual(r.status_code, 200, 'should list containers')

    def test_container_list_with_limit_marker_and_format_json_query_parameters(self):
        limit_marker_format = {'limit': '3', 'marker': 'a', 'format': 'json'}
        r = self.client.list_containers(params=limit_marker_format)
        self.assertEqual(r.status_code, 200, 'should list containers')

    def test_container_list_with_limit_marker_and_format_xml_query_parameters(self):
        limit_marker_format = {'limit': '3', 'marker': 'a', 'format': 'xml'}
        r = self.client.list_containers(params=limit_marker_format)
        self.assertEqual(r.status_code, 200, 'should list containers')

    """4.1.2. Retrieve Account Metadata"""
    def test_metadata_retrieval_with_existing_account(self):
        r = self.client.retrieve_account_metadata()
        self.assertEqual(r.status_code, 204, 'should return metadata')
