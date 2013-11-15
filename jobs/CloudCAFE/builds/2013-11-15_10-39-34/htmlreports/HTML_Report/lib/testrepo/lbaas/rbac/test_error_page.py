from ccengine.common.decorators import attr
import ccengine.common.tools.datagen as datagen
from testrepo.common.testfixtures.load_balancers \
    import LoadBalancersRBACFixture


class TestErrorPageRBAC(LoadBalancersRBACFixture):

    @attr('rbac')
    def test_rbac_get_error_page(self):
        '''Get error page with admin, observer, and creator roles'''
        api = self.roles.get_api_name()
        roles = self.roles.get_role_response_codes(api=api)
        api_args = {'load_balancer_id': self.rbac_lb.id}

        errors = self.roles.validate_roles(roles=roles, api=api,
                                           api_args=api_args)
        self.assertFalse(len(errors), 'ERRORS: {}'.format(errors))

    @attr('rbac')
    def test_rbac_update_error_page(self):
        '''Update error page with admin, observer, and creator roles'''
        api = self.roles.get_api_name()
        roles = self.roles.get_role_response_codes(api=api)
        api_args = {'load_balancer_id': self.rbac_lb.id,
                    'content': 'Some Random String'}

        errors = self.roles.validate_roles(roles=roles, api=api,
                                           api_args=api_args,
                                           check_lb_active=True)
        self.assertFalse(len(errors), 'ERRORS: {}'.format(errors))

    @attr('rbac')
    def test_rbac_delete_error_page(self):
        '''Delete error page with admin, observer, and creator roles'''
        api = self.roles.get_api_name()
        roles = self.roles.get_role_response_codes(api=api)
        api_args = {'load_balancer_id': self.rbac_lb.id}

        errors = list()
        for role, status in roles.iteritems():
            self._create_error_page()
            error_msg = self.roles.validate_roles(roles={role: status},
                                                  api=api, api_args=api_args,
                                                  check_lb_active=True)
            errors.extend(error_msg)
        self.assertFalse(len(errors), 'ERRORS: {}'.format(errors))

    # ----- INTERNAL ERROR PAGE ROUTINES -----
    def _create_error_page(self):
        api_args = {'load_balancer_id': self.rbac_lb.id,
                    'content': datagen.random_string('err_page')}
        self.user_admin.update_error_page(**api_args)
        self.lbaas_provider.wait_for_status(self.rbac_lb.id)
