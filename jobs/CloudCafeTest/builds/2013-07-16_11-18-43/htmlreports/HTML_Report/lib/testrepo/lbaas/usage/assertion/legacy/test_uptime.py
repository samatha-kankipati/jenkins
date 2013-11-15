from testrepo.common.testfixtures.load_balancers import \
                                            LoadBalancersAssertUsageFixture
from ccengine.common.decorators import attr
from testrepo.lbaas.usage import UsageKeys
from ccengine.domain.types import LoadBalancerUsageEventTypes as LBUETypes, \
                                  LoadBalancerSslModes as LBSModes, \
                                  LoadBalancerVirtualIpTypes as LBVipTypes
import testrepo.lbaas.usage.assertion.legacy.assert_helpers as helpers
import testrepo.lbaas.usage.assertion as assertion_utils
import dateutil.parser
import ConfigParser


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
        lb_id = assertion_utils.get_usage_data(self.usage_data, section, UsageKeys.LOAD_BALANCER_ID_FIELD)
        r = self.lbaas_provider.client.list_load_balancer_usage(lb_id)
        records = r.entity.loadBalancerUsageRecords
        event_order = [LBUETypes.CREATE_LOADBALANCER]
        helpers.verify_records_times(records, event_order)
        for rec in records:
            if rec.eventType == LBUETypes.DELETE_LOADBALANCER:
                helpers.verify_record_properties(rec, numVips=0)
            else:
                helpers.verify_record_properties(rec)

    @attr('assert_usage')
    def test_ssl_only_load_balancer_uptime(self):
        '''Assert uptime for an ssl only load balancer.'''
        section = 'test_ssl_only_load_balancer_uptime'
        if not self.usage_data.has_section(section):
            return
        lb_id = assertion_utils.get_usage_data(self.usage_data, section, UsageKeys.LOAD_BALANCER_ID_FIELD)
        r = self.lbaas_provider.client.list_load_balancer_usage(lb_id)
        records = r.entity.loadBalancerUsageRecords
        event_order = [LBUETypes.CREATE_LOADBALANCER,
                       LBUETypes.SSL_ONLY_ON]
        helpers.verify_records_times(records, event_order)
        ssl_on = False
        for rec in records:
            if not ssl_on and rec.eventType != LBUETypes.SSL_ONLY_ON:
                helpers.verify_record_properties(rec)
            elif rec.eventType == LBUETypes.DELETE_LOADBALANCER:
                helpers.verify_record_properties(rec, numVips=0)
            else:
                ssl_on = True
                helpers.verify_record_properties(rec, sslMode=LBSModes.ON)

    @attr('assert_usage')
    def test_ssl_mixed_load_balancer_uptime(self):
        '''Assert uptime for an ssl mixed load balancer.'''
        section = 'test_ssl_mixed_load_balancer_uptime'
        if not self.usage_data.has_section(section):
            return
        lb_id = assertion_utils.get_usage_data(self.usage_data, section, UsageKeys.LOAD_BALANCER_ID_FIELD)
        r = self.lbaas_provider.client.list_load_balancer_usage(lb_id)
        records = r.entity.loadBalancerUsageRecords
        event_order = [LBUETypes.CREATE_LOADBALANCER,
                       LBUETypes.SSL_MIXED_ON]
        helpers.verify_records_times(records, event_order)
        ssl_on = False
        for rec in records:
            if not ssl_on and rec.eventType != LBUETypes.SSL_MIXED_ON:
                helpers.verify_record_properties(rec)
            elif rec.eventType == LBUETypes.DELETE_LOADBALANCER:
                helpers.verify_record_properties(rec, numVips=0)
            else:
                ssl_on = True
                helpers.verify_record_properties(rec, sslMode=LBSModes.MIXED)

    @attr('assert_usage')
    def test_virtual_ips_uptime(self):
        '''Assert uptime for load balancer with extra virtual ip.'''
        section = 'test_virtual_ips_uptime'
        if not self.usage_data.has_section(section):
            return
        lb_id = assertion_utils.get_usage_data(self.usage_data, section, UsageKeys.LOAD_BALANCER_ID_FIELD)
        num_vips = assertion_utils.get_usage_data(self.usage_data, section, UsageKeys.NUM_VIPS)
        num_vips = int(num_vips)
        r = self.lbaas_provider.client.list_load_balancer_usage(lb_id)
        records = r.entity.loadBalancerUsageRecords
        event_order = [LBUETypes.CREATE_LOADBALANCER,
                       LBUETypes.CREATE_VIRTUAL_IP]
        helpers.verify_records_times(records, event_order)
        extra_vip = False
        for rec in records:
            if not extra_vip and rec.eventType != LBUETypes.CREATE_VIRTUAL_IP:
                helpers.verify_record_properties(rec,
                                                 numVips=num_vips - 1)
            elif rec.eventType == LBUETypes.DELETE_LOADBALANCER:
                helpers.verify_record_properties(rec, numVips=0)
            else:
                extra_vip = True
                helpers.verify_record_properties(rec, numVips=num_vips)

    @attr('assert_usage')
    def test_multiple_virtual_ips_uptime(self):
        '''Assert uptime for load balancer with extra virtual ips after CREATE and DELETE vips.'''
        section = 'test_multiple_virtual_ips_uptime'
        if not self.usage_data.has_section(section):
            return
        lb_id = assertion_utils.get_usage_data(self.usage_data, section, UsageKeys.LOAD_BALANCER_ID_FIELD)
        num_vips = assertion_utils.get_usage_data(self.usage_data, section, UsageKeys.NUM_VIPS)
        num_vips = int(num_vips)
        r = self.lbaas_provider.client.list_load_balancer_usage(lb_id)
        records = r.entity.loadBalancerUsageRecords
        event_order = [LBUETypes.CREATE_LOADBALANCER,
                       LBUETypes.CREATE_VIRTUAL_IP,
                       LBUETypes.CREATE_VIRTUAL_IP,
                       LBUETypes.DELETE_VIRTUAL_IP]
        helpers.verify_records_times(records, event_order)
        for i in range(len(event_order)):
            if i == 0:
                helpers.verify_record_properties(records[i], numVips=num_vips - 1)
            if i == 1:
                helpers.verify_record_properties(records[i], numVips=num_vips)
            if i == 2:
                helpers.verify_record_properties(records[i], numVips=num_vips + 1)
            if i == 3:
                helpers.verify_record_properties(records[i], numVips=num_vips)
        for i in range(len(event_order) - 1, len(records)):
            helpers.verify_record_properties(records[i], numVips=num_vips)

    @attr('assert_usage')
    def test_suspended_uptime(self):
        '''Assert uptime for load balancer in suspended status.'''
        section = 'test_suspended_uptime'
        if not self.usage_data.has_section(section):
            return
        lb_id = assertion_utils.get_usage_data(self.usage_data, section, UsageKeys.LOAD_BALANCER_ID_FIELD)
        r = self.lbaas_provider.client.list_load_balancer_usage(lb_id)
        records = r.entity.loadBalancerUsageRecords
        event_order = [LBUETypes.CREATE_LOADBALANCER,
                       LBUETypes.SUSPEND_LOADBALANCER]
        suspended_rec = False
        for rec in records:
            if rec.eventType == LBUETypes.DELETE_LOADBALANCER:
                suspended_rec = False
                event_order.append(LBUETypes.DELETE_LOADBALANCER)
            if suspended_rec:
                event_order.append(LBUETypes.SUSPENDED_LOADBALANCER)
            if rec.eventType == LBUETypes.SUSPEND_LOADBALANCER:
                suspended_rec = True
        helpers.verify_records_times(records, event_order)
        for rec in records:
            if rec.eventType == LBUETypes.DELETE_LOADBALANCER:
                helpers.verify_record_properties(rec, numVips=0)
            else:
                helpers.verify_record_properties(rec)

    @attr('assert_usage')
    def test_servicenet_load_balancer(self):
        '''Generate servicenet load balancer'''
        section = 'test_servicenet_load_balancer'
        if not self.usage_data.has_section(section):
            return
        lb_id = assertion_utils.get_usage_data(self.usage_data, section, UsageKeys.LOAD_BALANCER_ID_FIELD)
        r = self.lbaas_provider.client.list_load_balancer_usage(lb_id)
        records = r.entity.loadBalancerUsageRecords
        event_order = [LBUETypes.CREATE_LOADBALANCER]
        helpers.verify_records_times(records, event_order)
        for rec in records:
            if rec.eventType == LBUETypes.DELETE_LOADBALANCER:
                helpers.verify_record_properties(rec, numVips=0,
                                                 vipType=LBVipTypes.SERVICENET)
            else:
                helpers.verify_record_properties(rec,
                                                 vipType=LBVipTypes.SERVICENET)
