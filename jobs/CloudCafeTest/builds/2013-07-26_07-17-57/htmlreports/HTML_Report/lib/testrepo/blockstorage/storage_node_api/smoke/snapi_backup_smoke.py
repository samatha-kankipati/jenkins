'''
@summary: Basic smoke test for Storage Node Backup API - Create, List, Get Info, and Delete
@copyright: Copyright (c) 2012 Rackspace US, Inc.
'''
import os
import time
import unittest2 as unittest
from unittest2.suite import TestSuite
from testrepo.common.testfixtures.blockstorage import StorageNodeAPIFixture
from ccengine.domain.blockstorage.storage_node_api import Volume as _VolumeDomainObject, Backup as _BackupDomainObject
import json

class StorageNodeAPIBackupSmokeTest(StorageNodeAPIFixture):
    '''
    @summary: Basic smoke test for Storage Node Backup API - Create, List, Get Info, and Delete
    '''

    '''@TODO Complete this test, following the test strategy'''
    @classmethod
    def setUpClass(cls):
        '''
            @summary: Sets up smoke test by creating a volume for each Storage Node API Client
            These volumes will be used by the test to create backups for.
        '''
        super(StorageNodeAPIBackupSmokeTest, cls).setUpClass()

        #expected backups
        cls.expected_backups = {}

        #Create a volume on each storage node
        for snapi_client in cls.snapi_clients:
            created_volume = cls.StorageNodeAPIProvider.create_volume(snapi_client)
            api_response = snapi_client.Volumes.get_info(created_volume.id)
            volume = _VolumeDomainObject(**json.loads(api_response.content))
            node_name = snapi_client.name
            cls.expected_volumes[node_name] = volume

    @classmethod
    def tearDownClass(cls):
        cls.StorageNodeAPIProvider.delete_backups(cls.snapi_clients, cls.expected_volumes, cls.expected_backups)
        cls.StorageNodeAPIProvider.delete_storage_node_volumes(cls.snapi_clients, cls.expected_volumes)
        super(StorageNodeAPIBackupSmokeTest, cls).tearDownClass()

    def test_create_backup(self):
        '''
            @summary: Tests creation of backup using storage node API
        '''
        for snapi_client in self.snapi_clients:
            volume = self.expected_volumes[snapi_client.name]
            expected_backup_id = 'TestBackup_%s' % volume.id
            timestamp = int(time.time())
            api_response = snapi_client.Backups.create(volume.id, expected_backup_id, timestamp)

            self.assertTrue(api_response.ok, "Storage Node Create Backup API call Failed: '%s'"
                                                                        % json.loads(api_response.content))
            backup = _BackupDomainObject(**json.loads(api_response.content))
            self.StorageNodeAPIProvider.wait_for_storage_node_vol_backup_to_complete(snapi_client, volume.id, backup.id)
            self.assertEquals(backup.id, expected_backup_id)
            self.assertEquals(backup.origin, volume.id)
            self.assertEquals(backup.timestamp, timestamp)
            self.expected_backups[(snapi_client, volume.id)] = backup
            self.fixture_log.info("Created Backup: %s for Volume: %s on Node: %s" % (backup.id, volume.id, snapi_client.name))

    def test_list_backups(self):
        for snapi_client in self.snapi_clients:
            volume = self.expected_volumes[snapi_client.name]
            api_response = snapi_client.Backups.list(volume.id)
            self.assertTrue(api_response.ok, "Storage Node List Backups API call Failed: '%s'"
                                                                        % json.loads(api_response.content))
            actual_backups = json.loads(api_response.content).keys()
            expected_backup = self.expected_backups[(snapi_client, volume.id)]
            self.assertIn(expected_backup.id, actual_backups)

    def test_delete_backup(self):
        for snapi_client in self.snapi_clients:
            volume = self.expected_volumes[snapi_client.name]
            expected_backup = self.expected_backups[(snapi_client, volume.id)]
            api_response = snapi_client.Backups.delete(volume.id, expected_backup.id)
            self.assertTrue(api_response.ok, "Storage Node Delete Backup API call Failed: '%s'"
                                                                        % json.loads(api_response.content))

def load_tests(loader, standard_tests, pattern):
    suite = TestSuite()
    suite.addTest(StorageNodeAPIBackupSmokeTest("test_create_backup"))
    suite.addTest(StorageNodeAPIBackupSmokeTest("test_list_backups"))
    suite.addTest(StorageNodeAPIBackupSmokeTest("test_delete_backup"))
    return suite