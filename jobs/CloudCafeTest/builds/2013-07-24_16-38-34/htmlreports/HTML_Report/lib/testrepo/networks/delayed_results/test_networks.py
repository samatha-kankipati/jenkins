from testrepo.common.testfixtures.networks import NetworksTestFixture
from ccengine.domain.types import NovaServerStatusTypes
import unittest2
from ccengine.common.decorators import attr
import ccengine.common.tools.datagen as datagen
from aiclib.nvp import ResourceNotFound
import pickle
import os


class TestNetworks(NetworksTestFixture):

    @attr('positive')
    def test_add_server_to_network_after_ip_has_been_released(self):
        '''Removing a server from a network releases the IP'''
        section = 'test_add_server_to_network_after_ip_has_been_released'
        pkl_file = open('/'.join([os.getcwd(), 'data.pkl']), 'rb')
        pickle_data = pickle.load(pkl_file)
        network_id = pickle_data[section]['network_id']
        ip2 = pickle_data[section]['deleted_ip']
        server1_id = pickle_data[section]['server1_id']
        r = self.networks_provider.client.get_network(network_id)
        small_network = r.entity
        self.networks_to_delete.append(small_network.id)
        self.servers_to_delete.append(server1_id)
        server3_name = 'server3'
        server3_networks = [{'uuid':small_network.id}]
        r = self.servers_provider.create_active_server(name=server3_name,
                                                    networks=server3_networks)
        server3 = r.entity
        self.servers_to_delete.append(server3.id)
        self.assertEquals(r.status_code, 200)
        self.assertEquals(server3.status, NovaServerStatusTypes.ACTIVE,
                          'Possible melange address release issue.')
        ip3 = server3.addresses.get_by_name(small_network.label).ipv4
        self.assertEquals(ip3, ip2)
