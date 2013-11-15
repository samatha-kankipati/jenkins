from testrepo.common.testfixtures.load_balancers import \
                                            LoadBalancersAssertUsageFixture
from ccengine.common.decorators import attr
from testrepo.lbaas.usage import UsageKeys
from ccengine.domain.types import LoadBalancerSslModes as LBSModes, \
    LoadBalancerAtomHopperStatusTypes as LBAHST, \
    LoadBalancerVirtualIpTypes as VipTypes

import ConfigParser
import testrepo.lbaas.usage.assertion.atomhopper.assert_helpers as helpers
import testrepo.lbaas.usage.assertion as assertion_utils


class TestUptime(LoadBalancersAssertUsageFixture):

    @classmethod
    def setUpClass(cls):
        super(TestUptime, cls).setUpClass()
        cls.usage_data = ConfigParser.ConfigParser()
        path = '/'.join([UsageKeys.USAGE_DATA_PATH, UsageKeys.UPTIME_FILENAME])
        cls.usage_data.read(path)

    @classmethod
    def tearDownClass(cls):
        super(TestUptime, cls).tearDownClass()

    @attr('assert_usage')
    def test_normal_load_balancer_uptime(self):
        '''Assert uptime for a load balancer.'''
        section = 'test_normal_load_balancer_uptime'
        if not self.usage_data.has_section(section):
            return
        lb_id = assertion_utils.get_usage_data(
            self.usage_data, section, UsageKeys.LOAD_BALANCER_ID_FIELD)
        records = self.ah_provider.events_by_resource_id(lb_id)
        is_contiguous = helpers.are_records_contiguous(records)
        self.assertTrue(is_contiguous.result, 'The was a gap in the record: '
                        + str(is_contiguous.time1) + ' != ' +
                        str(is_contiguous.time2))
        self.assertTrue(
            helpers.recent_record_has_correct_time(records),
            'Most recent record did not have the latest timestamp.')

        records = records[::-1]

        helpers.verify_records(records)

    @attr('assert_usage')
    def test_ssl_only_load_balancer_uptime(self):
        '''Assert uptime for an ssl only load balancer.'''
        section = 'test_ssl_only_load_balancer_uptime'
        if not self.usage_data.has_section(section):
            return
        lb_id = assertion_utils.get_usage_data(self.usage_data, section, UsageKeys.LOAD_BALANCER_ID_FIELD)
        records = self.ah_provider.events_by_resource_id(lb_id)
        is_contiguous = helpers.are_records_contiguous(records)
        self.assertTrue(is_contiguous.result, 'The was a gap in the record: '
                        + str(is_contiguous.time1) + ' != ' +
                        str(is_contiguous.time2))
        self.assertTrue(helpers.recent_record_has_correct_time(records),
                    'Most recent record did not have the latest timestamp.')
        self.assertTrue(helpers.recent_record_has_correct_time(records),
                    'Most recent record did not have the latest timestamp.')

        records = records[::-1]
        mode_order = [LBSModes.OFF, LBSModes.ON]

        helpers.verify_records(records, mode_order=mode_order)

    @attr('assert_usage')
    def test_ssl_mixed_load_balancer_uptime(self):
        '''Assert uptime for an ssl mixed load balancer.'''
        section = 'test_ssl_mixed_load_balancer_uptime'
        if not self.usage_data.has_section(section):
            return
        lb_id = assertion_utils.get_usage_data(self.usage_data, section, UsageKeys.LOAD_BALANCER_ID_FIELD)
        records = self.ah_provider.events_by_resource_id(lb_id)
        is_contiguous = helpers.are_records_contiguous(records)
        self.assertTrue(is_contiguous.result, 'The was a gap in the record: '\
                        + str(is_contiguous.time1) + ' != ' + \
                        str(is_contiguous.time2))
        self.assertTrue(helpers.recent_record_has_correct_time(records),
                    'Most recent record did not have the latest timestamp.')
        self.assertTrue(helpers.recent_record_has_correct_time(records),
                    'Most recent record did not have the latest timestamp.')

        records = records[::-1]
        mode_order = [LBSModes.OFF, LBSModes.MIXED]

        helpers.verify_records(records, mode_order=mode_order)

    @attr('assert_usage')
    def test_virtual_ips_uptime(self):
        '''Assert uptime for load balancer with extra virtual ip.'''
        section = 'test_virtual_ips_uptime'
        if not self.usage_data.has_section(section):
            return
        lb_id = assertion_utils.get_usage_data(self.usage_data, section, UsageKeys.LOAD_BALANCER_ID_FIELD)
        num_vips = assertion_utils.get_usage_data(self.usage_data, section, UsageKeys.NUM_VIPS)
        records = self.ah_provider.events_by_resource_id(lb_id)
        is_contiguous = helpers.are_records_contiguous(records)
        self.assertTrue(is_contiguous.result, 'The was a gap in the record: '\
                        + str(is_contiguous.time1) + ' != ' + \
                        str(is_contiguous.time2))
        self.assertTrue(helpers.recent_record_has_correct_time(records),
                    'Most recent record did not have the latest timestamp.')

        records = records[::-1]
        num_vips_order = [1, 2]

        helpers.verify_records(records, num_vips_order=num_vips_order)

    @attr('assert_usage')
    def test_multiple_virtual_ips_uptime(self):
        '''Assert uptime for load balancer with extra virtual ips after CREATE and DELETE vips.'''
        section = 'test_multiple_virtual_ips_uptime'
        if not self.usage_data.has_section(section):
            return
        lb_id = assertion_utils.get_usage_data(self.usage_data, section, UsageKeys.LOAD_BALANCER_ID_FIELD)
        num_vips = assertion_utils.get_usage_data(self.usage_data, section, UsageKeys.NUM_VIPS)
        records = self.ah_provider.events_by_resource_id(lb_id)
        is_contiguous = helpers.are_records_contiguous(records)
        self.assertTrue(is_contiguous.result, 'The was a gap in the record: '\
                        + str(is_contiguous.time1) + ' != ' + \
                        str(is_contiguous.time2))
        self.assertTrue(helpers.recent_record_has_correct_time(records),
                    'Most recent record did not have the latest timestamp.')

        records = records[::-1]
        num_vips_order = [1, 2, 3, 2]

        helpers.verify_records(records, num_vips_order=num_vips_order)

    @attr('assert_usage')
    def test_suspended_uptime(self):
        '''Assert uptime for load balancer in suspended status.'''
        section = 'test_suspended_uptime'
        if not self.usage_data.has_section(section):
            return
        lb_id = assertion_utils.get_usage_data(self.usage_data, section, UsageKeys.LOAD_BALANCER_ID_FIELD)
        records = self.ah_provider.events_by_resource_id(lb_id)
        is_contiguous = helpers.are_records_contiguous(records)
        self.assertTrue(is_contiguous.result, 'The was a gap in the record: '\
                        + str(is_contiguous.time1) + ' != ' + \
                        str(is_contiguous.time2))
        self.assertTrue(helpers.recent_record_has_correct_time(records),
                    'Most recent record did not have the latest timestamp.')

        records = records[::-1]
        status_order = [LBAHST.ACTIVE, LBAHST.SUSPENDED]

        helpers.verify_records(records, status_order=status_order)

    @attr('assert_usage')
    def test_servicenet_load_balancer(self):
        '''Generate servicenet load balancer'''
        section = 'test_servicenet_load_balancer'
        if not self.usage_data.has_section(section):
            return
        lb_id = assertion_utils.get_usage_data(self.usage_data, section, UsageKeys.LOAD_BALANCER_ID_FIELD)
        records = self.ah_provider.events_by_resource_id(lb_id)
        is_contiguous = helpers.are_records_contiguous(records)
        self.assertTrue(is_contiguous.result, 'The was a gap in the record: '\
                        + str(is_contiguous.time1) + ' != ' + \
                        str(is_contiguous.time2))
        self.assertTrue(helpers.recent_record_has_correct_time(records),
                    'Most recent record did not have the latest timestamp.')

        records = records[::-1]
        vip_type_order = [VipTypes.SERVICENET]

        helpers.verify_records(records, vip_type_order=vip_type_order)
