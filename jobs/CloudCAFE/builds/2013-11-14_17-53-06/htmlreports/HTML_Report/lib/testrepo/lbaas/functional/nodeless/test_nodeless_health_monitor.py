import requests

from ccengine.common.decorators import attr
from testrepo.common.testfixtures.load_balancers \
    import LoadBalancersZeusFixture


class NodelessHealthMonitorTests(LoadBalancersZeusFixture):
    _HM_PATH = '/'
    _STATUS_REGEX = '.'
    _BODY_REGEX = '.'

    @classmethod
    def setUpClass(cls):
        super(NodelessHealthMonitorTests, cls).setUpClass()
        cls.lb = cls.lbaas_provider.create_active_load_balancer(
            nodeless=True).entity
        cls.lbs_to_delete.append(cls.lb.id)
        cls.zeus_vs_name = '{0}_{1}'.format(cls.tenant_id, cls.lb.id)

    @attr('nodeless')
    def test_passive_health_monitoring_disabled_for_new_lbs(self):
        """ Verify passive health monitoring is disabled for any created LB """
        lb = self.lbaas_provider.create_active_load_balancer(
            nodeless=True).entity
        self.lbs_to_delete.append(lb.id)

        response = self.zeus_pool.getPassiveMonitoring([self.zeus_vs_name])
        self.assertEqual(response[1][0], False)

    @attr('nodeless')
    def test_add_health_monitor_to_nodeless_lb(self):
        """ Try to add health monitor to nodeless LB. LB should be ACTIVE """

        response = self.client.update_health_monitor(
            self.lb.id, attemptsBeforeDeactivation=1, bodyRegex='200', delay=1,
            path='/', statusRegex='200', timeout=1, type='HTTP')

        self.assertEqual(response.status_code, requests.codes.accepted)
        self.lbaas_provider.wait_for_status(self.lb.id)

        response = self.client.delete_health_monitor(self.lb.id)
        self.assertEqual(response.status_code, requests.codes.accepted)
        self.lbaas_provider.wait_for_status(self.lb.id)

    @attr('nodeless')
    def test_remove_last_node_with_health_monitor(self):
        """
        Verify can delete node with health monitor, and then delete
        the health monitor
        """
        response = self.client.add_nodes(self.lb.id, address="100.0.10.100",
                                         condition='ENABLED',
                                         port=self.lb.port)
        self.assertEqual(response.status_code, requests.codes.accepted)
        self.lbaas_provider.wait_for_status(self.lb.id)

        node_id = response.entity[0].id
        response = self.client.update_health_monitor(
            self.lb.id, attemptsBeforeDeactivation=1, bodyRegex='200', delay=1,
            path='/', statusRegex='200', timeout=1, type='HTTP')
        self.assertEqual(response.status_code, requests.codes.accepted)
        self.lbaas_provider.wait_for_status(self.lb.id)

        response = self.client.delete_node(self.lb.id, node_id=node_id)
        self.assertEqual(response.status_code, requests.codes.accepted)
        self.lbaas_provider.wait_for_status(self.lb.id)

        response = self.client.delete_health_monitor(self.lb.id)
        self.assertEqual(response.status_code, requests.codes.accepted)
