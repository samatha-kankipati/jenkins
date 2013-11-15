from ccengine.common.decorators import attr
from testrepo.common.testfixtures.blockstorage.compute_integration import \
    BlockStorageLinuxIntegrationFixture
from ccengine.common.tools import datagen


class VolumeWriteActions(BlockStorageLinuxIntegrationFixture):
    @classmethod
    def setUpClass(cls):
        super(VolumeWriteActions, cls).setUpClass()

    def test_restore_backup_of_written_volume_to_larger_volume(self):
        """Tests restoring a volume snapshot to a larger volume size

        TODO:  Make the bulk of this test part of the setup, and have the
        methods test individual device properties, like file md5 hash,
        filesystem integrity, disk size, etc.
        """

        self.test_env = self.setup_mounted_and_formatted_volume_on_server()
        file_name = datagen.timestamp_string("cbs_write_test_")
        file_block_size = 4096
        file_block_count = 25600

        #Write a file to the original volume, and retain that file's md5 hash
        original_md5_hash = self.write_and_verify_data_on_mounted_volume(
            self.test_env.ssh_conn, self.test_env.mount_point,
            file_name=file_name, file_block_size=file_block_size,
            file_block_count=file_block_count)

        #Force snapshot of volume
        resp = self.volumes_provider.create_available_snapshot(
            self.test_env.volume.id, force_create=True)

        self.assertTrue(resp.ok, "Unable to create an available snapshot")
        snapshot = resp.entity

        #restore snapshot to a new volume
        new_larger_size = int(self.test_env.volume.size) + 100
        resp = self.volumes_provider.volumes_client.\
            create_volume_from_snapshot(snapshot.id, new_larger_size)
        self.assertTrue(
            resp.ok, "Unable to restore snapshot to a larger volume size")
        new_volume = resp.entity

        #Wait for restored volume to reach available state
        self.volumes_provider.wait_for_volume_status(
            new_volume.id, 'available')

        #attach restored volume to server
        self.explicit_attach_volume_to_server(
            self.test_env.server.id, new_volume.id, '/dev/xvdi',
            expected_volume_status='in-use', add_cleanup=True)

        #Mount restored volume on server
        new_mount_point = datagen.timestamp_string(prefix='/mnt/cbsvolume-')
        self.test_env.ssh_conn.mount_disk_device(
            '/dev/xvdi', new_mount_point, 'ext3')

        #Verify md5 sum
        new_file_path = "{0}/{1}".format(new_mount_point, file_name)
        self.verify_md5_hash(
            self.test_env.ssh_conn, new_file_path, original_md5_hash)
