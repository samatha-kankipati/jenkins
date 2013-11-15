import json
from testrepo.common.testfixtures.compute import ComputeFixture
from ccengine.clients.legacyserv.server_api import LegacyServClient
from ccengine.common.decorators import attr
from ccengine.providers.auth.auth_api import AuthProvider
from ccengine.providers.configuration import MasterConfigProvider as _MCP


class CleanUpLegacyManagedServersTest(ComputeFixture):
    @classmethod
    def setUpClass(cls):
        super(CleanUpLegacyManagedServersTest, cls).setUpClass()
        config = _MCP()
        auth_provider = AuthProvider(config)
        legacy_url = config.legacyserv.url
        cls.customer_id = config.compute_api.tenant_id
        legacy_url = "{0}/{1}".format(legacy_url, cls.customer_id)
        auth_token = auth_provider.authenticate().token.id
        cls.legacy_serv_client = LegacyServClient(legacy_url, auth_token)

    def test_delete_all_server_on_account(self):
        list_servers_response = json.loads(
            self.legacy_serv_client.list_server().text)
        for x in list_servers_response['servers']:
            self.deleted_server = self.legacy_serv_client.delete_server(
                x['id'])
