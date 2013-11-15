from testrepo.common.testfixtures.load_balancers \
    import LoadBalancersSmokeFixture, LoadBalancersZeusFixture
from ccengine.common.decorators import attr
import ccengine.common.tools.datagen as datagen
from ccengine.domain.lbaas.node import Node
from ccengine.domain.lbaas.health_monitor import HealthMonitor
import time


class HealthMonitorSmokeTests(LoadBalancersSmokeFixture):

    _HM_PATH = '/'
    _STATUS_REGEX = '.'
    _BODY_REGEX = '.'

    @attr('smoke', 'positive')
    def test_update_health_monitor(self):
        """Testing health monitor CRUD operations"""
        path = statusRegex = bodyRegex = None
        if self.lb.protocol == 'HTTP' or self.lb.protocol == 'HTTPS':
            type_ = self.lb.protocol
            path = self._HM_PATH
            statusRegex = self._STATUS_REGEX
            bodyRegex = self._BODY_REGEX
        else:
            type_ = 'CONNECT'
        delay = datagen.random_int(1, 3600)
        timeout = datagen.random_int(1, 300)
        aBD = datagen.random_int(1, 10)
        r = self.client.update_health_monitor(self.lb.id,
                                              attemptsBeforeDeactivation=aBD,
                                              delay=delay, timeout=timeout,
                                              type=type_, path=path,
                                              statusRegex=statusRegex,
                                              bodyRegex=bodyRegex)
        self.assertEquals(r.status_code, 202)
        self.lbaas_provider.wait_for_status(self.lb.id)
        r = self.client.get_health_monitor(self.lb.id)
        created_hm = r.entity
        self.assertEquals(r.status_code, 200)
        self.assertEquals(type_, created_hm.type)
        self.assertEquals(delay, created_hm.delay)
        self.assertEquals(timeout, created_hm.timeout)
        self.assertEquals(aBD, created_hm.attemptsBeforeDeactivation)
        if type_ == 'HTTP' or type_ == 'HTTPS':
            self.assertEquals(path, created_hm.path)
            self.assertEquals(statusRegex, created_hm.statusRegex)
            self.assertEquals(bodyRegex, created_hm.bodyRegex)
        r = self.client.delete_health_monitor(self.lb.id)
        self.assertEquals(r.status_code, 202)
        self.lbaas_provider.wait_for_status(self.lb.id)
        r = self.client.get_health_monitor(self.lb.id)
        self.assertEquals(r.status_code, 200)
        self.assertIsNone(r.entity.type)


class HealthMonitorTests(LoadBalancersZeusFixture):

    _HM_PATH = '/'
    _STATUS_REGEX = '.'
    _BODY_REGEX = '.'

    @classmethod
    def setUpClass(cls):
        super(HealthMonitorTests, cls).setUpClass()
        cls.lb = cls.lbaas_provider.create_active_load_balancer().entity
        cls.lbs_to_delete.append(cls.lb.id)
        cls.zeus_vs_name = '{0}_{1}'.format(cls.tenant_id, cls.lb.id)

    @attr('positive')
    def test_passive_health_monitoring_disabled_for_new_lbs(self):
        '''Verify passive health monitoring is disabled for any created LB.'''
        new_lb = self.lbaas_provider.create_active_load_balancer().entity
        self.lbs_to_delete.append(new_lb.id)
        resp = self.zeus_pool.getPassiveMonitoring([self.zeus_vs_name])
        self.assertEquals(resp[1][0], False)

    @attr('positive')
    def test_node_online_update_after_delete_health_monitor(self):
        '''Verify nodes go online after deleting a health monitor'''
        r = self.client.add_nodes(self.lb.id, address="100.0.10.100",
                                  condition='ENABLED', port=self.lb.port)
        self.assertEquals(r.status_code, 202)
        self.lbaas_provider.wait_for_status(self.lb.id)
        r = self.client.add_nodes(self.lb.id, address="100.0.10.101",
                                  condition='ENABLED', port=self.lb.port)
        self.assertEquals(r.status_code, 202)
        self.lbaas_provider.wait_for_status(self.lb.id)
        r = self.client.update_health_monitor(self.lb.id,
                                              attemptsBeforeDeactivation=1,
                                              bodyRegex='200', delay=1,
                                              path='/', statusRegex='200',
                                              timeout=1, type='HTTP')
        self.assertEquals(r.status_code, 202)
        self.lbaas_provider.wait_for_status(self.lb.id)
        node = Node()
        node2 = Node()
        num_checks = 0
        while num_checks < 20:
            r = self.client.get_load_balancer(self.lb.id)
            self.assertEquals(r.status_code, 200)
            for n in r.entity.nodes:
                if n.status == 'OFFLINE':
                    if n.address == "100.0.10.100":
                        node = n
                    elif n.address == "100.0.10.101":
                        node2 = n
            if node.id is not None and node2.id is not None:
                break
            num_checks += 1
            time.sleep(1)
        if num_checks == 20:
            self.fail("Inaccessible node's status did not go offline"
                      " when health monitoring was enabled.")
        r = self.client.update_node(self.lb.id, node_id=node2.id,
                                    condition='DISABLED')
        self.assertEquals(r.status_code, 202)
        self.lbaas_provider.wait_for_status(self.lb.id)
        r = self.client.delete_health_monitor(self.lb.id)
        self.assertEquals(r.status_code, 202)
        self.lbaas_provider.wait_for_status(self.lb.id)
        r = self.client.get_node(self.lb.id, node_id=node.id)
        self.assertEquals(r.status_code, 200)
        self.assertTrue(r.entity.status == 'ONLINE')
        r = self.client.get_node(self.lb.id, node_id=node2.id)
        self.assertEquals(r.status_code, 200)
        self.assertTrue(r.entity.status == 'OFFLINE')

    @attr('positive')
    def test_node_service_events_include_health_monitor_events(self):
        '''Verify presence of health monitor events'''
        r = self.client.add_nodes(self.lb.id, address="100.0.10.110",
                                  condition='ENABLED', port=self.lb.port)
        self.assertEquals(r.status_code, 202)
        node_id = r.entity[0].id
        self.lbaas_provider.wait_for_status(self.lb.id)
        r = self.client.update_health_monitor(self.lb.id,
                                              attemptsBeforeDeactivation=1,
                                              bodyRegex='200', delay=1,
                                              path='/', statusRegex='200',
                                              timeout=1, type='HTTP')
        self.assertEquals(r.status_code, 202)
        self.lbaas_provider.wait_for_status(self.lb.id)
        r = self.client.list_node_service_events(self.lb.id)
        self.assertEquals(r.status_code, 200)
        for event in r.entity:
            if node_id == event.nodeId:
                self.assertTrue(str(event.accountId) == str(self.tenant_id))
                self.assertTrue(event.loadbalancerId == self.lb.id)
                self.assertTrue(event.nodeId == node_id)
                break
        r = self.client.delete_node(self.lb.id, node_id)
        self.assertEquals(r.status_code, 202)
        self.lbaas_provider.wait_for_status(self.lb.id)
        r = self.client.delete_health_monitor(self.lb.id)
        self.assertEquals(r.status_code, 202)
        self.lbaas_provider.wait_for_status(self.lb.id)
