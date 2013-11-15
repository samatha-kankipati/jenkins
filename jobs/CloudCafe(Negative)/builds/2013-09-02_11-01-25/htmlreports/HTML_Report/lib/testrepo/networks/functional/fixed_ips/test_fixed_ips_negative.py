'''
@summary: Test Module for add and remove fixed IPs
@copyright: Copyright (c) 2013 Rackspace US, Inc.
@author: leon0944
'''
from ccengine.common.decorators import attr
from testrepo.common.testfixtures.networks import AdminFixture
from ccengine.common.constants.networks_constants import HTTPResponseCodes
from ccengine.domain.types import NovaServerStatusTypes


class TestFixedIPsNegative(AdminFixture):
    """
    Tests try to remove all public, private and isolated server IPs and
    should NOT be able to do so, the last IP of each network shall remain
    Requires the IPy Python package and the following data in the config file,
    [admin]
    admin_auth_url=<auth_url>
    admin_username=<admin_username>
    admin_password=<admin_password>
    """

    @classmethod
    def setUpClass(cls):
        """Class setUp - creating the test server"""
        super(TestFixedIPsNegative, cls).setUpClass()
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
        #cls.server_id = 'ed86a472-1f92-4342-91b9-3de5c4222f59'
        #cls.admin_pass = '<adminPass>'
        #cls.net_list = ([u'22addd69-45c8-4e8b-9d08-ba1131f45d08',
        #                u'84336296-8cbc-427f-a55e-41ba0516effb',
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
    def test_remove_all_fixed_ips_public(self):
        """Testing removing all public fixed IPs"""

        self.helper.remove_all_ips(self.server, self.public_network,
                                   self.admin_client)

    @attr('admin')
    def test_remove_all_fixed_ip_private(self):
        """Testing removing all private fixed IPs"""

        self.helper.remove_all_ips(self.server, self.private_network,
                                   self.admin_client)

    @attr('admin')
    def test_add_remove_fixed_ip_isolated(self):
        """Testing removing all isolated fixed IPs"""

        self.helper.remove_all_ips(self.server, self.isolated_network,
                                   self.admin_client)
