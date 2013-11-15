from ccengine.common.decorators import attr
import ccengine.common.tools.datagen as datagen
from testrepo.common.testfixtures.load_balancers \
    import LoadBalancersRBACFixture


class TestLoadBalancerMetadataRBAC(LoadBalancersRBACFixture):

    @attr('rbac')
    def test_rbac_list_load_balancer_metadata(self):
        ''' List LB metadata with admin, observer and creator roles'''
        api = self.roles.get_api_name()
        roles = self.roles.get_role_response_codes(api=api)
        api_args = {'load_balancer_id': self.rbac_lb.id}

        errors = self.roles.validate_roles(roles=roles, api=api,
                                           api_args=api_args)
        self.assertFalse(len(errors), 'ERRORS: {}'.format(errors))

    @attr('rbac')
    def test_rbac_get_load_balancer_meta_item(self):
        ''' Get LB metadata item with admin, observer, and creator roles'''
        api = self.roles.get_api_name()
        roles = self.roles.get_role_response_codes(api=api)
        api_args = {'load_balancer_id': self.rbac_lb.id,
                    'meta_id': self._add_lb_metadata().id}

        errors = self.roles.validate_roles(roles=roles, api=api,
                                           api_args=api_args)
        self.assertFalse(len(errors), 'ERRORS: {}'.format(errors))

    @attr('rbac')
    def test_rbac_add_load_balancer_metadata(self):
        ''' Add LB metadata with admin, observer, and creator roles'''
        api = self.roles.get_api_name()
        roles = self.roles.get_role_response_codes(api=api)

        api_args = list()
        for index in xrange(len(roles)):
            api_dict = {'load_balancer_id': self.rbac_lb.id,
                        'metadata': [{'key': datagen.random_string('color'),
                                      'value': 'blue'}]}
            api_args.append(api_dict)

        errors = self.roles.validate_roles(roles=roles, api=api,
                                           api_args=api_args,
                                           check_lb_active=True)
        self.assertFalse(len(errors), 'ERRORS: {}'.format(errors))

    @attr('rbac')
    def test_rbac_update_load_balancer_meta_item(self):
        '''Update LB meta item with admin, observer, and creator roles'''
        api = self.roles.get_api_name()
        roles = self.roles.get_role_response_codes(api=api)

        new_value = 'blue'
        api_args = {'load_balancer_id': self.rbac_lb.id,
                    'meta_id': self._add_lb_metadata().id,
                    'value': new_value}

        errors = self.roles.validate_roles(roles=roles, api=api,
                                           api_args=api_args,
                                           check_lb_active=True)
        self.assertFalse(len(errors), 'ERRORS: {}'.format(errors))

    @attr('rbac')
    def test_rbac_delete_load_balancer_meta_item(self):
        '''Delete LB meta item with admin, observer, and creator roles'''
        api = self.roles.get_api_name()
        roles = self.roles.get_role_response_codes(api=api)

        errors = list()
        for role, status in roles.iteritems():
            api_args = {'load_balancer_id': self.rbac_lb.id,
                        'meta_id': self._add_lb_metadata().id}

            error_msg = self.roles.validate_roles(roles={role: status},
                                                  api=api, api_args=api_args,
                                                  check_lb_active=True)
            errors.extend(error_msg)
        self.assertFalse(len(errors), 'ERRORS: {}'.format(errors))

    @attr('rbac')
    def test_rbac_batch_delete_load_balancer_meta_item(self):
        '''Batch delete LB meta items w/admin, observer and creator roles'''
        api = self.roles.get_api_name()
        roles = self.roles.get_role_response_codes(api=api)

        errors = list()
        for role, status in roles.iteritems():
            api_args = {'load_balancer_id': self.rbac_lb.id,
                        'meta_id_list': [self._add_lb_metadata().id]}

            error_msg = self.roles.validate_roles(roles={role: status},
                                                  api=api, api_args=api_args,
                                                  check_lb_active=True)
            errors.extend(error_msg)
        self.assertFalse(len(errors), 'ERRORS: {}'.format(errors))

    # ----- INTERNAL LB METADATA ROUTINES -----
    def _add_lb_metadata(self):
        args = {'load_balancer_id': self.rbac_lb.id,
                'metadata': [{'key': datagen.random_string('color'),
                             'value': 'red'}]}

        meta_item = (self.user_admin.add_load_balancer_metadata(**args).
                     entity[0])
        self.lbaas_provider.wait_for_status(self.rbac_lb.id)
        return meta_item


class TestNodeMetadataRBAC(LoadBalancersRBACFixture):

    @attr('rbac')
    def test_rbac_list_node_metadata(self):
        '''List metadata of a node with admin, observer, and creator roles'''
        api = self.roles.get_api_name()
        roles = self.roles.get_role_response_codes(api=api)
        api_args = {'load_balancer_id': self.rbac_lb.id,
                    'node_id': self._get_node_id()}

        errors = self.roles.validate_roles(roles=roles, api=api,
                                           api_args=api_args)
        self.assertFalse(len(errors), 'ERRORS: {}'.format(errors))

    @attr('rbac')
    def test_rbac_get_node_meta_item(self):
        '''Get node metadata item with admin, observer, and creator roles'''
        api = self.roles.get_api_name()
        roles = self.roles.get_role_response_codes(api=api)

        meta_node = self._add_lb_node_metadata()
        api_args = {'load_balancer_id': self.rbac_lb.id,
                    'node_id': self._get_node_id(),
                    'meta_id': meta_node.id}

        errors = self.roles.validate_roles(roles=roles, api=api,
                                           api_args=api_args)
        self.assertFalse(len(errors), 'ERRORS: {}'.format(errors))

    @attr('rbac')
    def test_rbac_add_node_metadata(self):
        '''Add node metadata with admin, observer, and creator roles'''
        api = self.roles.get_api_name()
        roles = self.roles.get_role_response_codes(api=api)

        api_args = list()
        for index in xrange(len(roles)):
            arg_dict = {'load_balancer_id': self.rbac_lb.id,
                        'node_id': self._get_node_id(),
                        'metadata': [{'key': datagen.random_string('color'),
                                      'value': 'node_value'}]}
            api_args.append(arg_dict)

        errors = self.roles.validate_roles(roles=roles, api=api,
                                           api_args=api_args,
                                           check_lb_active=True)
        self.assertFalse(len(errors), 'ERRORS: {}'.format(errors))

    @attr('rbac')
    def test_rbac_update_node_meta_item(self):
        '''Update node meta item with admin, observer, and creator roles'''
        api = self.roles.get_api_name()
        roles = self.roles.get_role_response_codes(api=api)

        orig_data = [{'key': 'node_descr_x',
                      'value': 'node_value_x'}]
        metadata = self._add_lb_node_metadata(metadata=orig_data)

        api_args = {'load_balancer_id': self.rbac_lb.id,
                    'node_id': self._get_node_id(),
                    'meta_id': metadata.id,
                    'value': 'updated_value_y'}

        errors = self.roles.validate_roles(roles=roles, api=api,
                                           api_args=api_args,
                                           check_lb_active=True)
        self.assertFalse(len(errors), 'ERRORS: {}'.format(errors))

    @attr('rbac')
    def test_rbac_delete_node_meta_item(self):
        '''Delete node meta item with admin, observer, and creator roles'''
        api = self.roles.get_api_name()
        roles = self.roles.get_role_response_codes(api=api)
        api_args = {'load_balancer_id': self.rbac_lb.id,
                    'node_id': self._get_node_id(),
                    'meta_id': 'TBD'}

        errors = list()
        for role, status in roles.iteritems():
            metadata = self._add_lb_node_metadata()
            api_args['meta_id'] = metadata.id

            error_msgs = self.roles.validate_roles(roles={role: status},
                                                   api=api, api_args=api_args,
                                                   check_lb_active=True)
            errors.extend(error_msgs)
        self.assertFalse(len(errors), 'ERRORS: {}'.format(errors))

    @attr('rbac')
    def test_rbac_batch_delete_node_meta_items(self):
        '''Batch delete node meta items with admin, obsvr and creator roles'''
        api = self.roles.get_api_name()
        roles = self.roles.get_role_response_codes(api=api)
        api_args = {'load_balancer_id': self.rbac_lb.id,
                    'node_id': self._get_node_id(),
                    'meta_id_list': 'TBD'}

        errors = list()
        for role, status in roles.iteritems():
            meta_item_1 = self._add_lb_node_metadata()
            meta_item_2 = self._add_lb_node_metadata()

            api_args['meta_id_list'] = [meta_item_1.id, meta_item_2.id]

            error_msgs = self.roles.validate_roles(roles={role: status},
                                                   api=api, api_args=api_args,
                                                   check_lb_active=True)
            errors.extend(error_msgs)
        self.assertFalse(len(errors), 'ERRORS: {}'.format(errors))

    # ----- INTERNAL LB METADATA ROUTINES -----
    def _add_lb_node_metadata(self, metadata=None):
        if metadata is None:
            metadata = [{'key': datagen.random_string('color'),
                         'value': 'red'}]

        args = {'load_balancer_id': self.rbac_lb.id,
                'node_id': self._get_node_id(),
                'metadata': metadata}

        meta_item = self.user_admin.add_node_metadata(**args).entity[0]
        self.lbaas_provider.wait_for_status(self.rbac_lb.id)
        return meta_item

    def _get_node_id(self):
        return self.user_admin.list_nodes(self.rbac_lb.id).entity[0].id
