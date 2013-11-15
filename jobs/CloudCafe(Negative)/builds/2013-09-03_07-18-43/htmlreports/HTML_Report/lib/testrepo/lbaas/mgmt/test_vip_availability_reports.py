from testrepo.common.testfixtures.load_balancers \
    import BaseLoadBalancersFixture
from ccengine.common.decorators import attr


class VipAvailabilityReportTests(BaseLoadBalancersFixture):

    @classmethod
    def setUpClass(cls):
        super(VipAvailabilityReportTests, cls).setUpClass()

    @attr('smoke', 'positive')
    def test_vip_availability_report(self):
        '''Retrieve reports for vip availability per cluster'''
        r = self.mgmt_client.get_vip_availability_report()
        self.assertEquals(r.status_code, 200)
        self.assertTrue(len(r.entity) > 0)
        r = self.mgmt_client.get_clusters()
        self.assertEquals(r.status_code, 200)
        cluster_id = r.entity[0].id
        r = self.mgmt_client.get_cluster_vip_availability_report(cluster_id)
        self.assertEquals(r.status_code, 200)
        self.assertTrue(len(r.entity) > 0)
