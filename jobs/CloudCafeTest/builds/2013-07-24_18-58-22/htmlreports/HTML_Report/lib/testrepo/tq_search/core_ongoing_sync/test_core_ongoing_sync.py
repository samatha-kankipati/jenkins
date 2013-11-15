from testrepo.common.testfixtures.tq_search import TQSearchFixture
from ccengine.common.decorators import attr
import time
import datetime
from datetime import timedelta
from ccengine.common.tools.datatools import string_to_datetime, \
    convert_date_from_cst_to_utc_date
from ccengine.domain.tq_search.response.tq_search import TicketDetails
from ccengine.domain.core.request.core_request import Where, WhereSet, \
    WhereCondition, WhereOperators, WhereEquals, WhereGreaterOrEquals, \
    WhereLessOrEquals, LoadArgs, CoreQuery, WhereIn, WhereNotEquals, \
    WhereNotIn, WhereLess, WhereGreater


class TestCoreOngoingSync(TQSearchFixture):

    @classmethod
    def setUpClass(cls):
        super(TestCoreOngoingSync, cls).setUpClass()
        cls.result_map = {
            "number": "number", "subject": "subject",
            "last_public_response_date": "last_public_response_date",
            "created": "created", "priority": "priority.id",
            "status.name": "status.name", "modified": "modified",
            "category.name": "category.name", "queue.name": "queue.name",
            "account.number": "account.number",
            "assignee.name": "assignee.name"}
        cls.queue_id = 11
        cls.sub_category = 11206
        cls.account_id = 11
        cls.ticket_text = "Ticket Text Message"
        cls.ticket_list = []
        cls.ticket_subject = "Generic core ticket"
        cls.ticket_subject2 = "Generic core ticket two"
        cls.source = 1
        cls.severity = 1
        cls.created_ticket_in_core = cls.core_provider.ticket_client.\
            create_generic_ticket(account=cls.account_id, queue=cls.queue_id,
                                  subcategory=cls.sub_category,
                                  source=cls.source,
                                  severity=cls.severity,
                                  subject=cls.ticket_subject,
                                  text=cls.ticket_text,
                                  result_map=cls.result_map).entity
        cls.created_ticket_in_core_three = cls.core_provider.ticket_client.\
            create_generic_ticket(account=cls.account_id, queue=cls.queue_id,
                                  subcategory=cls.sub_category,
                                  source=cls.source,
                                  severity=cls.severity,
                                  subject=cls.ticket_subject2,
                                  text=cls.ticket_text,
                                  result_map=cls.result_map).entity
        # This sleep time is required so that the ticket created/updated
        # in core is reflected in tq_search in almost 1 minute
        time.sleep(100)

    @classmethod
    def tearDownClass(cls):
        super(TestCoreOngoingSync, cls).tearDownClass()
        cls.core_provider.ticket_client.\
            set_status_by_name(
                ticket_number=cls.created_ticket_in_core.number,
                status_name="Closed")
        cls.core_provider.ticket_client.\
            set_status_by_name(
                ticket_number=cls.created_ticket_in_core_three.number,
                status_name="Closed")

    @attr(type='positive', module='read', suite='smoke')
    def test_ticket_created_in_core_reflects_in_one_minute_in_tqsearch(self):
        """
        @summary:test that when a ticket is created in core the \
        same is reflected in a minute in tq_search
        """
        results = \
            self.gate_provider.search_client.search_ticket_in_core(
                number=self.created_ticket_in_core.number).entity
        self.assertTrue(len(results.tickets) == 1,
                        "The ticket{%s} is not present in tq_search")

    @attr(type='positive', module='read', suite='smoke')
    def test_ticket_updated_in_core_reflects_in_one_minute_in_tqsearch(self):
        """
        @summary:test that when a ticket is updated in core\
        i.e. all the fields are updated in core the \
        same is reflected in a minute in tq_search
        """
        new_status = "In Progress"
        new_queue = "13"
        new_priority = "3"
        new_subject = "New subject"
        assignee_userid = "matt.printz"
        assignee_name = "Matthew Printz "
        assigneeContactCondition = WhereEquals("employee_userid",
                                               assignee_userid)
        assigneeContact = self.core_provider.contact_client.\
            build_contact_object(assigneeContactCondition)
        new_account_number = 11
        new_source_system = 5
        search_ticket = self.gate_provider.search_client.\
            search_ticket_in_core(number=self.created_ticket_in_core.number)\
            .entity
        # Getting the modofied date of a created ticket in core
        initial_date = string_to_datetime(search_ticket.tickets[0].updatedAt)
        self.core_provider.ticket_client.\
            set_status_by_name(ticket_number=self.
                               created_ticket_in_core.number,
                               status_name=new_status)
        self.core_provider.\
            ticket_client.update_ticket(self.created_ticket_in_core.number,
                                        "queue", {"class": "Ticket.Queue",
                                        "load_arg": new_queue}).entity[0]
        self.core_provider.\
            ticket_client.update_ticket(self.created_ticket_in_core.number,
                                        "priority",
                                        {"class": "Ticket.Priority",
                                        "load_arg": new_priority}).entity[0]
        self.core_provider.\
            ticket_client.update_ticket(self.created_ticket_in_core.number,
                                        "subject", new_subject).entity[0]
        self.core_provider.\
            ticket_client.update_ticket(self.created_ticket_in_core.number,
                                        "assignee", assigneeContact)
        cust_condition = WhereEquals("number", self.created_ticket_in_core.
                                     number)

        ticket_list_from_core = \
            self.core_provider.ticket_client.list_tickets_by_ticket_attributes(
                cust_condition, attributes=self.core_attributes).entity

        # This sleep time is required so that the ticket created/updated
        # in core is reflected in tq_search in almost 1 minute

        time.sleep(60)
        search_result = self.gate_provider.search_client.\
            search_ticket_in_core(number=self.created_ticket_in_core
                                  .number).entity
        self.assertTrue(string_to_datetime(search_result.tickets[0]
                        .updatedAt) > initial_date,
                        "Failed updated ticket in core does not\
                        match tq_search ticket expected:\
                        {0} actual {1}".format(search_result.tickets[0]
                                               .updatedAt, initial_date))

    @attr(type='positive', module='read', suite='smoke')
    def test_updating_status_in_core_marks_ticket_as_updated_in_search(self):
        """
        @summary:test when status field is updated in core \
        the updated_at field of the ticket updates the time
        """
        new_status = "In Progress"
        search_ticket = self.gate_provider.search_client.\
            search_ticket_in_core(
                number=self.created_ticket_in_core_three.number).entity
        # Getting the modofied date of a created ticket in core
        initial_date = string_to_datetime(search_ticket.tickets[0].updatedAt)
        # Changing the status of a ticket in core
        self.core_provider.ticket_client.\
            set_status_by_name(ticket_number=self.
                               created_ticket_in_core_three.number,
                               status_name=new_status)
        # This sleep time is required so that the ticket created/updated
        # in core is reflected in tq_search in almost 1 minute
        time.sleep(60)
        new_search_ticket = self.gate_provider.search_client.\
            search_ticket_in_core(
                number=self.created_ticket_in_core_three.number).entity
        # Asserting that the updated time of the ticket after the status
        # update is greater than the initial updated date
        self.assertTrue(string_to_datetime
                        (new_search_ticket.tickets[0].updatedAt) >
                        initial_date, "Failed Expected date:{%s}\
                        Actual date:{%s}" %
                        (initial_date,
                        string_to_datetime((new_search_ticket.
                                            tickets[0]).updatedAt)))

    @attr(type='positive', module='read', suite='smoke')
    def test_updating_priority_in_core_marks_ticket_as_updated_in_search(self):
        """
        @summary:test when priority field is updated in core \
        the updated_at fileld of the ticket updates the time
        """
        priority = 2
        search_ticket = self.gate_provider.search_client.\
            search_ticket_in_core(
                number=self.created_ticket_in_core_three.number).entity
        # Getting the modofied date of a created ticket in core
        initial_date = string_to_datetime(search_ticket.tickets[0].updatedAt)

        # Changing the priority of a ticket in core
        self.core_provider.ticket_client.\
            update_ticket(self.created_ticket_in_core_three.number,
                          "priority", {"class": "Ticket.Priority",
                          "load_arg": priority}).entity[0]
        # This sleep time is required so that the ticket created/updated
        # in core is reflected in tq_search in almost 1 minute
        time.sleep(60)
        new_search_ticket = self.gate_provider.search_client.\
            search_ticket_in_core(number=self.created_ticket_in_core_three
                                  .number).entity

        # Asserting that the updated time of the ticket after the status
        # update is greater than the initial updated date
        self.assertTrue(string_to_datetime
                        (new_search_ticket.tickets[0].updatedAt) >
                        initial_date, "Failed Expected date:{%s}\
                        Actual date:{%s}" %
                        (initial_date,
                        string_to_datetime(new_search_ticket.
                                           tickets[0].updatedAt)))

    @attr(type='positive', module='read', suite='smoke')
    def test_updating_queue_in_core_marks_ticket_as_updated_in_tq_search(self):
        """
        @summary:test when queue field is updated in core \
        the updated_at fileld of the ticket updates the time
        """
        queue = 2
        search_ticket = self.gate_provider.search_client.\
            search_ticket_in_core(
                number=self.created_ticket_in_core_three.number).entity
        # Getting the modofied date of a created ticket in core
        initial_date = string_to_datetime(search_ticket.tickets[0].updatedAt)

        # Changing the status of a ticket in core
        self.core_provider.ticket_client.\
            update_ticket(self.created_ticket_in_core_three.number,
                          "queue", {"class": "Ticket.Queue",
                          "load_arg": queue}).entity[0]
        # This sleep time is required so that the ticket created/updatedAt
        # in core is reflected in tq_search in almost 1 minute
        time.sleep(60)
        new_search_ticket = self.gate_provider.\
            search_client.search_ticket_in_core(
                number=self.created_ticket_in_core_three.number
            ).entity

        # Asserting that the updated time of the ticket after the status
        # update is greater than the initial updated date
        self.assertTrue(string_to_datetime
                        (new_search_ticket.tickets[0].updatedAt) >
                        initial_date, "Failed Expected date:{%s}\
                        Actual date:{%s}" %
                        (initial_date,
                         string_to_datetime(new_search_ticket.
                                            tickets[0].updatedAt)))
