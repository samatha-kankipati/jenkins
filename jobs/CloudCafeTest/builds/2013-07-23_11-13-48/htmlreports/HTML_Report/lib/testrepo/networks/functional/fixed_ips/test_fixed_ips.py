'''
@summary: Test Module for add and remove fixed IPs
@copyright: Copyright (c) 2013 Rackspace US, Inc.
@author: leon0944
'''
from ccengine.common.decorators import attr
from testrepo.common.testfixtures.networks import AdminFixture
from ccengine.common.constants.networks_constants import HTTPResponseCodes
from ccengine.domain.types import NovaServerStatusTypes


class TestFixedIPs(AdminFixture):
    """
    Tests add and remove one public, one private and one isolated server IP
    Requires the IPy Python package and the following data in the config file,
    [admin]
    admin_auth_url=<auth_url>
    admin_username=<admin_username>
    admin_password=<admin_password>
    """

    @classmethod
    def setUpClass(cls):
        """Class setUp - creating the test server"""
        super(TestFixedIPs, cls).setUpClass()
        cls.admin_client = cls.admin_provider.client
        cls.servers_client = cls.servers_provider.servers_client
        cls.networks_client = cls.networks_provider.client
        if cls.run_nvp:
            cls.nvp_client = cls.nvp_provider.aic_client

        # Server is expected with Public, ServiceNet and Isolated networks
        server_create = cls.helper.create_list_servers(
            1, [cls.public_network.id, cls.private_network.id])
        cls.server_id = server_create.id
        cls.admin_pass = server_create.adminPass
        cls.net_list = server_create.net_list

        # For debugging a specific server, if used, above lines should be
        # commented out since the test server is replaced
        #cls.server_id = 'ed86a472-1f92-4342-91b9-3de5c4222f59'
        #cls.admin_pass = '<adminPass>'
        #cls.net_list = ['22addd69-45c8-4e8b-9d08-ba1131f45d08', \
        #                '00000000-0000-0000-0000-000000000000', \
        #                '11111111-1111-1111-1111-111111111111']

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

        cls.add_msg = ('Unable to add a {0} network fixed IP to server {1} '
                       'Response: {2} {3} {4}')
        cls.rem_msg = ('Unable to remove a {0} network fixed IP to server {1} '
                       'Response: {2} {3} {4}')

    @attr('admin')
    def test_add_remove_fixed_ip_public(self):
        """Testing adding and removing a public fixed IP"""

        # Get initial IPs and assert the expected counts for IPv4 and IPv6
        ips = self.helper.get_server_ips(self.server, self.public_network)
        self.helper.assert_ips(self.server, self.public_network,
                               self.ini_public_ips, 1)

        #Add an IP and assert the new counts for IPv4
        add_req = self.admin_client.add_fixed_ip(self.server.id,
                                                 self.public_network.id)
        msg = self.add_msg.format(self.public_network.label, self.server.id,
            add_req.status_code, add_req.reason, add_req.content)
        self.assertEqual(add_req.status_code,
                         HTTPResponseCodes.ADD_FIXED_IP, msg)

        self.helper.assert_ips(self.server, self.public_network,
                               self.ini_public_ips + 1, 1)
        ips2 = self.helper.get_server_ips(self.server, self.public_network)

        # Get the added IP address and check it is in the server via ssh
        added_ip = self.networks_provider.get_new_ip(ips, ips2)
        if self.ifconfig_order_check:
            order_list = ['eth0:1']
        else:
            order_list = None
        self.helper.assert_ifconfig(self.server, added_ip, find=True,
                                    order_list=order_list)

        # Check it is in NVP public switch port allowed address pairs
        if self.run_nvp:
            self.helper.check_nvp_public_allowed_address_pairs(self.server.id,
                added_ip, find=True)

        # Remove the added IP and assert the updated counts for IPv4
        rem_req = self.admin_client.remove_fixed_ip(self.server.id, added_ip)
        msg = self.rem_msg.format(self.public_network.label, self.server.id,
            rem_req.status_code, rem_req.reason, rem_req.content)
        self.assertEqual(rem_req.status_code,
                         HTTPResponseCodes.REMOVE_FIXED_IP, msg)

        self.helper.assert_ips(self.server, self.public_network,
                               self.ini_public_ips, 1)

        # Verify the removed ip is no longer in the server via ssh
        self.helper.assert_ifconfig(self.server, added_ip, find=False)

        # Check it is no longer in NVP
        if self.run_nvp:
            self.helper.check_nvp_public_allowed_address_pairs(self.server.id,
                added_ip, find=False)

    @attr('admin')
    def test_add_remove_fixed_ip_private(self):
        """Testing adding and removing a private fixed IP"""

        # Get initial IPs and assert the expected counts for IPv4 and IPv6
        ips = self.helper.get_server_ips(self.server, self.private_network)
        self.helper.assert_ips(self.server, self.private_network,
                               self.ini_private_ips)

        #Add an IP and assert the new counts for IPv4
        add_req = self.admin_client.add_fixed_ip(self.server.id,
                                                 self.private_network.id)
        msg = self.add_msg.format(self.private_network.label, self.server.id,
            add_req.status_code, add_req.reason, add_req.content)
        self.assertEqual(add_req.status_code,
                         HTTPResponseCodes.ADD_FIXED_IP, msg)

        self.helper.assert_ips(self.server, self.private_network,
                               self.ini_private_ips + 1)
        ips2 = self.helper.get_server_ips(self.server, self.private_network)

        # Get the added IP address and check it is in the server via ssh
        added_ip = self.networks_provider.get_new_ip(ips, ips2)
        if self.ifconfig_order_check:
            order_list = ['eth1:1']
        else:
            order_list = None
        self.helper.assert_ifconfig(self.server, added_ip, find=True,
                                    order_list=order_list)

        # Check it is in NVP private switch port allowed address pairs
        if self.run_nvp:
            self.helper.check_nvp_private_allowed_address_pairs(self.server.id,
                added_ip, find=True)

        # Remove the added IP and assert the updated counts for IPv4
        rem_req = self.admin_client.remove_fixed_ip(self.server.id, added_ip)
        msg = self.rem_msg.format(self.private_network.label, self.server.id,
            rem_req.status_code, rem_req.reason, rem_req.content)
        self.assertEqual(rem_req.status_code,
                         HTTPResponseCodes.REMOVE_FIXED_IP, msg)

        self.helper.assert_ips(self.server, self.private_network,
                               self.ini_private_ips)

        # Verify the removed ip is no longer in the server via ssh
        self.helper.assert_ifconfig(self.server, added_ip, find=False)

        # Check it is no longer in NVP
        if self.run_nvp:
            self.helper.check_nvp_private_allowed_address_pairs(self.server.id,
                added_ip, find=False)

    @attr('admin')
    def test_add_remove_fixed_ip_isolated(self):
        """Testing adding and removing an isolated fixed IP"""

        # Get initial IPs and assert the expected counts for IPv4 and IPv6
        ips = self.helper.get_server_ips(self.server, self.isolated_network)
        self.helper.assert_ips(self.server, self.isolated_network,
                               self.ini_isolated_ips)

        #Add an IP and assert the new counts for IPv4
        add_req = self.admin_client.add_fixed_ip(self.server.id,
                                                 self.isolated_network.id)
        msg = self.add_msg.format(self.isolated_network.label, self.server.id,
            add_req.status_code, add_req.reason, add_req.content)
        self.assertEqual(add_req.status_code,
                         HTTPResponseCodes.ADD_FIXED_IP, msg)

        self.helper.assert_ips(self.server, self.isolated_network,
                               self.ini_isolated_ips + 1)
        ips2 = self.helper.get_server_ips(self.server, self.isolated_network)

        # Get the added IP address and check it is in the server via ssh
        added_ip = self.networks_provider.get_new_ip(ips, ips2)
        if self.ifconfig_order_check:
            order_list = ['eth2:1']
        else:
            order_list = None
        self.helper.assert_ifconfig(self.server, added_ip, find=True,
                                    order_list=order_list)

        # Remove the added IP and assert the updated counts for IPv4
        rem_req = self.admin_client.remove_fixed_ip(self.server.id, added_ip)
        msg = self.rem_msg.format(self.isolated_network.label, self.server.id,
            rem_req.status_code, rem_req.reason, rem_req.content)
        self.assertEqual(rem_req.status_code,
                         HTTPResponseCodes.REMOVE_FIXED_IP, msg)

        self.helper.assert_ips(self.server, self.isolated_network,
                               self.ini_isolated_ips)

        # Verify the removed ip is no longer in the server via ssh
        self.helper.assert_ifconfig(self.server, added_ip, find=False)

        # Allowed address Pairs are NOT seen in NVP for isolated network
        # switch ports, as design for now
