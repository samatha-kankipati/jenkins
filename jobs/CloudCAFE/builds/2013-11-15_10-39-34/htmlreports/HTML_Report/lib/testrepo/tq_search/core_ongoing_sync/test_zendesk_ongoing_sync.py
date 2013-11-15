import datetime
from datetime import timedelta
import time

from ccengine.common.decorators import attr
from ccengine.common.tools.datatools import string_to_datetime, \
    convert_date_from_cst_to_utc_date
from ccengine.domain.tq_search.response.tq_search import TicketDetails
from testrepo.common.testfixtures.tq_search import TQSearchFixture


class TestZenDeskOngoingSync(TQSearchFixture):

    @classmethod
    def setUpClass(cls):
        super(TestZenDeskOngoingSync, cls).setUpClass()
        cls.hybrid_int_smb_grp_id = 20596722
        cls.isl_dev_assignee_id = 296396271
        cls.comment_text = 'isl-staging'
        cls.subject = 'This is flow api test ticket'
        cls.priority = 'low'
        cls.zen_desk_tkt = cls.zendesk_provider.zendesk_client.create_ticket(
                group_id=20596722, comment_body='ts-staging',
                subject='zen desk ticket', assignee_id=296396271,
                priority='low', tags=['Linux']).entity
        cls.zen_desk_tkt_1 = cls.zendesk_provider.zendesk_client.create_ticket(
                group_id=20596722, comment_body='ts-staging',
                subject='zen desk ticket2', assignee_id=296396271,
                priority='low').entity
        print "TICKET NUMBER:"
        print cls.zen_desk_tkt.id
        print cls.zen_desk_tkt_1.id
        time.sleep(150)
    @classmethod
    def tearDownClass(cls):
        super(TestZenDeskOngoingSync, cls).tearDownClass()
        """
        @summary:Close the ticket as a part of tear down
        """
        update_tag=['auto-close']
        cls.zendesk_provider.zendesk_client.update_ticket(
            ticket_number=cls.zen_desk_tkt_1.id, tags=update_tag)
        cls.zendesk_provider.zendesk_client.update_ticket(
            ticket_number=cls.zen_desk_tkt.id, tags=update_tag)

    @attr(type='positive', module='read', suite='smoke')
    def test_tkt_create_zen_desk(self):
        """
        @summary:test that when a ticket is created in zen desk
        it reflects in to tq_search after a given time interval
        """
        results = \
            self.gate_provider.search_client.search_ticket_in_core(
                number=self.zen_desk_tkt.id).entity
        self.assertTrue(len(results.tickets) == 1,
                        "The ticket{0} is not present in tq_search".format(
                            self.zen_desk_tkt.id))
        self.assertEquals(results.tickets[0].subject,
                        'zen desk ticket')
        self.assertEquals(results.tickets[0].priority, 'Low')
        self.assertEquals(results.tickets[0].status, "Open")
        self.assertEquals(results.tickets[0].queue.id, unicode(20596722))
        self.assertEquals(results.tickets[0].source_system, "ZENDESK")
        self.assertEquals(results.tickets[0].tags, ["linux"])
        self.assertEquals(results.tickets[0].technology, "linux")
        self.assertEquals(results.tickets[0].location, "NONE")

    @attr(type='positive', module='read', suite='smoke')
    def test_tkt_update_zen_desk_status(self):
        """
        @summary:test that when a the status of a ticket is updated in
        zen desk same reflects in tq_search
        """
        update_status = "pending"

        # Write the  update method for zendesk for updating status
        self.zendesk_provider.zendesk_client.update_ticket(
            ticket_number=self.zen_desk_tkt.id, status=update_status)
        time.sleep(100)
        results = \
            self.gate_provider.search_client.search_ticket_in_core(
                number=self.zen_desk_tkt.id).entity
        self.assertEquals(results.tickets[0].status.lower(),
                          update_status.lower())

    @attr(type='positive', module='read', suite='smoke')
    def test_tkt_update_zen_desk_priority(self):
        """
        @summary:test that when a the priority of a ticket is updated in
        zen desk same reflects in tq_search
        """
        update_priority = "urgent"

        # Write the  update method for zendesk for updating priority
        self.zendesk_provider.zendesk_client.update_ticket(
            ticket_number=self.zen_desk_tkt.id, priority=update_priority)
        time.sleep(100)
        results = \
            self.gate_provider.search_client.search_ticket_in_core(
                number=self.zen_desk_tkt.id).entity
        self.assertEquals(results.tickets[0].priority.lower(),
                          update_priority.lower())

    @attr(type='positive', module='read', suite='smoke')
    def test_tkt_update_zen_desk_assignee(self):
        """
        @summary:test that when a the assignee of a ticket is updated in
        zen desk same reflects in tq_search
        """
        update_assignee = 472132118

        # Write the  update method for zendesk for updating assignee
        self.zendesk_provider.zendesk_client.update_ticket(
            ticket_number=self.zen_desk_tkt_1.id, assignee_id=update_assignee)
        time.sleep(100)
        results = \
            self.gate_provider.search_client.search_ticket_in_core(
                number=self.zen_desk_tkt_1.id).entity
        self.assertEquals(results.tickets[0].assignee.name,
                          "TQ_Delta Service Account")
        
    @attr(type='positive', module='read', suite='regression')
    def test_tkt_update_zen_desk_devices(self):
        """
        @summary:test that when a the device of a ticket is updated in
        zen desk same reflects in tq_search
        """
        update_device = ['windows']

        # Write the  update method for zendesk for updating assignee
        self.zendesk_provider.zendesk_client.update_ticket(
            ticket_number=self.zen_desk_tkt_1.id, tags=update_device)
        time.sleep(100)
        results = \
            self.gate_provider.search_client.search_ticket_in_core(
                number=self.zen_desk_tkt.id).entity
        self.assertTrue(results.tickets[0].has_linux_servers)

    #@attr(type='positive11', module='read', suite='regression')
    #def test_tkt_update_zen_desk_category(self):
    #    """
    #    @summary:test that when a the category of a ticket is updated in
    #    zen desk same reflects in tq_search
    #    """
    #    category = 14215
    #
    #    # Write the  update method for zendesk for updating assignee
    #    self.zendesk_provider.zendesk_client.update_ticket(
    #        ticket_number=self.zen_desk_tkt_1.id, categories=category)
    #    time.sleep(50)
    #    results = \
    #        self.gate_provider.search_client.search_ticket_in_core(
    #            number=self.zen_desk_tkt_1.id).entity
    #    print results.tickets[0]
    #    self.assertEquals(results.tickets[0].category, category)

    @attr(type='positive', module='read', suite='regression')
    def test_tkt_faceting(self):
        """
        @summary:test that facting works for zendesk
        """
        field = "zendesk"

        # Write the  update method for zendesk for updating assignee
        self.gate_provider.search_client.get_facets(
            fields=field)
        time.sleep(100)
        results = \
            self.gate_provider.search_client.search_ticket_in_core(
                number=self.zen_desk_tkt_1.id).entity
        self.assertTrue(results.tickets is not None)