from testrepo.common.testfixtures.load_balancers \
    import LoadBalancersRBACFixture
from ccengine.common.decorators import attr


class TestVirtualIpsRBAC(LoadBalancersRBACFixture):

    @classmethod
    def setUpClass(cls):
        super(TestVirtualIpsRBAC, cls).setUpClass()
        cls.rbac_public_lb = cls.lbaas_provider.create_active_load_balancer(
            virtualIps=[{'type': 'PUBLIC'}]).entity

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
        '''List virtual ips with observer and creator roles.'''
        observer_resp = self.observer.list_virtual_ips(self.rbac_lb.id)
        self.assertEquals(observer_resp.status_code, 200, 'Observer should be'
                          ' allowed to list virtual ips.')
        creator_resp = self.creator.list_virtual_ips(self.rbac_lb.id)
        self.assertEquals(creator_resp.status_code, 200, 'Creator should be'
                          ' allowed to list virtual ips.')

    @attr('rbac')
    def test_rbac_add_ipv6_virtual_ip(self):
        '''Add IPv6 virtual ip with observer and creator roles.'''
        observer_resp = self.observer.add_virtual_ip(self.rbac_public_lb.id,
                                                     type='PUBLIC',
                                                     ipVersion='IPV6')
        self.assertEquals(observer_resp.status_code, 405, 'Observer should not'
                          ' be allowed to add virtual ips.')
        creator_resp = self.creator.add_virtual_ip(self.rbac_public_lb.id,
                                                   type='PUBLIC',
                                                   ipVersion='IPV6')
        self.assertEquals(creator_resp.status_code, 202, 'Creator should be'
                          ' allowed to add virtual ips.')

    @attr('rbac')
    def test_rbac_remove_ipv6_virtual_ip(self):
        '''Remove IPv6 virtual ip with observer and creator roles.'''
        ipv6_vip = self.user_admin.add_virtual_ip(self.rbac_public_lb.id,
                                                  type='PUBLIC',
                                                  ipVersion='IPV6').entity
        self.lbaas_provider.wait_for_status(self.rbac_public_lb.id)
        observer_resp = self.observer.delete_virtual_ip(self.rbac_public_lb.id,
                                                        ipv6_vip.id)
        self.assertEquals(observer_resp.status_code, 405, 'Observer should not'
                          ' be allowed to remove virtual ips.')
        creator_resp = self.creator.delete_virtual_ip(self.rbac_public_lb.id,
                                                      ipv6_vip.id)
        self.assertEquals(creator_resp.status_code, 405, 'Creator should not '
                          'be allowed to remove virtual ips.')
