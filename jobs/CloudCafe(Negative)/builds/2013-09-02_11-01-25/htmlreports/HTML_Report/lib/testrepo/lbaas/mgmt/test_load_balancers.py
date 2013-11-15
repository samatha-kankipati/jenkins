from testrepo.common.testfixtures.load_balancers\
    import BaseLoadBalancersFixture
from ccengine.common.decorators import attr


class LoadBalancerTests(BaseLoadBalancersFixture):

    @classmethod
    def setUpClass(cls):
        super(LoadBalancerTests, cls).setUpClass()
        cls.lb = cls.lbaas_provider.create_active_load_balancer().entity
        cls.lbs_to_delete.append(cls.lb.id)

    @attr('positive')
    def test_functional_load_balancer_operations(self):
        '''Testing load balancer calls'''
        r = self.mgmt_client.get_load_balancers_with_vip(
            self.lb.virtualIps[0].id)
        self.assertEquals(r.status_code, 200)
        self.assertTrue(r.entity[0].id == self.lb.id)
        self.assertTrue(r.entity[0].virtualIps[0].id
                        == self.lb.virtualIps[0].id)

    @attr('positive')
    def test_extended_view_load_balancer(self):
        '''Testing extended view load balancer call'''
        r = self.mgmt_client.get_extended_view_load_balancer(self.lb.id)
        self.assertEquals(r.status_code, 200)
        self.assertEquals(r.entity.id, self.lb.id)
        self.assertEquals(r.entity.virtualIps[0].id, self.lb.virtualIps[0].id)
        r = self.mgmt_client.get_extended_load_balancers_on_account(
            self.tenant_id)
        self.assertEquals(r.status_code, 200)
        self.assertTrue(r.entity[0].loadBalancerId is not None)

    @attr('positive')
    def test_load_balancer_status_management(self):
        '''Test the status change urls for a load balancer'''
        r = self.mgmt_client.update_load_balancer_status_pending_update(
            self.lb.id)
        self.assertEquals(r.status_code, 200)
        r = self.client.get_load_balancer(self.lb.id)
        self.assertEquals(r.status_code, 200)
        self.assertTrue(r.entity.status == "PENDING_UPDATE")
        r = self.mgmt_client.update_load_balancer_status_pending_delete(
            self.lb.id)
        self.assertEquals(r.status_code, 200)
        r = self.client.get_load_balancer(self.lb.id)
        self.assertEquals(r.status_code, 200)
        self.assertTrue(r.entity.status == "PENDING_DELETE")
        r = self.mgmt_client.update_load_balancer_status_build(
            self.lb.id)
        self.assertEquals(r.status_code, 200)
        r = self.client.get_load_balancer(self.lb.id)
        self.assertEquals(r.status_code, 200)
        self.assertTrue(r.entity.status == "BUILD")
        r = self.mgmt_client.update_load_balancer_status_deleted(self.lb.id)
        self.assertEquals(r.status_code, 200)
        r = self.client.get_load_balancer(self.lb.id)
        self.assertEquals(r.status_code, 200)
        self.assertTrue(r.entity.status == "DELETED")
        r = self.mgmt_client.update_load_balancer_status_error(self.lb.id)
        self.assertEquals(r.status_code, 200)
        r = self.client.get_load_balancer(self.lb.id)
        self.assertEquals(r.status_code, 200)
        self.assertTrue(r.entity.status == "ERROR")
        r = self.mgmt_client.update_load_balancer_status_active(self.lb.id)
        self.assertEquals(r.status_code, 200)
        r = self.client.get_load_balancer(self.lb.id)
        self.assertEquals(r.status_code, 200)
        self.assertTrue(r.entity.status == "ACTIVE")

    @attr('positive')
    def test_load_balancer_status_history(self):
        r = self.mgmt_client.get_load_balancer_state_history(self.tenant_id)
        self.assertEquals(r.status_code, 200)
        self.assertTrue(len(r.entity) > 0)
