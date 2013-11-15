from ccengine.common.decorators import attr
from testrepo.common.testfixtures.load_balancers \
    import LoadBalancersRBACFixture


class TestHealthMonitorsRBAC(LoadBalancersRBACFixture):

    @attr('rbac')
    def test_rbac_get_health_monitor(self):
        '''View health monitor with admin, observer, and creator roles'''
        api = self.roles.get_api_name()
        roles = self.roles.get_role_response_codes(api=api)
        api_args = {'load_balancer_id': self.rbac_lb.id}

        errors = self.roles.validate_roles(roles=roles, api=api,
                                           api_args=api_args)
        self.assertFalse(len(errors), 'ERRORS: {}'.format(errors))

    @attr('rbac')
    def test_rbac_update_health_monitor(self):
        '''Update health monitor with admin, observer, and creator roles'''
        aBD = delay = timeout = 1

        api = self.roles.get_api_name()
        roles = self.roles.get_role_response_codes(api=api)
        api_args = {'load_balancer_id': self.rbac_lb.id,
                    'attemptsBeforeDeactivation': aBD,
                    'delay': delay,
                    'timeout': timeout,
                    'type': 'CONNECT'}

        errors = self.roles.validate_roles(roles=roles, api=api,
                                           api_args=api_args,
                                           check_lb_active=True)
        self.assertFalse(len(errors), 'ERRORS: {}'.format(errors))

    @attr('rbac')
    def test_rbac_delete_health_monitor(self):
        '''Delete health monitor with observer and creator roles'''
        api = self.roles.get_api_name()
        roles = self.roles.get_role_response_codes(api=api)
        api_args = {'load_balancer_id': self.rbac_lb.id}

        errors = list()
        for role, status in roles.iteritems():
            self._create_health_monitor()
            error_msgs = self.roles.validate_roles(roles={role: status},
                                                   api=api, api_args=api_args,
                                                   check_lb_active=True)
            errors.extend(error_msgs)
        self.assertFalse(len(errors), 'ERRORS: {}'.format(errors))

    # ----- INTERNAL HEALTH MONITOR ROUTINES -----
    def _create_health_monitor(self):
        test_value = 1

        api_args = {'load_balancer_id': self.rbac_lb.id,
                    'attemptsBeforeDeactivation': test_value,
                    'delay': test_value,
                    'timeout': test_value,
                    'type': 'CONNECT'}
        self.user_admin.update_health_monitor(**api_args)
        self.lbaas_provider.wait_for_status(self.rbac_lb.id)
