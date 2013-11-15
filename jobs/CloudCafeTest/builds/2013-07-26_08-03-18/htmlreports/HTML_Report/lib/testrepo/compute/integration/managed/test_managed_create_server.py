from testrepo.common.testfixtures.compute import ComputeFixture
from ccengine.common.decorators import attr
from ccengine.domain.types import NovaManagedMetaStatusTypes
from ccengine.common.tools.datagen import rand_name
from ccengine.domain.types import NovaServerStatusTypes


class CreateManagedServerTest(ComputeFixture):

    @classmethod
    def setUpClass(cls):
        super(CreateManagedServerTest, cls).setUpClass()
        # Creation of 1 servers needed for the tests
        active_server_response = cls.compute_provider.create_active_server()
        cls.server = active_server_response.entity

    @classmethod
    def tearDownClass(cls):
        super(CreateManagedServerTest, cls).tearDownClass()

    @attr(type='smoke', net='no')
    def test_created_server_is_managed(self):
        '''Verify Managed server process is completed'''
        self.compute_provider.wait_for_managed_status(server=self.server,
            status_to_wait_for=NovaManagedMetaStatusTypes.ACTIVE)

    @attr(type='smoke', net='no')
    def test_created_server_only_managed_admin_account_on_server(self):
        '''Verify Managed server account automation is set up on server'''
        metadata = {'build_config': 'core'}
        active_server_response = self.compute_provider.create_active_server(
            metadata=metadata)
        server = active_server_response.entity
        self.compute_provider.wait_for_managed_status(server=server,
            status_to_wait_for=NovaManagedMetaStatusTypes.ACTIVE)
