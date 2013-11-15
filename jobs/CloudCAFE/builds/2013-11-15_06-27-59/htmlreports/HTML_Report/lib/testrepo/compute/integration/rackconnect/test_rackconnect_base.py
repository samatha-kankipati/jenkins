from testrepo.common.testfixtures.compute import RackconnectIntegrationFixture
from ccengine.common.decorators import attr
from ccengine.domain.types import NovaRackConnectAutomationStatusTypes
from ccengine.common.tools.datagen import rand_name


class CreateRackconnectServerTest(RackconnectIntegrationFixture):

    @classmethod
    def setUpClass(cls):
        super(CreateRackconnectServerTest, cls).setUpClass()
        # Creation of 1 servers needed for the tests
        active_server_response = cls.compute_provider.create_active_server()
        cls.server = active_server_response.entity
        cls.resources.add(cls.server.id,
                          cls.servers_client.delete_server)
        cls.positive_codes = [200, 201, 202]
    
    @attr(type='smoke', net='no')
    def test_core_account_is_rack_connect(self):
        '''Verify RackConnect core account configurations'''
        acc_configs = self.rcc_provider.rackcore_client.get_core_account_configurations(
            account_number=self.config.rackconnect.account_number)
        self.assertIn(acc_configs.status_code, self.positive_codes,
                        msg="Configurations are present")

    @attr(type='smoke', net='no')
    def test_server_is_rack_connect(self):
        '''Verify Server has Rack Connect automation statuses'''
        tnn_configs = self.rcc_provider.rackcore_client.get_tenant_automation_status(
            account_number=self.config.rackconnect.account_number,
            tenant_id=self.config.compute_api.tenant_id)
        self.assertIn(tnn_configs.status_code, self.positive_codes,
                        msg="Configurations are present")
        flag_found = False
        for item in tnn_configs.entity:
            if item.api_server_id == self.server.id:
                flag_found = True
        self.assertTrue(flag_found, msg="Server wasn't found in the list")
    
    @attr(type='smoke', net='no')
    def test_server_finished_rackconnect_deployment(self):
        '''Verify Rack Connect Server is deployed'''
        self.rcc_provider.wait_for_rackconnect_deployed_status(
            account_number=self.config.rackconnect.account_number,
            tenant_id=self.config.compute_api.tenant_id,
            server_id=self.server.id,
            status_to_wait_for=NovaRackConnectAutomationStatusTypes.ACTIVE)
