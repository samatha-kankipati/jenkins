from testrepo.common.testfixtures.load_balancers \
    import LoadBalancersRBACFixture
from ccengine.common.decorators import attr


class TestHealthMonitorsRBAC(LoadBalancersRBACFixture):

    @attr('rbac')
    def test_rbac_get_health_monitor(self):
        '''View health monitor with observer and creator roles.'''
        observer_resp = self.observer.get_health_monitor(self.rbac_lb.id)
        self.assertEquals(observer_resp.status_code, 200, 'Observer should '
                          'be allowed to view health monitor.')
        creator_resp = self.creator.get_health_monitor(self.rbac_lb.id)
        self.assertEquals(creator_resp.status_code, 200, 'Creator should '
                          'be allowed to view health monitor.')

    @attr('rbac')
    def test_rbac_update_health_monitor(self):
        '''Update health monitor with observer and creator roles.'''
        aBD = delay = timeout = 1
        type_ = 'CONNECT'
        observer_resp = self.observer.update_health_monitor(self.rbac_lb.id,
                                                            aBD, delay,
                                                            timeout, type_)
        self.assertEquals(observer_resp.status_code, 405, 'Observer should '
                          'not be allowed to update health monitor.')
        creator_resp = self.creator.update_health_monitor(self.rbac_lb.id,
                                                          aBD, delay,
                                                          timeout, type_)
        self.assertEquals(creator_resp.status_code, 202, 'Creator should '
                          'be allowed to update health monitor.')

    @attr('rbac')
    def test_rbac_delete_health_monitor(self):
        '''Delete health monitor with observer and creator roles.'''
        observer_resp = self.observer.delete_health_monitor(self.rbac_lb.id)
        self.assertEquals(observer_resp.status_code, 405, 'Observer should '
                          'not be allowed to update health monitor.')
        creator_resp = self.creator.delete_health_monitor(self.rbac_lb.id)
        self.assertEquals(creator_resp.status_code, 405, 'Creator should '
                          'not be allowed to update health monitor.')
