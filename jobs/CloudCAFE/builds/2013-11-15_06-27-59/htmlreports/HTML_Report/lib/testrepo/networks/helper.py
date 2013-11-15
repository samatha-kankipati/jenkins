import unittest2
import time
from IPy import IP
import ccengine.common.tools.datagen as datagen
import ccengine.common.tools.sshtools as sshtools
from ccengine.common.constants.networks_constants import Constants
from ccengine.common.constants.networks_constants import HTTPResponseCodes


class Helper(unittest2.TestCase):

    def __init__(self, networks_provider, servers_provider, nvp_provider,
                 servers_to_delete, networks_to_delete, run_nvp=None):
        super(Helper, self).__init__(methodName='runTest')
        self.networks_provider = networks_provider
        self.servers_provider = servers_provider
        self.servers_client = self.servers_provider.servers_client
        self.networks_client = self.networks_provider.client
        self.nvp_provider = nvp_provider
        self.networks_to_delete = networks_to_delete
        self.servers_to_delete = servers_to_delete
        #provide IsolatedNetwork objects with cidr, id and label
        self.public = self.networks_provider.get_public_network()
        self.private = self.networks_provider.get_private_network()
        #provide static data ids like 11111111-1111-1111-1111-111111111111
        self.public_id = Constants.PUBLIC_NETWORK_ID
        self.private_id = Constants.PRIVATE_NETWORK_ID

        self.run_nvp = run_nvp
        if self.nvp_provider:
            self.nvp_client = self.nvp_provider.aic_client
        else:
            self.nvp_client = None

    def runTest(self):
        pass

    def create_n_networks(self, num_networks, prefix='192.*.*.0', suffix='24'):
        """Creates n isolated networks"""
        net_list = []
        for _ in range(num_networks):
            if prefix is not None and suffix is not None:
                cidr = datagen.random_cidr(ip_pattern=prefix, mask=suffix)
            elif suffix is not None:
                cidr = datagen.random_cidr(mask=suffix)
            elif prefix is not None:
                cidr = datagen.random_cidr(ip_pattern=prefix)

            name = datagen.rand_name('n_network')
            res = self.networks_provider.client.create_network(cidr=cidr,
                                                               label=name)
            assert res.status_code == HTTPResponseCodes.CREATE_NETWORK, \
                'Networks create failed: {0} {1} {2}'.format(res.status_code,
                    res.reason, res.content)
            self.networks_to_delete.append(res.entity.id)
            net_list.append(res.entity.id)
        return net_list

    def create_network_with_n_servers(self, num_servers, no_public=None,
                                            no_private=None, flavorRef=None,
                                            networks=None, name=None):
        """Creates a network with multiple servers and returns server and
        network ids. Networks create can be overridden by the networks param"""
        if networks and isinstance(networks, list):
            network_list = networks
        else:
            network_list = self.create_n_networks(1)
        if not no_public:
            network_list.append(self.public_id)
        if not no_private:
            network_list.append(self.private_id)
        new_net_list = self.networks_provider.get_server_network_dd(
                                                                network_list)
        server_list = []
        for _ in range(num_servers):
            res = self.servers_provider.create_server_no_wait(name=name,
                networks=new_net_list, flavorRef=flavorRef)
            assert res.status_code == HTTPResponseCodes.CREATE_SERVER, \
                'Server create failed: {0} {1} {2}'.format(res.status_code,
                    res.reason, res.content)
            self.servers_to_delete.append(res.entity.id)
            server_list.append(res.entity.id)
        return server_list, network_list

    def create_server_with_n_networks(self, num_networks, network_list=None,
                                      flavorRef=None):
        """Creates a server with multiple networks this method needs access to
        the servers provider (reason why is not in the networks provider)"""
        if num_networks:
            net_list = self.create_n_networks(num_networks)
        else:
            net_list = []
        if network_list is not None:
            net_list.extend(network_list)
        new_net_list = self.networks_provider.get_server_network_dd(net_list)
        res = self.servers_provider.create_server_no_wait(
            networks=new_net_list, flavorRef=flavorRef)
        assert res.status_code == HTTPResponseCodes.CREATE_SERVER, \
            'Server create failed: {0} {1} {2}'.format(res.status_code,
                res.reason, res.content)
        self.servers_to_delete.append(res.entity.id)
        return res, net_list

    class DataObj(object):
        def __init__(self):
            self.id = None
            self.adminPass = None
            self.net_list = None

    def create_list_servers(self, num_networks, network_list=None):
        """Pass id, adminPass and net_list of a create server with n networks
        call. It also verifies the 202 response code"""
        server, net_list = self.create_server_with_n_networks(num_networks,
                                                              network_list)
        #check the temporary test server was created OK, 202 status code
        assert server.status_code == HTTPResponseCodes.CREATE_SERVER, \
                                                'Unable to create test server'
        data = self.DataObj()
        data.id = server.entity.id
        data.adminPass = server.entity.adminPass
        data.net_list = net_list
        return data

    def create_build_list_server(self, wNetworks=None):
        """Creates a server for testing with the BUILD status"""
        if wNetworks:
            self.build_server = self.create_list_servers(1,
                                            [self.private.id, self.public.id])
        else:
            self.build_server = self.create_list_servers(0)
        return self.build_server

    def get_vi_id(self, interface_list, param):
        """Provides the Virtual Interface ID of a network type"""
        for interface in interface_list:
            if interface.network_label == self.public.label \
            and param == self.public.label:
                return interface.id
            elif interface.network_label == self.private.label \
            and param == self.private.label:
                return interface.id
            elif param == 'isolated' and \
            interface.network_label != self.public.label and \
            interface.network_label != self.private.label:
                return interface.id

    def list_interface_ips(self, server, network, version=4):
        """
        @summary: Makes a list virtual interfaces call and retrieves the
        IP addresses of the given server entity and network object
        @param server: server entity from the get server response call
        @type: Server instance
        @param network: network entity
        @type: IsolatedNetwork instance
        @param version: IP address version (4 or 6)
        @type: int
        @return: ip addresses
        @rtype: list
        """
        vlresp = self.networks_client.list_virtual_interfaces(server.id)
        msg = 'Unable to list virtual interfaces: {0} {1} {2}'.format(
                             vlresp.status_code, vlresp.reason, vlresp.content)
        assert HTTPResponseCodes.LIST_INTERFACES == vlresp.status_code, msg

        vif_list = vlresp.entity
        ip_list = []
        for vif in vif_list:
            for addr in vif.ip_addresses:
                if (addr.network_id == network.id and
                    IP(addr.address).version() == version):
                    ip_list.append(addr.address)
        return ip_list

    def get_server_ips(self, server, network, version=4):
        """
        @summary: Gets the network IPs from a get server client call
        response entity by address version
        @param server: server entity from the get server response call
        @type: Server instance
        @param network: network entity
        @type: IsolatedNetwork instance
        @param version: IP address version (4 or 6)
        @type: int
        @return: ip addresses
        @rtype: list
        """
        sresp = self.servers_client.get_server(server.id)
        msg = 'Unable to get server: {0} {1} {2}'.format(sresp.status_code,
                                                   sresp.reason, sresp.content)
        assert HTTPResponseCodes.GET_SERVER == sresp.status_code, msg

        # Overwriting the server object with a more recent one
        server = sresp.entity
        server_addresses = server.addresses.get_by_name(network.label)

        ip_list = []
        if hasattr(server_addresses, 'addresses'):
            addresses = getattr(server_addresses, 'addresses')
            for addr in addresses:
                if addr.version == version:
                    ip_list.append(addr.addr)
        return ip_list

    def list_server_ips(self, server, network, version=4):
        """
        @summary: Makes a list servers with detail call and retrieves the
        IP addresses of the given server entity and network object
        @param server: server entity from the get server response call
        @type: Server instance
        @param network: network entity
        @type: IsolatedNetwork instance
        @param version: IP address version (4 or 6)
        @type: int
        @return: ip addresses
        @rtype: list
        """
        slresp = self.servers_client.list_servers_with_detail()
        msg = 'Unable to list servers with detail: {0} {1} {2}'.format(
                             slresp.status_code, slresp.reason, slresp.content)
        assert HTTPResponseCodes.LIST_SERVERS == slresp.status_code, msg

        servers_list = slresp.entity
        ip_list = None
        for s in servers_list:
            if s.id == server.id:
                ip_list = self.get_server_ips(s, network, version)
        msg = 'Unable to find server {0} in list servers with detail response'
        self.assertIsNotNone(ip_list, msg.format(server.id))
        return ip_list

    def remove_all_ips(self, server, network, admin_client):
        """
        @summary: tries to remove all network IPs from a server and verifies
        that the last IP of a network can NOT be removed
        @param server: server entity
        @type: server instance
        @param network: server network entity
        @type: IsolatedNetwork instance
        @param admin_client: Compute Admin Client
        @type: AdminAPIClient instance
        """
        # Get initial IPs and IP counts
        ips = self.get_server_ips(server, network)
        ip_count = len(ips)

        msg = 'Server {0} is missing {1} network IPs'.format(server.id,
                                                             network.label)
        self.assertGreaterEqual(ip_count, 1, msg)

        # iv6 value needed for the assert_ips method call below, public
        # should have 1 while private and isolated 0 based on the setUp
        if network.label == 'public':
            ipv6 = 1
        else:
            ipv6 = 0

        # Initial check
        self.assert_ips(server, network, ip_count, ipv6)

        # Try to remove all IPs
        for ip_to_remove in ips:
            rem_req = admin_client.remove_fixed_ip(server.id, ip_to_remove)
            ip_count -= 1

            if ip_count >= 1:
                msg = ('Unable to remove a {0} network fixed IP to server {1} '
                    'Response: {2} {3} {4}'.format(network.label,
                    server.id, rem_req.status_code, rem_req.reason,
                    rem_req.content))
                self.assertEqual(rem_req.status_code,
                                 HTTPResponseCodes.REMOVE_FIXED_IP, msg)
                self.assert_ips(server, network, ip_count, ipv6)
                self.assert_ifconfig(server, ip_to_remove, find=False)
            else:
                msg = ('Tried to remove last IP of {0} network in server {1} '
                    'Unexpected Response: {2} {3} {4}'.format(network.label,
                    server.id, rem_req.status_code, rem_req.reason,
                    rem_req.content))

                # Bug: 202 response given instead of error, update needed
                # once fixed and expected status code given
                self.assertEqual(rem_req.status_code,
                                 HTTPResponseCodes.REMOVE_FIXED_IP, msg)

                # The IP should still be in the calls, setting to 1 the
                # expected IP count
                self.assert_ips(server, network, 1, ipv6)

                # The IP should be still in the server
                self.assert_ifconfig(server, ip_to_remove, find=True)

                # Check NVP allowed address pairs still has the last IP
                if self.run_nvp:
                    if network.label == 'public':
                        self.check_nvp_public_allowed_address_pairs(server.id,
                            ip_to_remove, find=True)
                    elif network.label == 'private':
                        self.check_nvp_private_allowed_address_pairs(server.id,
                            ip_to_remove, find=True)
                    else:
                        pass

    def assert_server_ips(self, server, network_label, version=4):
        """
        @summary: Asserts server IPs based on network and version and returns
            the IP. In case of multiple fixed ips will check the first one
        @param server: Server entity
        @type: ccengine.domain.compute.response.server.Server instance
        @param network_label: network label, for ex. Public
        @type: str
        @param version: IP address version for ex. 4 or 6
        @type: int
        """
        address = server.addresses.get_by_name(network_label)

        msg = 'Missing network or IPv{0} address for {1} network at server {2}'
        self.assertIsNotNone(address, msg.format(version, network_label,
                                                 server.id))

        # Check the server obj has the expected address attributes and values
        msg = 'Server {0} missing IPv{1} attribute from network {2}'
        if version == 6:
            self.assertTrue(hasattr(address, 'ipv6'),
                msg.format(server.id, version, network_label))
            ip_addr = getattr(address, 'ipv6')
        else:
            self.assertTrue(hasattr(address, 'ipv4'),
                msg.format(server.id, version, network_label))
            ip_addr = getattr(address, 'ipv4')
        msg = 'Unexpected IPv{0} version for {1} network at server {2}'
        try:
            self.assertEqual(IP(ip_addr).version(), version, msg.format(
                version, network_label, server.id))
        except (ValueError, TypeError):
            self.fail('IP address {0} Value or Type Error at IPv{1} version '
                      'for {2} network at server {3}'.format(ip_addr, version,
                          network_label, server.id))
        return ip_addr

    def assert_server_data(self, server_list, server_data, network_names,
                           network_list, ipv6_check_list=None):
        """
        @summary: Verify server addresses with servers data
        @param server_list: list of test servers
        @type: list of server entity instances
        @param network_names: network names in predefined server data dict
        @type: list of strings (public, private, isolated_B, etc.)
        @param network_list: list of server expected networks
        @type: list of network entity instances
        @param ipv6: enable IPv6 check for network within the same index of
                     the network_labels list
        @type: list of booleans (True or False)
        """
        msg = ('Server {0} IP address {1} different than expected data '
               'IP address {2}')

        total_results = []
        for index, server in enumerate(server_list):
            for index2, network_name in enumerate(network_names):
                if server_data[index][network_name]:
                    ip_label = '{0}_ip'.format(network_name)
                    data_ipv4s = server_data[index][ip_label]
                    if data_ipv4s:
                        data_ipv4 = data_ipv4s[0]
                        data_ipv4s.sort()
                    else:
                        data_ipv4 = None
                    ip_labelv6 = '{0}_ipv6'.format(network_name)
                    data_ipv6s = server_data[index][ip_labelv6]
                    if data_ipv6s:
                        data_ipv6 = data_ipv6s[0]
                        data_ipv6s.sort()
                    else:
                        data_ipv6 = None
                    ipv4s = self.get_server_ips(server, network_list[index2],
                                                version=4)
                    ipv4s.sort()
                    ipv6s = self.get_server_ips(server,
                        network_list[index2], version=6)
                    ipv6s.sort()

                    results = dict(server=server.id, network_name=network_name,
                        network_label=network_list[index2].label,
                        data_ipv4s=data_ipv4s, data_ipv6s=data_ipv6s,
                        server_ipv4s=ipv4s, server_ipv6s=ipv6s,
                        server_ipv4=None, server_ipv6=None,
                        result=None, resultv6=None)

                    try:
                        ipv4 = self.assert_server_ips(server,
                            network_list[index2].label, version=4)
                        results['server_ipv4'] = ipv4
                        self.assertEqual(data_ipv4, ipv4, msg.format(
                            server.id, ipv4, data_ipv4))
                        self.assertListEqual(data_ipv4s, ipv4s, msg.format(
                            server.id, ipv4s, data_ipv4s))
                    except AssertionError as error:
                        results['result'] = error.message
                    else:
                        results['result'] = Constants.EXPECTED_RESULT
                    if ipv6_check_list and ipv6_check_list[index2]:
                        try:
                            ipv6 = self.assert_server_ips(server,
                                network_list[index2].label, version=6)
                            results['server_ipv6'] = ipv6
                            self.assertEqual(data_ipv6, ipv6, msg.format(
                                server.id, ipv6, data_ipv6))
                            self.assertListEqual(data_ipv6s, ipv6s, msg.format(
                                server.id, ipv6s, data_ipv6s))
                        except AssertionError as error:
                            results['resultv6'] = error.message
                        else:
                            results['resultv6'] = Constants.EXPECTED_RESULT

                    total_results.append(results)
        return total_results

    def get_remote_client(self, server, username=None):
        """
        @summary: create a remote client via ssh
        @param server: server to connect to via ssh
        @type: Server object instance with adminPass attr
        @param username: username for ssh connection
        @type: string or None (default root)
        """
        if username:
            msg_usr = username
        else:
            msg_usr = 'root'

        remote_client = self.servers_provider.get_remote_instance_client(
            server, username=username)
        msg = 'Unable to ssh: {0}@{1}'.format(msg_usr,
                                              server.addresses.public.ipv4)
        self.assertTrue(remote_client.can_authenticate(), msg)

        # Verify expected hostname
        hostname = remote_client.get_hostname()
        hnmsg = 'Expected {0} hostname instead of {1}'.format(server.name,
                                                              hostname)
        self.assertEqual(hostname.lower().replace('_', '-'),
                         server.name.lower().replace('_', '-'), hnmsg)
        return remote_client

    def remote_ping(self, remote_client, ip_list, count=3,
                    accepted_packet_loss_pct=0, negative=False):
        """
        @summary: SSH into server and ping IPs
        @param remote_client: server connected to via ssh
        @type: remote client instance
        @param ip_list: list of IPs to ping from remote client
        @type: list
        @param count: Packets to transmit
        @type: int
        @param accepted_packet_loss_pct: acceptance criteria for packet loss
        @type: int
        """
        if not isinstance(ip_list, list):
            ip_list = [ip_list]

        res = remote_client.can_remote_ping_ips(ip_list=ip_list, count=count)

        result = []
        failure_flag = False
        for index, loss_pct in enumerate(res):
            if negative:
                accepted_packet_loss_pct = 100
                diff = loss_pct == accepted_packet_loss_pct
                msg_err = ('Network IP {0} ping from server {1} got unexpected'
                           ' packet loss of {2}%; expected {3}% with no '
                           'connectivity - FAILED')
                msg_ok = ('Network IP {0} ping from server {1} without '
                          'connectivity as expected - OK')
            else:
                diff = loss_pct <= accepted_packet_loss_pct
                msg_err = ('Network IP {0} ping from server {1} got unexpected'
                           ' packet loss of {2}%; expected at most {3}% - '
                           'FAILED')
                msg_ok = 'Network IP {0} ping from server {1} - OK'

            if diff:
                result.append(msg_ok.format(ip_list[index],
                    remote_client.server_id, loss_pct,
                    accepted_packet_loss_pct))
            else:
                result.append(msg_err.format(ip_list[index],
                    remote_client.server_id, loss_pct,
                    accepted_packet_loss_pct))
                failure_flag = True

        msg = 'Got unexpected connectivity. Remote Ping Results: {0}'
        self.assertFalse(failure_flag, msg.format(
            result))

    def assert_ifconfig(self, server=None, ips=None, find=True, username=None,
                        order_list=None, remote_client=None, retry=5):
        """
        @summary: Assert in the server or remote client the IPs given are
        or not found via ssh by ifconfig
        @param server: server to connect to via ssh
        @type: Server object instance with adminPass attr
        @param ip: server IPv4 address
        @type: string or list
        @param find: if the ip should or should not be found
        @type: boolean True or False
        @param username: username for ssh connection
        @type: string or None (default root)
        @param order_list: network interfaces of ips
        @type: list of strings, for ex. eth0, eth0:1, eth1, eth2, eth2:1, ...
        @param remote_client: server connected via ssh
        @type: ccengine.clients.remote_instance
        """
        if not isinstance(ips, list):
            ips = [ips]

        if order_list is not None:
            if not isinstance(order_list, list):
                order_list = [order_list]

        if remote_client is None:
            remote_client = self.get_remote_client(server=server,
                                                   username=username)

        # Adding addr and a trailing blank space to IP search string so there
        # is no mix up with Bcast or Mask data
        for index, ip in enumerate(ips):
            if IP(ip).version() == 6:
                ip_data = 'addr: {0}'.format(IP(ip).strNormal())
            else:
                ip_data = 'addr:{0} '.format(ip)

            # Assert based on find value
            fmsg = ('{0} ifconfig search result expected a {1} but returned a '
                '{2} on server {3}'.format(ip_data, str(find),
                                           str(not(find)),
                                           server.addresses.public.ipv4))
            if find:
                count = 0
                while count < retry:
                    # Get ifconfig data from server
                    ifconfig_data = remote_client.get_ifconfig()
                    addr_index = ifconfig_data.find(ip_data)
                    if addr_index != -1:
                        break
                    time.sleep(3)
                    count += 1
                self.assertTrue(addr_index != -1, fmsg)

                # Check IP server order
                if order_list is not None:
                    eth_index = ifconfig_data.find(order_list[index])
                    diff_index = addr_index - eth_index

                    # Expected diff around 73 chars
                    exp_diff = 73
                    imsg = ('Unexpected {0} char index difference between {1}'
                            ' and {2}, on ifconfig server response. Unable to'
                            ' confirm the IP expected eth'.format(diff_index,
                            order_list[index], ip_data, exp_diff))
                    self.assertAlmostEqual(diff_index, exp_diff, msg=imsg,
                                           delta=10)

            else:
                count = 0
                while count < retry:
                    # Get ifconfig data from server
                    ifconfig_data = remote_client.get_ifconfig()
                    addr_index = ifconfig_data.find(ip_data)
                    if addr_index == -1:
                        break
                    time.sleep(3)
                    count += 1
                self.assertTrue(addr_index == -1, fmsg)

    def assert_ip_version(self, ips, version=4):
        """
        @summary: Assert the IP version
        @param ip: IPv4 or IPv6 address or CIDR
        @type: string or list
        @param version: IP version (4 or 6)
        @type: int
        """
        if not isinstance(ips, list):
            ips = [ips]
        for ip in ips:
            try:
                ipmsg = 'Expected version {0} instead of {1} for IP {2}'.\
                    format(version, IP(ip).version(), ip)
                self.assertEqual(IP(ip).version(), version, ipmsg)
            except (ValueError, TypeError):
                self.fail('Unexpected data value or type for IP: {0}'.
                    format(ip))

    def assert_ips(self, server, network, ipv4, ipv6=0, interval_time=10,
                   timeout=45):
        """
        @summary: Assert the IPv4 and IPv6 addresses counts in the get server,
        list servers with detail, and virtual interface list calls
        @param server: server entity from the get server response call
        @type: Server instance
        @param network: network entity
        @type: IsolatedNetwork instance
        @param ipv4: expected count of IPv4 addresses
        @type: int
        @param ipv6: expected count of IPv6 addresses
        @type: int
        """
        # Get IPs from the get server call and wait the timeout to get the
        # expected counts
        time_count = 0
        while True:
            try:
                ips_v4 = self.get_server_ips(server, network)
                ips_v6 = self.get_server_ips(server, network, 6)
                if ((len(ips_v4) == ipv4 and len(ips_v6) == ipv6)
                    or time_count >= timeout):
                    break
            except:
                pass
            finally:
                time.sleep(interval_time)
                time_count += interval_time

        cmsg = 'Expected {0} {1} IPv{2} addresses instead of {3}'

        # Assert the expected address count from the get server response
        self.assertEqual(len(ips_v6), ipv6, cmsg.format(ipv6, network.label, 6,
                                                        len(ips_v6)))
        self.assertEqual(len(ips_v4), ipv4, cmsg.format(ipv4, network.label, 4,
                                                        len(ips_v4)))
        # Get IPs from the list servers with detail call
        lips_v4 = self.list_server_ips(server, network)
        lips_v6 = self.list_server_ips(server, network, 6)

        # Assert the expected address count from the list servers with detail
        # response
        self.assertEqual(len(lips_v6), ipv6, cmsg.format(ipv6, network.label,
                                                         6, len(lips_v6)))
        self.assertEqual(len(lips_v4), ipv4, cmsg.format(ipv4, network.label,
                                                         4, len(lips_v4)))

        lmsg = 'Different addresses in get server and list servers responses'
        self.assertListEqual(ips_v4, lips_v4, lmsg)
        self.assertListEqual(ips_v6, lips_v6, lmsg)

        # Get IPs from the list virtual interfaces call
        vips_v4 = self.list_interface_ips(server, network)
        vips_v6 = self.list_interface_ips(server, network, 6)

        # Assert the expected address count from the list virtual interfaces
        # response
        self.assertEqual(len(vips_v6), ipv6, cmsg.format(ipv6, network.label,
                                                         6, len(vips_v6)))
        self.assertEqual(len(vips_v4), ipv4, cmsg.format(ipv4, network.label,
                                                         4, len(vips_v4)))

        vlmsg = ('Different addresses in list servers and list virtual '
                'interfaces responses')
        self.assertListEqual(lips_v4, vips_v4, vlmsg)
        self.assertListEqual(lips_v6, vips_v6, vlmsg)

    def check_nvp_public_allowed_address_pairs(self, server_id, added_ip,
                                               find=True):
        """
        @summary: Gets IPv4 public addresses from the virtual interface call
        and asserts they are also in NVP as allowed address pairs in the
        expected public switch port. It also asserts that the added ip is
        there when expected and is gone after it is removed
        @param server_id: instance id
        @type: string
        @param added_ip: ip address of IP to be added and removed
        @type: string
        @param find: if the added ip is expected in NVP allowed address pairs
        @type: boolean (True or False)
        """
        public_interface = self.networks_provider.get_public_interface(
            server_id)
        msg = 'Unable to get server {0} public interface'.format(server_id)
        self.assertIsNotNone(public_interface, msg)
        public_mac_address = public_interface.mac_address

        # Get public IPv4 addresses from virtual interface call
        public_ipv4 = []
        for ip_address in public_interface.ip_addresses:
            if IP(ip_address.address).version() == 4:
                public_ipv4.append(ip_address.address)

        # Get IPv4 allowed address pairs from NVP Public Switch Port
        ports = self.nvp_client.list_lswitch_ports(
            attachment_vif_mac=public_mac_address)
        pmsg = 'Unable to get server {0} ports with mac address {1}'.format(
            server_id, public_mac_address)
        self.assertTrue(ports['results'], pmsg)
        port = ports['results'][0]['allowed_address_pairs']
        nvp_public_ipv4 = []
        for ip_address in port:
            if IP(ip_address['ip_address']).version() == 4:
                nvp_public_ipv4.append(ip_address['ip_address'])

        # Assert IPv4 addresses are in NVP and if the added IP should be there
        lmsg = ('Server {0} IPv4 addresses different from NVP allowed address '
            'pairs list in public switch port with mac address {1}'.format(
            server_id, public_mac_address))
        fmsg = ('Expected {0} IP find on NVP allowed address pairs to be {1} '
            'on server {2}'.format(added_ip, find, server_id))
        public_ipv4.sort()
        nvp_public_ipv4.sort()
        self.assertListEqual(public_ipv4, nvp_public_ipv4, lmsg)
        if not isinstance(added_ip, list):
            added_ip = [added_ip]
        if find:
            for ip in added_ip:
                self.assertTrue(ip in nvp_public_ipv4, fmsg)
        else:
            for ip in added_ip:
                self.assertFalse(ip in nvp_public_ipv4, fmsg)

    def check_nvp_private_allowed_address_pairs(self, server_id, added_ip,
                                                find=True):
        """
        @summary: Gets IPv4 private addresses from the virtual interface call
        and asserts they are also in NVP as allowed address pairs in the
        expected private switch port. It also asserts that the added ip is
        there when expected and is gone after it is removed
        @param server_id: instance id
        @type: string
        @param added_ip: ip address of IP to be added and removed
        @type: string
        @param find: if the added ip is expected in NVP allowed address pairs
        @type: boolean (True or False)
        """
        private_interface = self.networks_provider.get_private_interface(
            server_id)
        msg = 'Unable to get server {0} private interface'.format(server_id)
        self.assertIsNotNone(private_interface, msg)
        private_mac_address = private_interface.mac_address

        # Get private IPv4 addresses from virtual interface call
        private_ipv4 = []
        for ip_address in private_interface.ip_addresses:
            if IP(ip_address.address).version() == 4:
                private_ipv4.append(ip_address.address)

        # Get IPv4 allowed address pairs from NVP private Switch Port
        ports = self.nvp_client.list_lswitch_ports(
            attachment_vif_mac=private_mac_address)
        pmsg = 'Unable to get server {0} ports with mac address {1}'.format(
            server_id, private_mac_address)
        self.assertTrue(ports['results'], pmsg)
        port = ports['results'][0]['allowed_address_pairs']
        nvp_private_ipv4 = []
        for ip_address in port:
            if IP(ip_address['ip_address']).version() == 4:
                nvp_private_ipv4.append(ip_address['ip_address'])

        # Assert IPv4 addresses are in NVP and if the added IP should be there
        lmsg = ('Server {0} IPv4 addresses different from NVP allowed address '
            'pairs list in private switch port with mac address {1}'.format(
            server_id, private_mac_address))
        fmsg = ('Expected {0} IP find on NVP allowed address pairs to be {1} '
            'on server {2}'.format(added_ip, find, server_id))
        private_ipv4.sort()
        nvp_private_ipv4.sort()
        self.assertListEqual(private_ipv4, nvp_private_ipv4, lmsg)
        if not isinstance(added_ip, list):
            added_ip = [added_ip]
        if find:
            for ip in added_ip:
                self.assertTrue(ip in nvp_private_ipv4, fmsg)
        else:
            for ip in added_ip:
                self.assertFalse(ip in nvp_private_ipv4, fmsg)

    def check_virtual_interface_delete(self, server_id, net_list, vi_to_delete,
                                       interval_time=7, timeout=100):
        """Checks that the Virtual Interface was deleted"""

        msg = 'Unable to get virtual interfaces from server {0}'
        time_count = 0
        while True:
            try:
                #check the interface was deleted from the server
                interfaces = (
                    self.networks_provider.client.list_virtual_interfaces(
                        server_id))
                self.assertEqual(interfaces.status_code,
                    HTTPResponseCodes.LIST_INTERFACES, msg.format(server_id))
                interface_list = interfaces.entity
                if (len(net_list) - 1 == len(interface_list)
                    or time_count >= timeout):
                    break
            except:
                pass
            finally:
                time.sleep(interval_time)
                time_count += interval_time

        vmsg = 'Expected {0} instead of {1} virtual interfaces'
        self.assertEqual(len(net_list) - 1, len(interface_list),
                         vmsg.format(len(net_list) - 1, len(interface_list)))
        for i in range(len(interface_list)):
            self.assertNotEqual(interface_list[i].id, vi_to_delete)

    def check_virtual_interface_response(self, interface_list, net_list,
                                         server):
        """Checks the VirtualInterface Object params. Expects a
        VirtualInterface response object by the list or create service, the
        expected networks ids list and a server response obj for ipv4 and 6"""
        #assert with data from NVP like Logical Queue and Allowed Address Pairs
        if self.run_nvp:
            self.verify_nvp_interface_list(interface_list, server)
        for interface in interface_list:
            self.assertTrue(interface.id)
            self.assertTrue(interface.mac_address)
            for addr in interface.ip_addresses:
                #getting ipv4 and ipv6 for assertion
                server_addrs = server.addresses.get_by_name(addr.network_label)
                self.assertIsNotNone(server_addrs,
                        '%s Network Missing on Server' % (addr.network_label))
                #Public should have both but sometimes only gets IPv6, there
                #is a known bug D-10238. Isolated and private usually only
                #have IPv4
                ipvs = [server_addrs.ipv4, server_addrs.ipv6]
                #Check the IP of the virtual interface at least has one
                self.assertIn(addr.address, ipvs, 'Unexpected IP in virtual '
                                                                'interface')
                #Check the network ID of the virtual interface
                self.assertIn(addr.network_id, net_list, 'Network ID not found'
                                                    ' in virtual interfaces')
                #getting the networks data
                if addr.network_label == 'public':
                    data = self.networks_provider.get_public_network()
                    self.assertTrue(addr.address, 'Missing Public address')
                    self.assertEqual(data.id, addr.network_id, 'Unexpected '
                                                        'Public Network ID')
                elif addr.network_label == 'private':
                    data = self.networks_provider.get_private_network()
                    self.assertTrue(addr.address, 'Missing Private address')
                    self.assertEqual(data.id, addr.network_id, 'Unexpected '
                                                        'Private Network ID')
                else:
                    data = self.networks_provider.client.get_network(
                                                    addr.network_id).entity
                    self.assertIsNotNone(data,
                        'Unable to get network {0}'.format(addr.network_id))
                    #Check the cidr of the isolated network
                    self.assertEqual(data.cidr[:-4], addr.address[:-1],
                                     'Unexpected cidr on Isolated Network')
                #Check the network label
                self.assertEqual(data.label, addr.network_label, 'Unexpected'
                                                            'network label')

    def verify_interface_in_list(self, interface, interface_list,
                                 server, network):
        '''Asserts that an interface is correctly in the interface list.'''
        interface_ids = [interface_item.id
                         for interface_item in interface_list
                         if interface_item.id == interface.id]
        self.assertNotEquals(len(interface_ids), 0,
                             'No interfaces in list match the new id.')
        self.assertEquals(len(interface_ids), 1,
                          'Multiple interfaces with same id.')
        for interface_item in interface_list:
            if interface_item.id == interface.id:
                self.verify_interface(interface, server, network)
                break

    def verify_interface(self, interface, server, network):
        """Asserts interface data with server and network"""
        interface_network_id = interface.ip_addresses[0].network_id
        interface_network_label = interface.ip_addresses[0].network_label
        nmsg = ('Virtual Interface {0} network id {1} different than expected '
                'network id {2} for server {3}').format(interface.id,
                interface_network_id, network.id, server.id)
        self.assertEquals(interface_network_id, network.id, nmsg)
        lmsg = ('Virtual Interface {0} network label {1} different than '
                'expected network label {2} for server {3}').format(
                interface.id, interface_network_label, network.label,
                server.id)
        self.assertEquals(interface_network_label, network.label, lmsg)
        server_addr = server.addresses.get_by_name(network.label)
        amsg = ('Server {0} missing IP address of {1} Network {2} for '
                'VIF {3}'.format(server.id, network.label, network.id,
                                 interface.id))
        self.assertIsNotNone(server_addr, amsg)
        ipmsg = ('Interface {0} from server {1} missing {2} address of {3}'
                 'network {4}')
        aemsg = ('Virtual Interface {0} {1} address {2} different than '
                   'server {3} IPv4 address {4} for {5} network {6}')
        if server_addr.ipv4 is not None:
            self.assertIsNotNone(interface.get_ipv4_address(network.id),
                ipmsg.format(interface.id, server.id, 'IPv4',
                             network.label, network.id))
            interface_ipv4 = interface.get_ipv4_address(network.id).address
            self.assertEquals(interface_ipv4, server_addr.ipv4, aemsg.format(
                interface.id, 'IPv4', interface_ipv4, server.id,
                server_addr.ipv4, network.label, network.id))
        if server_addr.ipv6 is not None:
            self.assertIsNotNone(interface.get_ipv6_address(network.id),
                ipmsg.format(interface.id, server.id, 'IPv6',
                             network.label, network.id))
            interface_ipv6 = interface.get_ipv6_address(network.id).address
            self.assertEquals(interface_ipv6, server_addr.ipv6, aemsg.format(
                interface.id, 'IPv6', interface_ipv6, server.id,
                server_addr.ipv6, network.label, network.id))

    def verify_nvp_interface_list(self, interface_list, server):
        for interface in interface_list:
            if interface.network_id == self.public.id:
                network = self.public
            elif interface.network_id == self.private.id:
                network = self.private
            else:
                network = self.networks_provider.client.get_network(
                                                interface.network_id).entity
            self.verify_nvp_interface(interface, server, network)

    def verify_nvp_interface(self, interface, server, network):
        if network is None or network.id == self.public.id\
            or network.id == self.private.id:
            lswitch_ports = self.nvp_provider.aic_client.list_lswitch_ports(
                                    lswitch_uuid='*',
                                    attachment_vif_mac=interface.mac_address)
        else:
            #verify the isolated network virtual interface has a switch in nvp
            lswitch = self.nvp_provider.aic_client.get_lswitch(network.id)
            self.assertEqual(lswitch['display_name'], network.label,
                                                    'Unexpected switch name')
            self.assertEqual(lswitch['uuid'], network.id,
                                                    'Unexpected switch uuid')

            lswitch_ports = self.nvp_provider.aic_client.list_lswitch_ports(
                                    lswitch_uuid=network.id,
                                    attachment_vif_mac=interface.mac_address)
        #verify the virtual interface has a switch port in nvp
        self.assertEquals(len(lswitch_ports['results']), 1,
                          'Should only be 1 port with mac address %s.' %
                          interface.mac_address)
        self.assertEquals(lswitch_ports['result_count'], 1,
                                        'Unexpected switch ports result count')
        #TODO: Uncomment when bugs are fixed
#        nvp_lswitch_port = lswitch_ports['results'][0]
#        self.assertNotEquals(nvp_lswitch_port['allowed_address_pairs'], 0,
#                             'The servers address should be allowed.')
#        allowed_addresses = [ip_tools.expand_ipv6_zeroes(addr['ip_address'])
#                             for addr in
#                             nvp_lswitch_port['allowed_address_pairs']]
#        mac_addresses = [addr['mac_address'] for addr in
#                              nvp_lswitch_port['allowed_address_pairs']]
#        for mac_address in mac_addresses:
#            self.assertEquals(mac_address.upper(),
#                              interface.mac_address.upper(),
#                              'Invalid mac address in nvp allowed addresses')
#        if server.addresses.get_by_name(network.label).ipv4 is not None:
#            self.assertIn(server.addresses.get_by_name(network.label).ipv4,
#                          allowed_addresses,
#                          'Server IP is not in allowed addresses.')
#        if server.addresses.get_by_name(network.label).ipv6 is not None:
#            addr = server.addresses.get_by_name(network.label).ipv6
#            self.assertIn(ip_tools.expand_ipv6_zeroes(addr),
#                          allowed_addresses,
#                          'Server IP is not in allowed addresses.')
#        self.assertNotEquals(nvp_lswitch_port['queue_uuid'], None)
#        qos = self.nvp_provider.aic_client.get_qos(
#                                               nvp_lswitch_port['queue_uuid'])
#        self.assertEquals(qos['min_bandwidth_rate'], 0,
#                          'Min QoS bandwidth should be 0')
#        self.assertEquals(qos['max_bandwidth_rate'],
#                      Constants.FLAVOR_QOS_RATES[server.flavor.id],
#                      'Max QoS bandwidth is not set up correctly by flavor')

    def verify_ifconfig(self, server, network, gateway_server=None, retry=5):
        command = 'ifconfig'
        ip = server.addresses.get_by_name(network.label).ipv4

        if gateway_server:
            gw_ip = gateway_server.addresses.public.ipv4
            gw_password = gateway_server.adminPass
            remote_ip = server.addresses.get_by_name(network.label).ipv4
            remote_password = server.adminPass

        count = 0
        resp = False
        while count < retry:
            try:
                if gateway_server is None:
                    out = sshtools.execute_remote_command(
                        server.addresses.public.ipv4,
                        server.adminPass, command)
                else:
                    out = sshtools.execute_remote_command_through_gateway(
                        gw_ip, gw_password, remote_ip, remote_password,
                        [command])
                resp = out.index(ip)
                if resp:
                    break
            except AttributeError:
                time.sleep(5)
                count += 1
        else:
            resp = False

        if gateway_server:
            msg = ('Can NOT ssh with IP {0} on server {1} through gateway '
                   'server {2} with IP {3}'.format(ip, server.id,
                        gateway_server.id, gw_ip))
        else:
            msg = ('ifconfig on server {0} missing IP {1} for '
                   'network {2}'.format(server.id, ip, network.id))
        self.assertTrue(resp, msg)

    def verify_ping(self, server, network, gateway_server=None):
        command = 'ifconfig'
        if gateway_server is None:
            out = sshtools.execute_remote_command(server.addresses.public.ipv4,
                                                  server.adminPass, command)
        else:
            gw_ip = gateway_server.addresses.public.ipv4
            gw_password = gateway_server.adminPass
            remote_ip = server.addresses.get_by_name(network.label).ipv4
            remote_password = server.adminPass
            out = sshtools.execute_remote_command_through_gateway(gw_ip,
                                                              gw_password,
                                                              remote_ip,
                                                              remote_password,
                                                              [command])
        ip = server.addresses.get_by_name(network.label).ipv4
        self.assertTrue(out.index(ip),
                        'Server IP is not in ifconfig list.')
