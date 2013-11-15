'''
@summary: Functional test for Lunr Accounts Admin API
@copyright: Copyright (c) 2012 Rackspace US, Inc.
'''
from ccengine.domain.blockstorage.lunr_api import Account as _AccountDomainObject
from testrepo.common.testfixtures.blockstorage import LunrAPIFixture
from ccengine.domain.types import LunrVolumeStatusTypes
import json


class LunrAccountsAdminAPIFunctionalTest(LunrAPIFixture):
    '''
    @summary: Functional test for Lunr Accounts Admin API
    '''
    @classmethod
    def setUpClass(cls):
        super(LunrAccountsAdminAPIFunctionalTest, cls).setUpClass()

        '''@TODO Find way to create expected account domain object
                that persists between tests and to tearDownClass'''
        cls.accounts_to_cleanup = []

    @classmethod
    def tearDownClass(cls):
        api_response = cls.admin_client.Accounts.delete(cls.accounts_to_cleanup[0].account_id)
        deleted_account = _AccountDomainObject(**json.loads(api_response.content))
        if deleted_account.status == LunrVolumeStatusTypes.DELETED:
            cls.fixture_log.info("Deleted Account: %s" % cls.accounts_to_cleanup[0].account_id)
        super(LunrAccountsAdminAPIFunctionalTest, cls).tearDownClass()

    def volume_types(self):
        # Get volume types
        vtypes_resp = self.admin_client.VolumeTypes.list()
        assert vtypes_resp.ok, 'Unable to get volume types list'
        vtypes = json.loads(vtypes_resp.content)
        assert (vtypes is not None) and (vtypes != []),\
                'Volumes types list returned empty'

        return vtypes

    def setUp(self):
        super(LunrAccountsAdminAPIFunctionalTest, self).setUp()
        self.user_account = self.LunrAPIProvider.create_user_client()
        self.accounts_to_cleanup.append(self.user_account)
        self.vtypes = self.volume_types()
        self.active_volume = self.LunrAPIProvider.create_volume_for_user(self.user_account, self.vtypes[0])
        self.assertEqual(self.active_volume.status, LunrVolumeStatusTypes.READY, "Volume is does not have READY status")

    def test_delete_account_with_active_volume(self):
        api_response = self.admin_client.Accounts.delete(self.user_account.account_id)
        self.assertTrue(api_response.ok, "Delete Account that with Active Volume API call Failed: '%s'"
                                         % json.loads(api_response.content))

    def test_delete_account_with_deleted_volume(self):
        is_deleted = self.LunrAPIProvider.delete_user_volume(self.user_account, self.active_volume.id)
        self.assertTrue(is_deleted, "Volume '%s' does not have DELETED status" % self.active_volume.id)
        api_response = self.admin_client.Accounts.delete(self.user_account.account_id)
        self.assertTrue(api_response.ok, "Delete Account that with DELETED Volume API call Failed: '%s'"
                                         % json.loads(api_response.content))

    def test_delete_account_with_status_deleted(self):
        user_account = self.LunrAPIProvider.create_user_client()
        self.accounts_to_cleanup.append(user_account)
        api_response = self.admin_client.Accounts.delete(user_account.account_id)
        self.assertTrue(api_response.ok, "Delete Account API Call Failed: '%s'"
                                         % json.loads(api_response.content))
        api_response = self.admin_client.Accounts.get_info(user_account.account_id)
        self.assertTrue(api_response.ok, "Get info on Deleted account Failed: '%s'"
                                         % json.loads(api_response.content))
        if json.loads(api_response.content)['status'] is 'DELETED':
            api_response = self.admin_client.Accounts.delete(user_account.account_id)
            self.assertTrue(api_response.ok, "Delete Account with Status DELETED API Call Failed: '%s'"
                                         % json.loads(api_response.content))
