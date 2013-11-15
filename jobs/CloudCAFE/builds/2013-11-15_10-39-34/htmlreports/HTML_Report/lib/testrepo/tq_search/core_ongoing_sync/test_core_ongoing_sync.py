import datetime
from datetime import timedelta
import time

from ccengine.common.decorators import attr
from ccengine.common.tools.datatools import string_to_datetime, \
    convert_date_from_cst_to_utc_date
from ccengine.domain.core.request.core_request import Where, WhereSet, \
    WhereCondition, WhereOperators, WhereEquals, WhereGreaterOrEquals, \
    WhereLessOrEquals, LoadArgs, CoreQuery, WhereIn, WhereNotEquals, \
    WhereNotIn, WhereLess, WhereGreater
from ccengine.domain.tq_search.response.tq_search import TicketDetails
from testrepo.common.testfixtures.tq_search import TQSearchFixture


class TestCoreOngoingSync(TQSearchFixture):

    @classmethod
    def setUpClass(cls):
        super(TestCoreOngoingSync, cls).setUpClass()
        cls.created_ticket_in_core = cls.core_provider.ticket_client.\
            create_generic_ticket(account=cls.sync_account_id,
                                  queue=cls.sync_queue_id,
                                  subcategory=cls.sync_sub_category,
                                  source=cls.sync_source,
                                  severity=cls.sync_severity,
                                  subject=cls.sync_ticket_subject,
                                  text=cls.sync_ticket_text,
                                  result_map=cls.result_map).entity
        cls.created_ticket_in_core_two = cls.core_provider.ticket_client.\
            create_generic_ticket(account=cls.account_number_1,
                                  queue=cls.sync_queue_id,
                                  subcategory=cls.sync_sub_category,
                                  source=cls.sync_source,
                                  severity=cls.sync_severity,
                                  subject=cls.sync_ticket_subject,
                                  text=cls.sync_ticket_text,
                                  result_map=cls.result_map).entity
        cls.created_ticket_in_core_three = cls.core_provider.ticket_client.\
            create_generic_ticket(account=cls.sync_account_id,
                                  queue=cls.sync_queue_id,
                                  subcategory=cls.sync_sub_category,
                                  source=cls.sync_source,
                                  severity=cls.sync_severity,
                                  subject=cls.sync_ticket_subject2,
                                  text=cls.sync_ticket_text,
                                  result_map=cls.result_map).entity
        # This sleep time is required so that the ticket created/updated
        # in core is reflected in tq_search in almost 1 minute
        time.sleep(float(cls.sleep_100_sec))

    @classmethod
    def tearDownClass(cls):
        super(TestCoreOngoingSync, cls).tearDownClass()
        cls.core_provider.ticket_client.\
            set_status_by_name(
                ticket_number=cls.created_ticket_in_core.number,
                status_name="Closed")
        cls.core_provider.ticket_client.\
            set_status_by_name(
                ticket_number=cls.created_ticket_in_core_two.number,
                status_name="Closed")
        cls.core_provider.ticket_client.\
            set_status_by_name(
                ticket_number=cls.created_ticket_in_core_three.number,
                status_name="Closed")

    @attr(type='positive', module='read', suite='smoke')
    def test_ticket_created_in_core_reflects_in_one_minute_in_tqsearch(self):
        """
        @summary:test that when a ticket is created in core the
        same is reflected in a minute in tq_search
        """
        results = \
            self.gate_provider.search_client.search_ticket_in_core(
                number=self.created_ticket_in_core.number).entity
        self.assertTrue(len(results.tickets) == 1,
                        "The ticket{0} is not present in tq_search".format(
                            self.created_ticket_in_core.number))

    @attr(type='positive', module='read', suite='smoke')
    def test_ticket_updated_in_core_reflects_in_one_minute_in_tqsearch(self):
        """
        @summary:test that when a ticket is updated in core
        i.e. all the fields are updated in core the
        same is reflected in a minute in tq_search
        """
        assignee_contact_condition = WhereEquals("employee_userid",
                                                 self.assignee_user_id)
        assignee_contact = self.core_provider.contact_client.\
            build_contact_object(assignee_contact_condition)
        search_ticket = self.gate_provider.search_client.\
            search_ticket_in_core(
                number=self.created_ticket_in_core.number).entity
        # Getting the modofied date of a created ticket in core
        initial_date = string_to_datetime(search_ticket.tickets[0].updated_at)
        self.core_provider.ticket_client.set_status_by_name(
            ticket_number=self.created_ticket_in_core.number,
            status_name=self.status_3)
        self.core_provider.\
            ticket_client.update_ticket(self.created_ticket_in_core.number,
                                        "queue", {"class": "Ticket.Queue",
                                        "load_arg": self.queue_id}).entity[0]
        self.core_provider.\
            ticket_client.update_ticket(self.created_ticket_in_core.number,
                                        "priority",
                                        {"class": "Ticket.Priority",
                                        "load_arg": self.priority_3}).entity[0]
        self.core_provider.\
            ticket_client.update_ticket(self.created_ticket_in_core.number,
                                        "subject", self.subject_1).entity[0]
        self.core_provider.\
            ticket_client.update_ticket(self.created_ticket_in_core.number,
                                        "assignee", assignee_contact)
        cust_condition = WhereEquals(
            "number", self.created_ticket_in_core.number)

        ticket_list_from_core = \
            self.core_provider.ticket_client.list_tickets_by_ticket_attributes(
                cust_condition, attributes=self.core_attributes).entity

        # This sleep time is required so that the ticket created/updated
        # in core is reflected in tq_search in almost 1 minute

        time.sleep(float(self.sleep_30_sec))
        search_result = self.gate_provider.search_client.\
            search_ticket_in_core(number=self.created_ticket_in_core
                                  .number).entity
        self.assertGreater(
            string_to_datetime(search_result.tickets[0].updated_at),
            initial_date, "Failed updated ticket expected:{0} actual {1}"
            .format(search_result.tickets[0].updated_at, initial_date))

    @attr(type='positive', module='read', suite='smoke')
    def test_updating_status_in_core_marks_ticket_as_updated_in_search(self):
        """
        @summary:test when status field is updated in core
        the updated_at field of the ticket updates the time
        """
        search_ticket = self.gate_provider.search_client.\
            search_ticket_in_core(
                number=self.created_ticket_in_core_three.number).entity
        # Getting the modofied date of a created ticket in core
        initial_date = string_to_datetime(search_ticket.tickets[0].updated_at)
        # Changing the status of a ticket in core
        self.core_provider.ticket_client.\
            set_status_by_name(ticket_number=self.
                               created_ticket_in_core_three.number,
                               status_name=self.status_3)
        # This sleep time is required so that the ticket created/updated
        # in core is reflected in tq_search in almost 1 minute
        time.sleep(float(self.sleep_30_sec))
        new_search_ticket = self.gate_provider.search_client.\
            search_ticket_in_core(
                number=self.created_ticket_in_core_three.number).entity
        # Asserting that the updated time of the ticket after the status
        # update is greater than the initial updated date
        self.assertGreater(
            string_to_datetime(new_search_ticket.tickets[0].updated_at),
            initial_date, "Failed Expected date:{0} Actual date:{1}".format
            (initial_date, string_to_datetime((new_search_ticket.
                                              tickets[0]).updated_at)))

    @attr(type='positive', module='read', suite='smoke')
    def test_updating_priority_in_core_marks_ticket_as_updated_in_search(self):
        """
        @summary:test when priority field is updated in core
        the updated_at fileld of the ticket updates the time
        """
        search_ticket = self.gate_provider.search_client.search_ticket_in_core(
            number=self.created_ticket_in_core_three.number).entity
        # Getting the modofied date of a created ticket in core
        initial_date = string_to_datetime(search_ticket.tickets[0].updated_at)

        # Changing the priority of a ticket in core
        self.core_provider.ticket_client.\
            update_ticket(self.created_ticket_in_core_three.number,
                          "priority", {"class": "Ticket.Priority",
                          "load_arg": self.priority_2}).entity[0]
        # This sleep time is required so that the ticket created/updated
        # in core is reflected in tq_search in almost 1 minute
        time.sleep(float(self.sleep_30_sec))
        new_search_ticket = self.gate_provider.search_client.\
            search_ticket_in_core(number=self.created_ticket_in_core_three
                                  .number).entity

        # Asserting that the updated time of the ticket after the status
        # update is greater than the initial updated date
        self.assertGreater(
            string_to_datetime(new_search_ticket.tickets[0].updated_at),
            initial_date, "Failed Expected date:{0}Actual date:{1}".format
            (initial_date, string_to_datetime(new_search_ticket.
                                              tickets[0].updated_at)))

    @attr(type='positive', module='read', suite='smoke')
    def test_updating_queue_in_core_marks_ticket_as_updated_in_tq_search(self):
        """
        @summary:test when queue field is updated in core
        the updated_at fileld of the ticket updates the time
        """
        search_ticket = self.gate_provider.search_client.\
            search_ticket_in_core(
                number=self.created_ticket_in_core_three.number).entity
        # Getting the modofied date of a created ticket in core
        initial_date = string_to_datetime(search_ticket.tickets[0].updated_at)

        # Changing the status of a ticket in core
        self.core_provider.ticket_client.update_ticket(
            self.created_ticket_in_core_three.number, "queue",
            {"class": "Ticket.Queue", "load_arg": self.queue_id_ref}
        ).entity[0]
        # This sleep time is required so that the ticket created/updatedAt
        # in core is reflected in tq_search in almost 1 minute
        time.sleep(float(self.sleep_30_sec))
        new_search_ticket = self.gate_provider.\
            search_client.search_ticket_in_core(
                number=self.created_ticket_in_core_three.number
            ).entity

        # Asserting that the updated time of the ticket after the status
        # update is greater than the initial updated date
        self.assertGreater(
            string_to_datetime(new_search_ticket.tickets[0].updated_at),
            initial_date, "Failed Expected date:{0}Actual date:{1}".format
            (initial_date, string_to_datetime(new_search_ticket.
                                              tickets[0].updated_at)))

    @attr(type='positive', module='read', suite='smoke')
    def test_contacts_roles_in_the_ticket(self):
        """
        @summary:test contacts and roles values in a ticket
        """
        search_ticket = self.gate_provider.search_client.\
            search_ticket_in_core(
                number=self.created_ticket_in_core_two.number).entity
        # Getting the contact and role info for created ticket in core
        if search_ticket.tickets[0] is not None:
            self.assertEqual(
                search_ticket.tickets[0].account.contact_names,
                self.core_contact_names_list)
            self.assertEqual(
                search_ticket.tickets[0].account.contact_sso,
                self.core_contact_sso_list)
            self.assertEqual(
                search_ticket.tickets[0].account.contact_roles,
                self.core_contact_roles_list)
