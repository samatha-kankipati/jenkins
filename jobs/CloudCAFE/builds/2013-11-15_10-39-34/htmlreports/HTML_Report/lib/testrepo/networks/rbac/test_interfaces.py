'''
@summary: Test Module for Networks Role Based Access Control
@copyright: Copyright (c) 2013 Rackspace US, Inc.
@author: leon0944
'''
from ccengine.common.constants.networks_constants import HTTPResponseCodes
from ccengine.common.decorators import attr
from testrepo.common.testfixtures.networks import NetworksRBACFixture


class TestInterfacesRBAC(NetworksRBACFixture):
    """Testing Server Network Virtual Interfaces with RBAC"""

    @classmethod
    def setUpClass(cls):
        """Class setUp - creating the test servers"""
        super(TestInterfacesRBAC, cls).setUpClass()

        # Creating Admin Server with Networks
        networks_list = ([cls.public_network.id, cls.private_network.id,
            cls.admin_network.id])
        resp = cls.create_rbac_server(networks=networks_list, role='admin')
        admin_server_id = resp.id
        admin_admin_pass = resp.adminPass

        # Creating Admin Server 02 without networks
        resp = cls.create_rbac_server(networks=[], role='admin')
        admin_server_id_02 = resp.id
        admin_admin_pass_02 = resp.adminPass

        # Creating Creator Server with Networks
        networks_list = ([cls.public_network.id, cls.private_network.id,
            cls.creator_network.id])
        resp = cls.create_rbac_server(networks=networks_list, role='creator')
        creator_server_id = resp.id
        creator_admin_pass = resp.adminPass

        # Creating Creator Server 02 without Networks
        resp = cls.create_rbac_server(networks=[], role='creator')
        creator_server_id_02 = resp.id
        creator_admin_pass_02 = resp.adminPass

        # waiting for the servers to be ACTIVE
        cls.admin_server = cls.wait_for_rbac_server(server_id=admin_server_id,
                                                    role='admin')
        cls.admin_server.adminPass = admin_admin_pass

        cls.admin_server_02 = cls.wait_for_rbac_server(
            server_id=admin_server_id_02, role='admin')
        cls.admin_server_02.adminPass = admin_admin_pass_02

        cls.creator_server = cls.wait_for_rbac_server(
            server_id=creator_server_id, role='creator')
        cls.creator_server.adminPass = creator_admin_pass

        cls.creator_server_02 = cls.wait_for_rbac_server(
            server_id=creator_server_id_02, role='creator')
        cls.creator_server_02.adminPass = creator_admin_pass_02

    @attr('rbac', 'positive')
    def test_admin_server_create_w_networks(self):
        """
        Asserting the server interfaces after the create with the admin role
        in the setUp
        """

        # Get Interfaces for assertions
        pub_interface = self.admin_networks_provider.get_public_interface(
            self.admin_server.id)
        pri_interface = self.admin_networks_provider.get_private_interface(
            self.admin_server.id)
        iso_interface = self.admin_networks_provider.get_interface(
            self.admin_server.id, self.admin_network.id)

        self.admin_helper.verify_interface(pub_interface, self.admin_server,
                                           self.public_network)
        self.admin_helper.verify_interface(pri_interface, self.admin_server,
                                           self.private_network)
        self.admin_helper.verify_interface(iso_interface, self.admin_server,
                                           self.admin_network)

        # Check the interfaces are in the server
        resp = self.admin_networks_provider.client.list_virtual_interfaces(
            self.admin_server.id)
        interface_list = resp.entity

        count_msg = ('Unexpected interface count on server{0}. Expected 3: '
            'Public, ServiceNet and Isolated Networks'.format(
                self.admin_server.id))
        self.assertEquals(len(interface_list), 3, count_msg)
        net_list = ([self.admin_network.id, self.public_network.id,
                     self.private_network.id])
        self.admin_helper.check_virtual_interface_response(interface_list,
            net_list, self.admin_server)

        # Verify server addresses
        pub_ipv4 = self.helper.assert_server_ips(self.admin_server,
            self.public_network.label, version=4)
        pub_ipv6 = self.helper.assert_server_ips(self.admin_server,
            self.public_network.label, version=6)
        pri_ipv4 = self.helper.assert_server_ips(self.admin_server,
            self.private_network.label, version=4)
        iso_ipv4 = self.helper.assert_server_ips(self.admin_server,
            self.admin_network.label, version=4)

        # Assert the expected IPv4s are on the server via ssh
        ip_list = [pub_ipv4, pub_ipv6, pri_ipv4, iso_ipv4]
        self.admin_helper.assert_ifconfig(self.admin_server, ips=ip_list,
                                          find=True)

    @attr('rbac', 'positive')
    def test_creator_server_create_w_networks(self):
        """
        Asserting the server interfaces after the create with the Creator
        role in the setUp
        """

        # Get Interfaces for assertions
        pub_interface = self.creator_networks_provider.get_public_interface(
            self.creator_server.id)
        pri_interface = self.creator_networks_provider.get_private_interface(
            self.creator_server.id)
        iso_interface = self.creator_networks_provider.get_interface(
            self.creator_server.id, self.creator_network.id)

        self.creator_helper.verify_interface(pub_interface,
            self.creator_server, self.public_network)
        self.creator_helper.verify_interface(pri_interface,
            self.creator_server, self.private_network)
        self.creator_helper.verify_interface(iso_interface,
            self.creator_server, self.creator_network)

        # Check the interfaces are in the server
        resp = self.creator_networks_provider.client.list_virtual_interfaces(
            self.creator_server.id)
        interface_list = resp.entity

        count_msg = ('Unexpected interface count on server{0}. Expected 3: '
            'Public, ServiceNet and Isolated Networks'.format(
                self.creator_server.id))
        self.assertEquals(len(interface_list), 3, count_msg)
        net_list = ([self.creator_network.id, self.public_network.id,
                     self.private_network.id])

        self.creator_helper.check_virtual_interface_response(interface_list,
            net_list, self.creator_server)

        # Get and verify server addresses
        pub_ipv4 = self.helper.assert_server_ips(self.creator_server,
            self.public_network.label, version=4)
        pub_ipv6 = self.helper.assert_server_ips(self.creator_server,
            self.public_network.label, version=6)
        pri_ipv4 = self.helper.assert_server_ips(self.creator_server,
            self.private_network.label, version=4)
        iso_ipv4 = self.helper.assert_server_ips(self.creator_server,
            self.creator_network.label, version=4)

        # Assert the expected IPv4s are on the server via ssh
        ip_list = [pub_ipv4, pub_ipv6, pri_ipv4, iso_ipv4]
        self.creator_helper.assert_ifconfig(self.creator_server, ips=ip_list,
                                            find=True)

    @attr('rbac', 'negative')
    def test_observer_server_create_w_networks(self):
        """Asserting the observer can NOT boot a server with a network"""

        # Get networks data dict for server create request
        networks_dict = self.networks_provider.get_server_network_dd(
            [self.admin_network.id])

        resp = self.observer_servers_provider.create_server_no_wait(
            networks=networks_dict)
        if hasattr(resp.entity, 'id'):
            self.admin_servers_to_delete.append(resp.entity.id)

        smsg = ('Unexpected API Response: {0} {1}\n'
                'Response Content: {2}\n'
                'Expected Response: {3}\n'
                'Details: RBAC Observer should NOT be able to create a '
                'server'.format(resp.status_code, resp.reason,
                                resp.content, self.unallowed_status))

        # assert the expected status code is given by the response
        self.assertEqual(resp.status_code, self.unallowed_status, smsg)

    @attr('rbac', 'positive')
    def test_admin_server_vifs_w_admin(self):
        """
        Testing admin server network attach and detach with initial test
        server without any networks
        """
        # Public Attach Call - will be able to ssh into server
        resp = self.admin_networks_provider.client.create_virtual_interface(
            self.admin_server_02.id, self.public_network.id)
        msg = 'Unable to attach network {0} to server {1}'.format(
            self.public_network.id, self.admin_server_02.id)
        self.assertEquals(resp.status_code, HTTPResponseCodes.CREATE_INTERFACE,
                          msg)

        # Get Public interface and network objects for assertions
        pub_interface = resp.entity[0]
        updated_server = self.admin_servers_provider.servers_client.\
            get_server(self.admin_server_02.id).entity
        updated_server.adminPass = self.admin_server_02.adminPass
        public_network = self.public_network

        # Assert Public interface data with network data
        self.admin_helper.verify_interface(pub_interface, updated_server,
                                           public_network)

        # Check the Public interface is in the server
        resp = self.admin_networks_provider.client.list_virtual_interfaces(
            updated_server.id)
        interface_list = resp.entity

        count_msg = ('Unexpected interface count on server {0}. Expected 1: '
            'Public Network'.format(self.admin_server_02.id))
        self.assertEquals(len(interface_list), 1, count_msg)

        self.admin_helper.verify_interface_in_list(pub_interface,
            interface_list, updated_server, public_network)
        self.admin_helper.verify_ifconfig(updated_server, public_network)

        # Verify Public server addresses
        pub_ipv4 = self.helper.assert_server_ips(updated_server,
            self.public_network.label, version=4)
        pub_ipv6 = self.helper.assert_server_ips(updated_server,
            self.public_network.label, version=6)

        # Assert the expected Public IPv4s are on the server via ssh
        ip_list = [pub_ipv4, pub_ipv6]
        self.helper.assert_ifconfig(updated_server, ips=ip_list, find=True)

        # Check the Public interface has a switch port in NVP
        if self.run_nvp:
            self.admin_helper.verify_nvp_interface(pub_interface,
                updated_server, public_network)

        # Private Attach Call
        resp = self.admin_networks_provider.client.create_virtual_interface(
            self.admin_server_02.id, self.private_network.id)
        msg = 'Unable to attach network {0} to server {1}'.format(
            self.private_network.id, self.admin_server_02.id)
        self.assertEquals(resp.status_code, HTTPResponseCodes.CREATE_INTERFACE,
                          msg)

        # Get Private interface and network objects for assertions
        pri_interface = resp.entity[0]
        updated_server = self.admin_servers_provider.servers_client.\
            get_server(self.admin_server_02.id).entity
        updated_server.adminPass = self.admin_server_02.adminPass
        private_network = self.private_network

        # Assert Private interface data with network data
        self.admin_helper.verify_interface(pri_interface, updated_server,
                                           private_network)

        # Check the Private interface is in the server
        resp = self.admin_networks_provider.client.list_virtual_interfaces(
            updated_server.id)
        interface_list = resp.entity

        count_msg = ('Unexpected interface count on server{0}. Expected 2: '
            'Public and ServiceNet Networks'.format(self.admin_server_02.id))
        self.assertEquals(len(interface_list), 2, count_msg)

        self.admin_helper.verify_interface_in_list(pri_interface,
            interface_list, updated_server, private_network)
        self.admin_helper.verify_ifconfig(updated_server, private_network)

        # Verify Private server addresses
        pri_ipv4 = self.helper.assert_server_ips(updated_server,
            self.private_network.label, version=4)

        # Assert the expected Private IPv4s are on the server via ssh
        ip_list = [pri_ipv4, pub_ipv4, pub_ipv6]
        self.helper.assert_ifconfig(updated_server, ips=ip_list, find=True)

        # Check the Private interface has a switch port in NVP
        if self.run_nvp:
            self.admin_helper.verify_nvp_interface(pri_interface,
                updated_server, private_network)

        # Isolated Attach Call
        resp = self.admin_networks_provider.client.create_virtual_interface(
            self.admin_server_02.id, self.admin_network.id)
        msg = 'Unable to attach network {0} to server {1}'.format(
            self.admin_network.id, self.admin_server_02.id)
        self.assertEquals(resp.status_code, HTTPResponseCodes.CREATE_INTERFACE,
                          msg)

        # Get Isolated interface and network objects for assertions
        iso_interface = resp.entity[0]
        updated_server = self.admin_servers_provider.servers_client.\
            get_server(self.admin_server_02.id).entity
        updated_server.adminPass = self.admin_server_02.adminPass
        isolated_network = self.admin_network

        # Assert Isolated interface data with network data
        self.admin_helper.verify_interface(iso_interface, updated_server,
                                           isolated_network)

        # Check the Isolated interface is in the server
        resp = self.admin_networks_provider.client.list_virtual_interfaces(
            updated_server.id)
        interface_list = resp.entity

        count_msg = ('Unexpected interface count on server{0}. Expected 3: '
            'Public, ServiceNet and Isolated Networks'.format(
                self.admin_server_02.id))
        self.assertEquals(len(interface_list), 3, count_msg)

        self.admin_helper.verify_interface_in_list(iso_interface,
            interface_list, updated_server, isolated_network)
        self.admin_helper.verify_ifconfig(updated_server, isolated_network)

        # Verify Isolated server addresses
        iso_ipv4 = self.helper.assert_server_ips(updated_server,
            isolated_network.label, version=4)

        # Assert the expected Isolated IPv4s are on the server via ssh
        ip_list = [iso_ipv4, pri_ipv4, pub_ipv4, pub_ipv6]
        self.helper.assert_ifconfig(updated_server, ips=ip_list, find=True)

        # Check the Public interface has a switch port in NVP
        if self.run_nvp:
            self.admin_helper.verify_nvp_interface(iso_interface,
                updated_server, isolated_network)

        # Isolated Detach Call
        resp = self.admin_networks_provider.client.delete_virtual_interface(
            updated_server.id, iso_interface.id)
        msg = 'Unable to delete VIF {0} from server {1}'.format(
            iso_interface.id, updated_server.id)
        self.assertEquals(resp.status_code, HTTPResponseCodes.DELETE_INTERFACE,
                          msg)

        # Check the Isolated interface was deleted from the server
        network_list = [public_network.id, private_network.id, \
                        isolated_network.id]
        self.admin_helper.check_virtual_interface_delete(updated_server.id,
            network_list, iso_interface.id)

        # Private Detach Call
        resp = self.admin_networks_provider.client.delete_virtual_interface(
            updated_server.id, pri_interface.id)
        msg = 'Unable to delete VIF {0} from server {1}'.format(
            pri_interface.id, updated_server.id)
        self.assertEquals(resp.status_code, HTTPResponseCodes.DELETE_INTERFACE,
                          msg)

        # Check the Private interface was deleted from the server
        network_list = [public_network.id, private_network.id]
        self.admin_helper.check_virtual_interface_delete(updated_server.id,
            network_list, pri_interface.id)

        # Public Detach Call - no ssh into server will be available
        resp = self.admin_networks_provider.client.delete_virtual_interface(
            updated_server.id, pub_interface.id)
        msg = 'Unable to delete VIF {0} from server {1}'.format(
            pub_interface.id, updated_server.id)
        self.assertEquals(resp.status_code, HTTPResponseCodes.DELETE_INTERFACE,
                          msg)

        # Check the Public interface was deleted from the server
        network_list = [public_network.id]
        self.admin_helper.check_virtual_interface_delete(updated_server.id,
            network_list, pub_interface.id)

    @attr('rbac', 'positive')
    def test_creator_server_vifs_w_creator(self):
        """Testing creator server network attach and detach with creator"""
        # Public Attach Call
        resp = self.creator_networks_provider.client.create_virtual_interface(
            self.creator_server_02.id, self.public_network.id)
        msg = 'Unable to attach network {0} to server {1}'.format(
            self.public_network.id, self.creator_server_02.id)
        self.assertEquals(resp.status_code, HTTPResponseCodes.CREATE_INTERFACE,
                          msg)

        # Get Public interface and network objects for assertions
        pub_interface = resp.entity[0]
        updated_server = self.creator_servers_provider.servers_client.\
            get_server(self.creator_server_02.id).entity
        updated_server.adminPass = self.creator_server_02.adminPass
        public_network = self.public_network

        # Assert Public interface data with network data
        self.creator_helper.verify_interface(pub_interface, updated_server,
                                             public_network)

        # Check the Public interface is in the server
        resp = self.creator_networks_provider.client.list_virtual_interfaces(
            updated_server.id)
        interface_list = resp.entity

        count_msg = ('Unexpected interface count on server{0}. Expected 1: '
            'Public Network'.format(self.creator_server_02.id))
        self.assertEquals(len(interface_list), 1, count_msg)

        self.creator_helper.verify_interface_in_list(pub_interface,
            interface_list, updated_server, public_network)
        self.creator_helper.verify_ifconfig(updated_server, public_network)

        # Verify Public server addresses
        pub_ipv4 = self.helper.assert_server_ips(updated_server,
            self.public_network.label, version=4)
        pub_ipv6 = self.helper.assert_server_ips(updated_server,
            self.public_network.label, version=6)

        # Assert the expected Public IPv4s are on the server via ssh
        ip_list = [pub_ipv4, pub_ipv6]
        self.helper.assert_ifconfig(updated_server, ips=ip_list, find=True)

        # Check the Public interface has a switch port in NVP
        if self.run_nvp:
            self.creator_helper.verify_nvp_interface(pub_interface,
                updated_server, public_network)

        # Private Attach Call
        resp = self.creator_networks_provider.client.create_virtual_interface(
            self.creator_server_02.id, self.private_network.id)
        msg = 'Unable to attach network {0} to server {1}'.format(
            self.private_network.id, self.creator_server_02.id)
        self.assertEquals(resp.status_code, HTTPResponseCodes.CREATE_INTERFACE,
                          msg)

        # Get Private interface and network objects for assertions
        pri_interface = resp.entity[0]
        updated_server = self.creator_servers_provider.servers_client.\
            get_server(self.creator_server_02.id).entity
        updated_server.adminPass = self.creator_server_02.adminPass
        private_network = self.private_network

        # Assert Private interface data with network data
        self.creator_helper.verify_interface(pri_interface, updated_server,
                                             private_network)

        # Check the Private interface is in the server
        resp = self.creator_networks_provider.client.list_virtual_interfaces(
            updated_server.id)
        interface_list = resp.entity

        count_msg = ('Unexpected interface count on server{0}. Expected 2: '
            'Public and ServiceNet Networks'.format(self.creator_server_02.id))
        self.assertEquals(len(interface_list), 2, count_msg)

        self.creator_helper.verify_interface_in_list(pri_interface,
            interface_list, updated_server, private_network)
        self.creator_helper.verify_ifconfig(updated_server, private_network)

        # Verify Private server addresses
        pri_ipv4 = self.helper.assert_server_ips(updated_server,
            self.private_network.label, version=4)

        # Assert the expected Private IPv4s are on the server via ssh
        ip_list = [pri_ipv4, pub_ipv4, pub_ipv6]
        self.helper.assert_ifconfig(updated_server, ips=ip_list, find=True)

        # Check the Private interface has a switch port in NVP
        if self.run_nvp:
            self.creator_helper.verify_nvp_interface(pri_interface,
                updated_server, private_network)

        # Isolated Attach Call
        resp = self.creator_networks_provider.client.create_virtual_interface(
            self.creator_server_02.id, self.creator_network.id)
        msg = 'Unable to attach network {0} to server {1}'.format(
            self.creator_network.id, self.creator_server_02.id)
        self.assertEquals(resp.status_code, HTTPResponseCodes.CREATE_INTERFACE,
                          msg)

        # Get Isolated interface and network objects for assertions
        iso_interface = resp.entity[0]
        updated_server = self.creator_servers_provider.servers_client.\
            get_server(self.creator_server_02.id).entity
        updated_server.adminPass = self.creator_server_02.adminPass
        isolated_network = self.creator_network

        # Assert Isolated interface data with network data
        self.creator_helper.verify_interface(iso_interface, updated_server,
                                             isolated_network)

        # Check the Isolated interface is in the server
        resp = self.creator_networks_provider.client.list_virtual_interfaces(
            updated_server.id)
        interface_list = resp.entity

        count_msg = ('Unexpected interface count on server{0}. Expected 3: '
            'Public, ServiceNet and Isolated Networks'.format(
                self.creator_server_02.id))
        self.assertEquals(len(interface_list), 3, count_msg)

        self.creator_helper.verify_interface_in_list(iso_interface,
            interface_list, updated_server, isolated_network)
        self.creator_helper.verify_ifconfig(updated_server, isolated_network)

        # Verify Isolated server addresses
        iso_ipv4 = self.helper.assert_server_ips(updated_server,
            isolated_network.label, version=4)

        # Assert the expected Isolated IPv4s are on the server via ssh
        ip_list = [iso_ipv4, pri_ipv4, pub_ipv4, pub_ipv6]
        self.helper.assert_ifconfig(updated_server, ips=ip_list, find=True)

        # Check the Public interface has a switch port in NVP
        if self.run_nvp:
            self.creator_helper.verify_nvp_interface(iso_interface,
                updated_server, isolated_network)

        # Creator Forbidden Detach Calls
        msg = 'Unexpected: Able to delete VIF {0} from server {1} with Creator'
        resp = self.creator_networks_provider.client.delete_virtual_interface(
            updated_server.id, iso_interface.id)
        self.assertEquals(resp.status_code, self.unallowed_status,
                          msg.format(iso_interface.id, updated_server.id))
        resp = self.creator_networks_provider.client.delete_virtual_interface(
            updated_server.id, pri_interface.id)
        self.assertEquals(resp.status_code, self.unallowed_status,
                          msg.format(pri_interface.id, updated_server.id))
        resp = self.creator_networks_provider.client.delete_virtual_interface(
            updated_server.id, pub_interface.id)
        self.assertEquals(resp.status_code, self.unallowed_status,
                          msg.format(pub_interface.id, updated_server.id))

        # Double check the interfaces are still in the server
        resp = self.creator_networks_provider.client.list_virtual_interfaces(
            self.creator_server_02.id)
        interface_list = resp.entity

        count_msg = ('Unexpected interface count on server{0}. Expected 3: '
            'Public, ServiceNet and Isolated Networks'.format(
            self.creator_server_02.id))
        self.assertEquals(len(interface_list), 3, count_msg)
        net_list = ([self.creator_network.id, self.public_network.id,
                     self.private_network.id])

        self.creator_helper.check_virtual_interface_response(interface_list,
            net_list, updated_server)

    @attr('rbac', 'negative')
    def test_servers_vifs_attach_w_observer(self):
        """Testing server network attach with RBAC Observer"""
        # Forbidden Public Network Attach Calls to Admin and Creator Servers
        msg = ('Unexpected: Able to attach {0} network {1} to server {2} with '
            'RBAC Observer')
        resp = self.observer_networks_provider.client.create_virtual_interface(
            self.admin_server_02.id, self.public_network.id)
        self.assertEquals(resp.status_code, self.unallowed_status,
            msg.format('Public', self.public_network.id,
                       self.admin_server_02.id))

        resp = self.observer_networks_provider.client.create_virtual_interface(
            self.creator_server_02.id, self.public_network.id)
        self.assertEquals(resp.status_code, self.unallowed_status,
            msg.format('Public', self.public_network.id,
                       self.creator_server_02.id))

        # Forbidden Private Network Attach Calls to Admin and Creator Servers
        resp = self.observer_networks_provider.client.create_virtual_interface(
            self.admin_server_02.id, self.private_network.id)
        self.assertEquals(resp.status_code, self.unallowed_status,
            msg.format('Private', self.private_network.id,
                       self.admin_server_02.id))

        resp = self.observer_networks_provider.client.create_virtual_interface(
            self.creator_server_02.id, self.public_network.id)
        self.assertEquals(resp.status_code, self.unallowed_status,
            msg.format('Public', self.public_network.id,
                       self.creator_server_02.id))

        # Forbidden Private Network Attach Calls to Admin and Creator Servers
        resp = self.observer_networks_provider.client.create_virtual_interface(
            self.admin_server_02.id, self.admin_network.id)
        self.assertEquals(resp.status_code, self.unallowed_status,
            msg.format('Isolated', self.admin_network.id,
                       self.admin_server_02.id))

        resp = self.observer_networks_provider.client.create_virtual_interface(
            self.creator_server_02.id, self.creator_network.id)
        self.assertEquals(resp.status_code, self.unallowed_status,
            msg.format('Isolated', self.creator_network.id,
                       self.creator_server_02.id))

    @attr('rbac', 'negative')
    def test_servers_vifs_dettach_w_observer(self):
        """Testing server network dettach with RBAC Observer"""

        msg = ('Unexpected: RBAC Observer able to dettach {0} network {1} '
            ' from server {2}')

        # Try to delete the isolated interface from an admin server
        resp = self.delete_interface(self.admin_server, self.admin_network,
                                     role='observer')
        self.assertEquals(resp.status_code, self.unallowed_status,
            msg.format('Isolated', self.admin_network.id,
                       self.admin_server.id))

        # Try to delete the isolated interface from a creator server
        resp = self.delete_interface(self.creator_server, self.creator_network,
                                     role='observer')
        self.assertEquals(resp.status_code, self.unallowed_status,
            msg.format('Isolated', self.creator_network.id,
                       self.creator_server.id))

        # Try to delete the public interface from an admin server
        resp = self.delete_interface(self.admin_server, self.public_network,
                                     role='observer')
        self.assertEquals(resp.status_code, self.unallowed_status,
            msg.format('Public', self.public_network.id, self.admin_server.id))

        # Try to delete the public interface from a creator server
        resp = self.delete_interface(self.creator_server, self.public_network,
                                     role='observer')
        self.assertEquals(resp.status_code, self.unallowed_status,
            msg.format('Public', self.public_network.id,
                       self.creator_server.id))

        # Try to delete the private interface from an admin server
        resp = self.delete_interface(self.admin_server, self.private_network,
                                     role='observer')
        self.assertEquals(resp.status_code, self.unallowed_status,
            msg.format('Private', self.private_network.id,
                       self.admin_server.id))

        # Try to delete the private interface from a creator server
        resp = self.delete_interface(self.creator_server, self.private_network,
                                     role='observer')
        self.assertEquals(resp.status_code, self.unallowed_status,
            msg.format('Private', self.private_network.id,
                       self.creator_server.id))

    def get_provider(self, provider, role):
        """
        @summary: Get a provider based on an RBAC role
        @param provider: provider type, for ex. servers, networks, etc.
        @type: str
        @param role: RBAC role, for ex. admin, creator, observer
        @type: str
        """
        provider_path = '{0}_{1}_provider'.format(role, provider)
        if hasattr(self, provider_path):
            provider = getattr(self, provider_path)
        else:
            self.fail('{0} provider unavailable for the {1} role'.format(
                      provider, role))
        return provider

    def delete_interface(self, server, network, role):
        """
        @summary: Delete an interface from a server by network and role
        @param server: server object
        @type: instance
        @param network: network object
        @type: instance
        @param role: RBAC user type, for ex. admin, creator, observer
        @type: str
        """
        provider = self.get_provider(provider='networks', role=role)
        interface = None
        if network.label == 'public':
            interface = provider.get_public_interface(server.id)
        elif network.label == 'private':
            interface = provider.get_private_interface(server.id)
        else:
            interface = provider.get_interface(server.id, network.id)

        msg = ('Unable to get server {0} interface for network {1} for the '
               ' {2} role'.format(server.id, network.id, role))
        self.assertIsNotNone(interface, msg)
        resp = provider.client.delete_virtual_interface(server.id,
                                                        interface.id)
        return resp
