from ccengine.common.decorators import attr
from testrepo.common.testfixtures.load_balancers \
    import LoadBalancersRBACFixture


class TestNodesRBAC(LoadBalancersRBACFixture):

    @attr('rbac')
    def test_rbac_list_nodes(self):
        '''List nodes with admin, observer, and creator roles'''
        api = self.roles.get_api_name()
        roles = self.roles.get_role_response_codes(api=api)
        api_args = {'load_balancer_id': self.rbac_lb.id}

        errors = self.roles.validate_roles(roles=roles, api=api,
                                           api_args=api_args)
        self.assertFalse(len(errors), 'ERRORS: {}'.format(errors))

    @attr('rbac')
    def test_rbac_get_node(self):
        '''Get node details with admin, observer, and creator roles'''
        api = self.roles.get_api_name()
        roles = self.roles.get_role_response_codes(api=api)
        api_args = {'load_balancer_id': self.rbac_lb.id,
                    'node_id': self._get_node_id()}

        errors = self.roles.validate_roles(roles=roles, api=api,
                                           api_args=api_args)
        self.assertFalse(len(errors), 'ERRORS: {}'.format(errors))

    @attr('rbac')
    def test_rbac_list_node_service_events(self):
        '''List node service events with observer and creator roles'''
        api = self.roles.get_api_name()
        roles = self.roles.get_role_response_codes(api=api)
        api_args = {'load_balancer_id': self.rbac_lb.id}

        errors = self.roles.validate_roles(roles=roles, api=api,
                                           api_args=api_args)
        self.assertFalse(len(errors), 'ERRORS: {}'.format(errors))

    @attr('rbac')
    def test_rbac_delete_node(self):
        '''Delete node with admin, observer, and creator roles'''
        api = self.roles.get_api_name()
        roles = self.roles.get_role_response_codes(api=api)
        api_args = {'load_balancer_id': self.rbac_lb.id,
                    'node_id': 'NOT_SET'}

        octet123 = '192.167.1.'
        octet4 = 100
        errors = list()
        for role, status in roles.iteritems():
            node = self._add_node(address='{0}{1!s}'.format(octet123, octet4))
            api_args['node_id'] = node.id

            error_msgs = self.roles.validate_roles(roles={role: status},
                                                   api=api, api_args=api_args,
                                                   check_lb_active=True)
            errors.extend(error_msgs)
            octet4 += 10
        self.assertFalse(len(errors), 'ERRORS: {}'.format(errors))

    @attr('rbac')
    def test_rbac_batch_delete_nodes(self):
        '''Batch delete nodes with admin, observer, and creator roles'''
        api = self.roles.get_api_name()
        roles = self.roles.get_role_response_codes(api=api)
        api_args = {'load_balancer_id': self.rbac_lb.id,
                    'node_id_list': 'NOT_SET'}

        octet123 = '192.168.1.'
        octet4 = 100
        errors = list()
        for role, status in roles.iteritems():
            node1 = self._add_node(address='{0}{1!s}'.
                                   format(octet123, octet4))
            node2 = self._add_node(address='{0}{1!s}'.
                                   format(octet123, octet4 + 1))

            api_args['node_id_list'] = [node1.id, node2.id]
            error_msgs = self.roles.validate_roles(roles={role: status},
                                                   api=api, api_args=api_args,
                                                   check_lb_active=True)
            errors.extend(error_msgs)
            octet4 += 10
        self.assertFalse(len(errors), 'ERRORS: {}'.format(errors))

    @attr('rbac')
    def test_rbac_add_node(self):
        '''Add node with admin, observer, and creator roles'''
        api = self.roles.get_api_name()
        roles = self.roles.get_role_response_codes(api=api)

        api_args = list()
        for index in xrange(len(roles)):
            arg_dict = {'load_balancer_id': self.rbac_lb.id,
                        'address': '192.168.10.{0!s}'.format((index + 1) * 10),
                        'port': 80,
                        'condition': 'ENABLED'}
            api_args.append(arg_dict)
        errors = self.roles.validate_roles(roles=roles, api=api,
                                           api_args=api_args,
                                           check_lb_active=True)
        self.assertFalse(len(errors), 'ERRORS: {}'.format(errors))

    @attr('rbac')
    def test_rbac_update_node(self):
        '''Update node with admin, observer, and creator roles'''
        api = self.roles.get_api_name()
        roles = self.roles.get_role_response_codes(api=api)
        api_args = {'load_balancer_id': self.rbac_lb.id,
                    'node_id': self._get_node_id(),
                    'condition': 'ENABLED'}

        errors = self.roles.validate_roles(roles=roles, api=api,
                                           api_args=api_args,
                                           check_lb_active=True)
        self.assertFalse(len(errors), 'ERRORS: {}'.format(errors))

    # ---- INTERNAL NODE ROUTINES -----
    def _get_node_id(self):
        return self.user_admin.list_nodes(self.rbac_lb.id).entity[0].id

    def _add_node(self, address=None):
        if address is None:
            address = '10.1.1.1'
        args = {'load_balancer_id': self.rbac_lb.id,
                'address': address,
                'port': 80,
                'condition': 'ENABLED'}
        node_list = self.user_admin.add_nodes(**args)
        self.lbaas_provider.wait_for_status(self.rbac_lb.id)
        return node_list.entity[0]
