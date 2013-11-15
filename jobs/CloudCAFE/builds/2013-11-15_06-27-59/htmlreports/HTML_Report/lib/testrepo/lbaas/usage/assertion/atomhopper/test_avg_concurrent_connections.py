from testrepo.common.testfixtures.load_balancers import \
                                            LoadBalancersAssertUsageFixture
from ccengine.common.decorators import attr
from testrepo.lbaas.usage import UsageKeys
import testrepo.lbaas.usage.assertion.atomhopper.assert_helpers as helpers
from ccengine.domain.types import LoadBalancerSslModes as LBSModes
import testrepo.lbaas.usage.assertion as assertion_utils
import unittest
import ConfigParser


class TestAvgConcurrentConnections(LoadBalancersAssertUsageFixture):

    @classmethod
    def setUpClass(cls):
        super(TestAvgConcurrentConnections, cls).setUpClass()
        cls.usage_data = ConfigParser.ConfigParser()
        path = '/'.join([UsageKeys.USAGE_DATA_PATH, UsageKeys.ACC_FILENAME])
        cls.usage_data.read(path)

    @classmethod
    def tearDownClass(cls):
        super(TestAvgConcurrentConnections, cls).tearDownClass()

    @attr('assert_usage')
    def test_average_concurrent_connections(self):
        '''Assert average concurrent connections.'''
        section = 'test_average_concurrent_connections'
        if not self.usage_data.has_section(section):
            return
        lb_id = assertion_utils.get_usage_data(self.usage_data, section, UsageKeys.LOAD_BALANCER_ID_FIELD)
        con_conn = int(assertion_utils.get_usage_data(self.usage_data, section,
                                           UsageKeys.AVERAGE_NUM_CONNECTIONS))
        records = self.ah_provider.events_by_resource_id(lb_id)
        is_contiguous = helpers.are_records_contiguous(records)
        self.assertTrue(is_contiguous.result, 'The was a gap in the record: '\
                        + str(is_contiguous.time1) + ' != ' + \
                        str(is_contiguous.time2))
        self.assertTrue(helpers.recent_record_has_correct_time(records),
                    'Most recent record did not have the latest timestamp.')

        rev_records = records[::-1]

        acc_order = [con_conn]
        bandwidth_order = [-1]

        try:
            helpers.verify_records(rev_records, acc_order=acc_order,
                                   bandwidth_out_order=bandwidth_order,
                                   bandwidth_in_order=bandwidth_order,
                                   bandwidth_out_ssl_order=bandwidth_order,
                                   bandwidth_in_ssl_order=bandwidth_order)
        #Sometimes the ACC's can be on the 2nd record
        except AssertionError as e:
            rev_records.pop(0)
            helpers.verify_records(rev_records, acc_order=acc_order,
                                   bandwidth_out_order=bandwidth_order,
                                   bandwidth_in_order=bandwidth_order,
                                   bandwidth_out_ssl_order=bandwidth_order,
                                   bandwidth_in_ssl_order=bandwidth_order)

    @attr('assert_usage')
    def test_average_concurrent_connections_ssl(self):
        '''Assert SSL average concurrent connections.'''
        section = 'test_average_concurrent_connections_ssl'
        if not self.usage_data.has_section(section):
            return
        lb_id = assertion_utils.get_usage_data(self.usage_data, section, UsageKeys.LOAD_BALANCER_ID_FIELD)
        con_conn = int(assertion_utils.get_usage_data(self.usage_data, section,
                                           UsageKeys.AVERAGE_NUM_CONNECTIONS))
        records = self.ah_provider.events_by_resource_id(lb_id)
        is_contiguous = helpers.are_records_contiguous(records)
        self.assertTrue(is_contiguous.result, 'The was a gap in the record: '\
                        + str(is_contiguous.time1) + ' != ' + \
                        str(is_contiguous.time2))
        self.assertTrue(
            helpers.recent_record_has_correct_time(records),
            'Most recent record did not have the latest timestamp.')
        rev_records = records[::-1]

        acc_ssl_order = [con_conn]
        bandwidth_order = [-1]
        mode_order = [LBSModes.OFF, LBSModes.ON]

        try:
            helpers.verify_records(rev_records, acc_ssl_order=acc_ssl_order,
                                   bandwidth_out_order=bandwidth_order,
                                   bandwidth_in_order=bandwidth_order,
                                   bandwidth_out_ssl_order=bandwidth_order,
                                   bandwidth_in_ssl_order=bandwidth_order,
                                   mode_order=mode_order)
        #Sometimes the ACC's can be on the 2nd record
        except AssertionError:
            rev_records.pop(0)
            mode_order.pop(0)
            helpers.verify_records(rev_records, acc_ssl_order=acc_ssl_order,
                                   bandwidth_out_order=bandwidth_order,
                                   bandwidth_in_order=bandwidth_order,
                                   bandwidth_out_ssl_order=bandwidth_order,
                                   bandwidth_in_ssl_order=bandwidth_order,
                                   mode_order=mode_order)

    @unittest.skip('Unfinished')
    @attr('generate_usage')
    def test_servicenet_average_concurrent_connections(self):
        '''Generate servicenet average concurrent connections.'''
        pass
