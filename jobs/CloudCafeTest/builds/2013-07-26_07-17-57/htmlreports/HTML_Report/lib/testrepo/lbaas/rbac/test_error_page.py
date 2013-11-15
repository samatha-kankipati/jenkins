from testrepo.common.testfixtures.load_balancers \
    import LoadBalancersRBACFixture
from ccengine.common.decorators import attr


class TestErrorPageRBAC(LoadBalancersRBACFixture):

    @attr('rbac')
    def test_rbac_get_error_page(self):
        '''View error page details with observer and creator roles.'''
        observer_resp = self.observer.get_error_page(self.rbac_lb.id)
        self.assertEquals(observer_resp.status_code, 200, 'Observer should be'
                          ' allowed to view error page details.')
        creator_resp = self.creator.get_error_page(self.rbac_lb.id)
        self.assertEquals(creator_resp.status_code, 200, 'Creator should be'
                          ' allowed to view error page details.')

    @attr('rbac')
    def test_rbac_update_error_page(self):
        '''Update error page with observer and creator roles.'''
        observer_resp = self.observer.update_error_page(self.rbac_lb.id,
                                                        'Observer EP')
        self.assertEquals(observer_resp.status_code, 405, 'Observer should'
                          ' not be allowed to update error page.')
        creator_resp = self.creator.update_error_page(self.rbac_lb.id,
                                                      'Creator EP')
        self.assertEquals(creator_resp.status_code, 202, 'Creator should'
                          ' be allowed to update error page.')

    @attr('rbac')
    def test_rbac_delete_error_page(self):
        '''Delete error page with observer and creator roles.'''
        observer_resp = self.observer.delete_error_page(self.rbac_lb.id)
        self.assertEquals(observer_resp.status_code, 405, 'Observer should not'
                          ' be allowed to delete error page.')
        creator_resp = self.creator.delete_error_page(self.rbac_lb.id)
        self.assertEquals(creator_resp.status_code, 405, 'Creator should not '
                          'be allowed to delete error page.')
