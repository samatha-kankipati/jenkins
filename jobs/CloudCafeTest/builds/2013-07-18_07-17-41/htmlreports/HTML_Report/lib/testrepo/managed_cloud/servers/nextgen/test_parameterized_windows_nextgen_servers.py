import json

from testrepo.common.testfixtures.fixtures import BaseParameterizedTestFixture
from testrepo.common.testfixtures.compute import ComputeFixture
from ccengine.domain.types import NovaServerStatusTypes
from ccengine.clients.managed_cloud.valkyrie_api import ValkyrieClient
from ccengine.common.tools.datagen import rand_name
from ccengine.common.decorators import attr
from ccengine.clients.maas.maas_client import MaasAPIClient


class ManagedWindowsNextGenServersTest(ComputeFixture,
                                       BaseParameterizedTestFixture):
    @classmethod
    def setUpClass(cls):
        super(ManagedWindowsNextGenServersTest, cls).setUpClass()
        cls.customer_id = cls.config.compute_api.tenant_id
        cls.maas_url = "{0}/{1}".format(cls.config.managedcloud.maas_url,
                                        cls.customer_id)
        cls.valkyrie_url = "{0}/{1}/locations/us/servers".format(
            cls.config.managedcloud.valkyrie_base_url, cls.customer_id)
        cls.maas_client = MaasAPIClient(
            cls.maas_url,
            cls.compute_provider.auth_token)
        cls.valkyrieclient = ValkyrieClient(
            url=cls.valkyrie_url,
            auth_token=cls.config.managedcloud.valkyrie_auth_token)
        cls.managed_cloud_timeout = cls.config.managedcloud. \
            managed_cloud_timeout


    def setUp(self):
        self.created_server = self.compute_provider.servers_client.get_server(
            server_id=self.server_id).entity

    def test_managed_server_active(self):
        server_response = self.compute_provider.wait_for_server_status(
            self.server_id,
            NovaServerStatusTypes.ACTIVE,
            timeout=self.managed_cloud_timeout)

    def test_managed_server_rebuild(self):
        self.compute_provider.wait_for_server_status(
            self.server_id,
            NovaServerStatusTypes.REBUILD,
            timeout=self.managed_cloud_timeout)

    def test_managed_automation_process_started(self):
        self.compute_provider.wait_for_server_metadata(
            self.server_id, "rax_service_level_automation",
            timeout=self.managed_cloud_timeout)

    def test_managed_automation_complete(self):
        metadata_response = self.compute_provider. \
            wait_for_server_metadata_status(
            self.server_id, "rax_service_level_automation", "Complete",
            timeout=self.managed_cloud_timeout)
        metadata = metadata_response.entity
        self.assertEquals("Complete", metadata.rax_service_level_automation)

    def test_rack_account_password_from_valkyrie(self):
        password = self.valkyrieclient.get_rack_password_for_server(
            self.created_server.id)
        self.assertTrue(len(password) != 0,
                        msg="Managed cloud password not in valkyrie")

    def test_monitoring_entity_is_registered(self):
        json_dict = json.loads(self.maas_client.get_entities_list().text)
        entity_created = False
        for x in json_dict['values']:
            if self.created_server.name.lower() in x['label'].lower():
                entity_created = True
                self.assertTrue(x['id'] is not None,
                                msg='Monitoring entity is none')
                self.assertTrue(x['agent_id'] is not None,
                                msg='Monitoring entity is not mapped to agent')
                self.assertEquals(
                    x['agent_id'].lower(),
                    self.created_server.id.lower(),
                    msg='The monitoring entity id was {0}'.format(
                        x['agent_id']))
        self.assertTrue(entity_created, msg='Entity not found on Maas')

    def test_monitoring_agent_is_registered(self):
        json_dict = json.loads(self.maas_client.get_agents_list().text)
        agent_created = False
        for x in json_dict['values']:
            if self.created_server.id.lower() in x['id'].lower():
                agent_created = True
                self.assertTrue(x['id'] is not None,
                                msg='Agent entity is not created yet')
                self.assertEquals(x['id'].lower(),
                                  self.created_server.id.lower(),
                                  msg='The monitoring agent '
                                      'id was {0}'.format(x['id']))
        self.assertTrue(agent_created, msg='Matching Agent not found on Maas')

    def test_monitoring_agents_list(self):
        json_dict = json.loads(self.maas_client.get_agents_list().text)
        agent_connections_found = False
        for x in json_dict['values']:
            if self.created_server.id.lower() == x['id']:
                json_dict1 = json.loads(
                    self.maas_client.get_agent_connections_list
                        (self.created_server.id).text)
                for x in json_dict1['values']:
                    self.assertTrue(x['id'] is not None,
                                    msg='Agent connection not created yet')
                    self.assertTrue(x['agent_id'].lower(),
                                    self.created_server.id.lower())
                agent_connections_found = True
                self.assertTrue(len(json_dict1[
                    'values']) >= 1,
                                msg='No agent connections')
        self.assertTrue(agent_connections_found,
                        msg='Matching Agent connections not found')

    def test_create_server_image(self):
        servers_client = self.compute_provider.servers_client
        response = servers_client.create_image(
            server_id=self.created_server.id,
            name="Image.{0}".format(self.created_server.name))
        self.assertEqual(202, response.status_code)

    def test_delete_server(self):
        self.deleted_server = self.servers_client.delete_server(
            server_id=self.created_server.id)
        self.assertEqual(204, self.deleted_server.status_code,
                         msg='The delete call \
                         response was: {0}'.format(
                             self.deleted_server.status_code))
