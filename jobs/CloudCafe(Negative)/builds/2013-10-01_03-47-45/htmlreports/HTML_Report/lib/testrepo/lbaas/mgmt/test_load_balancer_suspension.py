from testrepo.common.testfixtures.load_balancers \
    import BaseLoadBalancersFixture
from ccengine.common.decorators import attr
from ccengine.domain.types import LoadBalancerStatusTypes as LBStatus
from ccengine.domain.lbaas.mgmt.ticket import Ticket


class SuspensionTests(BaseLoadBalancersFixture):

    @classmethod
    def setUpClass(cls):
        super(SuspensionTests, cls).setUpClass()
        cls.lb = cls.lbaas_provider.create_active_load_balancer().entity
        cls.lbs_to_delete.append(cls.lb.id)

    @attr('positive')
    def test_suspension_on_load_balancer(self):
        '''Test suspension on a load balancer'''
        r = self.mgmt_client.suspend_load_balancer(load_balancer_id=self.lb.id,
                                                   reason="testing purposes",
                                                   user="supportDudeA",
                                                   ticket=Ticket(
                                                   comment="Test ticket for"
                                                           "adding a vip.",
                                                   ticketId=12345)
                                                   ._auto_to_dict().get(
                                                   Ticket.ROOT_TAG))
        self.assertEquals(r.status_code, 202)
        self.lbaas_provider.wait_for_status(self.lb.id, LBStatus.SUSPENDED)
        r = self.mgmt_client.get_load_balancer_suspension(self.lb.id)
        self.assertEquals(r.status_code, 200)
        self.assertTrue(r.entity.id is not None)
        self.assertTrue(r.entity.reason is not None)
        r = self.mgmt_client.unsuspend_load_balancer(self.lb.id)
        self.assertEquals(r.status_code, 202)
        self.lbaas_provider.wait_for_status(self.lb.id, LBStatus.ACTIVE)
        r = self.mgmt_client.get_load_balancer_suspension(self.lb.id)
        self.assertEquals(r.status_code, 200)
        self.assertTrue(r.entity.id is None)
