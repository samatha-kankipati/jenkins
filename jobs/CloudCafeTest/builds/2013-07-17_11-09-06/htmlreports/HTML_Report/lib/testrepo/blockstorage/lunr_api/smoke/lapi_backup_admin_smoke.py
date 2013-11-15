'''
@summary: Basic smoke test for Lunr Backup Admin API
@copyright: Copyright (c) 2012 Rackspace US, Inc.
'''
import json
from unittest2.suite import TestSuite

from testrepo.common.testfixtures.blockstorage import LunrAPIFixture
from ccengine.domain.types import LunrBackupStatusTypes
from ccengine.domain.blockstorage.lunr_api import Backup as BackupResponse


def load_tests(loader, standard_tests, pattern):
    suite = TestSuite()
    suite.addTest(LunrBackupAdminAPISmokeTest("test_list_backups"))
    suite.addTest(LunrBackupAdminAPISmokeTest("test_get_backup_info"))
    suite.addTest(LunrBackupAdminAPISmokeTest("test_update_backup_info"))
    suite.addTest(LunrBackupAdminAPISmokeTest("test_delete_backup"))
    return suite


class LunrBackupAdminAPISmokeTest(LunrAPIFixture):
    '''
    @summary: Basic smoke test for Lunr Backup Admin API
    '''
    @classmethod
    def setUpClass(cls):
        super(LunrBackupAdminAPISmokeTest, cls).setUpClass()

        #Create User Client
        cls.user_client = cls.LunrAPIProvider.create_user_client()

        #Create Volumes
        cls.vtypes = json.loads(cls.admin_client.VolumeTypes.list().content)
        cls.expected_volumes = []
        for vtype in cls.vtypes:
            created_volume = cls.LunrAPIProvider.create_volume_for_user(
                        cls.user_client, vtype)
            if created_volume is None:
                raise Exception("Could not create a volume with Active status")
            cls.expected_volumes.append(created_volume)

        #Create Expected Backups
        cls.expected_backups = []
        for volume in cls.expected_volumes:
            created_backup = cls.LunrAPIProvider.create_volume_backup(
                    volume.id, cls.user_client)
            if created_backup:
                cls.expected_backups.append(created_backup)
            else:
                cls.fixture_log.info("Could not create a backup for volume {0}"
                        .format(volume.id))

    @classmethod
    def tearDownClass(cls):
        cls.LunrAPIProvider.delete_user_backups(cls.user_client)
        cls.LunrAPIProvider.delete_user_volumes(cls.user_client)
        cls.admin_client.Accounts.delete(cls.user_client.account_id)
        super(LunrBackupAdminAPISmokeTest, cls).tearDownClass()

    def test_list_backups(self):
        resp = self.admin_client.Backups.list()
        self.assertTrue(resp.ok, "List Backups call returned {0}, expected 2XX"
                .format(resp.status_code))

        actual_backup_list = self.LunrAPIProvider.\
                convert_json_to_domain_object_list(json.loads(resp.content),
                BackupResponse)

        for expected_backup in self.expected_backups:
            self.assertIn(expected_backup, actual_backup_list,
                    "Backup not in List")

    def test_get_backup_info(self):
        for expected_backup in self.expected_backups:
            resp = self.admin_client.Backups.get_info(expected_backup.id)
            self.assertTrue(resp.ok, "Backup Get Info call returned {0}, "
                    "expected 2Xx".format(resp.status_code))
            actual_backup_info = BackupResponse(**json.loads(resp.content))
            self.assertEqual(actual_backup_info, expected_backup,
                    "Backup info does not match")

    def test_update_backup_info(self):
        for expected_backup in self.expected_backups:
            expected_size = 200
            resp = self.admin_client.Backups.update(expected_backup.id,
                    params={'size':expected_size})
            self.assertTrue(resp.ok, "Update Backup API call failed")
            updated_backup = BackupResponse(**json.loads(resp.content))
            self.assertEquals(updated_backup.size, expected_size,
                    "Volume size was not updated to {0}".format(expected_size))

    def test_delete_backup(self):
        for expected_backup in self.expected_backups:
            expected_status = LunrBackupStatusTypes.DELETED
            resp = self.admin_client.Backups.delete(expected_backup.id)
            actual_deleted_backup = BackupResponse(**json.loads(resp.content))
            self.assertTrue(resp.ok, "Delete Backup API call returned {0},"
                    " expected 2XX".format(resp.status_code))
            wait_status = self.LunrAPIProvider.wait_for_volume_backup_status(
                    actual_deleted_backup.id, expected_status,
                    user_client=self.user_client)
            self.assertTrue(wait_status.ok, "Backup {0} was not deleted. "
                    "Status is {1}".format(actual_deleted_backup.id,
                    wait_status.entity.status))
