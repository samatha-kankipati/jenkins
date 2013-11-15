'''
@summary: Basic smoke test for Storage Node Backup API - Create, List, Get Info, and Delete
@copyright: Copyright (c) 2012 Rackspace US, Inc.
'''
from datetime import datetime
import os
import unittest2 as unittest
from unittest2.suite import TestSuite
from testrepo.common.testfixtures.blockstorage import StorageNodeAPIFixture
from testrepo.common.testfixtures.fixtures import BaseTestFixture
from ccengine.domain.types import LunrVolumeStatusTypes
from ccengine.domain.blockstorage.storage_node_api import Volume as _VolumeDomainObject
import json

class StorageNodeAPIVolumeSmokeTest(StorageNodeAPIFixture):
    '''
    @summary: Basic smoke test for Storage Node Backup API - Create, List, Get Info, and Delete
    '''

    @classmethod
    def tearDownClass(cls):
        cls.StorageNodeAPIProvider.delete_storage_node_volumes(cls.snapi_clients, cls.expected_volumes)
        super(StorageNodeAPIVolumeSmokeTest, cls).tearDownClass()

    def test_create_volume(self):
        for snapi_client in self.snapi_clients:
            ONE_GIGABYTE = 1073741824

            created_volume, expected_name, expected_size = self.create_volume_for_assertion(snapi_client)
            self.assertEqual(created_volume.id, expected_name, "Volume not created with indicated name")
            ''' @TODO instead of hardcoding 1gb as bytes, convert the expected size from gb to bytes
                      or convert actual bytes to gb
            '''
            self.assertEqual(created_volume.size, ONE_GIGABYTE, "Volume not created with indicated size")
            api_response = snapi_client.Volumes.get_info(created_volume.id)
            actual_volume = _VolumeDomainObject(**json.loads(api_response.content))
            node_name = snapi_client.name
            self.expected_volumes[node_name] = actual_volume

    def test_list_volumes(self):
        for snapi_client in self.snapi_clients:
            api_response = snapi_client.Volumes.list()
            self.assertTrue(api_response.ok, "Storage Node List Volumes API call Failed: '%s'"
                                                                        % json.loads(api_response.content))
            actual_volumes = self.LunrAPIProvider.convert_json_to_domain_object_list(json.loads(api_response.content), _VolumeDomainObject)

            volume_id_list = []
            for volume in actual_volumes:
                volume_id_list.append(volume.id)

            node_name = snapi_client.name
            expected_volume_id = self.expected_volumes[node_name].id
            self.assertIn(expected_volume_id, volume_id_list, "Volume ID not in list")

    def test_get_volume_info(self):
        for snapi_client in self.snapi_clients:
            expected_volume_info = self.expected_volumes[snapi_client.name]
            volume_id = expected_volume_info.id
            api_response = snapi_client.Volumes.get_info(volume_id)
            self.assertTrue(api_response.ok, "Storage Node Get Volume Info API call Failed: '%s'"
                                                                        % json.loads(api_response.content))
            actual_volume = _VolumeDomainObject(**json.loads(api_response.content))
            self.assertEqual(expected_volume_info, actual_volume, "Volume info does not match")

    def test_delete_volume(self):
        for snapi_client in self.snapi_clients:
            volume = self.expected_volumes[snapi_client.name]
            api_response = snapi_client.Volumes.delete(volume.id)
            self.assertTrue(api_response.ok, "Storage Node Delete Volume API call Failed: '%s'"
                                                                        % json.loads(api_response.content))

            volume_deleted = self.StorageNodeAPIProvider.wait_for_volume_deleted(snapi_client, volume.id)
            self.assertTrue(volume_deleted, "Volume was not Deleted.")

    def create_volume_for_storage_node(self, storage_node_api_client):
        expected_name = "TestVolume_%d" % datetime.now().microsecond
        expected_size = 1
        api_response = storage_node_api_client.Volumes.create(expected_name, params={'size':expected_size})
        return api_response, expected_name, expected_size

    def create_volume_for_assertion(self, storage_node_api_client):
        api_response, expected_name, expected_size = self.create_volume_for_storage_node(storage_node_api_client)
        actual_volume = _VolumeDomainObject(**json.loads(api_response.content))

        if api_response.ok:
            self.fixture_log.info("Created Volume: %s on Node: %s" % (actual_volume.id, storage_node_api_client.name))
            return actual_volume, expected_name, expected_size
        else:
            self.fixture_log.warning(json.loads(api_response.content))
            return None

def load_tests(loader, standard_tests, pattern):
    suite = TestSuite()
    suite.addTest(StorageNodeAPIVolumeSmokeTest("test_create_volume"))
    suite.addTest(StorageNodeAPIVolumeSmokeTest("test_list_volumes"))
    suite.addTest(StorageNodeAPIVolumeSmokeTest("test_get_volume_info"))
    suite.addTest(StorageNodeAPIVolumeSmokeTest("test_delete_volume"))
    return suite