__author__ = 'ram5454'

import time
from ccengine.clients.moneyball.moneyball_client import MoneyballAPIClient
from testrepo.common.testfixtures.fixtures import BaseTestFixture
from ccengine.domain.moneyball.response import  UsDefectionResponse
from ccengine.providers.auth.auth_api import AuthProvider as _AuthProvider



class LatencyTest(BaseTestFixture):

    @classmethod
    def setUpClass(cls):
        super(LatencyTest, cls).setUpClass()
        # Get Global Auth Token
        auth_provider = _AuthProvider(cls.config)
        auth_data = auth_provider.authenticate()
        auth_token = auth_data.token.id
        cls.default_headers = {'X-Auth-Token': auth_token}
        # Getting the client
        cls.client = MoneyballAPIClient(cls.config.moneyball.base_url,
                                        auth_token)

    # Testing DI for all US and UK accounts
    def test_latency_for_defection_index_US_accounts(self):
        accounts = ['332860','356693','407349','444816','500947','346654',
                    '790531','502790', '744182', '448588']
        latency = []
        for i in accounts:
            start_time = time.time()
            resp = self.client.give_defection_index(i)
            elapsed_time = time.time() - start_time
            usdefection = UsDefectionResponse._json_to_obj(resp.content)
            self.assertEqual(str(usdefection.accountId), i, 'Id is not equal')
            print elapsed_time, '\n'
            latency.append(elapsed_time)
        print 'length of latency ' + str(len(latency))
        print 'sum of latencies ' + (str(sum(latency))) , '\n'
        print 'average ' + (str(sum(latency)/10)) , '\n'
        self.assertGreater(4, sum(latency)/10, 'Latency is unacceptable')

    def test_latency_for_defection_index_US_single_account(self):
        latency = []
        for i in range(10):
            start_time = time.time()
            resp = self.client.give_defection_index('706760')
            elapsed_time = time.time() - start_time
            usdefection = UsDefectionResponse._json_to_obj(resp.content)
            self.assertEqual(usdefection.accountId, 706760, 'Id is not equal')
            print elapsed_time, '\n'
            latency.append(elapsed_time)
        print 'sum of latencies ' + (str(sum(latency))) , '\n'
        print 'average ' + (str(sum(latency)/10)) , '\n'
        self.assertGreater(1, sum(latency)/10, 'Latency is unacceptable')


