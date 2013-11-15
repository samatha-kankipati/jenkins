from testrepo.common.testfixtures.load_balancers import \
                                            LoadBalancersAssertUsageFixture
from ccengine.common.decorators import attr
from testrepo.lbaas.usage import UsageKeys
import unittest
import ConfigParser


class TestAvgConcurrentConnections(LoadBalancersAssertUsageFixture):

    @classmethod
    def setUpClass(cls):
        super(TestAvgConcurrentConnections, cls).setUpClass()
        cls.usage_data = ConfigParser.ConfigParser()
        path = '/'.join([UsageKeys.USAGE_DATA_PATH, UsageKeys.ACC_FILENAME])
        cls.usage_data.read(path)

    @classmethod
    def tearDownClass(cls):
        super(TestAvgConcurrentConnections, cls).tearDownClass()

    @attr('assert_usage')
    def test_average_concurrent_connections(self):
        '''Assert average concurrent connections.'''
        section = 'test_average_concurrent_connections'
        lb_id = self.usage_data.get(section, UsageKeys.LOAD_BALANCER_ID_FIELD)
        r = self.lbaas_provider.client.list_load_balancer_usage(lb_id)
        records = r.entity.loadBalancerUsageRecords
        acc_list = [record for record in records
                    if 99 < (float(record.averageNumConnections) * float(record.numPolls)) < 101]
        self.assertNotEqual(len(acc_list), 0, "Should be at least 1 record "
                            "with averageNumConnections")
        ssl_acc_list = [record for record in records
                        if float(record.averageNumConnectionsSsl) > 0]
        self.assertEquals(len(ssl_acc_list), 0,
                              "Should not be any records with ssl acc.")

    @attr('assert_usage')
    def test_average_concurrent_connections_ssl(self):
        '''Assert SSL average concurrent connections.'''
        section = 'test_average_concurrent_connections_ssl'
        lb_id = self.usage_data.get(section, UsageKeys.LOAD_BALANCER_ID_FIELD)
        r = self.lbaas_provider.client.list_load_balancer_usage(lb_id)
        records = r.entity.loadBalancerUsageRecords
        ssl_acc_list = [record for record in records
                        if 99 < (float(record.averageNumConnectionsSsl) * float(record.numPolls)) < 101]
        self.assertNotEqual(len(ssl_acc_list), 0, "Should be at least 1 "\
                            "record with averageNumConnections")
        acc_list = [record for record in records
                    if float(record.averageNumConnections) > 0]
        self.assertEquals(len(acc_list), 0,
                          "Should not be any records with normal acc.")

    @unittest.skip('Unfinished')
    @attr('generate_usage')
    def test_servicenet_average_concurrent_connections(self):
        '''Generate servicenet average concurrent connections.'''
        pass
