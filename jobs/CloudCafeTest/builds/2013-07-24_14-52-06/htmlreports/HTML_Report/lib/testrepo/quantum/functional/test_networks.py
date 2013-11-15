'''
@summary: Test Module for Quantum Networks
@copyright: Copyright (c) 2013 Rackspace US, Inc.
@author: leon0944
'''
import operator
import ccengine.common.tools.datagen as datagen
from ccengine.common.decorators import attr
from testrepo.common.testfixtures.networks import QuantumFixture
from ccengine.common.constants.networks_constants import QuantumResponseCodes


class TestQuantum(QuantumFixture):
    """Test Module for Quantum V2.0 Networks functionality"""

    @attr('smoke', 'positive')
    def test_create_network(self):
        """Testing create network POST"""
        network_name = datagen.rand_name('test_create')
        resp = self.quantum_provider.client.create_network(name=network_name)
        self.assertEqual(resp.status_code, QuantumResponseCodes.CREATE_NETWORK,
                         'Unable to create network: {0}'.format(resp.content))

        network = resp.entity
        self.assertTrue(network.id, 'Network id missing')
        self.q_networks_to_delete.append(network.id)

        # assert network default values
        self.assertEqual(network.status, 'ACTIVE')
        self.assertEqual(network.subnets, [])
        self.assertEqual(network.name, network_name)
        self.assertEqual(network.admin_state_up, True)
        self.assertEqual(network.port_security_enabled, True)
        self.assertEqual(network.tenant_id, self.tenant_id)
        self.assertEqual(network.router_external, False)
        self.assertEqual(network.shared, False)

    @attr('negative')
    def test_create_shared_network(self):
        """Negative test: regular user should not be able to create a shared
           network and will receive a 403 - Forbidden error"""
        network_name = datagen.rand_name('test_create_shared')
        resp = self.quantum_provider.client.create_network(name=network_name,
                                                           shared=True)
        msg = 'Unexpected {0} response, expecting {1} FORBIDDEN'
        self.assertEqual(resp.status_code, QuantumResponseCodes.FORBIDDEN,
                  msg.format(resp.status_code, QuantumResponseCodes.FORBIDDEN))

    @attr('smoke', 'positive')
    def test_show_network(self):
        """Testing show network GET"""
        # Test setUp
        network_name = datagen.rand_name('test_show')
        resp = self.quantum_provider.client.create_network(name=network_name)
        self.assertEqual(resp.status_code, QuantumResponseCodes.CREATE_NETWORK,
                         'Unable to create network: {0}'.format(resp.content))

        created_network = resp.entity
        self.assertTrue(created_network.id, 'Network id missing')
        self.q_networks_to_delete.append(created_network.id)

        # Test API show call
        show_resp = self.quantum_provider.client.show_network(
                                                            created_network.id)
        self.assertEqual(show_resp.status_code,
                         QuantumResponseCodes.SHOW_NETWORK,
                         'Unable to show network: {0}'.format(resp.content))
        network = show_resp.entity
        self.assertTrue(network.id, 'Network id missing in show response')
        msg = 'Unexpected network id, expected: {0} received: {1}'
        self.assertEqual(network.id, created_network.id, msg.format(
                                               created_network.id, network.id))
        # assert network default values
        msg = 'Unexpected default values, expecting: {0}, got: {1} instead'
        self.assertEqual(network.status, 'ACTIVE', msg.format('ACTIVE',
                                                              network.status))
        self.assertEqual(network.subnets, [])
        self.assertEqual(network.name, network_name)
        self.assertEqual(network.admin_state_up, True)
        self.assertEqual(network.port_security_enabled, True)
        self.assertEqual(network.tenant_id, self.tenant_id)
        self.assertEqual(network.router_external, False)
        self.assertEqual(network.shared, False)

    @attr('smoke', 'positive')
    def test_delete_network(self):
        """Testing delete network DELETE"""
        # Test setUp
        network_name = datagen.rand_name('test_delete')
        resp = self.quantum_provider.client.create_network(name=network_name)
        self.assertEqual(resp.status_code, QuantumResponseCodes.CREATE_NETWORK,
                         'Unable to create network: {0}'.format(resp.content))

        network = resp.entity
        self.assertTrue(network.id, 'Network id missing')

        # Test API Delete call
        del_resp = self.quantum_provider.client.delete_network(network.id)
        self.assertEqual(del_resp.status_code,
                    QuantumResponseCodes.DELETE_NETWORK,
                    'Unable to delete network: {0}'.format(del_resp.content))
        show_resp = self.quantum_provider.client.show_network(network.id)

        # Check the network is not there anymore
        msg = 'Unexpected {0} response, expecting {1} NOT FOUND'
        self.assertEqual(show_resp.status_code, QuantumResponseCodes.NOT_FOUND,
            msg.format(show_resp.status_code, QuantumResponseCodes.NOT_FOUND))

    @attr('smoke', 'positive')
    def test_update_network(self):
        """Testing update network PUT"""
        # Test setUp
        network_name = datagen.rand_name('test_update')
        resp = self.quantum_provider.client.create_network(name=network_name)
        self.assertEqual(resp.status_code, QuantumResponseCodes.CREATE_NETWORK,
                         'Unable to create network: {0}'.format(resp.content))

        network = resp.entity
        self.assertTrue(network.id, 'Network id missing')
        self.q_networks_to_delete.append(network.id)

        # Expected initial values
        msg = 'Unexpected {0} values, expecting: {1}, got: {2} instead'
        self.assertEqual(network.name, network_name, msg.format('initial',
                                                   network_name, network.name))
        self.assertEqual(network.admin_state_up, True, msg.format('initial',
                                               'True', network.admin_state_up))

        # Test API Update call: updating network name and admin_state_up
        updated_name = datagen.rand_name('updatedName')
        upd_resp = self.quantum_provider.client.update_network(network.id,
                                       name=updated_name, admin_state_up=False)
        self.assertEqual(upd_resp.status_code,
                    QuantumResponseCodes.UPDATE_NETWORK,
                    'Unable to update network: {0}'.format(upd_resp.content))
        upd_net = upd_resp.entity
        self.assertEqual(upd_net.id, network.id, msg.format('id',
                                                       network.id, upd_net.id))
        self.assertEqual(upd_net.name, updated_name, msg.format('updated',
                                                   updated_name, upd_net.name))
        self.assertEqual(upd_net.admin_state_up, False, msg.format('updated',
                                              'False', upd_net.admin_state_up))

        # Double check changing back to initial values
        dblck_resp = self.quantum_provider.client.update_network(network.id,
                                       name=network_name, admin_state_up=True)
        self.assertEqual(dblck_resp.status_code,
                  QuantumResponseCodes.UPDATE_NETWORK,
                 'Unable to re-update network: {0}'.format(dblck_resp.content))
        dblck_net = dblck_resp.entity
        self.assertEqual(dblck_net.name, network_name, msg.format('re-updated',
                                                 network_name, dblck_net.name))
        self.assertEqual(dblck_net.admin_state_up, True,
                    msg.format('re-updated', 'True', dblck_net.admin_state_up))

    @attr('negative')
    def test_negative_update_network(self):
        """Negative test: user should not be able to update tenant id,
           network id or status"""
        # Test setUp
        network_name = datagen.rand_name('test_neg_update')
        resp = self.quantum_provider.client.create_network(name=network_name)
        self.assertEqual(resp.status_code, QuantumResponseCodes.CREATE_NETWORK,
                         'Unable to create network: {0}'.format(resp.content))

        network = resp.entity
        self.assertTrue(network.id, 'Network id missing')
        self.q_networks_to_delete.append(network.id)

        # Test negative update call: updating network status
        msg = 'Expected {0} got {1} instead'
        status_resp = self.quantum_provider.client.update_network(network.id,
                                                                status='DOWN')
        self.assertEqual(status_resp.status_code,
                    QuantumResponseCodes.BAD_REQUEST, msg.format(
                    QuantumResponseCodes.BAD_REQUEST, status_resp.status_code))

        # Test negative update call: updating network id
        new_id_resp = self.quantum_provider.client.update_network(network.id,
                                            new_id='made-up-network-id-12345')
        self.assertEqual(new_id_resp.status_code,
                    QuantumResponseCodes.BAD_REQUEST, msg.format(
                    QuantumResponseCodes.BAD_REQUEST, new_id_resp.status_code))

        # Test negative update call: updating tenant id
        tenant_resp = self.quantum_provider.client.update_network(network.id,
                                          tenant_id='made-up-tenant-id-12345')
        self.assertEqual(tenant_resp.status_code,
                    QuantumResponseCodes.BAD_REQUEST, msg.format(
                    QuantumResponseCodes.BAD_REQUEST, tenant_resp.status_code))

    @attr('smoke', 'positive')
    def test_list_networks(self):
        """Testing list networks GET"""

        # Test setUp
        n_networks = 7
        name_prefix = 'test_list_networks'
        nets = self.quantum_provider.create_n_networks(n=n_networks,
                                                   name_startswith=name_prefix)
        test_nets = nets['networks']
        test_nets_ids = self.quantum_provider.get_attr_list(test_nets, 'id')
        self.q_networks_to_delete.extend(test_nets_ids)

        self.assertEqual(nets['count'], n_networks, ('Unable to create the {0}'
                                  'expected test networks'.format(n_networks)))
        # Test API List Call
        resp = self.quantum_provider.client.list_networks()
        self.assertEqual(resp.status_code, QuantumResponseCodes.LIST_NETWORKS,
                           'Unable to list networks: {0}'.format(resp.content))

        # Filter the networks getting only the ones created by this test
        list_nets = self.quantum_provider.get_network_by_kwarg(key='name',
                                           value=name_prefix, starts_with=True,
                                           networks=resp.entity)

        msg = 'Unexpected list count, expecting: {0} and got: {1}'
        self.assertEqual(len(test_nets), len(list_nets),
                                    msg.format(len(test_nets), len(list_nets)))
        # Sorting for the list assert
        test_nets.sort(key=operator.attrgetter('name'))
        list_nets.sort(key=operator.attrgetter('name'))
        msg = ('Unexpected network lists, network create response used for '
              'the test setUp may be different than the network list response')

        # This will fail if the API create and list network responses change
        self.assertListEqual(list_nets, test_nets, msg)
