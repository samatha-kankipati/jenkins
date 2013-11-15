# -*- coding: utf-8 -*-
import re
from ccengine.common.decorators import attr
from testrepo.common.testfixtures.rax_signup import\
    RaxSignupAPI_CloudSignupFixture_UK
from testrepo.common.testfixtures.rax_signup import CreditCards
from testrepo.common.testfixtures.rax_signup import Business_Type


class RaxSignupAPI_CloudSignupRequestUK_PositiveSmoke(
        RaxSignupAPI_CloudSignupFixture_UK):

    def test_cloud_signup_request_uk_minimal(self):
        """
        Tests base test fixture default request
        """
        request_dict = self.get_signup_request_dict()
        api_response = self.client.signup_new_cloud_customer(**request_dict)
        self.assertDefaultResponseOK(api_response)

    @attr('geography')
    def test_cloud_signup_request_with_geography_uk_minimal(self):
        """
        Tests base test fixture default request
        """
        signup_request = {'region': None,
                          'geography': 'UK'}
        request_dict = self.get_signup_request_dict(
            signup_request=signup_request)
        api_response = self.client.signup_new_cloud_customer(**request_dict)
        self.assertDefaultResponseOK(api_response)

    def test_uk_cloud_signup_with_affiliate_code(self):
        """
        Scenario: Test Signup with affiliate code sent in
        """
        affiliate_code_and_type = {'code': self.get_affiliate_code(),
                                   'type_': self.get_affiliate_type()}
        request_dict = self.get_signup_request_dict(affiliate_code_and_type=
                                                    affiliate_code_and_type)
        api_response = self.client.signup_new_cloud_customer(**request_dict)
        self.assertDefaultResponseOK(api_response)

    @attr('uk_cloud', 'smoke_test')
    def test_uk_cloud_signup_request_default(self):
        """
        Scenario: Create UK Cloud Account through SignUp Facade with all
        necessary details
        """
        metadata = [
            {"key": "cloudSitesPurchased",
             "value": "false"},
            {"key": "cloudFilesPurchased",
             "value": "true"},
            {"key": "cloudServersPurchased",
             "value": "true"},
            {"key": "loadBalancersPurchased",
             "value": "false"},
            {"key": "ipAddress",
             "value": "10.186.925.23"},
            {"key": "rackUID",
             "value": "1111110000"},
            {"key": "deviceFingerPrint",
             "value": "111.000-222"}, ]

        request_dict = self.get_signup_request_dict(
            metadata=metadata)

        api_response = self.client.signup_new_cloud_customer(**request_dict)
        self.assertDefaultResponseOK(api_response)

    @attr('smoke_test')
    def test_uk_cloud_signup_request_with_diactrics(self):
        """
        Scenario: Try UK cloud signup with Diactrics character in name
        """
        first = 'ÎÏÐÑÒÓÔ'
        last = 'ÕÖØÙÚÛÜ'
        # The encoding and decoding are done for that characters are not lost
        first1 = first.decode('utf-8')
        last1 = last.decode('utf-8')
        first2 = first1.encode('utf-8')
        last2 = last1.encode('utf-8')

        default_contact = {
            'first_name': first2,
            'last_name':  last2}
        signup_request = {'service_level': 'CORE'}

        request_dict = self.get_signup_request_dict(
            default_contact=default_contact, signup_request=signup_request)
        api_response = self.client.signup_new_cloud_customer(**request_dict)
        self.assertDefaultResponseOK(api_response)

        # To get the signupid
        signup_id = self.get_marker(api_response)

        # Steps to check whether the diactrics are passed to cybersource system

        api_response1 = (self.client.signup_steps(signup_id)).content
        regex = 'CYBERSOURCE_CARD_VALIDATION COMPLETE(.+?)CYBERSOURCE_CARD_VALIDATION'
        cs_request = re.search(regex, api_response1).group(1)
        self.assertIsNotNone(re.search(first2, cs_request),
                             "first name not found")
        self.assertIsNotNone(re.search(last2, cs_request),
                             "last name not found")

    def test_uk_cloud_signup_request_without_skip_fraud_check(self):
        """
        Scenario: Create UK Cloud Account through SignUp Facade without
        skip_fraud_check
        """
        signup_request = {'skip_fraud_check': None}

        request_dict = self.get_signup_request_dict(
            signup_request=signup_request)

        api_response = self.client.signup_new_cloud_customer(**request_dict)
        self.assertDefaultResponseOK(api_response)

    def test_uk_cloud_signup_request_with_skip_fraud_check_as_false(self):
        """
        Scenario: Create UK Cloud Account through SignUp Facade with
        skip_fraud_check as false
        """
        signup_request = {'skip_fraud_check': False}

        request_dict = self.get_signup_request_dict(
            signup_request=signup_request)

        api_response = self.client.signup_new_cloud_customer(**request_dict)
        self.assertDefaultResponseOK(api_response)

    def test_uk_cloud_signup_request_without_service_level(self):
        """
        Scenario: Create UK Cloud Account through SignUp Facade without
        Service Level
        """
        signup_request = {'service_level': None}

        request_dict = self.get_signup_request_dict(
            signup_request=signup_request)

        api_response = self.client.signup_new_cloud_customer(**request_dict)
        self.assertDefaultResponseOK(api_response)

    def test_uk_cloud_signup_request_with_service_level_as_core(self):
        """
        Scenario: Create UK Cloud Account through SignUp Facade with
        Service Level as CORE
        """
        signup_request = {'service_level': 'CORE'}

        request_dict = self.get_signup_request_dict(
            signup_request=signup_request)

        api_response = self.client.signup_new_cloud_customer(**request_dict)
        self.assertDefaultResponseOK(api_response)

    def test_uk_cloud_signup_request_with_service_level_as_managed(self):
        """
        Scenario: Create UK Cloud Account through SignUp Facade with
        Service Level as MANAGED
        """
        signup_request = {'service_level': 'MANAGED'}

        request_dict = self.get_signup_request_dict(
            signup_request=signup_request)

        api_response = self.client.signup_new_cloud_customer(**request_dict)
        self.assertDefaultResponseOK(api_response)

    def test_uk_cloud_signup_request_without_referral_code(self):
        """
        Scenario: Create UK Cloud Account through SignUp Facade without
        Referral Code
        """
        signup_request = {'referral_code': None}

        request_dict = self.get_signup_request_dict(
            signup_request=signup_request)

        api_response = self.client.signup_new_cloud_customer(**request_dict)
        self.assertDefaultResponseOK(api_response)

    def test_uk_cloud_signup_request_without_promo_code(self):
        """
        Scenario: Create UK Cloud Account through SignUp Facade without
        Promo Code
        """
        signup_request = {'promo_code': None}

        request_dict = self.get_signup_request_dict(
            signup_request=signup_request)

        api_response = self.client.signup_new_cloud_customer(**request_dict)
        self.assertDefaultResponseOK(api_response)

    def test_uk_cloud_signup_request_without_vat_code(self):
        """
        Scenario: Create UK Cloud Account through SignUp Facade without
        Vat Code
        """
        signup_request = {'vat_code': None}

        request_dict = self.get_signup_request_dict(
            signup_request=signup_request)

        api_response = self.client.signup_new_cloud_customer(**request_dict)
        self.assertDefaultResponseOK(api_response)

    def test_uk_cloud_signup_request_without_suffix(self):
        """
        Scenario: Create UK Cloud Account through SignUp Facade without Suffix
        """
        default_contact = {'suffix': None}

        request_dict = self.get_signup_request_dict(
            default_contact=default_contact)

        api_response = self.client.signup_new_cloud_customer(**request_dict)
        self.assertDefaultResponseOK(api_response)

    def test_uk_cloud_signup_request_without_title(self):
        """
        Scenario: Create UK Cloud Account through SignUp Facade without Title
        """
        default_contact = {'title': None}

        request_dict = self.get_signup_request_dict(
            default_contact=default_contact)

        api_response = self.client.signup_new_cloud_customer(**request_dict)
        self.assertDefaultResponseOK(api_response)

    def test_uk_cloud_signup_request_without_suffix_and_title(self):
        """
        Scenario: Create UK Cloud Account through SignUp Facade without Suffix
        and Title
        """
        default_contact = {'suffix': None, 'title': None}

        request_dict = self.get_signup_request_dict(
            default_contact=default_contact)

        api_response = self.client.signup_new_cloud_customer(**request_dict)
        self.assertDefaultResponseOK(api_response)

    def test_uk_cloud_signup_request_without_contact_state(self):
        """
        Scenario: Create UK Cloud Account through SignUp Facade without Contact
        State
        """
        default_address = {'state': None}

        request_dict = self.get_signup_request_dict(
            default_address=default_address)

        api_response = self.client.signup_new_cloud_customer(**request_dict)
        self.assertDefaultResponseOK(api_response)

    def test_uk_cloud_signup_request_without_contact_zipcode(self):
        """
        Scenario: Create UK Cloud Account through SignUp Facade without Contact
        Zipcode
        """
        default_address = {'zipcode': None}

        request_dict = self.get_signup_request_dict(
            default_address=default_address)

        api_response = self.client.signup_new_cloud_customer(**request_dict)
        self.assertDefaultResponseOK(api_response)

    def test_uk_cloud_signup_request_without_business_type(self):
        """
        Scenario: Create UK Cloud Account through SignUp Facade without
        Business Type
        """
        signup_request = {'business_type': None}

        request_dict = self.get_signup_request_dict(
            signup_request=signup_request)

        api_response = self.client.signup_new_cloud_customer(**request_dict)
        self.assertDefaultResponseOK(api_response)

    def test_uk_cloud_signup_request_with_business_type_as_business(self):
        """
        Scenario: Create UK Cloud Account through SignUp Facade with Business
        Type as BUSINESS
        """
        signup_request = {'business_type': 'BUSINESS'}

        request_dict = self.get_signup_request_dict(
            signup_request=signup_request)

        api_response = self.client.signup_new_cloud_customer(**request_dict)
        self.assertDefaultResponseOK(api_response)

    def test_uk_cloud_signup_request_with_business_type_as_consumer(self):
        """
        Scenario: Create UK Cloud Account through SignUp Facade with Business
        Type as CONSUMER
        """
        signup_request = {'business_type': 'CONSUMER'}

        request_dict = self.get_signup_request_dict(
            signup_request=signup_request)

        api_response = self.client.signup_new_cloud_customer(**request_dict)
        self.assertDefaultResponseOK(api_response)

    def test_uk_cloud_signup_request_without_terms_and_conditions(self):
        """
        Scenario: Create UK Cloud Account through SignUp Facade without Terms
        and Conditions
        """
        signup_request = {'terms_and_conditions': None}

        request_dict = self.get_signup_request_dict(
            signup_request=signup_request)

        api_response = self.client.signup_new_cloud_customer(**request_dict)
        self.assertDefaultResponseOK(api_response)

    def test_uk_cloud_signup_request_with_terms_and_conditions_as_us(self):
        """
        Scenario: Create UK Cloud Account through SignUp Facade with Terms
        and Conditions as US
        """
        signup_request = {'terms_and_conditions': 'US'}

        request_dict = self.get_signup_request_dict(
            signup_request=signup_request)

        api_response = self.client.signup_new_cloud_customer(**request_dict)
        self.assertDefaultResponseOK(api_response)

    def test_uk_cloud_signup_request_with_terms_and_conditions_as_international(self):
        """
        Scenario: Create UK Cloud Account through SignUp Facade with Terms
        and Conditions as INTERNATIONAL
        """
        signup_request = {'terms_and_conditions': 'INTL'}

        request_dict = self.get_signup_request_dict(
            signup_request=signup_request)

        api_response = self.client.signup_new_cloud_customer(**request_dict)
        self.assertDefaultResponseOK(api_response)

    def test_uk_cloud_signup_request_with_appropriate_description(self):
        """
        Scenario: Create UK Cloud Account through SignUp Facade with
        Appropriate Description
        """
        signup_request = {
            'description': 'A Cloud Signup Request from the Retail site'}

        request_dict = self.get_signup_request_dict(
            signup_request=signup_request)

        api_response = self.client.signup_new_cloud_customer(**request_dict)
        self.assertDefaultResponseOK(api_response)

    def test_uk_cloud_signup_request_without_description(self):
        """
        Scenario: Create UK Cloud Account through SignUp Facade without
        Description
        """
        signup_request = {'description': ''}

        request_dict = self.get_signup_request_dict(
            signup_request=signup_request)

        api_response = self.client.signup_new_cloud_customer(**request_dict)
        self.assertDefaultResponseOK(api_response)

    def test_uk_cloud_signup_request_without_complete_affiliate_details(self):
        """
        Scenario: Create UK Cloud Account through SignUp Facade without
        Complete Affiliate Details
        """
        affiliate_code_and_type = {}

        request_dict = self.get_signup_request_dict(
            affiliate_code_and_type=affiliate_code_and_type)

        api_response = self.client.signup_new_cloud_customer(**request_dict)
        self.assertDefaultResponseOK(api_response)

    def test_uk_cloud_signup_request_with_amex_credit_card_type(self):
        """
        Scenario: Create UK Cloud Account through SignUp Facade with AMEX
        Credit Card Type
        """
        default_payment_card = {
            'card_number': CreditCards.AMERICANEXPRESS_CARD_NUMBER,
            'card_type': CreditCards.AMERICANEXPRESS_CARD}

        request_dict = self.get_signup_request_dict(
            default_payment_card=default_payment_card)

        api_response = self.client.signup_new_cloud_customer(**request_dict)
        self.assertDefaultResponseOK(api_response)

    def test_uk_cloud_signup_request_with_visa_credit_card_type(self):
        """
        Scenario: Create UK Cloud Account through SignUp Facade with VISA
        Credit Card Type
        """
        default_payment_card = {
            'card_number': CreditCards.VISA_CARD_NUMBER,
            'card_type': CreditCards.VISA_CARD}

        request_dict = self.get_signup_request_dict(
            default_payment_card=default_payment_card)

        api_response = self.client.signup_new_cloud_customer(**request_dict)
        self.assertDefaultResponseOK(api_response)

    def test_uk_cloud_signup_request_with_master_card_credit_card_type(self):
        """
        Scenario: Create UK Cloud Account through SignUp Facade with
        MASTER CARD Credit Card Type
        """
        default_payment_card = {
            'card_number': CreditCards.MASTER_CARD_NUMBER,
            'card_type': CreditCards.MASTER_CARD}

        request_dict = self.get_signup_request_dict(
            default_payment_card=default_payment_card)

        api_response = self.client.signup_new_cloud_customer(**request_dict)
        self.assertDefaultResponseOK(api_response)

    def test_uk_cloud_signup_request_with_discover_credit_card_type(self):
        """
        Scenario: Create UK Cloud Account through SignUp Facade with DISCOVER
        Credit Card Type
        """
        default_payment_card = {
            'card_number': CreditCards.DISCOVER_CARD_NUMBER,
            'card_type': CreditCards.DISCOVER_CARD}

        request_dict = self.get_signup_request_dict(
            default_payment_card=default_payment_card)

        api_response = self.client.signup_new_cloud_customer(**request_dict)
        self.assertDefaultResponseOK(api_response)

    @attr('syd_test')
    def test_uK_cloud_with_au_primary_address_b2c_for_contract_entity(self):
        """
        Scenario to test uk cloud with b2c and au primary address for
        contract entity
        """
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
        api_response = self.client.signup_new_cloud_customer(**request_dict)
        self.assertDefaultResponseOK(api_response)

        # To validate the contract_entity
        self.validate_contract_entity(api_response=api_response,
                                      cloud_type=cloud_type,
                                      country_code=country_code,
                                      business_type=business_type)

    @attr('syd_test')
    def test_uK_cloud_with_gb_primary_address_b2b_for_contract_entity(self):
        """
        Scenario to test uk cloud with b2b and gb primary address for
        contract entity
        """
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
        api_response = self.client.signup_new_cloud_customer(**request_dict)
        self.assertDefaultResponseOK(api_response)

        # To validate the contract_entity
        self.validate_contract_entity(api_response=api_response,
                                      cloud_type=cloud_type,
                                      country_code=country_code,
                                      business_type=business_type)

    @attr('syd_test')
    def test_uK_cloud_with_us_primary_address_wo_business_type_for_contract_entity(self):
        """
        Scenario to test uk cloud without business type and us primary address
        for contract entity
        """
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
        api_response = self.client.signup_new_cloud_customer(**request_dict)
        self.assertDefaultResponseOK(api_response)

        # To validate the contract_entity
        self.validate_contract_entity(api_response=api_response,
                                      cloud_type=cloud_type,
                                      country_code=country_code,
                                      business_type=business_type)

    @attr('geo_location')
    def test_uk_cloud_with_geo_location(self):
        """
        Scenario to test uk cloud with geo_location
        """
        signup_request = {'geo_location': 'SYD'}
        request_dict = self.get_signup_request_dict(
            signup_request=signup_request)
        api_response = self.client.signup_new_cloud_customer(**request_dict)
        self.assertDefaultResponseOK(api_response)

        # To get the signupid
        signup_id = self.get_marker(api_response)

        # To validate the steps that no call to identity is done
        steps_response = (self.client.signup_steps(signup_id)).content
        identity_regex = 'CLOUD_GEO_LOCATION'
        self.assertIsNone(re.search(identity_regex, steps_response),
                          "Identity Call is done")

    @attr('welcome_email')
    def test_uk_cloud_signup_welcome_email(self):
        """
        Scenario: To test welcome email functionality
        """
        request_dict = self.get_signup_request_dict()
        api_response = self.client.signup_new_cloud_customer(**request_dict)
        self.assertDefaultResponseOK(api_response)
        self.welcome_email_assertions(api_response, geography='UK')

    @attr('welcome_email')
    def test_uk_cloud_signup_with_service_level_core(self):
        """
        Scenario: to test whether the correct mail template is selected when
        service_level is core
        """
        service_level = 'CORE'
        signup_request = {'service_level': service_level}
        request_dict = self.get_signup_request_dict(
            signup_request=signup_request)
        api_response = self.client.signup_new_cloud_customer(**request_dict)
        self.assertDefaultResponseOK(api_response)
        self.welcome_email_assertions(api_response,
                                      service_level=service_level,
                                      geography='UK')
