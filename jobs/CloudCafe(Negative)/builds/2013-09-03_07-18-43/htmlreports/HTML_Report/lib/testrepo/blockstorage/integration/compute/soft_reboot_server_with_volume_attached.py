from ccengine.common.decorators import attr
from testrepo.common.testfixtures.blockstorage.compute_integration import \
    BlockStorageLinuxIntegrationFixture


class SoftRebootServerWithVolumeAttached(BlockStorageLinuxIntegrationFixture):
    """Verifies correct volume behavior for server reboot scenarios where a
    volume is attached
    """

    @attr('smoke')
    def test_soft_server_reboot_with_volume_attached(self):
        testenv = self.setup_server_with_volume_attached()

        #Reboot server with volume attached
        server = self.compute_provider.reboot_and_await(
            testenv.server.id, 'SOFT')
        assert server is not None, 'Server reboot failed'

        #Assert volume is in-use after reboot (attached)
        resp = self.volumes_provider.wait_for_volume_status(
            testenv.volume.id, 'in-use', timeout=60)

        assert resp.ok, \
            ("Volume did not return to the 'in-use' status after"
             " the server it was attached to was soft-rebooted")

    @attr('smoke')
    def test_volume_write_after_soft_server_reboot(self):
        pass
