import unittest
import dateutil
from testrepo.common.testfixtures.load_balancers import \
                                            LoadBalancersAssertUsageFixture
from ccengine.common.decorators import attr
from testrepo.lbaas.usage import UsageKeys
from ccengine.domain.types import LoadBalancerUsageEventTypes as LBUETypes, \
                                  LoadBalancerSslModes as LBSModes
import testrepo.lbaas.usage.assertion.legacy.assert_helpers as helpers
import testrepo.lbaas.usage.assertion as assertion_utils
import ConfigParser


class TestEvents(LoadBalancersAssertUsageFixture):

    @classmethod
    def setUpClass(cls):
        super(TestEvents, cls).setUpClass()
        cls.usage_data = ConfigParser.ConfigParser()
        path = '/'.join([UsageKeys.USAGE_DATA_PATH, UsageKeys.EVENTS_FILENAME])
        cls.usage_data.read(path)

    @classmethod
    def tearDownClass(cls):
        super(TestEvents, cls).tearDownClass()

    @attr('assert_usage')
    def test_create_delete_events(self):
        '''Check create and delete events.'''
        section = 'test_create_delete_events'
        if not self.usage_data.has_section(section):
            return
        lb_id = assertion_utils.get_usage_data(self.usage_data, section, UsageKeys.LOAD_BALANCER_ID_FIELD)
        r = self.lbaas_provider.client.list_load_balancer_usage(lb_id)
        records = r.entity.loadBalancerUsageRecords
        event_order = [LBUETypes.CREATE_LOADBALANCER,
                       LBUETypes.DELETE_LOADBALANCER]
        helpers.verify_records_times(records, event_order)
        for rec in records:
            if rec.eventType == LBUETypes.DELETE_LOADBALANCER:
                helpers.verify_record_properties(rec, numVips=0)
            else:
                helpers.verify_record_properties(rec)

    @attr('assert_usage')
    def test_virtual_ips(self):
        '''Assert CREATE_VIRTUAL_IP and DELETE_VIRTUAL_IP events occur.'''
        section = 'test_virtual_ips'
        if not self.usage_data.has_section(section):
            return
        lb_id = assertion_utils.get_usage_data(self.usage_data, section, UsageKeys.LOAD_BALANCER_ID_FIELD)
        num_vips = int(assertion_utils.get_usage_data(self.usage_data, section, UsageKeys.NUM_VIPS))
        r = self.lbaas_provider.client.list_load_balancer_usage(lb_id)
        records = r.entity.loadBalancerUsageRecords
        event_order = [LBUETypes.CREATE_LOADBALANCER,
                       LBUETypes.CREATE_VIRTUAL_IP,
                       LBUETypes.DELETE_VIRTUAL_IP]
        helpers.verify_records_times(records, event_order)
        extra_vip = False
        for rec in records:
            if not extra_vip and rec.eventType != LBUETypes.CREATE_VIRTUAL_IP:
                helpers.verify_record_properties(rec,
                                                 numVips=num_vips - 1)
            elif rec.eventType == LBUETypes.DELETE_LOADBALANCER:
                helpers.verify_record_properties(rec, numVips=0)
            elif rec.eventType == LBUETypes.DELETE_VIRTUAL_IP:
                extra_vip = False
                helpers.verify_record_properties(rec, numVips=num_vips - 1)
            else:
                extra_vip = True
                helpers.verify_record_properties(rec, numVips=num_vips)

    @attr('assert_usage', 'new')
    def test_ssl_termination_events(self):
        '''Assert ssl termination events.'''
        section = 'test_ssl_termination_events'
        if not self.usage_data.has_section(section):
            return
        lb_id = assertion_utils.get_usage_data(self.usage_data, section, UsageKeys.LOAD_BALANCER_ID_FIELD)
        r = self.lbaas_provider.client.list_load_balancer_usage(lb_id)
        records = r.entity.loadBalancerUsageRecords
        event_order = [LBUETypes.CREATE_LOADBALANCER,
                       LBUETypes.SSL_ONLY_ON,
                       LBUETypes.SSL_MIXED_ON,
                       LBUETypes.SSL_OFF]
        helpers.verify_records_times(records, event_order)
        ssl_only_on = False
        ssl_mixed_on = False
        for rec in records:
            if rec.eventType == LBUETypes.DELETE_LOADBALANCER:
                helpers.verify_record_properties(rec, numVips=0)
                continue
            if rec.eventType == LBUETypes.SSL_ONLY_ON:
                ssl_mixed_on = False
                ssl_only_on = True
            if rec.eventType == LBUETypes.SSL_MIXED_ON:
                ssl_mixed_on = True
                ssl_only_on = False
            if rec.eventType == LBUETypes.SSL_OFF:
                ssl_mixed_on = False
                ssl_only_on = False
            if ssl_only_on:
                helpers.verify_record_properties(rec, sslMode=LBSModes.ON)
            if ssl_mixed_on:
                helpers.verify_record_properties(rec, sslMode=LBSModes.MIXED)
            if not ssl_only_on and not ssl_mixed_on:
                helpers.verify_record_properties(rec)

    @attr('assert_usage')
    def test_suspension_events(self):
        '''Assert suspension events were created.'''
        section = 'test_suspension_events'
        if not self.usage_data.has_section(section):
            return
        lb_id = assertion_utils.get_usage_data(self.usage_data, section, UsageKeys.LOAD_BALANCER_ID_FIELD)
        r = self.lbaas_provider.client.list_load_balancer_usage(lb_id)
        records = r.entity.loadBalancerUsageRecords
        event_order = [LBUETypes.CREATE_LOADBALANCER,
                       LBUETypes.SUSPEND_LOADBALANCER,
                       LBUETypes.UNSUSPEND_LOADBALANCER]
        helpers.verify_records_times(records, event_order)
        for rec in records:
            if rec.eventType == LBUETypes.DELETE_LOADBALANCER:
                helpers.verify_record_properties(rec, numVips=0)
            else:
                helpers.verify_record_properties(rec)

    @attr('assert_usage')
    def test_delete_lb_while_ssl_only_on(self):
        '''Assert SSL_OFF didn't occur after SSL_ONLY_ON on LB delete.'''
        section = 'test_delete_lb_while_ssl_only_on'
        if not self.usage_data.has_section(section):
            return
        lb_id = assertion_utils.get_usage_data(self.usage_data, section, UsageKeys.LOAD_BALANCER_ID_FIELD)
        r = self.lbaas_provider.client.list_load_balancer_usage(lb_id)
        records = r.entity.loadBalancerUsageRecords
        event_order = [LBUETypes.CREATE_LOADBALANCER,
                       LBUETypes.SSL_ONLY_ON,
                       LBUETypes.DELETE_LOADBALANCER]
        helpers.verify_records_times(records, event_order)
        ssl_on = False
        for rec in records:
            if rec.eventType == LBUETypes.SSL_ONLY_ON:
                ssl_on = True
                helpers.verify_record_properties(rec, sslMode=LBSModes.ON)
            if rec.eventType == LBUETypes.DELETE_LOADBALANCER:
                ssl_on = False
                helpers.verify_record_properties(rec, numVips=0)
            if ssl_on:
                helpers.verify_record_properties(rec, sslMode=LBSModes.ON)
            elif not ssl_on and rec.eventType != LBUETypes.DELETE_LOADBALANCER:
                helpers.verify_record_properties(rec)

    @attr('assert_usage')
    def test_delete_lb_while_ssl_mixed_on(self):
        '''Assert SSL_OFF didn't occur after SSL_MIXED_ON on LB delete.'''
        section = 'test_delete_lb_while_ssl_mixed_on'
        if not self.usage_data.has_section(section):
            return
        lb_id = assertion_utils.get_usage_data(self.usage_data, section, UsageKeys.LOAD_BALANCER_ID_FIELD)
        r = self.lbaas_provider.client.list_load_balancer_usage(lb_id)
        records = r.entity.loadBalancerUsageRecords
        event_order = [LBUETypes.CREATE_LOADBALANCER,
                       LBUETypes.SSL_MIXED_ON,
                       LBUETypes.DELETE_LOADBALANCER]
        helpers.verify_records_times(records, event_order)
        ssl_on = False
        for rec in records:
            if rec.eventType == LBUETypes.SSL_MIXED_ON:
                ssl_on = True
                helpers.verify_record_properties(rec, sslMode=LBSModes.MIXED)
            if rec.eventType == LBUETypes.DELETE_LOADBALANCER:
                ssl_on = False
                helpers.verify_record_properties(rec, numVips=0)
            if ssl_on:
                helpers.verify_record_properties(rec, sslMode=LBSModes.MIXED)
            elif not ssl_on and rec.eventType != LBUETypes.DELETE_LOADBALANCER:
                helpers.verify_record_properties(rec)

    @attr('assert_usage')
    def test_delete_lb_while_suspended(self):
        '''Assert UNSUSPEND event didn't occur after suspended LB deletion.'''
        section = 'test_delete_lb_while_suspended'
        if not self.usage_data.has_section(section):
            return
        lb_id = assertion_utils.get_usage_data(self.usage_data, section, UsageKeys.LOAD_BALANCER_ID_FIELD)
        r = self.lbaas_provider.client.list_load_balancer_usage(lb_id)
        records = r.entity.loadBalancerUsageRecords
        event_order = [LBUETypes.CREATE_LOADBALANCER,
                       LBUETypes.SUSPEND_LOADBALANCER,
                       LBUETypes.DELETE_LOADBALANCER]
        helpers.verify_records_times(records, event_order)
        for rec in records:
            if rec.eventType == LBUETypes.DELETE_LOADBALANCER:
                helpers.verify_record_properties(rec, numVips=0)
            else:
                helpers.verify_record_properties(rec)

    @attr('assert_usage')
    def test_delete_lb_after_adding_virtual_ip(self):
        '''Assert DELETE_VIRTUAL_IP event didn't occur after LB deletion.'''
        section = 'test_delete_lb_after_adding_virtual_ip'
        if not self.usage_data.has_section(section):
            return
        lb_id = assertion_utils.get_usage_data(self.usage_data, section, UsageKeys.LOAD_BALANCER_ID_FIELD)
        r = self.lbaas_provider.client.list_load_balancer_usage(lb_id)
        records = r.entity.loadBalancerUsageRecords
        event_order = [LBUETypes.CREATE_LOADBALANCER,
                       LBUETypes.CREATE_VIRTUAL_IP,
                       LBUETypes.DELETE_LOADBALANCER]
        helpers.verify_records_times(records, event_order)
        for rec in records:
            if rec.eventType == LBUETypes.CREATE_VIRTUAL_IP:
                helpers.verify_record_properties(rec, numVips=2)
            elif rec.eventType == LBUETypes.DELETE_LOADBALANCER:
                helpers.verify_record_properties(rec, numVips=0)
            else:
                helpers.verify_record_properties(rec)

    @attr('assert_usage')
    def test_suspended_event(self):
        """Assert suspended event when load balancer remains suspended."""
        section = 'test_suspended_event'
        if not self.usage_data.has_section(section):
            return
        lb_id = assertion_utils.get_usage_data(self.usage_data, section, UsageKeys.LOAD_BALANCER_ID_FIELD)
        r = self.lbaas_provider.client.list_load_balancer_usage(lb_id)
        records = r.entity.loadBalancerUsageRecords

        event_order = [LBUETypes.SUSPENDED_LOADBALANCER for _ in records]
        event_order[0] = LBUETypes.CREATE_LOADBALANCER
        event_order[1] = LBUETypes.SUSPEND_LOADBALANCER
        helpers.verify_records_times(records, event_order)
        for rec in records:
            if rec.eventType == LBUETypes.DELETE_LOADBALANCER:
                helpers.verify_record_properties(rec, numVips=0)
            else:
                helpers.verify_record_properties(rec)
                if rec.eventType == LBUETypes.SUSPENDED_LOADBALANCER:
                    startTime = dateutil.parser.parse(rec.startTime)
                    self.assertEquals(0, startTime.minute, "Record with {0} "
                        "event should start on the hour.".format(
                        LBUETypes.SUSPENDED_LOADBALANCER))
                    self.assertEquals(0, startTime.second, "Record with {0} "
                        "event should start on the hour.".format(
                        LBUETypes.SUSPENDED_LOADBALANCER))
