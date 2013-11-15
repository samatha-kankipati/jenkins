from testrepo.common.testfixtures.load_balancers import \
    LoadBalancersAssertUsageFixture
from ccengine.common.decorators import attr
from testrepo.lbaas.usage import UsageKeys
from ccengine.domain.types import LoadBalancerSslModes as LBSModes, \
    LoadBalancerAtomHopperEvents as LBAHE, \
    LoadBalancerAtomHopperStatusTypes as LBAHST
import testrepo.lbaas.usage.assertion.atomhopper.assert_helpers as helpers
from ccengine.domain.types import LoadBalancerVirtualIpTypes as VipTypes
import testrepo.lbaas.usage.assertion as assertion_utils
import unittest2 as unittest
import ConfigParser


class TestBandwidth(LoadBalancersAssertUsageFixture):

    BANDWIDTH_ACCEPTANCE_RATIO = 0.01
    BANDWIDTH_ZERO_ACCEPTANCE = 1000

    @classmethod
    def setUpClass(cls):
        super(TestBandwidth, cls).setUpClass()
        cls.usage_data = ConfigParser.ConfigParser()
        path = '/'.join([UsageKeys.USAGE_DATA_PATH,
                         UsageKeys.BANDWIDTH_FILENAME])
        cls.usage_data.read(path)

    @classmethod
    def tearDownClass(cls):
        super(TestBandwidth, cls).tearDownClass()

    @attr('assert_usage')
    def test_normal_bandwidth(self):
        '''Assert bandwidth generated is correct.'''
        section = 'test_normal_bandwidth'
        if not self.usage_data.has_section(section):
            return
        lb_id = assertion_utils.get_usage_data(self.usage_data, section, UsageKeys.LOAD_BALANCER_ID_FIELD)
        generated_band_out = assertion_utils.get_usage_data(self.usage_data, section,
                                                 UsageKeys.BANDWIDTH_OUT_FIELD)
        generated_band_in = assertion_utils.get_usage_data(self.usage_data, section,
                                                UsageKeys.BANDWIDTH_IN_FIELD)
        records = self.ah_provider.events_by_resourceId(lb_id)
        is_contiguous = helpers.are_records_contiguous(records)
        self.assertTrue(is_contiguous.result, 'The was a gap in the record: '\
                        + str(is_contiguous.time1) + ' != ' + \
                        str(is_contiguous.time2))
        self.assertTrue(
            helpers.recent_record_has_correct_time(records),
            'Most recent record did not have the latest timestamp.')
        generated_band_in = int(generated_band_in)
        generated_band_out = int(generated_band_out)
        rev_records = records[::-1]

        bandwidth_out_order = [generated_band_out]
        bandwidth_in_order = [generated_band_in]
        mode_order = [LBSModes.OFF]

        helpers.verify_records(rev_records, mode_order=mode_order,
                               bandwidth_out_order=bandwidth_out_order,
                               bandwidth_in_order=bandwidth_in_order)

    @attr('assert_usage')
    def test_ssl_termination_secure_traffic_only_bandwidth(self):
        '''Assert ssl only traffic.'''
        section = 'test_ssl_termination_secure_traffic_only_bandwidth'
        if not self.usage_data.has_section(section):
            return
        self._assert_ssl_termination_secure_traffic_only_bandwidth(section)

    @attr('assert_usage')
    def test_ssl_termination_secure_traffic_only_bandwidth_after_poller(self):
        '''Assert ssl only traffic.'''
        section = 'test_ssl_termination_secure_traffic_only_bandwidth_' \
                  'after_poller'
        if not self.usage_data.has_section(section):
            return
        self._assert_ssl_termination_secure_traffic_only_bandwidth(section)

    def _assert_ssl_termination_secure_traffic_only_bandwidth(self, section):
        lb_id = assertion_utils.get_usage_data(self.usage_data, section, UsageKeys.LOAD_BALANCER_ID_FIELD)
        generated_band_out_ssl = assertion_utils.get_usage_data(self.usage_data, section,
                                            UsageKeys.BANDWIDTH_OUT_SSL_FIELD)
        generated_band_in_ssl = assertion_utils.get_usage_data(self.usage_data, section,
                                            UsageKeys.BANDWIDTH_IN_SSL_FIELD)
        records = self.ah_provider.events_by_resourceId(lb_id)
        is_contiguous = helpers.are_records_contiguous(records)
        self.assertTrue(is_contiguous.result, 'The was a gap in the record: '\
                        + str(is_contiguous.time1) + ' != ' + \
                        str(is_contiguous.time2))
        self.assertTrue(
            helpers.recent_record_has_correct_time(records),
            'Most recent record did not have the latest timestamp.')
        generated_band_in_ssl = int(generated_band_in_ssl)
        generated_band_out_ssl = int(generated_band_out_ssl)
        rev_records = records[::-1]

        bandwidth_out_ssl_order = [0, generated_band_out_ssl]
        bandwidth_in_ssl_order = [0, generated_band_in_ssl]
        mode_order = [LBSModes.OFF, LBSModes.ON]

        helpers.verify_records(rev_records, mode_order=mode_order,
                               bandwidth_out_ssl_order=bandwidth_out_ssl_order,
                               bandwidth_in_ssl_order=bandwidth_in_ssl_order)

    @attr('assert_usage')
    def test_ssl_termination_secure_and_normal_bandwidth(self):
        '''Assert ssl and normal bandwidth.'''
        section = 'test_ssl_termination_secure_and_normal_bandwidth'
        if not self.usage_data.has_section(section):
            return
        self._assert_ssl_termination_secure_and_normal_bandwidth(section)

    @attr('assert_usage')
    def test_ssl_termination_secure_and_normal_bandwidth_after_poller(self):
        '''Assert ssl and normal bandwidth after poller.'''
        section = 'test_ssl_termination_secure_and_normal_bandwidth_' \
                  'after_poller'
        if not self.usage_data.has_section(section):
            return
        self._assert_ssl_termination_secure_and_normal_bandwidth(section)

    def _assert_ssl_termination_secure_and_normal_bandwidth(self, section):
        lb_id = assertion_utils.get_usage_data(self.usage_data, section, UsageKeys.LOAD_BALANCER_ID_FIELD)
        generated_band_out = assertion_utils.get_usage_data(self.usage_data, section,
                                                 UsageKeys.BANDWIDTH_OUT_FIELD)
        generated_band_in = assertion_utils.get_usage_data(self.usage_data, section,
                                                UsageKeys.BANDWIDTH_IN_FIELD)
        generated_band_out_ssl = assertion_utils.get_usage_data(self.usage_data, section,
                                            UsageKeys.BANDWIDTH_OUT_SSL_FIELD)
        generated_band_in_ssl = assertion_utils.get_usage_data(self.usage_data, section,
                                            UsageKeys.BANDWIDTH_IN_SSL_FIELD)
        records = self.ah_provider.events_by_resourceId(lb_id)
        is_contiguous = helpers.are_records_contiguous(records)
        self.assertTrue(is_contiguous.result, 'The was a gap in the record: '\
                        + str(is_contiguous.time1) + ' != ' + \
                        str(is_contiguous.time2))
        self.assertTrue(
            helpers.recent_record_has_correct_time(records),
            'Most recent record did not have the latest timestamp.')
        generated_band_in = int(generated_band_in)
        generated_band_out = int(generated_band_out)
        generated_band_in_ssl = int(generated_band_in_ssl)
        generated_band_out_ssl = int(generated_band_out_ssl)
        rev_records = records[::-1]

        bandwidth_out_order = [0, generated_band_out]
        bandwidth_in_order = [0, generated_band_in]
        bandwidth_out_ssl_order = [0, generated_band_out_ssl]
        bandwidth_in_ssl_order = [0, generated_band_in_ssl]
        mode_order = [LBSModes.OFF, LBSModes.MIXED]

        helpers.verify_records(rev_records, mode_order=mode_order,
                               bandwidth_out_order=bandwidth_out_order,
                               bandwidth_in_order=bandwidth_in_order,
                               bandwidth_out_ssl_order=bandwidth_out_ssl_order,
                               bandwidth_in_ssl_order=bandwidth_in_ssl_order)


    @attr('assert_usage')
    def test_normal_bandwidth_after_ssl_modes_toggled(self):
        '''Assert normal bandwidth after toggling ssl modes and back.'''
        section = 'test_normal_bandwidth_after_ssl_modes_toggled'
        if not self.usage_data.has_section(section):
            return
        lb_id = assertion_utils.get_usage_data(self.usage_data, section, UsageKeys.LOAD_BALANCER_ID_FIELD)
        generated_band_out = assertion_utils.get_usage_data(self.usage_data, section,
                                                 UsageKeys.BANDWIDTH_OUT_FIELD)
        generated_band_in = assertion_utils.get_usage_data(self.usage_data, section,
                                                UsageKeys.BANDWIDTH_IN_FIELD)
        records = self.ah_provider.events_by_resourceId(lb_id)
        is_contiguous = helpers.are_records_contiguous(records)
        self.assertTrue(is_contiguous.result, 'The was a gap in the record: '\
                        + str(is_contiguous.time1) + ' != ' + \
                        str(is_contiguous.time2))
        self.assertTrue(
            helpers.recent_record_has_correct_time(records),
            'Most recent record did not have the latest timestamp.')
        generated_band_in = int(generated_band_in)
        generated_band_out = int(generated_band_out)
        rev_records = records[::-1]

        bandwidth_out_order = [0, 0, 0, generated_band_out]
        bandwidth_in_order = [0, 0, 0, generated_band_in]
        mode_order = [LBSModes.OFF, LBSModes.ON, LBSModes.MIXED, LBSModes.OFF]

        helpers.verify_records(rev_records, mode_order=mode_order,
                               bandwidth_out_order=bandwidth_out_order,
                               bandwidth_in_order=bandwidth_in_order)

    @attr('assert_usage')
    def test_normal_bandwidth_after_ssl_mixed(self):
        '''Assert normal bandwidth after ssl mixed.'''
        section = 'test_normal_bandwidth_after_ssl_mixed'
        if not self.usage_data.has_section(section):
            return
        lb_id = assertion_utils.get_usage_data(self.usage_data, section, UsageKeys.LOAD_BALANCER_ID_FIELD)
        generated_band_out = assertion_utils.get_usage_data(self.usage_data, section,
                                                 UsageKeys.BANDWIDTH_OUT_FIELD)
        generated_band_in = assertion_utils.get_usage_data(self.usage_data, section,
                                                UsageKeys.BANDWIDTH_IN_FIELD)
        generated_band_out_ssl = assertion_utils.get_usage_data(self.usage_data, section,
                                            UsageKeys.BANDWIDTH_OUT_SSL_FIELD)
        generated_band_in_ssl = assertion_utils.get_usage_data(self.usage_data, section,
                                            UsageKeys.BANDWIDTH_IN_SSL_FIELD)
        records = self.ah_provider.events_by_resourceId(lb_id)
        is_contiguous = helpers.are_records_contiguous(records)
        self.assertTrue(is_contiguous.result, 'The was a gap in the record: '\
                        + str(is_contiguous.time1) + ' != ' + \
                        str(is_contiguous.time2))
        self.assertTrue(
            helpers.recent_record_has_correct_time(records),
            'Most recent record did not have the latest timestamp.')

        generated_band_in = int(generated_band_in)
        generated_band_out = int(generated_band_out)
        generated_band_in_ssl = int(generated_band_in_ssl)
        generated_band_out_ssl = int(generated_band_out_ssl)
        rev_records = records[::-1]

        bandwidth_out_order = [0, 0, generated_band_out]
        bandwidth_in_order = [0, 0, generated_band_in]
        bandwidth_out_ssl_order = [0, generated_band_out_ssl, 0]
        bandwidth_in_ssl_order = [0, generated_band_in_ssl, 0]
        mode_order = [LBSModes.OFF, LBSModes.MIXED, LBSModes.OFF]

        helpers.verify_records(rev_records, mode_order=mode_order,
                               bandwidth_out_order=bandwidth_out_order,
                               bandwidth_in_order=bandwidth_in_order,
                               bandwidth_out_ssl_order=bandwidth_out_ssl_order,
                               bandwidth_in_ssl_order=bandwidth_in_ssl_order)

    @attr('assert_usage')
    def test_normal_bandwidth_after_unsuspend(self):
        '''Assert bandwidth generated is correct.'''
        section = 'test_normal_bandwidth_after_unsuspend'
        if not self.usage_data.has_section(section):
            return
        lb_id = assertion_utils.get_usage_data(self.usage_data, section, UsageKeys.LOAD_BALANCER_ID_FIELD)
        generated_band_out = assertion_utils.get_usage_data(self.usage_data, section,
                                                 UsageKeys.BANDWIDTH_OUT_FIELD)
        generated_band_in = assertion_utils.get_usage_data(self.usage_data, section,
                                                UsageKeys.BANDWIDTH_IN_FIELD)
        records = self.ah_provider.events_by_resourceId(lb_id)
        is_contiguous = helpers.are_records_contiguous(records)
        self.assertTrue(is_contiguous.result, 'The was a gap in the record: '\
                        + str(is_contiguous.time1) + ' != ' + \
                        str(is_contiguous.time2))
        self.assertTrue(
            helpers.recent_record_has_correct_time(records),
            'Most recent record did not have the latest timestamp.')
        generated_band_in = int(generated_band_in)
        generated_band_out = int(generated_band_out)
        rev_records = records[::-1]

        bandwidth_out_order = [0, 0, generated_band_out]
        bandwidth_in_order = [0, 0, generated_band_in]
        status_order = [LBAHST.ACTIVE, LBAHST.SUSPENDED, LBAHST.ACTIVE]
        helpers.verify_records(rev_records, status_order=status_order,
                               bandwidth_out_order=bandwidth_out_order,
                               bandwidth_in_order=bandwidth_in_order)

    @attr('assert_usage')
    def test_ssl_bandwidth_across_ssl_states(self):
        '''Assert ssl bandwidth after SSL_ONLY_ON, then SSL_OFF, then SSL_ONLY_ON again.'''
        section = 'test_ssl_bandwidth_across_ssl_states'
        if not self.usage_data.has_section(section):
            return
        lb_id = assertion_utils.get_usage_data(self.usage_data, section, UsageKeys.LOAD_BALANCER_ID_FIELD)
        generated_band_out_ssl = float(assertion_utils.get_usage_data(self.usage_data,
            section, UsageKeys.BANDWIDTH_OUT_SSL_FIELD))
        generated_band_in_ssl = float(assertion_utils.get_usage_data(self.usage_data,
            section, UsageKeys.BANDWIDTH_IN_SSL_FIELD))
        generated_band_out_ssl2 = float(assertion_utils.get_usage_data(self.usage_data,
            section, UsageKeys.BANDWIDTH_OUT_SSL_FIELD_2))
        generated_band_in_ssl2 = float(assertion_utils.get_usage_data(self.usage_data,
            section, UsageKeys.BANDWIDTH_IN_SSL_FIELD_2))
        records = self.ah_provider.events_by_resourceId(lb_id)
        is_contiguous = helpers.are_records_contiguous(records)
        self.assertTrue(is_contiguous.result, 'The was a gap in the record: '
                        '{0} != {1}'.format(str(is_contiguous.time1),
                                            str(is_contiguous.time2)))
        self.assertTrue(
            helpers.recent_record_has_correct_time(records),
            'Most recent record did not have the latest timestamp.')
        rev_records = records[::-1]
        mode_order = [LBSModes.OFF, LBSModes.ON, LBSModes.OFF, LBSModes.ON]
        bandwidth_out_ssl_order = [0, generated_band_out_ssl,
                                   0, generated_band_out_ssl2]
        bandwidth_in_ssl_order = [0, generated_band_in_ssl,
                                  0, generated_band_in_ssl2]
        helpers.verify_records(rev_records, mode_order=mode_order,
                               bandwidth_out_ssl_order=bandwidth_out_ssl_order,
                               bandwidth_in_ssl_order=bandwidth_in_ssl_order)

    @attr('assert_usage')
    def test_bandwidth_before_suspend_and_after_unsuspend(self):
        '''Assert bandwidth before suspending a load balancer and also after unsuspending it.'''
        section = 'test_bandwidth_before_suspend_and_after_unsuspend'
        if not self.usage_data.has_section(section):
            return
        self._assert_bandwidth_before_and_after_suspend(section)

    @attr('assert_usage')
    def test_bandwidth_before_suspend_and_after_unsuspend_wait_for_next_poll(self):
        '''Assert bandwidth before suspending a load balancer and also after unsuspending it.'''
        section = 'test_bandwidth_before_suspend_and_after_unsuspend_wait_for_next_poll'
        if not self.usage_data.has_section(section):
            return
        self._assert_bandwidth_before_and_after_suspend(section)

    @attr('assert_usage')
    def test_bandwidth_before_suspend_and_after_unsuspend_wait_after_two_polls(self):
        '''Assert bandwidth before suspending a load balancer and also after unsuspending it.'''
        section = 'test_bandwidth_before_suspend_and_after_unsuspend_wait_after_two_polls'
        if not self.usage_data.has_section(section):
            return
        self._assert_bandwidth_before_and_after_suspend(section)

    def _assert_bandwidth_before_and_after_suspend(self, section):
        lb_id = assertion_utils.get_usage_data(self.usage_data, section, UsageKeys.LOAD_BALANCER_ID_FIELD)
        generated_band_out = float(assertion_utils.get_usage_data(self.usage_data,
            section, UsageKeys.BANDWIDTH_OUT_FIELD))
        generated_band_in = float(assertion_utils.get_usage_data(self.usage_data,
            section, UsageKeys.BANDWIDTH_IN_FIELD))
        generated_band_out2 = float(assertion_utils.get_usage_data(self.usage_data,
            section, UsageKeys.BANDWIDTH_OUT_FIELD_2))
        generated_band_in2 = float(assertion_utils.get_usage_data(self.usage_data,
            section, UsageKeys.BANDWIDTH_IN_FIELD_2))
        records = self.ah_provider.events_by_resourceId(lb_id)
        is_contiguous = helpers.are_records_contiguous(records)
        self.assertTrue(is_contiguous.result, 'The was a gap in the record: '
                        '{0} != {1}'.format(str(is_contiguous.time1),
                                            str(is_contiguous.time2)))
        self.assertTrue(
            helpers.recent_record_has_correct_time(records),
            'Most recent record did not have the latest timestamp.')
        rev_records = records[::-1]
        bandwidth_out_order = [generated_band_out, 0, generated_band_out2]
        bandwidth_in_order = [generated_band_in, 0, generated_band_in2]
        status_order = [LBAHST.ACTIVE, LBAHST.SUSPENDED, LBAHST.ACTIVE]
        helpers.verify_records(rev_records, status_order=status_order,
                               bandwidth_out_order=bandwidth_out_order,
                               bandwidth_in_order=bandwidth_in_order)

    @attr('assert_usage')
    def test_normal_bandwidth_across_ssl_states(self):
        """Assert normal bandwidth across ssl states."""
        section = 'test_normal_bandwidth_across_ssl_states'
        if not self.usage_data.has_section(section):
            return
        lb_id = assertion_utils.get_usage_data(self.usage_data, section, UsageKeys.LOAD_BALANCER_ID_FIELD)
        generated_band_out = float(assertion_utils.get_usage_data(self.usage_data,
            section, UsageKeys.BANDWIDTH_OUT_FIELD))
        generated_band_in = float(assertion_utils.get_usage_data(self.usage_data,
            section, UsageKeys.BANDWIDTH_IN_FIELD))
        generated_band_out2 = float(assertion_utils.get_usage_data(self.usage_data,
            section, UsageKeys.BANDWIDTH_OUT_FIELD_2))
        generated_band_in2 = float(assertion_utils.get_usage_data(self.usage_data,
            section, UsageKeys.BANDWIDTH_IN_FIELD_2))
        generated_band_out3 = float(assertion_utils.get_usage_data(self.usage_data,
            section, UsageKeys.BANDWIDTH_OUT_FIELD_3))
        generated_band_in3 = float(assertion_utils.get_usage_data(self.usage_data,
            section, UsageKeys.BANDWIDTH_IN_FIELD_3))
        records = self.ah_provider.events_by_resourceId(lb_id)
        is_contiguous = helpers.are_records_contiguous(records)
        self.assertTrue(is_contiguous.result, 'The was a gap in the record: '
                        '{0} != {1}'.format(str(is_contiguous.time1),
                                            str(is_contiguous.time2)))
        self.assertTrue(
            helpers.recent_record_has_correct_time(records),
            'Most recent record did not have the latest timestamp.')
        rev_records = records[::-1]
        bandwidth_out_order = [0, generated_band_out, 0, generated_band_out2 +
                               generated_band_out3]
        bandwidth_in_order = [0, generated_band_in, 0, generated_band_in2 +
                              generated_band_in3]
        mode_order = [LBSModes.OFF, LBSModes.MIXED, LBSModes.ON, LBSModes.OFF,
                      LBSModes.OFF]
        helpers.verify_records(rev_records, mode_order=mode_order,
                               bandwidth_out_order=bandwidth_out_order,
                               bandwidth_in_order=bandwidth_in_order)

    @attr('assert_usage')
    def test_bandwidth_on_extra_virtual_ip(self):
        """Assert bandwidth on extra virtual IP is correct."""
        section = 'test_bandwidth_on_extra_virtual_ip'
        if not self.usage_data.has_section(section):
            return
        self._assert_bandwidth_on_extra_virtual_ip(section)

    @attr('assert_usage')
    def test_bandwidth_on_extra_virtual_ip_after_poller(self):
        """Assert bandwidth on extra virtual IP is correct."""
        section = 'test_bandwidth_on_extra_virtual_ip_after_poller'
        if not self.usage_data.has_section(section):
            return
        self._assert_bandwidth_on_extra_virtual_ip(section)

    def _assert_bandwidth_on_extra_virtual_ip(self, section):
        lb_id = assertion_utils.get_usage_data(self.usage_data, section, UsageKeys.LOAD_BALANCER_ID_FIELD)
        generated_band_out = float(assertion_utils.get_usage_data(self.usage_data,
            section, UsageKeys.BANDWIDTH_OUT_FIELD))
        generated_band_in = float(assertion_utils.get_usage_data(self.usage_data,
            section, UsageKeys.BANDWIDTH_IN_FIELD))
        generated_band_out_ssl = float(assertion_utils.get_usage_data(self.usage_data,
            section, UsageKeys.BANDWIDTH_OUT_SSL_FIELD))
        generated_band_in_ssl = float(assertion_utils.get_usage_data(self.usage_data,
            section, UsageKeys.BANDWIDTH_IN_SSL_FIELD))

        records = self.ah_provider.events_by_resourceId(lb_id)
        is_contiguous = helpers.are_records_contiguous(records)
        self.assertTrue(is_contiguous.result, 'The was a gap in the record: '
                        '{0} != {1}'.format(str(is_contiguous.time1),
                                            str(is_contiguous.time2)))
        self.assertTrue(
            helpers.recent_record_has_correct_time(records),
            'Most recent record did not have the latest timestamp.')

        rev_records = records[::-1]
        bandwidth_out_order = [0, generated_band_out, 0]
        bandwidth_in_order = [0, generated_band_in, 0]
        bandwidth_out_ssl_order = [0, 0, generated_band_out_ssl, 0]
        bandwidth_in_ssl_order = [0, 0, generated_band_in_ssl, 0]
        mode_order = [LBSModes.OFF, LBSModes.OFF, LBSModes.ON]
        num_vips_order = [1, 2]
        helpers.verify_records(rev_records, mode_order=mode_order,
                               bandwidth_out_order=bandwidth_out_order,
                               bandwidth_in_order=bandwidth_in_order,
                               bandwidth_out_ssl_order=bandwidth_out_ssl_order,
                               bandwidth_in_ssl_order=bandwidth_in_ssl_order,
                               num_vips_order=num_vips_order)

    @unittest.skip('Unfinished')
    @attr('assert_usage', 'new_usage')
    def test_usage_on_failover_host(self):
        '''Assert bandwidth on a load balancer on a failover host.'''
        pass


