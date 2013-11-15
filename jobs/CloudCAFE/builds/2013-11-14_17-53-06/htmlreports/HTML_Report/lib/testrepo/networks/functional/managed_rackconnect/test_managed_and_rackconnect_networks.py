from IPy import IP
from ccengine.common.decorators import attr
from ccengine.common.constants.networks_constants import HTTPResponseCodes
from testrepo.common.testfixtures.networks import \
    NetworksManagedRackConnectUsersFixture


class TestManagedAndRackConnect(NetworksManagedRackConnectUsersFixture):

    @classmethod
    def setUpClass(cls):
        """Class setUp"""
        super(TestManagedAndRackConnect, cls).setUpClass()
        # Expected create server status code response if Wafflehaus disabled
        #cls.unallowed_status = HTTPResponseCodes.CREATE_SERVER

        # Expected create server status code response if Wafflehaus enabled
        cls.unallowed_status = HTTPResponseCodes.FORBIDDEN

    @attr('managed', 'negative', 'wafflehaus')
    def test_managed_create_server_with_only_isolated(self):
        """
        Managed user should not be able to create a server with only isolated
        networks
        """
        msg = ('Managed user should NOT be able to create servers with only '
               'isolated networks')
        networks = [self.managed_network_id]
        self.create_server_with_networks(network_list=networks,
            status_code=self.unallowed_status, msg=msg, managed=True)

    @attr('managed', 'negative', 'wafflehaus')
    def test_managed_create_server_with_only_public(self):
        """
        Managed user should not be able to create a server with only public
        network
        """
        msg = ('Managed user should NOT be able to create servers with only '
               'public network')
        networks = [self.public_id]
        self.create_server_with_networks(network_list=networks,
            status_code=self.unallowed_status, msg=msg, managed=True)

    @attr('managed', 'negative', 'wafflehaus')
    def test_managed_create_server_with_only_private(self):
        """
        Managed user should not be able to create a server with only private
        network
        """
        msg = ('Managed user should NOT be able to create servers with only '
               'private network')
        networks = [self.private_id]
        self.create_server_with_networks(network_list=networks,
            status_code=self.unallowed_status, msg=msg, managed=True)

    @attr('managed', 'negative', 'wafflehaus')
    def test_managed_create_server_with_only_public_and_isolated(self):
        """
        Managed user should not be able to create a server with only public
        and isolated networks
        """
        msg = ('Managed user should NOT be able to create servers with only '
               'public and isolated networks')
        networks = [self.public_id, self.managed_network_id]
        self.create_server_with_networks(network_list=networks,
            status_code=self.unallowed_status, msg=msg, managed=True)

    @attr('managed', 'negative', 'wafflehaus')
    def test_managed_create_server_with_only_private_and_isolated(self):
        """
        Managed user should not be able to create a server with only private
        and isolated networks
        """
        msg = ('Managed user should NOT be able to create servers with only '
               'private and isolated networks')
        networks = [self.private_id, self.managed_network_id]
        self.create_server_with_networks(network_list=networks,
            status_code=self.unallowed_status, msg=msg, managed=True)

    @attr('managed', 'positive', 'wafflehaus')
    def test_managed_create_server_with_networks(self):
        """
        Managed user should be able to create a server with public,
        private and isolated networks
        """

        # Create an active test server with public, private and isolated nets
        networks = [self.public_id, self.private_id, self.managed_network_id]
        nets_dd = self.networks_provider.get_server_network_dd(networks)
        resp = self.managed_servers_provider.create_active_server(
            networks=nets_dd)
        self.managed_servers_to_delete.append(resp.entity.id)

        cmsg = 'Unable to create active test server: {0} {1} {2}'.format(
            resp.status_code, resp.reason, resp.content)
        self.assertEqual(resp.status_code, HTTPResponseCodes.GET_SERVER, cmsg)

        # Verify server addresses
        pub = resp.entity.addresses.get_by_name(self.public_label)
        pri = resp.entity.addresses.get_by_name(self.private_label)
        iso = resp.entity.addresses.get_by_name(self.managed_network_label)

        amsg = 'Missing address for {0} network'
        self.assertIsNotNone(pub, amsg.format(self.public_label))
        self.assertIsNotNone(pri, amsg.format(self.private_label))
        self.assertIsNotNone(iso, amsg.format(self.managed_network_label))

        ipmsg = 'Unexpected IPv{0} version on {1} network'
        try:
            self.assertEqual(IP(pub.ipv4).version(), 4, ipmsg.format(4,
                self.public_label))
            self.assertEqual(IP(pub.ipv6).version(), 6, ipmsg.format(6,
                self.public_label))
            self.assertEqual(IP(pri.ipv4).version(), 4, ipmsg.format(4,
                self.private_label))
            self.assertEqual(IP(iso.ipv4).version(), 4, ipmsg.format(4,
                self.managed_network_label))
        except (ValueError, TypeError):
            self.fail('Managed Server IP address Error')

        # Assert the expected IPv4s are on the server via ssh
        ip_list = [pub.ipv4, pri.ipv4, iso.ipv4]
        self.helper.assert_ifconfig(server=resp.entity, ips=ip_list, find=True)

    @attr('managed', 'positive', 'wafflehaus')
    def test_managed_create_server_with_public_and_private(self):
        """
        Managed user should be able to create a server with public
        and private networks
        """

        # Create an active test server with public and private networks
        resp = self.managed_servers_provider.create_active_server()
        self.managed_servers_to_delete.append(resp.entity.id)

        cmsg = 'Unable to create active test server: {0} {1} {2}'.format(
            resp.status_code, resp.reason, resp.content)
        self.assertEqual(resp.status_code, HTTPResponseCodes.GET_SERVER, cmsg)

        # Verify server addresses
        pub = resp.entity.addresses.get_by_name(self.public_label)
        pri = resp.entity.addresses.get_by_name(self.private_label)

        amsg = 'Missing address for {0} network'
        self.assertIsNotNone(pub, amsg.format(self.public_label))
        self.assertIsNotNone(pri, amsg.format(self.private_label))

        ipmsg = 'Unexpected IPv{0} version on {1} network'
        try:
            self.assertEqual(IP(pub.ipv4).version(), 4, ipmsg.format(4,
                self.public_label))
            self.assertEqual(IP(pub.ipv6).version(), 6, ipmsg.format(6,
                self.public_label))
            self.assertEqual(IP(pri.ipv4).version(), 4, ipmsg.format(4,
                self.private_label))
        except (ValueError, TypeError):
            self.fail('Managed Server IP address Error')

        # Assert the expected IPv4s are on the server via ssh
        ip_list = [pub.ipv4, pri.ipv4]
        self.helper.assert_ifconfig(server=resp.entity, ips=ip_list, find=True)

    @attr('rackconnect', 'negative', 'wafflehaus')
    def test_rackconnect_create_server_with_only_isolated(self):
        """
        Rackconnect user should not be able to create a server with only
        isolated networks
        """
        msg = ('Rackconnect user should NOT be able to create servers with '
               'only isolated networks')
        networks = [self.rackconnect_network_id]
        self.create_server_with_networks(network_list=networks,
            status_code=self.unallowed_status, msg=msg, rackconnect=True)

    @attr('rackconnect', 'negative', 'wafflehaus')
    def test_rackconnect_create_server_with_only_public(self):
        """
        Rackconnect user should not be able to create a server with only
        public network
        """
        msg = ('Rackconnect user should NOT be able to create servers with '
               'only public network')
        networks = [self.public_id]
        self.create_server_with_networks(network_list=networks,
            status_code=self.unallowed_status, msg=msg, rackconnect=True)

    @attr('rackconnect', 'negative', 'wafflehaus')
    def test_rackconnect_create_server_with_only_private(self):
        """
        Rackconnect user should not be able to create a server with only
        private network
        """
        msg = ('Rackconnect user should NOT be able to create servers with '
               'only private network')
        networks = [self.private_id]
        self.create_server_with_networks(network_list=networks,
            status_code=self.unallowed_status, msg=msg, rackconnect=True)

    @attr('rackconnect', 'negative', 'wafflehaus')
    def test_rackconnect_create_server_with_only_public_and_isolated(self):
        """
        Rackconnect user should not be able to create a server with only
        public and isolated networks
        """
        msg = ('Rackconnect user should NOT be able to create servers with '
               'only public and isolated networks')
        networks = [self.public_id, self.rackconnect_network_id]
        self.create_server_with_networks(network_list=networks,
            status_code=self.unallowed_status, msg=msg, rackconnect=True)

    @attr('rackconnect', 'negative', 'wafflehaus')
    def test_rackconnect_create_server_with_only_private_and_isolated(self):
        """
        Rackconnect user should not be able to create a server with only
        private and isolated networks
        """
        msg = ('Rackconnect user should NOT be able to create servers with '
               'only private and isolated networks')
        networks = [self.private_id, self.rackconnect_network_id]
        self.create_server_with_networks(network_list=networks,
            status_code=self.unallowed_status, msg=msg, rackconnect=True)

    @attr('rackconnect', 'positive', 'wafflehaus')
    def test_rackconnect_create_server_with_networks(self):
        """
        Rackconnect user should be able to create a server with public,
        private and isolated networks
        """

        # Create an active test server with public, private and isolated nets
        networks = ([self.public_id, self.private_id,
                    self.rackconnect_network_id])
        nets_dd = self.networks_provider.get_server_network_dd(networks)
        resp = self.rackconnect_servers_provider.create_active_server(
            networks=nets_dd)
        self.rackconnect_servers_to_delete.append(resp.entity.id)

        cmsg = 'Unable to create active test server: {0} {1} {2}'.format(
            resp.status_code, resp.reason, resp.content)
        self.assertEqual(resp.status_code, HTTPResponseCodes.GET_SERVER, cmsg)

        # Verify server addresses
        pub = resp.entity.addresses.get_by_name(self.public_label)
        pri = resp.entity.addresses.get_by_name(self.private_label)
        iso = resp.entity.addresses.get_by_name(self.rackconnect_network_label)

        amsg = 'Missing address for {0} network'
        self.assertIsNotNone(pub, amsg.format(self.public_label))
        self.assertIsNotNone(pri, amsg.format(self.private_label))
        self.assertIsNotNone(iso, amsg.format(self.rackconnect_network_label))

        ipmsg = 'Unexpected IPv{0} version on {1} network'
        try:
            self.assertEqual(IP(pub.ipv4).version(), 4, ipmsg.format(4,
                self.public_label))
            self.assertEqual(IP(pub.ipv6).version(), 6, ipmsg.format(6,
                self.public_label))
            self.assertEqual(IP(pri.ipv4).version(), 4, ipmsg.format(4,
                self.private_label))
            self.assertEqual(IP(iso.ipv4).version(), 4, ipmsg.format(4,
                self.rackconnect_network_label))
        except (ValueError, TypeError):
            self.fail('Rackconnect Server IP address Error')

        # Assert the expected IPv4s are on the server via ssh
        ip_list = [pub.ipv4, pri.ipv4, iso.ipv4]
        self.helper.assert_ifconfig(server=resp.entity, ips=ip_list, find=True)

    @attr('Rackconnect', 'positive', 'wafflehaus')
    def test_rackconnect_create_server_with_public_and_private(self):
        """
        Rackconnect user should be able to create a server with public
        and private networks
        """

        # Create an active test server with public and private networks
        resp = self.rackconnect_servers_provider.create_active_server()
        self.rackconnect_servers_to_delete.append(resp.entity.id)

        cmsg = 'Unable to create active test server: {0} {1} {2}'.format(
            resp.status_code, resp.reason, resp.content)
        self.assertEqual(resp.status_code, HTTPResponseCodes.GET_SERVER, cmsg)

        # Verify server addresses
        pub = resp.entity.addresses.get_by_name(self.public_label)
        pri = resp.entity.addresses.get_by_name(self.private_label)

        amsg = 'Missing address for {0} network'
        self.assertIsNotNone(pub, amsg.format(self.public_label))
        self.assertIsNotNone(pri, amsg.format(self.private_label))

        ipmsg = 'Unexpected IPv{0} version on {1} network'
        try:
            self.assertEqual(IP(pub.ipv4).version(), 4, ipmsg.format(4,
                self.public_label))
            self.assertEqual(IP(pub.ipv6).version(), 6, ipmsg.format(6,
                self.public_label))
            self.assertEqual(IP(pri.ipv4).version(), 4, ipmsg.format(4,
                self.private_label))
        except (ValueError, TypeError):
            self.fail('Rackconnect Server IP address Error')

        # Assert the expected IPv4s are on the server via ssh
        ip_list = [pub.ipv4, pri.ipv4]
        self.helper.assert_ifconfig(server=resp.entity, ips=ip_list, find=True)

    def create_server_with_networks(self, network_list, status_code, msg=None,
                                    managed=None, rackconnect=None):
        """
        @summary: Creates a server with given networks and asserts the
        create server response has the provided status_code
        @param network_list: network uuids to be attached to the server
        @type: list
        @param status_code: expected status code response 202, 400, 403, etc.
        @type: int
        @param msg: user message in case of an unexpected status code
        @type: str
        @param managed: to use Managed user providers if True
        @type: boolean
        @param rackconnect: to use Rackconnect user providers if True
        @type: boolean
        """

        # Get networks data dict for server create request
        nets_dd = self.networks_provider.get_server_network_dd(network_list)

        if managed:
            resp = self.managed_servers_provider.create_server_no_wait(
                networks=nets_dd)
            if hasattr(resp.entity, 'id'):
                self.managed_servers_to_delete.append(resp.entity.id)
        elif rackconnect:
            resp = self.rackconnect_servers_provider.create_server_no_wait(
                networks=nets_dd)
            if hasattr(resp.entity, 'id'):
                self.rackconnect_servers_to_delete.append(resp.entity.id)
        else:
            resp = self.servers_provider.create_server_no_wait(
                networks=nets_dd)
            if hasattr(resp.entity, 'id'):
                self.servers_to_delete.append(resp.entity.id)

        smsg = ('Unexpected API Response: {0} {1}\n'
                'Response Content: {2}\n'
                'Expected Response: {3}\n'
                'Details: {4}'.format(resp.status_code, resp.reason,
                                      resp.content, status_code, msg))

        # assert the expected status code is given by the response
        self.assertEqual(resp.status_code, status_code, smsg)
