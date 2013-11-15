import json

from testrepo.common.testfixtures.fixtures import BaseParameterizedTestFixture
from testrepo.common.testfixtures.compute import ComputeFixture
from ccengine.domain.types import NovaServerStatusTypes
from ccengine.clients.managed_cloud.valkyrie_api import ValkyrieClient
from ccengine.common.tools.datagen import rand_name
from ccengine.common.decorators import attr
from ccengine.clients.maas.maas_client import MaasAPIClient


class ManagedLinuxNextGenServersTest(ComputeFixture,
                                     BaseParameterizedTestFixture):
    @classmethod
    def setUpClass(cls):
        super(ManagedLinuxNextGenServersTest, cls).setUpClass()
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

    def get_remote_client(self):
        remote_client = ""
        if (hasattr(self.created_server, 'accessIPv4')):
            remote_client = self.compute_provider.get_remote_instance_client(
                self.created_server, username="rack",
                password=self.valkyrieclient.get_rack_password_for_server(
                    self.server_id),
                ip_address=self.created_server.accessIPv4)
        else:
            remote_client = self.compute_provider.get_remote_instance_client(
                self.created_server,
                username="rack",
                password=self.valkyrieclient.get_rack_password_for_server(
                    self.server_id))
        return remote_client

    def test_managed_server_rebuild(self):
        self.compute_provider.wait_for_server_status(
            self.server_id,
            NovaServerStatusTypes.REBUILD,
            timeout=self.managed_cloud_timeout)

    def test_managed_server_active(self):
        self.compute_provider.wait_for_server_status(
            self.server_id,
            NovaServerStatusTypes.ACTIVE,
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

    def test_can_authenticate(self):
        remote_client = self.get_remote_client()
        self.assertTrue(remote_client.can_authenticate)

    def test_rackspace_monitoring_agent_file(self):
        remote_client = self.get_remote_client()
        status = remote_client.is_file_present(
            "/etc/rackspace-monitoring-agent.cfg")
        self.assertTrue(status,
                        msg="Monitoring config file not present")

    def test_rackspace_monitoring_agent_running(self):
        remote_client = self.get_remote_client()
        self.assertTrue("rackspace-monitoring-agent" in remote_client.
        remote_process_grep(
            "rackspace-monitoring-agent"),
                        msg="Monitoring Agent not running on the server")

    def test_mckick_complete(self):
        remote_client = self.get_remote_client()
        ssh_client = remote_client.ssh_client
        status = remote_client.is_file_present(
            "/var/log/mckick/mckick.log")
        self.assertTrue(status,
                        msg="MCKick log file is not present")

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
                self.assertEquals(
                    x['id'].lower(),
                    self.created_server.id.lower(),
                    msg='The monitoring agent id was {0}'.format(x['id']))
        self.assertTrue(agent_created,
                        msg='Matching Agent not found on Maas')

    def test_monitoring_agents_list(self):
        json_dict = json.loads(self.maas_client.get_agents_list().text)
        agent_connections_found = False
        for x in json_dict['values']:
            if self.created_server.id.lower() == x['id']:
                json_dict1 = json.loads(
                    self.maas_client.
                    get_agent_connections_list(self.created_server.id).text)
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

    def test_apache_open_port_80(self):
        remote_client = self.get_remote_client()
        ssh_client = remote_client.ssh_client
        status = ssh_client.exec_command(
            'sudo iptables-save | grep dport.80.*ACCEPT')
        self.assertTrue("tcp --dport 80" in status,
                        msg="apache port 80 not open")

    def test_apache_open_port_443(self):
        remote_client = self.get_remote_client()
        ssh_client = remote_client.ssh_client
        status = ssh_client.exec_command(
            'sudo iptables-save | grep dport.443.*ACCEPT')
        self.assertTrue("tcp --dport 443" in status,
                        msg="apache port 443 not open")

    def test_listen_port_80(self):
        remote_client = self.get_remote_client()
        ssh_client = remote_client.ssh_client
        status = ssh_client.exec_command('ss -ln | grep :80')
        self.assertIsNotNone(status)
        self.assertTrue(status, msg="port 80 not opened for tcp")

    def test_listen_port_443(self):
        remote_client = self.get_remote_client()
        ssh_client = remote_client.ssh_client
        status = ssh_client.exec_command('ss -ln | grep :443')
        self.assertIsNotNone(status)
        self.assertTrue(status, msg="port 443 not opened for tcp")

    def test_apache_http_200(self):
        remote_client = self.get_remote_client()
        ssh_client = remote_client.ssh_client
        status = ssh_client.exec_command(
            'curl -s -I http://localhost | head -1 | grep " 200 "')
        self.assertIsNotNone(status)
        self.assertTrue(status)
        self.assertTrue("200 OK" in status, msg="apache server not setup")

    def test_apache_http_404(self):
        remote_client = self.get_remote_client()
        ssh_client = remote_client.ssh_client
        status = ssh_client.exec_command(
            'curl -s -I http://localhost/test.txt | head -1 | grep " 404 "')
        self.assertIsNotNone(status)
        self.assertTrue(status)
        self.assertTrue("404 Not Found" in status,
                        msg="apache server not setup")

    def test_php_apc(self):
        remote_client = self.get_remote_client()
        ssh_client = remote_client.ssh_client
        status = ssh_client.exec_command('php -m | grep apc')
        self.assertIsNotNone(status)
        self.assertTrue(status, msg="PHP not setup")

    def test_fail2ban_firewall(self):
        remote_client = self.get_remote_client()
        ssh_client = remote_client.ssh_client
        status = ssh_client.exec_command('sudo iptables-save | grep fail2ban')
        self.assertIsNotNone(status)
        self.assertTrue(status, msg="fail2ban firewall not setup")

    def test_fail2ban_running(self):
        remote_client = self.get_remote_client()
        ssh_client = remote_client.ssh_client
        status = ssh_client.exec_command('ps auxw | grep fail2ban')
        self.assertTrue("/usr/bin/fail2ban-server" in status)
        self.assertIsNotNone(status)
        self.assertTrue(status, msg="fail2ban firewall not setup")

    def test_listen_port_3306(self):
        remote_client = self.get_remote_client()
        ssh_client = remote_client.ssh_client
        status = ssh_client.exec_command('ss -ln | grep :3306')
        self.assertIsNotNone(status)
        self.assertTrue(status, msg="port 3306 not open")

    def test_open_port_3306(self):
        remote_client = self.get_remote_client()
        ssh_client = remote_client.ssh_client
        status = ssh_client.exec_command(
            'sudo iptables-save | grep eth1.*3306')
        self.assertIsNotNone(status)
        self.assertTrue(status, msg="port 3306 not open")

    def test_show_processlist(self):
        remote_client = self.get_remote_client()
        ssh_client = remote_client.ssh_client
        status = ssh_client.exec_command(
            'sudo mysqladmin pr | grep "show processlist"')
        self.assertIsNotNone(status)
        self.assertTrue(status)
        self.assertTrue("show processlist" in status,
                        msg="process list error")

    def test_holland_bk(self):
        remote_client = self.get_remote_client()
        ssh_client = remote_client.ssh_client
        status = ssh_client.exec_command('sudo holland bk')
        self.assertIsNotNone(status)
        self.assertTrue("Acquired lock" in status,
                        msg="Error acquiring lock for holland_bk")
        self.assertTrue("Released lock" in status,
                        msg="Error releasing lock for holland_bk")

    def test_phpmyadmin(self):
        remote_client = self.get_remote_client()
        ssh_client = remote_client.ssh_client
        status = ssh_client.exec_command(
            'curl -s http://localhost/phpmyadmin/ | grep phpMyAdmin')
        self.assertIsNotNone(status)
        self.assertTrue(status)
        self.assertTrue("phpMyAdmin" in status,
                        msg="phpMyAdmin not setup")

    def test_localhost_in_hosts(self):
        remote_client = self.get_remote_client()
        ssh_client = remote_client.ssh_client
        status = ssh_client.exec_command('grep localhost /etc/hosts')
        self.assertIsNotNone(status)
        self.assertTrue(status)
        self.assertTrue("localhost" in status,
                        msg="No localhost entry in host file")

    def test_rhn_check(self):
        remote_client = self.get_remote_client()
        ssh_client = remote_client.ssh_client
        status = ssh_client.exec_command(
            'if [ -f /usr/sbin/rhn_check ]; then /usr/sbin/rhn_check; fi '
            '&& echo "Registration Successful" || echo "Failed Registration"')
        self.assertTrue("Registration Successful" in status,
                        msg="RHN registration failure")

    def test_root_statuspass(self):
        remote_client = self.get_remote_client()
        ssh_client = remote_client.ssh_client
        status = ssh_client.exec_command(
            'grep ^serverinfo.. /root/.statuspass')
        self.assertIsNotNone(status)
        self.assertTrue(status)
        self.assertTrue("serverinfo" in status,
                        msg="statuspass failure")

    def test_root_muninpass(self):
        remote_client = self.get_remote_client()
        ssh_client = remote_client.ssh_client
        status = ssh_client.exec_command(
            'sudo grep ^serverinfo.. /root/.muninpass')
        self.assertIsNotNone(status)
        self.assertTrue(status)
        self.assertTrue("serverinfo" in status,
                        msg="munin failure")

    def test_root_phpmyadminpass(self):
        remote_client = self.get_remote_client()
        ssh_client = remote_client.ssh_client
        status = ssh_client.exec_command(
            'sudo grep ^serverinfo.. /root/.phpmyadminpass')
        self.assertIsNotNone(status)
        self.assertTrue(status)
        self.assertTrue("serverinfo" in status,
                        msg="phpadminpass failure")

    def test_root_my_cnf(self):
        remote_client = self.get_remote_client()
        ssh_client = remote_client.ssh_client
        status = ssh_client.exec_command('sudo grep ^password=. /root/.my.cnf')
        self.assertIsNotNone(status)
        self.assertTrue(status)
        self.assertTrue("password" in status,
                        msg="password failure in config")

    def test_driveclient_installed(self):
        remote_client = self.get_remote_client()
        status = remote_client.is_file_present(
            "/etc/driveclient/cacert.pem")
        self.assertTrue(status,
                        msg="Driveclient not installed ")

    def test_driveclient_bootstrap(self):
        remote_client = self.get_remote_client()
        ssh_client = remote_client.ssh_client
        status = ssh_client.exec_command(
            'sudo tail -10 /var/log/driveclient.log;'
            ' grep AgentId /etc/driveclient/bootstrap.json')
        self.assertIsNotNone(status)
        self.assertTrue(status)
        self.assertTrue("AgentId" in status,
                        msg="Driveclient bootstrap issues")

    def test_driveclient_running(self):
        remote_client = self.get_remote_client()
        ssh_client = remote_client.ssh_client
        status = ssh_client.exec_command("pidof driveclient")
        self.assertIsNotNone(status)
        self.assertTrue(status,
                        msg="Driveclient not running")

    def test_munin_running(self):
        remote_client = self.get_remote_client()
        ssh_client = remote_client.ssh_client
        status = ssh_client.exec_command("sudo ps xo comm | grep munin")
        self.assertIsNotNone(status)
        self.assertTrue(status)
        self.assertTrue("munin" in status,
                        msg=" Munin not running")

    def test_swap_exists(self):
        remote_client = self.get_remote_client()
        ssh_client = remote_client.ssh_client
        status = ssh_client.exec_command('free -m | grep ^Swap')
        self.assertIsNotNone(status)
        self.assertTrue(status)
        self.assertTrue("Swap:" in status,
                        msg="Swap non existent")

    def test_rack_user_exists(self):
        remote_client = self.get_remote_client()
        ssh_client = remote_client.ssh_client
        status = ssh_client.exec_command('id rack')
        self.assertIsNotNone(status)
        self.assertTrue(status)
        self.assertTrue("uid" in status,
                        msg="rack user not setup")

    def test_monitoring_agent_running(self):
        remote_client = self.get_remote_client()
        ssh_client = remote_client.ssh_client
        status = ssh_client.exec_command("pidof rackspace-monitoring-agent")
        self.assertIsNotNone(status)
        self.assertTrue(status,
                        msg="monitoring agent not running")

    def test_monitoring_agent_configured(self):
        remote_client = self.get_remote_client()
        ssh_client = remote_client.ssh_client
        status = ssh_client.exec_command(
            "grep monitoring_id /etc/rackspace-monitoring-agent.cfg")
        self.assertIsNotNone(status)
        self.assertTrue(status)
        self.assertTrue("monitoring_id" in status,
                        msg="monitoring agent not configured")

    def test_create_server_image(self):
        remote_client = self.get_remote_client()
        servers_client = self.compute_provider.servers_client
        response = servers_client.create_image(
            server_id=self.created_server.id,
            name="Image.{0}".format(self.created_server.name))
        self.assertEqual(202, response.status_code)

    def test_create_lamp_server_image(self):
        servers_client = self.compute_provider.servers_client
        response = servers_client.create_image(
            server_id=self.created_server.id,
            name="Lamp.Image.{0}".format(self.created_server.name))
        self.assertEqual(202, response.status_code)

    def test_delete_server(self):
        self.deleted_server = self.servers_client.delete_server(
            server_id=self.created_server.id)
        self.assertEqual(204, self.deleted_server.status_code,
                         msg='The delete call \
                        response was: {0}'.format(
                             self.deleted_server.status_code))
