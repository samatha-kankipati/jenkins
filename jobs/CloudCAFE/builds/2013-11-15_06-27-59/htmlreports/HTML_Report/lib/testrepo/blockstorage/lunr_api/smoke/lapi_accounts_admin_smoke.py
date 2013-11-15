'''
@summary: Basic smoke test for Lunr Accounts Admin API
@copyright: Copyright (c) 2012 Rackspace US, Inc.
'''
import json
from datetime import datetime
from unittest2.suite import TestSuite

from testrepo.common.testfixtures.blockstorage import LunrAPIFixture
from ccengine.domain.types import LunrVolumeStatusTypes
from ccengine.domain.blockstorage.lunr_api import Account as AccountResponse


def load_tests(loader, standard_tests, pattern):
    suite = TestSuite()
    suite.addTest(LunrAccountsAdminAPISmokeTest("test_create_account"))
    suite.addTest(LunrAccountsAdminAPISmokeTest("test_list_account"))
    suite.addTest(LunrAccountsAdminAPISmokeTest("test_get_account_info"))
    suite.addTest(LunrAccountsAdminAPISmokeTest("test_update_account_info"))
    suite.addTest(LunrAccountsAdminAPISmokeTest("test_delete_account_info"))
    return suite


class LunrAccountsAdminAPISmokeTest(LunrAPIFixture):
    '''
    @summary: Basic smoke test for Lunr Accounts Admin API
    '''
    @classmethod
    def setUpClass(cls):
        super(LunrAccountsAdminAPISmokeTest, cls).setUpClass()

        #Create Expected Account
        '''@TODO Find way to create expected account domain object
                that persists between tests and to tearDownClass'''
        cls.expected_accounts = []

    @classmethod
    def tearDownClass(cls):
        teardown_status = True
        for account in cls.expected_accounts:
            resp = cls.admin_client.Accounts.delete(account.id)
            teardown_status = teardown_status and resp.ok

        super(LunrAccountsAdminAPISmokeTest, cls).tearDownClass()
        if not teardown_status:
            cls.fixture_log.warning("tearDownClass failure.  At least one "
                    "account was not deleted")

    def setUp(self):
        super(LunrAccountsAdminAPISmokeTest, self).setUp()
        if len(self.expected_accounts) == 1:
            self.expected_account = self.expected_accounts[0]

    def test_create_account(self):
        account_id = "LunrTestAccount_%d" % datetime.now().microsecond
        self.fixture_log.info("Creating Account: %s" % account_id)

        resp = self.admin_client.Accounts.create(
                params={'id':account_id})
        self.assertTrue(resp.ok,
                "Admin create account API call Failed.")
        created_account = AccountResponse(**json.loads(resp.content))
        self.assertTrue(created_account.id, "Account ID not generated, so "
                "account not created successfully.")
        self.expected_accounts.append(created_account)

    def test_list_account(self):
        resp = self.admin_client.Accounts.list()
        self.assertTrue(resp.ok, "List Accounts API call Failed")
        actual_account_list = self.LunrAPIProvider.\
                convert_json_to_domain_object_list(json.loads(
                resp.content), AccountResponse)
        self.assertIn(self.expected_account, actual_account_list)

    def test_get_account_info(self):
        resp = self.admin_client.Accounts.get_info(
                self.expected_account.id)
        self.assertTrue(resp.ok, "Get Account Information API retuend {0}, "
                "expected 2XX".format(resp.status_code))
        actual_account_info = AccountResponse(**json.loads(resp.content))
        self.assertEqual(self.expected_account, actual_account_info)

    def test_update_account_info(self):
        new_account_status = 'UPDATED'
        resp = self.admin_client.Accounts.update(self.expected_account.id,
                params={'status': new_account_status})
        self.assertTrue(resp.ok, "Update Account Information API call "
                "returned {0}, expected 2XX".format(resp.status_code))
        actual_account_info = AccountResponse(**json.loads(resp.content))
        self.assertEqual(new_account_status, actual_account_info.status)

    def test_delete_account_info(self):
        expected_status = LunrVolumeStatusTypes.DELETED
        resp = self.admin_client.Accounts.delete(self.expected_account.id)
        self.assertTrue(resp.ok, "Delete Account API call returned {0}, "
                "expected 2XX".format(resp.status_code))
        resp = self.admin_client.Accounts.get_info(self.expected_account.id)
        actual_account = AccountResponse(**json.loads(resp.content))
        self.assertEqual(actual_account.status, expected_status,
                "Account not marked Deleted.")
