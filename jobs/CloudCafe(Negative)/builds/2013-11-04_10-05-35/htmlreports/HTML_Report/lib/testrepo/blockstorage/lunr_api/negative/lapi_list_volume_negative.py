'''
@summary: Negative Lunr API List Volume Tests
@copyright: Copyright (c) 2012 Rackspace US, Inc.
'''
from ccengine.domain.status_codes import HttpStatusCodes
from testrepo.common.testfixtures.blockstorage import LunrAPIFixture
import unittest2 as unittest
import json

class LunrListVolumeAPINegativeTest(LunrAPIFixture):
    '''
    @summary: Negative Lunr API List Volume Tests
    '''
    @classmethod
    def setUpClass(cls):
        super(LunrListVolumeAPINegativeTest, cls).setUpClass()

        cls.common_user_client = cls.LunrAPIProvider.create_user_client()
        cls.fixture_log.info("Common User Account: %s" % cls.common_user_client.account_name)
        cls.vtypes = json.loads(cls.admin_client.VolumeTypes.list().content)
        cls.account_clients_to_cleanup = [cls.common_user_client]

    @classmethod
    def tearDownClass(cls):
        for account in cls.account_clients_to_cleanup:
            cls.LunrAPIProvider.cleanup_account(account)
        super(LunrListVolumeAPINegativeTest, cls).tearDownClass()

    def test_list_volumes_for_deleted_account(self):
        expected_status_code = HttpStatusCodes.NOT_FOUND
        user_account_b = self.LunrAPIProvider.create_user_client()
        self.account_clients_to_cleanup.append(user_account_b)
        self.admin_client.Accounts.delete(user_account_b.account_id)

        api_response = user_account_b.Volumes.list()
        self.assertEqual(api_response.status_code, expected_status_code, "Status code %s was returned, instead of the expected %s"
                                                                        % (api_response.status_code, expected_status_code))
        self.assertEqual(json.loads(api_response.content)['reason'], "Account is not ACTIVE")