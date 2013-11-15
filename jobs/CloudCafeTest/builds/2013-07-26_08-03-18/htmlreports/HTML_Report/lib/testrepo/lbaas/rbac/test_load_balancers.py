from ccengine.common.decorators import attr
from ccengine.domain.types import LoadBalancerStatusTypes as LBStatus
from testrepo.common.testfixtures.load_balancers \
    import LoadBalancersRBACFixture


class TestLoadBalancersRBAC(LoadBalancersRBACFixture):

    @attr('rbac')
    def test_rbac_list_load_balancers(self):
        '''List load balancers with admin, observer, and creator roles'''
        api = self.roles.get_api_name()
        roles = self.roles.get_role_response_codes(api=api)
        errors = self.roles.validate_roles(roles=roles, api=api)
        self.assertFalse(len(errors), 'ERRORS: {}'.format(errors))

    @attr('rbac')
    def test_rbac_get_load_balancer(self):
        '''Get load balancer details with admin, observer, and creator roles'''
        api = self.roles.get_api_name()
        roles = self.roles.get_role_response_codes(api=api)
        api_args = {'load_balancer_id': self.rbac_lb.id}
        errors = self.roles.validate_roles(roles=roles, api=api,
                                           api_args=api_args)
        self.assertFalse(len(errors), 'ERRORS: {}'.format(errors))

    @attr('rbac')
    def test_rbac_create_load_balancer(self):
        '''Create load balancer using admin, observer, and creator roles'''
        api = self.roles.get_api_name()
        roles = self.roles.get_role_response_codes(api=api)
        api_args = {'name': 'TestCreateLB',
                    'virtualIps': [{'type': 'SERVICENET'}],
                    'nodes': [{'address': '10.0.0.1',
                               'condition': 'ENABLED',
                               'port': '80'}],
                    'port': 80,
                    'protocol': 'HTTP'}

        errors = self.roles.validate_roles(roles=roles, api=api,
                                           api_args=api_args,
                                           check_lb_active=True,
                                           delete_lb=True)
        self.assertFalse(len(errors), 'ERRORS: {}'.format(errors))

    @attr('rbac')
    def test_rbac_update_load_balancer(self):
        '''Update load balancer using admin, observer, and creator roles'''
        api = self.roles.get_api_name()
        roles = self.roles.get_role_response_codes(api=api)
        api_args = {'load_balancer_id': self.rbac_lb.id,
                    'name': 'Test'}

        errors = self.roles.validate_roles(roles=roles, api=api,
                                           api_args=api_args,
                                           check_lb_active=True)
        self.assertFalse(len(errors), 'ERRORS: {}'.format(errors))

    @attr('rbac')
    def test_rbac_delete_load_balancer(self):
        '''Delete a load balancer using admin, observer, and creator roles'''
        api = self.roles.get_api_name()
        roles = self.roles.get_role_response_codes(api=api)

        errors = list()
        for role, status in roles.iteritems():
            lb_id_list = self._create_lb(num_lbs=1)
            api_args = {'load_balancer_id': lb_id_list[0]}
            error_msg = self.roles.validate_roles(roles={role: status},
                                                  api=api, api_args=api_args)
            errors.extend(error_msg)
        self.assertFalse(len(errors), 'ERRORS: {}'.format(errors))

    @attr('rbac')
    def test_rbac_batch_delete_load_balancers(self):
        '''Batch delete LBs using admin, observer, and creator roles'''
        api = self.roles.get_api_name()
        roles = self.roles.get_role_response_codes(api=api)

        errors = list()
        for role, status in roles.iteritems():
            api_args = {'load_balancer_id_list': self._create_lb(num_lbs=1)}
            error_msg = self.roles.validate_roles(roles={role: status},
                                                  api=api, api_args=api_args)
            errors.extend(error_msg)
        self.assertFalse(len(errors), 'ERRORS: {}'.format(errors))

    @attr('rbac')
    def test_rbac_list_load_balancer_stats(self):
        '''List load balancer stats with admin, observer, and creator roles'''
        api = self.roles.get_api_name()
        roles = self.roles.get_role_response_codes(api=api)
        api_args = {'load_balancer_id': self.rbac_lb.id}

        errors = self.roles.validate_roles(roles=roles, api=api,
                                           api_args=api_args)
        self.assertFalse(len(errors), 'ERRORS: {}'.format(errors))

    # ----- Private CREATE_LOADBALANCER Routines
    def _create_lb(self, num_lbs=1):
        kwargs = {'virtualIps': [{'type': 'SERVICENET'}],
                  'nodes': [{'address': '10.0.0.1',
                             'condition': 'ENABLED',
                             'port': '80'}]}
        lbs = self.lbaas_provider.create_n_load_balancers(n=num_lbs,
                                                          wait_for_active=True,
                                                          **kwargs)
        lb_id_list = [lb.id for lb in lbs if lb.status == LBStatus.ACTIVE]
        for lbid in lb_id_list:
            self.lbs_to_delete.append(lbid)
        return lb_id_list
