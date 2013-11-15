__author__ = 'ram5454'

import datetime
import json
import requests

from ccengine.clients.moneyball.moneyball_client import MoneyballAPIClient
from testrepo.common.testfixtures.fixtures import BaseTestFixture
from ccengine.providers.auth.auth_api import AuthProvider as _AuthProvider
from footprintconfig import first_record, week_one, week_two,\
    week_fourteen, day_eightyone, us_account1, us_account2, us_account3,\
    us_auth_account, us_billing_account, us_reach_account,\
    us_next_gen_account, us_first_gen_account, us_nova_account


class Month(object):
    JAN = 0
    FEB = 1
    MAR = 2
    APR = 3
    MAY = 4
    JUN = 5
    JUL = 6
    AUG = 7
    SEP = 8
    OCT = 9
    NOV = 10
    DEC = 11

class Quarter(object):
    Q1 = 0
    Q2 = 1
    Q3 = 2
    Q4 = 3

class CustomerFootprintTests(BaseTestFixture):


    accounts = {'test_footprint_only_with_account': '761762',
                'test_footprint_only_with_account_and_period_us':
                    '405930?period=2013',
                'test_footprint_with_bad_account': '30127999999999',
                'test_footprint_year_month_01_us': '500936?period=201201',
                'test_footprint_year_month_12_us': '500936?period=201212',
                'test_footprint_year_and_month_aggregation_us':
                    '500936?period=2011&grouping=month',
                'test_footprint_year_and_month_01_us':
                    '500936?period=2011&month=01',
                'test_footprint_year_and_month_12_us':
                    '500936?period=2012&month=12',
                'test_footprint_quarterly_1_us':
                    '500936?period=2012&quarter=1',
                'test_footprint_quarterly_3_us':
                    '390715?period=2012&quarter=3',
                'test_footprint_quarterly_grouping_us':
                    '390715?period=2012&grouping=quarter',
                'test_footprint_weekly_01_us': '500936?period=2013&week=01',
                'test_footprint_weekly_53_us': '500936?period=2012&week=53',
                'test_footprint_weekly_grouping_us':
                    '500936?period=2012&grouping=week',
                'test_footprint_daily_us': '500936?period=20130105',
                'test_footprint_daily_grouping':
                    '500936?period=2011&grouping=day',
                'test_footprint_with_bad_datetime': '301279?date=201208011',
                'test_auth_log_account': '322641?period=20120301',
                'test_billing_data_account': '322767?period=201304',
                'test_reach_log_account': '348554?period=20130502',
                'test_cloud_usage_account_ng': '425623?period=20130512',
                'test_cloud_nova_account_fg': '493791?period=20130511',
                'test_cloud_nova_account_fg_2': '515092?period=20130511',
                }

    @classmethod
    def setUpClass(cls):
        super(CustomerFootprintTests, cls).setUpClass()
        # Get Global Auth Token
        auth_provider = _AuthProvider(cls.config)
        auth_data = auth_provider.authenticate()
        auth_token = auth_data.token.id
        cls.default_headers = {'X-Auth-Token': auth_token}
        # Getting the client
        cls.client = MoneyballAPIClient(cls.config.moneyball.base_url_dev,
                                        auth_token)
        cls.client2 = MoneyballAPIClient(cls.config.moneyball.base_url_prod,
                                         auth_token)

    def test_footprint_only_with_account(self):
        ''' Verify Customer footprint API with only an US Account
        ID, does not work

        '''
        account = CustomerFootprintTests.accounts[
                  'test_footprint_only_with_account']
        resp = self.client.give_customer_footprint(account)
        split_response_string = resp.content.split(':"')[1]
        split_response_string = split_response_string.split('",')[0]
        self.assertEqual(split_response_string, "Invalid request"
                           " parameter \'period\',"
                           " expecting date: YYYY, YYYYMM or"
                           " YYYYMMDD.", 'error message does not match')

    def test_footprint_only_with_account_and_period_us(self):
        '''Verify this account since its having an issue'''
        account = CustomerFootprintTests.accounts[
                  'test_footprint_only_with_account_and_period_us']
        resp = self.client.give_customer_footprint(account)
        json_response = json.loads(resp.content)
        self.assertEqual(json_response['records'][first_record]['ddi'],
                        us_account1, 'account ids do not match')
        self.assertEqual(json_response['records'][first_record]
                        ['authRequests'], 1861, 'auth count does not match')
        self.assertEqual(json_response['records'][first_record]
                        ['cpcAuthRequests'], 33,
                        'classic auth requests do not match')
        self.assertEqual(json_response['records'][first_record]['memMBVolFG'],
                        23552,
                        'memory volatility for first gen does not match')

    def test_footprint_with_bad_account(self):
        '''Verify the error message when an incorrect Account ID is passed'''
        bad_account = CustomerFootprintTests.accounts[
                      'test_footprint_with_bad_account']
        resp = self.client.give_customer_footprint(bad_account)
        split_response_string = resp.content.split(':"')[1]
        split_response_string = split_response_string.split('",')[0]
        self.assertEqual(split_response_string, "Invalid request"
                           " parameter \'period\',"
                           " expecting date: YYYY, YYYYMM or"
                           " YYYYMMDD.", 'error message does not match')

    def test_footprint_year_month_01_us(self):
        ''' Verify Customer footprint API for an US Account with
        date-time of Year and month

        '''
        account_date = CustomerFootprintTests.accounts[
                       'test_footprint_year_month_01_us']
        resp = self.client.give_customer_footprint(account_date)
        json_response = json.loads(resp.content)
        self.assertEqual(json_response['records'][first_record]['ddi'],
                        us_account2, 'account ids do not match')
        self.assertEqual(json_response['records'][first_record]
                        ['authRequests'], 5604, 'auth requests do not match')
        self.assertEqual(json_response['records'][first_record]
                        ['cpcAuthRequests'], 2,
                        'cpc auth requests do not match')
        self.assertEqual(json_response['records'][first_record]
                        ['monthlyTotal'], 34470.22,
                        'monthly total does not match')

    def test_footprint_year_month_12_us(self):
        ''' Verify Customer footprint API for an US Account with
        date-time of Year and month

        '''
        account_date = CustomerFootprintTests.accounts[
                       'test_footprint_year_month_12_us']
        resp = self.client.give_customer_footprint(account_date)
        json_response = json.loads(resp.content)
        self.assertEqual(json_response['records'][first_record]['ddi'],
                        us_account2, 'account ids do not match')
        self.assertEqual(json_response['records'][first_record]
                        ['authRequests'], 38495, 'auth requests do not match')
        self.assertEqual(json_response['records'][first_record]
                        ['cpcAuthRequests'], 82,
                        'cpc auth requests do not match')
        self.assertEqual(json_response['records'][first_record]
                        ['monthlyTotal'], 92080.53,
                        'monthly total does not match')

    def test_footprint_year_and_month_aggregation_us(self):
        ''' Verify Customer footprint API for an US Account with
        date-time of Year and month aggregation

        '''
        account_date = CustomerFootprintTests.accounts[
                       'test_footprint_year_and_month_aggregation_us']
        resp = self.client.give_customer_footprint(account_date)
        json_response = json.loads(resp.content)
        self.assertEqual(json_response['records'][Month.JAN]['ddi'],
                        us_account2, 'account ids do not match')
        self.assertEqual(json_response['records'][Month.JAN]['authRequests'],
                        0, 'auth requests do not match')
        self.assertEqual(json_response['records'][Month.JAN]
                        ['cpcAuthRequests'], 0,
                        'cpc auth requests do not match')
        self.assertEqual(json_response['records'][Month.JAN]['monthlyTotal'],
                         25523.04, 'monthly total bill does not match')
        self.assertEqual(json_response['records'][Month.FEB]['monthlyTotal'],
                         40428.71, 'monthly total bill does not match')
        self.assertEqual(json_response['records'][Month.DEC]['monthlyTotal'],
                        31404.28, 'monthly total bill does not match')

    def test_footprint_year_and_month_01_us(self):
        ''' Verify Customer footprint API for an US Account with
        date-time of Year and month

        '''
        account_date = CustomerFootprintTests.accounts[
                       'test_footprint_year_and_month_01_us']
        resp = self.client.give_customer_footprint(account_date)
        json_response = json.loads(resp.content)
        self.assertEqual(json_response['records'][first_record]['ddi'],
                        us_account2, 'account ids do not match')
        self.assertEqual(json_response['records'][first_record]
                        ['authRequests'], 0, 'auth requests do not match')
        self.assertEqual(json_response['records'][first_record]
                        ['cpcAuthRequests'], 0,
                        'cpc auth requests do not match')
        self.assertEqual(json_response['records'][first_record]
                        ['monthlyTotal'], 0.0, 'monthly total does not match')

    def test_footprint_year_and_month_12_us(self):
        ''' Verify Customer footprint API for an US Account with
        date-time of Year and month

        '''
        account_date = CustomerFootprintTests.accounts[
                       'test_footprint_year_and_month_12_us']
        resp = self.client.give_customer_footprint(account_date)
        json_response = json.loads(resp.content)
        self.assertEqual(json_response['records'][first_record]['ddi'],
                        us_account2, 'account ids do not match')
        self.assertEqual(json_response['records'][first_record]
                        ['authRequests'], 127417,
                        'auth requests do not match')
        self.assertEqual(json_response['records'][first_record]
                        ['cpcAuthRequests'], 380,
                        'cpc auth requests do not match')
        self.assertEqual(json_response['records'][first_record]
                        ['monthlyTotal'], 0.0,
                        'monthly total does not match')

    def test_footprint_quarterly_1_us(self):
        ''' Verify Customer footprint API for an US Account with
        date-time of Quarterly

        '''
        account_date = CustomerFootprintTests.accounts[
                       'test_footprint_quarterly_1_us']
        resp = self.client.give_customer_footprint(account_date)
        json_response = json.loads(resp.content)
        self.assertEqual(json_response['records'][first_record]['ddi'],
                        us_account2, 'account ids do not match')
        self.assertEqual(json_response['records'][first_record]
                        ['authRequests'], 36802, 'auth requests do not match')
        self.assertEqual(json_response['records'][first_record]
                        ['cpcAuthRequests'], 108,
                        'cpc auth requests do not match')
        self.assertEqual(json_response['records'][first_record]
                        ['reachAuthRequests'], 29,
                        'reach auth requests do not match')

    def test_footprint_quarterly_3_us(self):
        ''' Verify Customer footprint API for an US Account with
        date-time of Quarterly BUGGGGG in 4th quarter

        '''
        account_date = CustomerFootprintTests.accounts[
                       'test_footprint_quarterly_3_us']
        resp = self.client.give_customer_footprint(account_date)
        json_response = json.loads(resp.content)
        self.assertEqual(json_response['records'][first_record]['ddi'],
                        us_account3, 'account ids do not match')
        self.assertEqual(json_response['records'][first_record]
                        ['authRequests'], 90841, 'auth requests do not match')
        self.assertEqual(json_response['records'][first_record]
                        ['cpcAuthRequests'], 83,
                        'cpc auth requests do not match')
        self.assertEqual(json_response['records'][first_record]
                        ['reachAuthRequests'] ,11982,
                        'reach auth requests do not match')

    def test_footprint_quarterly_grouping_us(self):
        ''' Verify Customer footprint API for an US Account with
        date-time of Quarterly BUGGGGG in 4th quarter here as well

        '''
        account_date = CustomerFootprintTests.accounts[
                       'test_footprint_quarterly_grouping_us']
        resp = self.client.give_customer_footprint(account_date)
        json_response = json.loads(resp.content)
        self.assertEqual(json_response['records'][Quarter.Q1]['ddi'],
                        us_account3, 'account ids do not match')
        self.assertEqual(json_response['records'][Quarter.Q1]['authRequests'],
                        21833, 'auth requests do not match')
        self.assertEqual(json_response['records'][Quarter.Q1]
                        ['cpcAuthRequests'], 124,
                        'cpc auth requests do not match')
        self.assertEqual(json_response['records'][Quarter.Q1]
                        ['reachAuthRequests'], 0,
                        'reach auth requests do not match')
        self.assertEqual(json_response['records'][Quarter.Q2]
                        ['authRequests'], 49912, 'auth requests do not match')
        self.assertEqual(json_response['records'][Quarter.Q2]
                        ['reachAuthRequests'], 6044,
                        'reach auth requests do not match')
        self.assertEqual(json_response['records'][Quarter.Q2]
                        ['reachAuthRequests'], 11982,
                        'reach auth requests do not match')


    def test_footprint_weekly_01_us(self):
        ''' Verify Customer footprint API for an US Account
        with date-time of weekly01

        '''
        account_date = CustomerFootprintTests.accounts[
                       'test_footprint_weekly_01_us']
        resp = self.client.give_customer_footprint(account_date)
        json_response = json.loads(resp.content)
        self.assertEqual(json_response['records'][first_record]['ddi'],
                        us_account2, 'account ids do not match')
        self.assertEqual(json_response['records'][first_record]
                        ['authRequests'], 8485, 'auth requests do not match')
        self.assertEqual(json_response['records'][first_record]
                        ['cpcAuthRequests'], 30,
                        'cpc auth requests do not match')
        self.assertEqual(json_response['records'][first_record]
                        ['reachAuthRequests'], 36,
                        'reach auth requests do not match')

    def test_footprint_weekly_53_us(self):
        ''' Verify Customer footprint API for an US Account
        with date-time of weekly53

        '''
        account_date = CustomerFootprintTests.accounts[
                       'test_footprint_weekly_53_us']
        resp = self.client.give_customer_footprint(account_date)
        json_response = json.loads(resp.content)
        self.assertEqual(json_response['records'][first_record]['ddi'],
                        us_account2, 'account ids do not match')
        self.assertEqual(json_response['records'][first_record]
                        ['authRequests'], 2310,
                        'auth requests do not match')
        self.assertEqual(json_response['records'][first_record]
                        ['cpcAuthRequests'], 0,
                        'cpc auth requests do not match')
        self.assertEqual(json_response['records'][first_record]
                        ['reachAuthRequests'], 0,
                        'reach auth requests do not match')

    def test_footprint_weekly_grouping_us(self):
        ''' Verify Customer footprint API for an US Account
        with date-time of weekly with grouping

        '''
        account_date = CustomerFootprintTests.accounts[
                       'test_footprint_weekly_grouping_us']
        resp = self.client.give_customer_footprint(account_date)
        json_response = json.loads(resp.content)
        self.assertEqual(json_response['records'][week_one]['ddi'],
                        us_account2, 'account ids do not match')
        self.assertEqual(json_response['records'][week_two]['authRequests'],
                        30, 'auth requests do not match')
        self.assertEqual(json_response['records'][week_one]
                        ['cpcAuthRequests'], 0,
                        'cpc auth requests do not match')
        self.assertEqual(json_response['records'][week_one]
                        ['reachAuthRequests'], 0,
                        'reach auth requests do not match')
        self.assertEqual(json_response['records'][week_fourteen]
                        ['authRequests'], 168,
                        'auth requests do not match')
        self.assertEqual(json_response['records'][week_fourteen]
                        ['cpcAuthRequests'], 8,
                        'cpc auth requests do not match')
        self.assertEqual(json_response['records'][week_fourteen]
                        ['reachAuthRequests'], 0,
                        'reach auth requests do not match')
        totalNumberWeeks = len(json_response['records']) - 1
        self.assertEqual(json_response['records'][totalNumberWeeks]
                        ['authRequests'], 57, 'auth requests do not match')
        self.assertEqual(json_response['records'][totalNumberWeeks]
                        ['cpcAuthRequests'], 0,
                        'cpc auth requests do not match')
        self.assertEqual(json_response['records'][totalNumberWeeks]
                        ['reachAuthRequests'], 0,
                        'reach auth requests do not match')


    def test_footprint_daily_us(self):
        ''' Verify Customer footprint API for an US Account
        with date-time of daily BUGGG memMBNetDeltaFG is incorrect in dev

        '''
        account_date = CustomerFootprintTests.accounts[
                       'test_footprint_daily_us']
        resp = self.client2.give_customer_footprint(account_date)
        json_response = json.loads(resp.content)
        self.assertEqual(json_response['records'][first_record]['ddi'],
                        us_account2, 'account ids do not match')
        self.assertEqual(json_response['records'][first_record]
                        ['authRequests'], 1158, 'auth requests do not match')
        self.assertEqual(json_response['records'][first_record]
                        ['cpcAuthRequests'], 0,
                        'cpc auth requests do not match')
        self.assertEqual(json_response['records'][first_record]
                        ['reachAuthRequests'], 0,
                        'reach auth requests do not match')
        self.assertEqual(json_response['records'][first_record]
                        ['memMBNetDeltaFG'], 8192.0,
                        'net change in memory for first gen does not match')


    def test_footprint_daily_grouping(self):
        ''' Verify Customer footprint API for an US account
        with date-time and grouping option

        '''
        account_date = CustomerFootprintTests.accounts[
                       'test_footprint_daily_grouping']
        resp = self.client.give_customer_footprint(account_date)
        json_response = json.loads(resp.content)
        total_days = len(json_response['records']) -1
        print total_days
        self.assertEqual(json_response['records'][first_record]['ddi'],
                        us_account2, 'account ids do not match')
        self.assertEqual(json_response['records'][first_record]
                        ['authRequests'], 0, 'auth requests do not match')
        self.assertEqual(json_response['records'][first_record]
                        ['cpcAuthRequests'], 0,
                        'cpc auth requests do not match')
        self.assertEqual(json_response['records'][first_record]
                        ['reachAuthRequests'], 0,
                        'reach auth requests do not match')
        self.assertEqual(json_response['records'][first_record]['nvmVolFG'],
                        2.0,
                        'net change in memory for first gen does not match')
        self.assertEqual(json_response['records'][day_eightyone]['ddi'],
                        us_account2, 'account ids do not match')
        self.assertEqual(json_response['records'][day_eightyone]
                        ['authRequests'], 0, 'auth requests do not match')
        self.assertEqual(json_response['records'][day_eightyone]
                        ['cpcAuthRequests'], 0,
                        'cpc auth requests do not match')
        self.assertEqual(json_response['records'][day_eightyone]
                        ['reachAuthRequests'], 0,
                        'reach auth requests do not match')
        self.assertEqual(json_response['records'][day_eightyone]['nvmVolFG'],
                        5.0,
                        'net change in memory for first gen does not match')

    def test_footprint_with_bad_datetime(self):
        ''' Verify the message when an Account with an invalid
        date-time format is passed

        '''
        bad_date = CustomerFootprintTests.accounts[
                   'test_footprint_with_bad_datetime']
        resp = self.client.give_customer_footprint(bad_date)
        split_response_string = resp.content.split(':"')[1]
        split_response_string = split_response_string.split('",')[0]
        self.assertEqual(split_response_string, "Invalid request "
                        "parameter \'period\',"
                        " expecting date: YYYY, YYYYMM or"
                        " YYYYMMDD.", 'error message does not match')

    def test_latency_average_ten_accounts(self): pass


    def test_auth_log_account(self):
        ''' Verify Auth log data through an account that has recent
        auth information

        '''
        auth_account = CustomerFootprintTests.accounts[
                       'test_auth_log_account']
        resp = self.client.give_customer_footprint(auth_account)
        json_response = json.loads(resp.content)
        self.assertEqual(json_response['records'][first_record]['ddi'],
                        us_auth_account, 'account ids do not match')
        self.assertEqual(json_response['records'][first_record]
                        ['authRequests'], 6,
                        'account auth requests do not match')
        self.assertEqual(json_response['records'][first_record]
                        ['cpcAuthRequests'], 0,
                        'account cpu auth requests do not match')
        self.assertEqual(json_response['records'][first_record]
                        ['failedAuthRequests'] ,0,
                        'account auth requests do not match')
        self.assertEqual(json_response['records'][first_record]
                        ['failedCpcAuthRequests'] ,0,
                        'account cpu auth requests do not match')
        self.assertEqual(json_response['records'][first_record]
                        ['failedAuthRatio'], 0,
                        'account cpu auth requests do not match')

    def test_billing_data_account(self):
        ''' Verify Billing data through an account that has recent
        billing information

        '''
        auth_account = CustomerFootprintTests.accounts[
                       'test_billing_data_account']
        resp = self.client2.give_customer_footprint(auth_account)
        json_response = json.loads(resp.content)
        self.assertEqual(json_response['records'][first_record]['ddi'],
                        us_billing_account, 'account ids do not match')
        self.assertEqual(json_response['records'][first_record]
                        ['spendCloudFiles'], 0.35,
                        'account spend cloud files does not match')
        self.assertEqual(json_response['records'][first_record]
                        ['spendTotal'], 1348.63,
                        'account total spend does not match')

    def test_reach_log_account(self):
        ''' Verify Reach log data through an account that has recent
        reach information

        '''
        auth_account = CustomerFootprintTests.accounts[
                       'test_reach_log_account']
        resp = self.client2.give_customer_footprint(auth_account)
        json_response = json.loads(resp.content)
        self.assertEqual(json_response['records'][first_record]['ddi'],
                        us_reach_account, 'account ids do not match')
        self.assertEqual(json_response['records'][first_record]
                        ['reachAuthRequests'], 41,
                        'account reach requests does not match')

    def test_cloud_usage_account_ng(self):
        ''' Verify Cloud usage data through an account that has recent
        cloud usage information

        '''
        auth_account = CustomerFootprintTests.accounts[
                       'test_cloud_usage_account_ng']
        resp = self.client2.give_customer_footprint(auth_account)
        json_response = json.loads(resp.content)
        self.assertEqual(json_response['records'][first_record]['ddi'],
                        us_next_gen_account,
                        'account ids do not match')
        self.assertEqual(json_response['records'][first_record]
                        ['memMBNetDeltaNG'], 4096.0,
                        'account change in memory usage does not match')

    def test_cloud_nova_account_fg(self):
        ''' Verify Cloud Nova events through an account that has recent
        cloud nova information

        '''
        auth_account = CustomerFootprintTests.accounts[
                       'test_cloud_nova_account_fg']
        resp = self.client2.give_customer_footprint(auth_account)
        json_response = json.loads(resp.content)
        self.assertEqual(json_response['records'][first_record]['ddi'],
                        us_first_gen_account, 'account ids do not match')
        self.assertEqual(json_response['records'][first_record]
                        ['memMBNetDeltaFG'] , -2048.0,
                        'account change in memory usage does not match')

    def test_cloud_nova_account_fg_2(self):
        ''' Verify Cloud Nova events through an account that has recent
        cloud nova information

        '''
        auth_account = CustomerFootprintTests.accounts[
                       'test_cloud_nova_account_fg_2']
        resp = self.client2.give_customer_footprint(auth_account)
        json_response = json.loads(resp.content)
        self.assertEqual(json_response['records'][first_record]['ddi'],
                        us_nova_account, 'account ids do not match')
        self.assertEqual(json_response['records'][first_record]
                        ['memMBNetDeltaFG'] , 2048.0,
                        'account change in memory usage do not match')




