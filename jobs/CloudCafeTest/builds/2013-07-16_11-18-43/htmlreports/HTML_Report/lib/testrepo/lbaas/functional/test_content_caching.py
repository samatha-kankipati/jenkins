from testrepo.common.testfixtures.load_balancers\
    import LoadBalancersSmokeFixture
from ccengine.common.decorators import attr
from ccengine.domain.types import LoadBalancerStatusTypes as LBStatus
import ccengine.common.tools.datagen as datagen


class ContentCachingSmokeTests(LoadBalancersSmokeFixture):

    @attr('smoke', 'positive')
    def test_content_caching_loadbalancer(self):
        '''Testing content caching on loadbalancers'''
        r = self.client.get_content_caching(self.lb.id)
        cc = r.entity
        self.assertEquals(r.status_code, 200)
        self.assertIsNotNone(cc.enabled)
        if not cc.enabled:
            r = self.client.update_content_caching(self.lb.id, True)
            self.assertEquals(r.status_code, 202)
            self.lbaas_provider.wait_for_status(self.lb.id)
            r = self.client.get_content_caching(self.lb.id)
            new_cc = r.entity
            self.assertEquals(r.status_code, 200)
            self.assertTrue(new_cc.enabled)
        if cc.enabled:
            r = self.client.update_content_caching(self.lb.id, False)
            self.assertEquals(r.status_code, 202)
            self.lbaas_provider.wait_for_status(self.lb.id)
            r = self.client.get_content_caching(self.lb.id)
            cc = r.entity
            self.assertEquals(r.status_code, 200)
            self.assertFalse(cc.enabled)
        lb2 = self.lbaas_provider.create_active_load_balancer(
            contentCaching={'enabled': True}).entity
        self.lbs_to_delete.append(lb2.id)
        self.assertIsNotNone(lb2.contentCaching)
        r = self.client.update_content_caching(self.lb.id, 'broken')
        self.assertEquals(r.status_code, 500)
