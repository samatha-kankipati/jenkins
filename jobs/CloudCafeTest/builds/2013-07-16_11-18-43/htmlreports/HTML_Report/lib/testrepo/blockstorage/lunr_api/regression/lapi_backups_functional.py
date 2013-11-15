'''
@summary: Functional Lunr API Backup Volume Tests
@copyright: Copyright (c) 2012 Rackspace US, Inc.
'''
from testrepo.common.testfixtures.blockstorage import LunrAPIFixture
import json

class LunrBackupAPIFunctionalTest(LunrAPIFixture):
    '''
    @summary: Functional Lunr API Backup Volume Tests
    '''
    @classmethod
    def setUpClass(cls):
        super(LunrBackupAPIFunctionalTest, cls).setUpClass()

        cls.common_user_client = cls.LunrAPIProvider.create_user_client()
        cls.fixture_log.info("Common User Account: %s" % cls.common_user_client.account_name)
        cls.account_clients_to_cleanup = [cls.common_user_client]

    @classmethod
    def tearDownClass(cls):
        for account in cls.account_clients_to_cleanup:
            cls.LunrAPIProvider.cleanup_account(account)
        super(LunrBackupAPIFunctionalTest, cls).tearDownClass()

    def test_list_backups_without_backups(self):
        api_response = self.common_user_client.Backups.list()
        self.assertTrue(api_response.ok, "API Call to list backups failed. API Response: %s"
                                        % json.loads(api_response.content))

    def test_list_backups_for_invalid_account(self):
        '''
        @summary: Testing listing backups for an invalid account ... This will create an auto generated account.
        '''
        invalid_user = self.LunrAPIProvider.create_invalid_user()
        self.account_clients_to_cleanup.append(invalid_user)
        api_response = invalid_user.Backups.list()
        self.assertTrue(api_response.ok, "API Call to list backups for invalid account failed. API Response: %s"
                                         % json.loads(api_response.content))
        self.assertEqual(json.loads(api_response.content), [], "List Volumes returned with %s instead of an empty list []" % json.loads(api_response.content))
        self.assertTrue(self.LunrAPIProvider.is_account_auto_generated(invalid_user.account_id, self.admin_client),
            "An account was not auto generated.")
