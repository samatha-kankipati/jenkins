'''
@summary: Negative Lunr API Delete Volume Tests
@copyright: Copyright (c) 2012 Rackspace US, Inc.
'''
from ccengine.domain.status_codes import HttpStatusCodes
from testrepo.common.testfixtures.blockstorage import LunrAPIFixture
from datetime import datetime
import json

class LunrDeleteVolumeAPINegativeTest(LunrAPIFixture):
    '''
    @summary: Negative Lunr API Delete Volume Tests
    '''
    @classmethod
    def setUpClass(cls):
        super(LunrDeleteVolumeAPINegativeTest, cls).setUpClass()

        cls.common_user_client = cls.LunrAPIProvider.create_user_client()
        cls.fixture_log.info("Common User Account: %s" % cls.common_user_client.account_name)
        cls.account_clients_to_cleanup = [cls.common_user_client]
        cls.vtypes = json.loads(cls.admin_client.VolumeTypes.list().content)

    @classmethod
    def tearDownClass(cls):
        for account in cls.account_clients_to_cleanup:
            cls.LunrAPIProvider.cleanup_account(account)
        super(LunrDeleteVolumeAPINegativeTest, cls).tearDownClass()

    def test_delete_non_existent_volume(self):
        non_existent_volume_id = "DELETE_NONEXISTENT_%d" % datetime.now().microsecond

        api_response = self.common_user_client.Volumes.delete(non_existent_volume_id)
        self.assertEqual(json.loads(api_response.content)['reason'], "Cannot delete non-existent volume '%s'" % non_existent_volume_id)

    def test_delete_volume_from_incorrect_account(self):
        expected_status_code = HttpStatusCodes.NOT_FOUND

        user_account_b = self.LunrAPIProvider.create_user_client()
        self.account_clients_to_cleanup.append(user_account_b)
        volume_a = self.LunrAPIProvider.create_volume_for_user(self.common_user_client,self.vtypes[0])

        api_response = user_account_b.Volumes.delete(volume_a.id)
        self.assertEqual(api_response.status_code, expected_status_code, "Status code %s was returned, instead of the expected %s"
                                                                    % (api_response.status_code, expected_status_code))
        self.assertEqual(json.loads(api_response.content)['reason'], "Cannot delete non-existent volume '%s'" % volume_a.id)

    def test_delete_volume_with_status_deleted(self):
        self.vtypes = json.loads(self.admin_client.VolumeTypes.list().content)
        expected_status_code = HttpStatusCodes.NOT_FOUND
        volume_a = self.LunrAPIProvider.create_volume_for_user(self.common_user_client,self.vtypes[0])
        self.LunrAPIProvider.delete_user_volume(self.common_user_client, volume_a.id)
        self.common_user_client.Volumes.delete(volume_a.id)

        api_response = self.common_user_client.Volumes.delete(volume_a.id)
        self.assertEqual(api_response.status_code, expected_status_code, "Status code %s was returned, instead of the expected %s"
                                                                    % (api_response.status_code, expected_status_code))
        self.assertIn("Cannot delete non-existant volume '%s'" % volume_a.id, json.loads(api_response.content)['reason'])

    def test_delete_volume_from_deleted_account(self):
        deleted_account_client = self.LunrAPIProvider.create_user_client()
        self.account_clients_to_cleanup.append(deleted_account_client)
        expected_status_code = 404

        #Create Volume
        volume_name = "TestVolume_%d" % datetime.now().microsecond
        deleted_account_client.Volumes.create(volume_name, 1, self.vtypes[0]['name'])

        #Delete Account
        self.admin_client.Accounts.delete(deleted_account_client.account_id)
        self.fixture_log.info("Deleted Account %s" % deleted_account_client.account_id)

        #Delete Volume
        api_response = deleted_account_client.Volumes.delete(volume_name)
        self.assertEqual(api_response.status_code, expected_status_code, "Status code %s was returned, instead of the expected %s"
                                                        % (api_response.status_code, expected_status_code))
        self.assertIn("Account is not ACTIVE", json.loads(api_response.content)['reason'])

