'''
@summary: Test cases classes for Compute Bandwidth tests
@copyright: Copyright (c) 2012-2013 Rackspace US, Inc.
'''
from ccengine.common.decorators import attr
from testrepo.common.testfixtures.stacktach_db_compute_bandwidth_integration \
    import (BwBeforeChangePasswordServerFixture,
            BwAfterChangePasswordServerFixture,
            BwBeforeAndAfterChangePasswordServerFixture,
            NoBwChangePasswordServerFixture)


class BwBeforeChangePasswordTests(BwBeforeChangePasswordServerFixture):
    '''
    @summary: Checks for bandwidth before changing password
        on the server
    @note:  Only one exists event emitted (periodic)
    '''

    @attr(type="bw")
    def test_bw_before_change_password(self):

        self.assertTrue(self.compute_provider
            .insert_exists_event(
                exists_type='periodic',
                server=self.changed_pw_server,
                launched_at=self.launched_at_created_server,
                test_name=self._testMethodName,
                test_type=self.test_type,
                gb_file_size=self.gb_file_size),
            msg="Failed to insert periodic exists event into DB.")


class BwAfterChangePasswordTests(BwAfterChangePasswordServerFixture):
    '''
    @summary: Checks for bandwidth after changing password
        on the server
    @note:  Only one exists event emitted (periodic)
    '''

    @attr(type="bw")
    def test_bw_after_change_password(self):

        self.assertTrue(self.compute_provider
            .insert_exists_event(
                exists_type='periodic',
                server=self.changed_pw_server,
                launched_at=self.launched_at_created_server,
                test_name=self._testMethodName,
                test_type=self.test_type,
                gb_file_size=self.gb_file_size),
            msg="Failed to insert periodic exists event into DB.")


class BwBeforeAfterChangePasswordTests(
        BwBeforeAndAfterChangePasswordServerFixture):
    '''
    @summary: Checks for bandwidth before and after changing
        password on the server
    @note:  Only one exists event emitted (periodic)
    '''

    @attr(type="bw")
    def test_bw_before_and_after_change_password(self):

        self.assertTrue(self.compute_provider
            .insert_exists_event(
                exists_type='periodic',
                server=self.changed_pw_server,
                launched_at=self.launched_at_created_server,
                test_name=self._testMethodName,
                test_type=self.test_type,
                gb_file_size=self.gb_file_size * 2),
            msg="Failed to insert periodic exists event into DB.")


class NoBwChangePasswordTests(NoBwChangePasswordServerFixture):
    '''
    @summary: Checks for no bandwidth on changing password
        on the server
    @note:  Only one exists event emitted (periodic)
    '''

    @attr(type="bw")
    def test_no_bw_change_password(self):

        self.assertTrue(self.compute_provider
            .insert_exists_event(
                exists_type='periodic',
                server=self.changed_pw_server,
                launched_at=self.launched_at_created_server,
                test_name=self._testMethodName,
                test_type=self.test_type,
                gb_file_size=0),
            msg="Failed to insert periodic exists event into DB.")
