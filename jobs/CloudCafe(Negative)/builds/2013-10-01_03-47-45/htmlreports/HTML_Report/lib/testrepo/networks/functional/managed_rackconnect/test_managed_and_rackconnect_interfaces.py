from IPy import IP
from testrepo.common.testfixtures.networks import \
    NetworksManagedRackConnectUsersFixture
from ccengine.common.decorators import attr
from ccengine.common.constants.networks_constants import HTTPResponseCodes
from ccengine.domain.types import NovaServerStatusTypes
import unittest2


class TestManagedRackConnectInterfaces(NetworksManagedRackConnectUsersFixture):

    @classmethod
    def setUpClass(cls):
        """Class setUp Creating test servers"""
        super(TestManagedRackConnectInterfaces, cls).setUpClass()
        # Create two managed test servers with public and private
        resp = cls.managed_servers_provider.create_server_no_wait()
        cls.managed_servers_to_delete.append(resp.entity.id)
        mserver = resp.entity

        # This one plus an isolated network
        networks = [cls.public_id, cls.private_id, cls.managed_network_id]
        nets_dd = cls.networks_provider.get_server_network_dd(networks)
        resp = cls.managed_servers_provider.create_server_no_wait(
            networks=nets_dd)
        cls.managed_servers_to_delete.append(resp.entity.id)
        mserver_w_iso = resp.entity

        # Create two rackconnect test servers with public and private
        resp = cls.rackconnect_servers_provider.create_server_no_wait()
        cls.rackconnect_servers_to_delete.append(resp.entity.id)
        rserver = resp.entity

        # This one plus an isolated network
        networks = ([cls.public_id, cls.private_id,
                    cls.rackconnect_network_id])
        nets_dd = cls.networks_provider.get_server_network_dd(networks)
        resp = cls.rackconnect_servers_provider.create_server_no_wait(
            networks=nets_dd)
        cls.rackconnect_servers_to_delete.append(resp.entity.id)
        rserver_w_iso = resp.entity

        # Wait for servers to be active
        resp = cls.managed_servers_provider.wait_for_server_status(
            mserver.id, NovaServerStatusTypes.ACTIVE)
        cls.mserver = resp.entity
        cls.mserver.adminPass = mserver.adminPass
        resp = cls.managed_servers_provider.wait_for_server_status(
            mserver_w_iso.id, NovaServerStatusTypes.ACTIVE)
        cls.mserver_w_iso = resp.entity
        cls.mserver_w_iso.adminPass = mserver_w_iso.adminPass

        resp = cls.rackconnect_servers_provider.wait_for_server_status(
            rserver.id, NovaServerStatusTypes.ACTIVE)
        cls.rserver = resp.entity
        cls.rserver.adminPass = rserver.adminPass
        resp = cls.rackconnect_servers_provider.wait_for_server_status(
            rserver_w_iso.id, NovaServerStatusTypes.ACTIVE)
        cls.rserver_w_iso = resp.entity
        cls.rserver_w_iso.adminPass = rserver_w_iso.adminPass

        # Expected create server status code response if Wafflehaus enabled
        cls.unallowed_status = HTTPResponseCodes.FORBIDDEN

    @attr('managed', 'positive', 'wafflehaus')
    def test_managed_isolated_interface_attach_detach(self):
        '''
        Managed user should be able to attach and detach an isolated
        virtual interface from a server with public and serviceNet
        '''
        # Attach Call
        r = self.managed_networks_provider.client.create_virtual_interface(
            self.mserver.id, self.managed_network_id)
        msg = 'Unable to attach network {0} to server {1}'.format(
            self.managed_network_id, self.mserver.id)
        self.assertEquals(r.status_code, HTTPResponseCodes.CREATE_INTERFACE,
                          msg)

        # Get interface and network objects for assertions
        new_interface = r.entity[0]
        updated_server = self.managed_servers_provider.servers_client.\
            get_server(self.mserver.id).entity
        updated_server.adminPass = self.mserver.adminPass
        network = self.managed_networks_provider.client.get_network(
            self.managed_network_id).entity

        # Assert interface data with network data
        self.managed_helper.verify_interface(new_interface, updated_server,
                                             network)

        # Check the interface is in the server
        r = self.managed_networks_provider.client.list_virtual_interfaces(
            updated_server.id)
        interface_list = r.entity
        msg = ('Unexpected interface count on server{0}. Expected 3: Public, '
               'ServiceNet and Isolated Networks'.format(self.mserver.id))
        self.assertEquals(len(interface_list), 3, msg)
        self.managed_helper.verify_interface_in_list(new_interface,
            interface_list, updated_server, network)
        self.managed_helper.verify_ifconfig(updated_server, network)

        # Verify server addresses
        pub = updated_server.addresses.get_by_name(self.public_label)
        pri = updated_server.addresses.get_by_name(self.private_label)
        iso = updated_server.addresses.get_by_name(network.label)

        amsg = 'Missing address for {0} network'
        self.assertIsNotNone(pub, amsg.format(self.public_label))
        self.assertIsNotNone(pri, amsg.format(self.private_label))
        self.assertIsNotNone(iso, amsg.format(network.label))

        ipmsg = 'Unexpected IPv{0} version on {1} network'
        try:
            self.assertEqual(IP(pub.ipv4).version(), 4, ipmsg.format(4,
                self.public_label))
            self.assertEqual(IP(pub.ipv6).version(), 6, ipmsg.format(6,
                self.public_label))
            self.assertEqual(IP(pri.ipv4).version(), 4, ipmsg.format(4,
                self.private_label))
            self.assertEqual(IP(iso.ipv4).version(), 4, ipmsg.format(4,
                network.label))
        except (ValueError, TypeError):
            self.fail('Managed Server IP address Error')

        # Assert the expected IPv4s are on the server via ssh
        ip_list = [pub.ipv4, pri.ipv4, iso.ipv4]
        self.helper.assert_ifconfig(updated_server, ips=ip_list, find=True)

        # Check the isolated interface has a switch port in NVP
        if self.run_nvp:
            self.managed_helper.verify_nvp_interface(new_interface,
                updated_server, network)

        # Detach Call
        r = self.managed_networks_provider.client.delete_virtual_interface(
            updated_server.id, new_interface.id)
        msg = 'Unable to delete VIF {0} from server {1}'.format(
            new_interface.id, updated_server.id)
        self.assertEquals(r.status_code, HTTPResponseCodes.DELETE_INTERFACE,
                          msg)

        # Check the interface was deleted from the server
        network_list = [network.id, self.public_id, self.private_id]
        self.managed_helper.check_virtual_interface_delete(updated_server.id,
            network_list, new_interface.id)

    @attr('managed', 'negative', 'wafflehaus')
    def test_managed_forbidden_public_interface_detach(self):
        '''
        Managed user should not be able to remove a public virtual interface
        from a server with public and serviceNet
        '''
        interface = self.managed_networks_provider.get_public_interface(
            self.mserver.id)
        r = self.managed_networks_provider.client.delete_virtual_interface(
            self.mserver.id, interface.id)
        self.assertEquals(r.status_code, self.unallowed_status,
            'Managed user should NOT be able to delete public interfaces')
        r = self.managed_networks_provider.get_public_interface(
            self.mserver.id)
        self.assertIsNotNone(r)

    @attr('managed', 'negative', 'wafflehaus')
    def test_managed_forbidden_public_interface_detach_w_iso(self):
        '''
        Managed user should not be able to remove a public virtual interface
        from a server with public, serviceNet and isolated
        '''
        interface = self.managed_networks_provider.get_public_interface(
            self.mserver_w_iso.id)
        r = self.managed_networks_provider.client.delete_virtual_interface(
            self.mserver_w_iso.id, interface.id)
        self.assertEquals(r.status_code, self.unallowed_status,
            'Managed user should NOT be able to delete public interfaces')
        r = self.managed_networks_provider.get_public_interface(
            self.mserver_w_iso.id)
        self.assertIsNotNone(r)

    @attr('managed', 'negative', 'wafflehaus')
    def test_managed_forbidden_private_interface_detach(self):
        '''
        Managed should not be able to remove a private virtual interface
        from a server with public and serviceNet
        '''
        interface = self.managed_networks_provider.get_private_interface(
            self.mserver.id)
        r = self.managed_networks_provider.client.delete_virtual_interface(
            self.mserver.id, interface.id)
        self.assertEquals(r.status_code, self.unallowed_status,
            'Managed user should NOT be able to delete private interfaces')
        r = self.managed_networks_provider.get_private_interface(
            self.mserver.id)
        self.assertIsNotNone(r)

    @attr('managed', 'negative', 'wafflehaus')
    def test_managed_forbidden_private_interface_detach_w_iso(self):
        '''
        Managed user should not be able to remove a private virtual interface
        from a server with public, serviceNet and isolated
        '''
        interface = self.managed_networks_provider.get_private_interface(
            self.mserver_w_iso.id)
        r = self.managed_networks_provider.client.delete_virtual_interface(
            self.mserver_w_iso.id, interface.id)
        self.assertEquals(r.status_code, self.unallowed_status,
            'Managed user should NOT be able to delete private interfaces')
        r = self.managed_networks_provider.get_private_interface(
            self.mserver_w_iso.id)
        self.assertIsNotNone(r)

    @attr('rackconnect', 'positive', 'wafflehaus')
    def test_rackconnect_isolated_interface_attach_detach(self):
        '''
        Rackconnect user should be able to attach and detach an isolated
        virtual interface from a server with public and serviceNet
        '''
        # Attach Call
        r = self.rackconnect_networks_provider.client.create_virtual_interface(
            self.rserver.id, self.rackconnect_network_id)
        msg = 'Unable to attach network {0} to server {1}'.format(
            self.rackconnect_network_id, self.rserver.id)
        self.assertEquals(r.status_code, HTTPResponseCodes.CREATE_INTERFACE,
                          msg)

        # Get interface and network objects for assertions
        new_interface = r.entity[0]
        updated_server = self.rackconnect_servers_provider.servers_client.\
            get_server(self.rserver.id).entity
        updated_server.adminPass = self.rserver.adminPass
        network = self.rackconnect_networks_provider.client.get_network(
            self.rackconnect_network_id).entity

        # Assert interface data with network data
        self.rackconnect_helper.verify_interface(new_interface, updated_server,
                                                 network)

        # Check the interface is in the server
        r = self.rackconnect_networks_provider.client.list_virtual_interfaces(
            updated_server.id)
        interface_list = r.entity
        msg = ('Unexpected interface count on server{0}. Expected 3: Public, '
               'ServiceNet and Isolated Networks'.format(self.rserver.id))
        self.assertEquals(len(interface_list), 3, msg)
        self.rackconnect_helper.verify_interface_in_list(new_interface,
            interface_list, updated_server, network)

        # Verify server addresses
        pub = updated_server.addresses.get_by_name(self.public_label)
        pri = updated_server.addresses.get_by_name(self.private_label)
        iso = updated_server.addresses.get_by_name(network.label)

        amsg = 'Missing address for {0} network'
        self.assertIsNotNone(pub, amsg.format(self.public_label))
        self.assertIsNotNone(pri, amsg.format(self.private_label))
        self.assertIsNotNone(iso, amsg.format(network.label))

        ipmsg = 'Unexpected IPv{0} version on {1} network'
        try:
            err_msg = 'Public IPv4'
            self.assertEqual(IP(pub.ipv4).version(), 4, ipmsg.format(4,
                self.public_label))
            err_msg = 'Public IPv6'
            self.assertEqual(IP(pub.ipv6).version(), 6, ipmsg.format(6,
                self.public_label))
            err_msg = 'ServiceNet IPv4'
            self.assertEqual(IP(pri.ipv4).version(), 4, ipmsg.format(4,
                self.private_label))
            err_msg = 'Isolated IPv4'
            self.assertEqual(IP(iso.ipv4).version(), 4, ipmsg.format(4,
                network.label))
        except (ValueError, TypeError):
            self.fail('Rackconnect Server {0} {1} address Error'.format(
                self.rserver.id, err_msg))

        # Assert the expected IPv4s are on the server via ssh
        ip_list = [pub.ipv4, pri.ipv4, iso.ipv4]
        self.helper.assert_ifconfig(updated_server, ips=ip_list, find=True)

        # Check the isolated interface has a switch port in NVP
        if self.run_nvp:
            self.rackconnect_helper.verify_nvp_interface(new_interface,
                updated_server, network)

        # Detach Call
        r = self.rackconnect_networks_provider.client.delete_virtual_interface(
            updated_server.id, new_interface.id)
        msg = 'Unable to delete VIF {0} from server {1}'.format(
            new_interface.id, updated_server.id)
        self.assertEquals(r.status_code, HTTPResponseCodes.DELETE_INTERFACE,
                          msg)

        # Check the interface was deleted from the server
        network_list = [network.id, self.public_id, self.private_id]
        self.rackconnect_helper.check_virtual_interface_delete(
            updated_server.id, network_list, new_interface.id)

    @attr('rackconnect', 'negative', 'wafflehaus')
    def test_rackconnect_forbidden_public_interface_detach(self):
        '''
        Rackconnect user should not be able to remove a public virtual
        interface from a server with public and serviceNet
        '''
        interface = self.rackconnect_networks_provider.get_public_interface(
            self.rserver.id)
        r = self.rackconnect_networks_provider.client.delete_virtual_interface(
            self.rserver.id, interface.id)
        self.assertEquals(r.status_code, self.unallowed_status,
            'rackconnect user should NOT be able to delete public interfaces')
        r = self.rackconnect_networks_provider.get_public_interface(
            self.rserver.id)
        self.assertIsNotNone(r)

    @attr('rackconnect', 'negative', 'wafflehaus')
    def test_rackconnect_forbidden_public_interface_detach_w_iso(self):
        '''
        Rackconnect user should not be able to remove a public virtual
        interface from a server with public, serviceNet and isolated
        '''
        interface = self.rackconnect_networks_provider.get_public_interface(
            self.rserver_w_iso.id)
        r = self.rackconnect_networks_provider.client.delete_virtual_interface(
            self.rserver_w_iso.id, interface.id)
        self.assertEquals(r.status_code, self.unallowed_status,
            'rackconnect user should NOT be able to delete public interfaces')
        r = self.rackconnect_networks_provider.get_public_interface(
            self.rserver_w_iso.id)
        self.assertIsNotNone(r)

    @attr('rackconnect', 'negative', 'wafflehaus')
    def test_rackconnect_forbidden_private_interface_detach(self):
        '''
        Rackconnect should not be able to remove a private virtual interface
        from a server with public and serviceNet
        '''
        interface = self.rackconnect_networks_provider.get_private_interface(
            self.rserver.id)
        r = self.rackconnect_networks_provider.client.delete_virtual_interface(
            self.rserver.id, interface.id)
        self.assertEquals(r.status_code, self.unallowed_status,
            'rackconnect user should NOT be able to delete private interfaces')
        r = self.rackconnect_networks_provider.get_private_interface(
            self.rserver.id)
        self.assertIsNotNone(r)

    @attr('rackconnect', 'negative', 'wafflehaus')
    def test_rackconnect_forbidden_private_interface_detach_w_iso(self):
        '''
        Rackconnect user should not be able to remove a private virtual
        interface from a server with public, serviceNet and isolated
        '''
        interface = self.rackconnect_networks_provider.get_private_interface(
            self.rserver_w_iso.id)
        r = self.rackconnect_networks_provider.client.delete_virtual_interface(
            self.rserver_w_iso.id, interface.id)
        self.assertEquals(r.status_code, self.unallowed_status,
            'rackconnect user should NOT be able to delete private interfaces')
        r = self.rackconnect_networks_provider.get_private_interface(
            self.rserver_w_iso.id)
        self.assertIsNotNone(r)
