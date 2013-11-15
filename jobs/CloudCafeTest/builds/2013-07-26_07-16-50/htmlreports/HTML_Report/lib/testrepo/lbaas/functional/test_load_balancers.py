from ccengine.domain.lbaas.load_balancer import LoadBalancer
from ccengine.domain.lbaas.node import Node, NodeList
from ccengine.domain.lbaas.virtual_ip import VirtualIpList, VirtualIp
from testrepo.common.testfixtures.load_balancers \
    import LoadBalancersZeusFixture
from ccengine.common.decorators import attr
import ccengine.common.tools.datagen as datagen
from ccengine.domain.lbaas.protocol import Protocol
from ccengine.domain.lbaas.algorithm import Algorithm
from ccengine.domain.types import LoadBalancerStatusTypes as LBStatus, \
    LoadBalancerVirtualIpTypes as LBVipTypes, \
    LoadBalancerNodeConditions as LBNCondits, \
    LoadBalancerHealthMonitorTypes as LBHMTypes, \
    LoadBalancerAccessListTypes as LBALTypes, \
    LoadBalancerSessionPersistenceTypes as LBSPTypes
from ccengine.clients.base_client import BaseRESTClient


class TestLoadBalancers(LoadBalancersZeusFixture):

    @classmethod
    def setUpClass(cls):
        super(TestLoadBalancers, cls).setUpClass()
        cls.lb = cls.lbaas_provider.create_active_load_balancer().entity
        cls.lbs_to_delete.append(cls.lb.id)
        cls.zeus_vs_name = '{0}_{1}'.format(cls.tenant_id, cls.lb.id)

    @attr('positive')
    def test_lb_crud_ops(self):
        '''Test create, update, get, and delete of a load balancer.'''
        name = 'cc_crud_lb'
        nodes = [{'address': self.config.lbaas_api.live_node1,
                  'port': '80', 'condition': 'ENABLED'},
                 {'address': self.config.lbaas_api.live_node2,
                  'port': '80', 'condition': 'ENABLED'}]
        protocol = 'HTTP'
        virtualIps = [{'type': self.default_vip_type}]
        r = self.client.create_load_balancer(name=name,
                                             nodes=nodes,
                                             protocol=protocol,
                                             virtualIps=virtualIps)
        lb = r.entity
        self.assertEquals(r.status_code, 202)
        self.assertEquals(r.entity.status, LBStatus.BUILD)
        self.assertEquals(r.entity.name, name)
        self.assertEquals(r.entity.protocol, protocol)
        self.assertEquals(len(r.entity.nodes), 2)
        self.assertEquals(r.entity.port, 80)
        if virtualIps[0]['type'] == LBVipTypes.SERVICENET:
            self.assertEquals(len(r.entity.virtualIps), 1)
        else:
            self.assertEquals(len(r.entity.virtualIps), 2)
        r = self.lbaas_provider.wait_for_status(lb.id)
        self.assertEquals(r.status_code, 200)
        self.assertEquals(r.entity.status, LBStatus.ACTIVE)
        self.assertEquals(r.entity.name, name)
        self.assertEquals(r.entity.protocol, protocol)
        self.assertEquals(len(r.entity.nodes), 2)
        self.assertEquals(r.entity.port, 80)
        if virtualIps[0]['type'] == LBVipTypes.SERVICENET:
            self.assertEquals(len(r.entity.virtualIps), 1)
        else:
            self.assertEquals(len(r.entity.virtualIps), 2)
        r = self.client.list_load_balancers()
        lb_id_list = [l_bal.id for l_bal in r.entity]
        self.assertIn(lb.id, lb_id_list,
                      'NON-DELETED Load balancer not in load balancers list.')
        new_name = 'cc_update_crud_lb'
        new_port = 79
        new_protocol = 'HTTPS'
        new_algorithm = 'RANDOM'
        new_timeout = 55
        r = self.client.update_load_balancer(lb.id,
                                             name=new_name,
                                             port=new_port,
                                             protocol=new_protocol,
                                             algorithm=new_algorithm,
                                             timeout=new_timeout)
        self.assertEquals(r.status_code, 202)
        r = self.client.get_load_balancer(lb.id)
        self.assertEquals(r.entity.status, LBStatus.PENDING_UPDATE)
        self.assertEquals(r.entity.name, new_name)
        self.assertEquals(r.entity.protocol, new_protocol)
        self.assertEquals(len(r.entity.nodes), 2)
        self.assertEquals(r.entity.port, new_port)
        if virtualIps[0]['type'] == LBVipTypes.SERVICENET:
            self.assertEquals(len(r.entity.virtualIps), 1)
        else:
            self.assertEquals(len(r.entity.virtualIps), 2)
        self.assertEquals(r.entity.algorithm, new_algorithm)
        self.assertEquals(r.entity.timeout, new_timeout)
        r = self.lbaas_provider.wait_for_status(lb.id)
        self.assertEquals(r.status_code, 200)
        self.assertEquals(r.entity.status, LBStatus.ACTIVE)
        r = self.client.delete_load_balancer(lb.id)
        self.assertEquals(r.status_code, 202)
        r = self.client.get_load_balancer(lb.id)
        self.assertEquals(r.status_code, 200)
        self.assertEquals(r.entity.status, LBStatus.PENDING_DELETE)
        r = self.lbaas_provider.wait_for_status(lb.id, LBStatus.DELETED)
        self.assertEquals(r.status_code, 200)
        self.assertEquals(r.entity.status, LBStatus.DELETED)
        r = self.client.list_load_balancers()
        lb_id_list = [l_bal.id for l_bal in r.entity]
        self.assertNotIn(lb.id, lb_id_list,
                         'DELETED Load balancer in load balancers list.')

    @attr('positive')
    def test_batch_delete_load_balancers(self):
        '''Test batch delete of load balancers'''
        new_lb_list = self.lbaas_provider.\
            create_n_load_balancers(n=3, wait_for_active=True)
        lb_id_list = [lb.id for lb in new_lb_list
                      if lb.status == LBStatus.ACTIVE]
        r = self.client.batch_delete_load_balancers(lb_id_list)
        self.assertEquals(r.status_code, 202)
        for lb in new_lb_list:
            self.lbaas_provider.wait_for_status(lb.id, LBStatus.DELETED)
        r = self.client.list_load_balancers()
        all_lb_ids = [loadbalancer.id for loadbalancer in r.entity]
        for deleted_lb_id in lb_id_list:
            self.assertNotIn(deleted_lb_id, all_lb_ids,
                             'Batch deleted load balancer in list LB call.')

    @attr('positive')
    def test_load_balancers_all_protocols(self):
        '''Verify load balancers created correctly with all protocols.'''
        protocol_list = self.client.list_protocols().entity
        lbs = []
        lb_ports = []
        for protocol in protocol_list:
            lb_port = protocol.port
            if protocol.port == 0:
                lb_port = datagen.random_int(1, 1000)
            lb_ports.append(lb_port)
            virtualIps = [{'type': LBVipTypes.SERVICENET}]
            nodes = [{'address': '10.1.1.1', 'condition': 'ENABLED',
                      'port': 80}]
            r = self.client.create_load_balancer(name='cc_' + protocol.name,
                                                 virtualIps=virtualIps,
                                                 nodes=nodes,
                                                 protocol=protocol.name,
                                                 port=lb_port)
            self.assertEquals(r.status_code, 202, 'Failed to create load ' +
                              'balancer: %s, %s: %s' % (str(protocol.name),
                                                        str(lb_port),
                                                        r.content))
            lbs.append(r.entity)
            self.lbs_to_delete.append(r.entity.id)
        for i in range(len(lbs)):
            r = self.lbaas_provider.wait_for_status(lbs[i].id)
            self.assertEquals(r.entity.status, LBStatus.ACTIVE,
                              'Load balancer %s wrong status (%s, %s)' %
                              (str(lbs[i].id), str(lbs[i].protocol),
                               str(lbs[i].port)))
        for i in range(len(lbs)):
            vs_name = '_'.join([str(self.lbaas_provider.tenant_id),
                                str(lbs[i].id)])
            basic_info = self.zeus_vs.getBasicInfo([vs_name])
            vs = basic_info[1][0]
            self.assertEquals(Protocol.zeus_name(lbs[i].protocol),
                              vs.protocol, 'Zeus virtual server ' +
                              'does not have correct protocol.')
            self.assertEquals(lb_ports[i], int(vs.port), 'Zeus ' +
                              'virtual server does not have correct port.')

    @attr('positive')
    def test_ipv6_only_vip_change_protocol(self):
        '''Changing protocol of a LB with only IPV6 Virtual Ip.'''
        virtualIps = [{'type': LBVipTypes.PUBLIC, 'ipVersion': 'IPV6'}]
        r = self.lbaas_provider.\
            create_active_load_balancer(virtualIps=virtualIps)
        lb = r.entity
        self.lbs_to_delete.append(lb.id)
        r = self.client.update_load_balancer(lb.id, protocol='FTP')
        self.assertEquals(r.status_code, 202)
        r = self.lbaas_provider.wait_for_status(lb.id)
        self.assertEquals(r.entity.status, LBStatus.ACTIVE)

    @attr('positive')
    def test_default_request_format(self):
        '''Default format type is JSON'''
        requestslib_kwargs = {'headers':
                              {'X-Auth-Token': self.client.auth_token,
                               'Accept': ''}}
        r = self.client.\
            list_load_balancers(requestslib_kwargs=requestslib_kwargs)
        self.assertEquals(r.status_code, 200)
        self.assertIsNotNone(r.entity)
        self.assertEquals(r.headers.get('Content-Type'), 'application/json')

    @attr('positive')
    def test_format_extension(self):
        '''Verify format extension (.json|.xml) returns correct format.'''
        rest_client = BaseRESTClient()
        headers = {'X-Auth-Token': self.client.auth_token,
                   'Accept': ''}
        r = rest_client.get('/'.join([self.client.base_url,
                                      'loadbalancers.json']), headers=headers)
        self.assertEquals(r.headers.get('Content-Type'), 'application/json')
        r = rest_client.get('/'.join([self.client.base_url,
                                      'loadbalancers.xml']), headers=headers)
        self.assertEquals(r.headers.get('Content-Type'), 'application/xml')

    @attr('positive')
    def test_load_balancers_return_with_list_of_vips(self):
        '''List load balancers include virtual ip list.'''
        lbs = self.client.list_load_balancers().entity
        for lb in lbs:
            self.assertGreater(len(lb.virtualIps), 0)

    @attr('positive')
    def test_load_balancer_crud_with_zeus(self):
        '''Verify load balancer and properties are set up correctly in zeus.'''
        virtualIps = [{'type': LBVipTypes.PUBLIC}]
        nodes = [{'address': '50.1.1.1', 'port': 80,
                  'condition': LBNCondits.ENABLED},
                 {'address': '50.1.1.2', 'port': 80,
                  'condition': LBNCondits.ENABLED}]
        algorithms = self.client.list_algorithms().entity
        algorithm = datagen.random_item_in_list(algorithms).name
        protocol = 'TCP'
        port = 54
        halfClosed = True
        timeout = 44
        name = 'cc_test_create_load_balancer_with_zeus'
        r = self.client.create_load_balancer(name=name, nodes=nodes,
                                             protocol=protocol,
                                             virtualIps=virtualIps,
                                             halfClosed=halfClosed,
                                             algorithm=algorithm,
                                             port=port, timeout=timeout)
        self.assertEquals(r.status_code, 202)
        new_lb = r.entity
        self.lbs_to_delete.append(new_lb.id)
        self.assertEquals(new_lb.name, name)
        self.assertEquals(new_lb.algorithm, algorithm)
        self.assertEquals(new_lb.port, port)
        self.assertEquals(new_lb.protocol, protocol)
        self.assertEquals(new_lb.halfClosed, halfClosed)
        self.assertEquals(new_lb.timeout, timeout)
        self.assertEquals(len(new_lb.virtualIps), 2)
        self.assertEquals(len(new_lb.virtualIps.get_ipv4_vips()), 1)
        self.assertEquals(len(new_lb.virtualIps.get_ipv6_vips()), 1)
        self.assertEquals(len(new_lb.nodes), 2)
        node1 = new_lb.nodes.get_by_address(nodes[0].get('address'))
        node2 = new_lb.nodes.get_by_address(nodes[1].get('address'))
        self.assertIsNotNone(node1)
        self.assertIsNotNone(node2)
        r = self.client.get_load_balancer(new_lb.id)
        self.assertEquals(r.status_code, 200)
        self.assertEquals(r.entity.status, LBStatus.BUILD)
        r = self.lbaas_provider.wait_for_status(new_lb.id)
        self.assertEquals(r.entity.status, LBStatus.ACTIVE)
        new_lb = r.entity
        self.assertEquals(new_lb.name, name)
        self.assertEquals(new_lb.algorithm, algorithm)
        self.assertEquals(new_lb.port, port)
        self.assertEquals(new_lb.protocol, protocol)
        self.assertEquals(new_lb.halfClosed, halfClosed)
        self.assertEquals(new_lb.timeout, timeout)
        self.assertEquals(len(new_lb.virtualIps), 2)
        self.assertEquals(len(new_lb.virtualIps.get_ipv4_vips()), 1)
        self.assertEquals(len(new_lb.virtualIps.get_ipv6_vips()), 1)
        self.assertEquals(len(new_lb.nodes), 2)
        node1 = new_lb.nodes.get_by_address(nodes[0].get('address'))
        node2 = new_lb.nodes.get_by_address(nodes[1].get('address'))
        self.assertIsNotNone(node1)
        self.assertIsNotNone(node2)
        new_lb_zeus_name = '{0}_{1}'.format(self.tenant_id, new_lb.id)
        basic_info = self.zeus_vs.getBasicInfo([new_lb_zeus_name])
        vs = basic_info[1][0]
        self.assertEquals(Protocol.zeus_name(new_lb.protocol),
                          vs.protocol, 'Zeus virtual server ' +
                          'does not have correct protocol.')
        self.assertEquals(new_lb.port, vs.port)
        resp = self.zeus_pool.getLoadBalancingAlgorithm([vs.default_pool])
        self.assertEquals(resp[1][0], Algorithm.zeus_name(new_lb.algorithm))
        resp = self.zeus_pool.getMaxReplyTime([new_lb_zeus_name])
        self.assertEquals(resp[1][0], timeout)
        resp = self.zeus_vs.getProxyClose([new_lb_zeus_name])
        self.assertEquals(resp[1][0], halfClosed)
        resp = self.zeus_vs.getListenTrafficIPGroups([new_lb_zeus_name])
        self.assertEquals(len(resp[1]), len(virtualIps))
        resp = self.zeus_vs.getDefaultPool([new_lb_zeus_name])
        def_pool = resp[1][0]
        resp = self.zeus_pool.getNodes([def_pool])
        self.assertEquals(len(resp[1][0]), len(nodes))
        algorithms = self.client.list_algorithms().entity
        algorithm = datagen.random_item_in_list(algorithms).name
        protocol = 'TCP_CLIENT_FIRST'
        port = 112
        halfClosed = False
        timeout = 85
        name = 'cc_test_create_load_balancer_with_zeus_update'
        r = self.client.update_load_balancer(new_lb.id,
                                             name=name, protocol=protocol,
                                             algorithm=algorithm,
                                             timeout=timeout,
                                             halfClosed=halfClosed, port=port)
        self.assertEquals(r.status_code, 202)
        r = self.client.get_load_balancer(new_lb.id)
        self.assertEquals(r.status_code, 200)
        self.assertEquals(r.entity.status, LBStatus.PENDING_UPDATE)
        new_lb = self.lbaas_provider.wait_for_status(new_lb.id).entity
        self.assertEquals(new_lb.status, LBStatus.ACTIVE)
        self.assertEquals(new_lb.name, name)
        self.assertEquals(new_lb.algorithm, algorithm)
        self.assertEquals(new_lb.port, port)
        self.assertEquals(new_lb.protocol, protocol)
        self.assertEquals(new_lb.halfClosed, halfClosed)
        self.assertEquals(new_lb.timeout, timeout)
        self.assertEquals(len(new_lb.virtualIps), 2)
        self.assertEquals(len(new_lb.virtualIps.get_ipv4_vips()), 1)
        self.assertEquals(len(new_lb.virtualIps.get_ipv6_vips()), 1)
        self.assertEquals(len(new_lb.nodes), 2)
        node1 = new_lb.nodes.get_by_address(nodes[0].get('address'))
        node2 = new_lb.nodes.get_by_address(nodes[1].get('address'))
        self.assertIsNotNone(node1)
        self.assertIsNotNone(node2)
        new_lb_zeus_name = '{0}_{1}'.format(self.tenant_id, new_lb.id)
        basic_info = self.zeus_vs.getBasicInfo([new_lb_zeus_name])
        vs = basic_info[1][0]
        self.assertEquals(Protocol.zeus_name(new_lb.protocol),
                          vs.protocol, 'Zeus virtual server ' +
                          'does not have correct protocol.')
        self.assertEquals(new_lb.port, vs.port)
        resp = self.zeus_pool.getLoadBalancingAlgorithm([vs.default_pool])
        self.assertEquals(resp[1][0], Algorithm.zeus_name(new_lb.algorithm))
        resp = self.zeus_pool.getMaxReplyTime([new_lb_zeus_name])
        self.assertEquals(resp[1][0], timeout)
        resp = self.zeus_vs.getProxyClose([new_lb_zeus_name])
        self.assertEquals(resp[1][0], halfClosed)
        resp = self.zeus_vs.getListenTrafficIPGroups([new_lb_zeus_name])
        tigroups = resp[1][0]
        self.assertEquals(len(tigroups), 2)
        resp = self.zeus_vs.getDefaultPool([new_lb_zeus_name])
        def_pool = resp[1][0]
        resp = self.zeus_pool.getNodes([def_pool])
        self.assertEquals(len(resp[1][0]), len(nodes))
        r = self.client.delete_load_balancer(new_lb.id)
        self.assertEquals(r.status_code, 202)
        r = self.client.get_load_balancer(new_lb.id)
        self.assertEquals(r.status_code, 200)
        self.assertEquals(r.entity.status, LBStatus.PENDING_DELETE)
        self.lbaas_provider.wait_for_status(new_lb.id, LBStatus.DELETED)
        resp = self.zeus_vs.getVirtualServerNames()
        self.assertNotIn(new_lb_zeus_name, resp[1])
        resp = self.zeus_tig.getTrafficIPGroupNames()
        for tigroup in tigroups:
            self.assertNotIn(tigroup, resp[1][0])
        resp = self.zeus_pool.getPoolNames()
        self.assertNotIn(def_pool, resp[1])

    @attr('positive')
    def test_create_load_balancer_non_weighted_algorithm(self):
        '''Non weighted algorithm, verify weights with zues.'''
        algorithms = self.client.list_algorithms().entity
        algorithm = datagen.\
            random_item_in_list(algorithms.get_non_weighted()).name
        nodes = [{'address': '50.1.1.1', 'port': 80, 'weight': 10,
                  'condition': LBNCondits.ENABLED},
                 {'address': '50.1.1.2', 'port': 80, 'weight': 5,
                  'condition': LBNCondits.ENABLED}]
        lb = self.lbaas_provider.\
            create_active_load_balancer(algorithm=algorithm,
                                        nodes=nodes).entity
        self.lbs_to_delete.append(lb.id)
        for node in lb.nodes:
            self.assertIsNone(node.weight, 'Node weight should not be ' +
                              'returned for load balancers with ' +
                              'non-weighted algorithms.')
        for node in lb.nodes:
            check_node = self.client.get_node(lb.id, node.id).entity
            if check_node.address == nodes[0]['address']:
                self.assertEquals(check_node.weight, nodes[0]['weight'],
                                  'Node weight should still be stored even '
                                  + ' if non-weighted algorithm is used.')
            if check_node.address == nodes[1]['address']:
                self.assertEquals(check_node.weight, nodes[1]['weight'],
                                  'Node weight should still be stored even '
                                  + ' if non-weighted algorithm is used.')
        new_lb_zeus_name = '{0}_{1}'.format(self.tenant_id, lb.id)
        resp = self.zeus_vs.getDefaultPool([new_lb_zeus_name])
        def_pool = resp[1][0]
        resp = self.zeus_pool.getWeightings([def_pool])
        self.assertEquals(len(lb.nodes), len(resp[1][0]))
        for node in resp[1][0]:
            self.assertEquals(node.weighting, 1, 'Zeus should store the node'
                              + ' weight as 1 for non weighted algorithms.')

    @attr('positive')
    def test_create_load_balancer_weighted_algorithm(self):
        '''Weighted algorithm, verify weights with zues.'''
        algorithms = self.client.list_algorithms().entity
        algorithm = datagen.random_item_in_list(algorithms.get_weighted()).name
        nodes = [{'address': '50.1.1.1', 'port': 80, 'weight': 10,
                  'condition': LBNCondits.ENABLED},
                 {'address': '50.1.1.2', 'port': 80, 'weight': 5,
                  'condition': LBNCondits.ENABLED}]
        lb = self.lbaas_provider.\
            create_active_load_balancer(algorithm=algorithm,
                                        nodes=nodes).entity
        self.lbs_to_delete.append(lb.id)
        for node in lb.nodes:
            self.assertIsNotNone(node.weight, 'Node weight should be ' +
                                 'returned for load balancers with ' +
                                 'weighted algorithms.')
            if node.address == nodes[0]['address']:
                self.assertEquals(node.weight, nodes[0]['weight'],
                                  'Node weight should still be stored even '
                                  + ' if non-weighted algorithm is used.')
            if node.address == nodes[1]['address']:
                self.assertEquals(node.weight, nodes[1]['weight'],
                                  'Node weight should still be stored even '
                                  + ' if non-weighted algorithm is used.')
        for node in lb.nodes:
            check_node = self.client.get_node(lb.id, node.id).entity
            if check_node.address == nodes[0]['address']:
                self.assertEquals(check_node.weight, nodes[0]['weight'],
                                  'Node weight should still be stored even '
                                  + ' if non-weighted algorithm is used.')
            if check_node.address == nodes[1]['address']:
                self.assertEquals(check_node.weight, nodes[1]['weight'],
                                  'Node weight should still be stored even '
                                  + ' if non-weighted algorithm is used.')
        new_lb_zeus_name = '{0}_{1}'.format(self.tenant_id, lb.id)
        resp = self.zeus_vs.getDefaultPool([new_lb_zeus_name])
        def_pool = resp[1][0]
        resp = self.zeus_pool.getWeightings([def_pool])
        self.assertEquals(len(lb.nodes), len(resp[1][0]))
        for node in resp[1][0]:
            if nodes[0]['address'] in node.node:
                self.assertEquals(node.weighting, nodes[0]['weight'],
                                  'Zeus should store specified node weight '
                                  + 'for weighted algorithms')
            if nodes[1]['address'] in node.node:
                self.assertEquals(node.weighting, nodes[1]['weight'],
                                  'Zeus should store specified node weight '
                                  + 'for weighted algorithms')

    @attr('positive')
    def test_update_load_balancer_to_same_protocol_and_port(self):
        '''Update load balancer to same protocol and port.'''
        port = self.lb.port
        protocol = self.lb.protocol
        algorithm = self.lb.algorithm
        r = self.client.update_load_balancer(self.lb.id, port=port,
                                             protocol=protocol)
        self.assertEquals(r.status_code, 202)
        self.lb = self.lbaas_provider.wait_for_status(self.lb.id).entity
        self.assertEquals(self.lb.status, LBStatus.ACTIVE)
        self.assertEquals(self.lb.port, port)
        self.assertEquals(self.lb.protocol, protocol)
        resp = self.zeus_vs.getBasicInfo([self.zeus_vs_name])
        self.assertEquals(resp[1][0].port, port)
        self.assertEquals(resp[1][0].protocol, Protocol.zeus_name(protocol))
        resp = self.zeus_pool.\
            getLoadBalancingAlgorithm([resp[1][0].default_pool])
        self.assertEquals(resp[1][0], Algorithm.zeus_name(algorithm))

    @attr('positive')
    def test_create_load_balancer_with_access_list(self):
        '''Verify Access List on load balancer create.'''
        name = 'cc_create_lb_access_list'
        nodes = [{'address': self.config.lbaas_api.live_node1,
                  'port': '80', 'condition': 'ENABLED'},
                 {'address': self.config.lbaas_api.live_node2,
                  'port': '80', 'condition': 'ENABLED'}]
        protocol = 'HTTPS'
        virtualIps = [{'type': self.default_vip_type}]
        accessList = [{'address': '10.1.1.1', 'type': LBALTypes.ALLOW},
                      {'address': '10.1.1.2', 'type': LBALTypes.DENY}]
        r = self.client.create_load_balancer(name=name,
                                             nodes=nodes,
                                             protocol=protocol,
                                             virtualIps=virtualIps,
                                             accessList=accessList)
        self.assertEquals(r.status_code, 202)
        self.lbs_to_delete.append(r.entity.id)
        al_lb = r.entity
        ntwrk_item1 = al_lb.accessList.get_by_address(accessList[0]['address'])
        ntwrk_item2 = al_lb.accessList.get_by_address(accessList[1]['address'])
        self.assertIsNotNone(ntwrk_item1, 'Network item was not found in ' +
                             'access list on create lb response.')
        self.assertIsNotNone(ntwrk_item2, 'Network item was not found in ' +
                             'access list on create lb response.')
        self.assertEquals(ntwrk_item1.type, accessList[0]['type'],
                          'Access list type not stored correctly for item.')
        self.assertEquals(ntwrk_item2.type, accessList[1]['type'],
                          'Access list type not stored correctly for item.')
        al_lb = self.lbaas_provider.wait_for_status(al_lb.id).entity
        self.assertEquals(al_lb.status, LBStatus.ACTIVE, 'LB did not go ' +
                          'ACTIVE after create of lb with access list.')
        ntwrk_item1 = al_lb.accessList.get_by_address(accessList[0]['address'])
        ntwrk_item2 = al_lb.accessList.get_by_address(accessList[1]['address'])
        self.assertIsNotNone(ntwrk_item1, 'Network item was not found in ' +
                             'access list on create lb response.')
        self.assertIsNotNone(ntwrk_item2, 'Network item was not found in ' +
                             'access list on create lb response.')
        self.assertEquals(ntwrk_item1.type, accessList[0]['type'],
                          'Access list type not stored correctly for item.')
        self.assertEquals(ntwrk_item2.type, accessList[1]['type'],
                          'Access list type not stored correctly for item.')
        r = self.client.get_access_list(al_lb.id)
        self.assertEquals(r.status_code, 200)
        access_list = r.entity
        ntwrk_item1 = access_list.get_by_address(accessList[0]['address'])
        ntwrk_item2 = access_list.get_by_address(accessList[1]['address'])
        self.assertIsNotNone(ntwrk_item1, 'Network item was not found in ' +
                             'access list on create lb response.')
        self.assertIsNotNone(ntwrk_item2, 'Network item was not found in ' +
                             'access list on create lb response.')
        self.assertEquals(ntwrk_item1.type, accessList[0]['type'],
                          'Access list type not stored correctly for item.')
        self.assertEquals(ntwrk_item2.type, accessList[1]['type'],
                          'Access list type not stored correctly for item.')
        new_zeus_vs_name = '{0}_{1}'.format(self.tenant_id, al_lb.id)
        resp = self.zeus_protection.getAllowedAddresses([new_zeus_vs_name])
        self.assertIn(accessList[0]['address'], resp[1][0], 'Allowed access '
                      + 'list item not in zeus allowed addresses list.')
        resp = self.zeus_protection.getBannedAddresses([new_zeus_vs_name])
        self.assertIn(accessList[1]['address'], resp[1][0], 'Denied access '
                      + 'list item not in zeus banned addresses list.')
        r = self.client.delete_load_balancer(al_lb.id)
        self.assertEquals(r.status_code, 202)
        self.lbaas_provider.wait_for_status(al_lb.id, LBStatus.DELETED)
        self.lbs_to_delete.pop()
        resp = self.zeus_protection.getAllowedAddresses([new_zeus_vs_name])
        self.assertEquals(resp[0], 500, 'Zeus did not delete virtual server' +
                          ' allowed list.')
        resp = self.zeus_protection.getBannedAddresses([new_zeus_vs_name])
        self.assertEquals(resp[0], 500, 'Zeus did not delete virtual server' +
                          ' banned list.')

    @attr('positive')
    def test_create_load_balancer_with_connect_health_monitor(self):
        '''Verify CONNECT health monitor on load balancer create.'''
        name = 'cc_crud_lb'
        nodes = [{'address': self.config.lbaas_api.live_node1,
                  'port': '80', 'condition': 'ENABLED'},
                 {'address': self.config.lbaas_api.live_node2,
                  'port': '80', 'condition': 'ENABLED'}]
        protocol = 'HTTP'
        virtualIps = [{'type': self.default_vip_type}]
        healthMonitor = {'type': LBHMTypes.CONNECT,
                         'delay': datagen.random_int(1, 3600),
                         'timeout': datagen.random_int(1, 300),
                         'attemptsBeforeDeactivation':
                         datagen.random_int(1, 10)}
        r = self.client.create_load_balancer(name=name,
                                             nodes=nodes,
                                             protocol=protocol,
                                             virtualIps=virtualIps,
                                             healthMonitor=healthMonitor)
        self.assertEquals(r.status_code, 202)
        self.lbs_to_delete.append(r.entity.id)
        hm_lb = r.entity
        self.assertEquals(hm_lb.healthMonitor.type, healthMonitor['type'],
                          'Response from create LB request.')
        self.assertEquals(hm_lb.healthMonitor.delay, healthMonitor['delay'],
                          'Response from create LB request.')
        self.assertEquals(hm_lb.healthMonitor.timeout,
                          healthMonitor['timeout'],
                          'Response from create LB request.')
        self.assertEquals(hm_lb.healthMonitor.attemptsBeforeDeactivation,
                          healthMonitor['attemptsBeforeDeactivation'],
                          'Response from create LB request.')
        hm_lb = self.lbaas_provider.wait_for_status(hm_lb.id).entity
        self.assertEquals(hm_lb.status, LBStatus.ACTIVE)
        self.assertEquals(hm_lb.healthMonitor.type, healthMonitor['type'],
                          'Response after LB is created and ACTIVE.')
        self.assertEquals(hm_lb.healthMonitor.delay, healthMonitor['delay'],
                          'Response after LB is created and ACTIVE.')
        self.assertEquals(hm_lb.healthMonitor.timeout,
                          healthMonitor['timeout'],
                          'Response after LB is created and ACTIVE.')
        self.assertEquals(hm_lb.healthMonitor.attemptsBeforeDeactivation,
                          healthMonitor['attemptsBeforeDeactivation'],
                          'Response after LB is created and ACTIVE.')
        new_zeus_vs_name = '{0}_{1}'.format(self.tenant_id, hm_lb.id)
        resp = self.zeus_monitor.getCustomMonitorNames()
        self.assertIn(new_zeus_vs_name, resp[1])
        resp = self.zeus_monitor.getType([new_zeus_vs_name])
        self.assertEquals(healthMonitor['type'].lower(), resp[1][0],
                          'Zeus did not store correct health monitor type.')
        resp = self.zeus_monitor.getDelay([new_zeus_vs_name])
        self.assertEquals(healthMonitor['delay'], resp[1][0],
                          'Zeus did not store correct health monitor delay.')
        resp = self.zeus_monitor.getTimeout([new_zeus_vs_name])
        self.assertEquals(healthMonitor['timeout'], resp[1][0],
                          'Zeus did not store correct health monitor timeout.')
        resp = self.zeus_monitor.getFailures([new_zeus_vs_name])
        self.assertEquals(healthMonitor['attemptsBeforeDeactivation'],
                          resp[1][0], 'Zeus did not store correct health ' +
                          'monitor attemptsBeforeDeactivation.')
        r = self.client.delete_load_balancer(hm_lb.id)
        self.assertEquals(r.status_code, 202)
        self.lbs_to_delete.pop(self.lbs_to_delete.index(hm_lb.id))
        self.lbaas_provider.wait_for_status(hm_lb.id, LBStatus.DELETED)
        resp = self.zeus_monitor.getCustomMonitorNames()
        self.assertNotIn(new_zeus_vs_name, resp[1], 'Health monitor not' +
                         ' deleted from zeus after load balancer was deleted.')

    @attr('positive')
    def test_create_load_balancer_with_http_health_monitor(self):
        '''Verify HTTP health monitor on load balancer create.'''
        name = 'cc_crud_lb'
        nodes = [{'address': self.config.lbaas_api.live_node1,
                  'port': '80', 'condition': 'ENABLED'},
                 {'address': self.config.lbaas_api.live_node2,
                  'port': '80', 'condition': 'ENABLED'}]
        protocol = 'HTTP'
        virtualIps = [{'type': self.default_vip_type}]
        healthMonitor = {'type': LBHMTypes.HTTP,
                         'delay': datagen.random_int(1, 3600),
                         'timeout': datagen.random_int(1, 300),
                         'attemptsBeforeDeactivation':
                         datagen.random_int(1, 10),
                         'bodyRegex': '.', 'statusRegex': '.', 'path': '/'}
        r = self.client.create_load_balancer(name=name,
                                             nodes=nodes,
                                             protocol=protocol,
                                             virtualIps=virtualIps,
                                             healthMonitor=healthMonitor)
        self.assertEquals(r.status_code, 202)
        self.lbs_to_delete.append(r.entity.id)
        hm_lb = r.entity
        self.assertEquals(hm_lb.healthMonitor.type, healthMonitor['type'],
                          'Response from create LB request.')
        self.assertEquals(hm_lb.healthMonitor.delay, healthMonitor['delay'],
                          'Response from create LB request.')
        self.assertEquals(hm_lb.healthMonitor.timeout,
                          healthMonitor['timeout'],
                          'Response from create LB request.')
        self.assertEquals(hm_lb.healthMonitor.attemptsBeforeDeactivation,
                          healthMonitor['attemptsBeforeDeactivation'],
                          'Response from create LB request.')
        self.assertEquals(hm_lb.healthMonitor.bodyRegex,
                          healthMonitor['bodyRegex'],
                          'Response from create LB request.')
        self.assertEquals(hm_lb.healthMonitor.statusRegex,
                          healthMonitor['statusRegex'],
                          'Response from create LB request.')
        self.assertEquals(hm_lb.healthMonitor.path,
                          healthMonitor['path'],
                          'Response from create LB request.')
        hm_lb = self.lbaas_provider.wait_for_status(hm_lb.id).entity
        self.assertEquals(hm_lb.status, LBStatus.ACTIVE)
        self.assertEquals(hm_lb.healthMonitor.type, healthMonitor['type'],
                          'Response after LB is created and ACTIVE.')
        self.assertEquals(hm_lb.healthMonitor.delay, healthMonitor['delay'],
                          'Response after LB is created and ACTIVE.')
        self.assertEquals(hm_lb.healthMonitor.timeout,
                          healthMonitor['timeout'],
                          'Response after LB is created and ACTIVE.')
        self.assertEquals(hm_lb.healthMonitor.attemptsBeforeDeactivation,
                          healthMonitor['attemptsBeforeDeactivation'],
                          'Response after LB is created and ACTIVE.')
        self.assertEquals(hm_lb.healthMonitor.bodyRegex,
                          healthMonitor['bodyRegex'],
                          'Response after LB is created and ACTIVE.')
        self.assertEquals(hm_lb.healthMonitor.statusRegex,
                          healthMonitor['statusRegex'],
                          'Response after LB is created and ACTIVE.')
        self.assertEquals(hm_lb.healthMonitor.path,
                          healthMonitor['path'],
                          'Response after LB is created and ACTIVE.')
        new_zeus_vs_name = '{0}_{1}'.format(self.tenant_id, hm_lb.id)
        resp = self.zeus_monitor.getCustomMonitorNames()
        self.assertIn(new_zeus_vs_name, resp[1])
        resp = self.zeus_monitor.getType([new_zeus_vs_name])
        self.assertEquals(healthMonitor['type'].lower(), resp[1][0],
                          'Zeus did not store correct health monitor type.')
        resp = self.zeus_monitor.getDelay([new_zeus_vs_name])
        self.assertEquals(healthMonitor['delay'], resp[1][0],
                          'Zeus did not store correct health monitor delay.')
        resp = self.zeus_monitor.getTimeout([new_zeus_vs_name])
        self.assertEquals(healthMonitor['timeout'], resp[1][0],
                          'Zeus did not store correct health monitor timeout.')
        resp = self.zeus_monitor.getFailures([new_zeus_vs_name])
        self.assertEquals(healthMonitor['attemptsBeforeDeactivation'],
                          resp[1][0], 'Zeus did not store correct health ' +
                          'monitor attemptsBeforeDeactivation.')
        resp = self.zeus_monitor.getBodyRegex([new_zeus_vs_name])
        self.assertEquals(healthMonitor['bodyRegex'], resp[1][0],
                          'Zeus did not store correct health monitor ' +
                          'bodyRegex.')
        resp = self.zeus_monitor.getStatusRegex([new_zeus_vs_name])
        self.assertEquals(healthMonitor['statusRegex'], resp[1][0],
                          'Zeus did not store correct health monitor ' +
                          'statusRegex.')
        resp = self.zeus_monitor.getPath([new_zeus_vs_name])
        self.assertEquals(healthMonitor['path'], resp[1][0],
                          'Zeus did not store correct health monitor path.')
        resp = self.zeus_monitor.getUseSSL([new_zeus_vs_name])
        self.assertFalse(resp[1][0], 'HTTP Health Monitor should not use SSL')
        r = self.client.delete_load_balancer(hm_lb.id)
        self.assertEquals(r.status_code, 202)
        self.lbs_to_delete.pop(self.lbs_to_delete.index(hm_lb.id))
        self.lbaas_provider.wait_for_status(hm_lb.id, LBStatus.DELETED)
        resp = self.zeus_monitor.getCustomMonitorNames()
        self.assertNotIn(new_zeus_vs_name, resp[1], 'Health monitor not' +
                         ' deleted from zeus after load balancer was deleted.')

    @attr('positive')
    def test_create_load_balancer_with_https_health_monitor(self):
        '''Verify HTTPS health monitor on load balancer create.'''
        name = 'cc_crud_lb'
        nodes = [{'address': self.config.lbaas_api.live_node1,
                  'port': '80', 'condition': 'ENABLED'},
                 {'address': self.config.lbaas_api.live_node2,
                  'port': '80', 'condition': 'ENABLED'}]
        protocol = 'HTTPS'
        virtualIps = [{'type': self.default_vip_type}]
        healthMonitor = {'type': LBHMTypes.HTTPS,
                         'delay': datagen.random_int(1, 3600),
                         'timeout': datagen.random_int(1, 300),
                         'attemptsBeforeDeactivation':
                         datagen.random_int(1, 10),
                         'bodyRegex': '.', 'statusRegex': '.', 'path': '/'}
        r = self.client.create_load_balancer(name=name,
                                             nodes=nodes,
                                             protocol=protocol,
                                             virtualIps=virtualIps,
                                             healthMonitor=healthMonitor)
        self.assertEquals(r.status_code, 202)
        self.lbs_to_delete.append(r.entity.id)
        hm_lb = r.entity
        self.assertEquals(hm_lb.healthMonitor.type, healthMonitor['type'],
                          'Response from create LB request.')
        self.assertEquals(hm_lb.healthMonitor.delay, healthMonitor['delay'],
                          'Response from create LB request.')
        self.assertEquals(hm_lb.healthMonitor.timeout,
                          healthMonitor['timeout'],
                          'Response from create LB request.')
        self.assertEquals(hm_lb.healthMonitor.attemptsBeforeDeactivation,
                          healthMonitor['attemptsBeforeDeactivation'],
                          'Response from create LB request.')
        self.assertEquals(hm_lb.healthMonitor.bodyRegex,
                          healthMonitor['bodyRegex'],
                          'Response from create LB request.')
        self.assertEquals(hm_lb.healthMonitor.statusRegex,
                          healthMonitor['statusRegex'],
                          'Response from create LB request.')
        self.assertEquals(hm_lb.healthMonitor.path,
                          healthMonitor['path'],
                          'Response from create LB request.')
        hm_lb = self.lbaas_provider.wait_for_status(hm_lb.id).entity
        self.assertEquals(hm_lb.status, LBStatus.ACTIVE)
        self.assertEquals(hm_lb.healthMonitor.type, healthMonitor['type'],
                          'Response after LB is created and ACTIVE.')
        self.assertEquals(hm_lb.healthMonitor.delay, healthMonitor['delay'],
                          'Response after LB is created and ACTIVE.')
        self.assertEquals(hm_lb.healthMonitor.timeout,
                          healthMonitor['timeout'],
                          'Response after LB is created and ACTIVE.')
        self.assertEquals(hm_lb.healthMonitor.attemptsBeforeDeactivation,
                          healthMonitor['attemptsBeforeDeactivation'],
                          'Response after LB is created and ACTIVE.')
        self.assertEquals(hm_lb.healthMonitor.bodyRegex,
                          healthMonitor['bodyRegex'],
                          'Response after LB is created and ACTIVE.')
        self.assertEquals(hm_lb.healthMonitor.statusRegex,
                          healthMonitor['statusRegex'],
                          'Response after LB is created and ACTIVE.')
        self.assertEquals(hm_lb.healthMonitor.path,
                          healthMonitor['path'],
                          'Response after LB is created and ACTIVE.')
        new_zeus_vs_name = '{0}_{1}'.format(self.tenant_id, hm_lb.id)
        resp = self.zeus_monitor.getCustomMonitorNames()
        self.assertIn(new_zeus_vs_name, resp[1])
        resp = self.zeus_monitor.getType([new_zeus_vs_name])
        # checking against http since getUseSSL determines if it is HTTPS
        self.assertEquals(LBHMTypes.HTTP.lower(), resp[1][0],
                          'Zeus did not store correct health monitor type.')
        resp = self.zeus_monitor.getDelay([new_zeus_vs_name])
        self.assertEquals(healthMonitor['delay'], resp[1][0],
                          'Zeus did not store correct health monitor delay.')
        resp = self.zeus_monitor.getTimeout([new_zeus_vs_name])
        self.assertEquals(healthMonitor['timeout'], resp[1][0],
                          'Zeus did not store correct health monitor timeout.')
        resp = self.zeus_monitor.getFailures([new_zeus_vs_name])
        self.assertEquals(healthMonitor['attemptsBeforeDeactivation'],
                          resp[1][0], 'Zeus did not store correct health ' +
                          'monitor attemptsBeforeDeactivation.')
        resp = self.zeus_monitor.getBodyRegex([new_zeus_vs_name])
        self.assertEquals(healthMonitor['bodyRegex'], resp[1][0],
                          'Zeus did not store correct health monitor ' +
                          'bodyRegex.')
        resp = self.zeus_monitor.getStatusRegex([new_zeus_vs_name])
        self.assertEquals(healthMonitor['statusRegex'], resp[1][0],
                          'Zeus did not store correct health monitor ' +
                          'statusRegex.')
        resp = self.zeus_monitor.getPath([new_zeus_vs_name])
        self.assertEquals(healthMonitor['path'], resp[1][0],
                          'Zeus did not store correct health monitor path.')
        resp = self.zeus_monitor.getUseSSL([new_zeus_vs_name])
        self.assertTrue(resp[1][0], 'HTTPS Health Monitor should use SSL')
        r = self.client.delete_load_balancer(hm_lb.id)
        self.assertEquals(r.status_code, 202)
        self.lbs_to_delete.pop(self.lbs_to_delete.index(hm_lb.id))
        self.lbaas_provider.wait_for_status(hm_lb.id, LBStatus.DELETED)
        resp = self.zeus_monitor.getCustomMonitorNames()
        self.assertNotIn(new_zeus_vs_name, resp[1], 'Health monitor not' +
                         ' deleted from zeus after load balancer was deleted.')

    @attr('positive')
    def test_create_load_balancer_with_connection_logging(self):
        '''Verify connection logging on create load balancer.'''
        name = 'cc_create_lb_connection_logging'
        nodes = [{'address': self.config.lbaas_api.live_node1,
                  'port': '80', 'condition': 'ENABLED'},
                 {'address': self.config.lbaas_api.live_node2,
                  'port': '80', 'condition': 'ENABLED'}]
        protocol = 'HTTPS'
        virtualIps = [{'type': self.default_vip_type}]
        connLogg = {'enabled': True}
        r = self.client.create_load_balancer(name=name,
                                             nodes=nodes,
                                             protocol=protocol,
                                             virtualIps=virtualIps,
                                             connectionLogging=connLogg)
        self.assertEquals(r.status_code, 202)
        self.lbs_to_delete.append(r.entity.id)
        cl_lb = r.entity
        self.assertEquals(cl_lb.connectionLogging.enabled, connLogg['enabled'],
                          'Connection logging incorrect on create load ' +
                          'balancer response')
        cl_lb = self.lbaas_provider.wait_for_status(cl_lb.id).entity
        self.assertEquals(cl_lb.status, LBStatus.ACTIVE, 'LB did not go ' +
                          'ACTIVE after create of lb with connection logging.')
        self.assertEquals(cl_lb.connectionLogging.enabled, connLogg['enabled'],
                          'Connection logging incorrect on get load ' +
                          'balancer response')
        r = self.client.get_connection_logging(cl_lb.id)
        self.assertEquals(r.status_code, 200)
        connection_logging = r.entity
        self.assertEquals(connection_logging.enabled, connLogg['enabled'],
                          'Connection logging incorrect on get connection ' +
                          'logging for load balancer.')
        new_zeus_vs_name = '{0}_{1}'.format(self.tenant_id, cl_lb.id)
        resp = self.zeus_vs.getLogEnabled([new_zeus_vs_name])
        self.assertEquals(connLogg['enabled'], resp[1][0], 'Connection ' +
                          'logging in zeus incorrect for virtual server.')
        r = self.client.delete_load_balancer(cl_lb.id)
        self.assertEquals(r.status_code, 202)
        self.lbaas_provider.wait_for_status(cl_lb.id, LBStatus.DELETED)
        self.lbs_to_delete.pop()
        resp = self.zeus_vs.getLogEnabled([new_zeus_vs_name])
        self.assertEquals(resp[0], 500, 'Zeus did not delete virtual server' +
                          'connection logging.')

    @attr('positive')
    def test_create_load_balancer_with_connection_throttle(self):
        '''Verify connection throttle on create load balancer.'''
        name = 'cc_create_lb_connection_logging'
        nodes = [{'address': self.config.lbaas_api.live_node1,
                  'port': '80', 'condition': 'ENABLED'},
                 {'address': self.config.lbaas_api.live_node2,
                  'port': '80', 'condition': 'ENABLED'}]
        protocol = 'HTTPS'
        virtualIps = [{'type': self.default_vip_type}]
        connThrott = {'minConnections': datagen.random_int(1, 30),
                      'maxConnections': datagen.random_int(31, 100),
                      'maxConnectionRate': datagen.random_int(1, 10),
                      'rateInterval': datagen.random_int(1, 10)}
        r = self.client.create_load_balancer(name=name,
                                             nodes=nodes,
                                             protocol=protocol,
                                             virtualIps=virtualIps,
                                             connectionThrottle=connThrott)
        self.assertEquals(r.status_code, 202)
        self.lbs_to_delete.append(r.entity.id)
        cl_lb = r.entity
        self.assertEquals(cl_lb.connectionThrottle.minConnections,
                          connThrott['minConnections'],
                          'Connection throttle incorrect on create load ' +
                          'balancer response')
        self.assertEquals(cl_lb.connectionThrottle.maxConnections,
                          connThrott['maxConnections'],
                          'Connection throttle incorrect on create load ' +
                          'balancer response')
        self.assertEquals(cl_lb.connectionThrottle.maxConnectionRate,
                          connThrott['maxConnectionRate'],
                          'Connection throttle incorrect on create load ' +
                          'balancer response')
        self.assertEquals(cl_lb.connectionThrottle.rateInterval,
                          connThrott['rateInterval'],
                          'Connection throttle incorrect on create load ' +
                          'balancer response')
        cl_lb = self.lbaas_provider.wait_for_status(cl_lb.id).entity
        self.assertEquals(cl_lb.status, LBStatus.ACTIVE, 'LB did not go ' +
                          'ACTIVE after create of lb with connection logging.')
        self.assertEquals(cl_lb.connectionThrottle.minConnections,
                          connThrott['minConnections'],
                          'Connection throttle incorrect on get load ' +
                          'balancer response')
        self.assertEquals(cl_lb.connectionThrottle.maxConnections,
                          connThrott['maxConnections'],
                          'Connection throttle incorrect on get load ' +
                          'balancer response')
        self.assertEquals(cl_lb.connectionThrottle.maxConnectionRate,
                          connThrott['maxConnectionRate'],
                          'Connection throttle incorrect on get load ' +
                          'balancer response')
        self.assertEquals(cl_lb.connectionThrottle.rateInterval,
                          connThrott['rateInterval'],
                          'Connection throttle incorrect on get load ' +
                          'balancer response')
        r = self.client.get_connection_throttle(cl_lb.id)
        self.assertEquals(r.status_code, 200)
        connection_throttle = r.entity
        self.assertEquals(connection_throttle.minConnections,
                          connThrott['minConnections'],
                          'Connection throttle incorrect on get connection ' +
                          'throttle for load balancer.')
        self.assertEquals(connection_throttle.maxConnections,
                          connThrott['maxConnections'],
                          'Connection throttle incorrect on get connection ' +
                          'throttle for load balancer.')
        self.assertEquals(connection_throttle.maxConnectionRate,
                          connThrott['maxConnectionRate'],
                          'Connection throttle incorrect on get connection ' +
                          'throttle for load balancer.')
        self.assertEquals(connection_throttle.rateInterval,
                          connThrott['rateInterval'],
                          'Connection throttle incorrect on get connection ' +
                          'throttle for load balancer.')
        new_zeus_vs_name = '{0}_{1}'.format(self.tenant_id, cl_lb.id)
        resp = self.zeus_protection.getMinConnections([new_zeus_vs_name])
        self.assertEquals(resp[1][0], connThrott['minConnections'],
                          'Connection throttle in zeus incorrect.')
        resp = self.zeus_protection.getMax1Connections([new_zeus_vs_name])
        self.assertEquals(resp[1][0], connThrott['maxConnections'],
                          'Connection throttle in zeus incorrect.')
        resp = self.zeus_protection.getMaxConnectionRate([new_zeus_vs_name])
        self.assertEquals(resp[1][0], connThrott['maxConnectionRate'],
                          'Connection throttle in zeus incorrect.')
        resp = self.zeus_protection.getRateTimer([new_zeus_vs_name])
        self.assertEquals(resp[1][0], connThrott['rateInterval'],
                          'Connection throttle in zeus incorrect.')
        r = self.client.delete_load_balancer(cl_lb.id)
        self.assertEquals(r.status_code, 202)
        self.lbaas_provider.wait_for_status(cl_lb.id, LBStatus.DELETED)
        self.lbs_to_delete.pop()
        resp = self.zeus_protection.getMinConnections([new_zeus_vs_name])
        self.assertEquals(resp[0], 500, 'Zeus did not delete virtual server' +
                          'connection throttle.')
        resp = self.zeus_protection.getMax1Connections([new_zeus_vs_name])
        self.assertEquals(resp[0], 500, 'Zeus did not delete virtual server' +
                          'connection throttle.')
        resp = self.zeus_protection.getMaxConnectionRate([new_zeus_vs_name])
        self.assertEquals(resp[0], 500, 'Zeus did not delete virtual server' +
                          'connection throttle.')
        resp = self.zeus_protection.getRateTimer([new_zeus_vs_name])
        self.assertEquals(resp[0], 500, 'Zeus did not delete virtual server' +
                          'connection throttle.')

    @attr('positive')
    def test_create_load_balancer_with_session_persistence(self):
        '''Verify session persistence on create load balancer.'''
        name = 'cc_create_lb_connection_logging'
        nodes = [{'address': self.config.lbaas_api.live_node1,
                  'port': '80', 'condition': 'ENABLED'},
                 {'address': self.config.lbaas_api.live_node2,
                  'port': '80', 'condition': 'ENABLED'}]
        protocol = 'HTTP'
        virtualIps = [{'type': self.default_vip_type}]
        sessPers = {'persistenceType': LBSPTypes.HTTP_COOKIE}
        r = self.client.create_load_balancer(name=name,
                                             nodes=nodes,
                                             protocol=protocol,
                                             virtualIps=virtualIps,
                                             sessionPersistence=sessPers)
        self.assertEquals(r.status_code, 202)
        self.lbs_to_delete.append(r.entity.id)
        sp_lb = r.entity
        self.assertEquals(sp_lb.sessionPersistence.persistenceType,
                          sessPers['persistenceType'],
                          'Session persistence incorrect on create load ' +
                          'balancer response')
        sp_lb = self.lbaas_provider.wait_for_status(sp_lb.id).entity
        self.assertEquals(sp_lb.status, LBStatus.ACTIVE, 'LB did not go ACTIVE'
                          + ' after create of lb with session persistence.')
        self.assertEquals(sp_lb.sessionPersistence.persistenceType,
                          sessPers['persistenceType'],
                          'Session persistence incorrect on get load ' +
                          'balancer response')
        r = self.client.get_session_persistence(sp_lb.id)
        self.assertEquals(r.status_code, 200)
        session_persistence = r.entity
        self.assertEquals(session_persistence.persistenceType,
                          sessPers['persistenceType'],
                          'Session persistence incorrect on get connection ' +
                          'logging for load balancer.')
        new_zeus_vs_name = '{0}_{1}'.format(self.tenant_id, sp_lb.id)
        resp = self.zeus_pool.getPersistence([new_zeus_vs_name])
        self.assertEquals(resp[1][0], sessPers['persistenceType'], 'Session ' +
                          'persistence in zeus incorrect for virtual server.')
        r = self.client.delete_load_balancer(sp_lb.id)
        self.assertEquals(r.status_code, 202)
        self.lbaas_provider.wait_for_status(sp_lb.id, LBStatus.DELETED)
        self.lbs_to_delete.pop()
        resp = self.zeus_pool.getPersistence([new_zeus_vs_name])
        self.assertEquals(resp[0], 500, 'Zeus did not delete virtual server' +
                          'connection logging.')

    @attr('positive')
    def test_passive_machine_load_balancer(self):
        '''Verify zeus settings for passive machine are correct.'''
        vip_id = self.lb.virtualIps.get_ipv4_vips()[0].id
        zeus_tig_name = '{0}_{1}'.format(self.tenant_id, vip_id)
        resp = self.zeus_tig.getPassiveMachine([zeus_tig_name])
        self.assertGreater(len(resp[1][0]), 0)

    @attr('positive')
    def test_share_both_vip_types_on_a_load_balancer(self):
        '''Share vip between 2 lbs with different protocols on the same port'''
        lb1, lb2 = self.make_lbs_for_shared_vip_different_protocols()
        r = self.client.create_load_balancer(
            **lb1._obj_to_dict()['loadBalancer'])
        self.assertEquals(r.status_code, 202)
        lb1 = r.entity
        self.lbs_to_delete.append(lb1.id)
        self.lbaas_provider.wait_for_status(lb1.id)
        lb2.virtualIps[0].id = lb1.virtualIps[0].id
        r = self.client.create_load_balancer(
            **lb2._obj_to_dict()['loadBalancer'])
        self.assertEquals(r.status_code, 202)
        lb2 = r.entity
        self.lbs_to_delete.append(lb2.id)
        self.lbaas_provider.wait_for_status(lb2.id)
        r = self.client.delete_load_balancer(lb1.id)
        self.assertEqual(r.status_code, 202)
        r = self.client.delete_load_balancer(lb2.id)
        self.assertEqual(r.status_code, 202)

    @attr('positive')
    def test_update_protocol_on_a_load_balancer_with_only_ipv6_vip(self):
        '''Test the ability to update a load balancer with only an ipv6 vip'''
        r = self.client.create_load_balancer(name="a-new-loadbalancer",
                                             port=53, protocol='UDP',
                                             virtualIps=[
                                                 {'type': 'PUBLIC',
                                                  'ipVersion': 'IPV6'}],
                                             nodes=[{'address': '10.10.1.1',
                                                     'port': 80,
                                                     'condition': 'ENABLED'}])
        self.assertEquals(r.status_code, 202)
        self.lbs_to_delete.append(r.entity.id)
        self.lbaas_provider.wait_for_status(r.entity.id)
        lb = r.entity
        r = self.client.update_load_balancer(lb.id, name="kinda-loadbalancer")
        self.assertEquals(r.status_code, 202)
        self.lbaas_provider.wait_for_status(lb.id)
        r = self.client.get_load_balancer(lb.id)
        self.assertEquals(r.status_code, 200)
        self.assertNotEquals(r.entity.name, lb.name)

    @attr('positive')
    def test_saved_state_on_a_load_balancer(self):
        '''Test that all states are saved on a load balancer'''
        # TODO: work on this in a capacity to work with Cloud Cafe
        state_lb = self.lbaas_provider.create_active_load_balancer().entity
        self.lbs_to_delete.append(state_lb.id)
        updated_port = state_lb.port + 1
        r = self.client.update_load_balancer(load_balancer_id=state_lb.id,
                                             port=updated_port)
        self.assertEquals(r.status_code, 202)
        self.lbaas_provider.wait_for_status(state_lb.id)
        r = self.client.delete_load_balancer(state_lb.id)
        self.assertTrue(r.status_code, 202)
        self.lbaas_provider.wait_for_status(state_lb.id,
                                            status_to_wait_for=
                                            LBStatus.DELETED)
        r = self.mgmt_client.get_load_balancer_state_history(self.tenant_id)
        self.assertEquals(r.status_code, 200)
        history_list = r.entity
        states = {}
        states['ACTIVE'] = False
        states['BUILD'] = False
        states['PENDING_UPDATE'] = False
        states['PENDING_DELETE'] = False
        states['DELETED'] = False
        for item in history_list:
            if item.loadBalancerId == state_lb.id:
                states[item.status] = True
        status_is_false = False
        for key in states.keys():
            if states[key] is False:
                status_is_false = True
                break
        self.assertFalse(status_is_false)

    @attr('positive')
    def test_vips_appear_on_simple_load_balancer(self):
        '''Test vips show when getting all load balancers'''
        r = self.client.list_load_balancers()
        self.assertEquals(r.status_code, 200)
        self.assertTrue(r.entity[0].virtualIps is not None)

    def make_lbs_for_shared_vip_different_protocols(self):
        lb1 = LoadBalancer()
        lb1.name = "a-new-loadbalancer"
        lb1.port = 53
        lb1.protocol = "UDP"
        vip1 = VirtualIp()
        vip1.type = 'PUBLIC'
        lb1.virtualIps = [vip1]
        node1 = Node()
        node1.address = "10.1.1.1"
        node1.port = 80
        node1.condition = "ENABLED"
        lb1.nodes = [node1]
        lb2 = LoadBalancer()
        lb2.name = "a-new-loadbalancer-2"
        lb2.port = 53
        lb2.protocol = "TCP"
        vip2 = VirtualIp()
        lb2.virtualIps = [vip2]
        node2 = Node()
        node2.address = "10.1.1.2"
        node2.port = 81
        node2.condition = "ENABLED"
        lb2.nodes = [node2]
        return lb1, lb2
