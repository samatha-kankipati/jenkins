"""
@copyright: Copyright (c) 2012 Rackspace US, Inc.
"""
from ccengine.common.tools import datagen
from ccengine.common.decorators import attr
from testrepo.common.testfixtures.blockstorage.volumes_api import \
    VolumesAPI_Fixture


class VolumeSnapshotRestoreSmokeTests(VolumesAPI_Fixture):
    """
    @summary: Test create volume from snapshot
    """

    @classmethod
    def setUpClass(cls):
        super(VolumeSnapshotRestoreSmokeTests, cls).setUpClass()
        cls.expected_volumes = []
        cls.volume_types = cls.volumes_client.list_all_volume_types().entity
        vol_name = datagen.timestamp_string(prefix="testvolume")
        snap_name = "{0}_snapshot".format(vol_name)

        #create volume
        resp = cls.volumes_provider.create_available_volume(
            vol_name, cls.volumes_provider.min_volume_size, "sata")
        assert resp.ok is True, "Volume create in setup failed"
        assert resp.entity is not None, (
            "Error deserializing volume create api response, response entity "
            "is None")
        cls.test_volume = resp.entity
        cls.expected_volumes.append(cls.test_volume)

        #create snapshot
        resp = cls.volumes_provider.create_available_snapshot(
            cls.test_volume.id, snap_name)
        assert resp.ok is True, "snapshot create in setup failed"
        assert resp.entity is not None, (
            "Error deserializing snapshot create api response, response entity"
            " is None")
        cls.test_volume_snapshot = resp.entity

    @classmethod
    def tearDownClass(cls):
        cls.volumes_provider.cleanup_volumes(cls.expected_volumes)
        super(VolumeSnapshotRestoreSmokeTests, cls).tearDownClass()

    @attr('positive', 'regression', 'smoke')
    def test_create_volume_from_snapshot(self):

        vol_name = "built_from_backup_of_{0}".format(
            self.test_volume.display_name)
        resp = self.volumes_client.create_volume_from_snapshot(
            display_name=vol_name, size=self.test_volume.size,
            snapshot_id=self.test_volume_snapshot.id)
        self.assertTrue(resp.ok, "Create volume from from snapshot failed")
        self.assertIsNotNone(
            resp.entity,
            "Failure deserializing create volume from snapshot response, "
            "response entity is None")
        new_volume = resp.entity

        self.expected_volumes.append(new_volume)
        provresp = self.volumes_provider.wait_for_volume_status(
            new_volume.id, "available")
        self.assertTrue(
            provresp.ok,
            "Volume created from snapshot never reached available status")
