'''
@summary: Negative test for Lunr Get Info Accounts Admin API
@copyright: Copyright (c) 2012 Rackspace US, Inc.
'''
import json
from testrepo.common.testfixtures.blockstorage import LunrAPIFixture


class LunrGetInfoAccountsAdminAPINegativeTest(LunrAPIFixture):
    '''
    @summary: Negative test for Lunr Get Info Accounts Admin API
    '''
    def test_get_info_on_nonexistent_account(self):
        nonexistent_account = 'NONEXISTENT_ACCOUNT'
        api_response = self.admin_client.Accounts.get_info(nonexistent_account)
        expected_status_code = 404
        assert api_response.status_code == expected_status_code,\
                "Expected {0}, recieved {1}".format(api_response.status_code,
                                                    expected_status_code)

        assert json.loads(api_response.content)['reason'],\
                "Cannot show non-existent account '{0}'".format(
                nonexistent_account)
