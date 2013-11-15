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
        cls.LunrAPIProvider.initiate_delete_for_user_backups(cls.user_client)
        cls.LunrAPIProvider.delete_user_volumes(cls.user_client)
        cls.admin_client.Accounts.delete(cls.user_client.account_id)
        cls.fixture_log.info("Deleting Account: %s" % cls.user_client.account_name)
        super(LunrBackupAPISmokeTest, cls).tearDownClass()

    def test_create_backup(self):
        #Create all the backups
        for volume in self.expected_volumes:
            backup_name = "Backup_{0}".format(datetime.now().microsecond)
            api_response = self.user_client.Backups.create(
                backup_name, params={'volume': volume.id})

            self.assertTrue(
                api_response.ok,
                "'Backup Create' call failed with a {0}".format(
                    api_response.content))

            backup = _BackupDomainObject(
                **json.loads(api_response.content))

            wait_status = self.LunrAPIProvider.wait_for_volume_backup_status(
                backup.id, LunrBackupStatusTypes.READY,
                user_client=self.user_client)

            self.assertTrue(
                wait_status.ok, "Backup '{0}' never became {1}".format(
                    backup.id, LunrBackupStatusTypes.READY))

            #Update to latest backup status and info
            api_response = self.user_client.Backups.get_info(
                backup.id)
            backup = _BackupDomainObject(
                **json.loads(api_response.content))

            self.assertEquals(
                backup.size, volume.size, "Backup {0} not given correct size "
                "(expected {1}, observed {2})".format(
                    backup.id, backup.size, volume.size))

            self.expected_backups.append(backup)

    def test_list_backups(self):
        api_response = self.user_client.Backups.list()
        self.assertTrue(
            api_response.ok,
            "'List Backups' API call failed with a {0}".format(
                api_response.status_code))

        backup_list = self.LunrAPIProvider.convert_json_to_domain_object_list(
            json.loads(api_response.content), _BackupDomainObject)

        backup_ids = [backup.id for backup in backup_list]

        for expected_backup in self.expected_backups:
            assert expected_backup.id in backup_ids, (
                "Backup {0} not found in {1}".format(
                    expected_backup.id, backup_ids))

    def test_get_backup_info(self):
        for expected_backup in self.expected_backups:
            api_response = self.user_client.Backups.get_info(
                expected_backup.id)

            self.assertTrue(
                api_response.ok,
                "'Get Backup Info' API call failed with a {0}".format(
                    api_response.status_code))

            actual_backup_info = _BackupDomainObject(
                **json.loads(api_response.content))

            assert expected_backup.account_id == actual_backup_info.account_id
            assert expected_backup.created_at == actual_backup_info.created_at
            assert expected_backup.volume_id == actual_backup_info.volume_id
            assert expected_backup.id == actual_backup_info.id
            assert expected_backup.size == actual_backup_info.size

    def test_update_backup_info(self):
        for expected_backup in self.expected_backups:
            expected_size = 200
            api_response = self.user_client.Backups.update(expected_backup.id, params={'size':expected_size})

            self.assertTrue(api_response.ok, "Update Backup API call failed:'%s'" % json.loads(api_response.content))
            updated_backup = _VolumeDomainObject(**json.loads(api_response.content))
            self.assertEquals(updated_backup.size, expected_size, "Volume size was not updated to %i" % expected_size)

    def test_delete_backup(self):
        delete_responses = []
        for expected_backup in self.expected_backups:
            resp = self.user_client.Backups.delete(expected_backup.id)
            delete_responses.append((expected_backup.id, resp))

        failure_messages = []
        successful_deletes = []
        for backup_id, api_response in delete_responses:
            if not api_response.ok:
                if api_response.status_code == 404:
                    self.fixture_log.warning(
                        "Delete on backup {0} resulted in 404 instead of a"
                        " 200.".format(backup_id))
                    successful_deletes.append(backup_id)
                    continue
                else:
                    failure_messages.append(
                        "\nDELETE for for backup {0} failed with response {1}"
                        .format(backup_id, api_response.status_code))
            else:
                entity = json.loads(api_response.content)
                reported_status = entity.get('status', None)
                if reported_status == 'DELETING':
                    successful_deletes.append(backup_id)
                else:
                    failure_messages.append(
                        "\nDELETE for for backup {0} returned a {1} status "
                        "instead of the expected DELETING status".format(
                            backup_id, api_response.status_code))

        for backup_id in successful_deletes:
            wait_result = self.LunrAPIProvider.wait_for_volume_backup_status(
                backup_id, 'DELETING',
                user_client=self.user_client, timeout=10)
            if not wait_result.ok:
                failure_messages.append(
                    "\nBackup {0} was never observed to have entered the "
                    "DELETING state".format(backup_id))

        assert len(failure_messages) == 0, str(failure_messages)


def load_tests(loader, standard_tests, pattern):
    suite = TestSuite()
    suite.addTest(LunrBackupAPISmokeTest("test_create_backup"))
    suite.addTest(LunrBackupAPISmokeTest("test_list_backups"))
    suite.addTest(LunrBackupAPISmokeTest("test_get_backup_info"))
    suite.addTest(LunrBackupAPISmokeTest("test_update_backup_info"))
    suite.addTest(LunrBackupAPISmokeTest("test_delete_backup"))
    return suite
