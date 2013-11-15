from testrepo.common.testfixtures.load_balancers\
    import BaseLoadBalancersFixture
from ccengine.common.decorators import attr
from ccengine.domain.lbaas.mgmt.ticket import Ticket


class TicketTests(BaseLoadBalancersFixture):

    @classmethod
    def setUpClass(cls):
        super(TicketTests, cls).setUpClass()
        cls.lb = cls.lbaas_provider.create_active_load_balancer().entity
        cls.lbs_to_delete.append(cls.lb.id)

    @attr('positive')
    def test_functional_tickets_operations(self):
        '''Testing ticket calls'''
        comment = 'This is the most awesome of tickets.'
        ticketId = 12321
        r = self.mgmt_client.add_ticket(self.lb.id, comment=comment,
                                        ticketId=ticketId)
        self.assertEquals(r.status_code, 200)
        self.assertTrue(r.entity.comment == comment)
        r2 = self.mgmt_client.get_tickets(self.lb.id)
        self.assertEquals(r2.status_code, 200)
        self.assertEqual(r.entity.ticketId, r2.entity[0].ticketId)
