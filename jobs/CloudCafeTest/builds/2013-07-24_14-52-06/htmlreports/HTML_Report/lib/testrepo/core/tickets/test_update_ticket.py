from testrepo.common.testfixtures.core import CoreFixture
from ccengine.common.decorators import attr
from ccengine.domain.core.request.core_request import WhereEquals


class TestUpdateTicket(CoreFixture):

    @classmethod
    def setUpClass(cls):
        super(TestUpdateTicket, cls).setUpClass()
        subject = "Ticket For Testing Ticket Updation"
        text = "Initial Message for Ticket Updation Tests Ticket"
        cls.ticket = cls.ticket_client. \
                 create_customer_ticket(queue=16,
                                        subcategory=2940,
                                        source=2,
                                        severity=3,
                                        subject=subject,
                                        text=text,
                                        account=11,
                                        result_map={"number": "number"}).entity

    @classmethod
    def tearDownClass(cls):
        super(TestUpdateTicket, cls).tearDownClass()
        cls.ticket_client.close_ticket(cls.ticket)

    @attr(type='smoke')
    def test_update_ticket_assignee(self):
        '''
        Test : Verify that user can update the assignee for a ticket
        '''
        ticket = self.ticket.number
        assignee_userid = "matt.printz"
        assignee_name = "Matthew Printz"
        assigneeContactCondition = WhereEquals("employee_userid",
                                               assignee_userid)
        assigneeContact = self.contact_client.\
                          build_contact_object(assigneeContactCondition)
        ticketAfterUpdate = self.ticket_client.update_ticket(ticket,
                                                             "assignee",
                                                             assigneeContact
                                                             ).entity[0]
        assigneeSuccess = ticketAfterUpdate.assignee
        self.assertEqual(assigneeSuccess, "success",
                         "Expected value {0}, Actual value {1}".
                         format("success", assigneeSuccess))
        attributes = {"assignee": "assignee.name"}
        result = self.ticket_client.get_ticket_details(ticket,
                                                       attributes).entity[0]
        actual_assignee = result.assignee
        self.assertEquals(actual_assignee, assignee_name)

    @attr(type='smoke')
    def test_add_computer_to_ticket(self):
        '''
        Test: Verify that user can Add computer to a ticket
        '''
        computer_id = "477574"
        ticket = self.ticket.number
        response = self.ticket_client.add_computer(ticket_number=ticket,
                                                   computer=computer_id
                                                   )
        self.assertEquals(response.status_code, 200)
        '''Get Ticket Details'''
        attributes = ["computers"]
        result = self.ticket_client.get_ticket_details(ticket,
                                                       attributes).entity[0]
        computers = result.computers
        actual_computers = [computer['load_value'] for computer in computers]
        self.assertTrue(int(computer_id) in actual_computers)

    @attr(type='smoke')
    def test_add_message_to_ticket(self):
        '''
        Test: Verify that user can Add Message to ticket
        '''
        message_text = "This is a test message"
        message_source = 1
        ticket = self.ticket.number
        response = self.ticket_client.add_message(ticket_number=ticket,
                                                  text=message_text,
                                                  source=message_source
                                                  )
        self.assertEqual(200, response.status_code, "Response code is not 200")

    @attr(type='smoke')
    def test_remove_computer_from_ticket(self):
        '''
        Test: Verify that user can Remove Computer from ticket
        '''
        computer_id = "477595"
        ticket = self.ticket.number
        self.ticket_client.add_computer(ticket_number=ticket,
                                        computer=computer_id)
        response = self.ticket_client.remove_computer(ticket_number=ticket,
                                                      computer=computer_id
                                                      )
        self.assertEquals(response.status_code, 200)
        attributes = ["computers"]
        result = self.ticket_client.get_ticket_details(ticket,
                                                       attributes).entity[0]
        computers = result.computers
        actual_computers = [computer['load_value'] for computer in computers]
        self.assertFalse(int(computer_id) in actual_computers)

    @attr(type='smoke')
    def test_update_status_by_name(self):
        '''
        Test: verify that user can update status by name
        '''
        status = "Pending Customer Response"
        ticket = self.ticket.number
        response = self.ticket_client.set_status_by_name(ticket_number=ticket,
                                                         status_name=status)
        self.assertEquals(response.status_code, 200)
        attributes = ["status"]
        result = self.ticket_client.get_ticket_details(ticket,
                                                       attributes).entity[0]
        actual_status = result.status
        self.assertEquals(actual_status.get('name'), status)

    @attr(type='smoke')
    def test_add_work_to_ticket(self):
        '''
        Test: Add work to ticket
        '''
        worktype_id = 1
        description = "Testing add Work to Ticket"
        duration = 10
        unit_count = 3
        fee_waived = 1
        ticket = self.ticket.number
        response = self.ticket_client.add_work(ticket, worktype_id,
                                               description, duration,
                                               unit_count, fee_waived
                                               )
        self.assertEquals(response.status_code, 200)
        attributes = {"description": "work_log.description"}
        result = self.ticket_client.get_ticket_details(ticket,
                                                       attributes).entity[0]
        self.assertTrue(description in result.description)
