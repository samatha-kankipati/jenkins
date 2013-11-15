from testrepo.common.testfixtures.load_balancers \
    import LoadBalancersRBACFixture
from ccengine.common.decorators import attr


class TestLoadBalancerMetadataRBAC(LoadBalancersRBACFixture):

    @attr('rbac')
    def test_rbac_list_load_balancer_metadata(self):
        '''List metadata of a load balancer with observer and creator roles.'''
        observer_resp = self.observer.list_load_balancer_metadata(
            self.rbac_lb.id)
        self.assertEquals(observer_resp.status_code, 200, 'Observer should '
                          'be allowed to list metadata of a load balancer.')
        creator_resp = self.creator.list_load_balancer_metadata(
            self.rbac_lb.id)
        self.assertEquals(creator_resp.status_code, 200, 'Creator should '
                          'be allowed to list metadata of a load balancer.')

    @attr('rbac')
    def test_rbac_get_load_balancer_metadata_item(self):
        '''Get load balancer metadata item with observer and creator roles.'''
        key = 'color'
        value = 'red'
        meta_item = self.user_admin.add_load_balancer_metadata(self.rbac_lb.id,
            [{'key': key, 'value': value}]).entity[0]
        observer_resp = self.observer.get_load_balancer_meta_item(
            self.rbac_lb.id, meta_item.id)
        self.assertEquals(observer_resp.status_code, 200, 'Observer should '
                          'be allowed to view a load balancer metadata item.')
        creator_resp = self.creator.get_load_balancer_meta_item(
            self.rbac_lb.id, meta_item.id)
        self.assertEquals(creator_resp.status_code, 200, 'Creator should '
                          'be allowed to view a load balancer metadata item.')

    @attr('rbac')
    def test_rbac_add_load_balancer_metadata(self):
        '''Add load balancer metadata with observer and creator roles.'''
        key = 'colour'
        value = 'red'
        observer_resp = self.observer.add_load_balancer_metadata(
            self.rbac_lb.id, [{'key': key, 'value': value}])
        self.assertEquals(observer_resp.status_code, 405, 'Observer should not'
                          ' be allowed to add load balancer metadata item.')
        creator_resp = self.creator.add_load_balancer_metadata(
            self.rbac_lb.id, [{'key': key, 'value': value}])
        self.assertEquals(creator_resp.status_code, 200, 'Creator should '
                          'be allowed to add load balancer metadata item.')

    @attr('rbac')
    def test_rbac_update_load_balancer_meta_item(self):
        '''Update load balancer meta item with observer and creator roles.'''
        key = 'kolor'
        value = 'red'
        new_value = 'blue'
        meta_item = self.user_admin.add_load_balancer_metadata(self.rbac_lb.id,
            [{'key': key, 'value': value}]).entity[0]
        observer_resp = self.observer.update_load_balancer_meta_item(
            self.rbac_lb.id, meta_item.id, new_value)
        self.assertEquals(observer_resp.status_code, 405, 'Observer should not'
                          ' be allowed to update a load balancer metadata '
                          'item.')
        creator_resp = self.creator.update_load_balancer_meta_item(
            self.rbac_lb.id, meta_item.id, new_value)
        self.assertEquals(creator_resp.status_code, 200, 'Creator should '
                          'be allowed to update a load balancer metadata '
                          'item.')

    @attr('rbac')
    def test_rbac_delete_load_balancer_meta_item(self):
        '''Delete load balancer meta item with observer and creator roles.'''
        key = 'kolour'
        value = 'red'
        meta_item = self.user_admin.add_load_balancer_metadata(self.rbac_lb.id,
            [{'key': key, 'value': value}]).entity[0]
        observer_resp = self.observer.delete_load_balancer_meta_item(
            self.rbac_lb.id, meta_item.id)
        self.assertEquals(observer_resp.status_code, 405, 'Observer should not'
                          ' be allowed to delete a load balancer metadata '
                          'item.')
        creator_resp = self.creator.delete_load_balancer_meta_item(
            self.rbac_lb.id, meta_item.id)
        self.assertEquals(creator_resp.status_code, 405, 'Creator should not'
                          'be allowed to delete a load balancer metadata '
                          'item.')

    @attr('rbac')
    def test_rbac_batch_delete_load_balancer_meta_item(self):
        '''Batch delete lb meta items with observer and creator roles.'''
        key = 'collor'
        value = 'red'
        meta_item = self.user_admin.add_load_balancer_metadata(self.rbac_lb.id,
            [{'key': key, 'value': value}]).entity[0]
        observer_resp = self.observer.batch_delete_load_balancer_meta_items(
            self.rbac_lb.id, [meta_item.id])
        self.assertEquals(observer_resp.status_code, 405, 'Observer should not'
                          ' be allowed to batch delete a load balancer '
                          'metadata items.')
        creator_resp = self.creator.batch_delete_load_balancer_meta_items(
            self.rbac_lb.id, [meta_item.id])
        self.assertEquals(creator_resp.status_code, 405, 'Creator should not'
                          'be allowed to batch delete a load balancer metadata'
                          ' items.')


class TestNodeMetadataRBAC(LoadBalancersRBACFixture):

    @attr('rbac')
    def test_rbac_list_node_metadata(self):
        '''List metadata of a node with observer and creator roles.'''
        node_id = self.user_admin.list_nodes(self.rbac_lb.id).entity[0].id
        observer_resp = self.observer.list_node_metadata(
            self.rbac_lb.id, node_id)
        self.assertEquals(observer_resp.status_code, 200, 'Observer should '
                          'be allowed to list metadata of a node.')
        creator_resp = self.creator.list_node_metadata(
            self.rbac_lb.id, node_id)
        self.assertEquals(creator_resp.status_code, 200, 'Creator should '
                          'be allowed to list metadata of a node.')

    @attr('rbac')
    def test_rbac_get_node_metadata_item(self):
        '''Get node metadata item with observer and creator roles.'''
        node_id = self.user_admin.list_nodes(self.rbac_lb.id).entity[0].id
        key = 'ccolor'
        value = 'red'
        meta_item = self.user_admin.add_node_metadata(self.rbac_lb.id, node_id,
            [{'key': key, 'value': value}]).entity[0]
        observer_resp = self.observer.get_node_meta_item(
            self.rbac_lb.id, node_id, meta_item.id)
        self.assertEquals(observer_resp.status_code, 200, 'Observer should '
                          'be allowed to view a node metadata item.')
        creator_resp = self.creator.get_node_meta_item(
            self.rbac_lb.id, node_id, meta_item.id)
        self.assertEquals(creator_resp.status_code, 200, 'Creator should '
                          'be allowed to view a node metadata item.')

    @attr('rbac')
    def test_rbac_add_node_metadata(self):
        '''Add node metadata with observer and creator roles.'''
        node_id = self.user_admin.list_nodes(self.rbac_lb.id).entity[0].id
        key = 'ccolour'
        value = 'red'
        observer_resp = self.observer.add_node_metadata(
            self.rbac_lb.id, node_id, [{'key': key, 'value': value}])
        self.assertEquals(observer_resp.status_code, 405, 'Observer should not'
                          ' be allowed to add node metadata item.')
        creator_resp = self.creator.add_node_metadata(
            self.rbac_lb.id, node_id, [{'key': key, 'value': value}])
        self.assertEquals(creator_resp.status_code, 200, 'Creator should '
                          'be allowed to add node metadata item.')

    @attr('rbac')
    def test_rbac_update_node_meta_item(self):
        '''Update node meta item with observer and creator roles.'''
        node_id = self.user_admin.list_nodes(self.rbac_lb.id).entity[0].id
        key = 'kkolor'
        value = 'red'
        new_value = 'blue'
        meta_item = self.user_admin.add_node_metadata(self.rbac_lb.id, node_id,
            [{'key': key, 'value': value}]).entity[0]
        observer_resp = self.observer.update_node_meta_item(
            self.rbac_lb.id, node_id, meta_item.id, new_value)
        self.assertEquals(observer_resp.status_code, 405, 'Observer should not'
                          ' be allowed to update a node metadata '
                          'item.')
        creator_resp = self.creator.update_node_meta_item(
            self.rbac_lb.id, node_id, meta_item.id, new_value)
        self.assertEquals(creator_resp.status_code, 200, 'Creator should '
                          'be allowed to update a node metadata '
                          'item.')

    @attr('rbac')
    def test_rbac_delete_node_meta_item(self):
        '''Delete node meta item with observer and creator roles.'''
        node_id = self.user_admin.list_nodes(self.rbac_lb.id).entity[0].id
        key = 'kkolour'
        value = 'red'
        meta_item = self.user_admin.add_node_metadata(self.rbac_lb.id, node_id,
            [{'key': key, 'value': value}]).entity[0]
        observer_resp = self.observer.delete_node_meta_item(
            self.rbac_lb.id, node_id, meta_item.id)
        self.assertEquals(observer_resp.status_code, 405, 'Observer should not'
                          ' be allowed to delete a node metadata '
                          'item.')
        creator_resp = self.creator.delete_node_meta_item(
            self.rbac_lb.id, node_id, meta_item.id)
        self.assertEquals(creator_resp.status_code, 405, 'Creator should not'
                          'be allowed to delete a node metadata '
                          'item.')

    @attr('rbac')
    def test_rbac_batch_delete_node_meta_item(self):
        '''Batch delete node meta items with observer and creator roles.'''
        node_id = self.user_admin.list_nodes(self.rbac_lb.id).entity[0].id
        key = 'ccollor'
        value = 'red'
        meta_item = self.user_admin.add_node_metadata(self.rbac_lb.id, node_id,
            [{'key': key, 'value': value}]).entity[0]
        observer_resp = self.observer.batch_delete_node_meta_items(
            self.rbac_lb.id, node_id, [meta_item.id])
        self.assertEquals(observer_resp.status_code, 405, 'Observer should not'
                          ' be allowed to batch delete a node '
                          'metadata items.')
        creator_resp = self.creator.batch_delete_node_meta_items(
            self.rbac_lb.id, node_id, [meta_item.id])
        self.assertEquals(creator_resp.status_code, 405, 'Creator should not'
                          'be allowed to batch delete a node metadata'
                          ' items.')
