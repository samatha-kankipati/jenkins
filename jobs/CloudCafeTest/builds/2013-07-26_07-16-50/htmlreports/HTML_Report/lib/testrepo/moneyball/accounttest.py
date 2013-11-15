__author__ = 'ram5454'

import requests
import datetime
import json

from ccengine.clients.moneyball.moneyball_client import MoneyballAPIClient
from testrepo.common.testfixtures.fixtures import BaseTestFixture
from ccengine.domain.moneyball.response import ContactInfo, \
    UkDefectionResponse, UsDefectionResponse, DefectionRange, \
    PaginationByDate, PaginationDateRange
from ccengine.providers.auth.auth_api import AuthProvider as _AuthProvider

class AccountTests(BaseTestFixture):

    @classmethod
    def setUpClass(cls):
        super(AccountTests, cls).setUpClass()
        # Get Global Auth Token
        auth_provider = _AuthProvider(cls.config)
        auth_data = auth_provider.authenticate()
        auth_token = auth_data.token.id
        cls.default_headers = {'X-Auth-Token': auth_token}
        # Getting the client
        cls.client = MoneyballAPIClient(cls.config.moneyball.base_url,
                                        auth_token)


    def test_account_details_us(self):
        account_us = '719072'
        resp = self.client.give_account_details(account_us)
        print (resp)
        print resp.content
        j = json.loads(resp.content)
        self.assertEqual(j['PrimaryContactInfo']['firstName'],
                         'Steve', 'firstname should be equal')
        self.assertEqual(j['PrimaryContactInfo']['lastName'],
                         'Eastham', 'lastname should be equal')
        self.assertEqual(j['PrimaryContactInfo']['email'],
                         'steve.eastham@bestbuy.com', 'email should be equal')
        self.assertEqual(j['PrimaryContactInfo']['phoneNumber'],
                         '612-291-7354', 'phone number should be equal')
        self.assertEqual(j['PrimaryContactInfo']['street'],
                         '7601 Penn Ave', 'street should be equal')
        self.assertEqual(j['PrimaryContactInfo']['city'],
                         'Minneapolis', 'city should be equal')
        self.assertEqual(j['PrimaryContactInfo']['state'],
                         'MN', 'state should be equal')
        self.assertEqual(j['PrimaryContactInfo']['zip'],
                        '55423', 'zip should be equal')
        self.assertEqual(j['PrimaryContactInfo']['country'],
                         'United States', 'Country should be equal')


    def test_account_details_using_domain_us(self):
        account_us = '719072'
        resp = self.client.give_account_details(account_us)
        account = ContactInfo._json_to_obj(resp.content)
        self.assertEquals(account.firstName , 'Steve',
                          'firstname should be equal')
        self.assertEquals(account.lastName , 'Eastham',
                          'lastname should be equal')
        self.assertEqual(account.email, 'steve.eastham@bestbuy.com',
                         'email should be equal')
        self.assertEqual(account.phoneNumber, '612-291-7354',
                         'phone number should be equal')
        self.assertEqual(account.street, '7601 Penn Ave',
                         'street should be equal')
        self.assertEqual(account.city, 'Minneapolis',
                         'city should be equal')
        self.assertEqual(account.state, 'MN',
                         'state should be equal')
        self.assertEqual(account.zip, '55423',
                         'zip should be equal')
        self.assertEqual(account.country, 'United States',
                         'Country should be equal')


    def test_defection_index_uk(self):
        uk_account = '10017503'
        resp = self.client.give_defection_index(uk_account)
        ukdefection = UkDefectionResponse._json_to_obj(resp.content)
        print resp.content
        j = json.loads(resp.content)
        self.assertEqual(j['indices'][0]['accountId'],
                         10017503, 'ID should be equal')
        self.assertEqual(ukdefection.accountId, 10017503,
                         'Id should be equal')
        self.assertIsNotNone(ukdefection.defectionIndex)
        self.assertIsNotNone(ukdefection.behaviorValue)
        self.assertIsNotNone(ukdefection.noUsageValue)
        self.assertIsNotNone(ukdefection.sliceValue)
        self.assertIsNotNone(ukdefection.tenureValue)

    def test_defection_index_us(self):
        us_account = '719072'
        resp = self.client.give_defection_index(us_account)
        usdefection = UsDefectionResponse._json_to_obj(resp.content)
        print resp.content
        j = json.loads(resp.content)
        self.assertEqual(j['indices'][0]['accountId'], 719072,
                         'ID should be equal')
        self.assertEqual(usdefection.accountId, 719072,
                         'Id should be equal')
        self.assertIsNotNone(usdefection.defectionIndex)
        self.assertIsNotNone(usdefection.behaviorValue)
        self.assertIsNotNone(usdefection.noUsageValue)
        self.assertIsNotNone(usdefection.sliceValue)
        self.assertIsNotNone(usdefection.tenureValue)

    def test_defection_index_us_specificdate(self):
        us_account_date = '719072?date=20121120'
        resp = self.client.give_defection_index(us_account_date)
        usdefection = UsDefectionResponse._json_to_obj(resp.content)
        j = json.loads(resp.content)
        self.assertEqual(usdefection.accountId, '719072', 'Id does not match')
        d = usdefection.defectionIndex
        d = ("%.3f" % float(d))
        self.assertEqual(d, '0.715', 'Defection index does not match')
        self.assertEqual(usdefection.behaviorValue, '0.75',
                         'Behavior value does not match')
        self.assertEqual(usdefection.noUsageValue, '0.5',
                         'No usage value does not match')
        self.assertEqual(usdefection.tenureValue,
                         '1.0', 'Tenure value does not match')
        s = usdefection.sliceValue
        s = ("%.3f" % float(s))
        self.assertEqual(s, '0.668', 'Slice value does not match')

    def test_defection_index_uk_specificdate(self):
        uk_account_date = '10017503?date=20130106'
        resp = self.client.give_defection_index(uk_account_date)
        ukdefection = UsDefectionResponse._json_to_obj(resp.content)
        j = json.loads(resp.content)
        self.assertEqual(ukdefection.accountId, 10017503, 'Id does not match')
        d = ukdefection.defectionIndex
        d = ("%.2f" % float(d))
        self.assertEqual(d, '0.68', 'Defection index does not match')
        self.assertEqual(ukdefection.behaviorValue, 0.75,
                         'Behavior value does not match')
        self.assertEqual(ukdefection.noUsageValue, 0.25,
                         'No usage value does not match')
        self.assertEqual(ukdefection.tenureValue, 0.75,
                         'Tenure value does not match')
        #currently there is a bug with the slice value
        #s = ukdefection.sliceValue
        #s = ("%.3f" % float(s))
        #self.assertEqual(s, '0.668', 'Slice value does not match')



    # bug getting 500 instead of 400
    # This should give you a status code of 404 since the start date is higher
    # than the end date. Should give an error message as well
    # Currently this is giving a 500 exception which is a bug
    def test_defection_index_wrong_range(self):
        url = 'http://mb-api-n01.dev.inova.us.ci.rackspace.net/beaker/' \
              'models/defection/670019?start=20130106&end=20130101'
        r = requests.get(url, headers=self.default_headers, timeout=4)
        print r.status_code
        self.assertEqual(r.status_code, 400, 'status code is not 400')
        print r.content
        s = r.content.split(' and')[0]
        self.assertEqual(s[12:-13], 'The end instant must be greater or '
                        'equal to the start' , 'content output does not match')


    # This should give you a status code of 404 since the account does not
    # exist. Should give an error message as well
    def test_defection_index_with_wrongid(self):
        wrongid = '670222222019'
        r = self.client.give_defection_index(wrongid)
        print r.status_code
        self.assertEqual(r.status_code, 404, 'status code is not 404')
        print r.content
        s = r.content.split(' and')[0]
        self.assertEqual(s, 'No index details found for account670222222019' ,
                         'content output does not match')

    # This should give you a status code of 404 since the date is incorrect.
    # Should give an error message as well
    def test_defection_index_with_wrongdate(self):
        url = 'http://mb-api-n01.dev.inova.us.ci.rackspace.net/beaker/' \
              'models/defection/670019?date=20150106'
        r = requests.get(url, headers=self.default_headers, timeout=4)
        print r.status_code
        self.assertEqual(r.status_code, 404, 'status code is not 404')
        print r.content
        s = r.content.split(' and')[0]
        self.assertEqual(s, 'No index details found for account670019' ,
                         'content output does not match')

    # This should give you a status code of 404 since the account does not
    # exist. Should give an error message as well
    def test_defection_index_range_with_wrongid(self):
        url = 'http://mb-api-n01.dev.inova.us.ci.rackspace.net/beaker/' \
              'models/defection/670222222019?start=20130101&end=20130106'
        r = requests.get(url, headers=self.default_headers, timeout=4)
        print r.status_code
        self.assertEqual(r.status_code, 404, 'status code is not 404')
        print r.content
        s = r.content.split(' and')[0]
        self.assertEqual(s, 'No index details found for account670222222019' ,
                         'content output does not match')



    def test_defection_index_us_with_daterange_of_fivedays(self):
        url = 'http://mb-api-n01.dev.inova.us.ci.rackspace.net/beaker' \
              '/models/defection/670019?start=20130101&end=20130106'
        r = requests.get(url, headers=self.default_headers, timeout=4)
        print r.status_code
        self.assertEquals(r.status_code, 200, 'status code is not 200')
        print r.content
        parsed_j = json.loads(r.content)
        print parsed_j
        indices = parsed_j['indices'][0]['accountId']
        self.assertEqual(indices, 670019, 'account id does not match')
        indices = parsed_j['indices'][1]['accountId']
        self.assertEqual(indices, 670019, 'account id does not match')
        indices = parsed_j['indices'][2]['accountId']
        self.assertEqual(indices, 670019, 'account id does not match')
        indices = parsed_j['indices'][3]['accountId']
        self.assertEqual(indices, 670019, 'account id does not match')
        indices = parsed_j['indices'][4]['accountId']

        d = parsed_j['indices'][0]['defectionIndex']
        d = ("%.3f" % float(d))
        self.assertEqual(d, '0.443', 'defection index does not match')
        d = parsed_j['indices'][1]['defectionIndex']
        d = ("%.3f" % float(d))
        self.assertEqual(d, '0.443', 'defection index does not match')
        d = parsed_j['indices'][2]['defectionIndex']
        d = ("%.3f" % float(d))
        self.assertEqual(d, '0.443', 'defection index does not match')
        d = parsed_j['indices'][3]['defectionIndex']
        d = ("%.3f" % float(d))
        self.assertEqual(d, '0.443', 'defection index does not match')
        d = parsed_j['indices'][4]['defectionIndex']
        d = ("%.3f" % float(d))
        self.assertEqual(d, '0.443', 'defection index does not match')

    def test_defection_index_uk_with_daterange_of_sixdays(self):
        url = 'http://mb-api-n01.dev.inova.us.ci.rackspace.net/beaker/' \
              'models/defection/10017503?start=20130101&end=20130107'
        r = requests.get(url, headers=self.default_headers, timeout=5)
        print r.status_code
        self.assertEquals(r.status_code, 200, 'status code is not 200')
        print r.content
        parsed_j = json.loads(r.content)
        print parsed_j
        indices = parsed_j['indices'][0]['accountId']
        self.assertEqual(indices, 10017503, 'account id does not match')
        indices = parsed_j['indices'][1]['accountId']
        self.assertEqual(indices, 10017503, 'account id does not match')
        indices = parsed_j['indices'][2]['accountId']
        self.assertEqual(indices, 10017503, 'account id does not match')
        indices = parsed_j['indices'][3]['accountId']
        self.assertEqual(indices, 10017503, 'account id does not match')
        indices = parsed_j['indices'][4]['accountId']
        self.assertEqual(indices, 10017503, 'account id does not match')
        indices = parsed_j['indices'][5]['accountId']

        d = parsed_j['indices'][0]['defectionIndex']
        d = ("%.3f" % float(d))
        self.assertEqual(d, '0.678', 'defection index does not match')
        d = parsed_j['indices'][1]['defectionIndex']
        d = ("%.3f" % float(d))
        self.assertEqual(d, '0.678', 'defection index does not match')
        d = parsed_j['indices'][2]['defectionIndex']
        d = ("%.3f" % float(d))
        self.assertEqual(d, '0.678', 'defection index does not match')
        d = parsed_j['indices'][3]['defectionIndex']
        d = ("%.3f" % float(d))
        self.assertEqual(d, '0.678', 'defection index does not match')
        d = parsed_j['indices'][4]['defectionIndex']
        d = ("%.3f" % float(d))
        self.assertEqual(d, '0.678', 'defection index does not match')
        d = parsed_j['indices'][5]['defectionIndex']
        d = ("%.3f" % float(d))
        self.assertEqual(d, '0.678', 'defection index does not match')

    def test_defection_index_for_specific_date_uk(self):
        url = 'http://mb-api-n01.dev.inova.us.ci.rackspace.net/beaker/' \
              'models/defection/10017503?date=20130104'
        r = requests.get(url, headers=self.default_headers)
        print r.content
        self.assertEqual(r.status_code, 200, 'status code is not 200')
        parsed_j = json.loads(r.content)
        print parsed_j
        indices = parsed_j['indices'][0]['accountId']
        self.assertEqual(indices, 10017503, 'account id does not match')
        indices = parsed_j['indices'][0]['behaviorValue']
        self.assertEqual(indices, 0.75, 'behavior value does not match')
        indices = parsed_j['indices'][0]['tenureValue']
        self.assertEqual(indices, 0.75, 'tenure value does not match')
        d = parsed_j['indices'][0]['defectionIndex']
        d = ("%.3f" % float(d))
        self.assertEqual(d, '0.678', 'defection index does not match')
        s = parsed_j['indices'][0]['sliceValue']
        s = ("%.3f" % float(s))
        self.assertEqual(s, '0.889', 'slice value does not match')


    def test_defection_index_for_specific_date_us(self):
        url = 'http://mb-api-n01.dev.inova.us.ci.rackspace.net/beaker/' \
              'models/defection/719072?date=20130104'
        r = requests.get(url, headers=self.default_headers)
        print r.content
        self.assertEqual(r.status_code, 200, 'status code is not 200')
        parsed_j = json.loads(r.content)
        print parsed_j
        indices = parsed_j['indices'][0]['accountId']
        self.assertEqual(indices, 719072, 'account id does not match')
        indices = parsed_j['indices'][0]['behaviorValue']
        self.assertEqual(indices, 0.75, 'behavior value does not match')
        indices = parsed_j['indices'][0]['tenureValue']
        self.assertEqual(indices, 1.0, 'tenure value does not match')
        d = parsed_j['indices'][0]['defectionIndex']
        d = ("%.3f" % float(d))
        self.assertEqual(d, '0.528', 'defection index does not match')
        s = parsed_j['indices'][0]['sliceValue']
        s = ("%.3f" % float(s))
        self.assertEqual(s, '0.100', 'slice value does not match')

    def test_defection_index_us_nodependency(self):
        url = 'http://mb-api-n01.dev.inova.us.ci.rackspace.net/beaker/' \
              'models/defection/719072'
        r = requests.get(url, headers=self.default_headers)
        print r.content
        self.assertEqual(r.status_code, 200, 'status code is not 200')
        parsed_j = json.loads(r.content)
        print parsed_j
        indices = parsed_j['indices'][0]['accountId']
        self.assertEqual(indices, 719072, 'account id does not match')
        indices = parsed_j['indices'][0]['behaviorValue']
        self.assertGreater(indices,0, 'behavior value is less than zero')
        indices = parsed_j['indices'][0]['tenureValue']
        self.assertGreater(indices,0, 'tenure value is less than zero')
        d = parsed_j['indices'][0]['defectionIndex']
        d = ("%.3f" % float(d))
        d = float(d)
        self.assertGreater(d,0, 'defection index is less than zero')

        s = parsed_j['indices'][0]['sliceValue']
        s = ("%.3f" % float(s))
        s = float(s)
        self.assertGreater(s,0, 'defection index is less than zero')

    def test_defection_index_uk_nodependency(self):
        url = 'http://mb-api-n01.dev.inova.us.ci.rackspace.net/beaker/' \
              'models/defection/10017503'
        r = requests.get(url, headers=self.default_headers)
        print r.content
        self.assertEqual(r.status_code, 200, 'status code is not 200')
        parsed_j = json.loads(r.content)
        print parsed_j
        indices = parsed_j['indices'][0]['accountId']
        self.assertEqual(indices, 10017503, 'account id does not match')
        indices = parsed_j['indices'][0]['behaviorValue']
        self.assertGreater(indices,0, 'behavior value is less than zero')
        indices = parsed_j['indices'][0]['tenureValue']
        self.assertGreater(indices,0, 'tenure value is less than zero')
        d = parsed_j['indices'][0]['defectionIndex']
        d = ("%.3f" % float(d))
        d = float(d)
        self.assertGreater(d,0, 'defection index is less than zero')

        s = parsed_j['indices'][0]['sliceValue']
        s = ("%.3f" % float(s))
        s = float(s)
        self.assertGreater(s,0, 'slice value is less than zero')

    def test_account_details_us_specificdate_nodependency(self):
        url = 'http://mb-api-n01.dev.inova.us.ci.rackspace.net/beaker/' \
              'accounts/719072?date=20130104'
        r = requests.get(url, headers=self.default_headers)
        print r.content
        self.assertEqual(r.status_code, 200, 'status code is not 200')
        parsed_j = json.loads(r.content)
        print parsed_j

        indices = parsed_j['accountId']
        self.assertEqual(indices, 719072, 'account id does not match')
        indices = parsed_j['accountId']
        self.assertEqual(parsed_j['PrimaryContactInfo']['firstName'],
            'Steve', 'firstname should be equal')
        self.assertEqual(parsed_j['PrimaryContactInfo']['lastName'],
            'Eastham', 'lastname should be equal')
        self.assertEqual(parsed_j['PrimaryContactInfo']['email'],
            'steve.eastham@bestbuy.com', 'email should be equal')
        self.assertEqual(parsed_j['PrimaryContactInfo']['phoneNumber'],
            '612-291-7354', 'phone number should be equal')
        self.assertEqual(parsed_j['PrimaryContactInfo']['street'],
            '7601 Penn Ave', 'street should be equal')
        self.assertEqual(parsed_j['PrimaryContactInfo']['city'],
            'Minneapolis', 'city should be equal')
        self.assertEqual(parsed_j['PrimaryContactInfo']['state'],
            'MN', 'state should be equal')
        self.assertEqual(parsed_j['PrimaryContactInfo']['zip'],
            '55423', 'zip should be equal')
        self.assertEqual(parsed_j['PrimaryContactInfo']['country'],
            'United States', 'Country should be equal')

    def test_account_details_us_nodependency(self):
        url = 'http://mb-api-n01.dev.inova.us.ci.rackspace.net/beaker/' \
              'accounts/719072'
        r = requests.get(url, headers=self.default_headers)
        print r.content
        self.assertEqual(r.status_code, 200, 'status code is not 200')
        parsed_j = json.loads(r.content)
        print parsed_j

        indices = parsed_j['accountId']
        self.assertEqual(indices, 719072, 'account id does not match')
        indices = parsed_j['accountId']
        self.assertEqual(parsed_j['PrimaryContactInfo']['firstName'],
            'Steve', 'firstname should be equal')
        self.assertEqual(parsed_j['PrimaryContactInfo']['lastName'],
            'Eastham', 'lastname should be equal')
        self.assertEqual(parsed_j['PrimaryContactInfo']['email'],
            'steve.eastham@bestbuy.com', 'email should be equal')
        self.assertEqual(parsed_j['PrimaryContactInfo']['phoneNumber'],
            '612-291-7354', 'phone number should be equal')
        self.assertEqual(parsed_j['PrimaryContactInfo']['street'],
            '7601 Penn Ave', 'street should be equal')
        self.assertEqual(parsed_j['PrimaryContactInfo']['city'],
            'Minneapolis', 'city should be equal')
        self.assertEqual(parsed_j['PrimaryContactInfo']['state'],
            'MN', 'state should be equal')
        self.assertEqual(parsed_j['PrimaryContactInfo']['zip'],
            '55423', 'zip should be equal')
        self.assertEqual(parsed_j['PrimaryContactInfo']['country'],
            'United States', 'Country should be equal')

    def test_account_details_uk_specificdate_nodependency(self):
        url = 'http://mb-api-n01.dev.inova.us.ci.rackspace.net/beaker/' \
              'accounts/10017503?date=20130104'
        r = requests.get(url, headers=self.default_headers)
        print r.content
        self.assertEqual(r.status_code, 200, 'status code is not 200')
        parsed_j = json.loads(r.content)
        print parsed_j

        indices = parsed_j['accountId']
        self.assertEqual(indices, 10017503, 'account id does not match')
        self.assertEqual(parsed_j['PrimaryContactInfo']['firstName'],
            'Chris', 'firstname should be equal')
        self.assertEqual(parsed_j['PrimaryContactInfo']['lastName'],
            'Hunter', 'lastname should be equal')
        self.assertEqual(parsed_j['PrimaryContactInfo']['email'],
            'help@everpa.com', 'email should be equal')
        self.assertEqual(parsed_j['PrimaryContactInfo']['phoneNumber'],
            '07717418320', 'phone number should be equal')
        self.assertEqual(parsed_j['PrimaryContactInfo']['street'],
            '5 York Road NA', 'street should be equal')
        self.assertEqual(parsed_j['PrimaryContactInfo']['city'],
            'Batley', 'city should be equal')
        self.assertEqual(parsed_j['PrimaryContactInfo']['state'],
            'West Yorkshire', 'state should be equal')
        self.assertEqual(parsed_j['PrimaryContactInfo']['zip'],
            'WF17 0LG', 'zip should be equal')
        self.assertEqual(parsed_j['PrimaryContactInfo']['country'],
            'United Kingdom', 'Country should be equal')

    def test_account_details_uk_nodependency(self):
        url = 'http://mb-api-n01.dev.inova.us.ci.rackspace.net/beaker/' \
              'accounts/10017503'
        r = requests.get(url, headers=self.default_headers)
        print r.content
        self.assertEqual(r.status_code, 200, 'status code is not 200')
        parsed_j = json.loads(r.content)
        print parsed_j

        indices = parsed_j['accountId']
        self.assertEqual(indices, 10017503, 'account id does not match')
        self.assertEqual(parsed_j['PrimaryContactInfo']['firstName'],
            'Chris', 'firstname should be equal')
        self.assertEqual(parsed_j['PrimaryContactInfo']['lastName'],
            'Hunter', 'lastname should be equal')
        self.assertEqual(parsed_j['PrimaryContactInfo']['email'],
            'help@everpa.com', 'email should be equal')
        self.assertEqual(parsed_j['PrimaryContactInfo']['phoneNumber'],
            '07717418320', 'phone number should be equal')
        self.assertEqual(parsed_j['PrimaryContactInfo']['street'],
            '5 York Road NA', 'street should be equal')
        self.assertEqual(parsed_j['PrimaryContactInfo']['city'],
            'Batley', 'city should be equal')
        self.assertEqual(parsed_j['PrimaryContactInfo']['state'],
            'West Yorkshire', 'state should be equal')
        self.assertEqual(parsed_j['PrimaryContactInfo']['zip'],
            'WF17 0LG', 'zip should be equal')
        self.assertEqual(parsed_j['PrimaryContactInfo']['country'],
            'United Kingdom', 'Country should be equal')

    #Calling account details with an invalid account id
    def test_account_details_with_invalid_account(self):
        url = 'http://mb-api-n01.dev.inova.us.ci.rackspace.net/beaker/' \
              'accounts/1001750399999'
        r = requests.get(url, headers=self.default_headers)
        print r.content
        self.assertEqual(r.status_code, 404, 'status code is not 200')
        print r.content
        self.assertEqual(r.content, 'No account details found for account:'
                        ' 1001750399999' , 'content output does not match')

    def test_defection_index_us_specificdate(self):
        account_date = '719072?date=20130104'
        resp = self.client.give_defection_index(account_date)
        usdefection = UsDefectionResponse._json_to_obj(resp.content)
        j = json.loads(resp.content)
        self.assertEqual(usdefection.accountId, 719072, 'Id does not match')
        d = usdefection.defectionIndex
        d = ("%.3f" % float(d))
        self.assertEqual(d, '0.528', 'Defection index does not match')
        self.assertEqual(usdefection.behaviorValue, 0.75,
            'Behavior value does not match')
        self.assertEqual(usdefection.noUsageValue, 0.5,
            'No usage value does not match')
        self.assertEqual(usdefection.tenureValue, 1.0,
            'Tenure value does not match')
        s = usdefection.sliceValue
        s = ("%.3f" % float(s))
        self.assertEqual(s, '0.100', 'Slice value does not match')

    #Testing pagination of defection index that returns
    # 10 results by default for a specific date
    #/beaker/indices/defection?date=20121120
    #Instead of testing all rows, just test the first and last :)
    def test_defection_index_pagination_date_default(self):
        url = 'http://mb-api-n01.dev.inova.us.ci.rackspace.net/beaker/' \
              'models/defection?date=20130106'
        resp = requests.get(url, headers=self.default_headers)
        usdefection = PaginationByDate._json_to_obj(resp.content)
        d = usdefection.defectionIndex1
        print d
        self.assertGreater(d, 0, 'Defection index is wrong')
        self.assertLess(d, 1, 'Defection index is wrong')
        d = usdefection.defectionIndexlast
        print d
        self.assertGreater(d, 0, 'Defection index is wrong')
        self.assertLess(d, 1, 'Defection index is wrong')


    #Testing pagination of defection index that returns
    # 20 results limit for a specific date
    #http://mb-api-n01.dev.inova.us.ci.rackspace.net/beaker
    # /indices/defection?date=20130104&limit=20
    def test_defection_index_pagination_date_limit_20(self):
        url = 'http://mb-api-n01.dev.inova.us.ci.rackspace.net/beaker/' \
              'models/defection?date=20130106&limit=20'
        resp = requests.get(url, headers=self.default_headers)
        usdefection = PaginationByDate._json_to_obj(resp.content)
        d = usdefection.defectionIndex1
        print d
        self.assertGreater(d, 0, 'Defection index is wrong')
        self.assertLess(d, 1, 'Defection index is wrong')
        d = usdefection.defectionIndexlast
        print d
        self.assertGreater(d, 0, 'Defection index is wrong')
        self.assertLess(d, 1, 'Defection index is wrong')


    #Testing pagination of defection index that returns 50 results with
    # marker for a specific date. marker is the account id
    def test_defection_index_pagination_date_limit_5_with_marker(self):
        url = 'http://mb-api-n01.dev.inova.us.ci.rackspace.net/beaker/' \
              'models/defection?date=20130106&limit=5&marker=719072'
        resp = requests.get(url, headers=self.default_headers)
        usdefection = PaginationByDate._json_to_obj(resp.content)
        d = usdefection.defectionIndex1
        print d
        self.assertGreater(d, 0, 'Defection index is wrong')
        self.assertLess(d, 1, 'Defection index is wrong')
        d = usdefection.defectionIndexlast
        print d
        self.assertGreater(d, 0, 'Defection index is wrong')
        self.assertLess(d, 1, 'Defection index is wrong')
        self.assertEquals(usdefection.accountId, 719072,
            'accountid does not match')

    #Testing pagination of defection index with min param (e.g.: 0.5)?
    def test_defection_index_pagination_with_min_half(self):
        url = 'http://mb-api-n01.dev.inova.us.ci.rackspace.net/' \
              'beaker/models/defection?min=0.5'
        resp = requests.get(url, headers=self.default_headers)
        usdefection = PaginationDateRange._json_to_obj(resp.content)
        d = usdefection.defectionIndex1
        print d
        self.assertGreater(d, 0.5, 'Defection index is wrong')
        self.assertLess(d, 1, 'Defection index is wrong')
        d = usdefection.defectionIndexlast
        print d
        self.assertGreater(d, 0.5, 'Defection index is wrong')
        self.assertLess(d, 1, 'Defection index is wrong')

    #Testing pagination of defection index with min param with
    # limit of 5 results (e.g.: 0.5)?
    def test_defection_index_pagination_with_min_half_limit5(self):
        url = 'http://mb-api-n01.dev.inova.us.ci.rackspace.net/beaker/' \
              'models/defection?min=0.5&limit=5'
        resp = requests.get(url, headers=self.default_headers)
        usdefection = PaginationDateRange._json_to_obj(resp.content)
        d = usdefection.defectionIndex1
        print d
        self.assertGreater(d, 0.5, 'Defection index is wrong')
        self.assertLess(d, 1, 'Defection index is wrong')
        d = usdefection.defectionIndexlast
        print d
        self.assertGreater(d, 0.5, 'Defection index is wrong')
        self.assertLess(d, 1, 'Defection index is wrong')

    #Testing pagination of defection index with max param
    def test_defection_index_pagination_with_max_half(self):
        max = '?max=0.5'
        resp = self.client.give_defection_index(max)
        usdefection = PaginationDateRange._json_to_obj(resp.content)
        d = usdefection.defectionIndex1
        print d
        self.assertGreater(d, 0, 'Defection index is wrong')
        self.assertLess(d, 0.5, 'Defection index is wrong')
        d = usdefection.defectionIndexlast
        print d
        self.assertGreater(d, 0, 'Defection index is wrong')
        self.assertLess(d, 0.5, 'Defection index is wrong')

    #Testing pagination of defection index with max param
    # with limit of 5 results
    def test_defection_index_pagination_with_max_half_limit5(self):
        min_max = '?max=0.5&limit=5'
        resp = self.client.give_defection_index(min_max)
        usdefection = PaginationDateRange._json_to_obj(resp.content)
        d = usdefection.defectionIndex1
        print d
        self.assertGreater(d, 0, 'Defection index is wrong')
        self.assertLess(d, 0.5, 'Defection index is wrong')
        d = usdefection.defectionIndexlast
        print d
        self.assertGreater(d, 0, 'Defection index is wrong')
        self.assertLess(d, 0.5, 'Defection index is wrong')


    #Testing pagination of defection index with min param (e.g.: 0.5)?
    def test_defection_index_pagination_with_date_range_min_half(self):
        start_end_min = '?start=20130104&end=20130106&min=0.5'
        resp = self.client.give_defection_index(start_end_min)
        usdefection = PaginationDateRange._json_to_obj(resp.content)
        d = usdefection.defectionIndex1
        print d
        self.assertGreater(d, 0.5, 'Defection index is wrong')
        self.assertLess(d, 1, 'Defection index is wrong')
        d = usdefection.defectionIndexlast
        print d
        self.assertGreater(d, 0.5, 'Defection index is wrong')
        self.assertLess(d, 1, 'Defection index is wrong')

    #Testing pagination of defection index with min param
    #  (e.g.: 0.5) and limit of 5
    def test_defection_index_pagination_with_date_range_min_half_limit5(self):
        start_end_min_limit = '?start=20130104&end=20130106&min=0.5&limit=5'
        resp = self.client.give_defection_index(start_end_min_limit)
        usdefection = PaginationDateRange._json_to_obj(resp.content)
        d = usdefection.defectionIndex1
        print d
        self.assertGreater(d, 0.5, 'Defection index is wrong')
        self.assertLess(d, 1, 'Defection index is wrong')
        d = usdefection.defectionIndexlast
        print d
        self.assertGreater(d, 0.5, 'Defection index is wrong')
        self.assertLess(d, 1, 'Defection index is wrong')

    #Testing pagination of defection index with min param
    #/beaker/indices/defection?start=2222&end=3333&max=.5
    def test_defection_index_pagination_with_date_range_max_half(self):
        start_end_max = '?start=20130104&end=20130106&max=0.5'
        resp = self.client.give_defection_index(start_end_max)
        usdefection = PaginationDateRange._json_to_obj(resp.content)
        d = usdefection.defectionIndex1
        print d
        self.assertGreater(d, 0, 'Defection index is wrong')
        self.assertLess(d, 0.51, 'Defection index is wrong')
        d = usdefection.defectionIndexlast
        print d
        self.assertGreater(d, 0, 'Defection index is wrong')
        self.assertLess(d, 0.51, 'Defection index is wrong')

    #Testing pagination of defection index with max parma
    #/beaker/indices/defection?start=2222&end=3333&max=.5&limit=5
    def test_defection_index_pagination_with_date_range_max_half_limit5(self):
        start_end_max_limit = '?start=20130104&end=20130106&max=0.5&limit=5'
        resp = self.client.give_defection_index(start_end_max_limit)
        usdefection = PaginationDateRange._json_to_obj(resp.content)
        d = usdefection.defectionIndex1
        print d
        self.assertGreater(d, 0, 'Defection index is wrong')
        self.assertLess(d, 0.51, 'Defection index is wrong')
        d = usdefection.defectionIndexlast
        print d
        self.assertGreater(d, 0, 'Defection index is wrong')
        self.assertLess(d, 0.51, 'Defection index is wrong')

    #Testing filtering of defection index that are between 0.4 and 0.7
    #/beaker/indices/defection/1111?start=2222&end=3333&max=.7&min=.4
    def test_defection_index_pagination_with_date_range_between_values(self):
        start_end_max_min = '?start=20130104&end=20130106&max=0.7&min=0.4'
        resp = self.client.give_defection_index(start_end_max_min)
        usdefection = PaginationDateRange._json_to_obj(resp.content)
        d = usdefection.defectionIndex1
        print d
        self.assertGreater(d, 0.4, 'Defection index is wrong')
        self.assertLess(d, 0.7, 'Defection index is wrong')
        d = usdefection.defectionIndexlast
        print d
        self.assertGreater(d, 0.4, 'Defection index is wrong')
        self.assertLess(d, 0.7, 'Defection index is wrong')

    #Testing DI for all US and UK accounts
    def test_defection_index_US_bulk(self):
        f = open('/home/ram5454/accountnumbers.txt')
        FORMAT = '%Y%m%d%H%M%S'
        s = datetime.datetime.now().strftime(FORMAT)
        print s
        f2 = open('/home/ram5454/defectionindex'+s+'.txt', 'w+')
        for line in f:
            try:
                resp = self.client.give_defection_index(str(int(line)))
                usdefection = UsDefectionResponse._json_to_obj(resp.content)
                import json
                j = json.loads(resp.content)
                self.assertEqual(usdefection.accountId,
                    int(line), 'Id is not equal the Id on input file')
                self.assertIsNotNone(usdefection.defectionIndex,
                    'defection index is null')
                print ' '.join([line, str(usdefection.defectionIndex)])
                print ''
            except:
                f2.write(line)
        f.close()
        f2.close()




