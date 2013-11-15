'''
@summary: Test cases classes for Compute Bandwidth tests
@copyright: Copyright (c) 2012-2013 Rackspace US, Inc.
'''
from ccengine.common.decorators import attr
from testrepo.common.testfixtures.stacktach_db_compute_bandwidth_integration \
    import BwBeforeSoftRebootServerFixture, BwAfterSoftRebootServerFixture, \
    BwBeforeAndAfterSoftRebootServerFixture, NoBwSoftRebootServerFixture


class BwBeforeSoftRebootTests(BwBeforeSoftRebootServerFixture):
    '''
    @summary: Checks for bandwidth before a server reboot Soft
    @note:  Only one exists event emitted (periodic)
    '''

    @attr(type="bw")
    def test_bw_before_soft_reboot(self):

        self.assertTrue(self.compute_provider
            .insert_exists_event(
                exists_type='periodic',
                server=self.rebooted_server,
                launched_at=self.launched_at_created_server,
                test_name=self._testMethodName,
                test_type=self.test_type,
                gb_file_size=self.gb_file_size),
            msg="Failed to insert periodic exists event into DB.")


class BwAfterSoftRebootTests(BwAfterSoftRebootServerFixture):
    '''
    @summary: Checks for bandwidth after a server reboot Soft
    @note:  Only one exists event emitted (periodic)
    '''

    @attr(type="bw")
    def test_bw_after_soft_reboot(self):

        self.assertTrue(self.compute_provider
            .insert_exists_event(
                exists_type='periodic',
                server=self.rebooted_server,
                launched_at=self.launched_at_created_server,
                test_name=self._testMethodName,
                test_type=self.test_type,
                gb_file_size=self.gb_file_size),
            msg="Failed to insert periodic exists event into DB.")


class BwBeforeAfterSoftRebootTests(BwBeforeAndAfterSoftRebootServerFixture):
    '''
    @summary: Checks for bandwidth before and after a server reboot Soft
    @note:  Only one exists event emitted (periodic)
    '''

    @attr(type="bw")
    def test_bw_before_and_after_soft_reboot(self):

        self.assertTrue(self.compute_provider
            .insert_exists_event(
                exists_type='periodic',
                server=self.rebooted_server,
                launched_at=self.launched_at_created_server,
                test_name=self._testMethodName,
                test_type=self.test_type,
                gb_file_size=self.gb_file_size * 2),
            msg="Failed to insert periodic exists event into DB.")


class NoBwSoftRebootTests(NoBwSoftRebootServerFixture):
    '''
    @summary: Checks for no bandwidth on a server reboot Soft
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
