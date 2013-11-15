from testrepo.common.testfixtures.load_balancers \
    import LoadBalancersSmokeFixture, LoadBalancersZeusFixture
from ccengine.common.decorators import attr
import ccengine.common.tools.datagen as datagen
from ccengine.domain.types import LoadBalancerNodeConditions as \
    LBNodeConditions
from ccengine.domain.types import LoadBalancerNodeTypes as LBNodeTypes, \
    LoadBalancerStatusTypes as LBStatus, \
    LoadBalancerVirtualIpTypes as LBVipTypes
import requests
import unittest2
import xmlrpclib
import time


class NodeSmokeTests(LoadBalancersSmokeFixture):

    @attr('smoke', 'positive')
    def test_node_count(self):
        """Testing node count attribute in load balancer list."""
        lb = self.lbaas_provider.create_active_load_balancer().entity
        self.lbs_to_delete.append(lb.id)
        r = self.client.list_load_balancers()
        lb_list = r.entity
        self.assertEqual(r.status_code, 200)
        lb_in_list = lb_list.get_by_id(lb.id)
        self.assertEquals(lb_in_list.nodeCount, len(lb.nodes))
        node1_address = datagen.random_ip()
        node1_port = datagen.random_int(1, 500)
        node1_condition = LBNodeConditions.ENABLED
        r = self.client.add_nodes(lb.id, node1_address, node1_condition,
                                  node1_port)
        added_node = r.entity[0]
        self.assertEqual(r.status_code, 202)
        self.lbaas_provider.wait_for_status(lb.id)
        r = self.client.list_load_balancers()
        lb_list = r.entity
        lb_in_list = lb_list.get_by_id(lb.id)
        self.assertEquals(lb_in_list.nodeCount, len(lb.nodes) + 1)
        r = self.client.list_load_balancers(lb.id)
        self.assertEquals(r.status_code, 200)
        r = self.client.delete_node(lb.id, added_node.id)
        self.assertEquals(r.status_code, 202)
        self.lbaas_provider.wait_for_status(lb.id)
        lb_list = self.client.list_load_balancers().entity
        lb_in_list = lb_list.get_by_id(lb.id)
        self.assertEquals(lb_in_list.nodeCount, len(lb.nodes))

    @attr('smoke', 'positive')
    def test_add_update_remove_node(self):
        """CRUD operations on nodes."""
        #Test node create
        node1_address = datagen.random_ip()
        node1_port = datagen.random_int(1, 500)
        node1_condition = LBNodeConditions.ENABLED
        r = self.client.add_nodes(self.lb.id, node1_address,
                                  node1_condition, node1_port)
        ret_node = r.entity[0]
        self.assertEqual(r.status_code, 202)
        self.assertEqual(ret_node.address, node1_address)
        self.assertEqual(ret_node.port, node1_port)
        self.assertEqual(ret_node.condition, node1_condition)
        self.lbaas_provider.wait_for_status(self.lb.id)
        #Test node was created successfully and added
        r = self.client.get_node(self.lb.id, ret_node.id)
        ret_node = r.entity
        self.assertEqual(r.status_code, 200)
        self.assertEqual(ret_node.address, node1_address)
        self.assertEqual(ret_node.port, node1_port)
        self.assertEqual(ret_node.condition, node1_condition)
        #Test node update
        node2_weight = datagen.random_int(5, 10)
        r = self.client.update_node(self.lb.id, ret_node.id,
                                    condition=LBNodeConditions.DISABLED,
                                    type=LBNodeTypes.SECONDARY,
                                    weight=node2_weight)
        self.assertEqual(r.status_code, 202)
        self.lbaas_provider.wait_for_status(self.lb.id)
        r = self.client.get_node(self.lb.id, ret_node.id)
        updated_node = r.entity
        self.assertEqual(updated_node.condition, LBNodeConditions.DISABLED)
        self.assertEqual(updated_node.weight, node2_weight)
        self.assertEqual(updated_node.id, ret_node.id)
        self.assertEqual(updated_node.address, ret_node.address)
        self.assertEqual(updated_node.port, ret_node.port)
        #Test node list and new node is in list
        r = self.client.list_nodes(self.lb.id)
        node_list = r.entity
        self.assertEqual(r.status_code, 200)
        node_in_list = node_list.get_by_id(updated_node.id)
        self.assertIsNotNone(node_in_list)
        self.assertEquals(node_in_list.address, updated_node.address)
        self.assertEquals(node_in_list.condition, updated_node.condition)
        self.assertEquals(node_in_list.port, updated_node.port)
        self.assertIsNotNone(node_in_list.status)
        #Test node delete and node was removed from list of nodes
        self.client.delete_node(self.lb.id, updated_node.id)
        self.lbaas_provider.wait_for_status(self.lb.id)
        r = self.client.list_nodes(self.lb.id)
        node_list = r.entity
        self.assertEqual(r.status_code, 200)
        node_in_list = node_list.get_by_id(updated_node.id)
        self.assertIsNone(node_in_list)
        r = self.client.get_node(self.lb.id, updated_node.id)
        self.assertEquals(r.status_code, 404)
        self.assertIsNone(r.entity)

    @attr('smoke', 'positive')
    def test_batch_delete_nodes(self):
        """Test batch delete of nodes"""
        orig_node = self.lb.nodes[0]
        nodes = self.lbaas_provider.add_n_nodes(self.lb.id, 5)
        self.lbaas_provider.wait_for_status(self.lb.id)
        node_ids = [n.id for n in nodes]
        r = self.client.batch_delete_nodes(self.lb.id, node_ids)
        self.assertEquals(r.status_code, 202)
        self.lbaas_provider.wait_for_status(self.lb.id)
        r = self.client.list_nodes(self.lb.id)
        nodes = r.entity
        self.assertEquals(r.status_code, 200)
        new_nodes_ids = [n.id for n in nodes]
        all_nodes_deleted = True
        for node_id in node_ids:
            if node_id in new_nodes_ids:
                all_nodes_deleted = False
        self.assertTrue(all_nodes_deleted)
        self.assertIn(orig_node.id, new_nodes_ids)


class NodeTests(LoadBalancersZeusFixture):

    @classmethod
    def setUpClass(cls):
        super(NodeTests, cls).setUpClass()
        cls.lb = cls.lbaas_provider.create_active_load_balancer().entity
        cls.lbs_to_delete.append(cls.lb.id)
        cls.default_nodes = cls.lb.nodes

    @classmethod
    def setUp(cls):
        addresses = [node.address for node in cls.default_nodes]
        r = cls.lbaas_provider.wait_for_status(cls.lb.id)
        delete_node_ids = [node.id for node in r.entity.nodes
                           if node.address not in addresses]
        cls.client.batch_delete_nodes(cls.lb.id, delete_node_ids)
        r = cls.lbaas_provider.wait_for_status(cls.lb.id)
        addresses = []
        conditions = []
        ports = []
        types = []
        weights = []
        for d_node in cls.default_nodes:
            curr_node_addrs = [node.address for node in r.entity.nodes]
            if d_node.address not in curr_node_addrs:
                addresses.append(d_node.address)
                conditions.append(d_node.condition)
                ports.append(d_node.port)
                types.append(d_node.type)
                weights.append(d_node.weight)
        if len(addresses) != 0:
            cls.client.add_nodes(cls.lb.id, address=addresses,
                                 condition=conditions, port=ports, type=types,
                                 weight=weights)
            cls.lbaas_provider.wait_for_status(cls.lb.id)

    @attr('positive')
    def test_domain_nodes(self):
        """Test domain nodes"""
        #Tests are tied directly to rackexp.org.  If this tests fails because
        #of bad domain name, check that the ip of the live node is still
        #pointed to what the config value is for domain_node.
        node_address = self.config.lbaas_api.domain_node
        nodes = [{'address': node_address,
                  'condition': LBNodeConditions.ENABLED,
                  'port': 80}]
        r = self.lbaas_provider.create_active_load_balancer(nodes=nodes)
        self.assertEquals(r.entity.status, LBStatus.ACTIVE)
        lb = r.entity
        self.lbs_to_delete.append(lb.id)
        self.assertEquals(lb.nodes[0].address, node_address)
        node_address2 = '100.1.1.1'
        r = self.client.add_nodes(lb.id, address=node_address2,
                                  condition=LBNodeConditions.ENABLED,
                                  port=80)
        self.assertEquals(r.status_code, 202)
        r = self.lbaas_provider.wait_for_status(lb.id)
        self.assertEquals(r.entity.status, LBStatus.ACTIVE)
        lb = r.entity
        addresses = [node.address for node in lb.nodes]
        self.assertIn(node_address, addresses)
        r = self.client.delete_node(lb.id, lb.nodes[0].id)
        self.assertEquals(r.status_code, 202)
        r = self.lbaas_provider.wait_for_status(lb.id)
        self.assertEquals(r.entity.status, LBStatus.ACTIVE)

    @attr('positive')
    def test_secondary_nodes(self):
        """Test secondary nodes"""
        lb = self.lbaas_provider.create_active_load_balancer().entity
        self.lbs_to_delete.append(lb.id)
        r = self.client.update_health_monitor(lb.id, 1, 1, 1, 'HTTP',
                                              '/', '.', '.')
        self.assertEquals(r.status_code, 202)
        self.lbaas_provider.wait_for_status(lb.id)
        prim_node = lb.nodes.get_by_address(self.config.lbaas_api.live_node1)
        sec_node = lb.nodes.get_by_address(self.config.lbaas_api.live_node2)
        r = self.client.update_node(lb.id, sec_node.id,
                                    type=LBNodeTypes.SECONDARY)
        self.assertEquals(r.status_code, 202)
        lb = self.lbaas_provider.wait_for_status(lb.id).entity
        sec_node = lb.nodes.get_by_address(self.config.lbaas_api.live_node2)
        self.assertEquals(sec_node.type, LBNodeTypes.SECONDARY)
        if (self.config.lbaas_api.is_qa_env or
                lb.virtualIps[0].type == LBVipTypes.SERVICENET):
            return
        web_vip = ''.join(['http://', lb.virtualIps[0].address])
        page = requests.api.get(web_vip).content
        self.assertIn('PRIMARY NODE', page, msg=page)
        xmlrpc_url = ''.join(['http://', prim_node.address, ':8081'])
        node_proxy = xmlrpclib.ServerProxy(xmlrpc_url)
        node_proxy.stop_apache()
        time.sleep(10)
        page = requests.api.get(web_vip).content
        self.assertIn('SECONDARY NODE', page, msg=page)
        node_proxy.start_apache()
        time.sleep(10)
        page = requests.api.get(web_vip).content
        self.assertIn('PRIMARY NODE', page, msg=page)

    @attr('positive')
    def test_secondary_nodes_health_monitor_validation(self):
        """Secondary nodes validate health monitor is enabled."""
        lb = self.lbaas_provider.create_active_load_balancer().entity
        self.lbs_to_delete.append(lb.id)
        sec_node = lb.nodes[1]
        r = self.client.update_node(lb.id, sec_node.id,
                                    type=LBNodeTypes.SECONDARY)
        self.assertEquals(r.status_code, 400)
        r = self.client.add_nodes(lb.id, address='100.1.1.1',
                                  condition=LBNodeConditions.ENABLED, port=80,
                                  type=LBNodeTypes.SECONDARY)
        self.assertEquals(r.status_code, 400)
        r = self.client.update_health_monitor(lb.id, 1, 1, 1, 'HTTP',
                                              '/', '.', '.')
        self.assertEquals(r.status_code, 202)
        r = self.lbaas_provider.wait_for_status(lb.id)
        self.assertEquals(r.entity.status, LBStatus.ACTIVE)
        r = self.client.update_node(lb.id, sec_node.id,
                                    type=LBNodeTypes.SECONDARY)
        self.assertEquals(r.status_code, 202)
        r = self.lbaas_provider.wait_for_status(lb.id)
        lb = r.entity
        r = self.client.add_nodes(lb.id, address='100.1.1.1',
                                  condition=LBNodeConditions.ENABLED, port=80,
                                  type=LBNodeTypes.SECONDARY)
        self.assertEquals(r.status_code, 202)
        r = self.lbaas_provider.wait_for_status(lb.id)
        lb = r.entity
        r = self.client.delete_health_monitor(lb.id)
        self.assertEquals(r.status_code, 400)
        sec_nodes = [node.id for node in lb.nodes
                     if node.type == LBNodeTypes.SECONDARY]
        r = self.client.batch_delete_nodes(lb.id, sec_nodes)
        self.assertEquals(r.status_code, 202)
        r = self.lbaas_provider.wait_for_status(lb.id)
        lb = r.entity
        r = self.client.delete_health_monitor(lb.id)
        self.assertEquals(r.status_code, 202)
        r = self.lbaas_provider.wait_for_status(lb.id)
        self.assertEquals(r.entity.status, LBStatus.ACTIVE)

    @attr('positive')
    def test_node_weight_update_defect(self):
        """Change weight on a singular enabled node on an LB"""
        algorithms = self.client.list_algorithms().entity
        algorithm = algorithms.get_weighted()[0].name
        nodes = [{'address': '100.1.1.1', 'port': 80,
                  'condition': LBNodeConditions.ENABLED}]
        r = self.lbaas_provider.create_active_load_balancer(
            algorithm=algorithm, nodes=nodes)
        lb = r.entity
        self.lbs_to_delete.append(lb.id)
        r = self.client.update_node(lb.id, lb.nodes[0].id, weight=10)
        self.assertEqual(r.status_code, 202)
        self.lbaas_provider.wait_for_status(lb.id)
        r = self.client.get_node(lb.id, lb.nodes[0].id)
        self.assertEquals(r.entity.weight, 10)

    @attr('positive')
    def test_node_address_longer_than_128(self):
        """Verify node address cannot be greater than 128 characters"""
        ad_list = self.client.list_allowed_domains().entity
        self.assertIsNotNone(ad_list)
        self.assertNotEqual(len(ad_list), 0)
        domain = ad_list[0].name
        subdomain = 'blah' * 30
        address = '.'.join([subdomain, domain])
        nodes = [{'address': address,
                  'condition': LBNodeConditions.ENABLED,
                  'port': 80}]
        r = self.client.add_nodes(self.lb.id, address=address,
                                  condition=nodes[0]['condition'],
                                  port=nodes[0]['port'])
        self.assertEqual(r.status_code, 400)

    @attr('negative')
    def test_duplicate_ipv6_node(self):
        '''Duplicate IPv6 Nodes are not allowed.'''
        node1_addr = '1a61:5f02:d5c2:fc06:63bb:38d7:0:7c9d'
        node2_addr = '1a61:5f02:d5c2:fc06:63bb:38d7:0000:7c9d'
        name = 'thisshouldnotbeallowed'
        virtualIps = [{'type': LBVipTypes.PUBLIC}]
        protocol = 'HTTP'
        nodes = [{
            'address': node1_addr, 'port': 80,
            'condition': LBNodeConditions.ENABLED},
            {'address': node2_addr, 'port': 80,
             'condition': LBNodeConditions.ENABLED}]
        r = self.client.create_load_balancer(name=name, protocol=protocol,
                                             virtualIps=virtualIps,
                                             nodes=nodes)
        self.assertEquals(r.status_code, 400)
        r = self.client.add_nodes(self.lb.id, address=[nodes[0]['address'],
                                                       nodes[1]['address']],
                                  port=[nodes[0]['port'], nodes[1]['port']],
                                  condition=[nodes[0]['condition'],
                                             nodes[1]['condition']])
        self.assertEquals(r.status_code, 422)
        node1_addr2 = '1a61:5f02:d5c2:fc06:63bb::7c9d'
        node2_addr2 = '1a61:5f02:d5c2:fc06:63bb:0000:0000:7c9d'
        nodes[0]['address'] = node1_addr2
        nodes[1]['address'] = node2_addr2
        r = self.client.create_load_balancer(name=name, protocol=protocol,
                                             virtualIps=virtualIps,
                                             nodes=nodes)
        self.assertEquals(r.status_code, 400)
        r = self.client.add_nodes(self.lb.id, address=[nodes[0]['address'],
                                                       nodes[1]['address']],
                                  port=[nodes[0]['port'], nodes[0]['port']],
                                  condition=[nodes[0]['condition'],
                                             nodes[0]['condition']])
        self.assertEquals(r.status_code, 422)
        r = self.client.add_nodes(self.lb.id, address=nodes[0]['address'],
                                  port=nodes[0]['port'],
                                  condition=nodes[0]['condition'])
        self.assertEquals(r.status_code, 202)
        self.lbaas_provider.wait_for_status(self.lb.id)
        r = self.client.add_nodes(self.lb.id, address=nodes[1]['address'],
                                  port=nodes[1]['port'],
                                  condition=nodes[1]['condition'])
        self.assertEquals(r.status_code, 422)

    @attr('positive')
    def test_node_events_call_exists(self):
        """Node events resource returns correctly."""
        r = self.client.list_node_service_events(self.lb.id)
        self.assertEqual(r.status_code, 200)

    @unittest2.skip('Need to generate actual node events.')
    @attr('positive')
    def test_actual_node_events(self):
        pass

    @attr('positive')
    def test_secondary_node_update_bug_becoming_primary(self):
        '''Update a node and verify it stays secondary'''
        r = self.client.update_health_monitor(load_balancer_id=self.lb.id,
                                              attemptsBeforeDeactivation=10,
                                              delay=1, timeout=10,
                                              type='CONNECT')
        self.assertEquals(r.status_code, 202)
        self.lbaas_provider.wait_for_status(self.lb.id)
        r = self.client.list_nodes(self.lb.id)
        self.assertEquals(r.status_code, 200)
        node_id = r.entity[0].id
        r = self.client.update_node(load_balancer_id=self.lb.id,
                                    node_id=node_id,
                                    type=LBNodeTypes.SECONDARY)
        self.assertEquals(r.status_code, 202)
        self.lbaas_provider.wait_for_status(self.lb.id)
        r = self.client.get_node(load_balancer_id=self.lb.id, node_id=node_id)
        self.assertEquals(r.status_code, 200)
        self.assertTrue(r.entity.type == LBNodeTypes.SECONDARY)
        r = self.client.update_node(load_balancer_id=self.lb.id,
                                    node_id=node_id,
                                    weight=10)
        self.assertEquals(r.status_code, 202)
        self.lbaas_provider.wait_for_status(self.lb.id)
        r = self.client.get_node(load_balancer_id=self.lb.id, node_id=node_id)
        self.assertEquals(r.status_code, 200)
        self.assertTrue(r.entity.type == LBNodeTypes.SECONDARY)
