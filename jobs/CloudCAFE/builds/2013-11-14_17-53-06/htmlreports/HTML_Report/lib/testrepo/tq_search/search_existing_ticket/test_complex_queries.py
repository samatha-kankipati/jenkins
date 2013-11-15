import time
import datetime
from datetime import timedelta

from ccengine.common.decorators import attr
from ccengine.domain.tq_search.request.complex_queries_request \
    import Property, ComplexQuery
from ccengine.domain.tq_search.response.tq_search import TicketDetails
from testrepo.common.testfixtures.tq_search import TQSearchFixture


class TestComplexQueries(TQSearchFixture):

    @attr(type='positive', module='complex_query', suite='regression')
    def test_and_operator(self):
        """
        @summary-Use and operator and verify that the complex query is
        working fine.
        """
        query = (Property("queue.id").equals(self.queue_id_alt_ref) &
                 Property("status").equals(self.status_1, self.status_5))

        payload = ComplexQuery(query)
        resp = self.complex_query_client.filter_tickets(payload)
        self.assertEquals(
            resp.status_code, 200,
            "Failed: Expected 200 but got {0}".format(resp.status_code)
        )
        actual_tickets = resp.entity.tickets
        actual_total = resp.entity.total

        query_params = {
            'queue.id': self.queue_id_alt_ref, 'status': self.status_1}
        set_one = \
            self.gate_provider.search_client.search_ticket_in_core(
                hardcoded_parameters=query_params).entity
        query_params = {
            'queue.id': self.queue_id_alt_ref, 'status': self.status_5}
        set_two = \
            self.gate_provider.search_client.search_ticket_in_core(
                hardcoded_parameters=query_params).entity
        expected_tickets = set_one.tickets + set_two.tickets
        expected_total = int(set_one.total) + int(set_two.total)
        self.assertEquals(actual_total, expected_total,
                          "The ticket totals are different :{} != {}"
                          .format(actual_total, expected_total))

    @attr(type='positive', module='complex_query', suite='regression')
    def test_or_operator(self):
        """
        @summary-Use or operator and verify that the complex query is
        working fine.
        """
        query = (Property("queue.id").equals(self.queue_id_alt_ref) |
                 Property("account.contacts.name").equals(self.team_name_alt))

        payload = ComplexQuery(query)
        resp = self.gate_provider.complex_query_client.filter_tickets(payload)
        self.assertEquals(
            resp.status_code, 200,
            "Failed: Expected 200 but got {0}".format(resp.status_code)
        )
        actual_tickets = resp.entity.tickets
        actual_total = resp.entity.total

        query_params = {'queue.id': self.queue_id_alt_ref}
        set_one = \
            self.gate_provider.search_client.search_ticket_in_core(
                hardcoded_parameters=query_params).entity
        query_params = {'account.contacts.name': self.team_name_alt}
        set_two = \
            self.gate_provider.search_client.search_ticket_in_core(
                hardcoded_parameters=query_params).entity
        expected_tickets = set_one.tickets + set_two.tickets
        expected_total = int(set_one.total) + int(set_two.total)
        self.assertEquals(actual_total, expected_total,
                          "The ticket totals are different :{} != {}"
                          .format(actual_total, expected_total))

    @attr(type='positive', module='complex_query', suite='smoke')
    def test_not_operator(self):
        """
        @summary-Use not operator and verify that the complex query is
        working fine.
        """
        query = (Property("queue.id").not_equals(self.queue_id_alt_ref))

        payload = ComplexQuery(query)
        resp = self.gate_provider.complex_query_client.filter_tickets(payload)
        actual_tickets = resp.entity.tickets
        actual_total = resp.entity.total
        query_params = {'queue.id!': self.queue_id_alt_ref}

        results = \
            self.gate_provider.search_client.search_ticket_in_core(
                hardcoded_parameters=query_params).entity
        self.assertEquals(
            resp.status_code, 200,
            "Failed: Expected 200 but got {0}".format(resp.status_code)
        )
        expected_tickets = results.tickets
        expected_total = results.total

        self.assertEquals(actual_total, expected_total,
                          "The ticket totals are different :{} != {}"
                          .format(actual_total, expected_total))
        for i in range(0, len(actual_tickets)):
            self.assertEquals(actual_tickets[i].number, expected_tickets[i].
                              number, msg="Data does not match for Ticket: {0}"
                              .format(actual_tickets[i].number))

    @attr(type='positive', module='complex_query', suite='smoke')
    def test_submitter_operator(self):
        """
        @summary-Verify that the query params and the complex query is working
        fine for submitter field.
        """
        query = (Property("submitter.sso").not_equals(self.assignee_user_id))

        payload = ComplexQuery(query)
        resp = self.gate_provider.complex_query_client.filter_tickets(payload)
        actual_tickets = resp.entity.tickets
        actual_total = resp.entity.total
        query_params = {'submitter.sso!': self.assignee_user_id}

        results = \
            self.gate_provider.search_client.search_ticket_in_core(
                hardcoded_parameters=query_params).entity
        self.assertEquals(
            resp.status_code, 200,
            "Failed: Expected 200 but got {0}".format(resp.status_code))
        expected_tickets = results.tickets
        expected_total = results.total
        self.assertEquals(actual_total, expected_total,
                          "The ticket totals are different :{0} != {1}"
                          .format(actual_total, expected_total))

    @attr(type='positive', module='complex_query', suite='smoke')
    def test_multi_operators(self):
        """
        @summary-Use combination of operator and verify that the complex
        query is working fine.
        """
        query = (
            Property("queue.id").equals(self.sync_queue_id) &
            Property("status").equals(self.status_1)) | (
                Property("queue.id").equals(self.queue_id_alt_ref_1) &
                Property("status").equals(self.status_5))

        payload = ComplexQuery(query)
        resp = self.gate_provider.complex_query_client.filter_tickets(payload)
        self.assertEquals(
            resp.status_code, 200,
            "Failed: Expected 200 but got {0}".format(resp.status_code)
        )
        actual_tickets = resp.entity.tickets
        actual_total = resp.entity.total
        query_params = {
            'queue.id': self.sync_queue_id, 'status': self.status_1}
        set_one = \
            self.gate_provider.search_client.search_ticket_in_core(
                hardcoded_parameters=query_params).entity
        query_params = {
            'queue.id': self.queue_id_alt_ref_1, 'status': self.status_5}
        set_two = \
            self.gate_provider.search_client.search_ticket_in_core(
                hardcoded_parameters=query_params).entity

        expected_tickets = set_one.tickets + set_two.tickets
        expected_total = set_one.total + set_two.total
        self.assertEquals(actual_total, expected_total,
                          "The ticket totals are different :{} != {}"
                          .format(actual_total, expected_total))

    @attr(type='positive', module='complex_query', suite='smoke')
    def test_list_query(self):
        """
        @summary-Use list operator and verify that the complex
        query is working fine.
        """
        query = (
            Property("queue.id").in_list(self.sync_queue_id, self.queue_id_alt)
            & Property("status").equals(self.status_1))
        payload = ComplexQuery(query)
        resp = self.gate_provider.complex_query_client.filter_tickets(payload)
        self.assertEquals(
            resp.status_code, 200,
            "Failed: Expected 200 but got {0}".format(resp.status_code)
        )
        actual_tickets = resp.entity.tickets
        actual_total = resp.entity.total
        query_params = {
            'queue.id': self.sync_queue_id, 'status': self.status_1}
        set_one = \
            self.gate_provider.search_client.search_ticket_in_core(
                hardcoded_parameters=query_params).entity
        query_params = {'queue.id': self.queue_id_alt, 'status': self.status_1}
        set_two = \
            self.gate_provider.search_client.search_ticket_in_core(
                hardcoded_parameters=query_params).entity

        expected_tickets = \
            set_one.tickets + set_two.tickets
        expected_total = set_one.total + set_two.total
        self.assertEquals(actual_total, expected_total,
                          "The ticket totals are different :{} != {}"
                          .format(actual_total, expected_total))

    @attr(type='positive', module='complex_query', suite='smoke')
    def test_range_query(self):
        """
        @summary-Use range operator and verify that the complex
        query is working fine.
        """
        query = (Property("createdAt").in_range(self.utc_start_time_3,
                                                self.utc_end_time_1
                                                ))

        payload = ComplexQuery(query)
        resp = self.gate_provider.complex_query_client.filter_tickets(payload)
        self.assertEquals(
            resp.status_code, 200,
            "Failed: Expected 200 but got {0}".format(resp.status_code)
        )
        actual_tickets = resp.entity.tickets
        actual_total = resp.entity.total
        result = \
            self.gate_provider.search_client.search_ticket_in_core(
                created_at_range=
                '[{0},{1}]'.format(self.utc_start_time_3,
                                   self.utc_end_time_1)).entity
        expected_tickets = result.tickets
        expected_total = result.total
        self.assertEquals(actual_total, expected_total,
                          "The ticket totals are different :{} != {}"
                          .format(actual_total, expected_total))

    @attr(type='positive', module='complex_query', suite='smoke')
    def test_result_sorting(self):
        """
        @summary-Use sort option and verify that the complex
        query is working fine.
        """
        query = ((Property("queue.id").equals(self.queue_id_alt_ref_2) &
                 Property("status").equals(self.status_3)))
        payload = ComplexQuery(query)
        requestslib_kwargs = {}
        requestslib_kwargs['params'] = {"sort": "number"}
        sorted_resp = self.gate_provider.complex_query_client.filter_tickets(
            payload, requestslib_kwargs)
        requestslib_kwargs['params'] = None
        unsorted_resp = self.gate_provider.complex_query_client.filter_tickets(
            payload, requestslib_kwargs)
        actual_tickets = sorted_resp.entity.tickets
        expected_tickets = sorted(
            unsorted_resp.entity.tickets, key=lambda ticket: ticket.number)
