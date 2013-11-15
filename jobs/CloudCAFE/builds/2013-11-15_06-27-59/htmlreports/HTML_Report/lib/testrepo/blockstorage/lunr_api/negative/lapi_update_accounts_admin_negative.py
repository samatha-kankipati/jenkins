'''
@summary: Negative test for UPDATE Lunr Accounts Admin API
@copyright: Copyright (c) 2012 Rackspace US, Inc.
'''
import json
import unittest2 as unittest
from ccengine.domain.status_codes import HttpStatusCodes
from testrepo.common.testfixtures.blockstorage import LunrAPIFixture
from ccengine.domain.blockstorage.lunr_api import Account as _AccountDomainObject
from ccengine.domain.types import LunrVolumeStatusTypes


class LunrUpdateAccountsAdminAPINegativeTest(LunrAPIFixture):
    '''
    @summary: Negative Tests for UPDATE Lunr Accounts Admin API
    '''

    @classmethod
    def setUpClass(cls):
        super(LunrUpdateAccountsAdminAPINegativeTest, cls).setUpClass()

        '''@TODO Find way to create expected account domain object
    that persists between tests and to tearDownClass'''
        cls.accounts_to_cleanup = []

        cls.user_account = cls.LunrAPIProvider.create_user_client()
        cls.accounts_to_cleanup.append(cls.user_account)

    @classmethod
    def tearDownClass(cls):
        api_response = cls.admin_client.Accounts.delete(
                cls.accounts_to_cleanup[0].account_id)
        deleted_account = _AccountDomainObject(
                **json.loads(api_response.content))
        if deleted_account.status == LunrVolumeStatusTypes.DELETED:
            cls.fixture_log.info("Deleted Account: %s"
            % cls.accounts_to_cleanup[0].account_id)
        super(LunrUpdateAccountsAdminAPINegativeTest, cls).tearDownClass()

    def setUp(self):
        super(LunrUpdateAccountsAdminAPINegativeTest, self).setUp()

    def test_update_invalid_account(self):
        updated_status = 'UPDATED'
        expected_status_code = HttpStatusCodes.NOT_FOUND
        invalid_account_client = self.LunrAPIProvider.create_invalid_user()
        self.accounts_to_cleanup.append(invalid_account_client)
        api_response = self.admin_client.Accounts.update(
                invalid_account_client.account_id,
                params={'status': updated_status})
        self.assertFalse(api_response.ok,
                "Call to update invalid account was successful")
        self.assertEqual(api_response.status_code, expected_status_code,
                "Status code %s was returned, instead of the expected %s"
                % (api_response.status_code, expected_status_code))
        self.assertEqual(json.loads(api_response.content)['reason'],
                "Cannot update non-existent account '%s'"
                % invalid_account_client.account_id)

    @unittest.skip('Issue #282: Call returns with an error (incorrect error?)'
                   'but account ID is updated regardless!!')
    def test_update_account_id_with_invalid_id(self):
        '''
        @summary: Test updates the account ID. At first it throws and error.
        But NOTE that it actually goes ahead an updates the ID
        '''
        new_account_id = 'NEW_ACCOUNT_ID'
        expected_status_code = HttpStatusCodes.INTERNAL_SERVER_ERROR
        api_response = self.admin_client.Accounts.update(
                self.user_account.account_id, params={'id': new_account_id})

        self.assertFalse(api_response.ok, "Recieved {0}, expected {1}".format(
                api_response.status_code, expected_status_code))

        self.assertEqual(json.loads(api_response.content)['reason'],
                "Internal controller error")

        api_response = self.admin_client.Accounts.get_info(new_account_id)
        self.assertNotEqual(json.loads(api_response.content)['id'],
                            new_account_id, "Account ID was not updated to new"
                            "account ID: '%s'" % new_account_id)

    @unittest.skip('Issue #281: Able to update account created_at property'
                   ' through the API')
    def test_update_account_created_at_timestamp_with_valid_format(self):
        new_account_created_at = '2012-10-02 19:36:15'
        expected_status_code = HttpStatusCodes.INTERNAL_SERVER_ERROR
        api_response = self.admin_client.Accounts.update(
                self.user_account.account_id,
                params={'created_at': new_account_created_at})
        self.assertFalse(api_response.ok, "Call to update account created_at "\
               "with valid format was successful when it should not have been")
        self.assertEqual(api_response.status_code, expected_status_code,
                "Status code %s was returned, instead of the expected %s"
                % (api_response.status_code, expected_status_code))
        self.assertEqual(json.loads(api_response.content)['reason'],
                "Internal controller error")

    @unittest.skip('Issue #281: Able to update account created_at property'
                   ' through the API')
    def test_update_account_created_at_timestamp_with_invalid_format(self):
        new_account_created_at = 'INVALID_FORMAT_TIMESTAMP_STRING'
        api_response = self.admin_client.Accounts.update(
                self.user_account.account_id,
                params={'created_at': new_account_created_at})
        self.assertFalse(api_response.ok, "Call to update account created_at "\
            "with invalid format was successful when it should not have been")
        expected_status_code = HttpStatusCodes.INTERNAL_SERVER_ERROR
        self.assertEqual(api_response.status_code, expected_status_code,
                "Status code %s was returned, instead of the expected %s"
                % (api_response.status_code, expected_status_code))
        self.assertEqual(json.loads(api_response.content)['reason'],
                "Internal controller error")
