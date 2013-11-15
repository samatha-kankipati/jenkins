from testrepo.common.testfixtures.load_balancers import \
                                            LoadBalancersGenerateUsageFixture
from testrepo.lbaas.usage import UsageKeys
import testrepo.lbaas.usage.generate.generate_helpers as helpers
from ccengine.common.decorators import attr
import datetime
import ConfigParser


class TestUptime(LoadBalancersGenerateUsageFixture):

    @classmethod
    def setUpClass(cls):
        super(TestUptime, cls).setUpClass()
        cls.usage_data = ConfigParser.SafeConfigParser()

    @classmethod
    def tearDownClass(cls):
        super(TestUptime, cls).tearDownClass()

    @attr('generate_usage')
    def test_normal_load_balancer_uptime(self):
        '''Generate uptime for a load balancer.'''
        self.usage_data.add_section(helpers.function_name())
        r = self.lbaas_provider.create_active_load_balancer()
        self.usage_data.set(helpers.function_name(),
                            UsageKeys.LOAD_BALANCER_ID_FIELD,
                            str(r.entity.id))
        self.usage_data.set(helpers.function_name(),
                            UsageKeys.CREATE_TIME,
                            datetime.datetime.utcnow().isoformat())
        helpers.write_usage_data(self.usage_data, UsageKeys.UPTIME_FILENAME)

    @attr('generate_usage')
    def test_ssl_only_load_balancer_uptime(self):
        '''Generate uptime for an ssl load balancer - SSL_ONLY_ON.'''
        self.usage_data.add_section(helpers.function_name())
        lb = self.lbaas_provider.create_active_load_balancer().entity
        self.usage_data.set(helpers.function_name(),
                            UsageKeys.LOAD_BALANCER_ID_FIELD,
                            str(lb.id))
        self.usage_data.set(helpers.function_name(),
                            UsageKeys.CREATE_TIME,
                            datetime.datetime.utcnow().isoformat())
        self.lbaas_provider.ssl_only_on(lb.id)
        r = self.lbaas_provider.client.get_load_balancer(lb.id)
        self.usage_data.set(helpers.function_name(),
                            UsageKeys.SSL_ON_TIME,
                            r.entity.updated.time)
        helpers.write_usage_data(self.usage_data, UsageKeys.UPTIME_FILENAME)

    @attr('generate_usage')
    def test_ssl_mixed_load_balancer_uptime(self):
        '''Generate uptime for an ssl load balancer - SSL_MIXED_ON.'''
        self.usage_data.add_section(helpers.function_name())
        lb = self.lbaas_provider.create_active_load_balancer().entity
        self.usage_data.set(helpers.function_name(),
                            UsageKeys.LOAD_BALANCER_ID_FIELD,
                            str(lb.id))
        self.usage_data.set(helpers.function_name(),
                            UsageKeys.CREATE_TIME,
                            datetime.datetime.utcnow().isoformat())
        self.lbaas_provider.ssl_mixed_on(lb.id)
        r = self.lbaas_provider.client.get_load_balancer(lb.id)
        self.usage_data.set(helpers.function_name(),
                            UsageKeys.SSL_ON_TIME,
                            r.entity.updated.time)
        helpers.write_usage_data(self.usage_data, UsageKeys.UPTIME_FILENAME)

    @attr('generate_usage')
    def test_virtual_ips_uptime(self):
        '''Generate uptime for load balancer with extra virtual ip.'''
        self.usage_data.add_section(helpers.function_name())
        lb = self.lbaas_provider.create_active_load_balancer().entity
        self.usage_data.set(helpers.function_name(),
                            UsageKeys.LOAD_BALANCER_ID_FIELD,
                            str(lb.id))
        self.usage_data.set(helpers.function_name(),
                            UsageKeys.CREATE_TIME,
                            datetime.datetime.utcnow().isoformat())
        self.lbaas_provider.add_virtual_ip(lb.id)
        r = self.lbaas_provider.client.get_load_balancer(lb.id)
        self.assertEquals(len(r.entity.virtualIps), 3)
        num_vips = 2
        self.usage_data.set(helpers.function_name(),
                            UsageKeys.NUM_VIPS, str(num_vips))
        helpers.write_usage_data(self.usage_data, UsageKeys.UPTIME_FILENAME)

    @attr('generate_usage')
    def test_multiple_virtual_ips_uptime(self):
        '''Generate uptime for load balancer with multiple extra virtual ips CREATE and DELETE vip..'''
        self.usage_data.add_section(helpers.function_name())
        lb = self.lbaas_provider.create_active_load_balancer().entity
        self.usage_data.set(helpers.function_name(),
                            UsageKeys.LOAD_BALANCER_ID_FIELD,
                            str(lb.id))
        self.usage_data.set(helpers.function_name(),
                            UsageKeys.CREATE_TIME,
                            datetime.datetime.utcnow().isoformat())
        self.lbaas_provider.add_virtual_ip(lb.id)
        vip_r = self.lbaas_provider.add_virtual_ip(lb.id)
        r = self.lbaas_provider.client.get_load_balancer(lb.id)
        self.assertEquals(len(r.entity.virtualIps), 4)
        self.lbaas_provider.delete_virtual_ip(lb.id, vip_r.entity.id)
        r = self.lbaas_provider.client.get_load_balancer(lb.id)
        self.assertEquals(len(r.entity.virtualIps), 3)
        num_vips = 2
        self.usage_data.set(helpers.function_name(),
                            UsageKeys.NUM_VIPS, str(num_vips))
        helpers.write_usage_data(self.usage_data, UsageKeys.UPTIME_FILENAME)

    @attr('generate_usage')
    def test_suspended_uptime(self):
        '''Generate uptime for load balancer in suspended status.'''
        self.usage_data.add_section(helpers.function_name())
        lb = self.lbaas_provider.create_active_load_balancer().entity
        self.usage_data.set(helpers.function_name(),
                            UsageKeys.LOAD_BALANCER_ID_FIELD,
                            str(lb.id))
        self.usage_data.set(helpers.function_name(),
                            UsageKeys.CREATE_TIME,
                            datetime.datetime.utcnow().isoformat())
        self.lbaas_provider.suspend_load_balancer(lb.id)
        helpers.write_usage_data(self.usage_data, UsageKeys.UPTIME_FILENAME)

    @attr('generate_usage')
    def test_servicenet_load_balancer(self):
        '''Generate servicenet load balancer'''
        self.usage_data.add_section(helpers.function_name())
        r = self.lbaas_provider.create_active_load_balancer(
                                           virtualIps=[{'type': 'SERVICENET'}])
        self.usage_data.set(helpers.function_name(),
                            UsageKeys.LOAD_BALANCER_ID_FIELD,
                            str(r.entity.id))
        self.usage_data.set(helpers.function_name(),
                            UsageKeys.CREATE_TIME,
                            datetime.datetime.utcnow().isoformat())
        helpers.write_usage_data(self.usage_data, UsageKeys.UPTIME_FILENAME)
