'''
@summary: Test Module for new networks tests, eventually tests at
          test_networks will be moved here once in RAXRoast
@copyright: Copyright (c) 2013 Rackspace US, Inc.
@author: leon0944
'''
import re
from IPy import IP
from ccengine.common.decorators import attr
from testrepo.common.testfixtures.networks import BaseNetworksFixture
from ccengine.common.constants.networks_constants import HTTPResponseCodes
from ccengine.domain.types import NovaServerStatusTypes


class TestNetworkIPs(BaseNetworksFixture):
    """Test Networks functionality"""

    @classmethod
    def setUpClass(cls):
        """Class setUp - creating the test network and server"""
        super(TestNetworkIPs, cls).setUpClass()

        # IPv4 test networks create
        cls.isolated_network = cls.networks_provider.create_ipv4_network()
        cls.networks_to_delete.append(cls.isolated_network.id)
        network_ids = ([cls.public_network.id, cls.private_network.id,
                        cls.isolated_network.id])
        networks_dict = cls.networks_provider.get_server_network_dd(
            network_ids)

        cls.server = cls.servers_provider.create_active_server(
            networks=networks_dict).entity
        cls.servers_to_delete.append(cls.server.id)

    @attr('smoke', 'positive', 'bug_fix')
    def test_server_ips(self):
        """
        Redmine Task 849 (bug 530)
        Verifying Melange does NOT hands out broadcast addresses to servers
        (IPv4 addresses ending in .255)
        """
        # Get and verify server addresses
        pub_ipv4 = self.helper.assert_server_ips(self.server,
            self.public_network.label, version=4)
        pub_ipv6 = self.helper.assert_server_ips(self.server,
            self.public_network.label, version=6)
        pri_ipv4 = self.helper.assert_server_ips(self.server,
            self.private_network.label, version=4)
        iso_ipv4 = self.helper.assert_server_ips(self.server,
            self.isolated_network.label, version=4)

        # Verify the IPv4 addresses do NOT end with .255
        for ip, label in [(pub_ipv4, self.public_network.label),
                          (pri_ipv4, self.private_network.label),
                          (iso_ipv4, self.isolated_network.label)]:
            result = re.split('\.', ip)
            msg = ('Unexpected {0} IPv4 {1} address ending with 255 at Server '
                   '{2}. Melange should NOT hand out broadcast addresses')
            self.assertNotEqual(result[-1], '255', msg.format(
                                label, ip, self.server.id))
