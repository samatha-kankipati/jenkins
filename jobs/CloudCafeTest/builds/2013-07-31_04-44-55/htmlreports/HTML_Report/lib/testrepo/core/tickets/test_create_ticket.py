from testrepo.common.testfixtures.core import CoreFixture
from ccengine.common.decorators import attr


class TestCreateTicket(CoreFixture):

    @classmethod
    def setUpClass(cls):
        super(TestCreateTicket, cls).setUpClass()
        cls.result_map = {"number": "number", "subject": "subject",
                  "source": "source.id", "severity": "severity.id",
                  "priority": "priority.id"}
        cls.queue_id = 1
        cls.sub_category = 11206
        cls.account_id = 11
        cls.ticket_text = "Ticket Text Message"

    @classmethod
    def tearDownClass(cls):
        super(TestCreateTicket, cls).tearDownClass()

    @attr(type='smoke')
    def test_create_internal_ticket(self):
        '''
        Verify creation of internal ticket using Ticket.Queue class's
        addInternalTicket's mandatory parameters
        '''
        ticket_subject = "Internal Ticket for Test"
        source = 3
        severity = 1
        ticket = self.ticket_client.\
                 create_internal_ticket(queue=self.queue_id,
                                        subcategory=self.sub_category,
                                        source=source, severity=severity,
                                        subject=ticket_subject,
                                        text=self.ticket_text,
                                        result_map=self.result_map).entity
        self.assertTrue(ticket.number is not None, "Ticket is not created")
        self.assertEquals(ticket.subject, ticket_subject,
                          "Ticket Subject {0} did not match :{1}"
                          .format(ticket_subject, ticket.subject))
        self.assertEquals(ticket.source, source,
                          "Ticket Source {0} did not match:{1}"
                          .format(source, ticket.source))
        self.assertEquals(ticket.severity, severity,
                          "Ticket Severity {0} did not match :{1}"
                          .format(severity, ticket.severity))
        self.resources.add(ticket, self.ticket_client.close_ticket)

    @attr(type='smoke')
    def test_create_generic_ticket(self):
        '''
        Verify creation of generic ticket using Account.Account class's
        addTicket's mandatory parameters
        '''
        ticket_subject = "Generic Ticket for Test"
        source = 2
        severity = 2
        ticket = self.ticket_client.\
                 create_generic_ticket(account=self.account_id,
                                       queue=self.queue_id,
                                       subcategory=self.sub_category,
                                       source=source,
                                       severity=severity,
                                       subject=ticket_subject,
                                       text=self.ticket_text,
                                       result_map=self.result_map).entity
        self.assertTrue(ticket.number is not None, "Ticket is not created")
        self.assertEquals(ticket.subject, ticket_subject,
                          "Ticket Subject {0} did not match :{1}"
                          .format(ticket_subject, ticket.subject))
        self.assertEquals(ticket.source, source,
                          "Ticket Source {0} did not match:{1}"
                          .format(source, ticket.source))
        self.assertEquals(ticket.severity, severity,
                          "Ticket Severity {0} did not match :{1}"
                          .format(severity, ticket.severity))
        self.resources.add(ticket, self.ticket_client.close_ticket)

    @attr(type='smoke')
    def test_create_customer_ticket(self):
        '''
        Verify creation of customer ticket using Ticket.Queue class's
        addCustomerTicket's mandatory parameters '''

        ticket_subject = "Customer Ticket for Test"
        source = 3
        severity = 3
        ticket = self.ticket_client. \
                 create_customer_ticket(queue=self.queue_id,
                                        subcategory=self.sub_category,
                                        source=source,
                                        severity=severity,
                                        subject=ticket_subject,
                                        text=self.ticket_text,
                                        account=self.account_id,
                                        result_map=self.result_map).entity
        self.assertTrue(ticket.number is not None, "Ticket is not created")
        self.assertEquals(ticket.subject, ticket_subject,
                          "Ticket Subject {0} did not match : {1}"
                          .format(ticket_subject, ticket.subject))
        self.assertEquals(ticket.source, source,
                          "Ticket Source {0} did not match: {1}"
                          .format(source, ticket.source))
        self.assertEquals(ticket.severity, severity,
                          "Ticket Severity {0} did not match : {1}"
                          .format(severity, ticket.severity))
        self.resources.add(ticket, self.ticket_client.close_ticket)

    @attr(type='smoke')
    def test_create_sub_ticket(self):
        ''' Verify a user can create a sub ticket using ticket.ticket class's
            addSubTicket method with the mandatory parameters
            (sub_ticket_subject,ticket_comments)
        '''

        sub_ticket_subject = "sub ticket for ticket"
        ticket_subject = "parent ticket subject"
        sub_ticket_comment = "sub ticket comment"
        source = 1
        severity = 1
        result_map = {"number": "number", "subject": "subject"}
        ticket = self.ticket_client.\
                 create_internal_ticket(queue=self.queue_id,
                                        subcategory=self.sub_category,
                                        source=source, severity=severity,
                                        subject=ticket_subject,
                                        text=self.ticket_text,
                                        result_map=self.result_map).entity
        sub_ticket = self.ticket_client.\
                     create_sub_ticket(ticket_number=ticket.number,
                                       subject=sub_ticket_subject,
                                       comment=sub_ticket_comment,
                                       result_map=result_map).entity
        self.assertTrue(sub_ticket.number is not None, "Subticket failed")
        self.assertEqual(sub_ticket.subject, sub_ticket_subject,
                        "Sub Ticket subject {0} does not match expected {1}"
                         .format(sub_ticket.subject, sub_ticket_subject))
        self.resources.add(sub_ticket, self.ticket_client.close_ticket)
        self.resources.add(ticket, self.ticket_client.close_ticket)
