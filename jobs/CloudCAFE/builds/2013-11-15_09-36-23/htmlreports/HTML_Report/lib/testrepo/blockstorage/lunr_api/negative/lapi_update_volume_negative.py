'''
@summary: Negative Lunr API Update Volume Tests
@copyright: Copyright (c) 2012 Rackspace US, Inc.
'''
from datetime import datetime
import json

from ccengine.domain.blockstorage.lunr_api import Volume as _VolumeDomainObject
from ccengine.domain.status_codes import HttpStatusCodes
from testrepo.common.testfixtures.blockstorage import LunrAPIFixture


class LunrUpdateVolumeAPINegativeTest(LunrAPIFixture):
    '''
    @summary: Negative Lunr API Update Volume Tests
    '''
    @classmethod
    def setUpClass(cls):
        super(LunrUpdateVolumeAPINegativeTest, cls).setUpClass()

        #Change this so that it pulls min volume size from vtypes, not config
        cls.min_volume_size = cls.config.lunr_api.min_volume_size

        cls.common_user_client = cls.LunrAPIProvider.create_user_client()
        cls.fixture_log.info("Common User Account: {0}".format(
                cls.common_user_client.account_name))
        cls.account_clients_to_cleanup = [cls.common_user_client]

        base_volume_name = "Update_BaseVolume_{0}".format(
                datetime.now().microsecond)
        base_volume_size = cls.min_volume_size
        base_volume_type = 'SATA'
        api_response = cls.common_user_client.Volumes.create(
                base_volume_name,
                base_volume_size,
                base_volume_type)
        assert api_response.ok, 'Unable to create Volume in setup'
        vol_resp = json.loads(api_response.content or {})
        cls.base_volume_domain_object = _VolumeDomainObject(**(vol_resp))

    @classmethod
    def tearDownClass(cls):
        for account in cls.account_clients_to_cleanup:
            cls.LunrAPIProvider.cleanup_account(account)
        super(LunrUpdateVolumeAPINegativeTest, cls).tearDownClass()

    def test_update_volume_with_incorrect_type(self):
        INVALID_VOLUME_TYPE_NAME = 'INVALID_VOLUME_TYPE_NAME'
        expected_status_code = HttpStatusCodes.INTERNAL_SERVER_ERROR

        api_response = self.common_user_client.Volumes.update(
                self.base_volume_domain_object.id,
                params={'volume_type_name': INVALID_VOLUME_TYPE_NAME})
        self.assertEqual(
                api_response.status_code,
                expected_status_code,
                "Status code {0} was returned, instead of the expected {1}".\
                        format(api_response.status_code, expected_status_code))

        self.assertEqual(
                json.loads(api_response.content)['reason'],
                'Internal controller error')

        api_response = self.common_user_client.Volumes.get_info(
                self.base_volume_domain_object.id)

        actual_volume_domain_object = _VolumeDomainObject(
                **json.loads(api_response.content))

        self.assertEqual(
                actual_volume_domain_object,
                self.base_volume_domain_object,
                "Volume with incorrect TYPE was updated!")

    def test_update_non_existent_volume(self):
        non_existent_volume_id = "UPDATE_NONEXISTENT_{0}".format(
                datetime.now().microsecond)

        expected_status_code = HttpStatusCodes.NOT_FOUND

        api_response = self.common_user_client.Volumes.update(
                non_existent_volume_id,
                params={'size': self.min_volume_size * 2})
        self.assertEqual(
                api_response.status_code,
                expected_status_code,
                "Status code {0} was returned, instead of the expected {1}".\
                        format(api_response.status_code, expected_status_code))

        self.assertEqual(
                json.loads(api_response.content)['reason'],
                "Cannot update non-existent volume '{0}'".format(
                        non_existent_volume_id))

        api_response = self.common_user_client.Volumes.get_info(
                non_existent_volume_id)

        self.assertFalse(
                api_response.ok,
                "Updating a Non Existent Volume created volume {0}".format(
                        json.loads(api_response.content)))

    def test_update_volume_from_incorrect_account(self):
        expected_status_code = HttpStatusCodes.NOT_FOUND
        user_account = self.LunrAPIProvider.create_user_client()
        self.account_clients_to_cleanup.append(user_account)

        vtypes = json.loads(self.admin_client.VolumeTypes.list().content)
        volume_a = self.LunrAPIProvider.create_volume_for_user(
                self.common_user_client,
                vtypes[0])

        api_response = user_account.Volumes.update(volume_a.id)
        self.assertEqual(
                api_response.status_code,
                expected_status_code,
                "Status code {0} was returned, instead of the expected {1}".\
                        format(api_response.status_code, expected_status_code))

        self.assertEqual(
                json.loads(api_response.content)['reason'],
                "Cannot update non-existent volume '{0}'".format(volume_a.id))
