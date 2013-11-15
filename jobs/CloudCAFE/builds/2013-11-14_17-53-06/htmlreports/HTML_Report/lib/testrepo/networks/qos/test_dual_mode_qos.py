'''
@summary: This test class creates VM's of every flavor and confirms they are
          getting the correct public and private networks QoS (Quality of
          service)
@copyright: Copyright (c) 2013 Rackspace US, Inc.
@author: migu6046
'''


import re

from ccengine.common.connectors.ssh import SSHConnector
from ccengine.common.decorators import attr
from ccengine.common.tools.datagen import rand_name
from ccengine.providers.hypervisor.hypervisor_api import HypervisorAPIProvider
from testrepo.common.testfixtures.networks import AdminFixture


class TestVMSetUpDualMode(AdminFixture):

    @classmethod
    def setUpClass(cls):
        super(TestVMSetUpDualMode, cls).setUpClass()
        flavors_client = cls.servers_provider.flavors_client
        cls.flavors = flavors_client.list_flavors_with_detail().entity

        # Create an iperf 'server' server. This server will receive the
        # transmissions of the serveres whose rates will be measured
        network_ids = ([cls.public_network.id, cls.private_network.id])
        networks_dict = cls.networks_provider.get_server_network_dd(
            network_ids)
        ptr = int(len(cls.flavors) / 2)
        flavor_name = cls.flavors[ptr].name
        server_name = rand_name(
            'qos-dual-mode-{0}-server-'.format(flavor_name))
        cls.server_server = cls.servers_provider.create_active_server(
            name=server_name, networks=networks_dict,
            flavor_ref=cls.flavors[ptr].id).entity
        cls.servers_to_delete.append(cls.server_server.id)
        cls.server_public_ip, cls.server_private_ip = cls._get_server_ips(
            cls.server_server)
        cls.fixture_log.debug('Server VM name: {0}'.format(server_name))
        cls.fixture_log.debug('Server VM id: {0}'.format(cls.server_server.id))
        cls.fixture_log.debug(
            'Server root password: {0}'.format(cls.server_server.adminPass))
        cls.fixture_log.debug(
            'Server public ip: {0}'.format(cls.server_public_ip))
        cls.fixture_log.debug(
            'Server private ip: {0}'.format(cls.server_private_ip))

        # Setup iperf in the server just created. Start iperf as a server in
        # daemon mode, to listen to other servers transmissions
        server_ssh = SSHConnector(cls.server_public_ip, 'root',
                                  cls.server_server.adminPass)
        server_ssh.start_shell()
        ssh_output, _ = server_ssh.exec_shell_command_wait_for_prompt(
            'apt-get install iperf')
        server_ssh.exec_shell_command('iperf -s -p 9000 -D', True)

    @classmethod
    def _get_server_ips(cls, server):
        public_ip = None
        private_ip = None
        for addr in server.addresses.public.addresses:
            if addr.version == 4:
                public_ip = addr.addr
                break
        for addr in server.addresses.private.addresses:
            if addr.version == 4:
                private_ip = addr.addr
                break
        return public_ip, private_ip

    @classmethod
    def _log_ssh_output(cls, action, output):
        lines = output.split('\n')
        cls.fixture_log.debug(
            'Output from ssh session after: {0}'.format(action))
        for n in xrange(len(lines)):
            cls.fixture_log.debug(lines[n])

    def _get_ip_rate(self, ssh_session, ip_address):
        output, _ = ssh_session.exec_shell_command_wait_for_prompt(
            'iperf -c {0} -p 9000 -t 30 -P 10'.format(ip_address))
        last_line = output.splitlines()[-1]
        return float(re.findall(r'(\d+.?\d*) Mbits/sec', last_line)[0])

    def _is_within_range(self, expected, actual, percent_max_error):
        max_error = expected * percent_max_error
        return abs(expected - actual) <= max_error

    @attr('smoke', 'positive')
    def test_public_private_qos(self):
        """Tests that VM's of every flavor achieve the tranmission rates
        defined in the rxtx_factor field of the corresponding flavor
        definition"""
        for flavor in self.flavors:
            # Create an iperf client server. This is the server whose
            # transmission rates are being measured. Public and private
            # networks rates are measured
            network_ids = ([self.public_network.id, self.private_network.id])
            networks_dict = self.networks_provider.get_server_network_dd(
                network_ids)
            server_name = rand_name(
                'qos-dual-mode-{0}-client-'.format(flavor.name))
            server_client = self.servers_provider.create_active_server(
                name=server_name, networks=networks_dict,
                flavor_ref=flavor.id).entity
            self.servers_to_delete.append(server_client.id)

            compute_ip = self.admin_provider.get_compute_node_ip_for_server(
                server_client.id)
            self.fixture_log.debug('Client VM hypervisor IP: {0}'.format(
                compute_ip))
            hypervisor_provider = HypervisorAPIProvider(
                compute_ip, self.config, self.fixture_log)
            vifs_flows = hypervisor_provider.get_vifs_flows(server_client.id)
            self.fixture_log.debug('Client VM flows: {0}'.format(vifs_flows))
            vifs_details = hypervisor_provider.get_vifs_network_details(
                server_client.id)
            phys_devs = [vif['phys_dev'] for vif in vifs_details.values()
                         if vif.get('phys_dev') is not None]
            self.fixture_log.debug(
                'Client VM VIFs physical devices: {0}'.format(phys_devs))
            for phys_dev in phys_devs:
                qdiscs = hypervisor_provider.get_tc_qdisc(phys_dev)
                classes = hypervisor_provider.get_tc_class(phys_dev)
                filters = hypervisor_provider.get_tc_filter(phys_dev)
                self.fixture_log.debug(
                    'Client VM hypervisor phys dev {0} qdiscs: {1}'.format(
                        phys_dev, qdiscs))
                self.fixture_log.debug(
                    'Client VM hypervisor phys dev {0} classes: {1}'.format(
                        phys_dev, classes))
                self.fixture_log.debug(
                    'Client VM hypervisor phys dev {0} filters: {1}'.format(
                        phys_dev, filters))

            public_ip, private_ip = self._get_server_ips(server_client)
            self.fixture_log.debug('Client VM name: {0}'.format(server_name))
            self.fixture_log.debug(
                'Client VM id: {0}'.format(server_client.id))
            self.fixture_log.debug(
                'Client root password: {0}'.format(server_client.adminPass))
            self.fixture_log.debug('Client public ip: {0}'.format(public_ip))
            self.fixture_log.debug('Client private ip: {0}'.format(private_ip))
            client_ssh = SSHConnector(public_ip, 'root',
                                      server_client.adminPass)
            client_ssh.start_shell()
            client_ssh.exec_shell_command_wait_for_prompt(
                'apt-get install iperf')
            ip_rate = self._get_ip_rate(client_ssh, self.server_public_ip)
            self.fixture_log.debug(
                'Public ip rate: {0} Mbits/sec'.format(ip_rate))
            self.assertTrue(self._is_within_range(flavor.rxtx_factor, ip_rate,
                                                  0.15))
            ip_rate = self._get_ip_rate(client_ssh, self.server_private_ip)
            self.fixture_log.debug(
                'Private ip rate: {0} Mbits/sec'.format(ip_rate))
            self.assertTrue(self._is_within_range(flavor.rxtx_factor, ip_rate,
                                                  0.15))
