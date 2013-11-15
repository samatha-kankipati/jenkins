from testrepo.common.testfixtures.load_balancers \
    import BaseLoadBalancersFixture
from ccengine.common.decorators import attr
from datetime import datetime, timedelta


class BillingAndUsageTests(BaseLoadBalancersFixture):

    @classmethod
    def setUpClass(cls):
        super(BillingAndUsageTests, cls).setUpClass()
        end = datetime.now()
        start = datetime.now() - timedelta(days=1)
        cls.start_time = start.isoformat()
        cls.end_time = end.isoformat()

    @attr('positive')
    def test_account_billing_and_usage_calls(self):
        '''Testing account billing, then account and load balancer usage'''
        r = self.mgmt_client.get_accounts_billing()
        self.assertEquals(r.status_code, 200)
        self.assertTrue(len(r.entity) > 0)
        r = self.mgmt_client.get_accounts_usage()
        self.assertEquals(r.status_code, 200)
        self.assertTrue(len(r.entity) > 0)
        r = self.mgmt_client.get_load_balancers_usage(
            start_time=self.start_time, end_time=self.end_time)
        self.assertEquals(r.status_code, 200)
        #Todo: find a way to populate this list, or find a populated list time
        #Todo: range
        #self.assertTrue(len(r.entity) > 0)

    @attr('positive')
    def test_host_usage_call(self):
        '''Testing the get call for host usage'''
        r = self.mgmt_client.get_host_usage(start_date=self.start_time,
                                            end_date=self.end_time)
        self.assertEquals(r.status_code, 200)
        self.assertTrue(len(r.entity) > 0)

    @attr('positive')
    def test_create_and_delete_events_in_usage_table(self):
        '''Test that the usage table includes create and delete LB events'''
        r = self.mgmt_client.get_load_balancers_usage(
            start_time=self.start_time, end_time=self.end_time)
        self.assertEquals(r.status_code, 200)
        create_present = False
        delete_present = False
        for event in r.entity:
            if event.eventType == 'CREATE_LOADBALANCER':
                create_present = True
            elif event.eventType == 'DELETE_LOADBALANCER':
                delete_present = True
        self.assertTrue(create_present)
        self.assertTrue(delete_present)
