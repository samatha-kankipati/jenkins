import requests

from ccengine.common.decorators import attr
import ccengine.common.tools.datagen as Datagen
from ccengine.domain.lbaas.node import NodeList
from ccengine.domain.types import LoadBalancerNodeTypes as LBNodeTypes, \
    LoadBalancerNodeConditions as LBNodeConditions
from testrepo.common.testfixtures.load_balancers \
    import LoadBalancersZeusFixture


class RemoveNodesToBecomeNodeless(LoadBalancersZeusFixture):

    @classmethod
    def setUpClass(cls):
        super(RemoveNodesToBecomeNodeless, cls).setUpClass()
        cls.lb = cls.lbaas_provider.create_active_load_balancer(
            nodeless=True).entity
        cls.lbs_to_delete.append(cls.lb.id)
        cls.default_nodes = cls.lb.nodes

    def tearDown(self):
        # If the default fixture LB was used, clear any nodes that might
        # have been configured, so that the next test doesn't fail.
        node_ids = self.client.list_nodes(self.lb.id).entity
        if node_ids:
            response = self.client.batch_delete_nodes(self.lb.id, node_ids)
            self.assertEqual(response.status_code, requests.codes.accepted)
            self.lbaas_provider.wait_for_status(self.lb.id)

    @attr('nodeless')
    def test_batch_delete_nodes_to_nodeless(self):
        """ Test batch delete of nodes """

        list_of_nodes = self.client.list_nodes(self.lb.id).entity
        self.assertEqual(list_of_nodes, [], 'Nodeless LB has nodes!!')

        # Add nodes to LB
        self.fixture_log.info("\n\n*** Adding nodes to LB ***\n")
        nodes = self.lbaas_provider.add_n_nodes(self.lb.id, n=5)
        self.lbaas_provider.wait_for_status(self.lb.id)

        # Get list of nodes
        node_ids = [n.id for n in nodes]
        self.fixture_log.info("\n\n**** Batch Delete all Nodes (num={num}***"
                              "\n".format(num=len(node_ids)))

        # Batch delete all nodes
        self.fixture_log.info("\n\nLIST OF ALL NODES: {0}\n".format(node_ids))
        response = self.client.batch_delete_nodes(self.lb.id, node_ids)
        self.assertEqual(response.status_code, requests.codes.accepted)
        self.lbaas_provider.wait_for_status(self.lb.id)

        # Get list of nodes on LB
        self.fixture_log.info("\n\n**** Getting list of nodes on the LB ***\n")
        response = self.client.list_nodes(self.lb.id)
        nodes = response.entity
        self.assertEqual(response.status_code, requests.codes.ok)
        self.assertEqual(len(nodes), 0,
                         "Node list not empty: {0}".format(
                             [n.id for n in nodes]))

    @attr('nodeless')
    def test_node_count_starting_as_nodeless(self):
        """ Testing node count attribute in load balancer list """

        # Create a nodeless load balancer
        lb = self.lbaas_provider.create_active_load_balancer(
            nodeless=True).entity
        self.lbs_to_delete.append(lb.id)
        num_nodes = 0

        # Get the list of load balancers
        response = self.client.list_load_balancers()
        lb_list = response.entity
        self.assertEqual(response.status_code, requests.codes.ok)

        # Verify number of reported nodes matches expected number of nodes
        lb_in_list = lb_list.get_by_id(lb.id)
        self.assertEqual(lb_in_list.nodeCount, num_nodes,
                         "Node count not 0: {0}".format(lb_in_list))

        # Add a node to the load balancer
        node1_cfg = dict(address=Datagen.random_ip(),
                         port=Datagen.random_int(1, 500),
                         condition=LBNodeConditions.ENABLED)
        response = self.client.add_nodes(lb.id, **node1_cfg)
        added_node = response.entity[0]
        self.assertEqual(response.status_code, requests.codes.accepted)
        self.lbaas_provider.wait_for_status(lb.id)
        num_nodes += 1

        # Verify the general load balancer API returns the updated node number
        response = self.client.list_load_balancers()
        lb_list = response.entity
        lb_in_list = lb_list.get_by_id(lb.id)
        self.assertEqual(lb_in_list.nodeCount, num_nodes)

        # Verify the detailed load balancer API returns information
        response = self.client.list_load_balancers(lb.id)
        self.assertEqual(response.status_code, requests.codes.ok)

        # Delete the added node
        response = self.client.delete_node(lb.id, added_node.id)
        self.assertEqual(response.status_code, requests.codes.accepted)
        self.lbaas_provider.wait_for_status(lb.id)
        num_nodes -= 1

        # Verify the number of nodes after deletion is correct
        lb_list = self.client.list_load_balancers().entity
        lb_in_list = lb_list.get_by_id(lb.id)
        self.assertEqual(lb_in_list.nodeCount, num_nodes)

    @attr('nodeless')
    def test_list_nodes_on_nodeless_lb(self):
        """ List nodes on nodeless load balancer """
        response = self.client.list_nodes(self.lb.id)
        self.assertEqual(response.status_code, requests.codes.ok)
        self.assertEqual(response.entity, [])

        non_existent_node = 44536
        response = self.client.get_node(self.lb.id, non_existent_node)
        self.assertEqual(response.status_code, requests.codes.not_found)

    @attr('nodeless')
    def test_add_update_remove_node_starting_as_nodeless(self):
        """ CRUD operations on nodes """

        # Test node create
        node_cfg = dict(address=Datagen.random_ip(),
                        port=Datagen.random_int(1, 500),
                        condition=LBNodeConditions.ENABLED,
                        weight=None)
        response = self.client.add_nodes(self.lb.id, **node_cfg)
        node_id = response.entity[0].id
        self._verify_node_attributes(response=response, node_cfg=node_cfg,
                                     expected_response=requests.codes.accepted)
        self.lbaas_provider.wait_for_status(self.lb.id)

        # Test node was created successfully and added
        response = self.client.get_node(self.lb.id, node_id)
        self._verify_node_attributes(response=response, node_cfg=node_cfg,
                                     expected_response=requests.codes.ok)

        # Test the following node configuration parameters
        # (set param_1, reset, set param_2, reset)
        node_permutations = [
            ('type', LBNodeTypes.SECONDARY, requests.codes.bad),
            ('type', LBNodeTypes.PRIMARY, requests.codes.accepted),
            ('condition', LBNodeConditions.DISABLED, requests.codes.accepted),
            ('condition', LBNodeConditions.ENABLED, requests.codes.accepted)]

        # Test node update
        for (parameter, setting, expected_response) in node_permutations:
            node_cfg['weight'] = Datagen.random_int(5, 10)
            node_cfg[parameter] = setting
            update_dict = {'weight': node_cfg['weight'],
                           parameter: node_cfg[parameter]}

            response = self.client.update_node(
                self.lb.id, node_id, **update_dict)

            self._verify_node_attributes(
                response=response, expected_response=expected_response)

            self.lbaas_provider.wait_for_status(self.lb.id)
            response = self.client.get_node(self.lb.id, node_id)

            # If configuration update was accepted (response = 2xx)
            if str(expected_response).startswith('20'):
                self._verify_node_attributes(
                    response=response, node_cfg=node_cfg,
                    expected_response=requests.codes.ok, node_id=node_id)

        updated_node = response.entity

        # Test node list and new node is in list
        response = self.client.list_nodes(self.lb.id)
        node_list = response.entity
        self.assertEqual(response.status_code, requests.codes.ok)
        node_in_list = node_list.get_by_id(node_id)

        self.assertIsNotNone(node_in_list)
        self.assertIsNotNone(node_in_list.status)
        self.assertEqual(node_in_list.address, updated_node.address)
        self.assertEqual(node_in_list.condition, updated_node.condition)
        self.assertEqual(node_in_list.port, updated_node.port)

        # Test node delete and node was removed from list of nodes
        self.client.delete_node(self.lb.id, node_id)
        self.lbaas_provider.wait_for_status(self.lb.id)

        response = self.client.list_nodes(self.lb.id)
        self.assertEqual(response.status_code, requests.codes.ok)
        node_in_list = response.entity.get_by_id(node_id)
        self.assertIsNone(node_in_list)

        response = self.client.get_node(self.lb.id, updated_node.id)
        self.assertEqual(response.status_code, requests.codes.not_found)
        self.assertIsNone(response.entity)

    @attr('nodeless')
    def test_convert_std_lb_to_nodeless(self):
        """ Convert normal load balancer to a nodeless load balancer """
        self.node_lb = self.lbaas_provider.\
            create_active_load_balancer().entity
        self.lbs_to_delete.append(self.node_lb.id)

        response = self.client.list_nodes(self.node_lb.id)
        self.assertEqual(response.status_code, requests.codes.ok)
        node_list = [node.id for node in response.entity]
        num_nodes = len(node_list)
        for node_id in node_list:
            self.fixture_log.info("\n\n*** Removing Node from LB ***")
            response = self.client.delete_node(self.node_lb.id, node_id)
            self.assertEqual(response.status_code, requests.codes.accepted)
            self.lbaas_provider.wait_for_status(self.node_lb.id)
            num_nodes -= 1

            response = self.client.list_nodes(self.node_lb.id)
            self.assertEqual(response.status_code, requests.codes.ok)
            updated_node_list = [node.id for node in response.entity]
            self.assertEqual(len(updated_node_list), num_nodes)

    @attr('nodeless')
    def test_delete_node_from_nodeless(self):
        """ Delete a node from a nodeless load balancer, verify response """
        node_id = '12345'
        response = self.client.delete_node(self.lb.id, node_id)
        self.assertEqual(response.status_code, requests.codes.not_found)
        self.lbaas_provider.wait_for_status(self.lb.id)

    @attr('nodeless')
    def test_nodeless_node_events_call_exists(self):
        """ Node events resource returns correctly """
        response = self.client.list_node_service_events(self.lb.id)
        self.assertEqual(response.status_code, requests.codes.ok)

    def _verify_node_attributes(self, response, expected_response,
                                node_cfg=None, node_id=None,):

        updated_node = response.entity[0] if \
            isinstance(response.entity, NodeList) else response.entity
        self.assertEqual(response.status_code, expected_response)

        if node_cfg is not None:
            self.assertEqual(updated_node.condition, node_cfg['condition'])
            self.assertEqual(updated_node.address, node_cfg['address'])

            if 'port' in node_cfg:
                self.assertEqual(updated_node.port, node_cfg['port'])

            if node_cfg['weight'] is not None:
                self.assertEqual(updated_node.weight, node_cfg['weight'])

        if node_id is not None:
            self.assertEqual(updated_node.id, node_id)
