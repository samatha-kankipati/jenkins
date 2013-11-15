import requests

from ccengine.common.decorators import attr
import ccengine.common.tools.datagen as Datagen
from ccengine.domain.lbaas.algorithm import Algorithm
from ccengine.domain.lbaas.protocol import Protocol
from ccengine.domain.types import LoadBalancerStatusTypes as LBStatus, \
    LoadBalancerVirtualIpTypes as LBVipTypes

from testrepo.common.testfixtures.load_balancers \
    import LoadBalancersZeusFixture


class TestNodelessLoadBalancers(LoadBalancersZeusFixture):

    @classmethod
    def setUpClass(cls):
        super(TestNodelessLoadBalancers, cls).setUpClass()
        cls.lb = cls.lbaas_provider.create_active_load_balancer(
            nodeless=True).entity
        cls.lbs_to_delete.append(cls.lb.id)
        cls.zeus_vs_name = '{0}_{1}'.format(cls.tenant_id, cls.lb.id)

    @attr('nodeless')
    def test_nodeless_lb_crud_ops(self):
        """
        Test create, update, get, and delete of a nodeless load balancer

        """
        lb_args = dict(name='cc_crud_lb', nodes=[], protocol='HTTP',
                       virtualIps=[{'type': self.default_vip_type}],
                       port=80, timeout=30, algorithm='RANDOM',
                       halfClosed=False)

        # Create a nodeless LB
        response = self.client.create_load_balancer(**lb_args)
        lb_id = response.entity.id
        self.lbs_to_delete.append(lb_id)
        self.validate_lb_response(
            response=response, lb_args=lb_args, state=LBStatus.BUILD,
            resp_code=requests.codes.accepted)

        # Wait for LB to be ACTIVE
        response = self.lbaas_provider.wait_for_status(lb_id)
        self.validate_lb_response(response=response, lb_args=lb_args,
                                  state=LBStatus.ACTIVE)

        # List Active LBs and verify new LB is in list
        response = self.client.list_load_balancers()
        lb_id_list = [l_bal.id for l_bal in response.entity]
        self.assertIn(lb_id, lb_id_list,
                      'NON-DELETED Load balancer not in load balancers list.')

        lb_args['name'] = 'cc_update_crud_lb'
        lb_args['port'] = 79
        lb_args['protocol'] = 'HTTPS'
        lb_args['algorithm'] = 'RANDOM'
        lb_args['timeout'] = 55

        # Update the LB configuration
        response = self.client.update_load_balancer(
            lb_id, name=lb_args['name'], port=lb_args['port'],
            protocol=lb_args['protocol'], timeout=lb_args['timeout'],
            algorithm=lb_args['algorithm'])

        self.validate_lb_response(response=response,
                                  resp_code=requests.codes.accepted)

        response = self.client.get_load_balancer(lb_id)
        self.validate_lb_response(response=response, lb_args=lb_args,
                                  state=LBStatus.PENDING_UPDATE,
                                  resp_code=requests.codes.ok)

        # Wait for the LB to be ACTIVE
        response = self.lbaas_provider.wait_for_status(lb_id)
        self.validate_lb_response(response=response, lb_args=lb_args,
                                  state=LBStatus.ACTIVE,
                                  resp_code=requests.codes.ok)

        # Delete the LB
        response = self.client.delete_load_balancer(lb_id)
        self.validate_lb_response(response=response,
                                  resp_code=requests.codes.accepted)

        # Verify LB is being DELETED
        response = self.client.get_load_balancer(lb_id)
        self.validate_lb_response(response=response,
                                  lb_args=lb_args,
                                  state=LBStatus.PENDING_DELETE,
                                  resp_code=requests.codes.ok)

        # Wait for LB to be DELETED
        response = self.lbaas_provider.wait_for_status(lb_id, LBStatus.DELETED)
        self.validate_lb_response(response=response,
                                  state=LBStatus.DELETED,
                                  resp_code=requests.codes.ok)

        # Verify LB is not in list of ACTIVE LBs
        response = self.client.list_load_balancers()
        lb_id_list = [l_bal.id for l_bal in response.entity]
        self.assertNotIn(lb_id, lb_id_list,
                         'DELETED Load balancer in load balancers list.')

        self.lbs_to_delete = [lb for lb in self.lbs_to_delete if lb != lb_id]

    @attr('nodeless', 'positive', 'smoke')
    def test_delete_nodeless_load_balancer(self):
        response = self.lbaas_provider.create_active_load_balancer(
            nodeless=True)
        lb = response.entity
        self.assertEqual(response.status_code, requests.codes.ok)
        self.lbs_to_delete.append(lb.id)

        response = self.client.delete_load_balancer(lb.id)
        self.assertTrue(response.status_code, requests.codes.accepted)
        self.lbaas_provider.wait_for_status(lb.id, LBStatus.DELETED)
        self.remove_lb_from_list_to_delete(lb.id)

    @attr('nodeless')
    def test_batch_delete_nodeless_load_balancers(self):
        """ Test batch delete of nodeless load balancers """
        lb_list = self.lbaas_provider.create_n_load_balancers(
            n=3, wait_for_active=True, nodeless=True)

        lb_id_list = [lb.id for lb in lb_list
                      if lb.status == LBStatus.ACTIVE]

        response = self.client.batch_delete_load_balancers(lb_id_list)
        self.assertEqual(response.status_code, requests.codes.accepted)

        for lb in lb_list:
            self.lbaas_provider.wait_for_status(lb.id, LBStatus.DELETED)

        response = self.client.list_load_balancers()
        all_lb_ids = [lb.id for lb in response.entity]

        for deleted_lb_id in lb_id_list:
            self.assertNotIn(
                deleted_lb_id, all_lb_ids,
                'Batch deleted load balancer {lb_id} in list LB '
                'call.'.format(lb_id=deleted_lb_id))
            self.remove_lb_from_list_to_delete(lb_id=deleted_lb_id)

    @attr('nodeless')
    def test_batch_delete_mixed_node_load_balancers(self):
        """ Test batch delete of mixed node load balancers """

        lb_list = list()

        for nodeless in [True, False]:
            lb_list.extend(self.lbaas_provider.create_n_load_balancers(
                n=3, wait_for_active=True, nodeless=nodeless))

        lb_id_list = [lb.id for lb in lb_list
                      if lb.status == LBStatus.ACTIVE]
        self.lbs_to_delete.extend(lb_id_list)

        response = self.client.batch_delete_load_balancers(lb_id_list)
        self.assertEqual(response.status_code, requests.codes.accepted)

        for lb in lb_list:
            self.lbaas_provider.wait_for_status(lb.id, LBStatus.DELETED)

        response = self.client.list_load_balancers()
        all_lb_ids = [lb.id for lb in response.entity]

        for deleted_lb_id in lb_id_list:
            self.assertNotIn(
                deleted_lb_id, all_lb_ids,
                'Batch deleted load balancer {lb_id} in list LB '
                'call.'.format(lb_id=deleted_lb_id))

    @attr('nodeless')
    def test_nodeless_ipv6_only_vip_change_protocol(self):
        """ Changing protocol of a LB with only IPV6 Virtual IP """
        virtual_ips = [{'type': LBVipTypes.PUBLIC, 'ipVersion': 'IPV6'}]
        response = self.lbaas_provider.create_active_load_balancer(
            virtualIps=virtual_ips, nodeless=True)
        lb = response.entity
        self.lbs_to_delete.append(lb.id)

        new_protocol = 'FTP'
        response = self.client.update_load_balancer(lb.id,
                                                    protocol=new_protocol)
        self.assertEqual(response.status_code, requests.codes.accepted)
        response = self.lbaas_provider.wait_for_status(lb.id)
        self.assertEqual(response.entity.status, LBStatus.ACTIVE)
        self.assertEqual(response.entity.protocol, new_protocol)

    @attr('nodeless')
    def test_nodeless_load_balancers_return_with_list_of_vips(self):
        """ List nodeless load balancers include virtual ip list """
        lbs = self.client.list_load_balancers().entity
        for lb in lbs:
            self.assertGreater(len(lb.virtualIps), 0)

    @attr('nodeless')
    def test_update_nodeless_load_balancer_to_same_protocol_and_port(self):
        """ Update nodeless load balancer to same protocol and port """
        port = self.lb.port
        protocol = self.lb.protocol
        algorithm = self.lb.algorithm
        r = self.client.update_load_balancer(self.lb.id, port=port,
                                             protocol=protocol)
        self.assertEqual(r.status_code, requests.codes.accepted)
        self.lb = self.lbaas_provider.wait_for_status(self.lb.id).entity
        self.assertEqual(self.lb.status, LBStatus.ACTIVE)
        self.assertEqual(self.lb.port, port)
        self.assertEqual(self.lb.protocol, protocol)
        resp = self.zeus_vs.getBasicInfo([self.zeus_vs_name])
        self.assertEqual(resp[1][0].port, port)
        self.assertEqual(resp[1][0].protocol, Protocol.zeus_name(protocol))
        resp = self.zeus_pool. \
            getLoadBalancingAlgorithm([resp[1][0].default_pool])
        self.assertEqual(resp[1][0], Algorithm.zeus_name(algorithm))

    @attr('nodeless')
    def test_nodeless_load_balancers_all_protocols(self):
        """
        Verify nodelss load balancers created correctly with all protocols

        """
        protocol_list = self.client.list_protocols().entity
        lbs = list()
        lb_ports = list()
        for protocol in protocol_list:
            lb_port = protocol.port
            if protocol.port == 0:
                lb_port = Datagen.random_int(1, 1000)
            lb_ports.append(lb_port)
            lb_args = dict(
                virtualIps=[{'type': LBVipTypes.SERVICENET}],
                nodes=[], protocol=protocol.name, port=lb_port,
                name='cc_{proto_name}'.format(proto_name=protocol.name))

            response = self.client.create_load_balancer(**lb_args)
            self.assertEqual(
                response.status_code,
                requests.codes.accepted,
                'Failed to create load balancer: {proto!s}, {port!s} '
                '{payload}'.format(proto=protocol.name,
                                   port=lb_port,
                                   payload=response.content))

            lbs.append(response.entity)
            self.lbs_to_delete.append(response.entity.id)

        for index in xrange(len(lbs)):
            response = self.lbaas_provider.wait_for_status(lbs[index].id)

            self.assertEqual(
                response.entity.status,
                LBStatus.ACTIVE,
                'Load balancer {id} wrong status ({proto}, {port})'.format(
                    id=lbs[index].id, proto=lbs[index].protocol,
                    port=lbs[index].port))

        for index in range(len(lbs)):
            vs_name = '{0!s}_{1!s}'.format(self.lbaas_provider.tenant_id,
                                           lbs[index].id)
            vs = (self.zeus_vs.getBasicInfo([vs_name]))[1][0]
            self.assertEqual(
                Protocol.zeus_name(lbs[index].protocol),
                vs.protocol,
                'Zeus virtual server does not have correct protocol.')

            self.assertEqual(
                lb_ports[index], int(vs.port),
                'Zeus virtual server does not have correct port.')

    @attr('nodeless')
    def test_nodeless_load_balancer_crud_with_zeus(self):
        """ Create, update, delete nodeless load balancers using Zeus """

        algorithms = self.client.list_algorithms().entity

        lb_args = dict(name='cc_test_create_load_balancer_with_zeus',
                       virtualIps=[{'type': LBVipTypes.PUBLIC}], port=54,
                       nodes=[], protocol='TCP', halfClosed=True, timeout=44,
                       algorithm=Datagen.random_item_in_list(algorithms).name)

        # Create Load Balancer
        lb_response = self.client.create_load_balancer(**lb_args)
        lb_id = lb_response.entity.id
        self.lbs_to_delete.append(lb_id)
        self.validate_lb_response(
            response=lb_response, lb_args=lb_args, state=LBStatus.BUILD,
            resp_code=requests.codes.accepted)

        # Get Load Balancer Info
        lb_response = self.client.get_load_balancer(lb_id)
        self.validate_lb_response(
            response=lb_response, state=LBStatus.BUILD,
            resp_code=requests.codes.ok)

        # Wait for Load Balancer to become ACTIVE
        lb_response = self.lbaas_provider.wait_for_status(lb_id)
        self.validate_lb_response(
            response=lb_response, state=LBStatus.ACTIVE,
            resp_code=requests.codes.ok, lb_args=lb_args)
        self.validate_zeus_response(response=lb_response, lb_args=lb_args)

        lb_args['algorithm'] = Datagen.random_item_in_list(algorithms).name
        lb_args['protocol'] = 'TCP_CLIENT_FIRST'
        lb_args['port'] = 112
        lb_args['halfClosed'] = False
        lb_args['timeout'] = 85
        lb_args['name'] = 'cc_test_create_load_balancer_with_zeus_update'

        # Update Load Balancer Configuration
        lb_response = self.client.update_load_balancer(
            lb_id, algorithm=lb_args['algorithm'],
            protocol=lb_args['protocol'], port=lb_args['port'],
            halfClosed=lb_args['halfClosed'], timeout=lb_args['timeout'],
            name=lb_args['name'])

        self.validate_lb_response(response=lb_response,
                                  resp_code=requests.codes.accepted)

        # Get Load Balancer Information
        lb_response = self.client.get_load_balancer(lb_id)
        self.validate_lb_response(response=lb_response,
                                  resp_code=requests.codes.ok,
                                  state=LBStatus.PENDING_UPDATE)

        # Wait for the Load Balancer to become ACTIVE
        lb_response = self.lbaas_provider.wait_for_status(lb_id)
        self.validate_lb_response(response=lb_response,
                                  resp_code=requests.codes.ok,
                                  state=LBStatus.ACTIVE, lb_args=lb_args)
        self.validate_zeus_response(response=lb_response, lb_args=lb_args)

        # Delete the Load Balancer
        lb_response = self.client.delete_load_balancer(lb_id)
        self.validate_lb_response(response=lb_response,
                                  resp_code=requests.codes.accepted)

        # Verify the load balancer state
        lb_response = self.client.get_load_balancer(lb_id)
        self.validate_lb_response(response=lb_response,
                                  resp_code=requests.codes.ok,
                                  state=LBStatus.PENDING_DELETE)

        # Wait for the load balancer to be deleted
        self.lbaas_provider.wait_for_status(lb_id, LBStatus.DELETED)

        # Verify Zeus acknowledges the deletion
        lb_response = self.zeus_vs.getVirtualServerNames()
        zeus_name = '{0}_{1}'.format(self.tenant_id, lb_id)
        self.assertNotIn(zeus_name, lb_response[1])

        lb_response = self.zeus_vs.getDefaultPool([zeus_name])
        def_pool = lb_response[1][0]

        lb_response = self.zeus_tig.getTrafficIPGroupNames()
        self.assertEqual(len(self.tigroups), 2)
        for tigroup in self.tigroups:
            self.assertNotIn(tigroup, lb_response[1][0])
        lb_response = self.zeus_pool.getPoolNames()
        self.assertNotIn(def_pool, lb_response[1])

    # ----------------- PRIVATE ROUTINES -------------------
    def validate_zeus_response(self, response, lb_args):
        lb = response.entity

        zeus_name = '{0}_{1}'.format(self.tenant_id, lb.id)
        basic_info = self.zeus_vs.getBasicInfo([zeus_name])
        virtual_server = basic_info[1][0]

        self.assertEqual(Protocol.zeus_name(response.entity.protocol),
                         virtual_server.protocol,
                         'Zeus virtual svr does not have correct protocol.')

        self.assertEqual(lb.port, virtual_server.port)

        lb_response = self.zeus_pool.getLoadBalancingAlgorithm(
            [virtual_server.default_pool])
        self.assertEqual(lb_response[1][0], Algorithm.zeus_name(lb.algorithm))
        lb_response = self.zeus_pool.getMaxReplyTime([zeus_name])
        self.assertEqual(lb_response[1][0], lb_args['timeout'])
        lb_response = self.zeus_vs.getProxyClose([zeus_name])
        if 'halfClosed' in lb_args:
            self.assertEqual(lb_response[1][0], lb_args['halfClosed'])
        lb_response = self.zeus_vs.getListenTrafficIPGroups([zeus_name])
        self.tigroups = lb_response[1][0]

        self.assertEqual(len(lb_response[1]), len(lb_args['virtualIps']))
        lb_response = self.zeus_vs.getDefaultPool([zeus_name])
        lb_response = self.zeus_pool.getNodes([lb_response[1][0]])
        self.assertEqual(len(lb_response[1][0]), len(lb_args['nodes']))

    def validate_lb_response(self, response, lb_args=None,
                             state=None, resp_code=requests.codes.ok):

        # Validate the actual response code to the expected response code
        self.assertEqual(response.status_code, resp_code)

        # Validate the LB state
        lb = response.entity
        if state is not None:
            self.assertEqual(lb.status, state,
                             'RESPONSE: {0}'.format(lb))

        # If configuration was returned, validate the configuration
        if lb_args is not None:
            self.assertEqual(lb.name, lb_args['name'])
            self.assertEqual(lb.protocol, lb_args['protocol'])

            num_nodes = 0 if lb.nodes is None else len(lb.nodes)

            self.assertEqual(num_nodes, len(lb_args['nodes']))
            self.assertEqual(lb.port, lb_args['port'])
            self.assertEqual(lb.algorithm, lb_args['algorithm'])
            self.assertEqual(lb.timeout, lb_args['timeout'])
            if 'halfClosed' in lb_args:
                self.assertEqual(lb.halfClosed, lb_args['halfClosed'])

            if lb_args['virtualIps'][0]['type'] == LBVipTypes.SERVICENET:
                self.assertEqual(len(lb.virtualIps), 1)
            else:
                self.assertEqual(len(lb.virtualIps), 2)
                self.assertEqual(len(lb.virtualIps.get_ipv4_vips()), 1)
                self.assertEqual(len(lb.virtualIps.get_ipv6_vips()), 1)

    def remove_lb_from_list_to_delete(self, lb_id):
        self.lbs_to_delete = [id_ for
                              id_ in self.lbs_to_delete if id_ != lb_id]
