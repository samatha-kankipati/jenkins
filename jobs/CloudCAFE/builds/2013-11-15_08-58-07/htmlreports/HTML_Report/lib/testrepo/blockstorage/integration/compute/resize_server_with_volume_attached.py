from ccengine.common.decorators import attr
from testrepo.common.testfixtures.blockstorage.compute_integration import \
    BlockStorageLinuxIntegrationFixture


class ResizeServerWithVolumeAttached(BlockStorageLinuxIntegrationFixture):
    """Verifies correct volume behavior for server resize scenarios where a
    volume is attached
    """

    @attr('smoke')
    def test_resize_server_with_volume_attached(self):
        testenv = self.setup_server_with_volume_attached()

        #Resize server with volume attached
        new_flavor = self.config.compute_api.flavor_ref_alt
        server = self.compute_provider.resize_and_confirm(
            testenv.server.id, new_flavor)
        assert server is not None, 'Server resize failed'

        resp = self.volumes_provider.wait_for_volume_status(
            testenv.volume.id, 'in-use', timeout=60)

        assert resp.ok, \
            ("Volume did not return to the 'in-use' status after"
             " the server it was attached to was rebooted")

    @attr('smoke')
    def test_resize_and_revert_server_with_volume_attached(self):
        testenv = self.setup_server_with_volume_attached()

        #Resize and revert server with volume attached
        new_flavor = self.config.compute_api.flavor_ref_alt
        server = self.compute_provider.resize_and_revert(
            testenv.server.id, new_flavor)
        assert server is not None, 'Server resize and revert failed'

        resp = self.volumes_provider.wait_for_volume_status(
            testenv.volume.id, 'in-use', timeout=60)

        assert resp.ok, \
            ("Volume did not return to the 'in-use' status after"
             " the server it was attached to was rebooted")

    @attr('regression')
    def test_resize_server_with_mounted_volume_then_verify_writability(self):
        """
            Creates server
            creates volume
            attaches volume to server
            Mounts volume as device on server
            formats device
            resizes server
            re-mounts volume
            Writes file to disk
            verifes written file
        """

        #Setup server with mounted volume
        testenv = self.setup_mounted_and_formatted_volume_on_server()

        #Resize server with mounted volume
        new_flavor = self.config.compute_api.flavor_ref_alt
        server = self.compute_provider.resize_and_confirm(
            testenv.server.id, new_flavor)

        assert server is not None, 'Server resize failed'

        assert server.status == "ACTIVE", (
            "Server did not enter ACTIVE status"
            " after resize.  Last observed status was {0}".format(
                server.status))

        resp = self.volumes_provider.wait_for_volume_status(
            testenv.volume.id, 'in-use', timeout=60)

        assert resp.ok, \
            ("Volume did not return to the 'in-use' status after"
             " the server it was attached to was rebooted")

        #Re-init ssh connection
        testenv.ssh_conn = self.setup_ssh_connection(
            server_ipv4_address=testenv.server.addresses.public.ipv4,
            server_user='root',
            server_user_password=testenv.server.adminPass)

        #Re-mount volume
        testenv.ssh_conn.mount_disk_device(
            testenv.device_name, testenv.mount_point, testenv.file_system_type)

        #Test write and read
        self.write_and_verify_data_on_mounted_volume(
            testenv.ssh_conn, testenv.mount_point)
