
'''
@summary: Negative Lunr API Create Backup Tests
@copyright: Copyright (c) 2012 Rackspace US, Inc.
'''
from datetime import datetime
import json

from ccengine.domain.status_codes import HttpStatusCodes
from testrepo.common.testfixtures.blockstorage import LunrAPIFixture


class LunrCreateBackupAPINegativeTest(LunrAPIFixture):
    '''
    @summary: Negative Lunr API Create Volume Tests
    '''
    @classmethod
    def setUpClass(cls):
        super(LunrCreateBackupAPINegativeTest, cls).setUpClass()

        #Create User Clients
        cls.common_user_client = cls.LunrAPIProvider.create_user_client()
        cls.fixture_log.info("Common User Account: {0}".format(
                cls.common_user_client.account_name))

        cls.vtypes = json.loads(cls.admin_client.VolumeTypes.list().content)
        cls.account_clients_to_cleanup = [cls.common_user_client]

        #Change this so that it pulls min volume size from vtypes, not config
        cls.min_volume_size = cls.config.lunr_api.min_volume_size

    @classmethod
    def tearDownClass(cls):
        for account in cls.account_clients_to_cleanup:
            cls.LunrAPIProvider.cleanup_account(account)
        super(LunrCreateBackupAPINegativeTest, cls).tearDownClass()

    def test_create_backup_for_deleted_account(self):
        deleted_account_client = self.LunrAPIProvider.create_user_client()
        self.account_clients_to_cleanup.append(deleted_account_client)
        timestamp = datetime.now().microsecond
        volume_name = "TestVolume_{0}".format(timestamp)
        expected_status_code = HttpStatusCodes.NOT_FOUND

        deleted_account_client.Volumes.create(
                volume_name,
                self.vtypes[0]['min_size'],
                self.vtypes[0]['name'])

        self.fixture_log.info("Deleted Account {0}".format(
                deleted_account_client.account_id))
        self.admin_client.Accounts.delete(deleted_account_client.account_id)
        backup_name = "TestBackup_{0}".format(timestamp)
        api_response = deleted_account_client.Backups.create(
                backup_name,
                params={'volume': volume_name})
        self.assertEqual(
                api_response.status_code,
                expected_status_code,
                "Status code is not the expected {0}. API Response: "
                "{1}".format(
                        expected_status_code,
                        json.loads(api_response.content)))

    def test_create_backup_for_nonexistent_volume(self):
        timestamp = datetime.now().microsecond
        volume_name = "NonexistentVolume_{0}".format(timestamp)
        backup_name = "BackupShouldntBeCreated_{0}".format(timestamp)
        expected_status_code = HttpStatusCodes.UNPROCESSABLE_ENTITY

        api_response = self.common_user_client.Backups.create(
                backup_name,
                params={'volume': volume_name})

        self.assertEqual(
                api_response.status_code,
                expected_status_code,
                "Status code is not the expected {0}. API Response: "
                "{1}".format(
                        expected_status_code,
                        json.loads(api_response.content)))

        self.assertEqual(
                json.loads(api_response.content)['reason'],
                "Cannot create backup for non-existent volume '{0}'".
                        format(volume_name))

    def test_create_backup_with_duplicate_id(self):
        timestamp = datetime.now().microsecond
        volume_name = "TestVolume_%d" % timestamp
        expected_status_code = HttpStatusCodes.CONFLICT

        api_response = self.common_user_client.Volumes.create(
                volume_name,
                self.min_volume_size,
                'SATA')

        self.assertTrue(
            api_response.ok,
            "Create volume Lunr API call failed. API response: %s"
                    % json.loads(api_response.content))

        duplicate_backup_id = "DuplicateBackupId_%d" % timestamp
        api_response = self.common_user_client.Backups.create(
                duplicate_backup_id,
                params={'volume':volume_name})
        self.assertTrue(
                api_response.ok,
                "Create backup Lunr API call failed. API response: %s"
                        % json.loads(api_response.content))

        api_response = self.common_user_client.Backups.create(
                duplicate_backup_id,
                params={'volume':volume_name})
        self.assertEqual(
                api_response.status_code,
                expected_status_code,
                "Status code is not the expected %s. API Response: %s"
                    % (expected_status_code, json.loads(api_response.content)))
        self.assertEqual(
                json.loads(api_response.content)['reason'],
                "Backup '%s' already exists" % duplicate_backup_id)

    def test_create_backup_with_duplicate_id_for_different_account(self):
        timestamp = datetime.now().microsecond
        volume_name = "TestVolume_%d" % timestamp
        duplicate_backup_id = "TestBackup_%d" % timestamp
        expected_status_code = HttpStatusCodes.CONFLICT

        user_account_b = self.LunrAPIProvider.create_user_client()
        self.account_clients_to_cleanup.append(user_account_b)
        self.common_user_client.Volumes.create(
                volume_name,
                self.min_volume_size, 'SATA')
        api_response = self.common_user_client.Backups.create(
                duplicate_backup_id,
                params={'volume':volume_name})
        self.assertTrue(
                api_response.ok,
                "API Call to create original backup failed: %s"
                        % duplicate_backup_id)

        volume_name2 = "TestVolume2_%d" % timestamp
        api_response = user_account_b.Volumes.create(
                volume_name2,
                self.min_volume_size,
                'SATA')
        self.assertTrue(
                api_response.ok,
                "Create backup Lunr API call failed. API response: %s"
                        % json.loads(api_response.content))

        api_response = user_account_b.Backups.create(
                duplicate_backup_id,
                params={'volume':volume_name2})
        self.assertEqual(
                api_response.status_code,
                expected_status_code,
                "Status code %s was returned, instead of the expected %s"
                        % (api_response.status_code, expected_status_code))
        self.assertEqual(
                json.loads(api_response.content)['reason'],
                "Backup '%s' already exists" % duplicate_backup_id)
