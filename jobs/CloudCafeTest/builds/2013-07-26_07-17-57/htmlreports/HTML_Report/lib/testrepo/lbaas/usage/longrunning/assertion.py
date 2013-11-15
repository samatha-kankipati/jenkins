import datetime
from testrepo.common.testfixtures.load_balancers import \
    LoadBalancersAssertUsageFixture
from ccengine.domain.types import LoadBalancerUsageEventTypes as LBUETypes, \
    LoadBalancerSslModes as LBSModes, LoadBalancerVirtualIpTypes as VipTypes
from ccengine.common.decorators import attr
from testrepo.lbaas.usage import UsageKeys
import testrepo.lbaas.usage.assertion as assertion_utils
import ConfigParser
import testrepo.lbaas.usage.generate.generate_helpers as helpers
from testrepo.lbaas.usage import UsageValues
import testrepo.lbaas.usage as usage_helpers


class TestBandwidth(LoadBalancersAssertUsageFixture):

    BANDWIDTH_ACCEPTANCE_RATIO = 0.33
    BANDWIDTH_ZERO_ACCEPTANCE = 1000

    @classmethod
    def setUpClass(cls):
        super(TestBandwidth, cls).setUpClass()
        cls.usage_data = ConfigParser.ConfigParser()
        path = '/'.join([UsageKeys.USAGE_DATA_PATH,
                         UsageKeys.LONGRUNNING_FILENAME])
        cls.usage_data.read(path)

    @classmethod
    def tearDownClass(cls):
        super(TestBandwidth, cls).tearDownClass()

    @attr('assert_long_running')
    def test_normal_bandwidth(self):
        """Assert long running normal bandwidth is correct."""
        self._verify_records(helpers.function_name())

    @attr('assert_long_running')
    def test_ssl_bandwidth(self):
        """Assert long running ssl bandwidth is correct."""
        self._verify_records(helpers.function_name(), ssl_mode=LBSModes.ON)

    @attr('assert_long_running')
    def test_mixed_bandwidth(self):
        """Assert long running ssl bandwidth is correct."""
        self._verify_records(helpers.function_name(), ssl_mode=LBSModes.MIXED)

    def _verify_records(self, section, num_vips=1, ssl_mode=LBSModes.OFF,
                        vip_type=VipTypes.PUBLIC):
        lb_id = assertion_utils.get_usage_data(
            self.usage_data, section, UsageKeys.LOAD_BALANCER_ID_FIELD)
        create_time = assertion_utils.get_usage_data(
            self.usage_data, section, UsageKeys.CREATE_TIME)
        start_time = assertion_utils.get_usage_data(
            self.usage_data, section, UsageKeys.START_TIME)
        start_time = usage_helpers.str_to_datetime(start_time)
        start_time = start_time - datetime.timedelta(hours=1)
        start_time = start_time.isoformat()

        bandwidth_values = self._get_values(section)

        r = self.lbaas_provider.client.list_load_balancer_usage(
            lb_id, startTime=start_time)
        current_records = r.entity.loadBalancerUsageRecords
        r = self.lbaas_provider.client.list_load_balancer_usage(
            lb_id, startTime=create_time)
        all_records = r.entity.loadBalancerUsageRecords

        self._assert_most_recent_values(bandwidth_values, current_records,
                                        num_vips=num_vips, ssl_mode=ssl_mode,
                                        vip_type=vip_type)
        self._assert_total_bandwidth(bandwidth_values, all_records)

    def _get_values(self, section):
        generated_band_out = assertion_utils.get_usage_data(
            self.usage_data, section, UsageKeys.BANDWIDTH_OUT_FIELD)
        generated_band_in = assertion_utils.get_usage_data(
            self.usage_data, section, UsageKeys.BANDWIDTH_IN_FIELD)
        generated_band_out_ssl = assertion_utils.get_usage_data(
            self.usage_data, section, UsageKeys.BANDWIDTH_OUT_SSL_FIELD)
        generated_band_in_ssl = assertion_utils.get_usage_data(
            self.usage_data, section, UsageKeys.BANDWIDTH_IN_SSL_FIELD)
        total_band_out = assertion_utils.get_usage_data(
            self.usage_data, section, UsageKeys.TOTAL_BANDWIDTH_OUT_FIELD)
        total_band_in = assertion_utils.get_usage_data(
            self.usage_data, section, UsageKeys.TOTAL_BANDWIDTH_IN_FIELD)
        total_band_out_ssl = assertion_utils.get_usage_data(
            self.usage_data, section, UsageKeys.TOTAL_BANDWIDTH_OUT_SSL_FIELD)
        total_band_in_ssl = assertion_utils.get_usage_data(
            self.usage_data, section, UsageKeys.TOTAL_BANDWIDTH_IN_SSL_FIELD)
        return UsageValues(bandwidth_out=generated_band_out,
                           bandwidth_in=generated_band_in,
                           bandwidth_out_ssl=generated_band_out_ssl,
                           bandwidth_in_ssl=generated_band_in_ssl,
                           total_bandwidth_in=total_band_in,
                           total_bandwidth_out=total_band_out,
                           total_bandwidth_in_ssl=total_band_in_ssl,
                           total_bandwidth_out_ssl=total_band_out_ssl)

    def _assert_most_recent_values(self, bandwidth_values, current_records,
                                   num_vips=1, ssl_mode=LBSModes.OFF,
                                   vip_type=VipTypes.PUBLIC):
        total_band_in = 0
        total_band_out = 0
        total_band_in_ssl = 0
        total_band_out_ssl = 0
        for record in current_records:
            total_band_in += record.incomingTransfer
            total_band_out += record.outgoingTransfer
            total_band_in_ssl += record.incomingTransferSsl
            total_band_out_ssl += record.outgoingTransferSsl
            if record.eventType != LBUETypes.CREATE_LOADBALANCER:
                self.assertEquals(record.numVips, num_vips)
                self.assertEquals(record.sslMode, ssl_mode)
                self.assertEquals(record.vipType, vip_type)

        band_in_delta = bandwidth_values.bandwidth_in * \
            self.BANDWIDTH_ACCEPTANCE_RATIO
        band_out_delta = bandwidth_values.bandwidth_out * \
            self.BANDWIDTH_ACCEPTANCE_RATIO
        band_in_ssl_delta = bandwidth_values.bandwidth_in_ssl * \
            self.BANDWIDTH_ACCEPTANCE_RATIO
        band_out_ssl_delta = bandwidth_values.bandwidth_out_ssl * \
            self.BANDWIDTH_ACCEPTANCE_RATIO
        self.assertAlmostEqual(
            total_band_in, bandwidth_values.bandwidth_in,
            delta=band_in_delta,
            msg="incomingTransfer not the same as what was generated.")
        self.assertAlmostEqual(
            total_band_out, bandwidth_values.bandwidth_out,
            delta=band_out_delta,
            msg="outgoingTransfer not the same as what was generated.")
        self.assertAlmostEqual(
            total_band_in_ssl, bandwidth_values.bandwidth_in_ssl,
            delta=band_in_ssl_delta,
            msg="incomingTransferSsl not the same as what was generated.")
        self.assertAlmostEqual(
            total_band_out_ssl, bandwidth_values.bandwidth_out_ssl,
            delta=band_out_ssl_delta,
            msg="outgoingTransferSsl not the same as what was generated.")

    def _assert_total_bandwidth(self, bandwidth_values, all_records):
        total_band_in = 0
        total_band_out = 0
        total_band_in_ssl = 0
        total_band_out_ssl = 0
        for record in all_records:
            total_band_in += record.incomingTransfer
            total_band_out += record.outgoingTransfer
            total_band_in_ssl += record.incomingTransferSsl
            total_band_out_ssl += record.outgoingTransferSsl

        band_in_delta = bandwidth_values.bandwidth_in * \
            self.BANDWIDTH_ACCEPTANCE_RATIO
        band_out_delta = bandwidth_values.bandwidth_out * \
            self.BANDWIDTH_ACCEPTANCE_RATIO
        band_in_ssl_delta = bandwidth_values.bandwidth_in_ssl * \
            self.BANDWIDTH_ACCEPTANCE_RATIO
        band_out_ssl_delta = bandwidth_values.bandwidth_out_ssl * \
            self.BANDWIDTH_ACCEPTANCE_RATIO
        self.assertAlmostEqual(
            total_band_in, bandwidth_values.total_bandwidth_in,
            delta=band_in_delta,
            msg="Total incomingTransfer not the same as what has been "
                "generated over the lifetime of the load balancer.")
        self.assertAlmostEqual(
            total_band_out, bandwidth_values.total_bandwidth_out,
            delta=band_out_delta,
            msg="Total outgoingTransfer not the same as what has been "
                "generated over the lifetime of the load balancer.")
        self.assertAlmostEqual(
            total_band_in_ssl, bandwidth_values.total_bandwidth_in_ssl,
            delta=band_in_ssl_delta,
            msg="Total incomingTransferSsl not the same as what has been "
                "generated over the lifetime of the load balancer.")
        self.assertAlmostEqual(
            total_band_out_ssl, bandwidth_values.total_bandwidth_out_ssl,
            delta=band_out_ssl_delta,
            msg="Total outgoingTransferSsl not the same as what has been "
                "generated over the lifetime of the load balancer.")