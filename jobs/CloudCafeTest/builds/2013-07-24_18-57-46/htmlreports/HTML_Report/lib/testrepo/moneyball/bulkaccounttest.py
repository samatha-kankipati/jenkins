__author__ = 'ram5454'

from ccengine.clients.moneyball.moneyball_client import MoneyballAPIClient
from testrepo.common.testfixtures.fixtures import BaseTestFixture
from ccengine.domain.moneyball.response import  UsDefectionResponse
from ccengine.providers.auth.auth_api import AuthProvider as _AuthProvider
import json


class BulkAccountTest(BaseTestFixture):


    @classmethod
    def setUpClass(cls):
        super(BulkAccountTest, cls).setUpClass()
        # Get Global Auth Token
        auth_provider = _AuthProvider(cls.config)
        auth_data = auth_provider.authenticate()
        auth_token = auth_data.token.id
        cls.default_headers = {'X-Auth-Token': auth_token}
        # Geeting the client
        cls.client = MoneyballAPIClient(cls.config.moneyball.base_url,
                                        auth_token)

    # Testing DI for all US and UK accounts
    def test_defection_index_US_bulk(self):
        accounts = ['332860','356693','407349','444816','500947','346654',
                    '790531','502790', '744182', '448588']
        for line in accounts:
            try:
                resp = self.client.give_defection_index(line)
                usdefection = UsDefectionResponse._json_to_obj(resp.content)

                self.assertEqual(usdefection.accountId, int(line),
                                'Id is not equal the Id on input file')
                self.assertIsNotNone(usdefection.defectionIndex,
                                     'defection index is null')
                print ' '.join([line, str(usdefection.defectionIndex)])
                print ''
            except:
                print ' '.join([line, 'failed account'])
