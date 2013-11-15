# -*- coding: utf-8 -*-
import re
from ccengine.common.decorators import attr
from testrepo.common.testfixtures.rax_signup import\
    RaxSignupAPI_TrustedCloudSignupFixture
from testrepo.common.testfixtures.rax_signup import CreditCards, Business_Type


class RaxSignupAPI_TrustedCloudSignupRequest_PositiveSmoke(
        RaxSignupAPI_TrustedCloudSignupFixture):

    def test_us_trusted_cloud_signup_request_default(self):
        """
        Scenario: Create US Trusted Cloud Account through SignUp Facade with
        all necessary details
        """
        request_dict = self.get_signup_request_dict()

        api_response = self.client.signup_new_trusted_cloud_customer(
            **request_dict)
        self.assertDefaultResponseOK(api_response)

    @attr('geography')
    def test_us_trusted_cloud_signup_request_minimal_with_geography(self):
        """
        Tests base test fixture default request
        """
        signup_request = {'region': None,
                          'geography': 'US'}
        request_dict = self.get_signup_request_dict(
            signup_request=signup_request)
        api_response = self.client.signup_new_cloud_customer(**request_dict)
        self.assertDefaultResponseOK(api_response)

    def test_us_trusted_cloud_signup_with_affiliate_code(self):
        """
        Scenario: Test Signup with affiliate code sent in
        """
        affiliate_code_and_type = {'code': self.get_affiliate_code(),
                                   'type_': self.get_affiliate_type()}
        request_dict = self.get_signup_request_dict(affiliate_code_and_type=
                                                    affiliate_code_and_type)
        api_response = self.client.signup_new_trusted_cloud_customer(
            **request_dict)
        self.assertDefaultResponseOK(api_response)

    def test_us_trusted_cloud_signup_request_without_skip_fraud_check(self):
        """
        Scenario: Create US Trusted Cloud Account through SignUp Facade without
        skip_fraud_check
        """
        signup_request = {'skip_fraud_check': None}

        request_dict = self.get_signup_request_dict(
            signup_request=signup_request)

        api_response = self.client.signup_new_trusted_cloud_customer(
            **request_dict)
        self.assertDefaultResponseOK(api_response)

    def test_us_trusted_cloud_signup_request_with_skip_fraud_check_as_false(self):
        """
        Scenario: Create US Trusted Cloud Account through SignUp Facade with
        skip_fraud_check as false
        """
        signup_request = {'skip_fraud_check': False}

        request_dict = self.get_signup_request_dict(
            signup_request=signup_request)

        api_response = self.client.signup_new_trusted_cloud_customer(
            **request_dict)
        self.assertDefaultResponseOK(api_response)

    def test_us_trusted_cloud_signup_request_with_skip_fraud_check_as_true(self):
        """
        Scenario: Create US Trusted Cloud Account through SignUp Facade with
        skip_fraud_check as true
        """
        signup_request = {'skip_fraud_check': True}

        request_dict = self.get_signup_request_dict(
            signup_request=signup_request)

        api_response = self.client.signup_new_trusted_cloud_customer(
            **request_dict)
        self.assertDefaultResponseOK(api_response)

    def test_us_trusted_cloud_signup_request_without_service_level(self):
        """
        Scenario: Create US Trusted Cloud Account through SignUp Facade without
        Service Level
        """
        signup_request = {'service_level': None}

        request_dict = self.get_signup_request_dict(
            signup_request=signup_request)

        api_response = self.client.signup_new_trusted_cloud_customer(
            **request_dict)
        self.assertDefaultResponseOK(api_response)

    def test_us_trusted_cloud_signup_request_with_service_level_as_core(self):
        """
        Scenario: Create US Trusted Cloud Account through SignUp Facade with
        Service Level as CORE
        """
        signup_request = {'service_level': 'CORE'}

        request_dict = self.get_signup_request_dict(
            signup_request=signup_request)

        api_response = self.client.signup_new_trusted_cloud_customer(
            **request_dict)
        self.assertDefaultResponseOK(api_response)

    def test_us_trusted_cloud_signup_request_with_service_level_as_managed(self):
        """
        Scenario: Create US Trusted Cloud Account through SignUp Facade with
        Service Level as MANAGED
        """
        signup_request = {'service_level': 'MANAGED'}

        request_dict = self.get_signup_request_dict(
            signup_request=signup_request)

        api_response = self.client.signup_new_trusted_cloud_customer(
            **request_dict)
        self.assertDefaultResponseOK(api_response)

    def test_us_trusted_cloud_signup_request_without_suffix(self):
        """
        Scenario: Create US Trusted Cloud Account through SignUp Facade without
        Suffix
        """
        default_contact = {'suffix': None}

        request_dict = self.get_signup_request_dict(
            default_contact=default_contact)

        api_response = self.client.signup_new_trusted_cloud_customer(
            **request_dict)
        self.assertDefaultResponseOK(api_response)

    def test_us_trusted_cloud_signup_request_without_title(self):
        """
        Scenario: Create US Trusted Cloud Account through SignUp Facade without
        Title
        """
        default_contact = {'title': None}

        request_dict = self.get_signup_request_dict(
            default_contact=default_contact)

        api_response = self.client.signup_new_trusted_cloud_customer(
            **request_dict)
        self.assertDefaultResponseOK(api_response)

    def test_us_trusted_cloud_signup_request_without_suffix_and_title(self):
        """
        Scenario: Create US Trusted Cloud Account through SignUp Facade without
        Suffix and Title
        """
        default_contact = {'suffix': None, 'title': None}

        request_dict = self.get_signup_request_dict(
            default_contact=default_contact)

        api_response = self.client.signup_new_trusted_cloud_customer(
            **request_dict)
        self.assertDefaultResponseOK(api_response)

    def test_us_trusted_cloud_signup_request_without_referral_code(self):
        """
        Scenario: Create US Trusted Cloud Account through SignUp Facade without
        Referral Code
        """
        signup_request = {'referral_code': None}

        request_dict = self.get_signup_request_dict(
            signup_request=signup_request)

        api_response = self.client.signup_new_cloud_customer(**request_dict)
        self.assertDefaultResponseOK(api_response)

    def test_us_trusted_cloud_signup_request_with_diactrics(self):
        """
        Scenario: Create Account using US trusted Cloud SignUp Facade with
        diactrics and check in get steps
        """
        first = 'ëìíîïðñ'
        last = 'òóôõöøù úûüýþÿ'
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
        signup_id = self.get_marker(api_response)

        # Steps to check whether the diactrics are passed to cybersource system
        api_response1 = (self.client.signup_steps(signup_id)).content
        cs_request = re.search('FRAUD_CHECK COMPLETE(.+?)FRAUD_CHECK',
                               api_response1).group(1)

        self.assertIsNotNone(re.search(first2, cs_request),
                             "first name not found")
        self.assertIsNotNone(re.search(last2, cs_request),
                             "last name not found")

    def test_us_trusted_cloud_signup_request_without_business_type(self):
        """
        Scenario: Create US Trusted Cloud Account through SignUp Facade without
        Business Type
        """
        signup_request = {'business_type': None}

        request_dict = self.get_signup_request_dict(
            signup_request=signup_request)

        api_response = self.client.signup_new_trusted_cloud_customer(
            **request_dict)
        self.assertDefaultResponseOK(api_response)

    def test_us_trusted_cloud_signup_request_with_business_type_as_business(self):
        """
        Scenario: Create US Trusted Cloud Account through SignUp Facade with
        Business Type as BUSINESS
        """
        signup_request = {'business_type': 'BUSINESS'}

        request_dict = self.get_signup_request_dict(
            signup_request=signup_request)

        api_response = self.client.signup_new_trusted_cloud_customer(
            **request_dict)
        self.assertDefaultResponseOK(api_response)

    def test_us_trusted_cloud_signup_request_with_business_type_as_consumer(self):
        """
        Scenario: Create US Trusted Cloud Account through SignUp Facade with
        Business Type as CONSUMER
        """
        signup_request = {'business_type': 'CONSUMER'}

        request_dict = self.get_signup_request_dict(
            signup_request=signup_request)

        api_response = self.client.signup_new_trusted_cloud_customer(
            **request_dict)
        self.assertDefaultResponseOK(api_response)

    def test_us_trusted_cloud_signup_request_without_terms_and_conditions(self):
        """
        Scenario: Create US Trusted Cloud Account through SignUp Facade without
        Terms and Conditions
        """
        signup_request = {'terms_and_conditions': None}

        request_dict = self.get_signup_request_dict(
            signup_request=signup_request)

        api_response = self.client.signup_new_trusted_cloud_customer(
            **request_dict)
        self.assertDefaultResponseOK(api_response)

    def test_us_trusted_cloud_signup_request_with_terms_and_conditions_as_us(self):
        """
        Scenario: Create US Trusted Cloud Account through SignUp Facade with
        Terms and Conditions as US
        """
        signup_request = {'terms_and_conditions': 'US'}

        request_dict = self.get_signup_request_dict(
            signup_request=signup_request)

        api_response = self.client.signup_new_trusted_cloud_customer(
            **request_dict)
        self.assertDefaultResponseOK(api_response)

    def test_us_trusted_cloud_signup_request_with_terms_and_conditions_as_international(self):
        """
        Scenario: Create US Trusted Cloud Account through SignUp Facade with
        Terms and Conditions as INTERNATIONAL
        """
        signup_request = {'terms_and_conditions': 'INTL'}

        request_dict = self.get_signup_request_dict(
            signup_request=signup_request)

        api_response = self.client.signup_new_trusted_cloud_customer(
            **request_dict)
        self.assertDefaultResponseOK(api_response)

    def test_us_trusted_cloud_signup_request_with_appropriate_description(self):
        """
        Scenario: Create US Trusted Cloud Account through SignUp Facade with
        Appropriate Description
        """
        signup_request = {
            'description': 'A Trusted Cloud Signup Request from the Portal '
            'site'}

        request_dict = self.get_signup_request_dict(
            signup_request=signup_request)

        api_response = self.client.signup_new_trusted_cloud_customer(
            **request_dict)
        self.assertDefaultResponseOK(api_response)

    def test_us_trusted_cloud_signup_request_with_amex_credit_card_type(self):
        """
        Scenario: Create US Trusted Cloud Account through SignUp Facade with
        AMEX Credit Card Type
        """
        default_payment_card = {
            'card_number': CreditCards.AMERICANEXPRESS_CARD_NUMBER,
            'card_type': CreditCards.AMERICANEXPRESS_CARD}

        payment_method = {'consolidated_invoice': None}

        request_dict = self.get_signup_request_dict(
            default_payment_card=default_payment_card,
            payment_method=payment_method)

        api_response = self.client.signup_new_trusted_cloud_customer(
            **request_dict)
        self.assertDefaultResponseOK(api_response)

    def test_us_trusted_cloud_signup_request_with_visa_credit_card_type(self):
        """
        Scenario: Create US Trusted Cloud Account through SignUp Facade with
        VISA Credit Card Type
        """
        default_payment_card = {
            'card_number': CreditCards.VISA_CARD_NUMBER,
            'card_type': CreditCards.VISA_CARD}

        payment_method = {'consolidated_invoice': None}

        request_dict = self.get_signup_request_dict(
            default_payment_card=default_payment_card,
            payment_method=payment_method)

        api_response = self.client.signup_new_trusted_cloud_customer(
            **request_dict)
        self.assertDefaultResponseOK(api_response)

    def test_us_trusted_cloud_signup_request_with_master_card_credit_card_type(self):
        """
        Scenario: Create US Trusted Cloud Account through SignUp Facade with
        MASTER CARD Credit Card Type
        """
        default_payment_card = {
            'card_number': CreditCards.MASTER_CARD_NUMBER,
            'card_type': CreditCards.MASTER_CARD}

        payment_method = {'consolidated_invoice': None}

        request_dict = self.get_signup_request_dict(
            default_payment_card=default_payment_card,
            payment_method=payment_method)

        api_response = self.client.signup_new_trusted_cloud_customer(
            **request_dict)
        self.assertDefaultResponseOK(api_response)

    def test_us_trusted_cloud_signup_request_with_discover_credit_card_type(self):
        """
        Scenario: Create US Trusted Cloud Account through SignUp Facade with
        DISCOVER Credit Card Type
        """
        default_payment_card = {
            'card_number': CreditCards.DISCOVER_CARD_NUMBER,
            'card_type': CreditCards.DISCOVER_CARD}

        payment_method = {'consolidated_invoice': None}

        request_dict = self.get_signup_request_dict(
            default_payment_card=default_payment_card,
            payment_method=payment_method)

        api_response = self.client.signup_new_trusted_cloud_customer(
            **request_dict)
        self.assertDefaultResponseOK(api_response)

    def test_us_trusted_cloud_signup_request_without_complete_order_items(self):
        """
        Scenario: Create US Trusted Cloud Account through SignUp Facade without
        Complete Order Items
        """
        order_items = []

        request_dict = self.get_signup_request_dict(order_items=order_items)

        api_response = self.client.signup_new_trusted_cloud_customer(
            **request_dict)
        self.assertDefaultResponseOK(api_response)

    def test_us_trusted_cloud_signup_request_without_description(self):
        """
        Scenario: Create US Trusted Cloud Account through SignUp Facade without
        Description
        """
        signup_request = {'description': ''}

        request_dict = self.get_signup_request_dict(
            signup_request=signup_request)

        api_response = self.client.signup_new_trusted_cloud_customer(
            **request_dict)
        self.assertDefaultResponseOK(api_response)

    def test_us_trusted_cloud_signup_request_without_complete_affiliate_details(self):
        """
        Scenario: Create US Trusted Cloud Account through SignUp Facade without
        Complete Affiliate Details
        """
        affiliate_code_and_type = {}

        request_dict = self.get_signup_request_dict(
            affiliate_code_and_type=affiliate_code_and_type)

        api_response = self.client.signup_new_trusted_cloud_customer(
            **request_dict)
        self.assertDefaultResponseOK(api_response)

    @attr('syd_test')
    def test_us_trusted_cloud_with_us_primary_address_cloud_sites_b2c_for_contract_entity(self):
        """
        Scenario to test us trusted cloud with b2c and us primary address for
        contract entity with cloud sites
        """
        # Defining country_code and business_type
        cloud_type = 'US'
        country_code = 'US'
        business_type = Business_Type.CONSUMER

        default_address = {
            'city': 'San Antonio',
            'country': country_code,
            'primary': True,
            'state': 'Texas',
            'street': '5000 Walzem Road',
            'zipcode': '78214'}
        signup_request = {'business_type': business_type}
        default_order_item = {
            'offering_id': 'CLOUD_SITES',
            'product_id': 'CLOUD_SITES',
            'quantity': '1'}
        request_dict = self.get_signup_request_dict(
            default_address=default_address, signup_request=signup_request,
            default_order_item=default_order_item)
        api_response = self.client.signup_new_trusted_cloud_customer(
            **request_dict)
        self.assertDefaultResponseOK(api_response)

        # To validate the contract entity
        self.validate_contract_entity(api_response=api_response,
                                      country_code=country_code,
                                      cloud_type=cloud_type,
                                      business_type=business_type)

    @attr('syd_test')
    def test_us_trusted_cloud_with_us_primary_address_b2b_for_contract_entity(self):
        """
        Scenario to test us trusted cloud with b2b and us primary address for
        contract entity
        """
        # Defining country_code and business_type
        cloud_type = 'US'
        country_code = 'US'
        business_type = Business_Type.BUSINESS

        default_address = {
            'city': 'San Antonio',
            'country': country_code,
            'primary': True,
            'state': 'Texas',
            'street': '5000 Walzem Road',
            'zipcode': '78214'}
        signup_request = {'business_type': business_type}
        request_dict = self.get_signup_request_dict(
            default_address=default_address, signup_request=signup_request)
        api_response = self.client.signup_new_trusted_cloud_customer(
            **request_dict)
        self.assertDefaultResponseOK(api_response)

        # To validate the contract entity
        self.validate_contract_entity(api_response=api_response,
                                      country_code=country_code,
                                      cloud_type=cloud_type,
                                      business_type=business_type)

    @attr('syd_test')
    def test_us_trusted_cloud_core_with_us_primary_address_b2b_for_contract_entity(self):
        """
        Scenario to test us trusted cloud with b2b and us primary address for
        contract entity and service level as CORE
        """
        # Defining country_code and business_type
        cloud_type = 'US'
        country_code = 'US'
        business_type = Business_Type.BUSINESS

        default_address = {
            'city': 'San Antonio',
            'country': country_code,
            'primary': True,
            'state': 'Texas',
            'street': '5000 Walzem Road',
            'zipcode': '78214'}
        signup_request = {'business_type': business_type,
                          'service_level': 'CORE'}
        request_dict = self.get_signup_request_dict(
            default_address=default_address, signup_request=signup_request)
        api_response = self.client.signup_new_trusted_cloud_customer(
            **request_dict)
        self.assertDefaultResponseOK(api_response)

        # To validate the contract entity
        self.validate_contract_entity(api_response=api_response,
                                      country_code=country_code,
                                      cloud_type=cloud_type,
                                      business_type=business_type)

    @attr('syd_test')
    def test_us_trusted_cloud_with_us_primary_address_wo_business_type_for_contract_entity(self):
        """
        Scenario to test us trusted cloud without business_type and with us
        primary address for contract entity
        """
        # Defining country_code and business_type
        cloud_type = 'US'
        country_code = 'US'

        default_address = {
            'city': 'San Antonio',
            'country': country_code,
            'primary': True,
            'state': 'Texas',
            'street': '5000 Walzem Road',
            'zipcode': '78214'}
        signup_request = {'business_type': None}
        request_dict = self.get_signup_request_dict(
            default_address=default_address, signup_request=signup_request)
        api_response = self.client.signup_new_trusted_cloud_customer(
            **request_dict)
        self.assertDefaultResponseOK(api_response)

        # To validate the contract entity
        self.validate_contract_entity(api_response=api_response,
                                      country_code=country_code,
                                      cloud_type=cloud_type)

    @attr('syd_test')
    def test_us_trusted_cloud_with_au_primary_address_wo_business_type_for_contract_entity(self):
        """
        Scenario to test us trusted cloud without business_type and with au
        primary address for contract entity and terms_and_conditions as INTL
        """
        # Defining country_code and business_type
        cloud_type = 'US'
        country_code = 'AU'

        default_address = {
            'city': 'Sydney',
            'country': country_code,
            'primary': True,
            'state': 'NSW',
            'street': '367 George Street',
            'zipcode': '2000'}
        signup_request = {'business_type': None,
                          'terms_and_conditions': 'INTL'}
        request_dict = self.get_signup_request_dict(
            default_address=default_address, signup_request=signup_request)
        api_response = self.client.signup_new_trusted_cloud_customer(
            **request_dict)
        self.assertDefaultResponseOK(api_response)

        # To validate the contract entity
        self.validate_contract_entity(api_response=api_response,
                                      country_code=country_code,
                                      cloud_type=cloud_type)

    @attr('syd_test')
    def test_us_trusted_cloud_with_au_primary_address_cloud_sites_b2b_type_for_contract_entity(self):
        """
        Scenario to test us trusted cloud with b2b and with au primary
        address for contract entity and with cloud sites
        """
        # Defining country_code and business_type
        cloud_type = 'US'
        country_code = 'AU'
        business_type = Business_Type.BUSINESS

        default_address = {
            'city': 'Sydney',
            'country': country_code,
            'primary': True,
            'state': 'NSW',
            'street': '367 George Street',
            'zipcode': '2000'}
        signup_request = {'business_type': business_type}
        default_order_item = {
            'offering_id': 'CLOUD_SITES',
            'product_id': 'CLOUD_SITES',
            'quantity': '1'}
        default_payment_card = {
            'card_number': CreditCards.MASTER_CARD_NUMBER,
            'card_type': CreditCards.MASTER_CARD}
        request_dict = self.get_signup_request_dict(
            default_address=default_address, signup_request=signup_request,
            default_order_item=default_order_item,
            default_payment_card=default_payment_card)
        api_response = self.client.signup_new_trusted_cloud_customer(
            **request_dict)
        self.assertDefaultResponseOK(api_response)

        # To validate the contract entity
        self.validate_contract_entity(api_response=api_response,
                                      country_code=country_code,
                                      cloud_type=cloud_type,
                                      business_type=business_type)

    @attr('syd_test')
    def test_us_trusted_cloud_with_au_primary_address_b2c_type_for_contract_entity(self):
        """
        Scenario to test us trusted cloud with b2c and with au primary
        address for contract entity
        """
        # Defining country_code and business_type
        cloud_type = 'US'
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

        # To validate the contract entity
        self.validate_contract_entity(api_response=api_response,
                                      country_code=country_code,
                                      cloud_type=cloud_type,
                                      business_type=business_type)

    @attr('syd_test')
    def test_us_trusted_cloud_with_nz_primary_address_b2b_type_for_contract_entity(self):
        """
        Scenario to test us trusted cloud with b2b and with nz primary
        address for contract entity with visa card
        """
        # Defining country_code and business_type
        cloud_type = 'US'
        country_code = 'NZ'
        business_type = Business_Type.BUSINESS

        default_address = {
            'city': 'Wellington',
            'country': country_code,
            'primary': True,
            'state': 'Wellington',
            'street': 'Flat 2, 173 Park Road',
            'zipcode': '6004'}
        signup_request = {'business_type': business_type}
        default_payment_card = {
            'card_number': CreditCards.VISA_CARD_NUMBER,
            'card_type': CreditCards.VISA_CARD}
        request_dict = self.get_signup_request_dict(
            default_address=default_address, signup_request=signup_request,
            default_payment_card=default_payment_card)
        api_response = self.client.signup_new_trusted_cloud_customer(
            **request_dict)
        self.assertDefaultResponseOK(api_response)

        # To validate the contract entity
        self.validate_contract_entity(api_response=api_response,
                                      country_code=country_code,
                                      cloud_type=cloud_type,
                                      business_type=business_type)

    @attr('syd_test')
    def test_us_trusted_cloud_with_nz_primary_address_b2c_type_for_contract_entity(self):
        """
        Scenario to test us trusted cloud with b2c and with nz primary
        address for contract entity
        """
        # Defining country_code and business_type
        cloud_type = 'US'
        country_code = 'AU'
        business_type = Business_Type.CONSUMER

        default_address = {
            'city': 'Wellington',
            'country': country_code,
            'primary': True,
            'state': 'Wellington',
            'street': 'Flat 2, 173 Park Road',
            'zipcode': '6004'}
        signup_request = {'business_type': business_type}
        request_dict = self.get_signup_request_dict(
            default_address=default_address, signup_request=signup_request)
        api_response = self.client.signup_new_trusted_cloud_customer(
            **request_dict)
        self.assertDefaultResponseOK(api_response)

        # To validate the contract entity
        self.validate_contract_entity(api_response=api_response,
                                      country_code=country_code,
                                      cloud_type=cloud_type,
                                      business_type=business_type)

    @attr('syd_test')
    def test_us_trusted_cloud_with_apac_primary_address_b2b_type_for_contract_entity(self):
        """
        Scenario to test us trusted cloud with b2b and with apac primary
        address for contract entity
        """
        # Defining country_code and business_type
        cloud_type = 'US'
        country_code = 'HK'
        business_type = Business_Type.BUSINESS

        default_address = {
            'city': 'Kwai Chung',
            'country': country_code,
            'primary': True,
            'state': 'NEW TERRITORIES',
            'street': 'Flat D, 6/F, Golden Industrial Center, Block 4',
            'zipcode': '852'}
        signup_request = {'business_type': business_type}
        request_dict = self.get_signup_request_dict(
            default_address=default_address, signup_request=signup_request)
        api_response = self.client.signup_new_trusted_cloud_customer(
            **request_dict)
        self.assertDefaultResponseOK(api_response)

        # To validate the contract entity
        self.validate_contract_entity(api_response=api_response,
                                      country_code=country_code,
                                      cloud_type=cloud_type,
                                      business_type=business_type)

    @attr('syd_test')
    def test_us_trusted_cloud_with_apac_primary_address_b2c_type_for_contract_entity(self):
        """
        Scenario to test us trusted cloud with b2c and with apac primary
        address for contract entity
        """
        # Defining country_code and business_type
        cloud_type = 'US'
        country_code = 'HK'
        business_type = Business_Type.CONSUMER

        default_address = {
            'city': 'Kwai Chung',
            'country': country_code,
            'primary': True,
            'state': 'NEW TERRITORIES',
            'street': 'Flat D, 6/F, Golden Industrial Center, Block 4',
            'zipcode': '852'}
        signup_request = {'business_type': business_type}
        request_dict = self.get_signup_request_dict(
            default_address=default_address, signup_request=signup_request)
        api_response = self.client.signup_new_trusted_cloud_customer(
            **request_dict)
        self.assertDefaultResponseOK(api_response)

        # To validate the contract entity
        self.validate_contract_entity(api_response=api_response,
                                      country_code=country_code,
                                      cloud_type=cloud_type,
                                      business_type=business_type)

    @attr('syd_test')
    def test_us_trusted_cloud_with_gb_primary_address_b2b_for_contract_entity(self):
        """
        Scenario to test us trusted cloud with b2b and gb primary address for
        contract entity
        """
        # Defining country_code and business_type
        cloud_type = 'US'
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

        # To validate the contract entity
        self.validate_contract_entity(api_response=api_response,
                                      country_code=country_code,
                                      cloud_type=cloud_type,
                                      business_type=business_type)

    @attr('syd_test')
    def test_us_trusted_cloud_with_gb_primary_address_b2c_for_contract_entity(self):
        """
        Scenario to test us trusted cloud with b2c and gb primary address for
        contract entity
        """
        # Defining country_code and business_type
        cloud_type = 'US'
        country_code = 'GB'
        business_type = Business_Type.CONSUMER

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

        # To validate the contract entity
        self.validate_contract_entity(api_response=api_response,
                                      country_code=country_code,
                                      cloud_type=cloud_type,
                                      business_type=business_type)

    @attr('syd_test')
    def test_wo_payment_card(self):
        """
        Scenario to test us trusted cloud with payment method as
        consolidated invoice
        """
        default_consolidated_invoice = {'managed_account_number': '91282392'}
        payment_method = {'consolidated_invoice': default_consolidated_invoice,
                          'default_payment_card': None}
        request_dict = self.get_signup_request_dict(
            payment_method=payment_method)
        del request_dict['payment_method']['payment_card']
        api_response = self.client.signup_new_trusted_cloud_customer(
            **request_dict)
        self.assertDefaultResponseOK(api_response)

        # To get the signupid
        signup_id = self.get_marker(api_response)

        # Get steps
        steps_response = (self.client.signup_steps(signup_id)).content

        # Checking that contract entity call is not made
        self.assertIsNotNone(re.search('CONTRACT_ENTITY', steps_response))

    @attr('cloud_sites')
    def test_us_trusted_cloud_with_cloud_sites_check_cloud_subscription(self):
        """
        Scenario to test us trusted cloud with cloud sites and check whether
        POST call is made to AtomHopper

        """
        # Defining the order tag
        default_order_item = {
            'offering_id': 'CLOUD_SITES',
            'product_id': 'CLOUD_SITES',
            'quantity': '1'}

        # Defining the metadata property
        metadata = [
            {"key": "cloudSitesPurchased",
             "value": "true"},
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
             "value": "111.000-222"}]

        request_dict = self.get_signup_request_dict(
            default_order_item=default_order_item, metadata=metadata)
        del request_dict['order']['metadata']

        api_response = self.client.signup_new_trusted_cloud_customer(
            **request_dict)
        self.assertDefaultResponseOK(api_response)
        self.validate_atom_hopper_call(api_response=api_response)

    @attr('cloud_sites')
    def test_us_trusted_cloud_with_cloud_sites_and_propery_as_false_check_cloud_subscription(self):
        """
        Scenario to test us trusted cloud with cloud sites purchase but with
        cloudSitesPurchased property as false and check whether
        POST call is made to AtomHopper

        """
        # Defining the order tag
        default_order_item = {
            'offering_id': 'CLOUD_SITES',
            'product_id': 'CLOUD_SITES',
            'quantity': '1'}

        # Defining the metadata property setting false for cloudSitesPurchased
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
             "value": "111.000-222"}]

        request_dict = self.get_signup_request_dict(
            default_order_item=default_order_item, metadata=metadata)
        del request_dict['order']['metadata']

        api_response = self.client.signup_new_trusted_cloud_customer(
            **request_dict)
        self.assertDefaultResponseOK(api_response)
        self.validate_atom_hopper_call(api_response=api_response)

    @attr('cloud_sites')
    def test_us_trusted_cloud_without_cloud_sites_and_propery_as_true_check_cloud_not_subscription(self):
        """
        Scenario to test us trusted cloud without cloud sites purchase but with
        cloudSitesPurchased property as true and check whether
        POST call is not made to AtomHopper and the status of signup is
        COMPLETE

        """

        # Defining the metadata property setting false for cloudSitesPurchased
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
             "value": "111.000-222"}]
        order_items = None

        request_dict = self.get_signup_request_dict(
            metadata=metadata, order_items=order_items)
        #del request_dict['order']['metadata']

        api_response = self.client.signup_new_trusted_cloud_customer(
            **request_dict)
        self.assertDefaultResponseOK(api_response)
        self.validate_atom_hopper_call(api_response=api_response,
                                       sites_purchased=False)

    @attr('geo_location')
    def test_us_trusted_cloud_signup_request_with_geo_location(self):
        """
        Scenario to test us trusted cloud with geo_location as SYD
        """
        signup_request = {'geo_location': "SYD"}
        request_dict = self.get_signup_request_dict(
            signup_request=signup_request)

        # username will be used for the user identity call
        username = request_dict['contacts'][0]['user']['username']
        api_response = self.client.signup_new_trusted_cloud_customer(
            **request_dict)
        self.assertDefaultResponseOK(api_response)

        # identity call validations
        self.validate_user_identity(
            api_response=api_response, username=username)

    @attr('geo_location', 'cloud_sites')
    def test_us_trusted_cloud_signup_with_geo_location_and_cloud_sites(self):
        """
        Scenario to test us trusted cloud signup with geo_location as SYD and
        with Cloud Sites

        """
        # Defining the order tag
        default_order_item = {
            'offering_id': 'CLOUD_SITES',
            'product_id': 'CLOUD_SITES',
            'quantity': '1'}

        # Defining the metadata property setting false for cloudSitesPurchased
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
             "value": "111.000-222"}]
        signup_request = {'geo_location': "SYD"}
        request_dict = self.get_signup_request_dict(
            metadata=metadata, default_order_item=default_order_item,
            signup_request=signup_request)
        del request_dict['order']['metadata']

        # username will be used for the user identity call
        username = request_dict['contacts'][0]['user']['username']
        api_response = self.client.signup_new_trusted_cloud_customer(
            **request_dict)
        self.assertDefaultResponseOK(api_response)

        # identity call validations
        self.validate_user_identity(
            api_response=api_response, username=username)

    @attr('geo_location', 'syd_test')
    def test_us_trusted_cloud_signup_request_with_geo_location_and_contract_as_ch(self):
        """
        Scenario to test us trusted cloud with geo_location as SYD and with 
        primary address AU and business_type BUSINESS

        """
        # Defining country_code and business_type
        cloud_type = 'US'
        country_code = 'AU'
        business_type = Business_Type.BUSINESS

        default_address = {
            'city': 'Wellington',
            'country': country_code,
            'primary': True,
            'state': 'Wellington',
            'street': 'Flat 2, 173 Park Road',
            'zipcode': '6004'}
        signup_request = {'business_type': business_type,
                          'geo_location': "SYD"}
        request_dict = self.get_signup_request_dict(
            default_address=default_address, signup_request=signup_request)
        api_response = self.client.signup_new_trusted_cloud_customer(
            **request_dict)
        self.assertDefaultResponseOK(api_response)

        # To validate the contract entity
        self.validate_contract_entity(api_response=api_response,
                                      country_code=country_code,
                                      cloud_type=cloud_type,
                                      business_type=business_type)
        # username will be used for the user identity call
        username = request_dict['contacts'][0]['user']['username']

        # identity call validations
        self.validate_user_identity(
            api_response=api_response, username=username)

    @attr('default_region')
    def test_us_trusted_cloud_signup_request_with_default_region_and_contract_as_ch(self):
        """
        Scenario to test us cloud with geo_location as SYD and with primary
        address AU and business_type BUSINESS

        """
        # Defining country_code and business_type
        cloud_type = 'US'
        country_code = 'AU'
        business_type = Business_Type.BUSINESS

        default_address = {
            'city': 'Wellington',
            'country': country_code,
            'primary': True,
            'state': 'Wellington',
            'street': 'Flat 2, 173 Park Road',
            'zipcode': '6004'}
        signup_request = {'business_type': business_type,
                          'default_region': "SYD"}
        request_dict = self.get_signup_request_dict(
            default_address=default_address, signup_request=signup_request)
        api_response = self.client.signup_new_trusted_cloud_customer(
            **request_dict)
        self.assertDefaultResponseOK(api_response)

        # To validate the contract entity
        self.validate_contract_entity(api_response=api_response,
                                      country_code=country_code,
                                      cloud_type=cloud_type,
                                      business_type=business_type)
        # username will be used for the user identity call
        username = request_dict['contacts'][0]['user']['username']

        # identity call validations
        self.validate_user_identity(
            api_response=api_response, username=username)

    @attr('geo_location', 'syd_test')
    def test_us_trusted_cloud_signup_with_consolidated_invoice_and_geo_location(self):
        """
        Scenario to test us trusted cloud signup with payment method as
        consolidated invoice and geo_location as SYD

        """
        default_consolidated_invoice = {'managed_account_number': '91282392'}
        payment_method = {'consolidated_invoice': default_consolidated_invoice,
                          'default_payment_card': None}
        signup_request = {'geo_location': 'SYD'}
        request_dict = self.get_signup_request_dict(
            payment_method=payment_method, signup_request=signup_request)
        del request_dict['payment_method']['payment_card']
        api_response = self.client.signup_new_trusted_cloud_customer(
            **request_dict)
        self.assertDefaultResponseOK(api_response)

        # Checking that contract entity call is made
        self.validate_contract_entity(api_response=api_response,
                                      is_consolidated_invoice=True)

        # username will be used for the user identity call
        username = request_dict['contacts'][0]['user']['username']

        # identity call validations
        self.validate_user_identity(
            api_response=api_response, username=username)

    @attr('default_region', 'geography', 'cloud_sites')
    def test_us_trusted_cloud_signup_with_default_region_and_geography_and_cloud_sites(self):
        """
        Scenario to test us cloud signup with geo_location as SYD and
        with Cloud Sites

        """
        # Defining the order tag
        default_order_item = {
            'offering_id': 'CLOUD_SITES',
            'product_id': 'CLOUD_SITES',
            'quantity': '1'}

        # Defining the metadata property setting false for cloudSitesPurchased
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
             "value": "111.000-222"}]
        signup_request = {'default_region': "SYD",
                          'geography': "US",
                          'region': None}
        request_dict = self.get_signup_request_dict(
            metadata=metadata, default_order_item=default_order_item,
            signup_request=signup_request)
        del request_dict['order']['metadata']

        # username will be used for the user identity call
        username = request_dict['contacts'][0]['user']['username']
        api_response = self.client.signup_new_trusted_cloud_customer(
            **request_dict)
        self.assertDefaultResponseOK(api_response)

        # Check cloud sites feed
        self.validate_atom_hopper_call(api_response=api_response)

        # identity call validations
        self.validate_user_identity(
            api_response=api_response, username=username)

    @attr('welcome_email')
    def test_us_trusted_cloud_signup_welcome_email(self):
        """
        Scenario: To test welcome email functionality
        """
        request_dict = self.get_signup_request_dict()
        api_response = self.client.signup_new_trusted_cloud_customer(
            **request_dict)
        self.assertDefaultResponseOK(api_response)
        self.welcome_email_assertions(api_response)

    @attr('welcome_email')
    def test_us_trusted_cloud_signup_with_defaultRegion(self):
        """
        Scenario: to test whether the SYD mail template is sent when
        defaultRegion is SYD
        """
        default_region = 'SYD'
        signup_request = {'geo_location': default_region}
        request_dict = self.get_signup_request_dict(
            signup_request=signup_request)
        api_response = self.client.signup_new_trusted_cloud_customer(
            **request_dict)
        self.assertDefaultResponseOK(api_response)
        self.welcome_email_assertions(api_response,
                                      default_region=default_region)

    @attr('welcome_email')
    def test_us_trusted_cloud_signup_with_service_level_core(self):
        """
        Scenario: to test whether the correct mail template is selected when
        service_level is core
        """
        service_level = 'CORE'
        signup_request = {'service_level': service_level}
        request_dict = self.get_signup_request_dict(
            signup_request=signup_request)
        api_response = self.client.signup_new_trusted_cloud_customer(
            **request_dict)
        self.assertDefaultResponseOK(api_response)
        self.welcome_email_assertions(api_response,
                                      service_level=service_level)
