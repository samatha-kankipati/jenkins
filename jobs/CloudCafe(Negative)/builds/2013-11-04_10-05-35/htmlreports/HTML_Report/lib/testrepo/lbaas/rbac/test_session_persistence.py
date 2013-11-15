from testrepo.common.testfixtures.load_balancers \
    import LoadBalancersRBACFixture
from ccengine.common.decorators import attr


class TestSessionPersistenceRBAC(LoadBalancersRBACFixture):

    @attr('rbac')
    def test_rbac_get_session_persistence(self):
        '''View session persistence with observer and creator roles.'''
        observer_resp = self.observer.get_session_persistence(self.rbac_lb.id)
        self.assertEquals(observer_resp.status_code, 200, 'Observer should '
                          'be allowed to view session persistence.')
        creator_resp = self.creator.get_session_persistence(self.rbac_lb.id)
        self.assertEquals(creator_resp.status_code, 200, 'Creator should '
                          'be allowed to view session persistence.')

    @attr('rbac')
    def test_rbac_update_session_persistence(self):
        '''Update session persistence with observer and creator roles.'''
        type_ = 'HTTP_COOKIE'
        observer_resp = self.observer.update_session_persistence(
            self.rbac_lb.id, persistenceType=type_)
        self.assertEquals(observer_resp.status_code, 405, 'Observer should '
                          'not be allowed to update session persistence.')
        creator_resp = self.creator.update_session_persistence(
            self.rbac_lb.id, persistenceType=type_)
        self.assertEquals(creator_resp.status_code, 202, 'Creator should '
                          'be allowed to update session persistence.')

    @attr('rbac')
    def test_rbac_delete_session_persistence(self):
        '''Delete session persistence with observer and creator roles.'''
        observer_resp = self.observer.delete_session_persistence(
            self.rbac_lb.id)
        self.assertEquals(observer_resp.status_code, 405, 'Observer should '
                          'not be allowed to update session persistence.')
        creator_resp = self.creator.delete_session_persistence(
            self.rbac_lb.id)
        self.assertEquals(creator_resp.status_code, 405, 'Creator should '
                          'not be allowed to update session persistence.')
