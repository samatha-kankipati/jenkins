from testrepo.common.testfixtures.load_balancers \
    import BaseLoadBalancersFixture
from ccengine.common.decorators import attr


class AbsoluteLimitsTests(BaseLoadBalancersFixture):

    @classmethod
    def setUpClass(cls):
        super(AbsoluteLimitsTests, cls).setUpClass()
        cls.lb = cls.lbaas_provider.create_active_load_balancer().entity
        cls.lbs_to_delete.append(cls.lb.id)

    @attr('positive')
    def test_functional_absolute_limits_operations(self):
        '''Testing absolute limits calls'''
        r = self.mgmt_client.get_absolute_limits(self.tenant_id)
        self.assertEquals(r.status_code, 200)
        defaults = r.entity.defaultLimits
        customs = r.entity.customLimits
        self.assertTrue(len(defaults) >= 1 or len(customs) >= 1)
        r = self.mgmt_client.add_absolute_limit(account_id=self.tenant_id,
                                                name=defaults[0].name,
                                                value=defaults[0].value + 10)
        self.assertEquals(r.status_code, 202)
        r = self.mgmt_client.get_absolute_limits(self.tenant_id)
        self.assertEquals(r.status_code, 200)
        customs = r.entity.customLimits
        limit_id = None
        for limit in customs:
            if limit.name == defaults[0].name:
                self.assertTrue(limit.value == defaults[0].value + 10)
                limit_id = limit.id
                break
        self.assertTrue(limit_id is not None)
        r = self.mgmt_client.update_absolute_limit(account_id=self.tenant_id,
                                                   value=defaults[0].value+20,
                                                   limit_id=limit_id)
        self.assertEquals(r.status_code, 202)
        r = self.mgmt_client.get_absolute_limits(self.tenant_id)
        self.assertEquals(r.status_code, 200)
        customs = r.entity.customLimits
        for limit in customs:
            if limit.id == limit_id:
                self.assertTrue(limit.value == defaults[0].value + 20)
                break
        r = self.mgmt_client.delete_absolute_limit(account_id=self.tenant_id,
                                                   limit_id=limit_id)
        self.assertEquals(r.status_code, 202)
        r = self.mgmt_client.get_absolute_limits(self.tenant_id)
        self.assertEquals(r.status_code, 200)
        customs = r.entity.customLimits
        for limit in customs:
            if limit.name == defaults[0].name:
                limit_id = None
                break
        self.assertTrue(limit_id is not None)
