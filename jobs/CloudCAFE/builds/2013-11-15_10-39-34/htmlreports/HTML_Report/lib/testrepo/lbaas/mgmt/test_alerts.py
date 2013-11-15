from testrepo.common.testfixtures.load_balancers \
    import BaseLoadBalancersFixture
from ccengine.common.decorators import attr


class AlertTests(BaseLoadBalancersFixture):

    @classmethod
    def setUpClass(cls):
        super(AlertTests, cls).setUpClass()

    @attr('positive')
    def test_alerts(self):
        """Testing alert calls"""
        r = self.mgmt_client.get_alerts()
        self.assertEquals(r.status_code, 200)
        alerts = r.entity
        self.assertTrue(len(alerts) > 0)
        r = self.mgmt_client.get_alerts_on_accounts(self.tenant_id)
        self.assertEquals(r.status_code, 200)
        self.assertTrue(len(r.entity) > 0)
        r = self.mgmt_client.get_alert(alerts[0].id)
        self.assertEquals(r.status_code, 200)
        self.assertTrue(r.entity.created == alerts[0].created and
                        r.entity.status == alerts[0].status)
        r = self.mgmt_client.get_alerts_on_load_balancers(
            alerts[0].loadbalancerId)
        self.assertEquals(r.status_code, 200)
        self.assertTrue(len(r.entity) > 0)
        r = self.mgmt_client.get_alerts_on_load_balancer(
            alerts[0].loadbalancerId)
        self.assertEquals(r.status_code, 200)
        self.assertTrue(len(r.entity) > 0)
        r = self.mgmt_client.get_alerts_on_cluster(cluster_id=1)
        self.assertEquals(r.status_code, 200)
        self.assertTrue(len(r.entity) > 0)
        for alert in alerts:
            if alert.status == 'UNACKNOWLEDGED':
                r = self.mgmt_client.update_alert_to_acknowledged(
                    alert_id=alert.id)
                self.assertEquals(r.status_code, 202)
                r = self.mgmt_client.get_alert(alert_id=alert.id)
                self.assertEquals(r.status_code, 200)
                self.assertTrue(r.entity.status == 'ACKNOWLEDGED')
                break
