import datetime
from datetime import timedelta
import time

from ccengine.common.decorators import attr
from ccengine.domain.core.request.core_request import Where, WhereSet, \
    WhereCondition, WhereOperators, WhereEquals, WhereGreaterOrEquals, \
    WhereNotEquals, WhereLessOrEquals, LoadArgs, CoreQuery
from ccengine.domain.tq_search.response.tq_search import TicketDetails
from testrepo.common.testfixtures.tq_search import TQSearchFixture


class TestPagination(TQSearchFixture):

    def tearDown(cls):
        '''
        @summary: This sleep is there as there as the core user that we use
        for testing has rate limitaion on it and in case where there are
        more than 10 requests in 10 seconds time outs show up, so as a
        temporary fix we need sleep over here
        '''
        super(TestPagination, cls).tearDownClass()
        time.sleep(3)

    @attr(type='positive', module='read', suite='smoke', defect='true')
    def test_next_previous_link_of_pagination_during_list_tickets(self):
        """
        @summary:Verify that next previous link takes the user to the
        corresponding page
        """
        results = self.gate_provider.search_client.\
            search_ticket_in_core().entity
        next_result = self.gate_provider.search_client.search_ticket_in_core(
            url=results.next).entity
        self.assertEqual(next_result.offset, results.offset+next_result.limit,
                         "The next link in the pagnation didnt navigate the \
                         user to the next page")
        previous_result = self.gate_provider.search_client.\
            search_ticket_in_core(url=results.previous).entity
        self.assertEqual(previous_result.offset,
                         next_result.offset-previous_result.limit,
                         "The previous link in the pagnation didnt navigate\
                         the user to the previous page")

    @attr(type='positive', module='read', suite='smoke')
    def test_first_link_of_pagination_during_list_ticket(self):
        """
        @summary:Verify that first link of the pagination takes the user to the
        first page
        """
        results = self.gate_provider.search_client.\
            search_ticket_in_core().entity
        first_page_result = self.gate_provider.search_client.\
            search_ticket_in_core(url=results.first).entity
        self.assertEqual(first_page_result.offset, results.offset)
        self.assertTrue((first_page_result.previous is None), "The\
                        previous link is not none")

    @attr(type='positive', module='read', suite='smoke')
    def test_last_link_of_pagination_during_list_ticket(self):
        """
        @summary:Verify last link of the pagination takes the user to the last
        page
        """
        results = self.gate_provider.search_client.\
            search_ticket_in_core().entity
        last_page_result = self.gate_provider.search_client.\
            search_ticket_in_core(url=results.last).entity
        self.assertTrue(last_page_result.next is None)

    @attr(type='in_progress', module='read', suite='regression')
    def test_find_a_ticket_using_pagination(self):
        """
        @summary:Verify that we can find a ticket using pagination
        """
        cust_condition = WhereEquals("status_name", self.status_1)
        ticket_list_from_core = self.core_provider.ticket_client.\
            list_tickets_by_ticket_attributes(cust_condition, limit=100,
                                              offset=0,
                                              attributes=self.core_attributes
                                              ).entity
        ticket_to_be_searched = ticket_list_from_core[(len(
                                                       ticket_list_from_core
                                                       )-1)].number
        results = self.gate_provider.\
            search_client.search_ticket_in_core(status=self.status_1).entity
        ticket_number = []
        flag = False
        offset_value = results.offset
        while(offset_value <= (results.total-(results.total % results.limit))):
            offset_value = offset_value+results.limit
            next_url = results.next
            for ticket in results.tickets:
                ticket_number.append(ticket.number)
                if (ticket_to_be_searched in ticket_number):
                    flag = True
                    return
            results = self.gate_provider.search_client.\
                search_ticket_in_core(url=next_url).entity
            if flag is True:
                return
        self.assertTrue(flag, "The ticket is not present in the list given ")

    @attr(type='positive', module='read', suite='smoke')
    def test_ascending_sorting_order_when_fetching_the_tickets(self):
        """
        @summary:Verify that when ASC is specified for sorting then
        tickets get arranged accordingly
        """
        date_range = "[{0},{1}]".format(self.utc_start_time, self.utc_end_time)

        # Fetching the tickets from ticket search and then sorting them
        sample_results = self.gate_provider.search_client.\
            search_ticket_in_core(sort="number|ASC",
                                  created_at_range=date_range).entity

        # Comparing the above lists elements are in ascending order
        for i in range(0, len(sample_results.tickets)-1):
            self.assertTrue((sample_results.tickets[i].number).replace
                            ('-', "") < (sample_results.tickets[i+1].number).
                            replace('-', ""),
                            "List not in ascending order at position\
                            {0}".format(i))

    @attr(type='positive', module='read', suite='smoke')
    def test_descending_sorting_order_when_fetching_the_tickets(self):
        """
        @summary:Verify that when DESC is specified for sorting then
        tickets get arranged accordingly
        """
        # Fetching the sorted list from the ticket search application
        date_range = "[{0},{1}]".format(self.utc_start_time, self.utc_end_time)

        # Fetching the tickets from ticket search and then sorting them
        sample_results = self.gate_provider.search_client.\
            search_ticket_in_core(sort="number|DESC",
                                  created_at_range=date_range).entity

        # Comparing the above lists elements are in descending order
        for i in range(0, len(sample_results.tickets)-1):
            self.assertTrue((sample_results.tickets[i].number).replace
                            ('-', "") > (sample_results.tickets[i+1].number).
                            replace('-', ""),
                            "List not in descending order at position\
                            {0}".format(i))

    @attr(type='positive', module='read', suite='smoke')
    def test_default_sorting_order_is_ascending(self):
        """
        @summary:Verify that default sorting order is ascending
        """
        # Fetching the sorted list from the ticket search application
        date_range = "[{0},{1}]".format(self.utc_start_time, self.utc_end_time)

        # Fetching the tickets from ticket search and then not specifying
        # anything for sorting
        sample_results = self.gate_provider.search_client.\
            search_ticket_in_core(sort="number",
                                  created_at_range=date_range).entity

        # Comparing the above lists elements are in ascending order
        for i in range(0, len(sample_results.tickets)-1):
            self.assertTrue((sample_results.tickets[i].number).replace
                            ('-', "") < (sample_results.tickets[i+1].number).
                            replace('-', ""),
                            "List not in ascending order at position\
                            {0}".format(i))

    @attr(type='negative', module='read', suite='smoke')
    def test_incorrect_sorting_specified_raises_bad_request(self):
        """@summary:verify that incorrect sorting order raise bad request"""
        date_range = "[{0},{1}]".format(self.utc_start_time, self.utc_end_time)
        results = self.gate_provider.search_client.\
            search_ticket_in_core(sort="number|xyz",
                                  created_at_range=date_range)

        self.assertEquals(eval(results.content).get('badRequest').
                          get('message'), "Bad Request", "Failed Expected:Bad\
                          Request Received:{%s}" % (eval(results.content).
                                                    get('badRequest')
                                                    .get('message')))
        self.assertEquals(eval(results.content).get('badRequest').
                          get('code'), 400, "Failed Expected:400 \
                          Returned:{%s}" % eval(results.content)
                          .get('badRequest'))
