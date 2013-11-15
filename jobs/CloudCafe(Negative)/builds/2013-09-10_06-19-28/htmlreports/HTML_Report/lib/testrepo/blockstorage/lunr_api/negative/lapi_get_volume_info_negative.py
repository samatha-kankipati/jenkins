'''
@summary: Negative Lunr API Get Volume Info Tests
@copyright: Copyright (c) 2012 Rackspace US, Inc.
'''
from ccengine.domain.status_codes import HttpStatusCodes
from testrepo.common.testfixtures.blockstorage import LunrAPIFixture
import json

class LunrGetVolumeInfoAPINegativeTest(LunrAPIFixture):
    '''
    @summary: Negative Lunr API Get Volume Info Tests
    '''
    @classmethod
    def setUpClass(cls):
        super(LunrGetVolumeInfoAPINegativeTest, cls).setUpClass()

        cls.common_user_client = cls.LunrAPIProvider.create_user_client()
        cls.fixture_log.info("Common User Account: %s" % cls.common_user_client.account_name)
        cls.vtypes = json.loads(cls.admin_client.VolumeTypes.list().content)
        cls.account_clients_to_cleanup = [cls.common_user_client]

    @classmethod
    def tearDownClass(cls):
        for account in cls.account_clients_to_cleanup:
            cls.LunrAPIProvider.cleanup_account(account)
        super(LunrGetVolumeInfoAPINegativeTest, cls).tearDownClass()

    def test_get_info_on_nonexistent_volume(self):
        nonexistent_volume_name = 'ThisVolumeShouldNotExist'
        expected_status_code = HttpStatusCodes.NOT_FOUND
        api_response = self.common_user_client.Volumes.get_info(nonexistent_volume_name)
        self.assertEquals(api_response.status_code, expected_status_code, "Status code %s was returned, instead of the expected %s"
                                                            % (api_response.status_code, expected_status_code))
        self.assertEqual(json.loads(api_response.content)['reason'], "Cannot show non-existent volume '%s'" % nonexistent_volume_name)

    def test_get_info_on_volume_from_another_account(self):
        expected_status_code = HttpStatusCodes.NOT_FOUND
        user_account_b = self.LunrAPIProvider.create_user_client()
        self.account_clients_to_cleanup.append(user_account_b)
        volume_a = self.LunrAPIProvider.create_volume_for_user(self.common_user_client,self.vtypes[0])

        api_response = user_account_b.Volumes.get_info(volume_a.id)
        self.assertEqual(api_response.status_code, expected_status_code, "Status code %s was returned, instead of the expected %s"
                                                                % (api_response.status_code, expected_status_code))
        self.assertEqual(json.loads(api_response.content)['reason'], "Cannot show non-existent volume '%s'" % volume_a.id)
