from ccengine.common.constants.lbaas import SSLConstants
from ccengine.common.decorators import attr
from testrepo.common.testfixtures.load_balancers \
    import LoadBalancersRBACFixture


class TestSslTerminationRBAC(LoadBalancersRBACFixture):

    @attr('rbac')
    def test_rbac_get_ssl_termination(self):
        '''View SSL termination with admin, observer, and creator roles'''
        api = self.roles.get_api_name()
        roles = self.roles.get_role_response_codes(api=api)
        api_args = {'load_balancer_id': self.rbac_lb.id}

        self._enable_ssl_termination()
        errors = self.roles.validate_roles(roles=roles, api=api,
                                           api_args=api_args)
        self.assertFalse(len(errors), 'ERRORS: {}'.format(errors))

    @attr('rbac')
    def test_rbac_update_ssl_termination(self):
        '''Update SSL termination with admin, observer, and creator roles'''
        api = self.roles.get_api_name()
        roles = self.roles.get_role_response_codes(api=api)
        api_args = {'load_balancer_id': self.rbac_lb.id,
                    'securePort': 443,
                    'enabled': True,
                    'secureTrafficOnly': False,
                    'privatekey': SSLConstants.privatekey,
                    'certificate': SSLConstants.certificate}

        self._enable_ssl_termination()
        errors = self.roles.validate_roles(roles=roles, api=api,
                                           api_args=api_args,
                                           check_lb_active=True)
        self.assertFalse(len(errors), 'ERRORS: {}'.format(errors))

    @attr('rbac')
    def test_rbac_delete_ssl_termination(self):
        '''Delete ssl termination with admin, observer, and creator roles'''
        api = self.roles.get_api_name()
        roles = self.roles.get_role_response_codes(api=api)
        api_args = {'load_balancer_id': self.rbac_lb.id}

        errors = list()
        for role, status in roles.iteritems():
            self._enable_ssl_termination()
            error_msgs = self.roles.validate_roles(roles={role: status},
                                                   api=api,
                                                   api_args=api_args,
                                                   check_lb_active=True)
            errors.extend(error_msgs)
        self.assertFalse(len(error_msgs), 'ERRORS: {}'.format(error_msgs))

    # ---- INTERNAL SSL TERMINATION ROUTINES -----
    def _enable_ssl_termination(self):
        ssl_args = {'load_balancer_id': self.rbac_lb.id,
                    'securePort': 443,
                    'enabled': True,
                    'secureTrafficOnly': False,
                    'privatekey': SSLConstants.privatekey,
                    'certificate': SSLConstants.certificate}

        self.user_admin.update_ssl_termination(**ssl_args)
        self.lbaas_provider.wait_for_status(self.rbac_lb.id)
