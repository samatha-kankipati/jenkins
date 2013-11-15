from ccengine.common.decorators import attr
from testrepo.common.testfixtures.load_balancers \
    import LoadBalancersRBACFixture


class TestAccessListsRBAC(LoadBalancersRBACFixture):

    @attr('rbac')
    def test_rbac_list_access_list(self):
        '''List access lists with admin, observer, creator roles'''
        api = self.roles.get_api_name()
        roles = self.roles.get_role_response_codes(api=api)
        api_args = {'load_balancer_id': self.rbac_lb.id}
        errors = self.roles.validate_roles(roles=roles, api=api,
                                           api_args=api_args)
        self.assertFalse(len(errors), 'ERRORS: {}'.format(errors))

    @attr('rbac')
    def test_rbac_create_access_list(self):
        '''Create access list item with admin, observer, and creator roles'''
        api = self.roles.get_api_name()
        roles = self.roles.get_role_response_codes(api=api)

        # Define unique ACLs - doesn't matter which role gets which ACL
        api_args = list()
        for octet in xrange(len(roles)):
            perm = 'ALLOW' if octet % 2 == 1 else 'DENY'
            arg_dict = {'load_balancer_id': self.rbac_lb.id,
                        'address': '11.11.11.{0!s}'.format(octet + 10),
                        'type': perm}
            api_args.append(arg_dict)

        errors = self.roles.validate_roles(roles=roles, api=api,
                                           api_args=api_args,
                                           check_lb_active=True)
        self.assertFalse(len(errors), 'ERRORS: {}'.format(errors))

    @attr('rbac')
    def test_rbac_delete_access_list_item(self):
        '''Delete ACL item with admin, observer, creator roles: FAIL'''
        api = self.roles.get_api_name()
        roles = self.roles.get_role_response_codes(api=api)
        api_args = {'load_balancer_id': self.rbac_lb.id,
                    'network_item_id': 'NOT SET'}

        acl_args = {'load_balancer_id': self.rbac_lb.id,
                    'address': 'NOT_SET',
                    'type': 'ALLOW'}

        acl_net = '10.10.10.'
        octet = 10

        errors = list()
        for role, status in roles.items():
            acl_args['address'] = '{0}{1!s}'.format(acl_net, octet)
            acl_item = self._create_acl_and_return_acl_item(args=acl_args)

            api_args['network_item_id'] = acl_item.id
            error_msgs = self.roles.validate_roles(roles={role: status},
                                                   api=api, api_args=api_args,
                                                   check_lb_active=True)
            errors.extend(error_msgs)
            octet += 10
        self.assertFalse(len(errors), 'ERRORS: {}'.format(errors))

    @attr('rbac')
    def test_rbac_batch_delete_access_list_items(self):
        ''' Batch delete ACL items with admin, observer, creator roles'''
        api = self.roles.get_api_name()
        roles = self.roles.get_role_response_codes(api=api)

        api_args = {'load_balancer_id': self.rbac_lb.id,
                    'network_item_id_list': 'NOT SET'}

        acl_args = {'load_balancer_id': self.rbac_lb.id,
                    'address': '12.12.12.12',
                    'type': 'ALLOW'}

        errors = list()
        for role, status in roles.iteritems():
            acl_item = self._create_acl_and_return_acl_item(args=acl_args)

            api_args['network_item_id_list'] = [acl_item.id]
            role_err = self.roles.validate_roles(api=api, roles={role: status},
                                                 api_args=api_args,
                                                 check_lb_active=True)
            errors.extend(role_err)
        self.assertFalse(len(errors), 'ERRORS: {}'.format(errors))

    @attr('rbac')
    def test_rbac_delete_access_list(self):
        ''' Delete access list with admin, observer and creator roles '''
        api = self.roles.get_api_name()
        roles = self.roles.get_role_response_codes(api=api)
        api_args = {'load_balancer_id': self.rbac_lb.id}
        acl_args = {'load_balancer_id': self.rbac_lb.id,
                    'address': '12.12.12.12',
                    'type': 'ALLOW'}

        errors = list()
        for role, status in roles.iteritems():
            self._create_acl_and_return_acl_item(args=acl_args)
            role_err = self.roles.validate_roles(api=api, roles={role: status},
                                                 api_args=api_args,
                                                 check_lb_active=True,)
            errors.extend(role_err)
        self.assertFalse(len(errors), 'ERRORS: {}'.format(errors))

    # ------- PRIVATE ACL-SPECIFIC ROUTINES --------
    def _create_acl_and_return_acl_item(self, args):
        setup_str = ('\n\n\n=====> Setting up ACL for deletion <=====\n\n')
        self.fixture_log.info(setup_str)
        lb_id = args['load_balancer_id']

        self.user_admin.create_access_list(**args)
        self.lbaas_provider.wait_for_status(lb_id)
        acl_list = self.user_admin.get_access_list(lb_id).entity

        acl_item = None
        for item in acl_list:
            if item.address == args['address']:
                acl_item = item
        return acl_item
