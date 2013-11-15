from testrepo.common.testfixtures.load_balancers \
    import LoadBalancersRBACFixture
from ccengine.common.decorators import attr


class TestAllowedDomainsRBAC(LoadBalancersRBACFixture):

    @attr('rbac')
    def test_rbac_list_allowed_domains(self):
        '''List allowed domains with observer and creator roles.'''
        observer_resp = self.observer.list_allowed_domains()
        self.assertEquals(observer_resp.status_code, 200, 'Observer should be'
                          ' allowed to list allowed domains.')
        creator_resp = self.creator.list_allowed_domains()
        self.assertEquals(creator_resp.status_code, 200, 'Creator should be'
                          ' allowed to list allowed domains.')

