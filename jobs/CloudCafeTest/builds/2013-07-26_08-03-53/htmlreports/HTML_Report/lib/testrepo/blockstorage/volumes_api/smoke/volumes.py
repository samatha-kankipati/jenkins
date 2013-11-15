"""
@summary: happy path tests for Volumes API
@copyright: Copyright (c) 2012 Rackspace US, Inc.
"""
from unittest2.suite import TestSuite

from ccengine.common.tools import datagen
from ccengine.common.tools import logging_tools
from testrepo.common.testfixtures.blockstorage.volumes_api import \
    VolumesAPI_Fixture


def load_tests(loader, standard_tests, pattern):
    suite = TestSuite()
    print logging_tools.get_object_namespace(VolumesAPI_VolumesSmoke)
    suite.addTest(VolumesAPI_VolumesSmoke("test_create_volume"))
    suite.addTest(VolumesAPI_VolumesSmoke("test_get_volume_info"))
    suite.addTest(VolumesAPI_VolumesSmoke("test_list_volumes"))
    suite.addTest(VolumesAPI_VolumesSmoke("test_list_detailed_volumes"))
    suite.addTest(VolumesAPI_VolumesSmoke("test_update_volume_info"))
    suite.addTest(VolumesAPI_VolumesSmoke("test_delete_volume"))
    return suite


class VolumesAPI_VolumesSmoke(VolumesAPI_Fixture):
    """
    @summary: Volumes API Smoke Tests
    """

    @classmethod
    def setUpClass(cls):
        super(VolumesAPI_VolumesSmoke, cls).setUpClass()
        cls.expected_volumes = []
        cls.volume_types = cls.volumes_client.list_all_volume_types().entity

    @classmethod
    def tearDownClass(cls):
        super(VolumesAPI_VolumesSmoke, cls).tearDownClass()
        cls.volumes_provider.cleanup_volumes(cls.expected_volumes)

    def test_create_volume(self):
        VOLUME_SIZE = str(self.volumes_provider.min_volume_size)
        for volume_type in self.volume_types:
            volume_name = datagen.timestamp_string()

            api_response = self.volumes_client.create_volume(
                volume_name, VOLUME_SIZE, volume_type.name)

            self.assertTrue(
                api_response.ok,
                "Create Volume call failed: {0}".format(api_response))

            actual_volume = api_response.entity

            actual_volume.volume_type = self.volumes_provider.\
                get_type_name_by_id(actual_volume.volume_type)

            self.assertEqual(
                actual_volume.display_name,
                volume_name,
                "Volume not created with indicated name. {0} != {1}"
                .format(actual_volume.display_name, volume_name))

            self.assertEqual(
                str(actual_volume.size),
                str(VOLUME_SIZE),
                "Volume not created with indicated size")

            self.expected_volumes.append(api_response.entity)

        self.assertTrue(
            len(self.expected_volumes) > 0,
            'No volumes were created to test, aborting')

    def test_list_volumes(self):

        self.assertTrue(
            len(self.expected_volumes) > 0,
            'No volumes were created to test, aborting')

        api_response = self.volumes_client.list_all_volumes()
        self.assertTrue(
            api_response.ok,
            "List Volumes call to CinderAPI failed")

        actual_volume_list = api_response.entity

        self.assertEqual(
            type(actual_volume_list), type([]), msg="Expected list of volumes")

        for expected_volume in self.expected_volumes:
            self.assertIn(
                expected_volume, actual_volume_list, "Volume not in list")

    def test_list_detailed_volumes(self):

        self.assertTrue(
            len(self.expected_volumes) > 0,
            'No volumes were created to test, aborting')

        api_response = self.volumes_client.list_all_volumes_info()

        self.assertTrue(
            api_response.ok,
            "List Detailed Volumes call to CinderAPI failed")

        actual_volume_list = api_response.entity
        self.assertEquals(
            type(actual_volume_list),
            type([]),
            "Expected list of volumes, {0} recieved".format(
                type(actual_volume_list)))

        for expected_volume in self.expected_volumes:
            self.assertIn(
                expected_volume,
                actual_volume_list,
                "Expected volume not in list of available volumes")

    def test_get_volume_info(self):

        self.assertTrue(
            len(self.expected_volumes) > 0,
            'No volumes were created to test, aborting')

        for expected_volume in self.expected_volumes:
            api_response = self.volumes_client.get_volume_info(
                expected_volume.id)
            self.assertTrue(
                api_response.ok,
                "Get Volume Info call to CinderAPI failed")

            actual_volume_info = api_response.entity

            self.assertEqual(
                actual_volume_info,
                expected_volume,
                "Volume info does not match")

    def test_update_volume_info(self):

        self.assertTrue(
            len(self.expected_volumes) > 0,
            'No volumes were created to test, aborting')

        for expected_volume in self.expected_volumes:
            updated_display_name = "{0}-Updated".format(
                expected_volume.display_name)
            updated_display_desc = "{0}-Updated".format(
                expected_volume.display_description)

            api_response = self.volumes_client.update_volume_info(
                expected_volume.id, display_name=updated_display_name,
                display_description=updated_display_desc)

            self.assertTrue(
                api_response.ok,
                "Update Volume Info call to CinderAPI failed")

            updated_vol = api_response.entity

            #Check the volume info update response
            assert updated_vol.display_name == updated_display_name, \
                "Volume update response did not reflect updated display name"
            assert updated_vol.display_description == updated_display_desc, \
                ("Volume update response did not reflect updated display "
                 "description")

            #Check the volume info directly
            api_response = self.volumes_client.get_volume_info(
                expected_volume.id)

            self.assertTrue(
                api_response.ok,
                "Get Volume Info call to CinderAPI failed "
                " - Unable to verify updated volume info")

            volume_info = api_response.entity

            assert volume_info.display_name == updated_display_name, \
                "Volume info did not reflect updated display name"
            assert volume_info.display_description == updated_display_desc, \
                ("Volume info did not reflect updated display description")

    def test_delete_volume(self):

        self.assertTrue(
            len(self.expected_volumes) > 0,
            'No volumes were created to test, aborting')

        delete_error = False
        for volume in self.expected_volumes:
            api_response = self.volumes_client.delete_volume(volume.id)
            if not api_response.ok:
                delete_error = True
                self.fixture_log.error(
                    "Delete Volume API call failed for volume {0}".format(
                        volume.id))
        self.assertFalse(delete_error, "At least one snapshot delete failed")
