from testrepo.common.testfixtures.load_balancers \
    import LoadBalancersRBACFixture
from ccengine.common.decorators import attr


class TestLoadBalancersRBAC(LoadBalancersRBACFixture):

    @attr('rbac')
    def test_rbac_list_load_balancers(self):
        '''List load balancers with observer and creator roles.'''
        observer_resp = self.observer.list_load_balancers()
        self.assertEquals(observer_resp.status_code,
                          200,
                          'Observer role should be allowed to list '
                          'load balancers.')
        creator_resp = self.creator.list_load_balancers()
        self.assertEquals(creator_resp.status_code,
                          200,
                          'Creator role should be allowed to list '
                          'load balancers.')

    @attr('rbac')
    def test_rbac_get_load_balancer(self):
        '''Get load balancer details with observer and creator roles.'''
        observer_resp = self.observer.get_load_balancer(self.rbac_lb.id)
        self.assertEquals(observer_resp.status_code,
                          200,
                          'Observer role should be allowed to list '
                          'load balancer details.')
        creator_resp = self.creator.get_load_balancer(self.rbac_lb.id)
        self.assertEquals(creator_resp.status_code,
                          200,
                          'Creator role should be allowed to get '
                          'load balancer details.')

    @attr('rbac')
    def test_rbac_create_load_balancer(self):
        '''Create load balancer using observer and creator roles.'''
        virtualIps = [{'type': 'SERVICENET'}]
        nodes = [{'address': '10.0.0.1', 'condition': 'ENABLED', 'port': '80'}]
        observer_resp = self.observer.create_load_balancer(
            name='ObserverLB',
            protocol='HTTP',
            port=80,
            virtualIps=virtualIps,
            nodes=nodes)
        self.assertEquals(observer_resp.status_code, 405, 'Observer should not'
                          'be allowed to create a load balancer.')
        creator_resp = self.creator.create_load_balancer(
            name='CreatorLB',
            protocol='HTTP',
            port=80,
            virtualIps=virtualIps,
            nodes=nodes)
        self.assertEquals(creator_resp.status_code, 202, 'Creator should '
                          'be allowed to create a load balancer.')
        self.lbaas_provider.wait_for_status(creator_resp.entity.id)
        self.lbs_to_delete.append(creator_resp.entity.id)

    @attr('rbac')
    def test_rbac_update_load_balancer(self):
        '''Update load balancer using observer and creator roles.'''
        observer_resp = self.observer.update_load_balancer(self.rbac_lb.id,
                                                           name='Test')
        self.assertEquals(observer_resp.status_code, 405, 'Observer should not'
                          ' be allowed to update a load balancer')
        creator_resp = self.creator.update_load_balancer(self.rbac_lb.id,
                                                         name='Test')
        self.assertEquals(creator_resp.status_code, 202, 'Creator should'
                          ' be allowed to update a load balancer')

    @attr('rbac')
    def test_rbac_delete_load_balancer(self):
        '''Delete a load balancer using observer and creator roles.'''
        observer_resp = self.observer.delete_load_balancer(self.rbac_lb.id)
        self.assertEquals(observer_resp.status_code, 405, 'Observer should not'
                          ' be allowed to delete a load balancer')
        creator_resp = self.creator.delete_load_balancer(self.rbac_lb.id)
        self.assertEquals(creator_resp.status_code, 405, 'Creator should not'
                          ' be allowed to delete a load balancer')

    @attr('rbac')
    def test_rbac_batch_delete_load_balancer(self):
        '''Batch delete a load balancer using observer and creator roles.'''
        observer_resp = self.observer.batch_delete_load_balancers(
            [self.rbac_lb.id])
        self.assertEquals(observer_resp.status_code, 405, 'Observer should not'
                          ' be allowed to batch delete a load balancer')
        creator_resp = self.creator.batch_delete_load_balancers(
            [self.rbac_lb.id])
        self.assertEquals(creator_resp.status_code, 405, 'Creator should not'
                          ' be allowed to batch delete a load balancer')

    @attr('rbac')
    def list_load_balancer_stats(self):
        '''List load balancer stats with observer and creator roles.'''
        observer_resp = self.observer.list_load_balancer_stats(self.rbac_lb.id)
        self.assertEquals(observer_resp.status_code, 200, 'Observer should be '
                          'allowed to list load balancer stats.')
        creator_resp = self.creator.list_load_balancer_stats(self.rbac_lb.id)
        self.assertEquals(creator_resp.status_code, 200, 'Creator should be '
                          'allowed to list load balancer stats.')
