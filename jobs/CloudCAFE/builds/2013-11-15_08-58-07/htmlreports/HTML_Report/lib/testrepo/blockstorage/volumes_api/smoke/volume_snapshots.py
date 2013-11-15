"""
@summary: happy path tests for Volumes Snapshot API
@copyright: Copyright (c) 2012 Rackspace US, Inc.
"""
from unittest2.suite import TestSuite
from time import sleep

from ccengine.common.tools import datagen
from ccengine.domain.types import CinderSnapshotStatusTypes
from testrepo.common.testfixtures.blockstorage.volumes_api import \
    VolumesAPI_Fixture


def load_tests(loader, standard_tests, pattern):
    suite = TestSuite()
    suite.addTest(VolumesAPISnapshotSmoke("test_create_snapshots"))
    suite.addTest(VolumesAPISnapshotSmoke("test_list_snapshots"))
    suite.addTest(VolumesAPISnapshotSmoke("test_list_detailed_snapshots"))
    suite.addTest(VolumesAPISnapshotSmoke("test_get_snapshot_info"))
    suite.addTest(VolumesAPISnapshotSmoke("test_update_snapshot_info"))
    suite.addTest(VolumesAPISnapshotSmoke("test_instant_snapshot_delete"))
    suite.addTest(VolumesAPISnapshotSmoke(
        "test_delete_volume_that_previously_had_a_snapshot_made_of_it"))
    return suite


class VolumesAPISnapshotSmoke(VolumesAPI_Fixture):
    """
    @summary: Happy path excercise of Volumes Snapshot API
    """

    @classmethod
    def setUpClass(cls):
        super(VolumesAPISnapshotSmoke, cls).setUpClass()

        #Create Volumes
        cls.expected_volumes = []
        cls.volume_types = cls.volumes_client.list_all_volume_types().entity

        volume_name_prefix = datagen.timestamp_string("CBSQE_{0}_TestVolume_")

        VOLUME_SIZE = int(cls.volumes_provider.min_volume_size)
        #cls.snapshot_timeout = max((VOLUME_SIZE * 30), 500)
        for volume_type in cls.volume_types:
            volume_name = volume_name_prefix + volume_type.name
            provider_response = cls.volumes_provider.\
                create_available_volume(
                    volume_name, VOLUME_SIZE, volume_type.name)
            if not provider_response.ok:
                cls.fixture_log.info(
                    "Could not create a volume. Will run tearDownClass to"
                    " cleanup")
                cls.assertClassSetupFailure(
                    "Failed to create volume in class setup")
            else:
                created_volume = provider_response.entity
                cls.expected_volumes.append(created_volume)

        #Expected Snapshots
        cls.expected_snapshots = []

    @classmethod
    def tearDownClass(cls):
        cls.volumes_provider.cleanup_volumes(cls.expected_volumes)
        super(VolumesAPISnapshotSmoke, cls).tearDownClass()

    def create_and_verify_snapshot(self, volume, add_cleanup=True):
        snapshot_name = volume.display_name
        api_response = self.volumes_client.create_snapshot(
            volume.id, snapshot_name)

        self.assertTrue(
            api_response.ok, "API call returned {0}, expected 2XX".format(
                api_response.status_code))

        created_snapshot = api_response.entity

        wait_result = self.volumes_provider.wait_for_snapshot_status(
            created_snapshot.id, CinderSnapshotStatusTypes.AVAILABLE)
        self.assertTrue(wait_result.ok, "Snapshot create failed")

        created_snapshot = wait_result.response.entity

        self.assertEqual(
            created_snapshot.display_name,
            snapshot_name,
            "Snapshot reporting incorrect name")

        self.assertEqual(
            created_snapshot.size,
            volume.size,
            "Snapshot reporting incorrect size")

        if add_cleanup:
            self.expected_snapshots.append(created_snapshot)

        return created_snapshot

    def test_create_snapshots(self):
        for volume in self.expected_volumes:
            self.create_and_verify_snapshot(volume)

    def test_list_snapshots(self):
        api_response = self.volumes_client.list_all_snapshots()
        self.assertTrue(api_response.ok, "List Snapshots API call failed")

        actual_snapshots = api_response.entity
        for expected_snapshot in self.expected_snapshots:
            self.assertIn(
                expected_snapshot, actual_snapshots, "Snapshot not in List")

    def test_list_detailed_snapshots(self):
        api_response = self.volumes_client.list_all_snapshots_info()
        self.assertTrue(
            api_response.ok, "List Detailed Snapshots API call failed")

        actual_snapshots = api_response.entity
        for expected_snapshot in self.expected_snapshots:
            self.assertIn(
                expected_snapshot, actual_snapshots, "Snapshot not in List")

    def test_get_snapshot_info(self):
        for expected_snapshot in self.expected_snapshots:
            api_response = self.volumes_client.get_snapshot_info(
                expected_snapshot.id)
            self.assertTrue(
                api_response.ok, "Snapshot Get Info API call failed")

            actual_snapshot = api_response.entity
            self.assertEqual(
                actual_snapshot, expected_snapshot,
                "Snapshot info does not match")

    def test_update_snapshot_info(self):
        for expected_snapshot in self.expected_snapshots:

            updated_display_name = "{0}-Updated".format(
                expected_snapshot.display_name)
            updated_display_desc = "{0}-Updated".format(
                expected_snapshot.display_description)

            resp = self.volumes_client.update_snapshot_info(
                expected_snapshot.id, display_name=updated_display_name,
                display_description=updated_display_desc)

            self.assertTrue(
                resp.ok, "Snapshot Info Update API call failed")

            updated_snap = resp.entity

            #Check the snapshot info update response
            assert updated_snap.display_name == updated_display_name, \
                "Snapshot update response did not reflect updated display name"
            assert updated_snap.display_description == updated_display_desc, \
                ("Snapshot update response did not reflect updated display "
                 "description")

            #Check the snapshot info directly
            resp = self.volumes_client.get_snapshot_info(
                expected_snapshot.id)

            self.assertTrue(
                resp.ok,
                "Get Snapshot Info call to CinderAPI failed "
                " - Unable to verify updated snapshot info")

            snapshot_info = resp.entity

            assert snapshot_info.display_name == updated_display_name, \
                "Snapshot info did not reflect updated display name"
            assert snapshot_info.display_description == updated_display_desc, \
                ("Snapshot info did not reflect updated display description")

    def test_instant_snapshot_delete(self):
        """
        Issue all the deletes first, then wait to make sure they are all gone
        'instantly'
        """
        delete_failures = []
        for snapshot in self.expected_snapshots:
            api_response = self.volumes_client.delete_snapshot(snapshot.id)
            if not api_response.ok:
                delete_failures.append(
                    (snapshot.id,
                     "response status code: {0}".format(api_response.id)))
                self.fixture_log.error(
                    "Delete Snapshot API call failed for snapshot {0}".format(
                        snapshot))

        self.assertTrue(
            len(delete_failures) == 0,
            "Some snapshot deletes failed: {0}".format(delete_failures))

        #Although 'instant' implies zero time, reality means that it should
        #take about a second.  I'm being generous and waiting two.
        for snapshot in self.expected_snapshots:
            for x in range(5):
                sleep(2)
                api_response = self.volumes_client.get_snapshot_info(
                    snapshot.id)
                if api_response.status_code == 404:
                    break

            self.assertEquals(
                api_response.status_code, 404,
                "The snapshot {0} should be deleted by now, but a delete call"
                " to it returned a {1} instead of the expected 404".format(
                    snapshot.id, api_response.status_code))

    def test_delete_volume_that_previously_had_a_snapshot_made_of_it(self):
        failures = []
        for volume in self.expected_volumes:
            resp = self.volumes_client.delete_volume(volume.id)
            if not resp.ok:
                failures.append("Could not delete volume {0}".format(volume.id))

        assert len(failures) == 0, str(failures)
