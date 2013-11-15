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


class ManagedLinuxFirstGenServersTest(ComputeFixture,
                                      BaseParameterizedTestFixture):

    @classmethod
    def setUpClass(cls):
        super(ManagedLinuxFirstGenServersTest, cls).setUpClass()
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
        cls.valkyrie_url = "{0}/cloud_account/{1}/locations/us/servers".format(
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
                    self.assertTrue(x['id'] is not None,
                                    msg='Maas entity is none')
                    self.assertTrue(x['agent_id'] is not None,
                                    msg='Maas entity is not mapped to agent')
                    self.assertEquals(
                        x['agent_id'].lower(),
                        str(self.created_server.name).lower(),
                        msg='The Maas entity id was {0}'.format(x['agent_id']))
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
                if str(self.created_server.name).lower() in x['id'].lower():
                    agent_created = True
                    self.assertTrue(x['id'] is not None,
                                    msg='Agent entity is not created yet')
                    self.assertEquals(
                        x['id'].lower(),
                        str(self.created_server.name).lower(),
                        msg='The monitoring agent id was {0}'.format(x['id']))
            sleep += 10
            time.sleep(10)
        self.assertTrue(agent_created,
                        msg='Matching Agent not found on Maas')

    def test_monitoring_agents_list(self):
        json_dict = json.loads(self.maas_client.get_agents_list().text)
        agent_connections_found = False
        for x in json_dict['values']:
            if str(self.created_server.name).lower() == x['id'].lower():
                json_dict1 = json.loads(
                    self.maas_client.
                    get_agent_connections_list(self.created_server.name).text)
                for x in json_dict1['values']:
                    self.assertTrue(x['id'] is not None,
                                    msg='Agent connection not created yet')
                    self.assertTrue(x['agent_id'].lower(), str(
                        self.created_server.name).lower())
                agent_connections_found = True
                self.assertTrue(len(json_dict1[
                    'values']) >= 1,
                    msg='No agent connections')
        self.assertTrue(agent_connections_found,
                        msg='Matching Agent connections not found')

    def test_delete_legacy_server(self):
        self.legacy_serv_client.delete_server(server_id=self.created_server.id)

    def test_backup_enabled(self):
        ip_address = self.created_server.accessIPv4
        agent_info = self.backupclient.get_backup_status(ip_address)
        self.assertIsNotNone(agent_info)
        self.assertEquals(str(agent_info['IsDisabled']), 'False',
                          msg="Backup is disabled by default")
        self.assertEquals(str(agent_info['CleanupAllowed']), 'True',
                          msg="Clean is disabled")
        self.assertEquals(str(agent_info['IsEncrypted']), 'False',
                          msg="Backup is encrypted")
        self.assertEquals(str(agent_info['UseServiceNet']), 'True',
                          msg="Not using ServiceNet")
        self.assertEquals(str(agent_info['UseFailoverUri']), 'False',
                          msg="FailoverURI is True")
        self.assertEquals(
            agent_info['Datacenter'], agent_info['BackupDatacenter'],
            msg="Server DC and Backup server not in the same location")
        self.assertEquals(str(agent_info['Flavor']), 'RaxCloudServer',
                          msg="Flavor has changed")

    def test_backup_config(self):
        server_name = self.created_server.name
        agent_config = self.backupclient_config.get_backup_config(server_name)
        self.assertIsNotNone(agent_config)
        included_folders = [
            '/var/lib/mysqlbackup',
            '/var/www',
            '/etc',
            '/home']
        self.assertIn(
            str(agent_config['Inclusions'][0]['FilePath']), included_folders,
            msg="Folder not included in backup")
        self.assertIn(
            str(agent_config['Inclusions'][1]['FilePath']), included_folders,
            msg="Folder not included in backup")
        self.assertIn(
            str(agent_config['Inclusions'][2]['FilePath']), included_folders,
            msg="Folder not included in backup")
        self.assertIn(
            str(agent_config['Inclusions'][3]['FilePath']), included_folders,
            msg="Folder not included in backup")
        self.assertIn(
            "Weekly" in str(agent_config['BackupConfigurationName']),
            msg="Weekly backup not configured")
        self.assertEquals(str(agent_config['VersionRetention']),
                          '30', msg='Backup retention not set')
        self.assertEquals(str(agent_config['Frequency']),
                          'Weekly', msg='Backup frequency not set')
        self.assertEquals(str(agent_config['NotifyFailure']),
                          'False', msg='Backup failure notification not set')
