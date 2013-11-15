'''
@summary: Test Module for Dual Mode testing
@copyright: Copyright (c) 2013 Rackspace US, Inc.
@author: leon0944
'''
from ccengine.common.connectors.ping import PingClient
from ccengine.common.decorators import attr
from testrepo.common.testfixtures.networks import DualModeFixture


class TestDualModeLimits(DualModeFixture):
    """Testing Dual Mode ping with 100 packets and 64 network limits"""

    @attr('dual_mode', 'positive')
    def test_public_ping_100(self):
        """Testing public ping with 100 packages"""

        msg = ('Unexpected {0}% packet loss for public IP address {1}. '
               'Expected at most {2}% packet loss')
        for addr in self.public_ips:
            res = PingClient.ping(ip=addr, ip_address_version_for_ssh=4,
                                  count=100)
            diff = (res <= self.accepted_packet_loss_pct)
            self.assertTrue(diff, msg.format(res, addr,
                                             self.accepted_packet_loss_pct))

    @attr('dual_mode', 'positive')
    def test_remote_public_ping_100(self):
        """Testing public network remote ping on servers with 100 packets"""
        self.verify_remote_ping(target_network='public', count=100,
            accepted_packet_loss_pct=self.accepted_packet_loss_pct)

    @attr('dual_mode', 'positive')
    def test_remote_private_ping_100(self):
        """Testing private network remote ping on servers with 100 packets"""
        self.verify_remote_ping(target_network='private', count=100,
            accepted_packet_loss_pct=self.accepted_packet_loss_pct)

    @attr('dual_mode', 'positive')
    def test_remote_isolated_A_ping_100(self):
        """
        Testing isolated network A remote ping on servers with 100 packets
        """
        self.verify_remote_ping(target_network='isolated_A', count=100,
            accepted_packet_loss_pct=self.accepted_packet_loss_pct)

    @attr('dual_mode', 'positive')
    def test_remote_isolated_B_ping_100(self):
        """
        Testing isolated network A remote ping on servers with 100 packets
        """
        self.verify_remote_ping(target_network='isolated_B', count=100,
            accepted_packet_loss_pct=self.accepted_packet_loss_pct)
