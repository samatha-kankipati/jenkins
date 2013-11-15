from testrepo.common.testfixtures.load_balancers import \
    BaseLoadBalancersFixture
from ccengine.common.decorators import attr
from ccengine.domain.types import LoadBalancerStatusTypes as LBST


class TestLoadBalancers(BaseLoadBalancersFixture):

    @attr('cleanup', 'delete_all')
    def test_delete_all_load_balancers(self):
        lbs = self.lbaas_provider.client.list_load_balancers().entity
        while len(lbs) >= 100:
            for lb in lbs:
                if lb.status == LBST.ACTIVE:
                    r = self.lbaas_provider.client.delete_load_balancer(str(lb.id))
                elif lb.status == LBST.ERROR:
                    r = self.lbaas_provider.mgmt_client.\
                        delete_errored_load_balancer(str(lb.id))
                elif lb.status == LBST.SUSPENDED:
                    r = self.lbaas_provider.mgmt_client.\
                        delete_suspended_load_balancer(str(lb.id))
                else:
                    r = self.lbaas_provider.mgmt_client.\
                        sync_load_balancer(str(lb.id))
                self.assertTrue(r.ok)
            lbs = self.lbaas_provider.client.list_load_balancers().entity
        for lb in lbs:
            if lb.status == LBST.ACTIVE:
                r = self.lbaas_provider.client.delete_load_balancer(str(lb.id))
            elif lb.status == LBST.ERROR:
                r = self.lbaas_provider.mgmt_client.\
                    delete_errored_load_balancer(str(lb.id))
            elif lb.status == LBST.SUSPENDED:
                r = self.lbaas_provider.mgmt_client.\
                    delete_suspended_load_balancer(str(lb.id))
            else:
                r = self.lbaas_provider.mgmt_client.\
                    sync_load_balancer(str(lb.id))
            self.assertTrue(r.ok)
