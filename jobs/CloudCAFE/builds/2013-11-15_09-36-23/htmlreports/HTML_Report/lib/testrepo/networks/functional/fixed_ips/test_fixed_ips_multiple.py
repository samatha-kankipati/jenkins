'''
@summary: Test Module for add and remove fixed IPs
@copyright: Copyright (c) 2013 Rackspace US, Inc.
@author: leon0944
'''
from ccengine.common.decorators import attr
from testrepo.common.testfixtures.networks import AdminFixture
from ccengine.common.constants.networks_constants import HTTPResponseCodes
from ccengine.domain.types import NovaServerStatusTypes


class TestFixedIPsMultiple(AdminFixture):
    """
    Tests add and remove 10 public, 10 private and 10 isolated server IP
    Requires the IPy Python package and the following data in the config file,
    [admin]
    admin_auth_url=<auth_url>
    admin_username=<admin_username>
    admin_password=<admin_password>
    """

    @classmethod
    def setUpClass(cls):
        """Class setUp - creating the test server"""
        super(TestFixedIPsMultiple, cls).setUpClass()
        cls.admin_client = cls.admin_provider.client
        cls.servers_client = cls.servers_provider.servers_client
        cls.networks_client = cls.networks_provider.client

        # Server is expected with Public, ServiceNet and Isolated networks
        server_create = cls.helper.create_list_servers(2,
                               [cls.public_network.id, cls.private_network.id])
        cls.server_id = server_create.id
        cls.admin_pass = server_create.adminPass
        cls.net_list = server_create.net_list

        # For debugging a specific server, if used, above lines should be
        # commented out since the test server is replaced, for ex.
        #cls.server_id = '221613d8-86ed-408f-8150-0c5a8cb0c389'
        #cls.admin_pass = '<adminPass>'
        #cls.net_list = ([u'6b752ef8-58c7-4a11-b5db-6b08568d764c',
        #                u'00000000-0000-0000-0000-000000000000',
        #                u'11111111-1111-1111-1111-111111111111'])

        # Initial IPv4 counts, update as needed if using a specific server
        cls.ini_public_ips = 1
        cls.ini_private_ips = 1
        cls.ini_isolated_ips = 1

        # isolated networks expected first
        isolated_id = cls.net_list[0]
        nresp = cls.networks_client.get_network(isolated_id)
        msg = 'Unable to get isolated network: {0} {1} {2}'.format(
            nresp.status_code, nresp.reason, nresp.content)
        assert HTTPResponseCodes.GET_NETWORK == nresp.status_code, msg

        # IsolatedNetwork object to be used in tests, public_network and
        # private_network objects defined in fixture
        cls.isolated_network = nresp.entity

        # waiting for the server to be ACTIVE
        sresp = cls.servers_provider.wait_for_server_status(
            cls.server_id, NovaServerStatusTypes.ACTIVE)
        msg = 'Unable to get Active server: {0} {1} {2}'.format(
            sresp.status_code, sresp.reason, sresp.content)

        # server object to be used in tests with admin password
        cls.server = sresp.entity
        cls.server.adminPass = cls.admin_pass

    @attr('admin')
    def test_multiple_add_remove_fixed_ips_public(self):
        """Testing adding and removing 10 public fixed IPs"""

        if self.ifconfig_order_check:
            eth_prefix = 'eth0:{0}'
        else:
            eth_prefix = None
        self.add_remove_n_ips(n_ips=10, ini_ips=self.ini_public_ips,
                              network=self.public_network, ipv6=1,
                              eth_prefix=eth_prefix)

    @attr('admin')
    def test_add_remove_fixed_ip_private(self):
        """Testing adding and removing 10 private fixed IPs"""

        if self.ifconfig_order_check:
            eth_prefix = 'eth1:{0}'
        else:
            eth_prefix = None
        self.add_remove_n_ips(n_ips=10, ini_ips=self.ini_private_ips,
                              network=self.private_network,
                              eth_prefix=eth_prefix)

    @attr('admin')
    def test_add_remove_fixed_ip_isolated(self):
        """Testing adding and removing 10 isolated fixed IPs"""

        if self.ifconfig_order_check:
            eth_prefix = 'eth2:{0}'
        else:
            eth_prefix = None
        self.add_remove_n_ips(n_ips=10, ini_ips=self.ini_isolated_ips,
                              network=self.isolated_network,
                              eth_prefix=eth_prefix)

    def add_remove_n_ips(self, n_ips, ini_ips, network, ipv6=0,
                         eth_prefix=None):
        """
        @summary: add and remove multiple ips from a server and verify
        these actions take place as expected
        @param n_ips: number of ips to add and remove from the server
        @type: int
        @param ini_ips: number of initial ips on the server
        @type: int
        @param network: server network where the ips will be added and removed
        @type: IsolatedNetwork instance
        @param ipv6: expected count of network IPv6 addresses
        @type: int
        """
        # Get initial IPs and assert the expected counts for IPv4 and IPv6
        ips = self.helper.get_server_ips(self.server, network)
        self.helper.assert_ips(self.server, network, ini_ips, ipv6)

        ip_count = ini_ips
        added_ips = []
        for _ in range(n_ips):
            #Add an IP and assert the new counts for IPv4
            add_req = self.admin_client.add_fixed_ip(self.server.id,
                                                     network.id)
            msg = ('Unable to add a {0} network fixed IP to server {1} '
                'Response: {2} {3} {4}'.format(network.label, self.server.id,
                add_req.status_code, add_req.reason, add_req.content))
            self.assertEqual(add_req.status_code,
                             HTTPResponseCodes.ADD_FIXED_IP, msg)
            ip_count += 1
            self.helper.assert_ips(self.server, network, ip_count, ipv6)
            ips2 = self.helper.get_server_ips(self.server, network)

            # Get the added IP address and check it is in the server via ssh
            added_ip = self.networks_provider.get_new_ip(ips, ips2)
            ips.append(added_ip)

            # saving the added ips for removing
            added_ips.append(added_ip)

            # setting the expected eth for the added IP
            if eth_prefix:
                eth = eth_prefix.format(ip_count - 1)
            else:
                eth = None
            self.helper.assert_ifconfig(self.server, added_ip, find=True,
                                        order_list=eth)

        # Check NVP allowed address pairs
        if self.run_nvp:
            if network.label == 'public':
                self.helper.check_nvp_public_allowed_address_pairs(
                    self.server.id, added_ips, find=True)
            elif network.label == 'private':
                self.helper.check_nvp_private_allowed_address_pairs(
                    self.server.id, added_ips, find=True)
            else:
                pass

        for ip_to_remove in added_ips:
            # Remove the added IP and assert the updated counts for IPv4
            rem_req = self.admin_client.remove_fixed_ip(self.server.id,
                                                        ip_to_remove)
            msg = ('Unable to remove a {0} network fixed IP to server {1} '
                'Response: {2} {3} {4}'.format(network.label, self.server.id,
                rem_req.status_code, rem_req.reason, rem_req.content))
            self.assertEqual(rem_req.status_code,
                             HTTPResponseCodes.REMOVE_FIXED_IP, msg)
            ip_count -= 1
            self.helper.assert_ips(self.server, network, ip_count, ipv6)

            # Verify the removed ip is no longer in the server via ssh
            self.helper.assert_ifconfig(self.server, ip_to_remove, find=False)

        # Check NVP allowed address pairs
        if self.run_nvp:
            if network.label == 'public':
                self.helper.check_nvp_public_allowed_address_pairs(
                    self.server.id, added_ips, find=False)
            elif network.label == 'private':
                self.helper.check_nvp_private_allowed_address_pairs(
                    self.server.id, added_ips, find=False)
            else:
                pass
