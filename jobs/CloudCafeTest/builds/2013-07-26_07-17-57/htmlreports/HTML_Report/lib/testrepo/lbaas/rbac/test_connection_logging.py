from testrepo.common.testfixtures.load_balancers \
    import LoadBalancersRBACFixture
from ccengine.common.decorators import attr


class TestConnectionLoggingRBAC(LoadBalancersRBACFixture):

    @attr('rbac')
    def test_rbac_get_connection_logging(self):
        '''View connection logging with observer and creator roles.'''
        observer_resp = self.observer.get_connection_logging(self.rbac_lb.id)
        self.assertEquals(observer_resp.status_code, 200, 'Observer should '
                          'be allowed to view connection logging.')
        creator_resp = self.creator.get_connection_logging(self.rbac_lb.id)
        self.assertEquals(creator_resp.status_code, 200, 'Creator should '
                          'be allowed to view connection logging.')

    @attr('rbac')
    def test_rbac_update_connection_logging(self):
        '''Update connection logging with observer and creator roles.'''
        enable_states = [True, False]

        for is_enabled in enable_states:
            observer_resp = self.observer.update_connection_logging(
                self.rbac_lb.id, enabled=is_enabled)
            self.assertEquals(observer_resp.status_code, 405, 'Observer should '
                              'not be allowed to update connection logging. '
                              '(enabled = {0!s})'.format(is_enabled))

            creator_resp = self.creator.update_connection_logging(
                self.rbac_lb.id, enabled=is_enabled)
            self.assertEquals(creator_resp.status_code, 202, 'Creator should '
                              'be allowed to update connection logging. '
                              '(enabled = {0!s})'.format(is_enabled))
