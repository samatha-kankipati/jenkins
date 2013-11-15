from ccengine.common.decorators import attr
from testrepo.common.testfixtures.load_balancers \
    import LoadBalancersRBACFixture


class TestSessionPersistenceRBAC(LoadBalancersRBACFixture):

    @attr('rbac')
    def test_rbac_get_session_persistence(self):
        '''View session persistence with observer, admin, and creator roles'''
        api = self.roles.get_api_name()
        roles = self.roles.get_role_response_codes(api=api)
        api_args = {'load_balancer_id': self.rbac_lb.id}
        errors = self.roles.validate_roles(roles=roles, api=api,
                                           api_args=api_args)
        self.assertFalse(len(errors), 'ERRORS: {}'.format(errors))

    @attr('rbac')
    def test_rbac_update_session_persistence(self):
        '''Update session persistence w/admin, observer, and creator roles'''
        api = self.roles.get_api_name()
        api_args = {'load_balancer_id': self.rbac_lb.id,
                    'persistenceType': 'HTTP_COOKIE'}
        roles = self.roles.get_role_response_codes(api=api)
        errors = self.roles.validate_roles(roles=roles, api=api,
                                           api_args=api_args)
        self.assertFalse(len(errors), 'ERRORS: {}'.format(errors))

    @attr('rbac')
    def test_rbac_delete_session_persistence(self):
        '''Delete session persistence with admin, observer and creator roles'''
        api = self.roles.get_api_name()
        api_args = {'load_balancer_id': self.rbac_lb.id}
        roles = self.roles.get_role_response_codes(api=api)

        errors = list()
        for role, status in roles.iteritems():
            self._enable_session_persistence()
            error_msgs = self.roles.validate_roles(roles={role: status},
                                                   api=api,
                                                   api_args=api_args,
                                                   check_lb_active=True)
            errors.extend(error_msgs)
        self.assertFalse(len(errors), 'ERRORS: {}'.format(errors))

    # ----- INTERNAL SESSION PERSISTENCE ROUTINES -----
    def _enable_session_persistence(self):
        self.fixture_log.info('\n\n*** Setting up session persistence ***\n\n')
        args = {'load_balancer_id': self.rbac_lb.id,
                'persistenceType': 'HTTP_COOKIE'}
        self.user_admin.update_session_persistence(**args)
        self.lbaas_provider.wait_for_status(self.rbac_lb.id)
