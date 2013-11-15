from testrepo.common.testfixtures.load_balancers \
    import LoadBalancersRBACFixture
from ccengine.common.decorators import attr


class TestUsageRBAC(LoadBalancersRBACFixture):

    @attr('rbac')
    def test_rbac_list_billable_load_balancers(self):
        '''List billable load balancers with observer and creator roles.'''
        startTime = '2012-11-10'
        endTime = '2012-11-11'
        observer_resp = self.observer.list_billable_load_balancers(
            startTime=startTime, endTime=endTime, limit=1)
        self.assertEquals(observer_resp.status_code, 200, 'Observer should be '
                          'allowed to list billable load balancers.')
        creator_resp = self.creator.list_billable_load_balancers(
            startTime=startTime, endTime=endTime, limit=1)
        self.assertEquals(creator_resp.status_code, 200, 'Creator should be '
                          'allowed to list billable load balancers.')

    @attr('rbac')
    def test_rbac_list_account_usage(self):
        '''List account usage with observer and creator roles.'''
        observer_resp = self.observer.list_account_usage(limit=1)
        self.assertEquals(observer_resp.status_code, 200, 'Observer should be '
                          'allowed to list account usage.')
        creator_resp = self.creator.list_account_usage(limit=1)
        self.assertEquals(creator_resp.status_code, 200, 'Creator should be '
                          'allowed to list account usage.')

    @attr('rbac')
    def test_rbac_list_historic_usage(self):
        '''List historic usage with observer and creator roles.'''
        observer_resp = self.observer.list_load_balancer_usage(self.rbac_lb.id,
                                                               limit=1)
        self.assertEquals(observer_resp.status_code, 200, 'Observer should be '
                          'allowed to list usage for a load balancer.')
        creator_resp = self.creator.list_load_balancer_usage(self.rbac_lb.id,
                                                             limit=1)
        self.assertEquals(creator_resp.status_code, 200, 'Creator should be '
                          'allowed to list usage for a load balancer.')

    @attr('rbac')
    def test_rbac_list_current_usage(self):
        '''List current usage with observer and creator roles.'''
        observer_resp = self.observer.list_current_usage(self.rbac_lb.id)
        self.assertEquals(observer_resp.status_code, 200, 'Observer should be '
                          'allowed to list current usage for a load balancer.')
        creator_resp = self.creator.list_current_usage(self.rbac_lb.id)
        self.assertEquals(creator_resp.status_code, 200, 'Creator should be '
                          'allowed to list current usage for a load balancer.')
