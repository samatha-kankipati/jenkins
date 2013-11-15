import datetime
from datetime import timedelta
import time

from ccengine.common.decorators import attr
from ccengine.common.tools.datatools import string_to_datetime, \
    convert_date_from_cst_to_utc_date
from ccengine.domain.tq_search.response.tq_search import TicketDetails
from ccengine.domain.core.request.core_request import Where, WhereSet, \
    WhereCondition, WhereOperators, WhereEquals, WhereGreaterOrEquals, \
    WhereLessOrEquals, LoadArgs, CoreQuery, WhereIn, WhereNotEquals, \
    WhereNotIn, WhereLess, WhereGreater
from testrepo.common.testfixtures.tq_search import TQSearchFixture


class TestListTickets(TQSearchFixture):

    def tearDown(cls):
        '''
        @summary: This sleep is there as there as the core user that we use
        for testing has rate limitaion on it and in case where there are
        more than 10 requests in 10 seconds time outs show up, so as a
        temporary fix we need sleep over here
        '''
        super(TestListTickets, cls).tearDownClass()
        time.sleep(3)

    @attr(type='positive', module='read', suite='smoke')
    def test_list_tickets_by_single_value_for_equal_operator(self):
        '''
        @summary:B-44514: list tickets by single value for "=" operator
        '''
        cust_condition = WhereEquals("status_name", self.status_2).AND(
            WhereGreaterOrEquals("created", self.start_time)).AND(
                WhereLessOrEquals("created", self.end_time))
        ticket_list_from_core = \
            self.core_provider.ticket_client.list_tickets_by_ticket_attributes(
                cust_condition, attributes=self.core_attributes).entity
        ticket_list_from_core.sort(key=lambda x: x.number, reverse=False)
        results = \
            self.gate_provider.search_client.search_ticket_in_core(
                created_at_range=
                "[{0},{1}]".format(self.utc_start_time, self.utc_end_time),
                status=self.status_2).entity
        results.tickets.sort(key=lambda x: x.number, reverse=False)

        self.assertTrue(len(ticket_list_from_core) == len(results.tickets),
                        "The length of two lists does not match. {0} != {1}".
                        format(len(ticket_list_from_core),
                               len(results.tickets)))

        for i in range(0, len(results.tickets)):
            self.assertEquals(results.tickets[i], ticket_list_from_core[i],
                              msg="The data does not match for Ticket: {0}".
                                  format(results.tickets[i].number) + str(i))

    @attr(type='positive', module='read', suite='smoke')
    def test_list_tickets_by_multiple_values_for_equal_operator(self):
        '''
        @summary:B-44514: list tickets by multiple values for "=" operator
        '''

        cust_condition = \
            WhereIn("status_name", ["Scheduled", "In Progress"]).AND(
                WhereGreaterOrEquals("created", self.start_time)).AND(
                    WhereLessOrEquals("created", self.end_time))
        ticket_list_from_core = \
            self.core_provider.ticket_client.list_tickets_by_ticket_attributes(
                cust_condition, attributes=self.core_attributes).entity
        ticket_list_from_core.sort(key=lambda x: x.number, reverse=False)

        results = \
            self.gate_provider.search_client.search_ticket_in_core(
                created_at_range=
                "[{0},{1}]".format(self.utc_start_time, self.utc_end_time),
                status="{0},{1}".format(self.status_2, self.status_3)).entity

        results.tickets.sort(key=lambda x: x.number, reverse=False)

        self.assertTrue(len(ticket_list_from_core) == len(results.tickets),
                        "The length of two lists does not match. {0} != {1}".
                        format(len(ticket_list_from_core),
                               len(results.tickets)))

        for i in range(0, len(results.tickets)):
            self.assertEquals(results.tickets[i], ticket_list_from_core[i],
                              msg="The data does not match for Ticket: {0}".
                                  format(results.tickets[i].number) + str(i))

    @attr(type='regression', module='read', suite='smoke')
    def test_list_tickets_query_params_with_single_value_and_eql_op(self):
        '''
        @summary:B-44514: list tickets by combination of query parameters
        with single value and "=" operator
        '''

        cust_condition = \
            WhereEquals("status_name", self.status_1).AND(
                WhereEquals("queue_name", self.queue_name)).AND(
                    WhereGreaterOrEquals("created", self.start_time)).AND(
                        WhereLessOrEquals("created", self.end_time))
        ticket_list_from_core = \
            self.core_provider.ticket_client.list_tickets_by_ticket_attributes(
                cust_condition, attributes=self.core_attributes).entity
        ticket_list_from_core.sort(key=lambda x: x.number, reverse=False)

        results = \
            self.gate_provider.search_client.search_ticket_in_core(
                created_at_range=
                "[{0},{1}]".format(self.utc_start_time, self.utc_end_time),
                status="new", queue=self.queue_name).entity

        results.tickets.sort(key=lambda x: x.number, reverse=False)

        self.assertTrue(len(ticket_list_from_core) == len(results.tickets),
                        "The length of two lists does not match. {0} != {1}".
                        format(len(ticket_list_from_core),
                               len(results.tickets)))

        for i in range(0, len(results.tickets)):
            self.assertEquals(results.tickets[i], ticket_list_from_core[i],
                              msg="The data does not match for Ticket: {0}".
                                  format(results.tickets[i].number) + str(i))

    @attr(type='regression', module='read', suite='smoke')
    def test_list_tickets_query_params_with_single_value_and_not_eql_op(self):
        '''
        @summary:B-44514: list tickets by combination of query
        parameters with single value and "!=" operator
        '''

        cust_condition = \
            WhereNotEquals("status_name", self.status_1).AND(
                WhereNotEquals("queue_name", self.queue_name)).AND(
                    WhereGreaterOrEquals("created", self.start_time)).AND(
                        WhereLessOrEquals("created", self.end_time)).AND(
                            WhereEquals("status_type", self.status_type))
        ticket_list_from_core = \
            self.core_provider.ticket_client.list_tickets_by_ticket_attributes(
                cust_condition, attributes=self.core_attributes).entity
        ticket_list_from_core.sort(key=lambda x: x.number, reverse=False)

        not_equals_params = {'status!': self.status_1,
                             'queue!': self.queue_name}

        results = \
            self.gate_provider.search_client.search_ticket_in_core(
                hardcoded_parameters=not_equals_params,
                created_at_range=
                '[{0},{1}]'.format(self.utc_start_time,
                                   self.utc_end_time)).entity

        results.tickets.sort(key=lambda x: x.number, reverse=False)

        self.assertTrue(len(ticket_list_from_core) == len(results.tickets),
                        "The length of two lists does not match. {0} != {1}".
                        format(len(ticket_list_from_core),
                               len(results.tickets)))

        for i in range(0, len(results.tickets)):
            self.assertEquals(results.tickets[i], ticket_list_from_core[i],
                              msg="The data does not match for Ticket: {0}".
                                  format(results.tickets[i].number) + str(i))

    @attr(type='positive', module='read', suite='smoke')
    def test_list_tickets_query_params_with_multiple_vals_and_not_eql_op(self):
        '''
        @summary:B-44514: list tickets by combination of
        query parameters with multiple values and "!=" operator
        '''

        cust_condition = \
            WhereNotIn("status_name", [self.status_1, self.status_3]).AND(
                WhereGreaterOrEquals("created", self.start_time)).AND(
                    WhereLessOrEquals("created", self.end_time)).AND(
                        WhereEquals("status_type", self.status_type))
        ticket_list_from_core = \
            self.core_provider.ticket_client.list_tickets_by_ticket_attributes(
                cust_condition, attributes=self.core_attributes).entity
        ticket_list_from_core.sort(key=lambda x: x.number, reverse=False)

        not_equals_params = {'status!': '{0},{1}'.format(self.status_1,
                                                         self.status_3)}

        results = \
            self.gate_provider.search_client.search_ticket_in_core(
                hardcoded_parameters=not_equals_params,
                created_at_range=
                '[{0},{1}]'.format(self.utc_start_time,
                                   self.utc_end_time)).entity

        results.tickets.sort(key=lambda x: x.number, reverse=False)

        self.assertTrue(len(ticket_list_from_core) == len(results.tickets),
                        "The length of two lists does not match. {0} != {1}".
                        format(len(ticket_list_from_core),
                               len(results.tickets)))

        for i in range(0, len(results.tickets)):
            self.assertEquals(results.tickets[i], ticket_list_from_core[i],
                              msg="The data does not match for Ticket: {0}".
                                  format(results.tickets[i].number) + str(i))

    @attr(type='positive', module='read', suite='smoke')
    def test_list_tickets_eql_and_not_eql_op_single_val_in_query_params(self):
        '''
        @summary:B-44514: list tickets by combination of
        "=" and "!=" operator with single value in query parameter
        '''

        cust_condition = \
            WhereEquals("priority", self.priority_1).AND(
                WhereNotEquals("account_number", self.account_number_1)).AND(
                    WhereGreaterOrEquals("created", self.start_time_1)).AND(
                        WhereLessOrEquals("created", self.end_time_1)).AND(
                            WhereEquals("status_type", self.status_type))
        ticket_list_from_core = \
            self.core_provider.ticket_client.list_tickets_by_ticket_attributes(
                cust_condition, attributes=self.core_attributes).entity
        ticket_list_from_core.sort(key=lambda x: x.number, reverse=False)
        not_equals_params = {'account.id!': self.tq_search_account_number_1}

        results = \
            self.gate_provider.search_client.search_ticket_in_core(
                priority=self.tq_search_priority_1,
                hardcoded_parameters=not_equals_params,
                created_at_range=
                '[{0},{1}]'.format(self.utc_start_time_1,
                                   self.utc_end_time_1)).entity

        results.tickets.sort(key=lambda x: x.number, reverse=False)
        self.assertTrue(len(ticket_list_from_core) == len(results.tickets),
                        "The length of two lists does not match. {0} != {1}".
                        format(len(ticket_list_from_core),
                               len(results.tickets)))

        for i in range(0, len(results.tickets)):
            self.assertEquals(results.tickets[i], ticket_list_from_core[i],
                              msg="The data does not match for Ticket: {0}".
                                  format(results.tickets[i].number) + str(i))

    @attr(type='positive', module='read', suite='smoke')
    def test_list_tickets_eql_and_noteql_op_multiple_vals_in_query_parms(self):
        '''
        @summary:B-44514: list tickets by combination of "="
        and "!=" operator with multiple values in query parameter
        '''

        cust_condition = \
            WhereIn("priority", [self.priority_1, self.priority_3]).\
            AND(WhereNotIn("account_number",
                           [self.account_number_1, self.account_number_2])).\
            AND(WhereGreaterOrEquals("created", self.start_time_1)).\
            AND(WhereLessOrEquals("created", self.end_time_1)).\
            AND(WhereEquals("status_type", self.status_type))
        ticket_list_from_core = \
            self.core_provider.ticket_client.list_tickets_by_ticket_attributes(
                cust_condition, attributes=self.core_attributes).entity
        ticket_list_from_core.sort(key=lambda x: x.number, reverse=False)

        not_equals_params = \
            {'account.id!': '{0},{1}'.format(self.tq_search_account_number_1,
                                             self.tq_search_account_number_2)}

        results = \
            self.gate_provider.search_client.search_ticket_in_core(
                priority=(self.tq_search_priority_1,
                          self.tq_search_priority_2),
                hardcoded_parameters=not_equals_params,
                created_at_range=
                '[{0},{1}]'.format(self.utc_start_time_1,
                                   self.utc_end_time_1)).entity

        results.tickets.sort(key=lambda x: x.number, reverse=False)

        self.assertTrue(len(ticket_list_from_core) == len(results.tickets),
                        "The length of two lists does not match. {0} != {1}".
                        format(len(ticket_list_from_core),
                               len(results.tickets)))

        for i in range(0, len(results.tickets)):
            self.assertEquals(results.tickets[i], ticket_list_from_core[i],
                              msg="The data does not match for Ticket: {0}".
                                  format(results.tickets[i].number) + str(i))

    @attr(type='positive', module='read', suite='smoke')
    def test_list_tickets_by_date_range_in_query_params_with_eql_op(self):
        '''
        @summary:B-44514: list tickets by date range in query parameter
        for "=" operator
        '''

        cust_condition = \
            WhereGreaterOrEquals("created", self.start_time).AND(
                WhereLessOrEquals("created", self.end_time)).AND(
                    WhereEquals("status_type", self.status_type))
        ticket_list_from_core = \
            self.core_provider.ticket_client.list_tickets_by_ticket_attributes(
                cust_condition, attributes=self.core_attributes).entity
        ticket_list_from_core.sort(key=lambda x: x.number, reverse=False)

        results = \
            self.gate_provider.search_client.search_ticket_in_core(
                created_at_range=
                '[{0},{1}]'.format(self.utc_start_time,
                                   self.utc_end_time)).entity
        results.tickets.sort(key=lambda x: x.number, reverse=False)

        self.assertTrue(len(ticket_list_from_core) == len(results.tickets),
                        "The length of two lists does not match. {0} != {1}".
                        format(len(ticket_list_from_core),
                               len(results.tickets)))

        for i in range(0, len(results.tickets)):
            self.assertEquals(results.tickets[i], ticket_list_from_core[i],
                              msg="The data does not match for Ticket: {0}".
                                  format(results.tickets[i].number) + str(i))

    @attr(type='positive1', module='read', suite='smoke')
    def test_list_tickets_by_date_range_in_query_params_with_not_eql_op(self):
        '''
        @summary:B-44514: list tickets by date range in query parameter
        for "!=" operator
        '''

        start_time = "2004-02-03 09:00:26"

        cust_condition = WhereLess("created", start_time).AND(
            WhereEquals("status_type", self.status_type))
        ticket_list_from_core = \
            self.core_provider.ticket_client.list_tickets_by_ticket_attributes(
                cust_condition, attributes=self.core_attributes).entity
        ticket_list_from_core.sort(key=lambda x: x.number, reverse=False)

        current_date_in_utc = convert_date_from_cst_to_utc_date(
            time.strftime("%Y-%m-%d %H:%M:%S",
                          datetime.datetime.now().timetuple()),
            date_format="%Y-%m-%dT%H:%M:%S") + ".000Z"

        not_equals_params =\
            {'createdAt_range!': '[{0},'.format(self.utc_start_time_2)
                + current_date_in_utc + ']'}
        results = self.gate_provider.search_client.search_ticket_in_core(
            hardcoded_parameters=not_equals_params).entity

        results.tickets.sort(key=lambda x: x.number, reverse=False)

        self.assertTrue(len(ticket_list_from_core) == len(results.tickets),
                        "The length of two lists does not match. {0} != {1}".
                        format(len(ticket_list_from_core),
                               len(results.tickets)))

    @attr(type='positive', module='read', suite='smoke')
    def test_list_tickets_queue_view_id(self):
        '''
        @summary:: list tickets by queue view id
        '''
        params = {'queueViewId!': self.utc_start_time_2}
        results = self.gate_provider.search_client.search_ticket_in_core(
            hardcoded_parameters=params).entity
        results_alt = self.gate_provider.search_client.\
            search_ticket_in_core().entity

        self.assertEquals(len(results_alt.tickets), len(results.tickets),
                          "The length of two lists does not match. {0} != {1}".
                          format(len(results_alt.tickets),
                                 len(results.tickets)))

    @attr(type='positive', module='read', suite='smoke')
    def test_get_specific_ticket_and_verify_it_exists_in_the_list(self):
        '''
        @summary:B-44514: Verify that a specific ticket
        exists in the list of tickets
        '''

        '''
        Fetching a ticket from core
        '''
        cust_condition = \
            WhereGreaterOrEquals("created", self.start_time).AND(
                WhereLessOrEquals("created", self.end_time)).AND(
                    WhereEquals("status_type", self.status_type))
        ticket_list_from_core = \
            self.core_provider.ticket_client.list_tickets_by_ticket_attributes(
                cust_condition, attributes=self.core_attributes).entity
        core_ticket = ticket_list_from_core[0]
        tq_search_ticket = self.gate_provider.search_client.\
            search_ticket_in_core(number=ticket_list_from_core[0]
                                  .number).entity
        self.assertEquals(tq_search_ticket.tickets[0], core_ticket,
                          "Failed Actual:{0} Expected:{1}"
                          .format(tq_search_ticket.ticket, core_ticket))

    @attr(type='positive', module='read', suite='smoke')
    def test_get_specific_ticket_using_query_parameters(self):
        '''
        @summary:B-44514: Verify that a specific ticket exists using
        query parameters
        '''
        cust_condition = \
            WhereGreaterOrEquals("created", self.start_time).AND(
                WhereLessOrEquals("created", self.end_time)).AND(
                    WhereEquals("status_type", self.status_type))
        ticket_list_from_core = self.core_provider.ticket_client.\
            list_tickets_by_ticket_attributes(cust_condition,
                                              attributes=self.
                                              core_attributes).entity
        core_ticket = ticket_list_from_core[0]
        tq_search_ticket = \
            self.gate_provider.\
            search_client.search_ticket_in_core(number=
                                                core_ticket.
                                                number).entity
        self.assertEquals(tq_search_ticket.tickets[0],
                          core_ticket, "Failed Expected:{0} Actual:{1}"
                          .format(tq_search_ticket.tickets[0], core_ticket))

    @attr(type='negative', module='read', status='smoke', defect='true')
    def test_incorrect_value_of_query_parameter_returns_no_ticket(self):
        '''
        @summary:B-44514: verify that no tickets are returned if the query is
        constructed using incorrect query parameter values
        '''
        results = \
            self.gate_provider.\
            search_client.search_ticket_in_core(status=1).entity
        self.assertTrue(len(results.tickets) == 0, "There are tickets coming\
                        for invalid query parameters.")

    @attr(type='negative', module='read', status='smoke', defect='true')
    def test_incorrect_query_parameter_returns_bad_request_400(self):
        '''
        @summary:B-44514: verify that bad request is returned if the query is
        constructed using incorrect query parameters
        '''
        new_params = {'1': '1'}
        results = self.gate_provider.search_client.search_ticket_in_core(
            hardcoded_parameters=new_params)

        self.assertEquals(eval(results.content).get('badRequest').
                          get('message'), "Bad Request", "Incorrect query\
                          parameters didnot return bad request")
        self.assertEquals(eval(results.content).get('badRequest').
                          get('code'), 400, "Incorrect quesry parameter\
                          didnot return code 400")

    @attr(type='negative', module='read', status='smoke', defect='true')
    def test_negative_value_of_limit_throws_bad_request_400(self):
        """
        @summary-Verify that if negative value of the limit is given
        then the application throws an exception of
        bad request with 400 code
        """
        results = self.gate_provider.search_client.\
            search_ticket_in_core(limit=-1)
        message = eval(results.content).get('badRequest').get('message')
        self.assertEquals(message, "Bad Request", "Incorrect query\
                          Expected:{0} Actual:{1}"
                          .format("Bad request", message))

    @attr(type='negative', module='read', status='smoke', defect='true')
    def test_no_value_of_limit_returns_zero_tickets(self):
        """
        @summary-Verify that if no value for the limit is given
        then the application returns 0 results
        """
        results = self.gate_provider.search_client.\
            search_ticket_in_core(limit=0).entity

        self.assertEquals(len(results.tickets), 0, "Incorrect Expected:{0} \
                          Actual:{1}".format(0, len(results.tickets)))
