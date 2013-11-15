from ccengine.common.decorators import attr
from testrepo.common.testfixtures.load_balancers \
    import LoadBalancersRBACFixture


class TestContentCachingRBAC(LoadBalancersRBACFixture):

    @attr('rbac')
    def test_rbac_get_content_caching(self):
        '''Get Content Caching settings using admin, creator, and observer'''
        api = self.roles.get_api_name()
        roles = self.roles.get_role_response_codes(api=api)
        api_args = {'load_balancer_id': self.rbac_lb.id}
        errors = self.roles.validate_roles(roles=roles, api=api,
                                           api_args=api_args)
        self.assertFalse(len(errors), 'ERRORS: {}'.format(errors))

    @attr('rbac')
    def test_rbac_update_content_caching(self):
        '''Update content caching with admin, observer, and creator roles'''
        api = self.roles.get_api_name()
        roles = self.roles.get_role_response_codes(api=api)
        api_args = {'load_balancer_id': self.rbac_lb.id,
                    'enabled': 'false'}
        errors = self.roles.validate_roles(roles=roles, api=api,
                                           api_args=api_args,
                                           check_lb_active=True)
        self.assertFalse(len(errors), 'ERRORS: {}'.format(errors))
