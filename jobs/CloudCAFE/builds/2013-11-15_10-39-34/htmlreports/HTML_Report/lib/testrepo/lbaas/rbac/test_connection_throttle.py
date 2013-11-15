from ccengine.common.decorators import attr
from testrepo.common.testfixtures.load_balancers \
    import LoadBalancersRBACFixture


class TestConnectionThrottleRBAC(LoadBalancersRBACFixture):

    @attr('rbac')
    def test_rbac_get_connection_throttle(self):
        '''View connection throttle with admin, observer, creator roles'''
        api = self.roles.get_api_name()
        roles = self.roles.get_role_response_codes(api=api)
        api_args = {'load_balancer_id': self.rbac_lb.id}
        errors = self.roles.validate_roles(roles=roles, api=api,
                                           api_args=api_args)
        self.assertFalse(len(errors), 'ERRORS: {}'.format(errors))

    @attr('rbac')
    def test_rbac_update_connection_throttle(self):
        '''Update connection throttle with admin, observer, creator roles'''
        api = self.roles.get_api_name()
        roles = self.roles.get_role_response_codes(api=api)

        start_value = 10
        api_args = {'load_balancer_id': self.rbac_lb.id,
                    'maxConnections': start_value,
                    'minConnections': start_value,
                    'maxConnectionRate': start_value,
                    'rateInterval': start_value}

        errors = self.roles.validate_roles(roles=roles, api=api,
                                           api_args=api_args,
                                           check_lb_active=True)
        self.assertFalse(len(errors), 'ERRORS: {}'.format(errors))

    @attr('rbac')
    def test_rbac_delete_connection_throttle(self):
        '''Delete connection throttle with admin, observer, creator roles '''
        api = self.roles.get_api_name()
        roles = self.roles.get_role_response_codes(api=api)
        api_args = {'load_balancer_id': self.rbac_lb.id}

        error_msgs = list()

        for role, status in roles.iteritems():
            self._create_throttle()
            errors = self.roles.validate_roles(roles={role: status}, api=api,
                                               api_args=api_args,
                                               check_lb_active=True)
            error_msgs.extend(errors)
        self.assertFalse(len(error_msgs), 'ERRORS: {}'.format(error_msgs))

    # ---- Internal Connection Throttle Routines ----
    def _create_throttle(self):
        arg_value = 10
        api_args = {'load_balancer_id': self.rbac_lb.id,
                    'maxConnections': arg_value,
                    'minConnections': arg_value,
                    'maxConnectionRate': arg_value,
                    'rateInterval': arg_value}
        self.user_admin.update_connection_throttle(**api_args)
        self.lbaas_provider.wait_for_status(self.rbac_lb.id)
