from datetime import datetime
import unittest2 as unittest
from unittest2.suite import TestSuite
from testrepo.common.testfixtures.fixtures import BaseTestFixture
from ccengine.providers.blockstorage.cindershell import CinderShellProvider
from ccengine.domain.types import NovaVolumeStatusTypes as _NovaVolumeStatusTypes
from ccengine.common.decorators import attr


def load_tests(loader, standard_tests, pattern):
    suite = TestSuite()
    suite.addTest(CinderShell_SmokeTest("test_create_volume"))
    suite.addTest(CinderShell_SmokeTest("test_create_volume_snapshot"))
    suite.addTest(CinderShell_SmokeTest("test_create_volume_from_snapshot"))
    suite.addTest(CinderShell_SmokeTest(
            "test_delete_volume_created_from_snapshot"))
    suite.addTest(CinderShell_SmokeTest("test_delete_volume_snapshot"))
    suite.addTest(CinderShell_SmokeTest("test_delete_volume"))
    return suite


class CinderShell_SmokeTest(BaseTestFixture):
    '''
    @summary: Smoke tests for the python-cindershell cli tool
    '''
    @classmethod
    def setUpClass(cls):
        super(CinderShell_SmokeTest, cls).setUpClass()
        stamp = datetime.now().microsecond

        cls.CinderShellProvider = CinderShellProvider(cls.config)
        cls.volume_name = "CinderShellTest_Volume:%d" % stamp
        cls.volume_size = int(cls.config.cinder_shell.min_volume_size)
        cls.snapshot_name = cls.volume_name + "-snapshot"
        cls.volume_from_snapshot_name = cls.snapshot_name + "-new_volume"

    @classmethod
    def tearDownClass(cls):
        cls.CinderShellProvider.delete_volume_snapshot(cls.snapshot_name)
        cls.CinderShellProvider.delete_volume(cls.volume_from_snapshot_name)
        cls.CinderShellProvider.delete_volume(cls.volume_name)
        super(CinderShell_SmokeTest, cls).tearDownClass()

    def test_create_volume(self):
        self.fixture_log.info("Testing creating a volume")
        volume_type_domain_object = self.CinderShellProvider.select_volume_type()
        self.assertIsNotNone(volume_type_domain_object, "Could not select a volume type to create volume")

        volume = self.CinderShellProvider.create_volume(self.volume_name, volume_type_domain_object.Name, self.volume_size)
        self.assertIsNotNone(volume, "Unable to create new volume!")
        self.assertEqual(volume['Size'], str(self.volume_size), "Volume created with incorrect size")
        self.assertEqual(volume['VolumeType'], volume_type_domain_object.Name, "Volume created with incorrect type")
        self.fixture_log.info("Volume Created: %s" % volume)

    def test_create_volume_snapshot(self):
        self.fixture_log.info("Testing creating a volume snapshot")
        new_volume_snapshot = self.CinderShellProvider.create_volume_snapshot(self.volume_name, display_name=self.snapshot_name)
        self.assertNotEqual(new_volume_snapshot, {}, "Unable to create new volume snapshot!")
        self.assertEqual(new_volume_snapshot['DisplayName'], self.snapshot_name, "Created Volume Snapshot name not created as expected")
        self.assertEqual(new_volume_snapshot['Status'], _NovaVolumeStatusTypes.AVAILABLE, "Created Volume Snapshot status is NOT Available")

    def test_create_volume_from_snapshot(self):
        self.fixture_log.info("Testing creating a volume from a snapshot")
        volume_from_snapshot = self.CinderShellProvider.create_volume_from_snapshot(self.volume_from_snapshot_name, self.snapshot_name, volume_size=self.volume_size)
        self.assertIsNotNone(volume_from_snapshot, "Unable to create new volume from snapshot!")
        self.assertEqual(volume_from_snapshot['DisplayName'], self.volume_from_snapshot_name, "Volume from Snapshot created with incorrect Name")
        self.assertEqual(volume_from_snapshot['Status'], _NovaVolumeStatusTypes.AVAILABLE, "Volume from Snapshot status is NOT available.")

    def test_delete_volume_created_from_snapshot(self):
        self.fixture_log.info("Testing deleting and removing volume from a snapshot: %s" % self.volume_from_snapshot_name)
        is_volume_from_snapshot_deleted = self.CinderShellProvider.delete_volume(self.volume_from_snapshot_name)
        self.assertTrue(is_volume_from_snapshot_deleted, "Unable to delete and remove volume %s!" % self.volume_from_snapshot_name)

    def test_delete_volume_snapshot(self):
        self.fixture_log.info("Testing deleting and removing volume snapshot: %s" % self.snapshot_name)
        is_snapshot_deleted = self.CinderShellProvider.delete_volume_snapshot(self.snapshot_name)
        self.assertTrue(is_snapshot_deleted, "Unable to delete and remove Snapshot %s!" % self.snapshot_name)

    def test_delete_volume(self):
        self.fixture_log.info("Testing deleting and removing a volume: %s" % self.volume_name)
        is_volume_name_deleted = self.CinderShellProvider.delete_volume(self.volume_name)
        assert is_volume_name_deleted == True, "Unable to delete and remove volume %s!" % self.volume_name
