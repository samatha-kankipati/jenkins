from testrepo.common.testfixtures.load_balancers import \
    LoadBalancersGenerateUsageFixture
from testrepo.lbaas.usage import UsageKeys
from ccengine.domain.types import LoadBalancerStatusTypes as LBST, \
    LoadBalancerVirtualIpTypes as LBVipTypes
from ccengine.common.decorators import attr
import testrepo.lbaas.usage.generate.generate_helpers as helpers
import ConfigParser
import datetime
import time


class TestBandwidth(LoadBalancersGenerateUsageFixture):

    SSL_SITE_PREFIX = 'sslterm'
    USAGE_POLLER_INTERVAL = 300

    @classmethod
    def setUpClass(cls):
        super(TestBandwidth, cls).setUpClass()
        cls.usage_data = ConfigParser.SafeConfigParser()

    @classmethod
    def tearDownClass(cls):
        super(TestBandwidth, cls).tearDownClass()

    @attr('generate_usage')
    def test_normal_bandwidth(self):
        """Generate normal bandwidth in and out on an LB."""
        virtualIps = [{'type': LBVipTypes.PUBLIC}]
        lb = self.lbaas_provider.create_active_load_balancer(
            virtualIps=virtualIps).entity
        created_time = datetime.datetime.utcnow().isoformat()
        vip = lb.get_public_ipv4_vip()

        bandwidth = self.lbaas_provider.generate_bandwidth_out(vip.address)
        bandwidth_in = bandwidth[0]
        bandwidth_out = bandwidth[1]
        bandwidth = self.lbaas_provider.generate_bandwidth_in(vip.address)
        bandwidth_in += bandwidth[0]
        bandwidth_out += bandwidth[1]

        self.usage_data.add_section(helpers.function_name())
        self.usage_data.set(helpers.function_name(),
                            UsageKeys.LOAD_BALANCER_ID_FIELD,
                            str(lb.id))
        self.usage_data.set(helpers.function_name(),
                            UsageKeys.CREATE_TIME, created_time)
        self.usage_data.set(helpers.function_name(),
                            UsageKeys.BANDWIDTH_OUT_FIELD,
                            str(bandwidth_out))
        self.usage_data.set(helpers.function_name(),
                            UsageKeys.BANDWIDTH_IN_FIELD,
                            str(bandwidth_in))
        helpers.write_usage_data(self.usage_data, UsageKeys.BANDWIDTH_FILENAME)

    @attr('generate_usage')
    def test_ssl_termination_secure_traffic_only_bandwidth(self):
        """Generate SSL bandwidth."""
        virtualIps = [{'type': LBVipTypes.PUBLIC}]
        lb = self.lbaas_provider.create_active_load_balancer(
            virtualIps=virtualIps).entity
        created_time = datetime.datetime.utcnow().isoformat()
        vip = lb.get_public_ipv4_vip()
        self.lbaas_provider.ssl_only_on(lb.id)

        bandwidth = self.lbaas_provider.generate_ssl_bandwidth_out(vip.address)
        bandwidth_in_ssl = bandwidth[0]
        bandwidth_out_ssl = bandwidth[1]
        bandwidth = self.lbaas_provider.generate_ssl_bandwidth_in(vip.address)
        bandwidth_in_ssl += bandwidth[0]
        bandwidth_out_ssl += bandwidth[1]

        self.usage_data.add_section(helpers.function_name())
        self.usage_data.set(helpers.function_name(),
                            UsageKeys.LOAD_BALANCER_ID_FIELD,
                            str(lb.id))
        self.usage_data.set(helpers.function_name(),
                            UsageKeys.CREATE_TIME, created_time)
        self.usage_data.set(helpers.function_name(),
                            UsageKeys.BANDWIDTH_OUT_SSL_FIELD,
                            str(bandwidth_out_ssl))
        self.usage_data.set(helpers.function_name(),
                            UsageKeys.BANDWIDTH_IN_SSL_FIELD,
                            str(bandwidth_in_ssl))
        helpers.write_usage_data(self.usage_data, UsageKeys.BANDWIDTH_FILENAME)

    @attr('generate_usage')
    def test_ssl_termination_secure_traffic_only_bandwidth_after_poller(self):
        """Generate SSL bandwidth after poller."""
        virtualIps = [{'type': LBVipTypes.PUBLIC}]
        lb = self.lbaas_provider.create_active_load_balancer(
            virtualIps=virtualIps).entity
        created_time = datetime.datetime.utcnow().isoformat()
        vip = lb.get_public_ipv4_vip()
        self.lbaas_provider.ssl_only_on(lb.id)

        time.sleep(self.USAGE_POLLER_INTERVAL)

        bandwidth = self.lbaas_provider.generate_ssl_bandwidth_out(vip.address)
        bandwidth_in_ssl = bandwidth[0]
        bandwidth_out_ssl = bandwidth[1]
        bandwidth = self.lbaas_provider.generate_ssl_bandwidth_in(vip.address)
        bandwidth_in_ssl += bandwidth[0]
        bandwidth_out_ssl += bandwidth[1]

        self.usage_data.add_section(helpers.function_name())
        self.usage_data.set(helpers.function_name(),
                            UsageKeys.LOAD_BALANCER_ID_FIELD,
                            str(lb.id))
        self.usage_data.set(helpers.function_name(),
                            UsageKeys.CREATE_TIME, created_time)
        self.usage_data.set(helpers.function_name(),
                            UsageKeys.BANDWIDTH_OUT_SSL_FIELD,
                            str(bandwidth_out_ssl))
        self.usage_data.set(helpers.function_name(),
                            UsageKeys.BANDWIDTH_IN_SSL_FIELD,
                            str(bandwidth_in_ssl))
        helpers.write_usage_data(self.usage_data, UsageKeys.BANDWIDTH_FILENAME)

    @attr('generate_usage')
    def test_ssl_termination_secure_and_normal_bandwidth(self):
        """Generate SSL and Normal Bandwidth."""
        virtualIps = [{'type': LBVipTypes.PUBLIC}]
        lb = self.lbaas_provider.create_active_load_balancer(
            virtualIps=virtualIps).entity
        created_time = datetime.datetime.utcnow().isoformat()
        vip = lb.get_public_ipv4_vip()
        self.lbaas_provider.ssl_mixed_on(lb.id)

        bandwidth = self.lbaas_provider.generate_bandwidth_out(vip.address)
        bandwidth_in = bandwidth[0]
        bandwidth_out = bandwidth[1]
        bandwidth = self.lbaas_provider.generate_bandwidth_in(vip.address)
        bandwidth_in += bandwidth[0]
        bandwidth_out += bandwidth[1]

        bandwidth = self.lbaas_provider.generate_ssl_bandwidth_out(vip.address)
        bandwidth_in_ssl = bandwidth[0]
        bandwidth_out_ssl = bandwidth[1]
        bandwidth = self.lbaas_provider.generate_ssl_bandwidth_in(vip.address)
        bandwidth_in_ssl += bandwidth[0]
        bandwidth_out_ssl += bandwidth[1]

        self.usage_data.add_section(helpers.function_name())
        self.usage_data.set(helpers.function_name(),
                            UsageKeys.LOAD_BALANCER_ID_FIELD,
                            str(lb.id))
        self.usage_data.set(helpers.function_name(),
                            UsageKeys.CREATE_TIME, created_time)
        self.usage_data.set(helpers.function_name(),
                            UsageKeys.BANDWIDTH_OUT_FIELD,
                            str(bandwidth_out))
        self.usage_data.set(helpers.function_name(),
                            UsageKeys.BANDWIDTH_IN_FIELD,
                            str(bandwidth_in))
        self.usage_data.set(helpers.function_name(),
                            UsageKeys.BANDWIDTH_OUT_SSL_FIELD,
                            str(bandwidth_out_ssl))
        self.usage_data.set(helpers.function_name(),
                            UsageKeys.BANDWIDTH_IN_SSL_FIELD,
                            str(bandwidth_in_ssl))
        helpers.write_usage_data(self.usage_data, UsageKeys.BANDWIDTH_FILENAME)

    @attr('generate_usage')
    def test_ssl_termination_secure_and_normal_bandwidth_after_poller(self):
        """Generate SSL and Normal Bandwidth After Poller Runs."""
        virtualIps = [{'type': LBVipTypes.PUBLIC}]
        lb = self.lbaas_provider.create_active_load_balancer(
            virtualIps=virtualIps).entity
        created_time = datetime.datetime.utcnow().isoformat()
        vip = lb.get_public_ipv4_vip()
        self.lbaas_provider.ssl_mixed_on(lb.id)
        self.fixture_log.info("Sleeping for {0} seconds...".format(
            self.USAGE_POLLER_INTERVAL))
        time.sleep(self.USAGE_POLLER_INTERVAL)

        bandwidth = self.lbaas_provider.generate_bandwidth_out(vip.address)
        bandwidth_in = bandwidth[0]
        bandwidth_out = bandwidth[1]
        bandwidth = self.lbaas_provider.generate_bandwidth_in(vip.address)
        bandwidth_in += bandwidth[0]
        bandwidth_out += bandwidth[1]

        bandwidth = self.lbaas_provider.generate_ssl_bandwidth_out(vip.address)
        bandwidth_in_ssl = bandwidth[0]
        bandwidth_out_ssl = bandwidth[1]
        bandwidth = self.lbaas_provider.generate_ssl_bandwidth_in(vip.address)
        bandwidth_in_ssl += bandwidth[0]
        bandwidth_out_ssl += bandwidth[1]

        self.usage_data.add_section(helpers.function_name())
        self.usage_data.set(helpers.function_name(),
                            UsageKeys.LOAD_BALANCER_ID_FIELD,
                            str(lb.id))
        self.usage_data.set(helpers.function_name(),
                            UsageKeys.CREATE_TIME, created_time)
        self.usage_data.set(helpers.function_name(),
                            UsageKeys.BANDWIDTH_OUT_FIELD,
                            str(bandwidth_out))
        self.usage_data.set(helpers.function_name(),
                            UsageKeys.BANDWIDTH_IN_FIELD,
                            str(bandwidth_in))
        self.usage_data.set(helpers.function_name(),
                            UsageKeys.BANDWIDTH_OUT_SSL_FIELD,
                            str(bandwidth_out_ssl))
        self.usage_data.set(helpers.function_name(),
                            UsageKeys.BANDWIDTH_IN_SSL_FIELD,
                            str(bandwidth_in_ssl))
        helpers.write_usage_data(self.usage_data, UsageKeys.BANDWIDTH_FILENAME)

    @attr('generate_usage')
    def test_normal_bandwidth_after_ssl_modes_toggled(self):
        """Generate normal bandwidth after toggling ssl modes and back."""
        virtualIps = [{'type': LBVipTypes.PUBLIC}]
        lb = self.lbaas_provider.create_active_load_balancer(
            virtualIps=virtualIps).entity
        created_time = datetime.datetime.utcnow().isoformat()
        self.lbaas_provider.ssl_only_on(lb.id)
#        ssl_only_time = datetime.datetime.utcnow().isoformat()
        self.lbaas_provider.ssl_mixed_on(lb.id)
#        ssl_mixed_time = datetime.datetime.utcnow().isoformat()
        self.lbaas_provider.client.delete_ssl_termination(lb.id)
        r = self.lbaas_provider.wait_for_status(lb.id)
        self.assertEquals(r.entity.status, LBST.ACTIVE)
        self.fixture_log.info("Sleeping for {0} seconds...".format(
            self.USAGE_POLLER_INTERVAL))
        time.sleep(self.USAGE_POLLER_INTERVAL)
#        ssl_off_time = datetime.datetime.utcnow().isoformat()
        vip = lb.get_public_ipv4_vip()

        bandwidth = self.lbaas_provider.generate_bandwidth_out(vip.address)
        bandwidth_in = bandwidth[0]
        bandwidth_out = bandwidth[1]
        bandwidth = self.lbaas_provider.generate_bandwidth_in(vip.address)
        bandwidth_in += bandwidth[0]
        bandwidth_out += bandwidth[1]

        self.usage_data.add_section(helpers.function_name())
        self.usage_data.set(helpers.function_name(),
                            UsageKeys.LOAD_BALANCER_ID_FIELD,
                            str(lb.id))
        self.usage_data.set(helpers.function_name(),
                            UsageKeys.CREATE_TIME, created_time)
        self.usage_data.set(helpers.function_name(),
                            UsageKeys.BANDWIDTH_OUT_FIELD,
                            str(bandwidth_out))
        self.usage_data.set(helpers.function_name(),
                            UsageKeys.BANDWIDTH_IN_FIELD,
                            str(bandwidth_in))
        helpers.write_usage_data(self.usage_data, UsageKeys.BANDWIDTH_FILENAME)

    @attr('generate_usage')
    def test_normal_bandwidth_after_ssl_mixed(self):
        """Generate normal bandwidth after ssl mixed."""
        virtualIps = [{'type': LBVipTypes.PUBLIC}]
        lb = self.lbaas_provider.create_active_load_balancer(
            virtualIps=virtualIps).entity
        created_time = datetime.datetime.utcnow().isoformat()
        vip = lb.get_public_ipv4_vip()
        self.lbaas_provider.ssl_mixed_on(lb.id)
#        ssl_only_time = datetime.datetime.utcnow().isoformat()
        self.fixture_log.info("Sleeping for {0} seconds...".format(
            self.USAGE_POLLER_INTERVAL))
        time.sleep(self.USAGE_POLLER_INTERVAL)
        bandwidth = self.lbaas_provider.generate_ssl_bandwidth_out(vip.address)
        bandwidth_in_ssl = bandwidth[0]
        bandwidth_out_ssl = bandwidth[1]
        bandwidth = self.lbaas_provider.generate_ssl_bandwidth_in(vip.address)
        bandwidth_in_ssl += bandwidth[0]
        bandwidth_out_ssl += bandwidth[1]
        self.lbaas_provider.client.delete_ssl_termination(lb.id)
        r = self.lbaas_provider.wait_for_status(lb.id)
        self.assertEquals(r.entity.status, LBST.ACTIVE)
#        ssl_off_time = datetime.datetime.utcnow().isoformat()
        self.fixture_log.info("Sleeping for {0} seconds...".format(
            self.USAGE_POLLER_INTERVAL))
        time.sleep(self.USAGE_POLLER_INTERVAL)
        bandwidth = self.lbaas_provider.generate_bandwidth_out(vip.address)
        bandwidth_in = bandwidth[0]
        bandwidth_out = bandwidth[1]
        bandwidth = self.lbaas_provider.generate_bandwidth_in(vip.address)
        bandwidth_in += bandwidth[0]
        bandwidth_out += bandwidth[1]
        self.usage_data.add_section(helpers.function_name())
        self.usage_data.set(helpers.function_name(),
                            UsageKeys.LOAD_BALANCER_ID_FIELD,
                            str(lb.id))
        self.usage_data.set(helpers.function_name(),
                            UsageKeys.CREATE_TIME, created_time)
        self.usage_data.set(helpers.function_name(),
                            UsageKeys.BANDWIDTH_OUT_FIELD,
                            str(bandwidth_out))
        self.usage_data.set(helpers.function_name(),
                            UsageKeys.BANDWIDTH_IN_FIELD,
                            str(bandwidth_in))
        self.usage_data.set(helpers.function_name(),
                            UsageKeys.BANDWIDTH_OUT_SSL_FIELD,
                            str(bandwidth_out_ssl))
        self.usage_data.set(helpers.function_name(),
                            UsageKeys.BANDWIDTH_IN_SSL_FIELD,
                            str(bandwidth_in_ssl))
        helpers.write_usage_data(self.usage_data, UsageKeys.BANDWIDTH_FILENAME)

    @attr('generate_usage')
    def test_normal_bandwidth_after_unsuspend(self):
        """Generate normal bandwidth after unsuspension."""
        virtualIps = [{'type': LBVipTypes.PUBLIC}]
        lb = self.lbaas_provider.create_active_load_balancer(
            virtualIps=virtualIps).entity
        created_time = datetime.datetime.utcnow().isoformat()
        vip = lb.get_public_ipv4_vip()
        self.lbaas_provider.suspend_load_balancer(lb.id)
        r = self.lbaas_provider.wait_for_status(lb.id, LBST.SUSPENDED)
        self.assertEquals(r.entity.status, LBST.SUSPENDED)
        self.fixture_log.info("Sleeping for {0} seconds...".format(
            self.USAGE_POLLER_INTERVAL))
        time.sleep(self.USAGE_POLLER_INTERVAL)
        self.lbaas_provider.mgmt_client.unsuspend_load_balancer(lb.id)
        self.lbaas_provider.wait_for_status(lb.id, LBST.ACTIVE)
        self.fixture_log.info("Sleeping for {0} seconds...".format(
            self.USAGE_POLLER_INTERVAL))
        time.sleep(self.USAGE_POLLER_INTERVAL)
        bandwidth = self.lbaas_provider.generate_bandwidth_out(vip.address)
        bandwidth_in = bandwidth[0]
        bandwidth_out = bandwidth[1]
        bandwidth = self.lbaas_provider.generate_bandwidth_in(vip.address)
        bandwidth_in += bandwidth[0]
        bandwidth_out += bandwidth[1]

        self.usage_data.add_section(helpers.function_name())
        self.usage_data.set(helpers.function_name(),
                            UsageKeys.LOAD_BALANCER_ID_FIELD,
                            str(lb.id))
        self.usage_data.set(helpers.function_name(),
                            UsageKeys.CREATE_TIME, created_time)
        self.usage_data.set(helpers.function_name(),
                            UsageKeys.BANDWIDTH_OUT_FIELD,
                            str(bandwidth_out))
        self.usage_data.set(helpers.function_name(),
                            UsageKeys.BANDWIDTH_IN_FIELD,
                            str(bandwidth_in))
        helpers.write_usage_data(self.usage_data, UsageKeys.BANDWIDTH_FILENAME)

    @attr('generate_usage')
    def test_ssl_bandwidth_across_ssl_states(self):
        """Generate ssl bandwidth after SSL_ONLY_ON, then SSL_OFF, then SSL_ONLY_ON again."""
        virtualIps = [{'type': LBVipTypes.PUBLIC}]
        lb = self.lbaas_provider.create_active_load_balancer(
            virtualIps=virtualIps).entity
        created_time = datetime.datetime.utcnow().isoformat()
        self.lbaas_provider.ssl_only_on(lb.id)

        vip = lb.get_public_ipv4_vip()
        bandwidth = self.lbaas_provider.generate_ssl_bandwidth_out(vip.address)
        bandwidth_in = bandwidth[0]
        bandwidth_out = bandwidth[1]
        bandwidth = self.lbaas_provider.generate_ssl_bandwidth_in(vip.address)
        bandwidth_in += bandwidth[0]
        bandwidth_out += bandwidth[1]

        self.lbaas_provider.client.delete_ssl_termination(lb.id)
        r = self.lbaas_provider.wait_for_status(lb.id)
        self.assertEquals(r.entity.status, LBST.ACTIVE)
        self.lbaas_provider.ssl_only_on(lb.id)

        bandwidth = self.lbaas_provider.generate_ssl_bandwidth_out(vip.address)
        bandwidth_in2 = bandwidth[0]
        bandwidth_out2 = bandwidth[1]
        bandwidth = self.lbaas_provider.generate_ssl_bandwidth_in(vip.address)
        bandwidth_in2 += bandwidth[0]
        bandwidth_out2 += bandwidth[1]

        self.usage_data.add_section(helpers.function_name())
        self.usage_data.set(helpers.function_name(),
                            UsageKeys.LOAD_BALANCER_ID_FIELD,
                            str(lb.id))
        self.usage_data.set(helpers.function_name(),
                            UsageKeys.CREATE_TIME, created_time)
        self.usage_data.set(helpers.function_name(),
                            UsageKeys.BANDWIDTH_OUT_SSL_FIELD,
                            str(bandwidth_out))
        self.usage_data.set(helpers.function_name(),
                            UsageKeys.BANDWIDTH_IN_SSL_FIELD,
                            str(bandwidth_in))
        self.usage_data.set(helpers.function_name(),
                            UsageKeys.BANDWIDTH_OUT_SSL_FIELD_2,
                            str(bandwidth_out2))
        self.usage_data.set(helpers.function_name(),
                            UsageKeys.BANDWIDTH_IN_SSL_FIELD_2,
                            str(bandwidth_in2))
        helpers.write_usage_data(self.usage_data, UsageKeys.BANDWIDTH_FILENAME)

    @attr('generate_usage')
    def test_bandwidth_before_suspend_and_after_unsuspend(self):
        """Generate bandwidth before suspending a load balancer and also after unsuspending it."""
        store_values = self._generate_bandwidth_before_suspend_and_after_unsuspend()
        self.usage_data.add_section(helpers.function_name())
        self.usage_data.set(helpers.function_name(),
                            UsageKeys.LOAD_BALANCER_ID_FIELD,
                            str(store_values['loadbalancer'].id))
        self.usage_data.set(helpers.function_name(),
                            UsageKeys.CREATE_TIME, store_values['created_time'])
        self.usage_data.set(helpers.function_name(),
                            UsageKeys.BANDWIDTH_OUT_FIELD,
                            str(store_values['bandwidth_out']))
        self.usage_data.set(helpers.function_name(),
                            UsageKeys.BANDWIDTH_IN_FIELD,
                            str(store_values['bandwidth_in']))
        self.usage_data.set(helpers.function_name(),
                            UsageKeys.BANDWIDTH_OUT_FIELD_2,
                            str(store_values['bandwidth_out2']))
        self.usage_data.set(helpers.function_name(),
                            UsageKeys.BANDWIDTH_IN_FIELD_2,
                            str(store_values['bandwidth_in2']))
        helpers.write_usage_data(self.usage_data, UsageKeys.BANDWIDTH_FILENAME)

    @attr('generate_usage')
    def test_bandwidth_before_suspend_and_after_unsuspend_wait_for_next_poll(self):
        """Generate bandwidth before suspending a load balancer and also after unsuspending it after one poll."""
        store_values = \
            self._generate_bandwidth_before_suspend_and_after_unsuspend(
                time_between=self.USAGE_POLLER_INTERVAL)
        self.usage_data.add_section(helpers.function_name())
        self.usage_data.set(helpers.function_name(),
                            UsageKeys.LOAD_BALANCER_ID_FIELD,
                            str(store_values['loadbalancer'].id))
        self.usage_data.set(helpers.function_name(),
                            UsageKeys.CREATE_TIME,
                            store_values['created_time'])
        self.usage_data.set(helpers.function_name(),
                            UsageKeys.BANDWIDTH_OUT_FIELD,
                            str(store_values['bandwidth_out']))
        self.usage_data.set(helpers.function_name(),
                            UsageKeys.BANDWIDTH_IN_FIELD,
                            str(store_values['bandwidth_in']))
        self.usage_data.set(helpers.function_name(),
                            UsageKeys.BANDWIDTH_OUT_FIELD_2,
                            str(store_values['bandwidth_out2']))
        self.usage_data.set(helpers.function_name(),
                            UsageKeys.BANDWIDTH_IN_FIELD_2,
                            str(store_values['bandwidth_in2']))
        helpers.write_usage_data(self.usage_data, UsageKeys.BANDWIDTH_FILENAME)

    @attr('generate_usage')
    def test_bandwidth_before_suspend_and_after_unsuspend_wait_after_two_polls(self):
        """Generate bandwidth before suspending a load balancer and also after unsuspending it after two polls."""
        store_values = \
            self._generate_bandwidth_before_suspend_and_after_unsuspend(
                time_between=self.USAGE_POLLER_INTERVAL * 2)
        self.usage_data.add_section(helpers.function_name())
        self.usage_data.set(helpers.function_name(),
                            UsageKeys.LOAD_BALANCER_ID_FIELD,
                            str(store_values['loadbalancer'].id))
        self.usage_data.set(helpers.function_name(),
                            UsageKeys.CREATE_TIME,
                            store_values['created_time'])
        self.usage_data.set(helpers.function_name(),
                            UsageKeys.BANDWIDTH_OUT_FIELD,
                            str(store_values['bandwidth_out']))
        self.usage_data.set(helpers.function_name(),
                            UsageKeys.BANDWIDTH_IN_FIELD,
                            str(store_values['bandwidth_in']))
        self.usage_data.set(helpers.function_name(),
                            UsageKeys.BANDWIDTH_OUT_FIELD_2,
                            str(store_values['bandwidth_out2']))
        self.usage_data.set(helpers.function_name(),
                            UsageKeys.BANDWIDTH_IN_FIELD_2,
                            str(store_values['bandwidth_in2']))
        helpers.write_usage_data(self.usage_data, UsageKeys.BANDWIDTH_FILENAME)

    def _generate_bandwidth_before_suspend_and_after_unsuspend(self,
                                                               time_between=0):
        virtualIps = [{'type': LBVipTypes.PUBLIC}]
        lb = self.lbaas_provider.create_active_load_balancer(
            virtualIps=virtualIps).entity
        created_time = datetime.datetime.utcnow().isoformat()

        vip = lb.get_public_ipv4_vip()
        bandwidth = self.lbaas_provider.generate_bandwidth_out(vip.address)
        bandwidth_in = bandwidth[0]
        bandwidth_out = bandwidth[1]
        bandwidth = self.lbaas_provider.generate_bandwidth_in(vip.address)
        bandwidth_in += bandwidth[0]
        bandwidth_out += bandwidth[1]

        self.lbaas_provider.suspend_load_balancer(lb.id)
        self.fixture_log.info("Sleeping for {0} seconds...".format(time_between))
        time.sleep(time_between)
        self.lbaas_provider.unsuspend_load_balancer(lb.id)

        bandwidth2 = self.lbaas_provider.generate_bandwidth_out(vip.address)
        bandwidth_in2 = bandwidth2[0]
        bandwidth_out2 = bandwidth2[1]
        bandwidth2 = self.lbaas_provider.generate_bandwidth_in(vip.address)
        bandwidth_in2 += bandwidth2[0]
        bandwidth_out2 += bandwidth2[1]

        return {"loadbalancer": lb,
                "created_time": created_time,
                "bandwidth_out": bandwidth_out,
                "bandwidth_in": bandwidth_in,
                "bandwidth_out2": bandwidth_out2,
                "bandwidth_in2": bandwidth_in2}

    @attr('generate_usage')
    def test_normal_bandwidth_across_ssl_states(self):
        """Generate normal bandwidth across ssl states."""
        virtualIps = [{'type': LBVipTypes.PUBLIC}]
        lb = self.lbaas_provider.create_active_load_balancer(
            virtualIps=virtualIps).entity
        created_time = datetime.datetime.utcnow().isoformat()
        vip = lb.get_public_ipv4_vip()

        self.lbaas_provider.ssl_mixed_on(lb.id)
        bandwidth = self.lbaas_provider.generate_bandwidth_out(vip.address)
        bandwidth_in = bandwidth[0]
        bandwidth_out = bandwidth[1]
        bandwidth = self.lbaas_provider.generate_bandwidth_in(vip.address)
        bandwidth_in += bandwidth[0]
        bandwidth_out += bandwidth[1]

        self.lbaas_provider.ssl_only_on(lb.id)

        self.lbaas_provider.ssl_disabled(lb.id)

        bandwidth2 = self.lbaas_provider.generate_bandwidth_out(vip.address)
        bandwidth_in2 = bandwidth2[0]
        bandwidth_out2 = bandwidth2[1]
        bandwidth2 = self.lbaas_provider.generate_bandwidth_in(vip.address)
        bandwidth_in2 += bandwidth2[0]
        bandwidth_out2 += bandwidth2[1]

        self.lbaas_provider.client.delete_ssl_termination(lb.id)
        r = self.lbaas_provider.wait_for_status(lb.id)
        self.assertEquals(LBST.ACTIVE, r.entity.status)
        bandwidth3 = self.lbaas_provider.generate_bandwidth_out(vip.address)
        bandwidth_in3 = bandwidth3[0]
        bandwidth_out3 = bandwidth3[1]
        bandwidth3 = self.lbaas_provider.generate_bandwidth_in(vip.address)
        bandwidth_in3 += bandwidth3[0]
        bandwidth_out3 += bandwidth3[1]

        self.usage_data.add_section(helpers.function_name())
        self.usage_data.set(helpers.function_name(),
                            UsageKeys.LOAD_BALANCER_ID_FIELD,
                            str(lb.id))
        self.usage_data.set(helpers.function_name(),
                            UsageKeys.CREATE_TIME, created_time)
        self.usage_data.set(helpers.function_name(),
                            UsageKeys.BANDWIDTH_OUT_FIELD,
                            str(bandwidth_out))
        self.usage_data.set(helpers.function_name(),
                            UsageKeys.BANDWIDTH_IN_FIELD,
                            str(bandwidth_in))
        self.usage_data.set(helpers.function_name(),
                            UsageKeys.BANDWIDTH_OUT_FIELD_2,
                            str(bandwidth_out2))
        self.usage_data.set(helpers.function_name(),
                            UsageKeys.BANDWIDTH_IN_FIELD_2,
                            str(bandwidth_in2))
        self.usage_data.set(helpers.function_name(),
                            UsageKeys.BANDWIDTH_OUT_FIELD_3,
                            str(bandwidth_out3))
        self.usage_data.set(helpers.function_name(),
                            UsageKeys.BANDWIDTH_IN_FIELD_3,
                            str(bandwidth_in3))
        helpers.write_usage_data(self.usage_data, UsageKeys.BANDWIDTH_FILENAME)

    @attr('generate_usage')
    def test_bandwidth_on_extra_virtual_ip(self):
        """Generate bandwidth on extra virtual ip."""
        virtualIps = [{'type': LBVipTypes.PUBLIC}]
        lb = self.lbaas_provider.create_active_load_balancer(
            virtualIps=virtualIps).entity
        created_time = datetime.datetime.utcnow().isoformat()
        vip = self.lbaas_provider.add_virtual_ip(lb.id).entity

        bandwidth = self.lbaas_provider.generate_bandwidth_out(vip.address)
        bandwidth_in = bandwidth[0]
        bandwidth_out = bandwidth[1]
        bandwidth = self.lbaas_provider.generate_bandwidth_in(vip.address)
        bandwidth_in += bandwidth[0]
        bandwidth_out += bandwidth[1]

        self.lbaas_provider.ssl_only_on(lb.id)
        bandwidth = self.lbaas_provider.generate_ssl_bandwidth_out(vip.address)
        bandwidth_in_ssl = bandwidth[0]
        bandwidth_out_ssl = bandwidth[1]
        bandwidth = self.lbaas_provider.generate_ssl_bandwidth_in(vip.address)
        bandwidth_in_ssl += bandwidth[0]
        bandwidth_out_ssl += bandwidth[1]

        self.usage_data.add_section(helpers.function_name())
        self.usage_data.set(helpers.function_name(),
                            UsageKeys.LOAD_BALANCER_ID_FIELD,
                            str(lb.id))
        self.usage_data.set(helpers.function_name(),
                            UsageKeys.CREATE_TIME, created_time)
        self.usage_data.set(helpers.function_name(),
                            UsageKeys.BANDWIDTH_OUT_FIELD,
                            str(bandwidth_out))
        self.usage_data.set(helpers.function_name(),
                            UsageKeys.BANDWIDTH_IN_FIELD,
                            str(bandwidth_in))
        self.usage_data.set(helpers.function_name(),
                            UsageKeys.BANDWIDTH_OUT_SSL_FIELD,
                            str(bandwidth_out_ssl))
        self.usage_data.set(helpers.function_name(),
                            UsageKeys.BANDWIDTH_IN_SSL_FIELD,
                            str(bandwidth_in_ssl))
        helpers.write_usage_data(self.usage_data, UsageKeys.BANDWIDTH_FILENAME)

    @attr('generate_usage')
    def test_bandwidth_on_extra_virtual_ip_after_poller(self):
        """Generate bandwidth on extra virtual ip after poller."""
        virtualIps = [{'type': LBVipTypes.PUBLIC}]
        lb = self.lbaas_provider.create_active_load_balancer(
            virtualIps=virtualIps).entity
        created_time = datetime.datetime.utcnow().isoformat()
        vip = self.lbaas_provider.add_virtual_ip(lb.id).entity

        time.sleep(self.USAGE_POLLER_INTERVAL)

        bandwidth = self.lbaas_provider.generate_bandwidth_out(vip.address)
        bandwidth_in = bandwidth[0]
        bandwidth_out = bandwidth[1]
        bandwidth = self.lbaas_provider.generate_bandwidth_in(vip.address)
        bandwidth_in += bandwidth[0]
        bandwidth_out += bandwidth[1]

        self.lbaas_provider.ssl_only_on(lb.id)
        bandwidth = self.lbaas_provider.generate_ssl_bandwidth_out(vip.address)
        bandwidth_in_ssl = bandwidth[0]
        bandwidth_out_ssl = bandwidth[1]
        bandwidth = self.lbaas_provider.generate_ssl_bandwidth_in(vip.address)
        bandwidth_in_ssl += bandwidth[0]
        bandwidth_out_ssl += bandwidth[1]

        self.usage_data.add_section(helpers.function_name())
        self.usage_data.set(helpers.function_name(),
                            UsageKeys.LOAD_BALANCER_ID_FIELD,
                            str(lb.id))
        self.usage_data.set(helpers.function_name(),
                            UsageKeys.CREATE_TIME, created_time)
        self.usage_data.set(helpers.function_name(),
                            UsageKeys.BANDWIDTH_OUT_FIELD,
                            str(bandwidth_out))
        self.usage_data.set(helpers.function_name(),
                            UsageKeys.BANDWIDTH_IN_FIELD,
                            str(bandwidth_in))
        self.usage_data.set(helpers.function_name(),
                            UsageKeys.BANDWIDTH_OUT_SSL_FIELD,
                            str(bandwidth_out_ssl))
        self.usage_data.set(helpers.function_name(),
                            UsageKeys.BANDWIDTH_IN_SSL_FIELD,
                            str(bandwidth_in_ssl))
        helpers.write_usage_data(self.usage_data, UsageKeys.BANDWIDTH_FILENAME)
