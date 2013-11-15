from testrepo.common.testfixtures.load_balancers \
    import BaseLoadBalancersFixture
from ccengine.common.decorators import attr


class AllowedDomainTests(BaseLoadBalancersFixture):

    @classmethod
    def setUpClass(cls):
        super(AllowedDomainTests, cls).setUpClass()

    @attr('positive')
    def test_allowed_domain_calls(self):
        '''Testing allowed domain calls'''
        r = self.mgmt_client.get_allowed_domains()
        self.assertEquals(r.status_code, 200)
        self.assertTrue(len(r.entity) > 0)
        r = self.mgmt_client.add_allowed_domain('rackspace.com')
        self.assertEquals(r.status_code, 200)
        r = self.mgmt_client.get_allowed_domains()
        self.assertEquals(r.status_code, 200)
        name = None
        for domain in r.entity:
            if domain.name == 'rackspace.com':
                name = domain.name
                break
        self.assertIsNotNone(name)
        r = self.mgmt_client.delete_allowed_domain(name)
        self.assertEquals(r.status_code, 200)
        r = self.mgmt_client.get_allowed_domains()
        self.assertEquals(r.status_code, 200)
        for domain in r.entity:
            if domain.name == 'rackspace.com':
                name = None
                break
        self.assertIsNotNone(name)
