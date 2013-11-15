from testrepo.common.testfixtures.load_balancers import \
                                              LoadBalancersFixtureParameterized
from ccengine.common.loaders.base_parameterized_loader import \
                                                        BaseParameterizedLoader
from ccengine.common.data_generators.fuzz.data_generator import \
                                                         SecDataGeneratorString
from unittest2.suite import TestSuite
import json


def load_tests(loader, standard_tests, pattern):
    suite = TestSuite()

    #string fuzz
    data = SecDataGeneratorString(2)
    cluster_loader = BaseParameterizedLoader(data)
    cluster_loader.addTest(LbaasFuzz("fuzz_name"))
    suite.addTest(cluster_loader.getSuite())

    return suite


class LbaasFuzz(LoadBalancersFixtureParameterized):
    @classmethod
    def setUpClass(cls):
        super(LbaasFuzz, cls).setUpClass()
        cls.delete_lbs = []

    def tearDown(self):
        for loadbal in self.delete_lbs:
            if loadbal.status == 'ACTIVE':
                response = self.lbaas_provider.client.delete_load_balancer(
                                                                    loadbal.id)
            if loadbal.status == 'ERROR':
                response = self.lbaas_provider.mgmt_client.\
                                       delete_errored_load_balancer(loadbal.id)
            if loadbal.status == 'SUSPENDED':
                response = self.lbaas_provider.mgmt_client.\
                                     delete_suspended_load_balancer(loadbal.id)
        super(LbaasFuzz, self).tearDown()

    def fuzz_name(self):
        client = self.lbaas_provider.client
        load_bal = DefaultLB(client)
        load_bal.name = self.fuzz_data
        response = load_bal.create()
        self.delete_lbs.append(response.entity)
        self.assertTrue(response.ok, 'Create call to lbaas failed.\n API '
                'Response: %s' % json.loads(response.content))


class DefaultLB(object):
    def __init__(self, client):
        self._client = client
        self.name = "a-new-loadbalancer"
        self.nodes = [{"address": "10.1.1.1", "port": 80,
                       "condition": "ENABLED"}]
        self.protocol = "HTTP"
        self.virtualIps = [{"type":"PUBLIC"}]
        self.halfClosed = None
        self.accessList = [{"address": "206.160.163.21", "type": "DENY"}]
        self.algorithm = "RANDOM"
        self.connectionLogging = {"enabled": False}
        self.connectionThrottle = {"maxConnections": 100, "minConnections": 10,
                                   "maxConnectionRate": 50, "rateInterval": 60}
        self.healthMonitor = {"type": "CONNECT", "delay": 10, "timeout": 10,
                              "attemptsBeforeDeactivation": 3}
        self.metadata = [{"key":"color", "value":"red"},
                         {"key":"label", "value":"web-load-balancer"}]
        self.port = 80
        self.timeout = 100
        self.sessionPersistence = {"persistenceType": "HTTP_COOKIE"}
        self.contentCaching = None
        self.requestslib_kwargs = None

    def get_lb(self):
        return {'name': self.name, 'nodes': self.nodes,
                'protocol': self.protocol, 'virtualIps': self.virtualIps,
                'halfClosed': self.halfClosed, 'accessList': self.accessList,
                'algorithm': self.algorithm, 'connectionLogging':
                self.connectionLogging, 'connectionThrottle':
                self.connectionThrottle, 'healthMonitor': self.healthMonitor,
                'metadata': self.metadata, 'port': self.port, 'timeout':
                self.timeout, 'sessionPersistence': self.sessionPersistence,
                'contentCaching': self.contentCaching, 'requestslib_kwargs':
                self.requestslib_kwargs}

    def create(self):
        ret_val = self._client.create_load_balancer(**self.get_lb())
        return ret_val
