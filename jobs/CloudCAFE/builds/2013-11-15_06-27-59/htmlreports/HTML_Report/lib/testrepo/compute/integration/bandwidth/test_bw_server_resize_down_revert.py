'''
@summary: Test cases classes for Compute Bandwidth tests
@copyright: Copyright (c) 2012-2013 Rackspace US, Inc.
'''
from ccengine.common.decorators import attr
from testrepo.common.testfixtures.stacktach_db_compute_bandwidth_integration \
    import (BwBeforeResizeDownRevertServerFixture,
            BwAfterResizeDownRevertServerFixture,
            BwBeforeAndAfterResizeDownRevertServerFixture,
            NoBwResizeDownRevertServerFixture)


class BwBeforeResizeDownRevertTests(BwBeforeResizeDownRevertServerFixture):
    '''
    @summary: Checks for bandwidth before resize down revert on the server
    @note:  Three exists events emitted (2 immediate and periodic)
    '''

    @attr(type="bw_bug")
    def test_bw_before_resize_down_revert(self):

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
                exists_type='immediate',
                server=self.resized_server,
                audit_period_ending=(self
                                     .reverted_expected_audit_period_ending),
                launched_at=self.launched_at_resized_server,
                test_name=self._testMethodName,
                test_type=self.test_type,
                state_description='resize_reverting'),
            msg="Failed to insert immediate exists event into DB.")
        self.assertTrue(self.compute_provider
            .insert_exists_event(
                exists_type='periodic',
                server=self.resized_server,
                launched_at=self.launched_at_reverted_resized_server,
                test_name=self._testMethodName,
                test_type=self.test_type,
                gb_file_size=self.gb_file_size),
            msg="Failed to insert periodic exists event into DB.")


class BwAfterResizeDownRevertTests(BwAfterResizeDownRevertServerFixture):
    '''
    @summary: Checks for bandwidth after resize down revert on the server
    @note:  Three exists events emitted (2 immediate and periodic)
    '''

    @attr(type="bw_bug")
    def test_bw_after_resize_down_revert(self):

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
                exists_type='immediate',
                server=self.resized_server,
                audit_period_ending=(self
                                     .reverted_expected_audit_period_ending),
                launched_at=self.launched_at_resized_server,
                test_name=self._testMethodName,
                test_type=self.test_type,
                state_description='resize_reverting'),
            msg="Failed to insert immediate exists event into DB.")
        self.assertTrue(self.compute_provider
            .insert_exists_event(
                exists_type='periodic',
                server=self.resized_server,
                launched_at=self.launched_at_reverted_resized_server,
                test_name=self._testMethodName,
                test_type=self.test_type,
                gb_file_size=self.gb_file_size),
            msg="Failed to insert periodic exists event into DB.")


class BwBeforeAfterResizeDownRevertTests(
        BwBeforeAndAfterResizeDownRevertServerFixture):
    '''
    @summary: Checks for bandwidth before and after resize down revert
        on the server
    @note:  Three exists events emitted (2 immediate and periodic)
    '''

    @attr(type="bw_bug")
    def test_bw_before_and_after_resize_down_revert(self):

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
                exists_type='immediate',
                server=self.resized_server,
                audit_period_ending=(self
                                     .reverted_expected_audit_period_ending),
                launched_at=self.launched_at_resized_server,
                test_name=self._testMethodName,
                test_type=self.test_type,
                state_description='resize_reverting'),
            msg="Failed to insert immediate exists event into DB.")
        self.assertTrue(self.compute_provider
            .insert_exists_event(
                exists_type='periodic',
                server=self.resized_server,
                launched_at=self.launched_at_reverted_resized_server,
                test_name=self._testMethodName,
                test_type=self.test_type,
                gb_file_size=self.gb_file_size * 2),
            msg="Failed to insert periodic exists event into DB.")


class NoBwResizeDownRevertTests(NoBwResizeDownRevertServerFixture):
    '''
    @summary: Checks for no bandwidth on resize down revert server only
    @note:  Three exists events emitted (2 immediate and periodic)
    '''

    @attr(type="bw_bug")
    def test_no_bw_resize_down_revert(self):

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
                exists_type='immediate',
                server=self.resized_server,
                audit_period_ending=(self
                                     .reverted_expected_audit_period_ending),
                launched_at=self.launched_at_resized_server,
                test_name=self._testMethodName,
                test_type=self.test_type,
                state_description='resize_reverting'),
            msg="Failed to insert immediate exists event into DB.")
        self.assertTrue(self.compute_provider
            .insert_exists_event(
                exists_type='periodic',
                server=self.resized_server,
                launched_at=self.launched_at_reverted_resized_server,
                test_name=self._testMethodName,
                test_type=self.test_type,
                gb_file_size=0),
            msg="Failed to insert periodic exists event into DB.")
