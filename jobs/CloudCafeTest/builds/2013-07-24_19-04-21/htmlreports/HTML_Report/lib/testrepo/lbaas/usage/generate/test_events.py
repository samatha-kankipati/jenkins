from testrepo.common.testfixtures.load_balancers import \
    LoadBalancersGenerateUsageFixture
from testrepo.lbaas.usage import UsageKeys
import testrepo.lbaas.usage.generate.generate_helpers as helpers
from ccengine.common.decorators import attr
import ConfigParser
import datetime


class TestEvents(LoadBalancersGenerateUsageFixture):

    SSL_SITE_PREFIX = 'sslterm'

    @classmethod
    def setUpClass(cls):
        super(TestEvents, cls).setUpClass()
        cls.usage_data = ConfigParser.SafeConfigParser()

    @classmethod
    def tearDownClass(cls):
        super(TestEvents, cls).tearDownClass()

    @attr('generate_usage')
    def test_create_delete_events(self):
        """Generate create and delete events."""
        self.usage_data.add_section(helpers.function_name())
        r = self.lbaas_provider.create_active_load_balancer()
        self.usage_data.set(helpers.function_name(),
                            UsageKeys.LOAD_BALANCER_ID_FIELD,
                            str(r.entity.id))
        self.usage_data.set(helpers.function_name(),
                            UsageKeys.CREATE_TIME,
                            datetime.datetime.utcnow().isoformat())
        r = self.lbaas_provider.client.delete_load_balancer(r.entity.id)
        helpers.write_usage_data(self.usage_data, UsageKeys.EVENTS_FILENAME)

    @attr('generate_usage')
    def test_virtual_ips(self):
        """Generate CREATE_VIRTUAL_IP and DELETE_VIRTUAL_IP events."""
        self.usage_data.add_section(helpers.function_name())
        lb = self.lbaas_provider.create_active_load_balancer().entity
        self.usage_data.set(helpers.function_name(),
                            UsageKeys.LOAD_BALANCER_ID_FIELD,
                            str(lb.id))
        self.usage_data.set(helpers.function_name(),
                            UsageKeys.CREATE_TIME,
                            datetime.datetime.utcnow().isoformat())
        r = self.lbaas_provider.add_virtual_ip(lb.id)
        vip_id = r.entity.id
        r = self.lbaas_provider.client.get_load_balancer(lb.id)
        self.assertEquals(len(r.entity.virtualIps), 3)
        num_vips = 2
        self.usage_data.set(helpers.function_name(),
                            UsageKeys.NUM_VIPS, str(num_vips))
        r = self.lbaas_provider.client.delete_virtual_ip(lb.id, vip_id)
        assert r.ok
        helpers.write_usage_data(self.usage_data, UsageKeys.EVENTS_FILENAME)

    @attr('generate_usage')
    def test_ssl_termination_events(self):
        """Generate ssl term events: SSL_ONLY_ON, SSL_MIXED_ON, SSL_OFF"""
        self.usage_data.add_section(helpers.function_name())
        lb = self.lbaas_provider.create_active_load_balancer().entity
        self.usage_data.set(helpers.function_name(),
                            UsageKeys.LOAD_BALANCER_ID_FIELD,
                            str(lb.id))
        self.usage_data.set(helpers.function_name(),
                            UsageKeys.CREATE_TIME,
                            datetime.datetime.utcnow().isoformat())
        self.lbaas_provider.ssl_only_on(lb.id)
        self.lbaas_provider.ssl_mixed_on(lb.id)
        self.lbaas_provider.ssl_disabled(lb.id)
        helpers.write_usage_data(self.usage_data, UsageKeys.EVENTS_FILENAME)

    @attr('generate_usage')
    def test_suspension_events(self):
        """Generate SUSPEND and UNSUSPEND events."""
        self.usage_data.add_section(helpers.function_name())
        lb = self.lbaas_provider.create_active_load_balancer().entity
        self.usage_data.set(helpers.function_name(),
                            UsageKeys.LOAD_BALANCER_ID_FIELD,
                            str(lb.id))
        self.usage_data.set(helpers.function_name(),
                            UsageKeys.CREATE_TIME,
                            datetime.datetime.utcnow().isoformat())
        self.lbaas_provider.suspend_load_balancer(lb.id)
        self.lbaas_provider.unsuspend_load_balancer(lb.id)
        helpers.write_usage_data(self.usage_data, UsageKeys.EVENTS_FILENAME)

    @attr('generate_usage')
    def test_delete_lb_while_ssl_only_on(self):
        """Generate SSL_ONLY_ON event and delete load balancer."""
        self.usage_data.add_section(helpers.function_name())
        lb = self.lbaas_provider.create_active_load_balancer().entity
        self.usage_data.set(helpers.function_name(),
                            UsageKeys.LOAD_BALANCER_ID_FIELD,
                            str(lb.id))
        self.usage_data.set(helpers.function_name(),
                            UsageKeys.CREATE_TIME,
                            datetime.datetime.utcnow().isoformat())
        self.lbaas_provider.ssl_only_on(lb.id)
        r = self.lbaas_provider.client.delete_load_balancer(lb.id)
        self.assertEquals(r.status_code, 202)
        helpers.write_usage_data(self.usage_data, UsageKeys.EVENTS_FILENAME)

    @attr('generate_usage')
    def test_delete_lb_while_ssl_mixed_on(self):
        """Generate SSL_MIXED_ON event and delete load balancer."""
        self.usage_data.add_section(helpers.function_name())
        lb = self.lbaas_provider.create_active_load_balancer().entity
        self.usage_data.set(helpers.function_name(),
                            UsageKeys.LOAD_BALANCER_ID_FIELD,
                            str(lb.id))
        self.usage_data.set(helpers.function_name(),
                            UsageKeys.CREATE_TIME,
                            datetime.datetime.utcnow().isoformat())
        self.lbaas_provider.ssl_mixed_on(lb.id)
        r = self.lbaas_provider.client.delete_load_balancer(lb.id)
        self.assertEquals(r.status_code, 202)
        helpers.write_usage_data(self.usage_data, UsageKeys.EVENTS_FILENAME)

    @attr('generate_usage')
    def test_delete_lb_while_suspended(self):
        """Generate SUSPEND event and then delete load balancer."""
        self.usage_data.add_section(helpers.function_name())
        lb = self.lbaas_provider.create_active_load_balancer().entity
        self.usage_data.set(helpers.function_name(),
                            UsageKeys.LOAD_BALANCER_ID_FIELD,
                            str(lb.id))
        self.usage_data.set(helpers.function_name(),
                            UsageKeys.CREATE_TIME,
                            datetime.datetime.utcnow().isoformat())
        self.lbaas_provider.suspend_load_balancer(lb.id)
        r = self.lbaas_provider.\
            mgmt_client.delete_suspended_load_balancer(lb.id)
        assert r.ok
        helpers.write_usage_data(self.usage_data, UsageKeys.EVENTS_FILENAME)

    @attr('generate_usage')
    def test_delete_lb_after_adding_virtual_ip(self):
        """Generate CREATE_VIRTUAL_IP event, then delete load balancer."""
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
        num_vips = 2
        self.assertEquals(len(r.entity.virtualIps), num_vips + 1)
        r = self.lbaas_provider.client.delete_load_balancer(lb.id)
        assert r.ok
        helpers.write_usage_data(self.usage_data, UsageKeys.EVENTS_FILENAME)

    @attr('generate_usage', 'new_usage')
    def test_suspended_event(self):
        """Generate suspended load balancer that remains suspended."""
        self.usage_data.add_section(helpers.function_name())
        lb = self.lbaas_provider.create_active_load_balancer().entity
        self.usage_data.set(helpers.function_name(),
                            UsageKeys.LOAD_BALANCER_ID_FIELD,
                            str(lb.id))
        self.usage_data.set(helpers.function_name(),
                            UsageKeys.CREATE_TIME,
                            datetime.datetime.utcnow().isoformat())
        self.lbaas_provider.suspend_load_balancer(lb.id)
        helpers.write_usage_data(self.usage_data, UsageKeys.EVENTS_FILENAME)
