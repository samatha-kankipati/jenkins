from testrepo.common.testfixtures.load_balancers \
    import LoadBalancersConnectionLogFixture, LoadBalancersSmokeFixture
from ccengine.common.decorators import attr
from ccengine.domain.types import LoadBalancerStatusTypes as LBStatus
import os


class ConnectionLoggingSmokeTests(LoadBalancersSmokeFixture):

    @attr('smoke', 'positive')
    def test_functional_connection_logging(self):
        """Testing connection logging update and get operations"""
        r = self.client.update_connection_logging(self.lb.id,
                                                  enabled=True)
        self.assertEquals(r.status_code, 202)
        self.lbaas_provider.wait_for_status(self.lb.id, LBStatus.ACTIVE)
        r = self.client.get_connection_logging(self.lb.id)
        self.assertEquals(r.status_code, 200)
        self.assertTrue(r.entity.enabled)
        r = self.client.update_connection_logging(self.lb.id,
                                                  enabled=False)
        self.assertEquals(r.status_code, 202)
        self.lbaas_provider.wait_for_status(self.lb.id, LBStatus.ACTIVE)
        r = self.client.get_connection_logging(self.lb.id)
        self.assertEquals(r.status_code, 200)
        self.assertFalse(r.entity.enabled)


class ConnectionLoggingTests(LoadBalancersConnectionLogFixture):

    @classmethod
    def setUpClass(cls):
        super(ConnectionLoggingTests, cls).setUpClass()
        vips = [{'type': 'PUBLIC'}]
        cls.lb = cls.lbaas_provider.create_active_load_balancer(
            virtualIps=vips).entity
        cls.zeus_vs_name = '{0}_{1}'.format(cls.tenant_id, cls.lb.id)
        cls.jenkins_job = cls.config.lbaas_api.connection_log_job

    def setUp(self):
        super(ConnectionLoggingTests, self).setUp()
        self.lbaas_provider.wait_for_status(self.lb.id)
        self.client.update_connection_logging(self.lb.id, enabled=False)
        self.lbaas_provider.wait_for_status(self.lb.id)

    @attr('positive')
    def test_connection_logging_with_zeus(self):
        '''Verify connection logging is set up correctly in Zeus.'''
        r = self.client.get_load_balancer(self.lb.id)
        self.assertEquals(r.entity.connectionLogging.enabled, False)
        r = self.client.get_connection_logging(self.lb.id)
        self.assertEquals(r.entity.enabled, False)
        zeus_resp = self.zeus_vs.getLogEnabled([self.zeus_vs_name])
        self.assertEquals(zeus_resp[1][0], False)
        r = self.client.update_connection_logging(self.lb.id, enabled=True)
        self.assertEquals(r.status_code, 202)
        r = self.lbaas_provider.wait_for_status(self.lb.id)
        self.assertEquals(r.entity.status, LBStatus.ACTIVE)
        self.assertEquals(r.entity.connectionLogging.enabled, True)
        r = self.client.get_connection_logging(self.lb.id)
        self.assertEquals(r.entity.enabled, True)
        zeus_resp = self.zeus_vs.getLogEnabled([self.zeus_vs_name])
        self.assertEquals(zeus_resp[1][0], True)
        r = self.client.update_connection_logging(self.lb.id, enabled=False)
        self.assertEquals(r.status_code, 202)
        r = self.lbaas_provider.wait_for_status(self.lb.id)
        self.assertEquals(r.entity.status, LBStatus.ACTIVE)
        self.assertEquals(r.entity.connectionLogging.enabled, False)
        r = self.client.get_connection_logging(self.lb.id)
        self.assertEquals(r.entity.enabled, False)
        zeus_resp = self.zeus_vs.getLogEnabled([self.zeus_vs_name])
        self.assertEquals(zeus_resp[1][0], False)

    @attr('positive')
    def test_generate_connection_logs(self):
        '''Generate connection logs on a load balancer.'''
        r = self.client.update_connection_logging(self.lb.id, enabled=True)
        self.assertEquals(r.status_code, 202)
        self.lbaas_provider.wait_for_status(self.lb.id)
        ip = self.lb.virtualIps.get_ipv4_vips()[0].address
        x = 0
        while x < 3:
            self.lbaas_provider.generate_bandwidth_out(ip=ip,
                                                       path='')
            x += 1
        job_url = '{0}/{1}/buildWithParameters?delay=7200sec&LBID={2}'.format(
            self.config.lbaas_api.jenkins_url,
            self.config.lbaas_api.connection_log_job,
            self.lb.id)
        self.client.get(job_url)

    @attr('positive')
    def test_log_region_matches_lb_region(self):
        '''Test that the LB id is in the logs for the region'''
        if self.jenkins_job not in os.getcwd():
            self.fail('Unable able to continue. Need lbid.out file.')
        lb_id = open("lbid.out", "r").read().rstrip()
        r = self.files_client.list_containers()
        self.assertEquals(r.status_code, 200)
        in_logs = False
        for line in r.content.splitlines():
            if line.startswith('lb_{0}'.format(lb_id)):
                in_logs = True
        self.assertTrue(in_logs)
        os.remove("lbid.out")
