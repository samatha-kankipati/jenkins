'''
@summary: Negative Lunr API Create Volume Tests
@copyright: Copyright (c) 2012 Rackspace US, Inc.
'''
from datetime import datetime
import json

from ccengine.domain.status_codes import HttpStatusCodes
from testrepo.common.testfixtures.blockstorage import LunrAPIFixture


class LunrCreateVolumeAPINegativeTest(LunrAPIFixture):
    '''
    @summary: Negative Lunr API Create Volume Tests
    '''
    @classmethod
    def setUpClass(cls):
        super(LunrCreateVolumeAPINegativeTest, cls).setUpClass()

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
        super(LunrCreateVolumeAPINegativeTest, cls).tearDownClass()

    def test_create_volume_for_deleted_account(self):
        deleted_account_client = self.LunrAPIProvider.create_user_client()
        self.account_clients_to_cleanup.append(deleted_account_client)
        self.admin_client.Accounts.delete(deleted_account_client.account_id)
        self.fixture_log.info("Deleted Account {0}".format(
                deleted_account_client.account_name))

        volume_name = "TestVolume_%d" % datetime.now().microsecond
        api_response = deleted_account_client.Volumes.create(
                volume_name,
                self.vtypes[0]['min_size'],
                self.vtypes[0]['name'])

        self.assertFalse(
                api_response.ok,
                "FAIL: Volume, {0} was created with deleted Account - {1}!".\
                        format(volume_name, deleted_account_client.account_id))

        self.assertEqual(
                api_response.status_code,
                HttpStatusCodes.NOT_FOUND,
                "Status code returned is {0}".format(api_response.status_code))

    def test_create_volume_with_duplicate_id(self):
        duplicate_volume_name = "TestVolume_{0}".format(
                datetime.now().microsecond)
        expected_status_code = HttpStatusCodes.CONFLICT

        api_response = self.common_user_client.Volumes.create(
                duplicate_volume_name,
                self.min_volume_size,
                'SATA')

        self.assertTrue(
                api_response.ok,
                "Create volume Lunr API call failed. API response: {0}".format(
                        json.loads(api_response.content)))

        api_response = self.common_user_client.Volumes.create(
                duplicate_volume_name,
                self.min_volume_size,
                'SATA')

        self.assertEqual(
                api_response.status_code,
                expected_status_code,
                "Status code {0} was returned, instead of the expected {1}".\
                        format(api_response.status_code, expected_status_code))

        self.assertEqual(
                json.loads(api_response.content)['reason'],
                "Volume '{0}' already exists".format(duplicate_volume_name))

    def test_create_volume_with_duplicate_id_for_different_account(self):
        duplicate_volume_name = "TestVolume_{0}".format(
                datetime.now().microsecond)
        expected_status_code = HttpStatusCodes.CONFLICT

        user_account_b = self.LunrAPIProvider.create_user_client()
        self.account_clients_to_cleanup.append(user_account_b)
        self.common_user_client.Volumes.create(
                duplicate_volume_name,
                self.min_volume_size,
                'SATA')

        api_response = user_account_b.Volumes.create(
                duplicate_volume_name,
                self.min_volume_size,
                'SATA')

        self.assertEqual(
                api_response.status_code,
                expected_status_code,
                "Status code {0} was returned, instead of the expected {1}".\
                        format(api_response.status_code, expected_status_code))

        self.assertEqual(
                json.loads(api_response.content)['reason'],
                "Volume '{0}' already exists".format(duplicate_volume_name))
