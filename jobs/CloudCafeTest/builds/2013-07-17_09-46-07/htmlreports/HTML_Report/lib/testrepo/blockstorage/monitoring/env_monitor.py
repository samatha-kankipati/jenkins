'''
@summary: Lunr API Volume Smoke Tests - Create, List, Get Info, Update, Delete Volume.
@copyright: Copyright (c) 2012 Rackspace US, Inc.
'''
from unittest2.suite import TestSuite
from testrepo.common.testfixtures.blockstorage import CloudBlockStorage_LinuxIntegrationFixture
from ccengine.common.tools import datagen
from ccengine.common.decorators import attr
import os
#from ccengine.clients.remote_instance.linux.base_client import BasePersistentLinuxClient as _LinuxClient

def load_tests(loader, standard_tests, pattern):
    suite = TestSuite()
    suite.addTest(BlockStorageEnvMonitor("test_write_to_and_unmount_volume"))
    suite.addTest(BlockStorageEnvMonitor("test_detach_and_snapshot_volume"))
    #suite.addTest(BlockStorageEnvMonitor("test_create_volume_from_snapshot"))
    suite.addTest(BlockStorageEnvMonitor("test_manual_attach_original_volume_to_server"))
    suite.addTest(BlockStorageEnvMonitor("test_mount_original_volume_and_verify_data"))
    #suite.addTest(BlockStorageEnvMonitor("test_manual_attach_volume_copy_to_server"))
    #suite.addTest(BlockStorageEnvMonitor("test_mount_volume_copy_and_verify_data"))
    return suite


class BlockStorageEnvMonitor(CloudBlockStorage_LinuxIntegrationFixture):
    '''
    @summary: Runs through a complete happy-path exercise of the api
              Designed to run every hour in an environment to make sure
              everything is still working.
    '''
    #Server and volume are created in setup
    #volume is attached, mounted, and formatted in setup

    #Write to volume
    #Create snapshot of volume
    #restore snapshot to a new volume

    def test_write_to_and_unmount_volume(self):
        #Write 1 GB to disk
        blocksize = 4096
        count = 262144

        sshresp = self.remote_server.write_random_data_to_disk(self.testvolume_mountpoint, self.volume_file_name, blocksize, count)
        assert sshresp is not None, 'Write to monted volume over ssh failed to return'

        sshresp = self.remote_server.get_file_size_bytes(self.volume_file_path)
        assert sshresp is not None, 'wc -c of file on monted volume over ssh failed to return anything'

        self.testfile_md5hash = self.remote_server.get_file_md5hash(self.volume_file_path)
        assert self.testfile_md5hash is not None, 'Unable to get md5hash of remote testfile'

        #Unmount volume
        '''@TODO: Figure out some way to verify the unmount'''
        self.remote_server.unmount_disk_device(self.testvolume_mountpoint)

    def test_detach_and_snapshot_volume(self):
        #Detach Volume
        resp = self.volume_attachments_api_provider.detach_volume_confirmed(self.testvolume_attachment.id, self.testserver.id)
        assert resp.ok, 'Volume did not detach from server correctly'

        #Wait for volume to become available
        resp = self.volumes_api_provider.wait_for_volume_status(self.testvolume.id, 'available')
        assert resp.ok, 'Volume did not become available after detaching within alloted time period'

        #Create available snapshot
        snapshotname = str(self.testvolume.display_name) + '_snapshot'
        resp = self.volumes_api_provider.create_available_snapshot(self.testvolume.id, snapshotname)
        assert resp.ok, 'Unable to create available snapshot after detaching volume from server'
        assert resp.entity is not None, 'Valid snapshot domain object was not returned from create_available_snapshot'
        self.testsnapshot = resp.entity

    def test_create_volume_from_snapshot(self):
        resp = self.volumes_api_provider.volumes_client.create_volume(display_name=str(self.testvolume.display_name) + '_recreated', snapshot_id=self.testsnapshot.id)
        assert resp.ok, "Volume create (from snapshot) returned an error code"
        assert resp.entity is not None, 'Volume create (from snapshot) entity is None, error encountered during response deserialization'
        resp = self.volumes_api_provider.wait_for_volume_status(resp.entity.id, 'available')
        assert resp.ok, "Volume created from snapshot did not reach the 'available' state within the alloted time."

    def test_manual_attach_original_volume_to_server(self):
        #Auto Attach volume to server
        self.fixture_log.info('Attaching Volume to the server')
        resp = self.volume_attachments_api_provider.client.attach_volume(self.server_id, self.testvolume.id, self.testvolume_device_name)
        assert resp.ok, 'Unable to attach volume to server'
        assert resp.entity is not None, 'Error deserializing auto attach response. Response entity is None'
        self.testvolume_attachment = resp.entity

    def test_mount_original_volume_and_verify_data(self):
        self.testvolume_device_name = '/dev/xvde'
        self.testvolume_fstype = 'ext3'
        #self.volume_file_path = os.path.join(self.testvolume_mountpoint, self.volume_file_name)
        self.remote_server.mount_disk_device(self.testvolume_device_name, self.testvolume_mountpoint, self.testvolume_fstype)

        #Get md5hash of file on re-mounted volume
        #md5hash = self.remote_server.get_file_md5hash(self.volume_file_path)
        #self.assertEqual(str(self.testfile_md5hash), str(md5hash), 'Original and remounted file md5 hashes are not equal')

    def test_manual_attach_volume_copy_to_server(self):
        #Auto Attach volume to server
        self.fixture_log.info('Attaching Volume to the server')
        resp = self.volume_attachments_api_provider.client.attach_volume(self.server_id, self.testvolume.id, self.testvolume_device_name)
        assert resp.ok, 'Unable to attach volume to server'
        assert resp.entity is not None, 'Error deserializing auto attach response. Response entity is None'
        self.testvolume_attachment = resp.entity

    def test_mount_volume_copy_and_verify_data(self):
        self.testvolume_device_name = '/dev/xvdf'
        self.testvolume_fstype = 'ext3'
        self.testvolume_mountpoint = datagen.timestamp_string('/mnt/cbsvolume-copy-')
