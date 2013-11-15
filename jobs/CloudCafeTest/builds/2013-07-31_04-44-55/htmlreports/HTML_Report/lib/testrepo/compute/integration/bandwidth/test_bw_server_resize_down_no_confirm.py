'''
@summary: Test cases classes for Compute Bandwidth tests
@copyright: Copyright (c) 2012-2013 Rackspace US, Inc.
'''
from ccengine.common.decorators import attr
from testrepo.common.testfixtures.stacktach_db_compute_bandwidth_integration \
    import BwBeforeResizeDownNoConfirmServerFixture as \
    BwBeforeResizeDownNCServerFixture, \
    BwAfterResizeDownNoConfirmServerFixture as \
    BwAfterResizeDownNCServerFixture, \
    BwBeforeAndAfterResizeDownNoConfirmServerFixture as \
    BwBAndAResizeDownNCServerFixture, \
    NoBwResizeDownNoConfirmServerFixture as NoBwResizeDownNCServerFixture


class BwBeforeResizeDownNoConfirmTests(BwBeforeResizeDownNCServerFixture):
    '''
    @summary: Checks for bandwidth before resize down unconfirmed
        on the server
    @note:  Two exists events emitted (immediate and periodic)
    '''

    @classmethod
    def setUpClass(cls):
        super(BwBeforeResizeDownNoConfirmTests, cls).setUpClass()

    @attr(type="bw")
    def test_bw_before_resize_down_no_confirm(self):

        self.assertTrue(self.compute_provider
            .insert_exists_event(
                exists_type='immediate',
                server=self.created_server,
                audit_period_ending=self.expected_audit_period_ending,
                launched_at=self.launched_at_created_server,
                test_name=self._testMethodName,
                test_type=self.test_type,
                state_description='resize_prep'),
            msg="Failed to insert immediate exists event into DB.")
        self.assertTrue(self.compute_provider
            .insert_exists_event(
                exists_type='periodic',
                server=self.resized_server,
                launched_at=self.launched_at_resized_server,
                test_name=self._testMethodName,
                test_type=self.test_type,
                gb_file_size=self.gb_file_size),
            msg="Failed to insert periodic exists event into DB.")


class BwAfterResizeDownNoConfirmTests(BwAfterResizeDownNCServerFixture):
    '''
    @summary: Checks for bandwidth after resize down unconfirmed
        on the server
    @note:  Two exists events emitted (immediate and periodic)
    '''

    @classmethod
    def setUpClass(cls):
        super(BwAfterResizeDownNoConfirmTests, cls).setUpClass()

    @attr(type="bw")
    def test_bw_after_resize_down_no_confirm(self):

        self.assertTrue(self.compute_provider
            .insert_exists_event(
                exists_type='immediate',
                server=self.created_server,
                audit_period_ending=self.expected_audit_period_ending,
                launched_at=self.launched_at_created_server,
                test_name=self._testMethodName,
                test_type=self.test_type,
                state_description='resize_prep'),
            msg="Failed to insert immediate exists event into DB.")
        self.assertTrue(self.compute_provider
            .insert_exists_event(
                exists_type='periodic',
                server=self.resized_server,
                launched_at=self.launched_at_resized_server,
                test_name=self._testMethodName,
                test_type=self.test_type,
                gb_file_size=self.gb_file_size),
            msg="Failed to insert periodic exists event into DB.")


class BwBeforeAfterResizeDownNoConfirmTests(BwBAndAResizeDownNCServerFixture):
    '''
    @summary: Checks for bandwidth before and after resize down unconfirmed
        on the server
    @note:  Two exists events emitted (immediate and periodic)
    '''

    @classmethod
    def setUpClass(cls):
        super(BwBeforeAfterResizeDownNoConfirmTests, cls).setUpClass()

    @attr(type="bw")
    def test_bw_before_and_after_resize_down_no_confirm(self):

        self.assertTrue(self.compute_provider
            .insert_exists_event(
                exists_type='immediate',
                server=self.created_server,
                audit_period_ending=self.expected_audit_period_ending,
                launched_at=self.launched_at_created_server,
                test_name=self._testMethodName,
                test_type=self.test_type,
                state_description='resize_prep'),
            msg="Failed to insert immediate exists event into DB.")
        self.assertTrue(self.compute_provider
            .insert_exists_event(
                exists_type='periodic',
                server=self.resized_server,
                launched_at=self.launched_at_resized_server,
                test_name=self._testMethodName,
                test_type=self.test_type,
                gb_file_size=self.gb_file_size * 2),
            msg="Failed to insert periodic exists event into DB.")


class NoBwResizeDownNoConfirmTests(NoBwResizeDownNCServerFixture):
    '''
    @summary: Checks for no bandwidth on resize down unconfirmed
        on the server only
    @note:  Two exists events emitted (immediate and periodic)
    '''

    @classmethod
    def setUpClass(cls):
        super(NoBwResizeDownNoConfirmTests, cls).setUpClass()

    @attr(type="bw")
    def test_no_bw_resize_down_no_confirm(self):

        self.assertTrue(self.compute_provider
            .insert_exists_event(
                exists_type='immediate',
                server=self.created_server,
                audit_period_ending=self.expected_audit_period_ending,
                launched_at=self.launched_at_created_server,
                test_name=self._testMethodName,
                test_type=self.test_type,
                state_description='resize_prep'),
            msg="Failed to insert immediate exists event into DB.")
        self.assertTrue(self.compute_provider
            .insert_exists_event(
                exists_type='periodic',
                server=self.resized_server,
                launched_at=self.launched_at_resized_server,
                test_name=self._testMethodName,
                test_type=self.test_type,
                gb_file_size=0),
            msg="Failed to insert periodic exists event into DB.")
