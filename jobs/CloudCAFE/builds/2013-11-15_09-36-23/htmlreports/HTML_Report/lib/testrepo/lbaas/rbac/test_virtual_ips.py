from testrepo.common.testfixtures.load_balancers \
    import LoadBalancersRBACFixture
from ccengine.common.decorators import attr


class TestVirtualIpsRBAC(LoadBalancersRBACFixture):
    type_ = 'PUBLIC'

    @classmethod
    def setUpClass(cls):
        super(TestVirtualIpsRBAC, cls).setUpClass()
        cls.rbac_public_lb = cls.lbaas_provider.create_active_load_balancer(
            virtualIps=[{'type': cls.type_}]).entity

    @classmethod
    def tearDownClass(cls):
        cls.lbaas_provider.wait_for_status(cls.rbac_public_lb.id)
        cls.user_admin.delete_load_balancer(cls.rbac_public_lb.id)
        super(TestVirtualIpsRBAC, cls).tearDownClass()

    def setUp(self):
        super(TestVirtualIpsRBAC, self).setUp()
        self.lbaas_provider.wait_for_status(self.rbac_public_lb.id)

    @attr('rbac')
    def test_rbac_list_virtual_ips(self):
        '''List IPv4 VIPs with admin, observer, and creator roles'''

        api = self.roles.get_api_name()
        roles = self.roles.get_role_response_codes(api=api)
        api_args = {'load_balancer_id': self.rbac_lb.id}

        errors = self.roles.validate_roles(roles=roles, api=api,
                                           api_args=api_args)
        self.assertFalse(len(errors), 'ERRORS: {}'.format(errors))

    @attr('rbac')
    def test_rbac_add_ipv6_virtual_ip(self):
        '''Add IPv6 VIP with admin, observer, and creator roles'''

        api = self.roles.get_api_name().replace('ipv6_', '')
        roles = self.roles.get_role_response_codes(api=api)
        api_args = {'load_balancer_id': self.rbac_public_lb.id,
                    'type': self.type_,
                    'ipVersion': 'IPV6'}

        errors = self.roles.validate_roles(lb_id=self.rbac_public_lb.id,
                                           roles=roles, api=api,
                                           api_args=api_args,
                                           check_lb_active=True)
        self.assertFalse(len(errors), 'ERRORS: {}'.format(errors))

    @attr('rbac')
    def test_rbac_delete_ipv6_virtual_ip(self):
        '''Remove IPv6 VIP with admin, observer, and creator roles: FAIL'''
        api = self.roles.get_api_name().replace('ipv6_', '')
        roles = self.roles.get_role_response_codes(api=api)
        api_args = {'load_balancer_id': self.rbac_public_lb.id,
                    'virtual_ip_id': 'NOT SET'}

        errors = list()
        for role, status in roles.iteritems():
            ipv6_vip = self._add_IPV6_vip()
            api_args['virtual_ip_id'] = ipv6_vip.id
            error_msg = self.roles.validate_roles(lb_id=self.rbac_public_lb.id,
                                                  roles={role: status},
                                                  api=api, api_args=api_args,
                                                  check_lb_active=True)
            errors.extend(error_msg)
        self.assertFalse(len(errors), 'ERRORS: {}'.format(errors))

    # ---- INTERNAL IPv6 VIP ROUTINES -----
    def _add_IPV6_vip(self):
        _addr_ver = 'IPV6'
        ipv6_api_args = {'load_balancer_id': self.rbac_public_lb.id,
                         'type': self.type_,
                         'ipVersion': _addr_ver}
        vip = self.user_admin.add_virtual_ip(**ipv6_api_args)
        self.lbaas_provider.wait_for_status(self.rbac_public_lb.id)
        return vip.entity
