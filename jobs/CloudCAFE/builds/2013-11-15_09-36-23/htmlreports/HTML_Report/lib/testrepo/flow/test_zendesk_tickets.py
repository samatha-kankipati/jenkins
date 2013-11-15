import time

from ccengine.common.decorators import attr
from testrepo.common.testfixtures.flow import FlowFixture
from testrepo.common.testfixtures.flow import TicketConst


class TestZendeskTickets(FlowFixture):
    @classmethod
    def setUpClass(cls):
        super(TestZendeskTickets, cls).setUpClass()
        comment_text = 'This is test'
        subject = 'This is flow api test ticket'
        cls.zd_closed_tkt = cls.zendesk_provider.zendesk_client.create_ticket(
            group_id=cls.zd_hybrid_int_smb_id, comment_body=comment_text,
            subject=subject, assignee_id=cls.testuser4_zd_id).entity
        zd_urgent_tkt = cls.zendesk_provider.zendesk_client.create_ticket(
            group_id=cls.zd_hybrid_int_smb_id, comment_body=comment_text,
            subject=subject, priority=TicketConst.zd_severity_urgent,
            status=TicketConst.zd_status_open, tags=['windows']).entity
        zd_high_tkt = cls.zendesk_provider.zendesk_client.create_ticket(
            group_id=cls.zd_hybrid_int_smb_id, comment_body=comment_text,
            subject=subject, priority=TicketConst.zd_severity_high,
            tags=['windows'], assignee_id=cls.testuser4_zd_id).entity
        zd_low_tkt = cls.zendesk_provider.zendesk_client.create_ticket(
            group_id=cls.zd_hybrid_int_smb_id, comment_body=comment_text,
            subject=subject, priority=TicketConst.zd_severity_low,
            status=TicketConst.zd_status_pending).entity
        zd_no_priority_tkt = cls.zendesk_provider.zendesk_client.create_ticket(
            group_id=cls.zd_hybrid_int_smb_id, comment_body=comment_text,
            subject=subject, assignee_id=cls.testuser4_zd_id,
            tags=['linux']).entity
        cls.zendesk_provider.zendesk_client.update_ticket(
            ticket_number=cls.zd_closed_tkt.id, tags=['auto_close'])

        # wait for the tickets from Zendesk to come to Flow API
        time.sleep(int(cls.wait_for_tickets))
        cls.flow_high_tkt = cls.flow_provider.\
            search_tickets_in_queue_views(
                zendesk_view_id=[cls.flow_hybrid_int_smb_id],
                ticket_number=zd_high_tkt.id)
        cls.flow_urgent_tkt = cls.flow_provider.\
            search_tickets_in_queue_views(
                zendesk_view_id=[cls.flow_hybrid_int_smb_id],
                ticket_number=zd_urgent_tkt.id)
        cls.flow_no_priority_tkt = cls.flow_provider.\
            search_tickets_in_queue_views(
                zendesk_view_id=[cls.flow_hybrid_int_smb_id],
                ticket_number=zd_no_priority_tkt.id)
        cls.flow_low_tkt = cls.flow_provider.\
            search_tickets_in_queue_views(
                zendesk_view_id=[cls.flow_hybrid_int_smb_id],
                ticket_number=zd_low_tkt.id)

    @attr(type='smoke', module='zendesk')
    def test_zendesk_queue_name(self):
        self.assertEqual(
            self.flow_no_priority_tkt.queue, 'Hybrid - International SMB',
            'Expected queue name is Hybrid - International SMB and actual'
            'is {0}'.format(self.flow_no_priority_tkt.queue))

    @attr(type='smoke', module='zendesk')
    def test_assignee_name(self):
        """
        @summary: The Assigned  ZD ticket should have correct assignee name
        """
        self.assertEqual(
            self.flow_high_tkt.assignee, self.testuser4_user_name,
            'Expected assignee is {0} and actual is {1}'.format(
                self.testuser4_user_name, self.flow_high_tkt.assignee))

    @attr(type='smoke', module='zendesk')
    def test_high_priority_ticket(self):
        """
        @summary: High ZD ticket should have correct priority in Flow
        """
        self.assertEqual(
            self.flow_high_tkt.severity, TicketConst.severity_level_2,
            'Expected priority is {0} and acutal is{1}'.format(
                TicketConst.severity_level_2, self.flow_high_tkt.severity))
        self.assertEqual(
            self.flow_high_tkt.severity_display.lower(),
            TicketConst.zd_severity_high, 'Expected priority is {0} and actual'
            'is {1}'.format(TicketConst.zd_severity_high,
                            self.flow_high_tkt.severity_display.lower()))

    @attr(type='smoke', module='zendesk')
    def test_urgent_priority_ticket(self):
        """
        @summary: Urgent ZD ticket should have correct priority in Flow
        """
        self.assertEqual(
            self. flow_urgent_tkt.severity, TicketConst.severity_level_1,
            'Expected priority is {0} and actual is {1}'.format(
                TicketConst.severity_level_1, self.flow_urgent_tkt.severity))
        self.assertEqual(
            self.flow_urgent_tkt.severity_display.lower(),
            TicketConst.zd_severity_urgent, 'Expected priority is {0} and'
            'actual is {1}'.format(
                TicketConst.zd_severity_urgent,
                self.flow_urgent_tkt.severity_display.lower()))

    @attr(type='smoke', module='zendesk')
    def test_low_priority_ticket(self):
        """
        @summary: Low priority ZD ticket should have correct priority in Flow
        """
        self.assertEqual(
            self.flow_low_tkt.severity, TicketConst.severity_level_4,
            'Expected priority is {0} and actual is {1}'.format(
                TicketConst.severity_level_4, self.flow_low_tkt.severity))
        self.assertEqual(
            self.flow_low_tkt.severity_display.lower(),
            TicketConst.zd_severity_low, 'Expected priority:{0} actual:{1}'.
            format(TicketConst.zd_severity_low,
                   self.flow_low_tkt.severity_display.lower()))

    @attr(type='smoke', module='zendesk')
    def test_no_priority_ticket(self):
        """
        @summary:The ZD ticket with no priority should have
        Normal as their priority in flow
        """
        self.assertEqual(
            self.flow_no_priority_tkt.severity, TicketConst.severity_level_3,
            'Expected priority is {0} and actual is {1}'.format(
                TicketConst.severity_level_3,
                self.flow_no_priority_tkt.severity))
        self.assertEqual(
            self.flow_no_priority_tkt.severity_display.lower(),
            TicketConst.zd_severity_normal, 'Expected priority is {0} and'
            'actual is {1}'.format(
                TicketConst.zd_severity_normal,
                self.flow_no_priority_tkt.severity_display.lower()))

    @attr(type='smoke', module='zendesk')
    def test_open_ticket_status_details(self):
        """
        @summary: The ZD ticket with Open status should have correct
        status and state in Flow
        """
        self.assertEqual(
            self.flow_urgent_tkt.status.lower(), TicketConst.zd_status_open,
            'Expected priority is {0} and actual is {1}'.
            format(TicketConst.zd_status_open,
                   self.flow_urgent_tkt.status.lower()))
        self.assertEqual(
            self.flow_urgent_tkt.state.lower(), TicketConst.flow_state_active,
            'Expected priority is {0} and actual is {1}'.format(
                TicketConst.flow_state_active,
                self.flow_urgent_tkt.state.lower()))

    @attr(type='smoke', module='zendesk')
    def test_pending_ticket_status_details(self):
        """
        @summary: The ZD ticket with pending status should have correct
        status and state in Flow
        """
        self.assertEqual(
            self.flow_low_tkt.status.lower(), TicketConst.zd_status_pending,
            'Expected priority is pending and actual is {0}'.format(
                self.flow_low_tkt.status))
        self.assertEqual(
            self.flow_low_tkt.state.lower(), TicketConst.flow_state_pending,
            'Expected priority is pending and actual is {0}'.format(
                self.flow_low_tkt.state))

    @attr(type='smoke', module='zendesk')
    def test_closed_ticket_presence_in_queue(self):
        """
        @summary: Closed ticket should not be present in ZD Queue view
        """
        zd_closed_ticket = self.flow_provider.search_tickets_in_queue_views(
            zendesk_view_id=[self.flow_hybrid_int_smb_id],
            ticket_number=self.zd_closed_tkt.id)
        self.assertIsNone(zd_closed_ticket, 'Closed ticket# {0} is in the'
                          'queue'.format(self.zd_closed_tkt.id))

    @attr(type='smoke', module='zendesk')
    def test_ticket_with_windows_device(self):
        """
        @summary: ZD ticket with windows should have has_windows
        attribute true
        """
        self.assertTrue(self.flow_high_tkt.has_windows_servers,
                        'Expected value is True but actual is {0}'.format(
                            self.flow_high_tkt.has_windows_servers))

    @attr(type='smoke', module='zendesk')
    def test_ticket_with_linux_device(self):
        """
        @summary: ZD ticket with windows should have has_linux
        attribute true
        """
        self.assertTrue(self.flow_no_priority_tkt.has_linux_servers,
                        'Expected value is True but actual is {0}'.format(
                            self.flow_no_priority_tkt.has_linux_servers))
