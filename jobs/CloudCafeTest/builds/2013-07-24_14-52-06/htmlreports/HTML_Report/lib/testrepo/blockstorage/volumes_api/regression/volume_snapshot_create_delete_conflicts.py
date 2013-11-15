"""
@summary: Regression tests for Volumes Snapshot API
@copyright: Copyright (c) 2012 Rackspace US, Inc.
"""
from ccengine.common.tools import datagen
from ccengine.common.decorators import attr
from testrepo.common.testfixtures.blockstorage import VolumesAPIFixture


class CinderAPISnapshotRegressionTests(VolumesAPIFixture):
    """
    @summary: Regression for Cinder Snapshot API
    """

    def double_snapshot_create_conflict_regression(self, vol_type):
        """
            Creating back-to-back snapshots should result in a single 200 for
            the first snapshot, and 400's for every subsequent snapshot request
            until the first is completed.  Cycle repeats when another
            snapshot request is made.
        """
        self.vol_name = datagen.timestamp_string()

        #Create a volume
        resp = self.volumes_api_provider.create_available_volume(
            self.vol_name,
            self.volumes_api_provider.min_volume_size, vol_type)

        self.assertTrue(resp.ok, "Unable to create volume for test setup")
        self.assertIsNotNone(
            resp.entity,
            "Unable to deserialize volume create response in setup for test")

        self.volume = resp.entity
        self.addCleanup(
            self.volumes_api_provider.delete_volume_confirmed,
            self.volume.id)

        #Create a snapshot
        resp = self.volumes_api_provider.volumes_client.create_snapshot(
            self.volume.id, "{0}_snap1".format(self.vol_name))
        self.assertTrue(
            resp.ok,
            "Original returned {0}, expected 200".format(resp.status_code))
        self.assertIsNotNone(
            resp.entity, 'Could not deserialize snapshot create response')
        snapshot_1 = resp.entity

        self.addCleanup(
            self.volumes_api_provider.delete_snapshot_confirmed,
            snapshot_1.id)

        #create another snapshot while the first is running, expect failure
        resp = self.volumes_api_provider.volumes_client.create_snapshot(
            self.volume.id, "{0}_snap2".format(self.vol_name))

        self.assertFalse(
            resp.ok,
            "2nd snapshot create returned {0}, expected 400".format(
                resp.status_code))

        #Wait for the first snapshot, expect success
        resp = self.volumes_api_provider.wait_for_snapshot_status(
            snapshot_1.id, "available")

        self.assertTrue(
            resp.ok, "Original snapshot never reached available status")

    def snapshot_stuck_in_deleting_regression(self, vol_type):
        '''
        Create a volume
        Create a snapshot of the volume
        Wait for the volume snapshot to finish
        Create another snapshot of the original volume
        While the second snapshot it creating, (immediately) attempt to
            delete the first snapshot.
        Verify that the first snapshot remains in the 'available' state.
        Wait for the second snapshot to finish, expect success
        '''
        #Create a volume
        self.vol_name = datagen.timestamp_string()

        resp = self.volumes_api_provider.create_available_volume(
            self.vol_name,
            self.volumes_api_provider.min_volume_size,
            vol_type)

        self.assertTrue(resp.ok, "Volume create failed, cannot continue test")
        self.assertIsNotNone(
            resp.entity, "Volume create response could not be deserialized")
        self.volume = resp.entity
        self.addCleanup(
            self.volumes_api_provider.delete_volume_confirmed, self.volume.id)

        #Create a snapshot of the volume
        resp = self.volumes_api_provider.volumes_client.create_snapshot(
            self.volume.id, "{0}_snap1".format(self.vol_name))
        self.assertTrue(
            resp.ok,
            "Snapshot_1 create returned {0}, expected 200".format(
                resp.status_code))

        self.assertIsNotNone(
            resp.entity, "Volume create response could not be deserialized")
        snapshot_1 = resp.entity
        self.addCleanup(
            self.volumes_api_provider.delete_snapshot_confirmed, snapshot_1.id)

        #Wait for the volume snapshot to finish
        resp = self.volumes_api_provider.wait_for_snapshot_status(
            snapshot_1.id, "available")
        self.assertTrue(
            resp.ok, "Original snapshot never reached available status")

        #Create another snapshot of the original volume
        resp = self.volumes_api_provider.volumes_client.create_snapshot(
            self.volume.id, "{0}_snap2".format(self.vol_name))
        self.assertTrue(
            resp.ok,
            "Second snapshot returned {0}, expected 200".format(
                resp.status_code))
        snapshot_2 = resp.entity
        self.addCleanup(
            self.volumes_api_provider.delete_snapshot_confirmed, snapshot_2.id)

        #While the second snapshot it creating, immediately attempt to
        #delete the first snapshot.  Expect success (This could change)
        resp = self.volumes_api_provider.volumes_client.delete_snapshot(
            snapshot_1.id)
        self.assertTrue(
            resp.ok,
            "Delete of snapshot1 while snapshot2 was running did not succeed, "
            "it was expected to.")

        #Verify that the first snapshot remains in the 'available' state.
        resp = self.volumes_api_provider.volumes_client.get_snapshot_info(
            snapshot_1.id)

        self.assertEquals(
            resp.entity.status,
            'available',
            "First snapshot status was expected to be {0} after delete "
            "attempt, but reported status was {1}".format(
                'available', resp.entity.status))

        #Wait for the second snapshot to finish, expect success
        resp = self.volumes_api_provider.wait_for_snapshot_status(
            snapshot_2.id, "available")

        self.assertTrue(
            resp.ok, "Original snapshot never reached available status")

    @attr('negative', 'positive', 'regression')
    def test_sata_double_snapshot_create_conflict_regression(self):
        self.double_snapshot_create_conflict_regression("sata")

    @attr('negative', 'positive', 'regression')
    def test_ssd_double_snapshot_create_conflict_regression(self):
        self.double_snapshot_create_conflict_regression("ssd")

    @attr('negative', 'positive', 'regression')
    def test_sata_snapshot_stuck_in_deleting_regression(self):
        self.snapshot_stuck_in_deleting_regression("sata")

    @attr('negative', 'positive', 'regression')
    def test_ssd_snapshot_stuck_in_deleting_regression(self):
        self.snapshot_stuck_in_deleting_regression("ssd")
