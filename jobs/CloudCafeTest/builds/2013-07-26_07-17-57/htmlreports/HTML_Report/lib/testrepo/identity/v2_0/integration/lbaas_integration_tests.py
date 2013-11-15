'''
Created on Mar 14, 2013

@author: vara.chinnappareddy
'''
from ccengine.common.decorators import attr
from ccengine.domain.types import LoadBalancerStatusTypes as LBStatus
from testrepo.common.testfixtures.identity.v2_0.identity \
    import IdentityLbaaSIntegrationFixture


class CreateLoadBalancerTest(IdentityLbaaSIntegrationFixture):

    lbs_to_delete = []
    servers_to_delete = []

    @classmethod
    def setUpClass(cls):
        super(CreateLoadBalancerTest, cls).setUpClass()
        cls.lb = cls.lbaas_provider.create_active_load_balancer().entity
        cls.lbs_to_delete.append(cls.lb.id)
        cls.zeus_vs_name = '{0}_{1}'.format(cls.tenant_id, cls.lb.id)

    @attr('smoke', 'positive')
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
        self.assertEquals(len(r.entity.virtualIps), 1)
        r = self.lbaas_provider.wait_for_status(lb.id)
        self.assertEquals(r.status_code, 200)
        self.assertEquals(r.entity.status, LBStatus.ACTIVE)
        self.assertEquals(r.entity.name, name)
        self.assertEquals(r.entity.protocol, protocol)
        self.assertEquals(len(r.entity.nodes), 2)
        self.assertEquals(r.entity.port, 80)
        self.assertEquals(len(r.entity.virtualIps), 1)
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
        self.assertEquals(len(r.entity.virtualIps), 1)
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
