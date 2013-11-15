from testrepo.common.testfixtures.load_balancers \
    import LoadBalancersRBACFixture
from ccengine.common.decorators import attr


class TestContentCachingRBAC(LoadBalancersRBACFixture):

    @attr('rbac')
    def test_rbac_get_content_caching(self):
        '''View content caching with observer and creator roles.'''
        observer_resp = self.observer.get_content_caching(self.rbac_lb.id)
        self.assertEquals(observer_resp.status_code, 200, 'Observer should '
                          'be allowed to view content caching.')
        creator_resp = self.creator.get_content_caching(self.rbac_lb.id)
        self.assertEquals(creator_resp.status_code, 200, 'Creator should '
                          'be allowed to view content caching.')

    @attr('rbac')
    def test_rbac_update_content_caching(self):
        '''Update content caching with observer and creator roles.'''
        enabled = True
        observer_resp = self.observer.update_content_caching(
            self.rbac_lb.id, enabled=enabled)
        self.assertEquals(observer_resp.status_code, 405, 'Observer should '
                          'not be allowed to update content caching.')
        creator_resp = self.creator.update_content_caching(
            self.rbac_lb.id, enabled=enabled)
        self.assertEquals(creator_resp.status_code, 202, 'Creator should '
                          'be allowed to update content caching.')
