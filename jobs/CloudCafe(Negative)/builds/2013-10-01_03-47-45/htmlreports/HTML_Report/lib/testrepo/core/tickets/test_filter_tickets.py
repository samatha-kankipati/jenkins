from ccengine.common.decorators import attr
from ccengine.domain.core.request.core_request import WhereEquals
from testrepo.common.testfixtures.core import CoreFixture


class TestListTicket(CoreFixture):

    @attr(type='smoke')
    def test_list_ticket(self):
        """@summary: Verify that listing of tickets by a creator returns only\
        the tickets created by the specified creator
        """
        creator_firstname = "Sunita"
        creator_lastname = "Venkatachalam"
        creator_name = "%s %s" % (creator_firstname, creator_lastname)
        creatorCondition = \
            WhereEquals("creator_first_name", creator_firstname)\
            .AND(WhereEquals("creator_last_name", creator_lastname))
        tickets = self.ticket_client.\
                  list_tickets_by_ticket_attributes(creatorCondition,
                  attributes={"id": "number", "creator_name": "creator.name"}
                  ).entity
        # Verify the ticket list for the creator condition
        for ticket in tickets:
            self.assertEqual(ticket.creator_name, creator_name,
            "Expected creator ='%s', Actual creator ='%s' for ticket id %s"
             % (creator_name, ticket.creator_name, ticket.id))

    @attr(type='smoke')
    def test_count_tickets_using_loadQueueView(self):
        """ @summary: Verify response of the count tickets with a specific\
        status type for a queue using method: 'loadQueueView' and
        class: Ticket.Ticket
        """
        queue_id = 3
        status_type = [8]
        offset = 0
        limit = 10
        response = self.ticket_client.\
                            get_ticket_count(queue_id, status_type,
                                             offset, limit)

        self.assertEqual(200, response.status_code,
                         "Actual response code is not 200")
        self.assertTrue(response.entity.result is not None,
                        "Ticket count is not returning any result {0}"
                        .format(response.entity.result))

    @attr(type='smoke')
    def test_list_ticket_for_specific_queue_and_status(self):
        """@summary: Verifying the ticket details for all ticket belonging to\
        specific queue and specific status using Ticket.TicketWhere"""
        queue_name = "Enterprise Services (All Teams)"
        status_type = 4
        limit = 10
        offset = 1
        attribute = {"id": "number", "queue_name": "queue.name",
                     "status": "status"}
        filter_condition = \
                          WhereEquals("queue_name", queue_name)\
                          .AND(WhereEquals("status_type", status_type))
        tickets = self.ticket_client.\
                  list_tickets_by_ticket_attributes(filter_condition,
                                                    attributes=attribute,
                                                    limit=limit,
                                                    offset=offset).entity
        for ticket in tickets:
            self.assertEqual(ticket.queue_name, queue_name,
                             "Expected queue name {0} is not same as actual\
                             queue name {1}".format(queue_name, ticket.queue_name))

    @attr(type='smoke')
    def test_list_tickets_using_loadQueueView_with_conditions(self):
        """
        @summary: Verify response of the list tickets with a specific
        status type for a queue using method: 'loadQueueView' &
        class: Ticket.Ticket
        """
        attributes = {"assignee": "assignee.name", "number": "number",
                      "subject": "subject",
                      "has_linux_servers": "has_linux_servers"}
        queue_id = 3
        status_type = [8]
        offset = 0
        limit = 10
        response = self.ticket_client.\
                            get_ticket_count(queue_id, status_type, offset,
                                             limit, attributes,)

        self.assertEqual(200, response.status_code,
                         "Actual response code is not 200")
        self.assertTrue(len(response.entity) > 0,
                        "Ticket count is not returning any result {0}\
                        ".format(len(response.entity)))
