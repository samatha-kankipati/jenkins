# -*- coding: utf-8 -*-
import re
from ccengine.common.decorators import attr
from testrepo.common.testfixtures.rax_signup import\
    RaxSignupAPI_TrustedCloudSignupFixture_UK
from testrepo.common.testfixtures.rax_signup import CreditCards, Business_Type


class RaxSignupAPI_TrustedCloudSignupRequest_UK_PositiveSmoke(
        RaxSignupAPI_TrustedCloudSignupFixture_UK):

    @attr('uk_cloud', 'smoke_test')
    def test_uk_trusted_cloud_signup_request_default(self):
        '''
        Scenario: Create UK Trusted Cloud Account through SignUp Facade with
        all necessary details
        '''
        request_dict = self.get_signup_request_dict()

        api_response = self.client.signup_new_trusted_cloud_customer(
            **request_dict)
        self.assertDefaultResponseOK(api_response)

    def test_uk_trusted_cloud_signup_request_without_skip_fraud_check(self):
        '''
        Scenario: Create UK Trusted Cloud Account through SignUp Facade without
        skip_fraud_check
        '''
        signup_request = {'skip_fraud_check': None}

        request_dict = self.get_signup_request_dict(
            signup_request=signup_request)

        api_response = self.client.signup_new_trusted_cloud_customer(
            **request_dict)
        self.assertDefaultResponseOK(api_response)

    def test_uk_trusted_cloud_signup_request_with_skip_fraud_check_false(self):
        '''
        Scenario: Create UK Trusted Cloud Account through SignUp Facade with
        skip_fraud_check as false
        '''
        signup_request = {'skip_fraud_check': False}

        request_dict = self.get_signup_request_dict(
            signup_request=signup_request)

        api_response = self.client.signup_new_trusted_cloud_customer(
            **request_dict)
        self.assertDefaultResponseOK(api_response)

    def test_uk_trusted_cloud_signup_request_with_skip_fraud_check_true(self):
        '''
        Scenario: Create UK Trusted Cloud Account through SignUp Facade with
        skip_fraud_check as true
        '''
        signup_request = {'skip_fraud_check': True}

        request_dict = self.get_signup_request_dict(
            signup_request=signup_request)

        api_response = self.client.signup_new_trusted_cloud_customer(
            **request_dict)
        self.assertDefaultResponseOK(api_response)

    def test_uk_trusted_cloud_signup_request_without_service_level(self):
        '''
        Scenario: Create UK Trusted Cloud Account through SignUp Facade without
        Service Level
        '''
        signup_request = {'service_level': None}

        request_dict = self.get_signup_request_dict(
            signup_request=signup_request)

        api_response = self.client.signup_new_trusted_cloud_customer(
            **request_dict)
        self.assertDefaultResponseOK(api_response)

    def test_uk_trusted_cloud_signup_request_with_service_level_core(self):
        '''
        Scenario: Create UK Trusted Cloud Account through SignUp Facade with
        Service Level as CORE
        '''
        signup_request = {'service_level': 'CORE'}

        request_dict = self.get_signup_request_dict(
            signup_request=signup_request)

        api_response = self.client.signup_new_trusted_cloud_customer(
            **request_dict)
        self.assertDefaultResponseOK(api_response)

    def test_uk_trusted_cloud_signup_request_with_service_level_managed(self):
        '''
        Scenario: Create UK Trusted Cloud Account through SignUp Facade with
        Service Level as MANAGED
        '''
        signup_request = {'service_level': 'MANAGED'}

        request_dict = self.get_signup_request_dict(
            signup_request=signup_request)

        api_response = self.client.signup_new_trusted_cloud_customer(
            **request_dict)
        self.assertDefaultResponseOK(api_response)

    def test_uk_trusted_cloud_signup_request_without_referral_code(self):
        '''
        Scenario: Create UK Trusted Cloud Account through SignUp Facade without
        Referral Code
        '''
        signup_request = {'referral_code': None}

        request_dict = self.get_signup_request_dict(
            signup_request=signup_request)

        api_response = self.client.signup_new_trusted_cloud_customer(
            **request_dict)
        self.assertDefaultResponseOK(api_response)

    def test_uk_trusted_cloud_signup_request_without_vatcode(self):
        '''
        Scenario: Create UK Trusted Cloud Account through SignUp Facade without
        Vat Code
        '''
        signup_request = {'vat_code': None}

        request_dict = self.get_signup_request_dict(
            signup_request=signup_request)

        api_response = self.client.signup_new_trusted_cloud_customer(
            **request_dict)
        self.assertDefaultResponseOK(api_response)

    def test_uk_trusted_cloud_signup_request_without_suffix(self):
        '''
        Scenario: Create UK Trusted Cloud Account through SignUp Facade without
        Suffix
        '''
        default_contact = {'suffix': None}

        request_dict = self.get_signup_request_dict(
            default_contact=default_contact)

        api_response = self.client.signup_new_trusted_cloud_customer(
            **request_dict)
        self.assertDefaultResponseOK(api_response)

    def test_uk_trusted_cloud_signup_request_without_title(self):
        '''
        Scenario: Create UK Trusted Cloud Account through SignUp Facade without
        Title
        '''
        default_contact = {'title': None}

        request_dict = self.get_signup_request_dict(
            default_contact=default_contact)

        api_response = self.client.signup_new_trusted_cloud_customer(
            **request_dict)
        self.assertDefaultResponseOK(api_response)

    def test_uk_trusted_cloud_signup_request_without_suffix_and_title(self):
        '''
        Scenario: Create UK Trusted Cloud Account through SignUp Facade without
        Suffix and Title
        '''
        default_contact = {'suffix': None, 'title': None}

        request_dict = self.get_signup_request_dict(
            default_contact=default_contact)

        api_response = self.client.signup_new_trusted_cloud_customer(
            **request_dict)
        self.assertDefaultResponseOK(api_response)

    def test_uk_trusted_cloud_signup_request_without_contact_state(self):
        '''
        Scenario: Create UK Trusted Cloud Account through SignUp Facade without
        State
        '''
        default_address = {'state': None}

        request_dict = self.get_signup_request_dict(
            default_address=default_address)

        api_response = self.client.signup_new_trusted_cloud_customer(
            **request_dict)
        self.assertDefaultResponseOK(api_response)

    def test_uk_trusted_cloud_signup_request_without_contact_zipcode(self):
        '''
        Scenario: Create UK Trusted Cloud Account through SignUp Facade without
        Zipcode
        '''
        default_address = {'zipcode': None}

        request_dict = self.get_signup_request_dict(
            default_address=default_address)

        api_response = self.client.signup_new_trusted_cloud_customer(
            **request_dict)
        self.assertDefaultResponseOK(api_response)

    def test_uk_trusted_cloud_signup_request_without_business_type(self):
        '''
        Scenario: Create UK Trusted Cloud Account through SignUp Facade without
        Business Type
        '''
        signup_request = {'business_type': None}

        request_dict = self.get_signup_request_dict(
            signup_request=signup_request)

        api_response = self.client.signup_new_trusted_cloud_customer(
            **request_dict)
        self.assertDefaultResponseOK(api_response)

    def test_uk_trusted_cloud_signup_request_with_business_type_as_business(self):
        '''
        Scenario: Create UK Trusted Cloud Account through SignUp Facade with
        Business Type as BUSINESS
        '''
        signup_request = {'business_type': 'BUSINESS'}

        request_dict = self.get_signup_request_dict(
            signup_request=signup_request)

        api_response = self.client.signup_new_trusted_cloud_customer(
            **request_dict)
        self.assertDefaultResponseOK(api_response)

    def test_uk_trusted_cloud_signup_request_with_business_type_as_consumer(self):
        '''
        Scenario: Create UK Trusted Cloud Account through SignUp Facade with
        Business Type as CONSUMER
        '''
        signup_request = {'business_type': 'CONSUMER'}

        request_dict = self.get_signup_request_dict(
            signup_request=signup_request)

        api_response = self.client.signup_new_trusted_cloud_customer(
            **request_dict)
        self.assertDefaultResponseOK(api_response)

    def test_uk_trusted_cloud_signup_request_without_terms_and_conditions(self):
        '''
        Scenario: Create UK Trusted Cloud Account through SignUp Facade without
        Terms and Conditions
        '''
        signup_request = {'terms_and_conditions': None}

        request_dict = self.get_signup_request_dict(
            signup_request=signup_request)

        api_response = self.client.signup_new_trusted_cloud_customer(
            **request_dict)
        self.assertDefaultResponseOK(api_response)

    def test_uk_trusted_cloud_signup_request_with_terms_and_conditions_as_us(self):
        '''
        Scenario: Create UK Trusted Cloud Account through SignUp Facade with
        Terms and Conditions as US
        '''
        signup_request = {'terms_and_conditions': 'US'}

        request_dict = self.get_signup_request_dict(
            signup_request=signup_request)

        api_response = self.client.signup_new_trusted_cloud_customer(
            **request_dict)
        self.assertDefaultResponseOK(api_response)

    def test_uk_trusted_cloud_signup_request_with_terms_and_conditions_as_international(self):
        '''
        Scenario: Create UK Trusted Cloud Account through SignUp Facade with
        Terms and Conditions as INTERNATIONAL
        '''
        signup_request = {'terms_and_conditions': 'INTL'}

        request_dict = self.get_signup_request_dict(
            signup_request=signup_request)

        api_response = self.client.signup_new_trusted_cloud_customer(
            **request_dict)
        self.assertDefaultResponseOK(api_response)

    def test_uk_trusted_cloud_signup_request_with_appropriate_description(self):
        '''
        Scenario: Create UK Trusted Cloud Account through SignUp Facade with
        Appropriate Description
        '''
        signup_request = {
            'description': 'A Trusted Cloud Signup Request from the Portal '
            'site'}

        request_dict = self.get_signup_request_dict(
            signup_request=signup_request)

        api_response = self.client.signup_new_cloud_customer(**request_dict)
        self.assertDefaultResponseOK(api_response)

    def test_uk_trusted_cloud_signup_request_with_diactrics(self):
        '''
        Scenario: Create Account using UK trusted Cloud SignUp Facade with
        diactrics and check in get steps
        '''
        first = 'ÝÞßàáâã'
        last = 'äåæçèéê'
        # The encoding and decoding are done for that characters are not lost
        first1 = first.decode('utf-8')
        last1 = last.decode('utf-8')
        first2 = first1.encode('utf-8')
        last2 = last1.encode('utf-8')

        default_contact = {
            'first_name': first2,
            'last_name':  last2}
        signup_request = {'service_level': 'CORE',
                          'skip_fraud_check': False}

        request_dict = self.get_signup_request_dict(
            default_contact=default_contact, signup_request=signup_request)
        api_response = self.client.signup_new_trusted_cloud_customer(
            **request_dict)
        self.assertDefaultResponseOK(api_response)

        # To get the signupid
        response_headers = "{0}".format(api_response.headers)
        signup_id = re.search('v1/signups/(.+?)\',', response_headers).group(1)
        signup_id = {'id': signup_id}
        print signup_id
        # Steps to check whether the diactrics are passed to cybersource system

        api_response1 = "{0}".format((self.client.signup_steps(signup_id))
                             .content)
        regex = 'CYBERSOURCE_CARD_VALIDATION COMPLETE(.+?)CYBERSOURCE_CARD_VALIDATION'
        cs_request = re.search(regex, api_response1).group(1)
        self.assertIsNotNone(re.search(first2, cs_request),
                             "first name not found")
        self.assertIsNotNone(re.search(last2, cs_request),
                             "last name not found")

    def test_uk_trusted_cloud_signup_request_without_complete_order_items(self):
        '''
        Scenario: Create UK Trusted Cloud Account through SignUp Facade without
        Complete Order Items
        '''
        order_items = []

        request_dict = self.get_signup_request_dict(
            order_items=order_items)

        api_response = self.client.signup_new_trusted_cloud_customer(
            **request_dict)
        self.assertDefaultResponseOK(api_response)

    def test_uk_trusted_cloud_signup_request_with_amex_credit_card_type(self):
        '''
        Scenario: Create UK Trusted Cloud Account through SignUp Facade with
        AMEX Credit Card Type
        '''
        default_payment_card = {
            'card_number': CreditCards.AMERICANEXPRESS_CARD_NUMBER,
            'card_type': CreditCards.AMERICANEXPRESS_CARD}

        request_dict = self.get_signup_request_dict(
            default_payment_card=default_payment_card)

        api_response = self.client.signup_new_trusted_cloud_customer(
            **request_dict)
        self.assertDefaultResponseOK(api_response)

    def test_uk_trusted_cloud_signup_request_with_visa_credit_card_type(self):
        '''
        Scenario: Create UK Trusted Cloud Account through SignUp Facade with
        VISA Credit Card Type
        '''
        default_payment_card = {
            'card_number': CreditCards.VISA_CARD_NUMBER,
            'card_type': CreditCards.VISA_CARD}

        request_dict = self.get_signup_request_dict(
            default_payment_card=default_payment_card)

        api_response = self.client.signup_new_trusted_cloud_customer(
            **request_dict)
        self.assertDefaultResponseOK(api_response)

    def test_uk_trusted_cloud_signup_request_with_master_card_credit_card_type(self):
        '''
        Scenario: Create UK Trusted Cloud Account through SignUp Facade with
        MASTER CARD Credit Card Type
        '''
        default_payment_card = {
            'card_number': CreditCards.MASTER_CARD_NUMBER,
            'card_type': CreditCards.MASTER_CARD}

        request_dict = self.get_signup_request_dict(
            default_payment_card=default_payment_card)

        api_response = self.client.signup_new_trusted_cloud_customer(
            **request_dict)
        self.assertDefaultResponseOK(api_response)

    def test_uk_trusted_cloud_signup_request_with_discover_credit_card_type(self):
        '''
        Scenario: Create UK Trusted Cloud Account through SignUp Facade with
        DISCOVER Credit Card Type
        '''
        default_payment_card = {
            'card_number': CreditCards.DISCOVER_CARD_NUMBER,
            'card_type': CreditCards.DISCOVER_CARD}

        request_dict = self.get_signup_request_dict(
            default_payment_card=default_payment_card)

        api_response = self.client.signup_new_trusted_cloud_customer(
            **request_dict)
        self.assertDefaultResponseOK(api_response)

    def test_uk_trusted_cloud_signup_request_without_description(self):
        '''
        Scenario: Create UK Trusted Cloud Account through SignUp Facade without
        Description
        '''
        signup_request = {'description': ''}

        request_dict = self.get_signup_request_dict(
            signup_request=signup_request)

        api_response = self.client.signup_new_trusted_cloud_customer(
            **request_dict)
        self.assertDefaultResponseOK(api_response)

    def test_uk_trusted_cloud_signup_request_without_complete_affiliate_details(self):
        '''
        Scenario: Create UK Trusted Cloud Account through SignUp Facade without
        Complete Affiliate Details
        '''
        affiliate_code_and_type = {}

        request_dict = self.get_signup_request_dict(
            affiliate_code_and_type=affiliate_code_and_type)

        api_response = self.client.signup_new_trusted_cloud_customer(
            **request_dict)
        self.assertDefaultResponseOK(api_response)

    @attr('syd_test')
    def test_uk_trsted_cloud_with_au_primary_address_b2c_for_contract_entity(self):
        '''
        Scenario to test uk trusted cloud with b2c and au primary address for
        contract entity
        '''
        # Defining country_code and business_type
        cloud_type = 'UK'
        country_code = 'AU'
        business_type = Business_Type.CONSUMER

        default_address = {
            'city': 'Sydney',
            'country': country_code,
            'primary': True,
            'state': 'NSW',
            'street': '367 George Street',
            'zipcode': '2000'}
        signup_request = {'business_type': business_type}
        request_dict = self.get_signup_request_dict(
            default_address=default_address, signup_request=signup_request)
        api_response = self.client.signup_new_trusted_cloud_customer(
            **request_dict)
        self.assertDefaultResponseOK(api_response)

        # To get the signupid
        response_headers = "{0}".format(api_response.headers)
        signup_id = re.search('v1/signups/(.+?)\',', response_headers).group(1)

        # To validate the contract_entity
        self.validate_contract_entity(signup_id=signup_id,
                                      cloud_type=cloud_type,
                                      country_code=country_code,
                                      business_type=business_type)

    @attr('syd_test')
    def test_uk_trsted_cloud_with_gb_primary_address_b2b_for_contract_entity(self):
        '''
        Scenario to test uk trusted cloud with b2b and gb primary address for
        contract entity
        '''
        # Defining country_code and business_type
        cloud_type = 'UK'
        country_code = 'GB'
        business_type = Business_Type.BUSINESS

        default_address = {
            'city': 'London',
            'country': country_code,
            'primary': True,
            'state': 'England',
            'street': '5000 Walzem Road',
            'zipcode': 'W37RP'}
        signup_request = {'business_type': business_type}
        request_dict = self.get_signup_request_dict(
            default_address=default_address, signup_request=signup_request)
        api_response = self.client.signup_new_trusted_cloud_customer(
            **request_dict)
        self.assertDefaultResponseOK(api_response)

        # To get the signupid
        response_headers = "{0}".format(api_response.headers)
        signup_id = re.search('v1/signups/(.+?)\',', response_headers).group(1)

        # To validate the contract_entity
        self.validate_contract_entity(signup_id=signup_id,
                                      cloud_type=cloud_type,
                                      country_code=country_code,
                                      business_type=business_type)

    @attr('syd_test')
    def test_uk_trsted_cloud_with_us_primary_address_wo_business_type_for_contract_entity(self):
        '''
        Scenario to test uk trusted cloud without business type and us primary
        address for contract entity
        '''
        # Defining country_code and business_type
        cloud_type = 'UK'
        country_code = 'GB'
        business_type = None

        default_address = {
            'city': 'San Antonio',
            'country': country_code,
            'primary': True,
            'state': 'Texas',
            'street': '5000 Walzem Road',
            'zipcode': '78218'}
        signup_request = {'business_type': business_type}
        request_dict = self.get_signup_request_dict(
            default_address=default_address, signup_request=signup_request)
        api_response = self.client.signup_new_trusted_cloud_customer(
            **request_dict)
        self.assertDefaultResponseOK(api_response)

        # To get the signupid
        response_headers = "{0}".format(api_response.headers)
        signup_id = re.search('v1/signups/(.+?)\',', response_headers).group(1)

        # To validate the contract_entity
        self.validate_contract_entity(signup_id=signup_id,
                                      cloud_type=cloud_type,
                                      country_code=country_code,
                                      business_type=business_type)

    @attr('geo_location')
    def test_uk_trusted_cloud_with_geo_location(self):
        '''
        Scenario to test uk cloud with geo_location
        '''
        signup_request = {'geo_location': 'SYD'}
        request_dict = self.get_signup_request_dict(
            signup_request=signup_request)
        api_response = self.client.signup_new_trusted_cloud_customer(
            **request_dict)
        self.assertDefaultResponseOK(api_response)

        # To get the signupid
        response_headers = "{0}".format(api_response.headers)
        signup_id = re.search('v1/signups/(.+?)\',', response_headers).group(1)

        # To validate the steps that no call to identity is done
        signup_id = {'id': signup_id}
        steps_response = "{0}".format((self.client.signup_steps(signup_id))
                              .content)
        identity_regex = 'CLOUD_GEO_LOCATION'
        self.assertIsNone(re.search(identity_regex, steps_response),
                          "Identity Call is done")
