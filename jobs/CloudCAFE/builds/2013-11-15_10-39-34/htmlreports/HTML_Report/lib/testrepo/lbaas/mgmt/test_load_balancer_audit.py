from testrepo.common.testfixtures.load_balancers \
    import BaseLoadBalancersFixture
from ccengine.common.decorators import attr


class LoadbalancerAuditTests(BaseLoadBalancersFixture):

    @classmethod
    def setUpClass(cls):
        super(LoadbalancerAuditTests, cls).setUpClass()

    @attr('smoke', 'positive')
    def test_vip_availability_report(self):
        '''Retrieve reports for vip availability per cluster'''
        r = self.mgmt_client.get_load_balancer_audit(status='ERROR')
        self.assertEquals(r.status_code, 200)
        # print
        # print r.entity
