'''
@summary: Negative test for DELETE Lunr Accounts Admin API
@copyright: Copyright (c) 2012 Rackspace US, Inc.
'''
from ccengine.domain.status_codes import HttpStatusCodes
from testrepo.common.testfixtures.blockstorage import LunrAPIFixture
import json

class LunrDeleteAccountsAdminAPINegativeTest(LunrAPIFixture):
    '''
    @summary: Negative test for Lunr Accounts Admin API - Create, List, Get Info, Update, and Delete
    '''
    def test_delete_non_existent_account(self):
        non_existent_account = "NON_EXISTENT_ACCOUNT"
        api_response = self.admin_client.Accounts.delete(non_existent_account)
        expected_status_code = HttpStatusCodes.NOT_FOUND
        self.assertEqual(api_response.status_code, expected_status_code, "Status code %s was returned, instead of the expected %s"
                                                        % (api_response.status_code, expected_status_code))
        self.assertEqual(json.loads(api_response.content)['reason'], "Cannot delete non-existent account '%s'" % non_existent_account)