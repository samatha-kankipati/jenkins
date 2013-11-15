'''
@summary: Test Module for Dual Mode testing
@copyright: Copyright (c) 2013 Rackspace US, Inc.
@author: leon0944
'''
from ccengine.common.connectors.ping import PingClient
from ccengine.common.decorators import attr
from testrepo.common.testfixtures.networks import DualModeFixture


class TestDualMode(DualModeFixture):
    """Testing Dual Mode implementation"""

    @classmethod
    def setUpClass(cls):
        """Class setUp"""
        super(TestDualMode, cls).setUpClass()

        cls.ssh_msg = ('Failed remote ssh connection for {0} network from '
                       'server on the same network with Public: {1}. '
                       'Complete ssh results: {2}')

    @attr('dual_mode', 'positive')
    def test_server_ips(self):
        """Testing ips on servers"""

        network_names = ['public', 'private', 'isolated_A', 'isolated_B']
        network_list = [self.public_network, self.private_network,
                        self.isolated_network_A, self.isolated_network_B]
        ipv6_check_list = [True, False, False, False]

        # Verify server addresses with servers data
        results = self.helper.assert_server_data(server_list=self.servers,
            server_data=self.server_data, network_names=network_names,
            network_list=network_list, ipv6_check_list=ipv6_check_list)
        self.assert_server_data_results(results)

    @attr('dual_mode', 'positive')
    def test_server_ifconfig(self):
        """Testing ifconfig on servers"""

        for index, server in enumerate(self.servers):
            if self.server_data[index]['public']:
                self.helper.assert_ifconfig(server=server,
                    ips=self.server_data[index]['all_ips'])

    @attr('dual_mode', 'positive')
    def test_public_ping(self):
        """Testing ping on servers w public network"""

        msg_err = 'Public ping to IP address {0} - FAILED'
        msg_ok = 'Public ping to IP address {0} - OK'

        data_ips = self.get_data_ips()
        public_ip = data_ips['public_ip']
        result = []
        failure_flag = False
        for addr in public_ip:
            res = (PingClient.ping(ip=addr, ip_address_version_for_ssh=4)
                != 100)
            if res:
                result.append(msg_ok.format(addr))
            else:
                result.append(msg_err.format(addr))
                failure_flag = True
        msg = 'Got connectivity failures. Ping Results: {0}'
        self.assertFalse(failure_flag, msg.format(result))

    @attr('dual_mode', 'positive')
    def test_remote_public_ping(self):
        """Testing public network remote ping on servers"""
        self.verify_remote_ping(target_network='public')

    @attr('dual_mode', 'positive')
    def test_remote_private_ping(self):
        """Testing private network remote ping on servers"""
        self.verify_remote_ping(target_network='private')

    @attr('dual_mode', 'positive')
    def test_remote_isolated_A_ping(self):
        """Testing isolated network A remote ping on servers"""
        self.verify_remote_ping(target_network='isolated_A')

    @attr('dual_mode', 'positive')
    def test_remote_isolated_B_ping(self):
        """Testing isolated network B remote ping on servers"""
        self.verify_remote_ping(target_network='isolated_B')

    @attr('dual_mode', 'positive')
    def test_remote_public_ssh(self):
        """Testing Public remote ssh on servers"""
        target_network = 'public'
        res = self.verify_remote_ssh(target_network=target_network)
        self.assertSSH(res, target_network, self.ssh_msg)

    @attr('dual_mode', 'positive')
    def test_remote_private_ssh(self):
        """Testing ServiceNet remote ssh on servers"""
        target_network = 'private'
        res = self.verify_remote_ssh(target_network=target_network)
        self.assertSSH(res, target_network, self.ssh_msg)

    @attr('dual_mode', 'positive')
    def test_remote_isolated_A_ssh(self):
        """Testing isolated network A remote ssh on servers"""
        target_network = 'isolated_A'
        res = self.verify_remote_ssh(target_network=target_network)
        self.assertSSH(res, target_network, self.ssh_msg)

    @attr('dual_mode', 'positive')
    def test_remote_isolated_B_ssh(self):
        """Testing isolated network B remote ssh on servers"""
        target_network = 'isolated_B'
        res = self.verify_remote_ssh(target_network=target_network)
        self.assertSSH(res, target_network, self.ssh_msg)
