from testrepo.common.testfixtures.load_balancers import \
                                            LoadBalancersGenerateUsageFixture
from testrepo.lbaas.usage import UsageKeys
from ccengine.common.decorators import attr
from ccengine.domain.types import LoadBalancerVirtualIpTypes as LBVipTypes
import testrepo.lbaas.usage.generate.generate_helpers as helpers
import ConfigParser
import time
import datetime
from requests import ConnectionError
try:
    from urllib3.exceptions import SSLError
except:
    pass


class TestAvgConcurrentConnections(LoadBalancersGenerateUsageFixture):

    POLLER_INTERVAL = 300

    @classmethod
    def setUpClass(cls):
        super(TestAvgConcurrentConnections, cls).setUpClass()
        cls.usage_data = ConfigParser.SafeConfigParser()

    @classmethod
    def tearDownClass(cls):
        super(TestAvgConcurrentConnections, cls).tearDownClass()

    @attr('generate_usage')
    def test_average_concurrent_connections(self):
        '''Generate average concurrent connections.'''
        virtualIps = [{'type': LBVipTypes.PUBLIC}]
        lb = self.lbaas_provider.create_active_load_balancer(
            virtualIps=virtualIps).entity
        created_time = datetime.datetime.utcnow().isoformat()
        vip = lb.get_public_ipv4_vip()
        try:
            self.lbaas_provider.\
                generate_avg_concurrent_connections(vip.address,
                UsageKeys.GENERATED_NUM_CONNECTIONS)
        except ConnectionError:
            self.lbaas_provider.\
                generate_avg_concurrent_connections(vip.address,
                UsageKeys.GENERATED_NUM_CONNECTIONS)
        self.usage_data.add_section(helpers.function_name())
        self.usage_data.set(helpers.function_name(),
                            UsageKeys.LOAD_BALANCER_ID_FIELD,
                            str(lb.id))
        self.usage_data.set(helpers.function_name(),
                            UsageKeys.CREATE_TIME, created_time)
        self.usage_data.set(helpers.function_name(),
                            UsageKeys.AVERAGE_NUM_CONNECTIONS,
                            str(UsageKeys.GENERATED_NUM_CONNECTIONS))
        helpers.write_usage_data(self.usage_data, UsageKeys.ACC_FILENAME)

    @attr('generate_usage')
    def test_average_concurrent_connections_ssl(self):
        '''Generate SSL average concurrent connections.'''
        virtualIps = [{'type': LBVipTypes.PUBLIC}]
        lb = self.lbaas_provider.create_active_load_balancer(
            virtualIps=virtualIps).entity
        created_time = datetime.datetime.utcnow().isoformat()
        vip = lb.get_public_ipv4_vip()
        self.lbaas_provider.ssl_only_on(lb.id)
        time.sleep(self.POLLER_INTERVAL)
        try:
            self.lbaas_provider.generate_ssl_avg_concurrent_connections(
                vip.address, UsageKeys.GENERATED_NUM_CONNECTIONS)
        except ConnectionError, SSLError:
            self.lbaas_provider.generate_ssl_avg_concurrent_connections(
                vip.address, UsageKeys.GENERATED_NUM_CONNECTIONS)
        self.usage_data.add_section(helpers.function_name())
        self.usage_data.set(helpers.function_name(),
                            UsageKeys.LOAD_BALANCER_ID_FIELD,
                            str(lb.id))
        self.usage_data.set(helpers.function_name(),
                            UsageKeys.CREATE_TIME, created_time)
        self.usage_data.set(helpers.function_name(),
                            UsageKeys.AVERAGE_NUM_CONNECTIONS,
                            str(UsageKeys.GENERATED_NUM_CONNECTIONS))
        helpers.write_usage_data(self.usage_data, UsageKeys.ACC_FILENAME)

    @attr('generate_usage')
    def test_servicenet_average_concurrent_connections(self):
        '''Generate servicenet average concurrent connections.'''
        pass
