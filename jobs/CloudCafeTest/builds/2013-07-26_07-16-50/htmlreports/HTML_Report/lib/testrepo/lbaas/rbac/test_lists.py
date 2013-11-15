from testrepo.common.testfixtures.load_balancers \
    import LoadBalancersRBACFixture
from ccengine.common.decorators import attr


class TestListsRBAC(LoadBalancersRBACFixture):

    @attr('smoke', 'positive')
    def test_list_protocols(self):
        '''List protocols with observer and creator roles.'''
        observer_resp = self.observer.list_protocols()
        self.assertEqual(observer_resp.status_code, 200, 'Observer should be '
                         'allowed to list protocols.')
        creator_resp = self.creator.list_protocols()
        self.assertEqual(creator_resp.status_code, 200, 'Creator should be '
                         'allowed to list protocols.')

    @attr('smoke', 'positive')
    def test_list_algorithms(self):
        '''List algorithms with observer and creator roles.'''
        observer_resp = self.observer.list_algorithms()
        self.assertEqual(observer_resp.status_code, 200, 'Observer should be '
                         'allowed to list algorithms.')
        creator_resp = self.creator.list_algorithms()
        self.assertEqual(creator_resp.status_code, 200, 'Creator should be '
                         'allowed to list algorithms.')

    @attr('smoke', 'positive')
    def test_list_absolute_limits(self):
        '''List protocols with observer and creator roles.'''
        observer_resp = self.observer.list_absolute_limits()
        self.assertEqual(observer_resp.status_code, 200, 'Observer should be '
                         'allowed to list absolute limits.')
        creator_resp = self.creator.list_absolute_limits()
        self.assertEqual(creator_resp.status_code, 200, 'Creator should be '
                         'allowed to list absolute limits.')
