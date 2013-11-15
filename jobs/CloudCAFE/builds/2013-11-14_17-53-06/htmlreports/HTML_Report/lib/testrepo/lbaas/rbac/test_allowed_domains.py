from ccengine.common.decorators import attr
from testrepo.common.testfixtures.load_balancers \
    import LoadBalancersRBACFixture


class TestAllowedDomainsRBAC(LoadBalancersRBACFixture):
    @attr('rbac')
    def test_rbac_list_allowed_domains(self):
        '''List allowed domains with admin, observer, and creator roles'''
        api = self.roles.get_api_name()
        roles = self.roles.get_role_response_codes(api=api)
        errors = self.roles.validate_roles(roles=roles, api=api)
        self.assertFalse(len(errors), 'ERRORS: {}'.format(errors))
