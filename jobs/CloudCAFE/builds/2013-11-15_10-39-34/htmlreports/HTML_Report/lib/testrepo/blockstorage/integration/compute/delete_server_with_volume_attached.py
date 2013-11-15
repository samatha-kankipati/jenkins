from ccengine.common.decorators import attr
from testrepo.common.testfixtures.blockstorage.compute_integration import \
    BlockStorageLinuxIntegrationFixture


class DeleteServerWithVolumeAttached(BlockStorageLinuxIntegrationFixture):
    """Verifies correct volume behavior for server delete scenarios where a
    volume is attached
    """

    @attr('smoke')
    def test_delete_server_with_volume_attached(self):
        testenv = self.setup_server_with_volume_attached()

        #Delete server with volume attached
        resp = self.compute_provider.servers_client.delete_server(
            testenv.server.id)
        assert resp.ok, "Server delete failed with {0}, expected 204".format(
            resp.status_code)

        resp = self.volumes_provider.wait_for_volume_status(
            testenv.volume.id, 'available', timeout=60)

        assert resp.ok, \
            ("Volume did not return to the 'available' status after"
             " the server it was attached to was deleted")
