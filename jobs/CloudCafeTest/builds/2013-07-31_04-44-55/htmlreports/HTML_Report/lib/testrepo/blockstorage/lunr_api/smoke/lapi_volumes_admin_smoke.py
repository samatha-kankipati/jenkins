'''
@summary: Lunr API Volume Admin smoke tests - Create, List, Get Info, Update, Delete Volume as an Admin
@copyright: Copyright (c) 2012 Rackspace US, Inc.
'''
from testrepo.common.testfixtures.blockstorage import LunrAPIFixture
from ccengine.domain.blockstorage.lunr_api import Volume as _VolumeDomainObject
from ccengine.domain.types import LunrVolumeStatusTypes
from unittest2.suite import TestSuite
import json


class LunrVolumeAdminAPISmokeTest(LunrAPIFixture):
    '''
    @summary: Lunr API Volume Admin smoke tests
    Create, List, Get Info, Update, Delete Volume as an Admin
    '''
    @classmethod
    def setUpClass(cls):
        super(LunrVolumeAdminAPISmokeTest, cls).setUpClass()

        #Create User Client
        cls.fixture_log.debug("Creating new user account and client")
        cls.user_client = cls.LunrAPIProvider.create_user_client()
        cls.fixture_log.debug("Created Account: %s" % cls.user_client.account_id)

        #Create Volumes
        cls.vtypes = json.loads(cls.admin_client.VolumeTypes.list().content)
        cls.expected_volumes = []
        for vtype in cls.vtypes:
            created_volume = cls.LunrAPIProvider.create_volume_for_user(
                    cls.user_client, vtype)
            if created_volume is None:
                raise Exception("Could not create a volume with Active status")
            cls.expected_volumes.append(created_volume)

    @classmethod
    def tearDownClass(cls):
        cls.LunrAPIProvider.delete_user_volumes(cls.user_client)
        cls.admin_client.Accounts.delete(cls.user_client.account_id)
        cls.fixture_log.info("Deleting Account: %s" % cls.user_client.account_name)
        super(LunrVolumeAdminAPISmokeTest, cls).tearDownClass()

    def test_list_volumes(self):
        api_response = self.admin_client.Volumes.list()
        self.assertTrue(api_response.ok, "User List Volumes API call Failed")

        actual_volume_list = self.LunrAPIProvider.convert_json_to_domain_object_list(json.loads(api_response.content), _VolumeDomainObject)
        for expected_volume in self.expected_volumes:
            self.assertIn(expected_volume, actual_volume_list, "Volume not in list")

    def test_get_volume_info(self):
        for expected_volume in self.expected_volumes:
            api_response = self.admin_client.Volumes.get_info(expected_volume.id)
            self.assertTrue(api_response.ok, "User get Volume info API call Failed: '%s'"
                                             % json.loads(api_response.content))
            actual_volume_info = _VolumeDomainObject(**json.loads(api_response.content))
            self.assertEqual(actual_volume_info, expected_volume, "Volume info does not match")

    def test_update_volume_info(self):
        for expected_volume in self.expected_volumes:
            expected_size = 200
            api_response = self.admin_client.Volumes.update(expected_volume.id, params={'size':expected_size})

            self.assertTrue(api_response.ok, "User Update Volume info API call Failed: '%s'"
                                             % json.loads(api_response.content))
            updated_volume = _VolumeDomainObject(**json.loads(api_response.content))
            self.assertEquals(updated_volume.size, expected_size, "Volume size was not updated to %i" % expected_size)

    def test_delete_volume(self):
        for expected_volume in self.expected_volumes:
            api_response = self.admin_client.Volumes.delete(expected_volume.id)
            self.assertTrue(api_response.ok, "User Delete Volume API call Failed: '%s'"
                                             % json.loads(api_response.content))
            actual_deleted_volume = _VolumeDomainObject(**json.loads(api_response.content))
            wait_result = self.LunrAPIProvider.wait_for_volume_status(actual_deleted_volume.id, LunrVolumeStatusTypes.DELETED, self.admin_client)
            self.assertTrue(wait_result.ok, "Deleted volume status not updated")

def load_tests(loader, standard_tests, pattern):
    suite = TestSuite()
    suite.addTest(LunrVolumeAdminAPISmokeTest("test_list_volumes"))
    suite.addTest(LunrVolumeAdminAPISmokeTest("test_get_volume_info"))
    suite.addTest(LunrVolumeAdminAPISmokeTest("test_update_volume_info"))
    suite.addTest(LunrVolumeAdminAPISmokeTest("test_delete_volume"))
    return suite