import json
import time

from testrepo.common.testfixtures.fixtures import BaseParameterizedTestFixture
from testrepo.common.testfixtures.compute import ComputeFixture
from ccengine.providers.legacyserv.server_api import ServerProvider
from ccengine.providers.auth.auth_api import AuthProvider
from ccengine.clients.legacyserv.server_api import LegacyServClient
from ccengine.clients.legacyserv.images_api import ImagesAPIClient
from ccengine.clients.managed_cloud.valkyrie_api import ValkyrieClient
from ccengine.domain.types import LegacyServerStatusTypes as ServStatus
from ccengine.common.decorators import attr
from ccengine.clients.maas.maas_client import MaasAPIClient
from ccengine.providers.configuration import MasterConfigProvider as _MCP


class ManagedWindowsFirstGenServersTest(ComputeFixture,
                                        BaseParameterizedTestFixture):
    @classmethod
    def setUpClass(cls):
        super(ManagedWindowsFirstGenServersTest, cls).setUpClass()
        config = _MCP()
        auth_provider = AuthProvider(config)
        legacy_url = config.legacyserv.url
        cls.customer_id = config.compute_api.tenant_id
        legacy_url = "{0}/{1}".format(legacy_url, cls.customer_id)
        auth_token = auth_provider.authenticate().token.id
        cls.legacy_serv_client = LegacyServClient(legacy_url, auth_token)
        cls.maas_url = "{0}/{1}".format(
            cls.config.managedcloud.maas_url, cls.customer_id)
        cls.maas_client = MaasAPIClient(
            cls.maas_url, cls.compute_provider.auth_token)
        cls.valkyrie_url = "{0}/{1}/locations/us/servers".format(
            cls.config.managedcloud.valkyrie_base_url, cls.customer_id)
        cls.valkyrieclient = ValkyrieClient(
            url=cls.valkyrie_url,
            auth_token=cls.config.managedcloud.valkyrie_auth_token)
        cls.managed_cloud_timeout = cls.config.managedcloud. \
            managed_cloud_timeout

    def setUp(self):
        self.created_server = self.legacy_serv_client.list_server_id(
            server_id=self.server_id).entity

    def test_legacy_server_active(self):
        timeout = self.managed_cloud_timeout
        sleep = 0
        while (self.created_server.status != "ACTIVE"):
            sleep += 60
            time.sleep(60)
            self.created_server = self.legacy_serv_client.list_server_id(
                server_id=self.server_id).entity
            if sleep > timeout:
                self.fail(msg='Legacy Server not active')

    def test_rack_account_password_from_valkyrie(self):
        password = self.valkyrieclient.get_rack_password_for_server(
            self.created_server.id)
        self.assertTrue(len(password) != 0)

    def test_monitoring_entity_is_registered(self):
        timeout = self.managed_cloud_timeout
        sleep = 0
        entity_created = False
        while (sleep < timeout and not entity_created):
            json_dict = json.loads(self.maas_client.get_entities_list().text)
            for x in json_dict['values']:
                if self.created_server.name.lower() in x['label'].lower():
                    entity_created = True
                    self.assertTrue(x[
                                        'id'] is not None,
                                    msg='Monitoring entity is none')
                    self.assertTrue(x[
                                        'agent_id'] is not None,
                                    msg='MaaS entity is not mapped to agent')
                    self.assertEquals(
                        x['agent_id'].lower(),
                        str(self.created_server.id),
                        msg='The monitoring entity id was {0}'.format(
                            x['agent_id']))
            sleep += 10
            time.sleep(10)
        self.assertTrue(entity_created, msg='Entity not found on Maas')

    def test_monitoring_agent_is_registered(self):
        json_dict = json.loads(self.maas_client.get_agents_list().text)
        agent_created = False
        timeout = self.managed_cloud_timeout
        sleep = 0
        while (sleep < timeout and not agent_created):
            for x in json_dict['values']:
                if str(self.created_server.id) in x['id'].lower():
                    agent_created = True
                    self.assertTrue(x['id'] is not None,
                                    msg='Agent entity is not created yet')
                    self.assertEquals(
                        x['id'].lower(),
                        str(self.created_server.id).lower(),
                        msg='The maas agent id was {0}'.format(x['id']))
        self.assertTrue(agent_created, msg='Matching Agent not found on Maas')

    def test_monitoring_agents_list(self):
        json_dict = json.loads(self.maas_client.get_agents_list().text)
        agent_connections_found = False
        for x in json_dict['values']:
            if str(self.created_server.id) == x['id']:
                json_dict1 = json.loads(
                    self.maas_client.
                    get_agent_connections_list(self.created_server.id).text)
                for x in json_dict1['values']:
                    self.assertTrue(x['id'] is not None,
                                    msg='Agent connection not created yet')
                    self.assertTrue(x['agent_id'].lower(), str(
                        self.created_server.id))
                agent_connections_found = True
                self.assertTrue(len(json_dict1[
                    'values']) >= 1, msg='No agent connections')
        self.assertTrue(agent_connections_found,
                        msg='Matching Agent connections not found')

    def test_delete_legacy_server(self):
        self.legacy_serv_client.delete_server(server_id=self.created_server.id)
