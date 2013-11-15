from testrepo.common.testfixtures.load_balancers \
    import BaseLoadBalancersFixture
from ccengine.common.decorators import attr


class EventTests(BaseLoadBalancersFixture):

    @classmethod
    def setUpClass(cls):
        super(EventTests, cls).setUpClass()

    @attr('positive')
    def test_functional_event_operations(self):
        """Testing event calls:  EXPECTED FAILURE"""
        r = self.mgmt_client.get_events_on_load_balancer(
            account_id=self.tenant_id)
        self.assertEquals(r.status_code, 200)
        self.assertTrue(len(r.entity) > 0)
        name = None
        for event in r.entity[0].loadBalancerServiceEvents:
            if event.author is not None:
                name = event.author
                break
        self.assertNotEquals(name, None)
        r = self.mgmt_client.get_events_for_user(user_name=name)
        self.assertEquals(r.status_code, 200)
        #TODO: find a way to have this returning list partially populated
