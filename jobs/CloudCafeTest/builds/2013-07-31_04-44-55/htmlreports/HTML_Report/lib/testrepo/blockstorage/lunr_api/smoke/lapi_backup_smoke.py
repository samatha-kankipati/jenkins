'''
@summary: Basic smoke test for Lunr Backup API - Create, List, Get Info, Update, and Delete
@copyright: Copyright (c) 2012 Rackspace US, Inc.
'''
from datetime import datetime
from testrepo.common.testfixtures.blockstorage import LunrAPIFixture
from ccengine.domain.types import LunrVolumeStatusTypes, LunrBackupStatusTypes
from ccengine.domain.blockstorage.lunr_api import Volume as _VolumeDomainObject, Backup as _BackupDomainObject
from unittest2.suite import TestSuite
import json

class LunrBackupAPISmokeTest(LunrAPIFixture):
    '''
    @summary: Basic smoke test for Lunr Backup API - Create, List, Get Info, Update, and Delete
    '''
    @classmethod
    def setUpClass(cls):
        super(LunrBackupAPISmokeTest, cls).setUpClass()

        #Create User Client
        cls.user_client = cls.LunrAPIProvider.create_user_client()
        cls.fixture_log.info("Created Account: %s" % cls.user_client.account_name)

        #Create Volumes
        cls.vtypes = json.loads(cls.admin_client.VolumeTypes.list().content)
        cls.expected_volumes = []
        for vtype in cls.vtypes:
            created_volume = cls.LunrAPIProvider.create_volume_for_user(cls.user_client, vtype)
            if created_volume is None:
                raise Exception("Could not create a volume with Active status")
            cls.expected_volumes.append(created_volume)

        #Expected Backup
        cls.expected_backups = []

    @classmethod
    def tearDownClass(cls):
        cls.LunrAPIProvider.delete_user_backups(cls.user_client)
        cls.LunrAPIProvider.delete_user_volumes(cls.user_client)
        cls.admin_client.Accounts.delete(cls.user_client.account_id)
        cls.fixture_log.info("Deleting Account: %s" % cls.user_client.account_name)
        super(LunrBackupAPISmokeTest, cls).tearDownClass()

    def test_create_backup(self):
        for volume in self.expected_volumes:
            backup_name = "Backup_%d" % datetime.now().microsecond
            api_response = self.user_client.Backups.create(backup_name, params={'volume': volume.id})
            self.assertTrue(api_response.ok, "API call failed:'%s'" % json.loads(api_response.content))

            created_backup = _BackupDomainObject(**json.loads(api_response.content))
            self.fixture_log.info("Creating Backup: %s" % created_backup.id)

            wait_status = self.LunrAPIProvider.wait_for_volume_backup_status(created_backup.id, LunrBackupStatusTypes.READY, user_client=self.user_client)
            self.assertTrue(wait_status.ok, "Backup '%s' status never became %s" % (created_backup.id, LunrBackupStatusTypes.READY))

            api_response = self.user_client.Backups.get_info(created_backup.id)
            created_backup = _BackupDomainObject(**json.loads(api_response.content))
            self.assertEqual(created_backup.id, backup_name, "Backup not given correct name")
            self.assertEqual(created_backup.size, volume.size, "Backup not given correct size")

            self.expected_backups.append(created_backup)

    def test_list_backups(self):
        api_response = self.user_client.Backups.list()
        self.assertTrue(api_response.ok, "List Backups API call failed: '%s'" % json.loads(api_response.content))

        actual_backup_list = self.LunrAPIProvider.convert_json_to_domain_object_list(json.loads(api_response.content), _BackupDomainObject)
        for expected_backup in self.expected_backups:
            self.assertIn(expected_backup, actual_backup_list, "Backup not in List")

    def test_get_backup_info(self):
        for expected_backup in self.expected_backups:
            api_response = self.user_client.Backups.get_info(expected_backup.id)
            self.assertTrue(api_response.ok, "Backup Get Info API call failed:'%s'" % json.loads(api_response.content))
            actual_backup_info = _BackupDomainObject(**json.loads(api_response.content))
            self.assertEqual(actual_backup_info, expected_backup, "Backup info does not match")

    def test_update_backup_info(self):
        for expected_backup in self.expected_backups:
            expected_size = 200
            api_response = self.user_client.Backups.update(expected_backup.id, params={'size':expected_size})

            self.assertTrue(api_response.ok, "Update Backup API call failed:'%s'" % json.loads(api_response.content))
            updated_backup = _VolumeDomainObject(**json.loads(api_response.content))
            self.assertEquals(updated_backup.size, expected_size, "Volume size was not updated to %i" % expected_size)

    def test_delete_backup(self):
        for expected_backup in self.expected_backups:
            expected_status = LunrBackupStatusTypes.DELETED
            api_response = self.user_client.Backups.delete(expected_backup.id)
            actual_deleted_backup = _BackupDomainObject(**json.loads(api_response.content))
            self.assertTrue(api_response.ok, "Delete Backup API call failed:'%s'" % json.loads(api_response.content))
            wait_result = self.LunrAPIProvider.wait_for_volume_backup_status(actual_deleted_backup.id, LunrBackupStatusTypes.DELETED, user_client = self.user_client)
            self.assertTrue(wait_result.ok, "Backup %s status not deleted. Status is %s" % (actual_deleted_backup.id, wait_result.entity.status))

def load_tests(loader, standard_tests, pattern):
    suite = TestSuite()
    suite.addTest(LunrBackupAPISmokeTest("test_create_backup"))
    suite.addTest(LunrBackupAPISmokeTest("test_list_backups"))
    suite.addTest(LunrBackupAPISmokeTest("test_get_backup_info"))
    suite.addTest(LunrBackupAPISmokeTest("test_update_backup_info"))
    suite.addTest(LunrBackupAPISmokeTest("test_delete_backup"))
    return suite