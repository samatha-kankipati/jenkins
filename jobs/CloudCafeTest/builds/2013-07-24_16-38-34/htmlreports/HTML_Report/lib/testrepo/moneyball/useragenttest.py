__author__ = 'ram5454'

import datetime
import json
import requests

from ccengine.clients.moneyball.moneyball_client import MoneyballAPIClient
from testrepo.common.testfixtures.fixtures import BaseTestFixture
from ccengine.providers.auth.auth_api import AuthProvider as _AuthProvider

class UserAgentTests(BaseTestFixture):

    accounts = {'test_useragent_for_given_day': 'userAgent?date=2013-01-01',
                'test_useragent_for_given_day_staging':
                'userAgent?date=2013-01-01',
                'test_useragent_for_date_range_dev':
                'userAgent?fromDate=2013-01-01&toDate=2013-01-05',
                'test_useragent_with_marker_10':
                'userAgent?fromDate=2013-01-01&toDate=2013-01-01&marker=10',
                'test_useragent_with_limit_2':
                'userAgent?fromDate=2013-01-01&toDate=2013-01-01&limit=2',
                'test_useragent_with_regex_google':
                'userAgent?date=2013-02-23&nameFilter=google',
                'test_useragent_with_regex_and_limit':
                'userAgent?date=2013-02-14&nameFilter=google&limit=4',
                'test_useragent_with_regex_limit_and_marker':
                'userAgent?date=2013-02-14&nameFilter=google&limit=4&marker=4',
                }

    @classmethod
    def setUpClass(cls):
        super(UserAgentTests, cls).setUpClass()
        # Get Global Auth Token
        auth_provider = _AuthProvider(cls.config)
        auth_data = auth_provider.authenticate()
        auth_token = auth_data.token.id
        cls.default_headers = {'X-Auth-Token': auth_token}
        # Getting the client
        cls.client1 = MoneyballAPIClient(cls.config.moneyball.base_url,
            auth_token)
        cls.client = MoneyballAPIClient(cls.config.moneyball.base_url_dev,
            auth_token)
        cls.client2 = MoneyballAPIClient(cls.config.moneyball.base_url_prod,
            auth_token)

    def callApi(self, account):
        resp = self.client.give_user_agent(account)
        json_response = json.loads(resp.content)
        return json_response

    def callApiStaging(self, account):
        resp = self.client1.give_user_agent(account)
        json_response = json.loads(resp.content)
        return json_response

    def test_useragent_for_given_day(self):
        ''' Verify that useragents are shown for a given day on dev '''
        account = UserAgentTests.accounts['test_useragent_for_given_day']
        json_response = self.callApi(account)
        #check the first and last element
        self.assertEquals(json_response['userAgents'][0]['userAgent'],
                         'Java/1.6.0_24', 'UserAgent does not match')
        self.assertEquals(json_response['userAgents'][49]['requestsCount'],
                         9804, 'requestCount does not match')

    def test_useragent_for_given_day_staging(self):
        ''' Verify that useragents are shown for a given day on staging '''
        account = UserAgentTests.accounts[
                  'test_useragent_for_given_day_staging']
        json_response = self.callApiStaging(account)
        #check the first and last element
        self.assertEquals(json_response['userAgents'][0]['userAgent'],
                         'Java/1.6.0_24', 'UserAgent does not match')
        self.assertEquals(json_response['userAgents'][49]['requestsCount'],
                         9804, 'requestCount does not match')
        self.assertEqual(json_response['userAgents'][49]['distinctIPAddrCount'],
                        4, 'distinctIPAddrCount does not match')

    def test_useragent_for_date_range_dev(self):
        ''' Verify useragents are shown for a given date range on dev '''
        account = UserAgentTests.accounts['test_useragent_for_date_range_dev']
        json_response = self.callApi(account)
        #check the first and last element
        self.assertEquals(json_response['userAgents'][0]['userAgent'],
                         'Java/1.6.0_24', 'UserAgent does not match')
        self.assertEquals(json_response['userAgents'][0]['requestsCount'],
                         35043888, 'requestCount does not match')
        self.assertEquals(json_response['userAgents'][49]['requestsCount'],
                         72272, 'requestCount does not match')

    def test_useragent_with_marker_10(self):
        ''' Verify user agents for a given date range with a marker at 10,
        meaning giving you results that are after the first ten results
        on staging.

        '''
        account = UserAgentTests.accounts['test_useragent_with_marker_10']
        json_response = self.callApiStaging(account)
        #check the first and last element
        self.assertEquals(json_response['userAgents'][0]['userAgent'],
                         'Java/1.6.0_31', 'UserAgent does not match')
        self.assertEquals(json_response['userAgents'][0]['requestsCount'],
                         445229, 'requestCount does not match')
        self.assertEquals(json_response['userAgents'][49]['requestsCount'],
                         6814, 'requestCount does not match')

    def test_useragent_with_limit_2(self):
        ''' Verify user agents for a given date range with a limit of 2,
        meaning it will give you two results for that date range

        '''
        account = UserAgentTests.accounts['test_useragent_with_limit_2']
        json_response = self.callApi(account)
        #check the first and second element
        self.assertEquals(json_response['userAgents'][0]['userAgent'],
                         'Java/1.6.0_24', 'UserAgent does not match')
        self.assertEquals(json_response['userAgents'][0]['requestsCount'],
                         6720873, 'requestCount does not match')
        self.assertEquals(json_response['userAgents'][1]['userAgent'],
                         'Java/1.6.0_18', 'UserAgent does not match')
        self.assertEquals(json_response['userAgents'][1]['requestsCount'],
                         3792288, 'requestCount does not match')

    def test_useragent_with_regex_google(self):
        ''' Verify user agents for a given date with a filter, meaning
        it will give you results that has google within the user agent
        CURRENTLY NO RESULTS
        '''
        account = UserAgentTests.accounts['test_useragent_with_regex_google']
        json_response = self.callApiStaging(account)
        #check the first and last element
        self.assertEquals(json_response['userAgents'][0]['userAgent'],
                         'Mozilla/5.0 (compatible; Googlebot/2.1;'
                         ' +http://www.google.com/bot.html)',
                         'UserAgent does not match')
        self.assertEquals(json_response['userAgents'][0]['requestsCount'],
                         9143, 'requestCount does not match')
        self.assertEquals(json_response['userAgents'][19]['requestsCount'], 1,
                         'requestCount does not match')

    def test_useragent_with_regex_and_limit(self):
        ''' Verify user agents for a given date with a filter, meaning
        it will give you results that has google within the user agent
        and limit to four results
        CURRENTLY NO RESULTS
        '''
        account = UserAgentTests.accounts[
                  'test_useragent_with_regex_and_limit']
        json_response = self.callApi(account)
        #check the first and fourth element
        self.assertEquals(json_response['userAgents'][0]['userAgent'],
                         'Mozilla/5.0 (compatible; Googlebot/2.1;'
                         ' +http://www.google.com/bot.html)')
        self.assertEquals(json_response['userAgents'][0]['requestsCount'],
                         6142, 'requestCount does not match')
        self.assertEquals(json_response['userAgents'][3]['requestsCount'],
                         1309, 'requestCount does not match')

    def test_useragent_with_regex_limit_and_marker(self):
        ''' Verify user agents for a given date with a filter, meaning
        it will give you results that has google within the user agent
        and limit to four results that are after the first four results
        CURRENTLY NO RESULTS
        '''
        account = UserAgentTests.accounts[
                  'test_useragent_with_regex_limit_and_marker']
        json_response = self.callApi(account)
        #check the first and fourth element
        self.assertEquals(json_response['userAgents'][0]['userAgent'],
                         'python-cloudfiles/1.7.11 AppEngine-Google;'
                         ' (+http://code.google.com/appengine)')
        self.assertEquals(json_response['userAgents'][0]['requestsCount'],
                         307, 'requestCount does not match')
        self.assertEquals(json_response['userAgents'][3]['requestsCount'],
                         112, 'requestCount does not match')
