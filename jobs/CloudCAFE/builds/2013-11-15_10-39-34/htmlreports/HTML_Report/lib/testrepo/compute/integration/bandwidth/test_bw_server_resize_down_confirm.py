'''
@summary: Test cases classes for Compute Bandwidth tests
@copyright: Copyright (c) 2012-2013 Rackspace US, Inc.
'''
from ccengine.common.decorators import attr
from testrepo.common.testfixtures.stacktach_db_compute_bandwidth_integration \
    import (BwBeforeResizeDownConfirmServerFixture,
            BwAfterResizeDownConfirmServerFixture,
            BwBeforeAndAfterResizeDownConfirmServerFixture,
            NoBwResizeDownConfirmServerFixture)


class BwBeforeResizeDownConfirmTests(BwBeforeResizeDownConfirmServerFixture):
    '''
    @summary: Checks for bandwidth before resize down confirmed on the server
    @note:  Two exists events emitted (immediate and periodic)
    '''

    @attr(type="bw_bug")
    def test_bw_before_resize_down_confirm(self):

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


class BwAfterResizeDownConfirmTests(BwAfterResizeDownConfirmServerFixture):
    '''
    @summary: Checks for bandwidth after resize down confirmed on the server
    @note:  Two exists events emitted (immediate and periodic)
    '''

    @attr(type="bw_bug")
    def test_bw_after_resize_down_confirm(self):

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


class BwBeforeAfterResizeDownConfirmTests(
        BwBeforeAndAfterResizeDownConfirmServerFixture):
    '''
    @summary: Checks for bandwidth before and after resize down confirmed
        on the server
    @note:  Two exists events emitted (immediate and periodic)
    '''

    @attr(type="bw_bug")
    def test_bw_before_and_after_resize_down_confirm(self):

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


class NoBwResizeDownConfirmTests(NoBwResizeDownConfirmServerFixture):
    '''
    @summary: Checks for no bandwidth on resize down confirmed server only
    @note:  Two exists events emitted (immediate and periodic)
    '''

    @attr(type="bw_bug")
    def test_no_bw_resize_down_confirm(self):

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
