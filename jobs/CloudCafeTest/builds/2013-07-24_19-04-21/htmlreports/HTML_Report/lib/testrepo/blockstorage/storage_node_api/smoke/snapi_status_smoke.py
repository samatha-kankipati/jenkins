'''
@summary: Tests for Volumes Administration
@copyright: Copyright (c) 2012 Rackspace US, Inc.
'''
import os
from testrepo.common.testfixtures.blockstorage import StorageNodeAPIFixture
import unittest2 as unittest
from unittest2.suite import TestSuite
import json


class StorageNodeAPIStatusSmokeTest(StorageNodeAPIFixture):
    '''
        @summary: Basic smoke test for Storage Node Status API - All, API, Volumes, Backups, and Exports
    '''

    @unittest.skip("Makes swift connections and fails sometimes in lab.")
    def test_all_status(self):
        for snapi_client in self.snapi_clients:
            api_response = snapi_client.Status.all()
            self.assertTrue(api_response.ok, "Storage Node Status-All API call Failed: '%s'" % json.loads(api_response.content))

    def test_api_status(self):
        for snapi_client in self.snapi_clients:
            api_response = snapi_client.Status.api()
            self.assertTrue(api_response.ok, "Storage Node Status-API API call Failed: '%s'" % json.loads(api_response.content))

    def test_volumes_status(self):
        for snapi_client in self.snapi_clients:
            api_response = snapi_client.Status.volumes()
            self.assertTrue(api_response.ok, "Storage Node Status-Volumes API call Failed: '%s'" % json.loads(api_response.content))

    @unittest.skip("Makes swift connections and fails sometimes in lab.")
    def test_backups_status(self):
        for snapi_client in self.snapi_clients:
            api_response = snapi_client.Status.backups()
            self.assertTrue(api_response.ok, "Storage Node Status-Backups API call Failed: '%s'" % json.loads(api_response.content))

    def test_exports_status(self):
        for snapi_client in self.snapi_clients:
            api_response = snapi_client.Status.exports()
            self.assertTrue(api_response.ok, "Storage Node Status-Exports API call Failed: '%s'" % json.loads(api_response.content))

def load_tests(loader, standard_tests, pattern):
    suite = TestSuite()
    suite.addTest(StorageNodeAPIStatusSmokeTest("test_api_status"))
    suite.addTest(StorageNodeAPIStatusSmokeTest("test_volumes_status"))
    suite.addTest(StorageNodeAPIStatusSmokeTest("test_exports_status"))
    suite.addTest(StorageNodeAPIStatusSmokeTest("test_backups_status"))
    suite.addTest(StorageNodeAPIStatusSmokeTest("test_all_status"))
    return suite