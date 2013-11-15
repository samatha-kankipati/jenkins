'''
@summary: Negative Lunr API Update Backup Tests
@copyright: Copyright (c) 2012 Rackspace US, Inc.
'''
from datetime import datetime
import unittest2 as unittest
from ccengine.domain.blockstorage.lunr_api import Volume as _VolumeDomainObject
from ccengine.domain.status_codes import HttpStatusCodes
from testrepo.common.testfixtures.blockstorage import LunrAPIFixture
import json


class LunrUpdateBackupAPINegativeTest(LunrAPIFixture):
    '''
    @summary: Negative Lunr API Update Backup Tests
    '''
    @classmethod
    def setUpClass(cls):
        super(LunrUpdateBackupAPINegativeTest, cls).setUpClass()

        cls.common_user_client = cls.LunrAPIProvider.create_user_client()
        cls.fixture_log.info("Common User Account: %s" % cls.common_user_client.account_name)
        cls.account_clients_to_cleanup = [cls.common_user_client]

        timestamp = datetime.now().microsecond
        base_volume_id = "Update_BaseVolume_%d" % timestamp

        #Change this so that it grabs the min volume size on a per-vtype basis
        #instead of from the config
        base_volume_size = cls.config.lunr_api.min_volume_size

        base_volume_type = 'SATA'
        api_response = json.loads(cls.common_user_client.Volumes.create(base_volume_id, base_volume_size, base_volume_type).content)
        cls.base_volume_domain_object = _VolumeDomainObject(**api_response)

        cls.base_backup = cls.LunrAPIProvider.create_volume_backup(base_volume_id, cls.common_user_client)

    @classmethod
    def tearDownClass(cls):
        for account in cls.account_clients_to_cleanup:
            cls.LunrAPIProvider.cleanup_account(account)
        super(LunrUpdateBackupAPINegativeTest, cls).tearDownClass()

    def test_update_backup_with_incorrect_account_id(self):
        expected_status_code = HttpStatusCodes.NOT_FOUND
        invalid_account_client = self.LunrAPIProvider.create_invalid_user()
        self.account_clients_to_cleanup.append(invalid_account_client)
        api_response = invalid_account_client.Backups.update(self.base_backup.id)
        self.assertFalse(api_response.ok, "Call to create backup with invalid account id was successful")
        self.assertEqual(api_response.status_code, expected_status_code, "Status code %s was returned, instead of the expected %s"
                                                        % (api_response.status_code, expected_status_code))
        self.assertEqual(json.loads(api_response.content)['reason'], "Cannot update non-existent backup '%s'" % self.base_backup.id)

    def test_update_non_existent_backup(self):
        non_existent_backup_id = "UPDATE_NONEXISTENT_BACKUP_%d" % datetime.now().microsecond
        expected_status_code = HttpStatusCodes.NOT_FOUND

        api_response = self.common_user_client.Backups.update(non_existent_backup_id, params={'size':2})
        self.assertEqual(api_response.status_code, expected_status_code, "Status code %s was returned, instead of the expected %s"
                                                        % (api_response.status_code, expected_status_code))
        self.assertEqual(json.loads(api_response.content)['reason'], "Cannot update non-existent backup '%s'" % non_existent_backup_id)
        api_response = self.common_user_client.Volumes.get_info(non_existent_backup_id)
        self.assertFalse(api_response.ok, "Updating a Non Existent Backup created backup %s" % json.loads(api_response.content))
