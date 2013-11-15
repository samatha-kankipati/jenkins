'''
@summary: Lunr API Volume Smoke Tests - Create, List, Get Info, Update, Delete Volume.
@copyright: Copyright (c) 2012 Rackspace US, Inc.
'''
from testrepo.common.testfixtures.blockstorage import LunrAPIFixture
from ccengine.domain.types import LunrVolumeStatusTypes
from ccengine.domain.blockstorage.lunr_api import Volume as _VolumeDomainObject
from datetime import datetime
from unittest2.suite import TestSuite
import json

class LunrVolumeAPISmokeTest(LunrAPIFixture):
    '''
    @summary: Lunr API Volume Smoke Tests - Create, List, Get Info, Update, Delete Volume.
    '''
    @classmethod
    def setUpClass(cls):
        super(LunrVolumeAPISmokeTest, cls).setUpClass()

        #Create User Client
        cls.user_client = cls.LunrAPIProvider.create_user_client()
        cls.fixture_log.info("Created Account: %s" % cls.user_client.account_name)

        #Expected Volumes
        cls.expected_volumes = []
        cls.volume_name_prefix = "LunrVolumeAPISmokeTest_%d" % datetime.now().microsecond

    @classmethod
    def tearDownClass(cls):
        cls.LunrAPIProvider.delete_user_volumes(cls.user_client)
        cls.admin_client.Accounts.delete(cls.user_client.account_id)
        cls.fixture_log.info("Deleting Account: %s" % cls.user_client.account_name)
        super(LunrVolumeAPISmokeTest, cls).tearDownClass()

    def test_create_volume(self):
        self.vtypes = json.loads(self.admin_client.VolumeTypes.list().content)

        for vtype in self.vtypes:
            expected_name = self.volume_name_prefix + vtype['name']
            expected_size = vtype['min_size']
            api_response = self.user_client.Volumes.create(expected_name, expected_size, vtype['name'])
            self.assertTrue(api_response.ok, 'Create Volume call to Lunr API failed. API Response: %s' % json.loads(api_response.content))
            actual_volume = _VolumeDomainObject(**json.loads(api_response.content))
            wait_result = self.LunrAPIProvider.wait_for_volume_status(actual_volume.id, LunrVolumeStatusTypes.READY, self.user_client)
            self.assertTrue(wait_result.ok, "Volume not %s" % LunrVolumeStatusTypes.READY)
            self.assertEqual(actual_volume.id, expected_name, "Volume not created with indicated name")
            self.assertEqual(actual_volume.size, expected_size , "Volume not created with indicated size")
            self.assertEqual(actual_volume.volume_type_name, vtype['name'], "Volume not created with indicated type")

            self.fixture_log.info("Created Volume: %s Size: %i Type: %s" % (actual_volume.id, actual_volume.size, vtype['name']))
            self.expected_volumes.append(actual_volume)

    def test_list_volumes(self):
        api_response = self.user_client.Volumes.list()
        self.assertTrue(api_response.ok, "User List Volumes API call Failed: '%s'"
                                            % json.loads(api_response.content))

        actual_volume_list = self.LunrAPIProvider.convert_json_to_domain_object_list(json.loads(api_response.content), _VolumeDomainObject)
        for expected_volume in self.expected_volumes:
            self.assertIn(expected_volume, actual_volume_list, "Volume not in list")

    def test_get_volume_info(self):
        for expected_volume in self.expected_volumes:
            api_response = self.user_client.Volumes.get_info(expected_volume.id)
            self.assertTrue(api_response.ok, "User get Volume info API call Failed: '%s'"
                                             % json.loads(api_response.content))
            actual_volume_info = _VolumeDomainObject(**json.loads(api_response.content))
            self.assertEqual(actual_volume_info, expected_volume, "Volume info does not match")

    def test_update_volume_info(self):
        for expected_volume in self.expected_volumes:
            expected_size = 200
            api_response = self.user_client.Volumes.update(expected_volume.id, params={'size':expected_size})

            self.assertTrue(api_response.ok, "User Update Volume info API call Failed: '%s'"
                                             % json.loads(api_response.content))
            updated_volume =  _VolumeDomainObject(**json.loads(api_response.content))
            self.assertEquals(updated_volume.size, expected_size, "Volume size was not updated to %i" % expected_size)

    def test_delete_volume(self):
        for expected_volume in self.expected_volumes:
            expected_status = LunrVolumeStatusTypes.DELETED
            api_response = self.user_client.Volumes.delete(expected_volume.id)
            self.assertTrue(api_response.ok, "User Delete Volume API call Failed: '%s'"
                                             % json.loads(api_response.content))
            actual_deleted_volume = _VolumeDomainObject(**json.loads(api_response.content))
            wait_result = self.LunrAPIProvider.wait_for_volume_status(actual_deleted_volume.id, LunrVolumeStatusTypes.DELETED, self.user_client)
            self.assertTrue(wait_result.ok, "Deleted volume status not updated")

def load_tests(loader, standard_tests, pattern):
    suite = TestSuite()
    suite.addTest(LunrVolumeAPISmokeTest("test_create_volume"))
    suite.addTest(LunrVolumeAPISmokeTest("test_list_volumes"))
    suite.addTest(LunrVolumeAPISmokeTest("test_get_volume_info"))
    suite.addTest(LunrVolumeAPISmokeTest("test_update_volume_info"))
    suite.addTest(LunrVolumeAPISmokeTest("test_delete_volume"))
    return suite