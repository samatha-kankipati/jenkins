from ccengine.common.decorators import attr
from testrepo.common.testfixtures.blockstorage.compute_integration import \
    BlockStorageLinuxIntegrationFixture
from ccengine.common.tools import datagen


class VolumeWriteActions(BlockStorageLinuxIntegrationFixture):
    @classmethod
    def setUpClass(cls):
        super(VolumeWriteActions, cls).setUpClass()

    def test_restore_and_verify_backup_of_written_volume(self):
        self.test_env = self.setup_mounted_and_formatted_volume_on_server()

        file_name = datagen.timestamp_string("cbs_write_test_")
        file_block_size = 4096
        file_block_count = 25600

        original_md5_hash = self.write_and_verify_data_on_mounted_volume(
            self.test_env.ssh_conn, self.test_env.mount_point,
            file_name=file_name, file_block_size=file_block_size,
            file_block_count=file_block_count)

        #Force snapshot of volume
        resp = self.volumes_provider.create_available_snapshot(
            self.test_env.volume.id, force_create=True)

        assert resp.ok, 'Unable to create an available snapshot'
        snapshot = resp.entity

        #Create a new volume from the snapshot
        resp = self.volumes_provider.volumes_client.\
            create_volume_from_snapshot(snapshot.id, self.test_env.volume.size)
        assert resp.ok, (
            "Unable to restore snapshot to a volume of the original size")
        new_volume = resp.entity

        #Wait for volume to reach available state
        self.volumes_provider.wait_for_volume_status(
            new_volume.id, 'available')

        #attach new volume to server
        self.explicit_attach_volume_to_server(
            self.test_env.server.id, new_volume.id, '/dev/xvdi',
            expected_volume_status='in-use', add_cleanup=True)

        #Mount volume on server
        new_mount_point = datagen.timestamp_string(prefix='/mnt/cbsvolume-')
        self.test_env.ssh_conn.mount_disk_device(
            '/dev/xvdi', new_mount_point, 'ext3')

        #Verify md5 sum
        new_file_path = "{0}/{1}".format(new_mount_point, file_name)
        self.verify_md5_hash(
            self.test_env.ssh_conn, new_file_path, original_md5_hash)

