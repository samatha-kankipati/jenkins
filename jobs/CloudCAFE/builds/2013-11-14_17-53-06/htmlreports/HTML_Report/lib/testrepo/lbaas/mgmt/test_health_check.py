from testrepo.common.testfixtures.load_balancers \
    import BaseLoadBalancersFixture
from ccengine.common.decorators import attr


class HealthCheckTests(BaseLoadBalancersFixture):

    @classmethod
    def setUpClass(cls):
        super(HealthCheckTests, cls).setUpClass()

    @attr('positive')
    def test_customer_list_calls(self):
        '''Test get health check method'''
        #TODO: Verify that this call is even implemented any longer
        #r = self.mgmt_client.get_health_check()
        #self.assertEquals(r.status_code, 200)
        pass
