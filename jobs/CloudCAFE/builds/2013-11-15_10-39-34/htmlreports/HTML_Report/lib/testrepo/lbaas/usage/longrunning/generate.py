from testrepo.common.testfixtures.load_balancers import \
    LoadBalancersGenerateUsageFixture
from testrepo.lbaas.usage import UsageKeys
from ccengine.domain.types import LoadBalancerStatusTypes as LBST, \
    LoadBalancerVirtualIpTypes as LBVipTypes, LoadBalancerSslModes as LBSModes
from ccengine.common.decorators import attr
import testrepo.lbaas.usage.generate.generate_helpers as helpers
import ConfigParser
import datetime
import os
import random
import testrepo.lbaas.usage as usage_helpers
from testrepo.lbaas.usage import UsageValues


class TestGenerateLongRunning(LoadBalancersGenerateUsageFixture):

    SSL_SITE_PREFIX = 'sslterm'
    USAGE_POLLER_INTERVAL = 300

    @classmethod
    def setUpClass(cls):
        super(TestGenerateLongRunning, cls).setUpClass()
        cls.usage_data = ConfigParser.ConfigParser()
        path = '/'.join([UsageKeys.USAGE_DATA_PATH,
                         UsageKeys.LONGRUNNING_FILENAME])

        if not os.path.exists(path):
            open(path, 'wb')
        cls.usage_data.read(path)

    @classmethod
    def tearDownClass(cls):
        super(TestGenerateLongRunning, cls).tearDownClass()

    @attr('generate_long_running')
    def test_normal_bandwidth(self):
        """Generate normal bandwidth in and out on an LB - Long Running."""
        section = helpers.function_name()

        start_time = self._get_start_time(section)

        lb = self._create_new_lb_if_last_is_not_active(section)

        vip = lb.get_public_ipv4_vip()

        usage_values = self._get_bandwidth(section)

        self._generate_bandwidth(vip, usage_values,
                                 normal_out=True, normal_in=True,
                                 add_to_current=self._is_same_hour(section))

        self._write_new_values(section, start_time,
                               usage_values.bandwidth_out,
                               usage_values.bandwidth_in,
                               usage_values.bandwidth_out_ssl,
                               usage_values.bandwidth_in_ssl,
                               usage_values.total_bandwidth_in,
                               usage_values.total_bandwidth_out,
                               usage_values.total_bandwidth_in_ssl,
                               usage_values.total_bandwidth_out_ssl,
                               [LBSModes.OFF])

    @attr('generate_long_running')
    def test_ssl_bandwidth(self):
        """Generate ssl bandwidth in and out on an LB - Long Running."""
        section = helpers.function_name()

        start_time = self._get_start_time(section)

        lb = self._create_new_lb_if_last_is_not_active(section)

        if lb.sslTermination is None or not lb.sslTermination.enabled or \
                not lb.sslTermination.secureTrafficOnly:
            self.lbaas_provider.ssl_only_on(lb.id)

        vip = lb.get_public_ipv4_vip()

        usage_values = self._get_bandwidth(section)

        self._generate_bandwidth(vip, usage_values,
                                 ssl_out=True, ssl_in=True,
                                 add_to_current=self._is_same_hour(section))

        self._write_new_values(section, start_time,
                               usage_values.bandwidth_out,
                               usage_values.bandwidth_in,
                               usage_values.bandwidth_out_ssl,
                               usage_values.bandwidth_in_ssl,
                               usage_values.total_bandwidth_in,
                               usage_values.total_bandwidth_out,
                               usage_values.total_bandwidth_in_ssl,
                               usage_values.total_bandwidth_out_ssl,
                               [LBSModes.OFF, LBSModes.ON])

    @attr('generate_long_running')
    def test_mixed_bandwidth(self):
        """Generate mixed bandwidth in and out on an LB - Long Running."""
        section = helpers.function_name()

        start_time = self._get_start_time(section)

        lb = self._create_new_lb_if_last_is_not_active(section)

        if lb.sslTermination is None or not lb.sslTermination.enabled or \
                lb.sslTermination.secureTrafficOnly:
            self.lbaas_provider.ssl_mixed_on(lb.id)

        vip = lb.get_public_ipv4_vip()

        usage_values = self._get_bandwidth(section)

        self._generate_bandwidth(vip, usage_values, normal_out=True,
                                 normal_in=True, ssl_out=True, ssl_in=True,
                                 add_to_current=self._is_same_hour(section))

        self._write_new_values(section, start_time,
                               usage_values.bandwidth_out,
                               usage_values.bandwidth_in,
                               usage_values.bandwidth_out_ssl,
                               usage_values.bandwidth_in_ssl,
                               usage_values.total_bandwidth_in,
                               usage_values.total_bandwidth_out,
                               usage_values.total_bandwidth_in_ssl,
                               usage_values.total_bandwidth_out_ssl,
                               [LBSModes.OFF, LBSModes.MIXED])

    @attr('generate_long_running')
    def test_randomly_changing_ssl_state(self):
        """Generate load balancer bandwidth with random ssl states."""
        section = helpers.function_name()

        start_time = self._get_start_time(section)

        lb = self._create_new_lb_if_last_is_not_active(section)

        ssl_mode_order = self._get_ssl_mode_order(section)

        ssl_only = random.randint(0, 50) == 1
        ssl_mixed = random.randint(0, 50) == 2
        no_ssl = random.randint(0, 50) == 3

        if no_ssl and lb.sslTermination is not None and \
                not lb.sslTermination.enabled:
            self.lbaas_provider.ssl_disabled(lb.id)
            ssl_mode_order.append(LBSModes.OFF)

        if ssl_mixed:
            if lb.sslTermination is not None and (
                not lb.sslTermination.enabled or
                    lb.sslTermination.secureTrafficOnly):
                self.lbaas_provider.ssl_mixed_on(lb.id)
                ssl_mode_order.append(LBSModes.MIXED)

        if ssl_only:
            if lb.sslTermination is not None and (
                not lb.sslTermination.enabled or
                    lb.sslTermination.secureTrafficOnly):
                self.lbaas_provider.ssl_only_on(lb.id)
                ssl_mode_order.append(LBSModes.ON)

        vip = lb.get_public_ipv4_vip()

        usage_values = self._get_bandwidth(section)

        normal_out = True
        normal_in = True
        ssl_out = True
        ssl_in = True

        if ssl_only:
            normal_out = False
            normal_in = False
        elif no_ssl:
            ssl_out = False
            ssl_in = False
        elif lb.sslTermination is None or not lb.sslTermination.enabled:
            ssl_out = False
            ssl_in = False
        elif lb.sslTermination.enabled and lb.sslTermination.secureTrafficOnly:
            normal_out = False
            normal_in = False

        self._generate_bandwidth(vip, usage_values, normal_out=normal_out,
                                 normal_in=normal_in, ssl_out=ssl_out,
                                 ssl_in=ssl_in,
                                 add_to_current=self._is_same_hour(section))

        self._write_new_values(section, start_time,
                               usage_values.bandwidth_out,
                               usage_values.bandwidth_in,
                               usage_values.bandwidth_out_ssl,
                               usage_values.bandwidth_in_ssl,
                               usage_values.total_bandwidth_in,
                               usage_values.total_bandwidth_out,
                               usage_values.total_bandwidth_in_ssl,
                               usage_values.total_bandwidth_out_ssl,
                               ssl_mode_order)

    def _create_new_lb_if_last_is_not_active(self, section):
        if not self.usage_data.has_section(section):
            self.usage_data.add_section(section)
            self.usage_data.set(section, UsageKeys.LOAD_BALANCER_ID_FIELD,
                                '-1')
        lb_id = self.usage_data.get(section, UsageKeys.LOAD_BALANCER_ID_FIELD)
        resp = self.lbaas_provider.client.get_load_balancer(lb_id)
        if resp.status_code == 404 or resp.entity.status in (
                LBST.DELETED, LBST.PENDING_DELETE, LBST.ERROR):
            virtualIps = [{'type': LBVipTypes.PUBLIC}]
            create_time = datetime.datetime.utcnow().isoformat()
            resp = self.lbaas_provider.create_active_load_balancer(
                virtualIps=virtualIps)

            self.usage_data.set(section, UsageKeys.LOAD_BALANCER_ID_FIELD,
                                str(resp.entity.id))
            self.usage_data.set(section, UsageKeys.CREATE_TIME, create_time)
            self.usage_data.set(section, UsageKeys.TOTAL_BANDWIDTH_IN_FIELD,
                                '0')
            self.usage_data.set(section, UsageKeys.TOTAL_BANDWIDTH_OUT_FIELD,
                                '0')
            self.usage_data.set(section,
                                UsageKeys.TOTAL_BANDWIDTH_IN_SSL_FIELD,
                                '0')
            self.usage_data.set(section,
                                UsageKeys.TOTAL_BANDWIDTH_OUT_SSL_FIELD,
                                '0')
            self.usage_data.set(section, UsageKeys.BANDWIDTH_IN_FIELD,
                                '0')
            self.usage_data.set(section, UsageKeys.BANDWIDTH_OUT_FIELD,
                                '0')
            self.usage_data.set(section,
                                UsageKeys.BANDWIDTH_IN_SSL_FIELD,
                                '0')
            self.usage_data.set(section,
                                UsageKeys.BANDWIDTH_OUT_SSL_FIELD,
                                '0')
            self.usage_data.set(section,
                                UsageKeys.SSL_MODE_ORDER,
                                LBSModes.OFF)
        return resp.entity

    def _generate_bandwidth(self, vip, usage_values, normal_out=False,
                            normal_in=False, ssl_out=False, ssl_in=False,
                            add_to_current=False):

        bandwidth_out = bandwidth_in = bandwidth_out_ssl = bandwidth_in_ssl = 0

        if normal_out:
            bandwidth = self.lbaas_provider.generate_bandwidth_out(vip.address)
            bandwidth_in += bandwidth[0]
            bandwidth_out += bandwidth[1]
        if normal_in:
            bandwidth = self.lbaas_provider.generate_bandwidth_in(vip.address)
            bandwidth_in += bandwidth[0]
            bandwidth_out += bandwidth[1]
        if ssl_out:
            bandwidth = self.lbaas_provider.generate_ssl_bandwidth_out(vip.address)
            bandwidth_in_ssl += bandwidth[0]
            bandwidth_out_ssl += bandwidth[1]
        if ssl_in:
            bandwidth = self.lbaas_provider.generate_ssl_bandwidth_in(vip.address)
            bandwidth_in_ssl += bandwidth[0]
            bandwidth_out_ssl += bandwidth[1]

        usage_values.bandwidth_out += bandwidth_out
        usage_values.bandwidth_in += bandwidth_in
        usage_values.bandwidth_out_ssl += bandwidth_out_ssl
        usage_values.bandwidth_in_ssl += bandwidth_in_ssl
        if not add_to_current:
            usage_values.bandwidth_out = bandwidth_out
            usage_values.bandwidth_in = bandwidth_in
            usage_values.bandwidth_out_ssl = bandwidth_out_ssl
            usage_values.bandwidth_in_ssl = bandwidth_in_ssl

        usage_values.total_bandwidth_out += bandwidth_out
        usage_values.total_bandwidth_in += bandwidth_in
        usage_values.total_bandwidth_out_ssl += bandwidth_out_ssl
        usage_values.total_bandwidth_in_ssl += bandwidth_in_ssl

    def _get_bandwidth(self, section):
        bandwidth_out = int(self.usage_data.get(
            section, UsageKeys.BANDWIDTH_OUT_FIELD))
        bandwidth_out_ssl = int(self.usage_data.get(
            section, UsageKeys.BANDWIDTH_OUT_SSL_FIELD))
        bandwidth_in = int(self.usage_data.get(
            section, UsageKeys.BANDWIDTH_IN_FIELD))
        bandwidth_in_ssl = int(self.usage_data.get(
            section, UsageKeys.BANDWIDTH_IN_SSL_FIELD))
        total_bandwidth_out = int(self.usage_data.get(
            section, UsageKeys.TOTAL_BANDWIDTH_OUT_FIELD))
        total_bandwidth_out_ssl = int(self.usage_data.get(
            section, UsageKeys.TOTAL_BANDWIDTH_OUT_SSL_FIELD))
        total_bandwidth_in = int(self.usage_data.get(
            section, UsageKeys.TOTAL_BANDWIDTH_IN_FIELD))
        total_bandwidth_in_ssl = int(self.usage_data.get(
            section, UsageKeys.TOTAL_BANDWIDTH_IN_SSL_FIELD))

        usage_values = UsageValues(
            bandwidth_in=bandwidth_in,
            bandwidth_out=bandwidth_out,
            bandwidth_in_ssl=bandwidth_in_ssl,
            bandwidth_out_ssl=bandwidth_out_ssl,
            total_bandwidth_in=total_bandwidth_in,
            total_bandwidth_out=total_bandwidth_out,
            total_bandwidth_in_ssl=total_bandwidth_in_ssl,
            total_bandwidth_out_ssl=total_bandwidth_out_ssl)

        return usage_values

    def _get_ssl_mode_order(self, section):
        ssl_modes = self.usage_data.get(section, UsageKeys.SSL_MODE_ORDER)
        return ssl_modes.split(',')

    def _write_new_values(self, section, start_time, bandwidth_out,
                          bandwidth_in, bandwidth_out_ssl, bandwidth_in_ssl,
                          total_bandwidth_in, total_bandwidth_out,
                          total_bandwidth_in_ssl, total_bandwidth_out_ssl,
                          ssl_mode_order):
        self.usage_data.set(section,
                            UsageKeys.START_TIME, start_time)
        self.usage_data.set(section,
                            UsageKeys.BANDWIDTH_OUT_FIELD,
                            str(bandwidth_out))
        self.usage_data.set(section,
                            UsageKeys.BANDWIDTH_IN_FIELD,
                            str(bandwidth_in))
        self.usage_data.set(section,
                            UsageKeys.BANDWIDTH_OUT_SSL_FIELD,
                            str(bandwidth_out_ssl))
        self.usage_data.set(section,
                            UsageKeys.BANDWIDTH_IN_SSL_FIELD,
                            str(bandwidth_in_ssl))
        self.usage_data.set(section,
                            UsageKeys.TOTAL_BANDWIDTH_OUT_FIELD,
                            str(total_bandwidth_out))
        self.usage_data.set(section,
                            UsageKeys.TOTAL_BANDWIDTH_IN_FIELD,
                            str(total_bandwidth_in))
        self.usage_data.set(section,
                            UsageKeys.TOTAL_BANDWIDTH_OUT_SSL_FIELD,
                            str(total_bandwidth_out_ssl))
        self.usage_data.set(section,
                            UsageKeys.TOTAL_BANDWIDTH_IN_SSL_FIELD,
                            str(total_bandwidth_in_ssl))
        self.usage_data.set(section, UsageKeys.SSL_MODE_ORDER,
                            ','.join(ssl_mode_order))
        helpers.write_usage_data(self.usage_data,
                                 UsageKeys.LONGRUNNING_FILENAME)

    def _is_same_hour(self, section):
        if hasattr(self, '_same_hour'):
            return self._same_hour
        old_start_time = datetime.datetime.min
        if self.usage_data.has_option(section, UsageKeys.START_TIME):
            old_start_time = self.usage_data.get(section, UsageKeys.START_TIME)
            old_start_time = usage_helpers.str_to_datetime(old_start_time)
        start_time = datetime.datetime.utcnow().isoformat()
        start_time = usage_helpers.str_to_datetime(start_time)

        if start_time.hour != old_start_time.hour:
            self._same_hour = False
            return False
        self._same_hour = True
        return True

    def _get_start_time(self, section):
        if not self.usage_data.has_section(section) or \
                not self._is_same_hour(section):
            start_time = datetime.datetime.utcnow()
        else:
            start_time = self.usage_data.get(section, UsageKeys.START_TIME)
        return start_time
