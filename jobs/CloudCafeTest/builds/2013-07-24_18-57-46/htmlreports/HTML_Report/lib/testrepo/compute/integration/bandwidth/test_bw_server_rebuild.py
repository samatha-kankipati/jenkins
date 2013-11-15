'''
@summary: Test cases classes for Compute Bandwidth tests
@copyright: Copyright (c) 2012-2013 Rackspace US, Inc.
'''
from ccengine.common.decorators import attr
from testrepo.common.testfixtures.stacktach_db_compute_bandwidth_integration \
    import BwBeforeRebuildServerFixture, BwAfterRebuildServerFixture, \
    BwBeforeAndAfterRebuildServerFixture, NoBwRebuildServerFixture


class BwBeforeRebuildTests(BwBeforeRebuildServerFixture):
    '''
    @summary: Checks for bandwidth before a server rebuild
    @todo:  Check for immediate events in AtomHopper; it can be done here
        or in the test fixture / test provider
    @note: audit period ending is when we made the request to rebuild
        or the time when we emitted the immediate exists event
    '''

    @attr(type="bw")
    def test_bw_before_rebuild(self):

        self.assertTrue(self.compute_provider
            .insert_exists_event(
                exists_type='immediate',
                server=self.created_server,
                audit_period_ending=self.expected_audit_period_ending,
                launched_at=self.launched_at_created_server,
                test_name=self._testMethodName,
                test_type=self.test_type,
                state_description='rebuilding'),
            msg="Failed to insert immediate exists event into DB.")
        self.assertTrue(self.compute_provider
            .insert_exists_event(
                exists_type='periodic',
                server=self.rebuilt_server,
                launched_at=self.launched_at_rebuilt_server,
                test_name=self._testMethodName,
                test_type=self.test_type,
                gb_file_size=self.gb_file_size),
            msg="Failed to insert periodic exists event into DB.")


class BwAfterRebuildTests(BwAfterRebuildServerFixture):
    '''
    @summary: Checks for bandwidth after a server rebuild
    @todo:  Check for immediate events in AtomHopper; it can be done here
        or in the test fixture / test provider
    @note: audit period ending is when we made the request to rebuild
        or the time when we emitted the immediate exists event
    '''

    @attr(type="bw")
    def test_bw_after_rebuild(self):

        self.assertTrue(self.compute_provider
            .insert_exists_event(
                exists_type='immediate',
                server=self.created_server,
                audit_period_ending=self.expected_audit_period_ending,
                launched_at=self.launched_at_created_server,
                test_name=self._testMethodName,
                test_type=self.test_type,
                state_description='rebuilding'),
            msg="Failed to insert immediate exists event into DB.")
        self.assertTrue(self.compute_provider
            .insert_exists_event(
                exists_type='periodic',
                server=self.rebuilt_server,
                launched_at=self.launched_at_rebuilt_server,
                test_name=self._testMethodName,
                test_type=self.test_type,
                gb_file_size=self.gb_file_size),
            msg="Failed to insert periodic exists event into DB.")


class BwBeforeAfterRebuildTests(BwBeforeAndAfterRebuildServerFixture):
    '''
    @summary: Checks for bandwidth before and after a server rebuild
    @todo:  Check for immediate events in AtomHopper; it can be done here
        or in the test fixture / test provider
    @note: audit period ending is when we made the request to rebuild
        or the time when we emitted the immediate exists event
    '''

    @attr(type="bw")
    def test_bw_before_and_after_rebuild(self):

        self.assertTrue(self.compute_provider
            .insert_exists_event(
                exists_type='immediate',
                server=self.created_server,
                audit_period_ending=self.expected_audit_period_ending,
                launched_at=self.launched_at_created_server,
                test_name=self._testMethodName,
                test_type=self.test_type,
                state_description='rebuilding'),
            msg="Failed to insert immediate exists event into DB.")
        self.assertTrue(self.compute_provider
            .insert_exists_event(
                exists_type='periodic',
                server=self.rebuilt_server,
                launched_at=self.launched_at_rebuilt_server,
                test_name=self._testMethodName,
                test_type=self.test_type,
                gb_file_size=self.gb_file_size * 2),
            msg="Failed to insert periodic exists event into DB.")


class NoBwRebuildTests(NoBwRebuildServerFixture):
    '''
    @summary: Checks for no bandwidth on a server rebuild
    @todo:  Check for immediate events in AtomHopper; it can be done here
        or in the test fixture / test provider
    @note: audit period ending is when we made the request to rebuild
        or the time when we emitted the immediate exists event
    '''

    @attr(type="bw")
    def test_no_bw_rebuild(self):

        self.assertTrue(self.compute_provider
            .insert_exists_event(
                exists_type='immediate',
                server=self.created_server,
                audit_period_ending=self.expected_audit_period_ending,
                launched_at=self.launched_at_created_server,
                test_name=self._testMethodName,
                test_type=self.test_type,
                state_description='rebuilding'),
            msg="Failed to insert immediate exists event into DB.")
        self.assertTrue(self.compute_provider
            .insert_exists_event(
                exists_type='periodic',
                server=self.rebuilt_server,
                launched_at=self.launched_at_rebuilt_server,
                test_name=self._testMethodName,
                test_type=self.test_type,
                gb_file_size=0),
            msg="Failed to insert periodic exists event into DB.")
