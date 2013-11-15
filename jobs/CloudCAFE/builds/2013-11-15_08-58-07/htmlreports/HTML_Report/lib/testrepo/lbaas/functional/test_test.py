from testrepo.common.testfixtures.load_balancers\
    import BaseLoadBalancersFixture
from ccengine.common.decorators import attr


class TestLoadBalancers(BaseLoadBalancersFixture):

    @attr('test')
    def test_test(self):
        pass
