from ccengine.common.decorators import attr
import testrepo.lbaas.functional.test_content_caching as LBContentCaching


class NodelessContentCachingSmokeTests(
        LBContentCaching.ContentCachingSmokeTests):

    @classmethod
    def setUpClass(cls):
        super(NodelessContentCachingSmokeTests, cls).setUpClass()
        cls.orig_lb = cls.lb
        cls.lb = cls.lbaas_provider.create_active_load_balancer(
            nodeless=True).entity
        cls.lbs_to_delete.append(cls.lb.id)

    @attr('nodeless')
    def test_nodeless_content_caching_loadbalancer(self):
        """ Testing content caching on nodeless loadbalancers """
        return self.test_content_caching_loadbalancer()
