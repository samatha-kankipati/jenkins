from testrepo.common.testfixtures.load_balancers \
    import LoadBalancersRBACFixture
from ccengine.common.decorators import attr


class TestNodesRBAC(LoadBalancersRBACFixture):

    @attr('rbac')
    def test_rbac_list_nodes(self):
        '''List nodes with observer and creator roles.'''
        observer_resp = self.observer.list_nodes(self.rbac_lb.id)
        self.assertEquals(observer_resp.status_code, 200, 'Observer should '
                          'be allowed to list nodes.')
        creator_resp = self.creator.list_nodes(self.rbac_lb.id)
        self.assertEquals(creator_resp.status_code, 200, 'Creator should '
                          'be allowed to list nodes.')

    @attr('rbac')
    def test_rbac_get_node_details(self):
        '''Get node details with observer and creator roles.'''
        node_id = self.user_admin.list_nodes(self.rbac_lb.id).entity[0].id
        observer_resp = self.observer.get_node(self.rbac_lb.id, node_id)
        self.assertEquals(observer_resp.status_code, 200, 'Observer should '
                          'be allowed to view node details.')
        creator_resp = self.creator.get_node(self.rbac_lb.id, node_id)
        self.assertEquals(creator_resp.status_code, 200, 'Creator should '
                          'be allowed to view node details.')

    @attr('rbac')
    def test_rbac_view_node_service_events(self):
        '''List node service events with observer and creator roles.'''
        observer_resp = self.observer.list_node_service_events(self.rbac_lb.id)
        self.assertEquals(observer_resp.status_code, 200, 'Observer should '
                          'be allowed to list node service events.')
        creator_resp = self.creator.list_node_service_events(self.rbac_lb.id)
        self.assertEquals(creator_resp.status_code, 200, 'Creator should '
                          'be allowed to list node service events.')

    @attr('rbac')
    def test_rbac_delete_node(self):
        '''Delete node with observer and creator roles.'''
        node_id = self.user_admin.list_nodes(self.rbac_lb.id).entity[0].id
        observer_resp = self.observer.delete_node(self.rbac_lb.id, node_id)
        self.assertEquals(observer_resp.status_code, 405, 'Observer should '
                          'not be allowed to delete nodes.')
        creator_resp = self.creator.delete_node(self.rbac_lb.id, node_id)
        self.assertEquals(creator_resp.status_code, 405, 'Creator should '
                          'not be allowed to delete nodes.')

    @attr('rbac')
    def test_rbac_batch_delete_nodes(self):
        '''Batch delete nodes with observer and creator roles.'''
        node_id = self.user_admin.list_nodes(self.rbac_lb.id).entity[0].id
        observer_resp = self.observer.batch_delete_nodes(self.rbac_lb.id,
                                                         [node_id])
        self.assertEquals(observer_resp.status_code, 405, 'Observer should '
                          'not be allowed to batch delete nodes.')
        creator_resp = self.creator.batch_delete_nodes(self.rbac_lb.id,
                                                       [node_id])
        self.assertEquals(creator_resp.status_code, 405, 'Creator should '
                          'not be allowed to batch delete nodes.')

    @attr('rbac')
    def test_rbac_add_node(self):
        '''Add node with observer and creator roles.'''
        address = '10.1.1.1'
        port = 80
        condition = 'ENABLED'
        observer_resp = self.observer.add_nodes(self.rbac_lb.id,
                                                address=address,
                                                port=port,
                                                condition=condition)
        self.assertEquals(observer_resp.status_code, 405, 'Observer should '
                          'not be allowed to add nodes.')
        creator_resp = self.creator.add_nodes(self.rbac_lb.id,
                                              address=address,
                                              port=port,
                                              condition=condition)
        self.assertEquals(creator_resp.status_code, 202, 'Creator should '
                          'be allowed to add nodes.')

    @attr('rbac')
    def test_rbac_update_node(self):
        '''Update node with observer and creator roles.'''
        condition='ENABLED'
        node_id = self.user_admin.list_nodes(self.rbac_lb.id).entity[0].id
        observer_resp = self.observer.update_node(self.rbac_lb.id, node_id,
                                                  condition=condition)
        self.assertEquals(observer_resp.status_code, 405, 'Observer should '
                          'not be allowed to update node.')
        creator_resp = self.creator.update_node(self.rbac_lb.id, node_id,
                                                condition=condition)
        self.assertEquals(creator_resp.status_code, 202, 'Creator should '
                          'be allowed to update node.')
