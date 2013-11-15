'''
@summary: Test cases classes for Compute Bandwidth tests
@copyright: Copyright (c) 2012-2013 Rackspace US, Inc.
'''
from ccengine.common.decorators import attr
from testrepo.common.testfixtures.stacktach_db_compute_bandwidth_integration \
    import BwCreateServerFixture, NoBwCreateServerFixture


class BwCreateServerTests(BwCreateServerFixture):
    '''
    @summary: Checks for bandwidth after a server create
    @note: there is no immediate exists event; only applies for
        server rebuild, resize and, soon, rescue
    @todo:  Check for immediate events in AtomHopper; it can be done here
        or in the test fixture / test provider
    '''

    @attr(type="bw")
    def test_bw_create(self):

        self.assertTrue(self.compute_provider
            .insert_exists_event(
                exists_type='periodic',
                server=self.created_server,
                launched_at=self.launched_at_created_server,
                test_name=self._testMethodName,
                test_type=self.test_type,
                gb_file_size=self.gb_file_size),
            msg="Failed to insert periodic exists event into DB.")


class NoBwCreateServerTests(NoBwCreateServerFixture):
    '''
    @summary: Checks for no bandwidth after a server create
    @note: there is no immediate exists event; only applies for
        server rebuild, resize and, soon, rescue
    @todo:  Check for immediate events in AtomHopper; it can be done here
        or in the test fixture / test provider
    '''

    @attr(type="bw")
    def test_no_bw_create(self):

        self.assertTrue(self.compute_provider
            .insert_exists_event(
                exists_type='periodic',
                server=self.created_server,
                launched_at=self.launched_at_created_server,
                test_name=self._testMethodName,
                test_type=self.test_type,
                gb_file_size=0),
            msg="Failed to insert periodic exists event into DB.")
