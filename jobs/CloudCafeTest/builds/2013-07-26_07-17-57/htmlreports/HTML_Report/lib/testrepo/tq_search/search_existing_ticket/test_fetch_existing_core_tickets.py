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
    WhereLessOrEquals, LoadArgs, CoreQuery


class TestFetchExistingCoreTickets(TQSearchFixture):

    def tearDown(cls):
        '''
        @summary: This sleep is there as there as the core user that we use
        for testing has rate limitaion on it and in case where there are
        more than 10 requests in 10 seconds time outs show up, so as a
        temporary fix we need sleep over here
        '''
        super(TestFetchExistingCoreTickets, cls).tearDownClass()
        time.sleep(3)

    @attr(type='positive', module='read', suite='smoke')
    def test_load_existing_tickets_to_ticket_search(self):
        '''
        @summary:B-42997: Load existing tickets to ticket search
        '''
        cust_condition = WhereEquals("status_name", self.status_1).AND(
            WhereGreaterOrEquals("created", self.start_time)).AND(
                WhereLessOrEquals("created", self.end_time))

        ticket_list_from_core = \
            self.core_provider.ticket_client.list_tickets_by_ticket_attributes(
                cust_condition, attributes=self.core_attributes).entity

        ticket_list_from_core.sort(key=lambda x: x.number, reverse=False)
        results = \
            self.gate_provider.search_client.search_ticket_in_core(
                status=self.status_1,
                created_at_range='[{0},{1}]'.format(self.utc_start_time,
                                                    self.utc_end_time)).entity

        results.tickets.sort(key=lambda x: x.number, reverse=False)

        self.assertTrue(len(ticket_list_from_core) == len(results.tickets),
                        "The length of two lists does not match. {0} != {1}"
                        .format(len(ticket_list_from_core),
                                len(results.tickets)))

        for i in range(0, len(results.tickets)):
            self.assertEquals(results.tickets[i], ticket_list_from_core[i],
                              msg="The data does not match for Ticket: {0}"
                              .format(results.tickets[i].number))

    @attr(type='positive', module='read', suite='smoke', defect='true')
    def test_all_the_dates_are_converted_to_UTC_format(self):
        '''
        @summary:B-42997: Load existing tickets to ticket search and
        test that the date fields are converted to UTC
        '''

        cust_condition = \
            WhereEquals("status_name", self.status_1).AND(
                WhereGreaterOrEquals("created", self.start_time)).AND(
                    WhereLessOrEquals("created", self.end_time))
        ticket_list_from_core = \
            self.core_provider.ticket_client.list_tickets_by_ticket_attributes(
                cust_condition, attributes=self.core_attributes).entity
        ticket_list_from_core.sort(key=lambda x: x.number, reverse=False)
        results = self.gate_provider.\
            search_client.\
            search_ticket_in_core(status=self.status_1,
                                  created_at_range='[{0},{1}]'.
                                  format(self.utc_start_time,
                                         self.utc_end_time)).entity
        results.tickets.sort(key=lambda x: x.number, reverse=False)

        for i in range(0, len(results.tickets)):
            self.assertEquals(results.tickets[i].created_at,
                              convert_date_from_cst_to_utc_date(
                              ticket_list_from_core[i].created) +
                              self.utc_date_constant,
                              msg="The created date is not converted to \
                                  UTC for Ticket: {0}".format(
                                  results.tickets[i].number))
            self.assertEquals(results.tickets[i].updated_at,
                              convert_date_from_cst_to_utc_date(
                              ticket_list_from_core[i].modified) +
                              self.utc_date_constant,
                              msg="The modified date is not converted to \
                                  UTC for Ticket: {0}".format(
                                  results.tickets[i].number))
            if ticket_list_from_core[i].last_public_response_date is not None:
                self.assertEquals(results.tickets[i].last_public_response_date,
                                  convert_date_from_cst_to_utc_date(
                                  ticket_list_from_core[i].
                                  last_public_response_date) +
                                  self.utc_date_constant,
                                  msg="The last_public_response_date is not \
                                      converted to UTC for Ticket: {0}".format(
                                      results.tickets[i].number))

    @attr(type='positive', module='read', suite='smoke', defect='true')
    def test_content_type_of_response(self):
        '''
        @summary:B-42997: Verify the content-type should be application/json
        '''
        results = self.gate_provider.search_client.search_ticket_in_core()
        self.assertEqual(results.headers.get("content-type"),
                         self.content_type, "The content type is {0} and not \
                         application/json".format(
                         results.headers.get("content-type")))
