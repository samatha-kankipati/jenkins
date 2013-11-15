from testrepo.common.testfixtures.compute import ComputeFixture
from ccengine.common.decorators import attr
from ccengine.domain.types import NovaManagedMetaStatusTypes
from ccengine.common.tools.datagen import rand_name
from ccengine.domain.types import NovaServerStatusTypes


class RebuildManagedServerTest(ComputeFixture):

    @classmethod
    def setUpClass(cls):
        super(RebuildManagedServerTest, cls).setUpClass()
        # Creation of 1 servers needed for the tests
        active_server_response = cls.compute_provider.create_active_server()
        cls.server = active_server_response.entity

    @classmethod
    def tearDownClass(cls):
        super(RebuildManagedServerTest, cls).tearDownClass()

    @attr(type='smoke', net='no')
    def test_rebuild_server_is_managed(self):
        '''Verify Managed server process is completed on '''
        rebuilt_server_response = self.servers_client.rebuild(
            self.server.id,
            self.image_ref_alt)
        self._verify_managed_server(server_id=self.server.id)
    
    @attr(type='smoke', net='no')
    def test_rebuild_server_only_managed_admin_account_on_server(self):
        """Verify Managed admin account server process is completed after rebuild """
        metadata = {'build_config': 'core'}
        active_server_response = self.compute_provider.create_active_server(
            metadata=metadata)
        rebuild_server_response = self.servers_client.rebuild(
            server_id=active_server_response.entity.id,
            image_ref=self.image_ref_alt,
            metadata=metadata)
        self._verify_managed_server(server_id=active_server_response.entity.id)
    
    def _verify_managed_server(self, server_id):
        self.rebuilt_server_response = self.compute_provider.wait_for_server_status(
            server_id,
            NovaServerStatusTypes.ACTIVE)
        self.compute_provider.wait_for_server_metadata(
            server_id=server_id,
            metadata_to_wait_for='rax_service_level_automation')
        self.compute_provider.wait_for_server_metadata_status(
            server_id=server_id,
            metadata_key='rax_service_level_automation',
            metadata_value=NovaManagedMetaStatusTypes.ACTIVE)
