from testrepo.common.testfixtures.load_balancers \
    import BaseLoadBalancersFixture
from ccengine.common.decorators import attr


class HostCapacityReportTests(BaseLoadBalancersFixture):

    @classmethod
    def setUpClass(cls):
        super(HostCapacityReportTests, cls).setUpClass()

    @attr('smoke', 'positive')
    def test_host_capacity_report_calls(self):
        '''Retrieve a list of capacity on all hosts and a host'''
        r = self.mgmt_client.get_hosts()
        self.assertEqual(r.status_code, 200)
        host = r.entity[0]
        r = self.mgmt_client.get_hosts_capacity_report()
        self.assertEqual(r.status_code, 200)
        r = self.mgmt_client.get_host_capacity_report(host_id=host.id)
        self.assertEqual(r.status_code, 200)
        self.assertTrue(len(r.entity) > 0)
