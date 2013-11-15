from testrepo.common.testfixtures.load_balancers import \
    LoadBalancersAssertUsageFixture
from ccengine.domain.types import LoadBalancerUsageEventTypes as LBUETypes
from ccengine.common.decorators import attr
from testrepo.lbaas.usage import UsageKeys
import ConfigParser


class TestBandwidth(LoadBalancersAssertUsageFixture):

    BANDWIDTH_ACCEPTANCE_RATIO = 0.33
    BANDWIDTH_ZERO_ACCEPTANCE = 1000

    @classmethod
    def setUpClass(cls):
        super(TestBandwidth, cls).setUpClass()
        cls.usage_data = ConfigParser.ConfigParser()
        path = '/'.join([UsageKeys.USAGE_DATA_PATH,
                         UsageKeys.BANDWIDTH_FILENAME])
        cls.usage_data.read(path)

    @classmethod
    def tearDownClass(cls):
        super(TestBandwidth, cls).tearDownClass()

    @attr('assert_usage')
    def test_normal_bandwidth(self):
        '''Assert bandwidth generated is correct.'''
        section = 'test_normal_bandwidth'
        lb_id = self.usage_data.get(section, UsageKeys.LOAD_BALANCER_ID_FIELD)
        generated_band_out = self.usage_data.get(section,
                                                 UsageKeys.BANDWIDTH_OUT_FIELD)
        generated_band_in = self.usage_data.get(section,
                                                UsageKeys.BANDWIDTH_IN_FIELD)
        r = self.lbaas_provider.client.list_load_balancer_usage(lb_id)
        records = r.entity.loadBalancerUsageRecords
        total_band_in = 0
        total_band_out = 0
        total_band_in_ssl = 0
        total_band_out_ssl = 0
        for record in records:
            total_band_in += record.incomingTransfer
            total_band_out += record.outgoingTransfer
            total_band_in_ssl += record.incomingTransferSsl
            total_band_out_ssl += record.outgoingTransferSsl
        generated_band_in = int(generated_band_in)
        generated_band_out = int(generated_band_out)
        band_in_delta = generated_band_in * self.BANDWIDTH_ACCEPTANCE_RATIO
        band_out_delta = generated_band_out * self.BANDWIDTH_ACCEPTANCE_RATIO
        self.assertNotEquals(total_band_in, 0, 'Bandwidth In should not be 0')
        self.assertNotEquals(total_band_out, 0,
                             'Bandwidth Out should not be 0')
        self.assertAlmostEqual(total_band_in, generated_band_in,
                   delta=band_in_delta,
                   msg="incomingTransfer not the same as what was generated.")
        self.assertAlmostEqual(total_band_out, generated_band_out,
                   delta=band_out_delta,
                   msg="outgoingTransfer not the same as what was generated.")
        self.assertEquals(total_band_in_ssl, 0,
                   msg="incomingTransferSsl should be 0.")
        self.assertEquals(total_band_out_ssl, 0,
                   msg="outgoingTransferSsl should be 0.")

    @attr('assert_usage')
    def test_ssl_termination_secure_traffic_only_bandwidth(self):
        '''Assert ssl only traffic.'''
        section = 'test_ssl_termination_secure_traffic_only_bandwidth'
        lb_id = self.usage_data.get(section, UsageKeys.LOAD_BALANCER_ID_FIELD)
        generated_band_out = 0
        generated_band_in = 0
        generated_band_out_ssl = self.usage_data.get(section,
                                            UsageKeys.BANDWIDTH_OUT_SSL_FIELD)
        generated_band_in_ssl = self.usage_data.get(section,
                                            UsageKeys.BANDWIDTH_IN_SSL_FIELD)
        r = self.lbaas_provider.client.list_load_balancer_usage(lb_id)
        records = r.entity.loadBalancerUsageRecords
        total_band_in = 0
        total_band_out = 0
        total_band_out_ssl = 0
        total_band_in_ssl = 0
        for record in records:
            total_band_in += record.incomingTransfer
            total_band_out += record.outgoingTransfer
            total_band_in_ssl += record.incomingTransferSsl
            total_band_out_ssl += record.outgoingTransferSsl
        generated_band_in_ssl = int(generated_band_in_ssl)
        generated_band_out_ssl = int(generated_band_out_ssl)
        band_in_delta_ssl = generated_band_in_ssl * \
                            self.BANDWIDTH_ACCEPTANCE_RATIO
        band_out_delta_ssl = generated_band_out_ssl * \
                            self.BANDWIDTH_ACCEPTANCE_RATIO
        self.assertEquals(total_band_in, generated_band_in,
                   msg="incomingTransfer should be 0.")
        self.assertEquals(total_band_out, generated_band_out,
                   msg="outgoingTransfer should be 0.")
        self.assertAlmostEqual(total_band_in_ssl, generated_band_in_ssl,
               delta=band_in_delta_ssl,
               msg="incomingTransferSsl not the same as what was generated.")
        self.assertAlmostEqual(total_band_out_ssl, generated_band_out_ssl,
               delta=band_out_delta_ssl,
               msg="outgoingTransferSsl not the same as what was generated.")

    @attr('assert_usage')
    def test_ssl_termination_secure_traffic_only_bandwidth_after_poller(self):
        '''Assert ssl only traffic after poll.'''
        section = "test_ssl_termination_secure_traffic_only_bandwidth_" \
                  "after_poller"
        lb_id = self.usage_data.get(section, UsageKeys.LOAD_BALANCER_ID_FIELD)
        generated_band_out = 0
        generated_band_in = 0
        generated_band_out_ssl = self.usage_data.get(section,
            UsageKeys.BANDWIDTH_OUT_SSL_FIELD)
        generated_band_in_ssl = self.usage_data.get(section,
            UsageKeys.BANDWIDTH_IN_SSL_FIELD)
        r = self.lbaas_provider.client.list_load_balancer_usage(lb_id)
        records = r.entity.loadBalancerUsageRecords
        total_band_in = 0
        total_band_out = 0
        total_band_out_ssl = 0
        total_band_in_ssl = 0
        for record in records:
            total_band_in += record.incomingTransfer
            total_band_out += record.outgoingTransfer
            total_band_in_ssl += record.incomingTransferSsl
            total_band_out_ssl += record.outgoingTransferSsl
        generated_band_in_ssl = int(generated_band_in_ssl)
        generated_band_out_ssl = int(generated_band_out_ssl)
        band_in_delta_ssl = generated_band_in_ssl * \
                            self.BANDWIDTH_ACCEPTANCE_RATIO
        band_out_delta_ssl = generated_band_out_ssl * \
                            self.BANDWIDTH_ACCEPTANCE_RATIO
        self.assertEquals(total_band_in, generated_band_in,
                   msg="incomingTransfer should be 0.")
        self.assertEquals(total_band_out, generated_band_out,
                   msg="outgoingTransfer should be 0.")
        self.assertAlmostEqual(total_band_in_ssl, generated_band_in_ssl,
               delta=band_in_delta_ssl,
               msg="incomingTransferSsl not the same as what was generated.")
        self.assertAlmostEqual(total_band_out_ssl, generated_band_out_ssl,
               delta=band_out_delta_ssl,
               msg="outgoingTransferSsl not the same as what was generated.")

    @attr('assert_usage')
    def test_ssl_termination_secure_and_normal_bandwidth(self):
        '''Assert ssl and normal bandwidth.'''
        section = 'test_ssl_termination_secure_and_normal_bandwidth'
        lb_id = self.usage_data.get(section, UsageKeys.LOAD_BALANCER_ID_FIELD)
        generated_band_out = self.usage_data.get(section,
                                                 UsageKeys.BANDWIDTH_OUT_FIELD)
        generated_band_in = self.usage_data.get(section,
                                                UsageKeys.BANDWIDTH_IN_FIELD)
        generated_band_out_ssl = self.usage_data.get(section,
                                            UsageKeys.BANDWIDTH_OUT_SSL_FIELD)
        generated_band_in_ssl = self.usage_data.get(section,
                                            UsageKeys.BANDWIDTH_IN_SSL_FIELD)
        r = self.lbaas_provider.client.list_load_balancer_usage(lb_id)
        records = r.entity.loadBalancerUsageRecords
        self.assertGreaterEqual(len(records), 1,
                                'Should be at least 1 records.')
        total_band_in = 0
        total_band_out = 0
        total_band_out_ssl = 0
        total_band_in_ssl = 0
        for record in records:
            total_band_in += record.incomingTransfer
            total_band_out += record.outgoingTransfer
            total_band_in_ssl += record.incomingTransferSsl
            total_band_out_ssl += record.outgoingTransferSsl
        generated_band_in = int(generated_band_in)
        generated_band_out = int(generated_band_out)
        band_in_delta = generated_band_in * self.BANDWIDTH_ACCEPTANCE_RATIO
        band_out_delta = generated_band_out * self.BANDWIDTH_ACCEPTANCE_RATIO
        generated_band_in_ssl = int(generated_band_in_ssl)
        generated_band_out_ssl = int(generated_band_out_ssl)
        band_in_delta_ssl = generated_band_in_ssl * \
                            self.BANDWIDTH_ACCEPTANCE_RATIO
        band_out_delta_ssl = generated_band_out_ssl * \
                            self.BANDWIDTH_ACCEPTANCE_RATIO
        self.assertNotEquals(total_band_in, 0, 'Bandwidth In should not be 0')
        self.assertNotEquals(total_band_out, 0,
                             'Bandwidth Out should not be 0')
        self.assertNotEquals(total_band_in_ssl, 0,
                             'SSL Bandwidth In should not be 0')
        self.assertNotEquals(total_band_out_ssl, 0,
                             'SSL Bandwidth Out should not be 0')
        self.assertAlmostEqual(total_band_in, generated_band_in,
                   delta=band_in_delta,
                   msg="incomingTransfer not the same as what was generated.")
        self.assertAlmostEqual(total_band_out, generated_band_out,
                   delta=band_out_delta,
                   msg="outgoingTransfer not the same as what was generated.")
        self.assertAlmostEqual(total_band_in_ssl, generated_band_in_ssl,
               delta=band_in_delta_ssl,
               msg="incomingTransferSsl not the same as what was generated.")
        self.assertAlmostEqual(total_band_out_ssl, generated_band_out_ssl,
               delta=band_out_delta_ssl,
               msg="outgoingTransferSsl not the same as what was generated.")

    @attr('assert_usage')
    def test_ssl_termination_secure_and_normal_bandwidth_after_poller(self):
        '''Assert ssl and normal bandwidth after poller.'''
        section = 'test_ssl_termination_secure_and_'\
                + 'normal_bandwidth_after_poller'
        lb_id = self.usage_data.get(section, UsageKeys.LOAD_BALANCER_ID_FIELD)
        generated_band_out = self.usage_data.get(section,
                                                 UsageKeys.BANDWIDTH_OUT_FIELD)
        generated_band_in = self.usage_data.get(section,
                                                UsageKeys.BANDWIDTH_IN_FIELD)
        generated_band_out_ssl = self.usage_data.get(section,
                                            UsageKeys.BANDWIDTH_OUT_SSL_FIELD)
        generated_band_in_ssl = self.usage_data.get(section,
                                            UsageKeys.BANDWIDTH_IN_SSL_FIELD)
        r = self.lbaas_provider.client.list_load_balancer_usage(lb_id)
        records = r.entity.loadBalancerUsageRecords
        self.assertGreaterEqual(len(records), 1,
                                'Should be at least 1 records.')
        total_band_in = 0
        total_band_out = 0
        total_band_out_ssl = 0
        total_band_in_ssl = 0
        for record in records:
            total_band_in += record.incomingTransfer
            total_band_out += record.outgoingTransfer
            total_band_in_ssl += record.incomingTransferSsl
            total_band_out_ssl += record.outgoingTransferSsl
        generated_band_in = int(generated_band_in)
        generated_band_out = int(generated_band_out)
        band_in_delta = generated_band_in * self.BANDWIDTH_ACCEPTANCE_RATIO
        band_out_delta = generated_band_out * self.BANDWIDTH_ACCEPTANCE_RATIO
        generated_band_in_ssl = int(generated_band_in_ssl)
        generated_band_out_ssl = int(generated_band_out_ssl)
        band_in_delta_ssl = generated_band_in_ssl * \
                            self.BANDWIDTH_ACCEPTANCE_RATIO
        band_out_delta_ssl = generated_band_out_ssl * \
                            self.BANDWIDTH_ACCEPTANCE_RATIO
        self.assertNotEquals(total_band_in, 0, 'Bandwidth In should not be 0')
        self.assertNotEquals(total_band_out, 0,
                             'Bandwidth Out should not be 0')
        self.assertNotEquals(total_band_in_ssl, 0,
                             'SSL Bandwidth In should not be 0')
        self.assertNotEquals(total_band_out_ssl, 0,
                             'SSL Bandwidth Out should not be 0')
        self.assertAlmostEqual(total_band_in, generated_band_in,
                   delta=band_in_delta,
                   msg="incomingTransfer not the same as what was generated.")
        self.assertAlmostEqual(total_band_out, generated_band_out,
                   delta=band_out_delta,
                   msg="outgoingTransfer not the same as what was generated.")
        self.assertAlmostEqual(total_band_in_ssl, generated_band_in_ssl,
               delta=band_in_delta_ssl,
               msg="incomingTransferSsl not the same as what was generated.")
        self.assertAlmostEqual(total_band_out_ssl, generated_band_out_ssl,
               delta=band_out_delta_ssl,
               msg="outgoingTransferSsl not the same as what was generated.")

    @attr('assert_usage')
    def test_normal_bandwidth_after_ssl_modes_toggled(self):
        '''Assert normal bandwidth after toggling ssl modes and back.'''
        section = 'test_normal_bandwidth_after_ssl_modes_toggled'
        lb_id = self.usage_data.get(section, UsageKeys.LOAD_BALANCER_ID_FIELD)
        generated_band_out = self.usage_data.get(section,
                                                 UsageKeys.BANDWIDTH_OUT_FIELD)
        generated_band_in = self.usage_data.get(section,
                                                UsageKeys.BANDWIDTH_IN_FIELD)
        r = self.lbaas_provider.client.list_load_balancer_usage(lb_id)
        records = r.entity.loadBalancerUsageRecords
        total_band_in = 0
        total_band_out = 0
        total_band_in_ssl = 0
        total_band_out_ssl = 0
        for record in records:
            total_band_in += record.incomingTransfer
            total_band_out += record.outgoingTransfer
            total_band_in_ssl += record.incomingTransferSsl
            total_band_out_ssl += record.outgoingTransferSsl
        generated_band_in = int(generated_band_in)
        generated_band_out = int(generated_band_out)
        band_in_delta = generated_band_in * self.BANDWIDTH_ACCEPTANCE_RATIO
        band_out_delta = generated_band_out * self.BANDWIDTH_ACCEPTANCE_RATIO
        self.assertNotEquals(total_band_in, 0, 'Bandwidth In should not be 0')
        self.assertNotEquals(total_band_out, 0,
                             'Bandwidth Out should not be 0')
        self.assertAlmostEqual(total_band_in, generated_band_in,
                   delta=band_in_delta,
                   msg="incomingTransfer not the same as what was generated.")
        self.assertAlmostEqual(total_band_out, generated_band_out,
                   delta=band_out_delta,
                   msg="outgoingTransfer not the same as what was generated.")
        self.assertEquals(total_band_in_ssl, 0,
                   msg="incomingTransferSsl should be 0.")
        self.assertEquals(total_band_out_ssl, 0,
                   msg="outgoingTransferSsl should be 0.")

    @attr('assert_usage')
    def test_normal_bandwidth_after_ssl_mixed(self):
        '''Assert normal bandwidth after ssl mixed.'''
        section = 'test_normal_bandwidth_after_ssl_mixed'
        lb_id = self.usage_data.get(section, UsageKeys.LOAD_BALANCER_ID_FIELD)
        generated_band_out = self.usage_data.get(section,
                                                 UsageKeys.BANDWIDTH_OUT_FIELD)
        generated_band_in = self.usage_data.get(section,
                                                UsageKeys.BANDWIDTH_IN_FIELD)
        generated_band_out_ssl = self.usage_data.get(section,
                                            UsageKeys.BANDWIDTH_OUT_SSL_FIELD)
        generated_band_in_ssl = self.usage_data.get(section,
                                            UsageKeys.BANDWIDTH_IN_SSL_FIELD)
        r = self.lbaas_provider.client.list_load_balancer_usage(lb_id)
        records = r.entity.loadBalancerUsageRecords
        total_band_in = 0
        total_band_out = 0
        total_band_in_ssl = 0
        total_band_out_ssl = 0
        for record in records:
            total_band_in += record.incomingTransfer
            total_band_out += record.outgoingTransfer
            total_band_in_ssl += record.incomingTransferSsl
            total_band_out_ssl += record.outgoingTransferSsl
        generated_band_in = int(generated_band_in)
        generated_band_out = int(generated_band_out)
        band_in_delta = generated_band_in * self.BANDWIDTH_ACCEPTANCE_RATIO
        band_out_delta = generated_band_out * self.BANDWIDTH_ACCEPTANCE_RATIO
        generated_band_in_ssl = int(generated_band_in_ssl)
        generated_band_out_ssl = int(generated_band_out_ssl)
        band_in_delta_ssl = generated_band_in_ssl * \
                            self.BANDWIDTH_ACCEPTANCE_RATIO
        band_out_delta_ssl = generated_band_out_ssl * \
                            self.BANDWIDTH_ACCEPTANCE_RATIO
        self.assertNotEquals(total_band_in, 0, 'Bandwidth In should not be 0')
        self.assertNotEquals(total_band_out, 0,
                             'Bandwidth Out should not be 0')
        self.assertNotEquals(total_band_in_ssl, 0,
                             'SSL Bandwidth In should not be 0')
        self.assertNotEquals(total_band_out_ssl, 0,
                             'SSL Bandwidth Out should not be 0')
        self.assertAlmostEqual(total_band_in, generated_band_in,
                   delta=band_in_delta,
                   msg="incomingTransfer not the same as what was generated.")
        self.assertAlmostEqual(total_band_out, generated_band_out,
                   delta=band_out_delta,
                   msg="outgoingTransfer not the same as what was generated.")
        self.assertAlmostEqual(total_band_in_ssl, generated_band_in_ssl,
                   delta=band_in_delta_ssl,
                   msg="incomingTransferSsl should be 0.")
        self.assertAlmostEqual(total_band_out_ssl, generated_band_out_ssl,
                   delta=band_out_delta_ssl,
                   msg="outgoingTransferSsl should be 0.")

    @attr('assert_usage')
    def test_normal_bandwidth_after_unsuspend(self):
        '''Assert bandwidth generated is correct.'''
        section = 'test_normal_bandwidth_after_unsuspend'
        lb_id = self.usage_data.get(section, UsageKeys.LOAD_BALANCER_ID_FIELD)
        generated_band_out = self.usage_data.get(section,
                                                 UsageKeys.BANDWIDTH_OUT_FIELD)
        generated_band_in = self.usage_data.get(section,
                                                UsageKeys.BANDWIDTH_IN_FIELD)
        r = self.lbaas_provider.client.list_load_balancer_usage(lb_id)
        records = r.entity.loadBalancerUsageRecords
        total_band_in = 0
        total_band_out = 0
        total_band_in_ssl = 0
        total_band_out_ssl = 0
        for record in records:
            total_band_in += record.incomingTransfer
            total_band_out += record.outgoingTransfer
            total_band_in_ssl += record.incomingTransferSsl
            total_band_out_ssl += record.outgoingTransferSsl
        generated_band_in = int(generated_band_in)
        generated_band_out = int(generated_band_out)
        band_in_delta = generated_band_in * self.BANDWIDTH_ACCEPTANCE_RATIO
        band_out_delta = generated_band_out * self.BANDWIDTH_ACCEPTANCE_RATIO
        self.assertNotEquals(total_band_in, 0, 'Bandwidth In should not be 0')
        self.assertNotEquals(total_band_out, 0,
                             'Bandwidth Out should not be 0')
        self.assertAlmostEqual(total_band_in, generated_band_in,
                   delta=band_in_delta,
                   msg="incomingTransfer not the same as what was generated.")
        self.assertAlmostEqual(total_band_out, generated_band_out,
                   delta=band_out_delta,
                   msg="outgoingTransfer not the same as what was generated.")
        self.assertEquals(total_band_in_ssl, 0,
                   msg="incomingTransferSsl should be 0.")
        self.assertEquals(total_band_out_ssl, 0,
                   msg="outgoingTransferSsl should be 0.")

    @attr('assert_usage')
    def test_ssl_bandwidth_across_ssl_states(self):
        '''Assert ssl bandwidth after SSL_ONLY_ON, then SSL_OFF, then SSL_ONLY_ON again.'''
        section = 'test_ssl_bandwidth_across_ssl_states'
        lb_id = self.usage_data.get(section, UsageKeys.LOAD_BALANCER_ID_FIELD)
        generated_band_out_ssl = float(self.usage_data.get(
            section, UsageKeys.BANDWIDTH_OUT_SSL_FIELD))
        generated_band_in_ssl = float(self.usage_data.get(
            section, UsageKeys.BANDWIDTH_IN_SSL_FIELD))
        generated_band_out_ssl2 = float(self.usage_data.get(
            section, UsageKeys.BANDWIDTH_OUT_SSL_FIELD_2))
        generated_band_in_ssl2 = float(self.usage_data.get(
            section, UsageKeys.BANDWIDTH_IN_SSL_FIELD_2))
        r = self.lbaas_provider.client.list_load_balancer_usage(lb_id)
        records = r.entity.loadBalancerUsageRecords
        is_first_ssl_only_on = True
        for record in records:
            if record.eventType == LBUETypes.SSL_ONLY_ON:
                if is_first_ssl_only_on:
                    is_first_ssl_only_on = False
                    self.assertAlmostEquals(
                        generated_band_out_ssl,
                        record.outgoingTransferSsl,
                        delta=generated_band_out_ssl *
                        self.BANDWIDTH_ACCEPTANCE_RATIO)
                    self.assertAlmostEquals(
                        generated_band_in_ssl, record.incomingTransferSsl,
                        delta=generated_band_in_ssl *
                        self.BANDWIDTH_ACCEPTANCE_RATIO)
                else:
                    self.assertAlmostEquals(generated_band_out_ssl2,
                                            record.outgoingTransferSsl,
                                            delta=generated_band_out_ssl2 *
                                            self.BANDWIDTH_ACCEPTANCE_RATIO)
                    self.assertAlmostEquals(generated_band_in_ssl2,
                                            record.incomingTransferSsl,
                                            delta=generated_band_in_ssl2 *
                                            self.BANDWIDTH_ACCEPTANCE_RATIO)

    @attr('assert_usage')
    def test_bandwidth_before_suspend_and_after_unsuspend(self):
        '''Assert bandwidth before suspending a load balancer and also after unsuspending it.'''
        section = 'test_bandwidth_before_suspend_and_after_unsuspend'
        self._assert_bandwidth_before_suspend_and_after_unsuspend(section)

    @attr('assert_usage')
    def test_bandwidth_before_suspend_and_after_unsuspend_wait_for_next_poll(self):
        '''Assert bandwidth before suspending a load balancer and also after unsuspending it.'''
        section = 'test_bandwidth_before_suspend_and_after_unsuspend_wait_for_next_poll'
        self._assert_bandwidth_before_suspend_and_after_unsuspend(section)

    @attr('assert_usage')
    def test_bandwidth_before_suspend_and_after_unsuspend_wait_after_two_polls(self):
        '''Assert bandwidth before suspending a load balancer and also after unsuspending it.'''
        section = 'test_bandwidth_before_suspend_and_after_unsuspend_wait_after_two_polls'
        self._assert_bandwidth_before_suspend_and_after_unsuspend(section)

    def _assert_bandwidth_before_suspend_and_after_unsuspend(self, section):
        lb_id = self.usage_data.get(section, UsageKeys.LOAD_BALANCER_ID_FIELD)
        generated_band_out = float(self.usage_data.get(
            section, UsageKeys.BANDWIDTH_OUT_FIELD))
        generated_band_in = float(self.usage_data.get(
            section, UsageKeys.BANDWIDTH_IN_FIELD))
        generated_band_out2 = float(self.usage_data.get(
            section, UsageKeys.BANDWIDTH_OUT_FIELD_2))
        generated_band_in2 = float(self.usage_data.get(
            section, UsageKeys.BANDWIDTH_IN_FIELD_2))
        r = self.lbaas_provider.client.list_load_balancer_usage(lb_id)
        records = r.entity.loadBalancerUsageRecords
        self.assertGreaterEqual(len(records), 3, "There should at least be 3"
                                "records (CREATE, SUSPEND, UNSUSPEND).")
        for index, rec in enumerate(records):
            if rec.eventType == LBUETypes.CREATE_LOADBALANCER:
                delt_out = generated_band_out * self.BANDWIDTH_ACCEPTANCE_RATIO
                delt_in = generated_band_in * self.BANDWIDTH_ACCEPTANCE_RATIO
                bandwidth_out = rec.outgoingTransfer
                bandwidth_in = rec.incomingTransfer
                if records[index + 1].eventType is None:
                    bandwidth_out += records[index + 1].outgoingTransfer
                    bandwidth_in += records[index + 1].incomingTransfer
                self.assertAlmostEquals(generated_band_out, bandwidth_out,
                                        delta=delt_out,
                                        msg="Bandwidth out does not "
                                        "fall within the acceptance criteria.")
                self.assertAlmostEquals(generated_band_in, bandwidth_in,
                                        delta=delt_in,
                                        msg="Bandwidth in does not "
                                        "fall within the acceptance criteria.")
            if rec.eventType == LBUETypes.SUSPEND_LOADBALANCER:
                self.assertEquals(0, rec.outgoingTransfer)
                self.assertEquals(0, rec.incomingTransfer)
            if rec.eventType == LBUETypes.UNSUSPEND_LOADBALANCER:
                delt_out = generated_band_out2 * self.BANDWIDTH_ACCEPTANCE_RATIO
                delt_in = generated_band_in2 * self.BANDWIDTH_ACCEPTANCE_RATIO
                bandwidth_out = rec.outgoingTransfer
                bandwidth_in = rec.incomingTransfer
                if len(records) >= index + 1:
                    bandwidth_out += records[index + 1].outgoingTransfer
                    bandwidth_in += records[index + 1].incomingTransfer
                self.assertAlmostEquals(generated_band_out2, bandwidth_out,
                                        delta=delt_out,
                                        msg="Bandwidth out does not "
                                        "fall within the acceptance criteria.")
                self.assertAlmostEquals(generated_band_in2, bandwidth_in,
                                        delta=delt_in,
                                        msg="Bandwidth in does not "
                                        "fall within the acceptance criteria.")

    @attr('assert_usage')
    def test_normal_bandwidth_across_ssl_states(self):
        """Assert normal bandwidth across ssl states."""
        section = 'test_normal_bandwidth_across_ssl_states'
        lb_id = self.usage_data.get(section, UsageKeys.LOAD_BALANCER_ID_FIELD)
        generated_band_out = float(self.usage_data.get(
            section, UsageKeys.BANDWIDTH_OUT_FIELD))
        generated_band_in = float(self.usage_data.get(
            section, UsageKeys.BANDWIDTH_IN_FIELD))
        generated_band_out2 = float(self.usage_data.get(
            section, UsageKeys.BANDWIDTH_OUT_FIELD_2))
        generated_band_in2 = float(self.usage_data.get(
            section, UsageKeys.BANDWIDTH_IN_FIELD_2))
        generated_band_out3 = float(self.usage_data.get(
            section, UsageKeys.BANDWIDTH_OUT_FIELD_3))
        generated_band_in3 = float(self.usage_data.get(
            section, UsageKeys.BANDWIDTH_IN_FIELD_3))
        r = self.lbaas_provider.client.list_load_balancer_usage(lb_id)
        records = r.entity.loadBalancerUsageRecords
        is_first_ssl_off = True
        for record in records:
            if record.eventType == LBUETypes.SSL_MIXED_ON:
                self.assertAlmostEquals(generated_band_out, record.outgoingTransfer,
                                        delta=generated_band_out * self.BANDWIDTH_ACCEPTANCE_RATIO)
                self.assertAlmostEquals(generated_band_in, record.incomingTransfer,
                                        delta=generated_band_in * self.BANDWIDTH_ACCEPTANCE_RATIO)
            if record.eventType == LBUETypes.SSL_ONLY_ON:
                self.assertEquals(0, record.outgoingTransfer)
                self.assertEquals(0, record.incomingTransfer)
            if record.eventType == LBUETypes.SSL_OFF:
                if is_first_ssl_off:
                    is_first_ssl_off = False
                    self.assertAlmostEquals(generated_band_out2, record.outgoingTransfer,
                                            delta=generated_band_out2 * self.BANDWIDTH_ACCEPTANCE_RATIO)
                    self.assertAlmostEquals(generated_band_in2, record.incomingTransfer,
                                            delta=generated_band_in2 * self.BANDWIDTH_ACCEPTANCE_RATIO)
                else:
                    self.assertAlmostEquals(generated_band_out3, record.outgoingTransfer,
                                            delta=generated_band_out3 * self.BANDWIDTH_ACCEPTANCE_RATIO)
                    self.assertAlmostEquals(generated_band_in3, record.incomingTransfer,
                                            delta=generated_band_in3 * self.BANDWIDTH_ACCEPTANCE_RATIO)

    @attr('assert_usage')
    def test_bandwidth_on_extra_virtual_ip(self):
        """Assert bandwidth on extra virtual IP is correct."""
        section = 'test_bandwidth_on_extra_virtual_ip'
        self._assert_virtual_ip_bandwidth(section)

    @attr('assert_usage')
    def test_bandwidth_on_extra_virtual_ip_after_poller(self):
        """Assert bandwidth on extra virtual IP is correct after poller."""
        section = 'test_bandwidth_on_extra_virtual_ip_after_poller'
        self._assert_virtual_ip_bandwidth(section)

    def _assert_virtual_ip_bandwidth(self, section):
        lb_id = self.usage_data.get(section, UsageKeys.LOAD_BALANCER_ID_FIELD)
        generated_band_out = self.usage_data.get(section,
                                                 UsageKeys.BANDWIDTH_OUT_FIELD)
        generated_band_in = self.usage_data.get(section,
                                                UsageKeys.BANDWIDTH_IN_FIELD)
        generated_band_out_ssl = self.usage_data.get(section,
                                            UsageKeys.BANDWIDTH_OUT_SSL_FIELD)
        generated_band_in_ssl = self.usage_data.get(section,
                                            UsageKeys.BANDWIDTH_IN_SSL_FIELD)
        r = self.lbaas_provider.client.list_load_balancer_usage(lb_id)
        records = r.entity.loadBalancerUsageRecords
        self.assertGreaterEqual(len(records), 1,
                                'Should be at least 1 records.')
        total_band_in = 0
        total_band_out = 0
        total_band_out_ssl = 0
        total_band_in_ssl = 0
        for record in records:
            total_band_in += record.incomingTransfer
            total_band_out += record.outgoingTransfer
            total_band_in_ssl += record.incomingTransferSsl
            total_band_out_ssl += record.outgoingTransferSsl
        generated_band_in = int(generated_band_in)
        generated_band_out = int(generated_band_out)
        band_in_delta = generated_band_in * self.BANDWIDTH_ACCEPTANCE_RATIO
        band_out_delta = generated_band_out * self.BANDWIDTH_ACCEPTANCE_RATIO
        generated_band_in_ssl = int(generated_band_in_ssl)
        generated_band_out_ssl = int(generated_band_out_ssl)
        band_in_delta_ssl = generated_band_in_ssl * \
                            self.BANDWIDTH_ACCEPTANCE_RATIO
        band_out_delta_ssl = generated_band_out_ssl * \
                            self.BANDWIDTH_ACCEPTANCE_RATIO
        self.assertNotEquals(total_band_in, 0, 'Bandwidth In should not be 0')
        self.assertNotEquals(total_band_out, 0,
                             'Bandwidth Out should not be 0')
        self.assertNotEquals(total_band_in_ssl, 0,
                             'SSL Bandwidth In should not be 0')
        self.assertNotEquals(total_band_out_ssl, 0,
                             'SSL Bandwidth Out should not be 0')
        self.assertAlmostEqual(total_band_in, generated_band_in,
                   delta=band_in_delta,
                   msg="incomingTransfer not the same as what was generated.")
        self.assertAlmostEqual(total_band_out, generated_band_out,
                   delta=band_out_delta,
                   msg="outgoingTransfer not the same as what was generated.")
        self.assertAlmostEqual(total_band_in_ssl, generated_band_in_ssl,
               delta=band_in_delta_ssl,
               msg="incomingTransferSsl not the same as what was generated.")
        self.assertAlmostEqual(total_band_out_ssl, generated_band_out_ssl,
               delta=band_out_delta_ssl,
               msg="outgoingTransferSsl not the same as what was generated.")

