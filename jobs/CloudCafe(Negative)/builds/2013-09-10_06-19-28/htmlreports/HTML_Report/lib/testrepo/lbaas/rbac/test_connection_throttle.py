from testrepo.common.testfixtures.load_balancers \
    import LoadBalancersRBACFixture
from ccengine.common.decorators import attr


class TestConnectionThrottleRBAC(LoadBalancersRBACFixture):

    @attr('rbac')
    def test_rbac_get_connection_throttle(self):
        '''View connection throttle with observer and creator roles.'''
        observer_resp = self.observer.get_connection_throttle(self.rbac_lb.id)
        self.assertEquals(observer_resp.status_code, 200, 'Observer should '
                          'be allowed to view connection throttle.')
        creator_resp = self.creator.get_connection_throttle(self.rbac_lb.id)
        self.assertEquals(creator_resp.status_code, 200, 'Creator should '
                          'be allowed to view connection throttle.')

    @attr('rbac')
    def test_rbac_update_connection_throttle(self):
        '''Update connection throttle with observer and creator roles.'''
        max_conns = min_conns = max_conn_rate = rate_interval = 10
        observer_resp = self.observer.update_connection_throttle(
            self.rbac_lb.id, maxConnections=max_conns,
            minConnections=min_conns, maxConnectionRate=max_conn_rate,
            rateInterval=rate_interval)
        self.assertEquals(observer_resp.status_code, 405, 'Observer should '
                          'not be allowed to update connection throttle.')
        creator_resp = self.creator.update_connection_throttle(
            self.rbac_lb.id, maxConnections=max_conns,
            minConnections=min_conns, maxConnectionRate=max_conn_rate,
            rateInterval=rate_interval)
        self.assertEquals(creator_resp.status_code, 202, 'Creator should '
                          'be allowed to update connection throttle.')

    @attr('rbac')
    def test_rbac_delete_connection_throttle(self):
        '''Delete connection throttle with observer and creator roles.'''
        observer_resp = self.observer.delete_connection_throttle(
            self.rbac_lb.id)
        self.assertEquals(observer_resp.status_code, 405, 'Observer should '
                          'not be allowed to update connection throttle.')
        creator_resp = self.creator.delete_connection_throttle(
            self.rbac_lb.id)
        self.assertEquals(creator_resp.status_code, 405, 'Creator should '
                          'not be allowed to update connection throttle.')
