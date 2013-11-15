from testrepo.common.testfixtures.load_balancers import \
    LoadBalancersAssertUsageFixture
from ccengine.domain.types import LoadBalancerSslModes as LBSModes, \
    LoadBalancerAtomHopperEvents as LBAHE, \
    LoadBalancerAtomHopperStatusTypes as LBAHST
from ccengine.common.decorators import attr
from testrepo.lbaas.usage import UsageKeys
import ConfigParser
import testrepo.lbaas.usage.assertion.atomhopper.assert_helpers as helpers
import testrepo.lbaas.usage.assertion as assertion_utils


class TestEvents(LoadBalancersAssertUsageFixture):

    @classmethod
    def setUpClass(cls):
        super(TestEvents, cls).setUpClass()
        cls.usage_data = ConfigParser.ConfigParser()
        path = '/'.join([UsageKeys.USAGE_DATA_PATH, UsageKeys.EVENTS_FILENAME])
        cls.usage_data.read(path)

    @classmethod
    def tearDownClass(cls):
        super(TestEvents, cls).tearDownClass()

    @attr('assert_usage')
    def test_create_delete_events(self):
        """Check create and delete events."""
        section = 'test_create_delete_events'
        if not self.usage_data.has_section(section):
            return
        lb_id = assertion_utils.get_usage_data(self.usage_data, section, UsageKeys.LOAD_BALANCER_ID_FIELD)
        records = self.ah_provider.events_by_resource_id(lb_id)
        is_contiguous = helpers.are_records_contiguous(records)
        self.assertTrue(is_contiguous.result, 'The was a gap in the record: '
                        '{0} != {1}'.format(is_contiguous.time1,
                                            is_contiguous.time2))
        self.assertGreater(len(records), 1,
                           'There should only be 2-3 records.')
        self.assertLessEqual(len(records), 3,
                             'There should only be 2-3 records.')
        records = records[::-1]
        self.assertEquals(records[1].type, LBAHE.DELETE,
                          'The last record should be a DELETE event.')

    @attr('assert_usage')
    def test_virtual_ips(self):
        """Assert CREATE_VIRTUAL_IP and DELETE_VIRTUAL_IP events occur."""
        section = 'test_virtual_ips'
        if not self.usage_data.has_section(section):
            return
        lb_id = assertion_utils.get_usage_data(self.usage_data, section, UsageKeys.LOAD_BALANCER_ID_FIELD)
        records = self.ah_provider.events_by_resource_id(lb_id)
        is_contiguous = helpers.are_records_contiguous(records)
        self.assertTrue(is_contiguous.result, 'The was a gap in the record: '
                        '{0} != {1}'.format(is_contiguous.time1,
                                            is_contiguous.time2))
        self.assertTrue(helpers.recent_record_has_correct_time(records),
                        'Most recent record did not have the latest '
                        'timestamp.')

        records = records[::-1]
        num_vips_order = [1, 2, 1]
        helpers.verify_records(records, num_vips_order=num_vips_order)

    @attr('assert_usage')
    def test_ssl_termination_events(self):
        """Assert ssl termination events."""
        section = 'test_ssl_termination_events'
        if not self.usage_data.has_section(section):
            return
        lb_id = assertion_utils.get_usage_data(self.usage_data, section, UsageKeys.LOAD_BALANCER_ID_FIELD)
        records = self.ah_provider.events_by_resource_id(lb_id)
        is_contiguous = helpers.are_records_contiguous(records)
        self.assertTrue(is_contiguous.result, 'The was a gap in the record: '
                        '{0} != {1}'.format(is_contiguous.time1,
                                            is_contiguous.time2))

        records = records[::-1]
        mode_order = [LBSModes.OFF, LBSModes.ON, LBSModes.MIXED, LBSModes.OFF]

        helpers.verify_records(records, mode_order=mode_order)

    @attr('assert_usage')
    def test_suspension_events(self):
        """Assert suspension events were created."""
        section = 'test_suspension_events'
        if not self.usage_data.has_section(section):
            return
        lb_id = assertion_utils.get_usage_data(self.usage_data, section, UsageKeys.LOAD_BALANCER_ID_FIELD)
        records = self.ah_provider.events_by_resource_id(lb_id)
        is_contiguous = helpers.are_records_contiguous(records)
        self.assertTrue(is_contiguous.result, 'The was a gap in the record: '
                        '{0} != {1}'.format(is_contiguous.time1,
                                            is_contiguous.time2))
        records = records[::-1]
        status_order = [LBAHST.ACTIVE, LBAHST.SUSPENDED, LBAHST.ACTIVE]

        helpers.verify_records(records, status_order=status_order)

    @attr('assert_usage')
    def test_delete_lb_while_ssl_only_on(self):
        """Assert SSL_OFF didn't occur after SSL_ONLY_ON on LB delete."""
        section = 'test_delete_lb_while_ssl_only_on'
        if not self.usage_data.has_section(section):
            return
        lb_id = assertion_utils.get_usage_data(self.usage_data, section, UsageKeys.LOAD_BALANCER_ID_FIELD)
        records = self.ah_provider.events_by_resource_id(lb_id)
        is_contiguous = helpers.are_records_contiguous(records)
        self.assertTrue(is_contiguous.result, 'The was a gap in the record: '
                        '{0} != {1}'.format(is_contiguous.time1,
                                            is_contiguous.time2))

        records = records[::-1]
        mode_order = [LBSModes.OFF, LBSModes.ON]
        last_record = records.pop()

        helpers.verify_records(records, mode_order=mode_order)
        self.assertEquals(LBAHE.DELETE, last_record.type, "The last record"
                          "should be a DELETE event type.")

    @attr('assert_usage')
    def test_delete_lb_while_ssl_mixed_on(self):
        """Assert SSL_OFF didn't occur after SSL_MIXED_ON on LB delete."""
        section = 'test_delete_lb_while_ssl_mixed_on'
        if not self.usage_data.has_section(section):
            return
        lb_id = assertion_utils.get_usage_data(self.usage_data, section, UsageKeys.LOAD_BALANCER_ID_FIELD)
        records = self.ah_provider.events_by_resource_id(lb_id)
        is_contiguous = helpers.are_records_contiguous(records)
        self.assertTrue(is_contiguous.result, 'The was a gap in the record: '
                        '{0} != {1}'.format(is_contiguous.time1,
                                            is_contiguous.time2))

        records = records[::-1]
        mode_order = [LBSModes.OFF, LBSModes.MIXED]
        last_record = records.pop()

        helpers.verify_records(records, mode_order=mode_order)
        self.assertEquals(LBAHE.DELETE, last_record.type, "The last record"
                          "should be a DELETE event type.")

    @attr('assert_usage')
    def test_delete_lb_while_suspended(self):
        """Assert UNSUSPEND event didn't occur after suspended LB deletion."""
        section = 'test_delete_lb_while_suspended'
        if not self.usage_data.has_section(section):
            return
        lb_id = assertion_utils.get_usage_data(self.usage_data, section, UsageKeys.LOAD_BALANCER_ID_FIELD)
        records = self.ah_provider.events_by_resource_id(lb_id)
        is_contiguous = helpers.are_records_contiguous(records)
        self.assertTrue(is_contiguous.result, 'The was a gap in the record: '
                        '{0} != {1}'.format(is_contiguous.time1,
                                            is_contiguous.time2))

        records = records[::-1]
        status_order = [LBAHST.ACTIVE, LBAHST.SUSPENDED]
        last_record = records.pop()

        helpers.verify_records(records, status_order=status_order)
        self.assertEquals(LBAHE.DELETE, last_record.type, "The last record"
                          "should be a DELETE event type.")

    @attr('assert_usage')
    def test_delete_lb_after_adding_virtual_ip(self):
        """Assert DELETE_VIRTUAL_IP event didn't occur after LB deletion."""
        section = 'test_delete_lb_after_adding_virtual_ip'
        if not self.usage_data.has_section(section):
            return
        lb_id = assertion_utils.get_usage_data(self.usage_data, section, UsageKeys.LOAD_BALANCER_ID_FIELD)
        records = self.ah_provider.events_by_resource_id(lb_id)
        is_contiguous = helpers.are_records_contiguous(records)
        self.assertTrue(is_contiguous.result, 'The was a gap in the record: '
                        '{0} != {1}'.format(is_contiguous.time1,
                                            is_contiguous.time2))

        records = records[::-1]
        num_vips_order = [1, 2]
        last_record = records.pop()

        helpers.verify_records(records, num_vips_order=num_vips_order)
        self.assertEquals(LBAHE.DELETE, last_record.type, "The last record"
                          "should be a DELETE event type.")
