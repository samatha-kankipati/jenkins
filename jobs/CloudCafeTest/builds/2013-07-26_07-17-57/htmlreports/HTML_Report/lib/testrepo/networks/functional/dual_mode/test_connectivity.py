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

    @attr('dual_mode', 'positive')
    def test_server_ips(self):
        """Testing ips on servers"""
        msg = ('Server {0} IP address {1} different than expected data '
               'IP address {2}')

        # Verify server addresses with servers data
        for index, server in enumerate(self.servers):
            if self.server_data[index]['public']:
                pub_ipv4 = self.helper.assert_server_ips(server,
                    self.public_network.label, version=4)
                self.assertEqual(self.server_data[index]['public_ip'],
                    pub_ipv4, msg.format(server.id, pub_ipv4,
                        self.server_data[index]['public_ip']))
                ipv6_msg = 'Missing Public IPv6 address in server {0}'
                pub_ipv6 = self.helper.assert_server_ips(server,
                    self.public_network.label, version=6)
                self.assertTrue(pub_ipv6, ipv6_msg.format(server.id))
            if self.server_data[index]['private']:
                pri_ipv4 = self.helper.assert_server_ips(server,
                    self.private_network.label, version=4)
                self.assertEqual(self.server_data[index]['private_ip'],
                    pri_ipv4, msg.format(server.id, pri_ipv4,
                        self.server_data[index]['private_ip']))
            if self.server_data[index]['isolated_A']:
                iso_A_ipv4 = self.helper.assert_server_ips(server,
                    self.isolated_network_A.label, version=4)
                self.assertEqual(self.server_data[index]['isolated_A_ip'],
                    iso_A_ipv4, msg.format(server.id, iso_A_ipv4,
                        self.server_data[index]['isolated_A_ip']))
            if self.server_data[index]['isolated_B']:
                iso_B_ipv4 = self.helper.assert_server_ips(server,
                    self.isolated_network_B.label, version=4)
                self.assertEqual(self.server_data[index]['isolated_B_ip'],
                    iso_B_ipv4, msg.format(server.id, iso_B_ipv4,
                        self.server_data[index]['isolated_B_ip']))

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

        msg = 'Can NOT ping public IP address {0}'
        for addr in self.public_ips:
            res = (PingClient.ping(ip=addr, ip_address_version_for_ssh=4)
                != 100)
            self.assertTrue(res, msg.format(addr))

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
