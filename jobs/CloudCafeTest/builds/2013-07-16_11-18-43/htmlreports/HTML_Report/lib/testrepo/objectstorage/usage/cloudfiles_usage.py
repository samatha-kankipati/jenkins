"""This is a stub for the new billing test"""
import calendar
import datetime
import time
import hashlib
import os.path
import sys
import unittest

from testrepo.common.testfixtures.object_storage_fixture \
        import CloudFilesTestFixture


CONTAINER_NAME = 'longshot'
OBJ_NAME = 'longshot_object'
UPLOAD_FILE = '/home/sn1p3r/Cloudfiles-Test-Repo/uploads/testfile.txt'
GZIP_FILE = '/home/sn1p3r/Cloudfiles-Test-Repo/uploads/testfile.gzip'
CONTENT_TYPE_TEXT = 'text/plain; charset=UTF-8'


class UsageTest(CloudFilesTestFixture):

    def test_bandwidth_usage_happy_path(self):
        container_1 = self.client.generate_unique_container_name()
        container_2 = self.client.generate_unique_container_name()
        container_3 = self.client.generate_unique_container_name()

        self.client.create_container(container_1)
        self.client.create_container(container_2)
        self.client.create_container(container_3)

        self.addCleanup(self.client.force_delete_containers, [container_1,
                container_2, container_3])

        #object_name = self.client.generate_unique_object_name()
        #object_data = 'Test file data'
        #content_length = str(len(object_data))
        #self.client.set_storage_object(container_name, object_name,
        #        content_length=content_length,
        #        content_type=CONTENT_TYPE_TEXT,
        #        payload=object_data)
        #
        #r = self.client.get_storage_object(container_name, object_name)
        #self.assertEqual(r.status_code, 200, 'should return object.')
