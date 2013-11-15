from testrepo.common.testfixtures.networks import NetworksTestFixture
from ccengine.domain.types import NovaServerStatusTypes
from ccengine.common.exceptions import compute as exceptions
import unittest2
from ccengine.common.decorators import attr
import time
import ccengine.common.tools.datagen as datagen
from aiclib.nvp import ResourceNotFound
from ccengine.common.constants.networks_constants import Constants


class TestNetworks(NetworksTestFixture):

    NETWORK_SERVER_LIMIT = 3

    @attr('smoke', 'positive', 'cc_unittest')
    def test_create_network(self):
        '''Create, delete, and get details of a network.'''
        #not randomizing this since the cidr will be changed by the api if the
        #cidr sent in does not make sense. Don't want to import a library.
        #(example 192.1.1.250/30 = 192.1.1.248/30)
#        cidr = datagen.random_cidr()
        cidr = '192.1.1.248/30'
        network_label = datagen.random_string('crud_network')
        r = self.networks_provider.client.create_network(cidr=cidr,
                                                         label=network_label)
        network = r.entity
        self.assertEquals(r.status_code, 200)
        self.networks_to_delete.append(network.id)
        self.assertEquals(network.cidr, cidr,
                          'CIDR does not match what was sent')
        self.assertEquals(network.label, network_label,
                          'Label does not match what was sent')
        if self.run_nvp:
            nvp_switch = self.nvp_provider.aic_client.get_lswitch(network.id)
            self.assertEquals(nvp_switch['display_name'], network.label)
        r = self.networks_provider.client.list_networks()
        network_list = r.entity
        self.assertEquals(r.status_code, 200)
        self.assertIn(network, network_list)
        r = self.networks_provider.client.get_network(network.id)
        get_network = r.entity
        self.assertEquals(r.status_code, 200)
        self.assertEquals(get_network, network)
        self.assertEquals(get_network.cidr, cidr,
                          'CIDR does not match what was sent')
        self.assertEquals(get_network.label, network_label,
                          'Label does not match what was sent')
        r = self.networks_provider.client.delete_network(network.id)
        self.assertEquals(r.status_code, 202)
        if self.run_nvp:
            nvp_switch = None
            try:
                nvp_switch = self.nvp_provider.aic_client.get_lswitch(
                    network.id)
            except ResourceNotFound:
                pass
            self.assertIsNone(nvp_switch,
                              'NVP API still shows switch is alive.')
        r = self.networks_provider.client.list_networks()
        network_list = r.entity
        self.assertEquals(r.status_code, 200)
        self.assertNotIn(network, network_list)
        r = self.networks_provider.client.get_network(network.id)
        network = r.entity
        self.assertEquals(r.status_code, 404)

    @attr('smoke', 'positive', 'test')
    def test_public_and_private_networks_correct(self):
        '''Verify public and private networks have correct IDs'''
        networks = self.networks_provider.client.list_networks().entity
        public = [n for n in networks if n.id == Constants.PUBLIC_NETWORK_ID]
        private = [n for n in networks if n.id == Constants.PRIVATE_NETWORK_ID]
        self.assertNotEqual(len(public), 0,
                            'Public network did not have correct ID.')
        self.assertNotEqual(len(private), 0,
                            'Private network did not have correct ID.')
        self.assertEquals(len(public), 1,
                          'There are more than 1 networks with public ID.')
        self.assertEquals(len(private), 1,
                          'There are more than 1 networks with private ID.')

    @attr('smoke', 'positive')
    def test_create_ipv6_network(self):
        '''Create IPv6 network, delete, and get details of a network.'''
        cidr = '1234::fff8/126'
        network_label = datagen.random_string('ipv6_crud_network')
        r = self.networks_provider.client.create_network(cidr=cidr,
                                                         label=network_label)
        network = r.entity
        self.assertEquals(r.status_code, 200)
        self.networks_to_delete.append(network.id)
        self.assertEquals(network.cidr, cidr,
                          'CIDR does not match what was sent')
        self.assertEquals(network.label, network_label,
                          'Label does not match what was sent')
        if self.run_nvp:
            nvp_switch = self.nvp_provider.aic_client.get_lswitch(network.id)
            self.assertEquals(nvp_switch['display_name'], network.label)
        r = self.networks_provider.client.list_networks()
        network_list = r.entity
        self.assertEquals(r.status_code, 200)
        self.assertIn(network, network_list)
        r = self.networks_provider.client.get_network(network.id)
        get_network = r.entity
        self.assertEquals(r.status_code, 200)
        self.assertEquals(get_network, network)
        self.assertEquals(get_network.cidr, cidr,
                          'CIDR does not match what was sent')
        self.assertEquals(get_network.label, network_label,
                          'Label does not match what was sent')
        r = self.networks_provider.client.delete_network(network.id)
        self.assertEquals(r.status_code, 202)
        if self.run_nvp:
            nvp_switch = None
            try:
                nvp_switch = self.nvp_provider.aic_client.get_lswitch(
                    network.id)
            except ResourceNotFound:
                pass
            self.assertIsNone(nvp_switch,
                'NVP API still shows switch is alive.')
        r = self.networks_provider.client.list_networks()
        network_list = r.entity
        self.assertEquals(r.status_code, 200)
        self.assertNotIn(network, network_list)
        r = self.networks_provider.client.get_network(network.id)
        network = r.entity
        self.assertEquals(r.status_code, 404)

    @attr('smoke', 'positive')
    def test_attach_server_to_ipv4_network(self):
        '''Create IPv4 network and attach server to the network.'''
        cidr = '192.1.1.248/30'
        network_label = datagen.random_string('ipv4_network')
        r = self.networks_provider.client.create_network(cidr=cidr,
                                                         label=network_label)
        network = r.entity
        self.assertEquals(r.status_code, 200)
        self.networks_to_delete.append(network.id)
        if self.run_nvp:
            nvp_switch = self.nvp_provider.aic_client.get_lswitch(network.id)
            self.assertEquals(nvp_switch['display_name'], network.label)
        networks = [{"uuid": network.id}]
        r = self.servers_provider.create_active_server(networks=networks)
        self.servers_to_delete.append(r.entity.id)
        server = r.entity
        self.assertEquals(server.status, NovaServerStatusTypes.ACTIVE)
        net_addrs = server.addresses.get_by_name(network.label)
        self.assertIsNotNone(net_addrs)
        if self.run_nvp:
            switch_ports = self.nvp_provider.aic_client.\
                list_lswitch_ports(network.id)
            self.assertEquals(len(switch_ports['results']), 1)
        #TODO: Enable below when bugs are fixed
#        allowed_ips = [ip['ip_address'] for ip in \
#                       switch_ports['results'][0]['allowed_address_pairs']]
#        self.assertIn(net_addrs.ipv4, allowed_ips,
#                      'NVP does not have address as allowed address.')
#        self.assertIsNotNone(switch_ports['results'][0].get('queue_uuid'),
#                             'NVP did not set up QoS appropriately.')
#        self.assertNotEquals(len(switch_ports['results'][0]['queue_uuid']), 0,
#                             'NVP did not set up QoS appropriately.')

    @attr('smoke', 'positive')
    def test_attach_server_to_ipv6_network(self):
        '''Create IPv6 network and attach server to the network.'''
        cidr = '1234::/126'
        network_label = datagen.random_string('ipv6_network')
        r = self.networks_provider.client.create_network(cidr=cidr,
                                                         label=network_label)
        network = r.entity
        self.assertEquals(r.status_code, 200)
        self.networks_to_delete.append(network.id)
        if self.run_nvp:
            nvp_switch = self.nvp_provider.aic_client.get_lswitch(network.id)
            self.assertEquals(nvp_switch['display_name'], network.label)
            nvp_switch = self.nvp_provider.aic_client.get_lswitch(network.id)
            self.assertEquals(nvp_switch['display_name'], network.label)
        networks = [{"uuid": network.id}]
        r = self.servers_provider.create_active_server(networks=networks)
        self.servers_to_delete.append(r.entity.id)
        server = r.entity
        self.assertEquals(server.status, NovaServerStatusTypes.ACTIVE)
        self.assertIsNotNone(server.addresses.get_by_name(network.label))
        if self.run_nvp:
            switch_ports = self.nvp_provider.aic_client.\
                list_lswitch_ports(network.id)
            self.assertEquals(len(switch_ports['results']), 1)
        #TODO: Enable below when bugs are fixed
#        allowed_ips = [ip['ip_address'] for ip in \
#                       switch_ports['results'][0]['allowed_address_pairs']]
#        self.assertIn(net_addrs.ipv4, allowed_ips,
#                      'NVP does not have address as allowed address.')
#        self.assertIsNotNone(switch_ports['results'][0].get('queue_uuid'),
#                             'NVP did not set up QoS appropriately.')
#        self.assertNotEquals(len(switch_ports['results'][0]['queue_uuid']), 0,
#                             'NVP did not set up QoS appropriately.')

    @attr('negative')
    def test_cannot_delete_private_and_public_networks(self):
        '''Verify a user cannot delete private and public networks.'''
        public = self.networks_provider.get_public_network()
        r = self.networks_provider.client.delete_network(public.id)
        self.assertEquals(r.status_code, 404)
        private = self.networks_provider.get_private_network()
        r = self.networks_provider.client.delete_network(private.id)
        self.assertEquals(r.status_code, 404)
        self.assertIsNotNone(self.networks_provider.get_private_network())
        self.assertIsNotNone(self.networks_provider.get_public_network())

    @attr('negative')
    def test_allocation_of_more_than_max_ips(self):
        '''Cannot allocate more IPs than the cidr range specifies.'''
        #this only allows 2 IPs since the 2 others are used internally
        cidr = datagen.random_cidr(ip_pattern="*.*.*.0", mask=30)
        label = datagen.random_string('max_ips_network')
        r = self.networks_provider.client.create_network(cidr=cidr,
                                                         label=label)
        small_network = r.entity
        self.networks_to_delete.append(small_network.id)
        if self.run_nvp:
            nvp_switch = self.nvp_provider.aic_client.get_lswitch(
                small_network.id)
            self.assertEquals(nvp_switch['display_name'], small_network.label)
        server1_name = datagen.random_string('max_ips_server1')
        server1_networks = [{'uuid':small_network.id}]
        server2_name = datagen.random_string('max_ips_server2')
        server2_networks = [{'uuid':small_network.id}]
        server3_name = datagen.random_string('max_ips_server3')
        server3_networks = [{'uuid':small_network.id}]
        r = self.servers_provider.servers_client.create_server(
                                 name=server1_name,
                                 image_ref=self.config.compute_api.image_ref,
                                 flavor_ref=self.config.compute_api.flavor_ref,
                                 networks=server1_networks)
        server1 = r.entity
        r = self.servers_provider.servers_client.create_server(
                                 name=server2_name,
                                 image_ref=self.config.compute_api.image_ref,
                                 flavor_ref=self.config.compute_api.flavor_ref,
                                 networks=server2_networks)
        server2 = r.entity
        self.servers_provider.wait_for_server_status(server1.id,
                                                NovaServerStatusTypes.ACTIVE)
        self.servers_provider.wait_for_server_status(server2.id,
                                                NovaServerStatusTypes.ACTIVE)
        self.servers_to_delete.append(server1.id)
        self.servers_to_delete.append(server2.id)
        if self.run_nvp:
            switch_ports = self.nvp_provider.aic_client.\
                list_lswitch_ports(small_network.id)
            self.assertEquals(len(switch_ports['results']), 2)
        r = self.servers_provider.servers_client.create_server(
                                 name=server3_name,
                                 image_ref=self.config.compute_api.image_ref,
                                 flavor_ref=self.config.compute_api.flavor_ref,
                                 networks=server3_networks)
        server3 = r.entity
        self.servers_to_delete.append(server3.id)
        self.servers_provider.wait_for_server_status(server3.id,
                                                NovaServerStatusTypes.ERROR)
        r = self.servers_provider.servers_client.get_server(server3.id)
        server3 = r.entity
        self.assertEquals(server3.status.lower(),
                          NovaServerStatusTypes.ERROR.lower())
        if self.run_nvp:
            switch_ports = self.nvp_provider.aic_client.\
                list_lswitch_ports(small_network.id)
            self.assertEquals(len(switch_ports['results']), 2)

    @attr('positive')
    def test_add_server_to_network_after_ip_has_been_released(self):
        '''Removing a server from a network releases the IP'''
        cidr = '172.99.10.100/30'
        label = datagen.random_string('no_ips_network')
        r = self.networks_provider.client.create_network(cidr=cidr,
                                                         label=label)
        small_network = r.entity
        self.networks_to_delete.append(small_network.id)
        server1_name = datagen.random_string('net_no_space_server1')
        server1_networks = [{'uuid':small_network.id}]
        server2_name = datagen.random_string('net_no_space_server2')
        server2_networks = [{'uuid':small_network.id}]
        r = self.servers_provider.servers_client.create_server(
                                 name=server1_name,
                                 image_ref=self.config.compute_api.image_ref,
                                 flavor_ref=self.config.compute_api.flavor_ref,
                                 networks=server1_networks)
        server1 = r.entity
        r = self.servers_provider.servers_client.create_server(
                                 name=server2_name,
                                 image_ref=self.config.compute_api.image_ref,
                                 flavor_ref=self.config.compute_api.flavor_ref,
                                 networks=server2_networks)
        server2 = r.entity
        self.servers_to_delete.append(server1.id)
        self.servers_to_delete.append(server2.id)
        self.servers_provider.wait_for_server_status(server1.id,
                                              NovaServerStatusTypes.ACTIVE)
        self.servers_provider.wait_for_server_status(server2.id,
                                              NovaServerStatusTypes.ACTIVE)
        r = self.servers_provider.servers_client.get_server(server1.id)
        server1 = r.entity
        r = self.servers_provider.servers_client.get_server(server2.id)
        server2 = r.entity
        ip1 = server1.addresses.get_by_name(small_network.label).ipv4
        ip2 = server2.addresses.get_by_name(small_network.label).ipv4
        ip_list = [ip1, ip2]
        self.assertIn('172.99.10.101', ip_list)
        self.assertIn('172.99.10.102', ip_list)
        r = self.servers_provider.servers_client.delete_server(server2.id)
        self.assertEquals(r.status_code, 204, 'Server deletion problem.')
        self.servers_to_delete.pop()
        #We don't want the first server or the network to get cleaned up.
        self.servers_to_delete.pop()
        self.networks_to_delete.pop()
        import pickle
        import os
        pickle_data = \
            {'test_add_server_to_network_after_ip_has_been_released':
             {'network_id': small_network.id,
              'deleted_ip': ip2,
              'server1_id': server1.id}}
        output = open('/'.join([os.getcwd(), 'data.pkl']), 'wb')
        pickle.dump(pickle_data, output)
        output.close()

    @attr('negative')
    def test_cannot_delete_network_with_server_still_attached(self):
        '''Can only delete a network that has no servers attached.'''
        cidr = datagen.random_cidr(ip_pattern="*.*.*.0", mask=24)
        label = datagen.random_string('still_attached_network')
        r = self.networks_provider.client.create_network(cidr=cidr,
                                                         label=label)
        test_net = r.entity
        self.networks_to_delete.append(test_net.id)
        if self.run_nvp:
            nvp_switch = self.nvp_provider.aic_client.get_lswitch(test_net.id)
            self.assertEquals(nvp_switch['display_name'], test_net.label)
        server1_name = datagen.random_string('still_attached_server1')
        server1_networks = [{'uuid':test_net.id}]
        r = self.servers_provider.create_active_server(name=server1_name,
                                                    networks=server1_networks)
        server1 = r.entity
        self.servers_to_delete.append(server1.id)
        if self.run_nvp:
            switch_ports = self.nvp_provider.aic_client.\
                list_lswitch_ports(test_net.id)
            self.assertEquals(len(switch_ports['results']), 1)
        r = self.networks_provider.client.delete_network(test_net.id)
        self.assertEquals(r.status_code, 403)
        r = self.servers_provider.servers_client.delete_server(server1.id)
        self.assertEquals(r.status_code, 204)
        r = self.servers_provider.servers_client.get_server(server1.id)
        count = 0
        while count < 60:
            time.sleep(2)
            count += 1
            try:
                r = self.servers_provider.servers_client.get_server(server1.id)
            except exceptions.ItemNotFound:
                self.servers_to_delete.pop()
                break
        if self.run_nvp:
            switch_ports = self.nvp_provider.aic_client.\
                list_lswitch_ports(test_net.id)
            self.assertEquals(len(switch_ports['results']), 0)
        r = self.networks_provider.client.delete_network(test_net.id)
        self.assertEquals(r.status_code, 202)
        self.networks_to_delete.pop()
        if self.run_nvp:
            nvp_switch = None
            try:
                nvp_switch = self.nvp_provider.aic_client.get_lswitch(
                    test_net.id)
            except ResourceNotFound:
                pass
            self.assertIsNone(nvp_switch,
                'NVP API still shows switch is alive.')

    @unittest2.skip('Need to use account that has a low limit.')
    @attr('positive')
    def test_attach_more_servers_than_limit(self):
        '''Cannot attach more servers than the server limit.'''
        cidr = datagen.random_cidr(ip_pattern="*.*.*.0", mask=24)
        network_label = datagen.random_string('servers_per_net_limit_network')
        r = self.alt_networks_provider.client.create_network(cidr=cidr,
                                                         label=network_label)
        self.alt_networks_to_delete.append(r.entity.id)
        test_net = r.entity
        server1_name = datagen.random_string('servers_per_net_limit_server1')
        server1_networks = [{'uuid':test_net.id},
                {'uuid': self.alt_networks_provider.get_public_network().id},
                {'uuid': self.alt_networks_provider.get_private_network().id}]
        servers_created = []
        #TODO: Find a way to get the limit from the API instead of having it
        #hard coded
        for _ in range(0, self.NETWORK_SERVER_LIMIT):
            r = self.alt_servers_provider.servers_client.create_server(
                                 name=server1_name,
                                 image_ref=self.config.compute_api.image_ref,
                                 flavor_ref=self.config.compute_api.flavor_ref,
                                 networks=server1_networks)
            self.alt_servers_to_delete.append(r.entity.id)
            servers_created.append(r.entity)
        for server in servers_created:
            r = self.alt_servers_provider.wait_for_server_status(server.id,
                                                  NovaServerStatusTypes.ACTIVE)
        name = datagen.random_string('over_limit_server')
        r = self.alt_servers_provider.create_active_server(name,
                                                    networks=server1_networks)
        self.alt_servers_to_delete.append(r.entity.id)
        self.assertEquals(r.entity.status, NovaServerStatusTypes.ERROR,
                          "Account used: %s" %
                          self.config.auth.alt_username)

    @attr('smoke', 'negative')
    def test_ipv4_cidr_prefix_length_greater_than_30(self):
        '''Cannot use ipv4 cidr prefix length greater than 30.'''
        cidr = '172.200.33.12/31'
        network_label = datagen.random_string('cidr_31_network')
        r = self.networks_provider.client.create_network(cidr=cidr,
                                                         label=network_label)
        if r.entity is not None:
            self.networks_to_delete.append(r.entity.id)
        self.assertFalse(r.ok,
                "Shouldn't be able to create network with cidr prefix of 31.")
        cidr = '172.200.33.12/32'
        network_label = datagen.random_string('cidr_32_network')
        r = self.networks_provider.client.create_network(cidr=cidr,
                                                         label=network_label)
        if r.entity is not None:
            self.networks_to_delete.append(r.entity.id)
        self.assertFalse(r.ok,
                "Shouldn't be able to create network with cidr prefix of 32.")

    @attr('smoke', 'negative')
    def test_ipv6_cidr_prefix_length_greater_than_126(self):
        '''Cannot use ipv6 cidr prefix length greater than 126.'''
        cidr = '1234::/127'
        network_label = datagen.random_string('cidr_127_network')
        r = self.networks_provider.client.create_network(cidr=cidr,
                                                         label=network_label)
        if r.entity is not None:
            self.networks_to_delete.append(r.entity.id)
        self.assertFalse(r.ok,
                "Shouldn't be able to create network with cidr prefix of 127.")
        cidr = '1234::/128'
        network_label = datagen.random_string('cidr_128_network')
        r = self.networks_provider.client.create_network(cidr=cidr,
                                                         label=network_label)
        if r.entity is not None:
            self.networks_to_delete.append(r.entity.id)
        self.assertFalse(r.ok,
                "Shouldn't be able to create network with cidr prefix of 128.")

    @attr('smoke', 'positive')
    def test_standard_user_only_networks_specified_are_created(self):
        '''As standard user, only networks specified on create are configured.
        '''
        cidr = datagen.random_cidr(ip_pattern="*.*.*.0", mask=24)
        network_label = datagen.random_string('only_networks_specified')
        r = self.networks_provider.client.create_network(cidr=cidr,
                                                         label=network_label)
        test_net = r.entity
        self.networks_to_delete.append(test_net.id)
        public_net = self.networks_provider.get_public_network()
        private_net = self.networks_provider.get_private_network()
        networks = [{'uuid': test_net.id},
                    {'uuid': private_net.id}]
        server_name = datagen.random_string('only_networks_specified')
        r = self.servers_provider.create_active_server(name=server_name,
                                                       networks=networks)
        self.servers_to_delete.append(r.entity.id)
        addresses = r.entity.addresses
        self.assertIsNotNone(addresses.get_by_name(test_net.label))
        self.assertIsNotNone(addresses.get_by_name(private_net.label))
        self.assertIsNone(addresses.get_by_name(public_net.label))

    @attr('smoke', 'negative')
    def test_create_network_with_invalid_ip(self):
        '''Verify invalid IP cannot be used to create network.'''
        name = datagen.random_string('invalid_ip_network')
        ip = '1111'
        r = self.networks_provider.client.create_network(cidr=ip, label=name)
        if r.entity is not None:
            self.networks_to_delete.append(r.entity.id)
        self.assertEquals(r.status_code, 400,
                          '%s should not be allowed as cidr' % ip)
        ip = '111111111111'
        r = self.networks_provider.client.create_network(cidr=ip, label=name)
        if r.entity is not None:
            self.networks_to_delete.append(r.entity.id)
        self.assertEquals(r.status_code, 400,
                          '%s should not be allowed as cidr' % ip)
        ip = '270.10.10.10'
        r = self.networks_provider.client.create_network(cidr=ip, label=name)
        if r.entity is not None:
            self.networks_to_delete.append(r.entity.id)
        self.assertEquals(r.status_code, 400,
                          '%s should not be allowed as cidr' % ip)
        ip = '270.10.10.10/28'
        r = self.networks_provider.client.create_network(cidr=ip, label=name)
        if r.entity is not None:
            self.networks_to_delete.append(r.entity.id)
        self.assertEquals(r.status_code, 400,
                          '%s should not be allowed as cidr' % ip)
        ip = '1111/30'
        r = self.networks_provider.client.create_network(cidr=ip, label=name)
        if r.entity is not None:
            self.networks_to_delete.append(r.entity.id)
        self.assertEquals(r.status_code, 400,
                          '%s should not be allowed as cidr' % ip)
        ip = '111111111111/30'
        r = self.networks_provider.client.create_network(cidr=ip, label=name)
        if r.entity is not None:
            self.networks_to_delete.append(r.entity.id)
        self.assertEquals(r.status_code, 400,
                          '%s should not be allowed as cidr.' % ip)

    @attr('smoke', 'negative')
    def test_create_network_with_invalid_cidr_prefix(self):
        '''Verify invalid CIDR prefix cannot be used to create network.'''
        name = datagen.random_string('invalid_cidr_network')
        ip = '1.1.1.1/33'
        r = self.networks_provider.client.create_network(cidr=ip, label=name)
        if r.entity is not None:
            self.networks_to_delete.append(r.entity.id)
        self.assertEquals(r.status_code, 400,
                          '%s should not be allowed as cidr' % ip)
        ip = '1.1.1.1/-1'
        r = self.networks_provider.client.create_network(cidr=ip, label=name)
        if r.entity is not None:
            self.networks_to_delete.append(r.entity.id)
        self.assertEquals(r.status_code, 400,
                          '%s should not be allowed as cidr' % ip)
        ip = '1.1.1.1/243'
        r = self.networks_provider.client.create_network(cidr=ip, label=name)
        if r.entity is not None:
            self.networks_to_delete.append(r.entity.id)
        self.assertEquals(r.status_code, 400,
                          '%s should not be allowed as cidr' % ip)

    @attr('smoke', 'negative')
    def test_create_network_without_cidr_prefix(self):
        '''Verify if CIDR prefix is not specified, network cannot be created.
        '''
        name = datagen.random_string('invalid_cidr_network')
        ip = '1.1.1.1'
        r = self.networks_provider.client.create_network(cidr=ip, label=name)
        if r.entity is not None:
            self.networks_to_delete.append(r.entity.id)
        self.assertEquals(r.status_code, 400,
                          '%s should not be allowed as cidr' % ip)

    @unittest2.skip('QoS Bug not fixed')
    @attr('negative', 'new')
    def test_qos_set_correctly(self):
        '''Verify QoS is applied for an attached server.
        '''
        cidr = '192.1.1.248/30'
        network_label = datagen.random_string('qos_network')
        r = self.networks_provider.client.create_network(cidr=cidr,
                                                         label=network_label)
        network = r.entity
        self.assertEquals(r.status_code, 200)
        self.networks_to_delete.append(network.id)
        if self.run_nvp:
            nvp_switch = self.nvp_provider.aic_client.get_lswitch(network.id)
            self.assertEquals(nvp_switch['display_name'], network.label)
            nvp_switch = self.nvp_provider.aic_client.get_lswitch(network.id)
            self.assertEquals(nvp_switch['display_name'], network.label)
        networks = [{"uuid": network.id}]
        r = self.servers_provider.create_server_no_wait(networks=networks)
        self.servers_to_delete.append(r.entity.id)
        priv_server = r.entity
        networks.append({'uuid':
                         self.networks_provider.get_public_network().id})
        r = self.servers_provider.create_server_no_wait(networks=networks)
        self.servers_to_delete.append(r.entity.id)
        pub_server = r.entity
        self.servers_provider.wait_for_server_status(priv_server.id,
                                            NovaServerStatusTypes.ACTIVE)
        self.servers_provider.wait_for_server_status(pub_server.id,
                                            NovaServerStatusTypes.ACTIVE)
        if self.run_nvp:
            switch_ports = self.nvp_provider.aic_client.\
                list_lswitch_ports(network.id)
            self.assertEquals(len(switch_ports['results']), 2)
            priv_server_port = [p for p in switch_ports['results']
                                if p['portno'] == 1][0]
            pub_server_port = [p for p in switch_ports['results']
                                if p['portno'] == 2][0]
            priv_server_qos = priv_server_port['queue_uuid']
            pub_server_qos = pub_server_port['queue_uuid']
            self.assertIsNotNone(priv_server_qos,
                ('Server attached only to isolated network was'
                ' not applied QoS.'))
            self.assertIsNotNone(pub_server_qos,
                ('Server attached to public and isolated network'
                ' was not applied QoS.'))
