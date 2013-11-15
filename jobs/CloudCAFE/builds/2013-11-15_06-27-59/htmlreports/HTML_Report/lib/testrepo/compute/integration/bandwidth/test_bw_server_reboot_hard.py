'''
@summary: Test cases classes for Compute Bandwidth tests
@copyright: Copyright (c) 2012-2013 Rackspace US, Inc.
'''
from ccengine.common.decorators import attr
from testrepo.common.testfixtures.stacktach_db_compute_bandwidth_integration \
    import BwBeforeHardRebootServerFixture, BwAfterHardRebootServerFixture, \
    BwBeforeAndAfterHardRebootServerFixture, NoBwHardRebootServerFixture


class BwBeforeHardRebootTests(BwBeforeHardRebootServerFixture):
    '''
    @summary: Checks for bandwidth before a server reboot hard
    @note:  Only one exists event emitted (periodic)
    '''

    @attr(type="bw")
    def test_bw_before_hard_reboot(self):

        self.assertTrue(self.compute_provider
            .insert_exists_event(
                exists_type='periodic',
                server=self.rebooted_server,
                launched_at=self.launched_at_created_server,
                test_name=self._testMethodName,
                test_type=self.test_type,
                gb_file_size=self.gb_file_size),
            msg="Failed to insert periodic exists event into DB.")


class BwAfterHardRebootTests(BwAfterHardRebootServerFixture):
    '''
    @summary: Checks for bandwidth after a server reboot hard
    @note:  Only one exists event emitted (periodic)
    '''

    @attr(type="bw")
    def test_bw_after_hard_reboot(self):

        self.assertTrue(self.compute_provider
            .insert_exists_event(
                exists_type='periodic',
                server=self.rebooted_server,
                launched_at=self.launched_at_created_server,
                test_name=self._testMethodName,
                test_type=self.test_type,
                gb_file_size=self.gb_file_size),
            msg="Failed to insert periodic exists event into DB.")


class BwBeforeAfterHardRebootTests(BwBeforeAndAfterHardRebootServerFixture):
    '''
    @summary: Checks for bandwidth before and after a server reboot hard
    @note:  Only one exists event emitted (periodic)
    '''

    @attr(type="bw")
    def test_bw_before_and_after_hard_reboot(self):

        self.assertTrue(self.compute_provider
            .insert_exists_event(
                exists_type='periodic',
                server=self.rebooted_server,
                launched_at=self.launched_at_created_server,
                test_name=self._testMethodName,
                test_type=self.test_type,
                gb_file_size=self.gb_file_size * 2),
            msg="Failed to insert periodic exists event into DB.")


class NoBwHardRebootTests(NoBwHardRebootServerFixture):
    '''
    @summary: Checks for no bandwidth on a server reboot hard
    @note:  Only one exists event emitted (periodic)
    '''

    @attr(type="bw")
    def test_no_bw_reboot(self):

        self.assertTrue(self.compute_provider
            .insert_exists_event(
                exists_type='periodic',
                server=self.rebooted_server,
                launched_at=self.launched_at_created_server,
                test_name=self._testMethodName,
                test_type=self.test_type,
                gb_file_size=0),
            msg="Failed to insert periodic exists event into DB.")
