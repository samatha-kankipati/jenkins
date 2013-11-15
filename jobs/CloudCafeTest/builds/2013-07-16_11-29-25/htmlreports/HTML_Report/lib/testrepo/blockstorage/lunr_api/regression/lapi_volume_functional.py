'''
@summary: Functional Lunr API Volume Smoke Tests
@copyright: Copyright (c) 2012 Rackspace US, Inc.
'''
from datetime import datetime
import json
from ccengine.domain.blockstorage.lunr_api import Volume as _VolumeDomainObject
from testrepo.common.testfixtures.blockstorage import LunrAPIFixture


class LunrVolumeFunctionalTest(LunrAPIFixture):
    '''
    @summary: Functional Lunr API Volume Smoke Tests
    '''
    @classmethod
    def setUpClass(cls):
        super(LunrVolumeFunctionalTest, cls).setUpClass()

        cls.common_user_client = cls.LunrAPIProvider.create_user_client()
        cls.fixture_log.info("Common User Account: {0}".format(
                cls.common_user_client.account_id))
        cls.vtypes = json.loads(cls.admin_client.VolumeTypes.list().content)
        cls.account_clients_to_cleanup = [cls.common_user_client]

        #Change this so that it pulls min volume size from vtypes, not config
        cls.min_volume_size = cls.config.lunr_api.min_volume_size

    @classmethod
    def tearDownClass(cls):
        for account in cls.account_clients_to_cleanup:
            cls.LunrAPIProvider.cleanup_account(account)
        super(LunrVolumeFunctionalTest, cls).tearDownClass()

    def test_list_volumes_for_invalid_account(self):
        invalid_user = self.LunrAPIProvider.create_invalid_user()
        self.account_clients_to_cleanup.append(invalid_user)

        api_response = invalid_user.Volumes.list()
        self.assertTrue(
                api_response.ok,
                "Could not list a volume for invalid account: '{0}'".format(
                        json.loads(api_response.content)))
        self.assertEqual(
                json.loads(api_response.content),
                [],
                "List Volumes returned with {0} instead of an empty list []".\
                        format(json.loads(api_response.content)))

        self.assertTrue(
                self.LunrAPIProvider.is_account_auto_generated(
                        invalid_user.account_id,
                        self.admin_client),
                "An account was not auto generated.")

    def test_create_volume_for_invalid_account(self):
        '''
        @summary: Creating an auto generated account via creating a volume
                  with an invalid account
        '''
        volume_name = "TestCreateVolumeFunctional_{0}".format(
                datetime.now().microsecond)
        invalid_user = self.LunrAPIProvider.create_invalid_user()
        self.account_clients_to_cleanup.append(invalid_user)

        api_response = invalid_user.Volumes.create(
                volume_name,
                self.min_volume_size,
                'SSD')

        self.assertTrue(
                api_response.ok,
                "Could not create a volume with invalid account {0}".format(
                        json.loads(api_response.content)))

        volume_domain_object = _VolumeDomainObject(
                **json.loads(api_response.content))

        self.assertEqual(
                volume_domain_object.id,
                volume_name,
                "Volume not created with expected name.")

        self.assertEqual(
                volume_domain_object.volume_type_name,
                'SSD',
                "Volume not created with expected type.")

        self.assertEqual(
                volume_domain_object.size,
                self.min_volume_size,
                "Volume not created with expected size.")

        self.assertTrue(
                self.LunrAPIProvider.is_account_auto_generated(
                        invalid_user.account_id,
                        self.admin_client),
                "An account '{0}' was not auto generated.".format(
                        invalid_user.account_id))

    def test_get_volume_info_from_auto_generated_account(self):
        '''
        @summary: Get Info of a volume created by an auto generated account
        '''
        invalid_user = self.LunrAPIProvider.create_invalid_user()
        self.account_clients_to_cleanup.append(invalid_user)

        auto_generated_account = self.LunrAPIProvider.\
                create_auto_generated_account(invalid_user, self.admin_client)

        self.assertEqual(
                auto_generated_account.status,
                'ACTIVE',
                "Auto Generated Account status NOT Active")

        volume_name = "TestVolumeInfoFunctional_{0}".format(
                datetime.now().microsecond)
        api_response = invalid_user.Volumes.create(
                volume_name,
                self.min_volume_size,
                'SSD')

        self.assertTrue(
                api_response.ok,
                "Could not create a volume for auto generated account")

        expected_volume_domain_object = _VolumeDomainObject(
                **json.loads(api_response.content))

        api_response = invalid_user.Volumes.get_info(
                expected_volume_domain_object.id)
        self.assertTrue(
                api_response.ok,
                "Could not get info on volume '{0}' created by Auto "
                "Generated Account: '{1}'".format(
                        expected_volume_domain_object.id,
                        json.loads(api_response.content)))
