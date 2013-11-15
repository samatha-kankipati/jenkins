'''
@summary: Test cases classes for Compute Bandwidth tests
@copyright: Copyright (c) 2012-2013 Rackspace US, Inc.
'''
from ccengine.common.decorators import attr
from testrepo.common.testfixtures.stacktach_db_compute_bandwidth_integration \
    import BwBeforeRescueServerFixture, BwAfterRescueServerFixture, \
    BwBeforeAndAfterRescueServerFixture, NoBwRescueServerFixture


class BwBeforeRescueTests(BwBeforeRescueServerFixture):
    '''
    @summary: Checks for bandwidth before rescue on the server
    @note:  Only one exists event emitted (periodic)
    '''

    @attr(type="bw")
    def test_bw_before_rescue(self):

        self.assertTrue(self.compute_provider
            .insert_exists_event(
                exists_type='periodic',
                server=self.rescued_server,
                launched_at=self.launched_at_created_server,
                test_name=self._testMethodName,
                test_type=self.test_type,
                gb_file_size=self.gb_file_size),
            msg="Failed to insert periodic exists event into DB.")


class BwAfterRescueTests(BwAfterRescueServerFixture):
    '''
    @summary: Checks for bandwidth after rescue on the server
    @note:  Only one exists event emitted (periodic)
    '''

    @attr(type="bw")
    def test_bw_after_rescue(self):

        self.assertTrue(self.compute_provider
            .insert_exists_event(
                exists_type='periodic',
                server=self.rescued_server,
                launched_at=self.launched_at_created_server,
                test_name=self._testMethodName,
                test_type=self.test_type,
                gb_file_size=self.gb_file_size),
            msg="Failed to insert periodic exists event into DB.")


class BwBeforeAfterRescueTests(BwBeforeAndAfterRescueServerFixture):
    '''
    @summary: Checks for bandwidth before and after rescuing server
    @note:  Only one exists event emitted (periodic)
    '''

    @attr(type="bw")
    def test_bw_before_and_after_rescue(self):

        self.assertTrue(self.compute_provider
            .insert_exists_event(
                exists_type='periodic',
                server=self.rescued_server,
                launched_at=self.launched_at_created_server,
                test_name=self._testMethodName,
                test_type=self.test_type,
                gb_file_size=self.gb_file_size * 2),
            msg="Failed to insert periodic exists event into DB.")


class NoBwRescueTests(NoBwRescueServerFixture):
    '''
    @summary: Checks for no bandwidth on rescue server only
    @note:  Only one exists event emitted (periodic)
    '''

    @attr(type="bw")
    def test_no_bw_rescue(self):

        self.assertTrue(self.compute_provider
            .insert_exists_event(
                exists_type='periodic',
                server=self.rescued_server,
                launched_at=self.launched_at_created_server,
                test_name=self._testMethodName,
                test_type=self.test_type,
                gb_file_size=0),
            msg="Failed to insert periodic exists event into DB.")
