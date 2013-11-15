'''
@summary: Test Module for Dual Mode testing
@copyright: Copyright (c) 2013 Rackspace US, Inc.
@author: leon0944
'''
from ccengine.common.connectors.ping import PingClient
from ccengine.common.decorators import attr
from testrepo.common.testfixtures.networks import DualModeFixture


class TestDualModeNegative(DualModeFixture):
    """
    Testing Dual Mode implementation: no network connectivity across servers
    on different networks
    """

    @classmethod
    def setUpClass(cls):
        """Class setUp"""
        super(TestDualModeNegative, cls).setUpClass()

        cls.ssh_msg = ('Unexpected remote ssh connection for {0} network from '
                       'server on diff network with Public: {1}. Complete ssh '
                       'results: {2}')

    @attr('dual_mode', 'negative')
    def test_remote_private_ping(self):
        """
        Testing there is no private connectivity from servers
        without private networks
        """
        self.verify_remote_ping(target_network='private', negative=True)

    @attr('dual_mode', 'negative')
    def test_remote_isolated_A_ping(self):
        """
        Testing there is no isolated A connectivity from servers
        without isolated A networks
        """
        self.verify_remote_ping(target_network='isolated_A', negative=True)

    @attr('dual_mode', 'negative')
    def test_remote_isolated_B_ping(self):
        """
        Testing there is no isolated B connectivity from servers
        without isolated B networks
        """
        self.verify_remote_ping(target_network='isolated_B', negative=True)

    @attr('dual_mode', 'negative')
    def test_remote_private_ssh(self):
        """Testing ServiceNet remote ssh on servers is unavailable"""
        target_network = 'private'
        res = self.verify_remote_ssh(target_network=target_network,
                                     negative=True)
        self.assertSSH(res, target_network, self.ssh_msg, negative=True)

    @attr('dual_mode', 'negative')
    def test_remote_isolated_A_ssh(self):
        """Testing isolated network A remote ssh on servers is unavailable"""
        target_network = 'isolated_A'
        res = self.verify_remote_ssh(target_network=target_network,
                                     negative=True)
        self.assertSSH(res, target_network, self.ssh_msg, negative=True)

    @attr('dual_mode', 'negative')
    def test_remote_isolated_B_ssh(self):
        """Testing isolated network B remote ssh on servers is unavailable"""
        target_network = 'isolated_B'
        res = self.verify_remote_ssh(target_network=target_network,
                                     negative=True)
        self.assertSSH(res, target_network, self.ssh_msg, negative=True)
