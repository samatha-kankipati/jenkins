from ccengine.common.decorators import attr
from testrepo.common.testfixtures.load_balancers \
    import LoadBalancersRBACFixture


class TestListsRBAC(LoadBalancersRBACFixture):

    @attr('smoke', 'positive', 'rbac')
    def test_rbac_list_protocols(self):
        '''List protocols with admin, observer, and creator roles'''
        api = self.roles.get_api_name()
        roles = self.roles.get_role_response_codes(api=api)
        errors = self.roles.validate_roles(api=api, roles=roles)
        self.assertFalse(len(errors), 'ERRORS: {}'.format(errors))

    @attr('smoke', 'positive', 'rbac')
    def test_rbac_list_algorithms(self):
        '''List algorithms with admin, observer, and creator roles'''
        api = self.roles.get_api_name()
        roles = self.roles.get_role_response_codes(api=api)
        errors = self.roles.validate_roles(api=api, roles=roles)
        self.assertFalse(len(errors), 'ERRORS: {}'.format(errors))

    @attr('smoke', 'positive', 'rbac')
    def test_rbac_list_absolute_limits(self):
        '''List protocols with admin, observer, and creator roles'''
        api = self.roles.get_api_name()
        roles = self.roles.get_role_response_codes(api=api)
        errors = self.roles.validate_roles(api=api, roles=roles)
        self.assertFalse(len(errors), 'ERRORS: {}'.format(errors))
