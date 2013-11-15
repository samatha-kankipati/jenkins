import re
import time
from ccengine.common.decorators import attr
from testrepo.common.testfixtures.rax_signup import \
    RaxSignupAPI_EmailAndAppsSignupFixture
from testrepo.common.testfixtures.rax_signup import CreditCards, Account_Type


class RaxSignupAPI_EmailAndAppsSignupRequest_PositiveSmoke(
        RaxSignupAPI_EmailAndAppsSignupFixture):

    def replace_spaces_with_plus(self, str):
        return str.replace(' ', '\+').replace('?', '\?').replace('@', '%40')

    def domain_value(self, domain="com"):
        now = time.time()
        a = int(now % 100000)
        domain_value = ("ea{0}@reg." + domain).format(a)
        return domain_value

    def method_for_metadata_property_check(
            self, api_response=None, nexus="Business Entity", us_country="US",
            purpose="For Profit", domain=""):
        signup_id = self.get_marker(api_response)
        api_response1 = self.client.signup_steps(signup_id)

        steps_response = api_response1.content
        nexus = self.replace_spaces_with_plus(nexus)
        us_country = self.replace_spaces_with_plus(us_country)
        domain = self.replace_spaces_with_plus(domain)
        purpose = self.replace_spaces_with_plus(purpose)
        # Assertions to check whether the values for the properties are present
        self.assertIsNotNone(re.search("&us_country=" + us_country,
                             steps_response), us_country +
                             " value for us_country not found")
        self.assertIsNotNone(re.search("&nexus=" + nexus,
                             steps_response), nexus +
                             " value for nexus not found")
        self.assertIsNotNone(re.search("&purpose=" + purpose,
                             steps_response), purpose +
                             " value for purpose not found")

        if(len(domain) > 0):
            self.assertIsNotNone(re.search("&domainName=" + domain,
                                 steps_response), domain +
                                 " value for domain not found")

    def check_absence_of_domain_attributes(self, api_response=None):
        signup_id = self.get_marker(api_response)

        signup_steps_response = self.client.signup_steps(signup_id)
        signup_steps_content = signup_steps_response.content
        # Assertions to check whether Domain Attributes are not present in the
        # Get Signup Steps Response for the given SignupID
        self.assertIsNone(re.search("&DNSType", signup_steps_content),
                          "DNSType Value is Found in Email & Apps Order")

        self.assertIsNone(re.search("&domRegPrice", signup_steps_content),
                          "Domain Registration Price Value is Found "
                          "in Email & Apps Order")

        self.assertIsNone(re.search("&noOfYear", signup_steps_content),
                          "Domian Years Value is Found in Email & Apps Order")

        domain_name_count = len(re.findall("&domainName",
                                signup_steps_content))

        # Assertion to check domainName attribute is not present in
        # Email & Apps Order call when SHARE_POINT STORAGE product alone
        # purchased in order
        self.assertNotEquals(domain_name_count, 2,
                             "Domain Name is Found in Email & Apps Order")

    @attr('email', 'us_registration')
    def test_email_and_apps_signup_request_minimal(self):
        """
        Tests base test fixture default request
        """
        request_dict = self.get_signup_request_dict()
        api_response = self.client.signup_new_email_and_apps_customer(
            **request_dict)
        self.assertDefaultResponseOK(api_response)
        self.method_for_metadata_property_check(api_response)

    @attr('email', 'smoke_test')
    def test_email_and_apps_signup_with_b2b(self):
        """
        Tests base test fixture default request
        """
        signup_request = {'business_type': 'CONSUMER'}
        request_dict = self.get_signup_request_dict(
            signup_request=signup_request)

        api_response = self.client.signup_new_email_and_apps_customer(
            **request_dict)
        self.assertDefaultResponseOK(api_response)
        self.method_for_metadata_property_check(api_response)

    @attr('email', 'us_registration', 'smoke_test')
    def test_email_and_apps_signup_request_default(self):
        """
        Scenario: Create Account using SignUp Facade for Email & Apps with all
        necessary details
        """
        order_items = [
            {"offering_id": "RACKSPACE_EMAIL",
             "quantity": 30,
             "product_id": "RACKSPACE_MAILBOX"},
            {"offering_id": "MICROSOFT_EXCHANGE",
             "quantity": 5,
             "product_id": "MICROSOFT_EXCHANGE_MAILBOX"},
            {"offering_id": "MICROSOFT_EXCHANGE",
             "quantity": 1,
             "product_id": "BLACKBERRY_LICENSE"},
            {"offering_id": "MICROSOFT_EXCHANGE",
             "quantity": 20,
             "product_id": "MICROSOFT_EXCHANGE_STORAGE"},
            {"offering_id": "EMAIL_ARCHIVING",
             "quantity": 1,
             "product_id": "EMAIL_ARCHIVING"},
            {"offering_id": "SHAREPOINT",
             "quantity": 30,
             "product_id": "SHAREPOINT_STORAGE"}]

        request_dict = self.get_signup_request_dict(
            order_items=order_items)

        api_response = self.client.signup_new_email_and_apps_customer(
            **request_dict)
        self.assertDefaultResponseOK(api_response)
        self.method_for_metadata_property_check(api_response)

    @attr('email', 'us_registration', 'smoke_test')
    def test_email_and_apps_signup_request_with_domain_us(self):
        """
        Scenario: Create Account using SignUp Facade for Email & Apps with all
        necessary details and with somain as .us
        """
        order_items = [
            {"offering_id": "RACKSPACE_EMAIL",
             "quantity": 30,
             "product_id": "RACKSPACE_MAILBOX"},
            {"offering_id": "MICROSOFT_EXCHANGE",
             "quantity": 5,
             "product_id": "MICROSOFT_EXCHANGE_MAILBOX"},
            {"offering_id": "MICROSOFT_EXCHANGE",
             "quantity": 1,
             "product_id": "BLACKBERRY_LICENSE"},
            {"offering_id": "MICROSOFT_EXCHANGE",
             "quantity": 20,
             "product_id": "MICROSOFT_EXCHANGE_STORAGE"},
            {"offering_id": "EMAIL_ARCHIVING",
             "quantity": 1,
             "product_id": "EMAIL_ARCHIVING"},
            {"offering_id": "SHAREPOINT",
             "quantity": 30,
             "product_id": "SHAREPOINT_STORAGE"}]

        nexus = "C3"
        purpose = "P11"
        us_country = "US"
        domain_value = self.domain_value("us")
        order_metadata = [
            {"key": "domainName",
             "value": domain_value},
            {"key": "domainRegistrationPrice",
             "value": '10'},
            {"key": "domainYears",
             "value": '1'},
            {"key": "dnsType",
             "value": "new"},
            {"key": "nexus",
             "value": nexus},
            {"key": "purpose",
             "value": purpose},
            {"key": "us_country",
             "value": us_country}]

        request_dict = self.get_signup_request_dict(
            order_items=order_items, order_metadata=order_metadata)

        api_response = self.client.signup_new_email_and_apps_customer(
            **request_dict)
        self.assertDefaultResponseOK(api_response)
        self.method_for_metadata_property_check(api_response, nexus=nexus,
                                                purpose=purpose,
                                                us_country=us_country,
                                                domain=domain_value)

    @attr('email', 'us_registration')
    def test_email_and_apps_signup_request_with_domain_us_nexus_null(self):
        """
        Scenario: Create Account using SignUp Facade for Email & Apps with all
        necessary details
        """
        order_items = [
            {"offering_id": "RACKSPACE_EMAIL",
             "quantity": 30,
             "product_id": "RACKSPACE_MAILBOX"},
            {"offering_id": "MICROSOFT_EXCHANGE",
             "quantity": 5,
             "product_id": "MICROSOFT_EXCHANGE_MAILBOX"},
            {"offering_id": "MICROSOFT_EXCHANGE",
             "quantity": 1,
             "product_id": "BLACKBERRY_LICENSE"},
            {"offering_id": "MICROSOFT_EXCHANGE",
             "quantity": 20,
             "product_id": "MICROSOFT_EXCHANGE_STORAGE"},
            {"offering_id": "EMAIL_ARCHIVING",
             "quantity": 1,
             "product_id": "EMAIL_ARCHIVING"},
            {"offering_id": "SHAREPOINT",
             "quantity": 30,
             "product_id": "SHAREPOINT_STORAGE"}]
        domain_value = self.domain_value()
        order_metadata = [
            {"key": "domainName",
             "value": domain_value},
            {"key": "domainRegistrationPrice",
             "value": '10'},
            {"key": "domainYears",
             "value": '1'},
            {"key": "dnsType",
             "value": "new"},
            {"key": "nexus",
             "value": None},
            {"key": "purpose",
             "value": "For Profit"},
            {"key": "us_country",
             "value": "US"}]

        request_dict = self.get_signup_request_dict(
            order_items=order_items, order_metadata=order_metadata)

        api_response = self.client.signup_new_email_and_apps_customer(
            **request_dict)
        self.assertDefaultResponseOK(api_response)

        self.method_for_metadata_property_check(api_response, nexus="",
                                                domain=domain_value)

    def test_email_and_apps_signup_request_with_values_given_in_contract(self):
        """
        Scenario: Test to check with the values given in the contract
        """
        domain_value = self.domain_value("US")
        nexus = "C11"
        purpose = "P3"
        us_country = "US"
        order_metadata = [
            {"key": "domainName",
             "value": domain_value},
            {"key": "domainRegistrationPrice",
             "value": '10'},
            {"key": "domainYears",
             "value": '1'},
            {"key": "dnsType",
             "value": "new"},
            {"key": "nexus",
             "value": nexus},
            {"key": "purpose",
             "value": purpose},
            {"key": "us_country",
             "value": us_country}]
        request_dict = self.get_signup_request_dict(
            order_metadata=order_metadata)

        api_response = self.client.signup_new_email_and_apps_customer(
            **request_dict)
        self.assertDefaultResponseOK(api_response)

        self.method_for_metadata_property_check(api_response, nexus=nexus,
                                                purpose=purpose,
                                                domain=domain_value)

    def test_email_and_apps_signup_request_with_values_dns_type_as_old(self):
        """
        Scenario: Test to check with the values given in the contract
        """
        domain_value = self.domain_value("ca")
        nexus = "C11"
        purpose = "P3"
        us_country = "US"
        order_metadata = [
            {"key": "domainName",
             "value": domain_value},
            {"key": "domainRegistrationPrice",
             "value": '10'},
            {"key": "domainYears",
             "value": '1'},
            {"key": "dnsType",
             "value": "pointtous"},
            {"key": "nexus",
             "value": nexus},
            {"key": "purpose",
             "value": purpose},
            {"key": "us_country",
             "value": us_country}]
        request_dict = self.get_signup_request_dict(
            order_metadata=order_metadata)

        api_response = self.client.signup_new_email_and_apps_customer(
            **request_dict)
        self.assertDefaultResponseOK(api_response)

        self.method_for_metadata_property_check(api_response, nexus=nexus,
                                                purpose=purpose,
                                                domain=domain_value)

    def test_email_and_apps_signup_request_without_business_type(self):
        """
        Scenario: Create Email & Apps Account through SignUp Facade without
        Business Type
        """
        signup_request = {'business_type': None}

        request_dict = self.get_signup_request_dict(
            signup_request=signup_request)

        api_response = self.client.signup_new_email_and_apps_customer(
            **request_dict)
        self.assertDefaultResponseOK(api_response)
        self.method_for_metadata_property_check(api_response)

    def test_email_and_apps_request_with_business_type_as_business(self):
        """
        Scenario: Create Email & Apps Account through SignUp Facade with
        Business Type as BUSINESS
        """
        signup_request = {'business_type': 'BUSINESS'}

        request_dict = self.get_signup_request_dict(
            signup_request=signup_request)

        api_response = self.client.signup_new_email_and_apps_customer(
            **request_dict)
        self.assertDefaultResponseOK(api_response)
        self.method_for_metadata_property_check(api_response)

    def test_email_and_apps_request_with_business_type_as_consumer(self):
        """
        Scenario: Create Email & Apps Account through SignUp Facade with
        Business Type as CONSUMER
        """
        signup_request = {'business_type': 'CONSUMER'}

        request_dict = self.get_signup_request_dict(
            signup_request=signup_request)

        api_response = self.client.signup_new_email_and_apps_customer(
            **request_dict)
        self.assertDefaultResponseOK(api_response)
        self.method_for_metadata_property_check(api_response)

    def test_email_and_apps_signup_request_without_promo_code(self):
        """
        Scenario: Create Email & Apps Account through SignUp Facade without
        Promocode
        """
        signup_request = {'promo_code': None}

        request_dict = self.get_signup_request_dict(
            signup_request=signup_request)

        api_response = self.client.signup_new_email_and_apps_customer(
            **request_dict)
        self.assertDefaultResponseOK(api_response)
        self.method_for_metadata_property_check(api_response)

    def test_email_and_apps_signup_request_without_referral_code(self):
        """
        Scenario: Create Email & Apps Account through SignUp Facade without
        Referral Code
        """
        signup_request = {'referral_code': None}

        request_dict = self.get_signup_request_dict(
            signup_request=signup_request)

        api_response = self.client.signup_new_email_and_apps_customer(
            **request_dict)
        self.assertDefaultResponseOK(api_response)
        self.method_for_metadata_property_check(api_response)

    def test_email_and_apps_signup_request_without_vat_code(self):
        """
        Scenario: Create Email & Apps Account through SignUp Facade without
        Vat Code
        """
        signup_request = {'vat_code': None}

        request_dict = self.get_signup_request_dict(
            signup_request=signup_request)

        api_response = self.client.signup_new_email_and_apps_customer(
            **request_dict)
        self.assertDefaultResponseOK(api_response)
        self.method_for_metadata_property_check(api_response)

    def test_email_and_apps_signup_request_without_service_level(self):
        """
        Scenario: Create Email & Apps Account through SignUp Facade without
        Service Level
        """
        signup_request = {'service_level': None}

        request_dict = self.get_signup_request_dict(
            signup_request=signup_request)

        api_response = self.client.signup_new_email_and_apps_customer(
            **request_dict)
        self.assertDefaultResponseOK(api_response)
        self.method_for_metadata_property_check(api_response)

    def test_email_and_apps_signup_request_without_terms_and_conditions(self):
        """
        Scenario: Create Email & Apps Account through SignUp Facade without
        Terms and Conditions
        """
        signup_request = {'terms_and_conditions': None}

        request_dict = self.get_signup_request_dict(
            signup_request=signup_request)

        api_response = self.client.signup_new_email_and_apps_customer(
            **request_dict)
        self.assertDefaultResponseOK(api_response)
        self.method_for_metadata_property_check(api_response)

    def test_email_and_apps_request_with_terms_and_conditions_as_us(self):
        """
        Scenario: Create Email & Apps Account through SignUp Facade with
        Terms and Conditions as US
        """
        signup_request = {'terms_and_conditions': 'US'}

        request_dict = self.get_signup_request_dict(
            signup_request=signup_request)

        api_response = self.client.signup_new_email_and_apps_customer(
            **request_dict)
        self.assertDefaultResponseOK(api_response)
        self.method_for_metadata_property_check(api_response)

    def test_email_apps_request_with_terms_and_conditions_as_intl(self):
        """
        Scenario: Create Email & Apps Account through SignUp Facade with
        Terms and Conditions as INTERNATIONAL
        """
        signup_request = {'terms_and_conditions': 'INTL'}

        request_dict = self.get_signup_request_dict(
            signup_request=signup_request)

        api_response = self.client.signup_new_email_and_apps_customer(
            **request_dict)
        self.assertDefaultResponseOK(api_response)
        self.method_for_metadata_property_check(api_response)

    def test_email_and_apps_signup_request_without_contact_suffix(self):
        """
        Scenario: Create Email & Apps Account through SignUp Facade without
        Contact Suffix
        """
        default_contact = {'suffix': None}

        request_dict = self.get_signup_request_dict(
            default_contact=default_contact)

        api_response = self.client.signup_new_email_and_apps_customer(
            **request_dict)
        self.assertDefaultResponseOK(api_response)
        self.method_for_metadata_property_check(api_response)

    def test_email_and_apps_signup_request_without_contact_title(self):
        """
        Scenario: Create Email & Apps Account through SignUp Facade without
        Contact Title
        """
        default_contact = {'title': None}

        request_dict = self.get_signup_request_dict(
            default_contact=default_contact)

        api_response = self.client.signup_new_email_and_apps_customer(
            **request_dict)
        self.assertDefaultResponseOK(api_response)
        self.method_for_metadata_property_check(api_response)

    def test_email_and_apps_signup_request_without_metadata(self):
        """
        Scenario: Create Email & Apps Account through SignUp Facade without
        Metadata
        """
        signup_request = {'metadata': None}

        request_dict = self.get_signup_request_dict(
            signup_request=signup_request)

        api_response = self.client.signup_new_email_and_apps_customer(
            **request_dict)
        self.assertDefaultResponseOK(api_response)
        self.method_for_metadata_property_check(api_response)

    def test_email_and_apps_signup_request_without_affiliate_details(self):
        """
        Scenario: Create Email & Apps Account through SignUp Facade without
        Affiliate Details
        """
        signup_request = {'affiliate_code_and_type': None}

        request_dict = self.get_signup_request_dict(
            signup_request=signup_request)

        api_response = self.client.signup_new_email_and_apps_customer(
            **request_dict)
        self.assertDefaultResponseOK(api_response)
        self.method_for_metadata_property_check(api_response)

    def test_email_and_apps_signup_request_with_only_rackspace_mailbox(self):
        """
        Scenario: Create Email & Apps Account through SignUp Facade with only
        Rackspace Mailbox in Order Items
        """
        order_items = [
            {"offering_id": "RACKSPACE_EMAIL",
             "quantity": 10,
             "product_id": "RACKSPACE_MAILBOX"}]

        request_dict = self.get_signup_request_dict(order_items=order_items)

        api_response = self.client.signup_new_email_and_apps_customer(
            **request_dict)
        self.assertDefaultResponseOK(api_response)
        self.method_for_metadata_property_check(api_response)

    def test_email_and_apps_request_with_only_microsoft_exchange_mailbox(self):
        """
        Scenario: Create Email & Apps Account through SignUp Facade with only
        Microsoft Exchange Mailbox in Order Items
        """
        order_items = [
            {"offering_id": "MICROSOFT_EXCHANGE",
             "quantity": 5,
             "product_id": "MICROSOFT_EXCHANGE_MAILBOX"}]

        request_dict = self.get_signup_request_dict(order_items=order_items)

        api_response = self.client.signup_new_email_and_apps_customer(
            **request_dict)
        self.assertDefaultResponseOK(api_response)
        self.method_for_metadata_property_check(api_response)

    def test_email_and_apps_signup_request_with_only_sharepoint_storage(self):
        """
        Scenario: Create Email & Apps Account through SignUp Facade with only
        Sharepoint Storage in Order Items
        """
        order_items = [
            {"offering_id": "SHAREPOINT",
             "quantity": 10,
             "product_id": "SHAREPOINT_STORAGE"}]

        request_dict = self.get_signup_request_dict(order_items=order_items)

        api_response = self.client.signup_new_email_and_apps_customer(
            **request_dict)
        self.assertDefaultResponseOK(api_response)
        self.method_for_metadata_property_check(api_response)

    def test_email_and_apps_request_with_rackspace_mailbox_and_archiving(self):
        """
        Scenario: Create Email & Apps Account through SignUp Facade with
        Rackspace Mailbox and Email Archiving in Order Items
        """
        order_items = [
            {"offering_id": "RACKSPACE_EMAIL",
             "quantity": 10,
             "product_id": "RACKSPACE_MAILBOX"},
            {"offering_id": "EMAIL_ARCHIVING",
             "quantity": 1,
             "product_id": "EMAIL_ARCHIVING"}]

        request_dict = self.get_signup_request_dict(order_items=order_items)

        api_response = self.client.signup_new_email_and_apps_customer(
            **request_dict)
        self.assertDefaultResponseOK(api_response)
        self.method_for_metadata_property_check(api_response)

    def test_email_apps_request_with_ms_exchange_mailbox_and_archiving(self):
        """
        Scenario: Create Email & Apps Account through SignUp Facade with
        Microsoft Exchange Mailbox and Email Archiving in Order Items
        """
        order_items = [
            {"offering_id": "MICROSOFT_EXCHANGE",
             "quantity": 5,
             "product_id": "MICROSOFT_EXCHANGE_MAILBOX"},
            {"offering_id": "EMAIL_ARCHIVING",
             "quantity": 1,
             "product_id": "EMAIL_ARCHIVING"}]

        request_dict = self.get_signup_request_dict(order_items=order_items)

        api_response = self.client.signup_new_email_and_apps_customer(
            **request_dict)
        self.assertDefaultResponseOK(api_response)
        self.method_for_metadata_property_check(api_response)

    def test_email_apps_request_with_ms_exchange_mailbox_and_blackberry(self):
        """
        Scenario: Create Email & Apps Account through SignUp Facade with
        Microsoft Exchange Mailbox and Blackberry License in Order Items
        """
        order_items = [
            {"offering_id": "MICROSOFT_EXCHANGE",
             "quantity": 5,
             "product_id": "MICROSOFT_EXCHANGE_MAILBOX"},
            {"offering_id": "MICROSOFT_EXCHANGE",
             "quantity": 1,
             "product_id": "BLACKBERRY_LICENSE"}]

        request_dict = self.get_signup_request_dict(order_items=order_items)

        api_response = self.client.signup_new_email_and_apps_customer(
            **request_dict)
        self.assertDefaultResponseOK(api_response)
        self.method_for_metadata_property_check(api_response)

    def test_email_apps_request_with_ms_exchange_mailbox_and_ms_storage(self):
        """
        Scenario: Create Email & Apps Account through SignUp Facade with
        Microsoft Exchange Mailbox and Microsoft Exchange Storage in
        Order Items
        """
        order_items = [
            {"offering_id": "MICROSOFT_EXCHANGE",
             "quantity": 5,
             "product_id": "MICROSOFT_EXCHANGE_MAILBOX"},
            {"offering_id": "MICROSOFT_EXCHANGE",
             "quantity": 20,
             "product_id": "MICROSOFT_EXCHANGE_STORAGE"}]

        request_dict = self.get_signup_request_dict(order_items=order_items)

        api_response = self.client.signup_new_email_and_apps_customer(
            **request_dict)
        self.assertDefaultResponseOK(api_response)
        self.method_for_metadata_property_check(api_response)

    def test_email_and_apps_signup_request_with_all_microsoft_products(self):
        """
        Scenario: Create Email & Apps Account through SignUp Facade with
        all Microsoft Products in Order Items
        """
        order_items = [
            {"offering_id": "MICROSOFT_EXCHANGE",
             "quantity": 5,
             "product_id": "MICROSOFT_EXCHANGE_MAILBOX"},
            {"offering_id": "MICROSOFT_EXCHANGE",
             "quantity": 1,
             "product_id": "BLACKBERRY_LICENSE"},
            {"offering_id": "MICROSOFT_EXCHANGE",
             "quantity": 20,
             "product_id": "MICROSOFT_EXCHANGE_STORAGE"}]

        request_dict = self.get_signup_request_dict(order_items=order_items)

        api_response = self.client.signup_new_email_and_apps_customer(
            **request_dict)
        self.assertDefaultResponseOK(api_response)
        self.method_for_metadata_property_check(api_response)

    def test_email_apps_request_with_all_mailboxes_and_email_archiving(self):
        """
        Scenario: Create Email & Apps Account through SignUp Facade with
        all Mailboxes and Email Archiving in Order Items
        """
        order_items = [
            {"offering_id": "RACKSPACE_EMAIL",
             "quantity": 10,
             "product_id": "RACKSPACE_MAILBOX"},
            {"offering_id": "MICROSOFT_EXCHANGE",
             "quantity": 5,
             "product_id": "MICROSOFT_EXCHANGE_MAILBOX"},
            {"offering_id": "EMAIL_ARCHIVING",
             "quantity": 1,
             "product_id": "EMAIL_ARCHIVING"}]

        request_dict = self.get_signup_request_dict(order_items=order_items)

        api_response = self.client.signup_new_email_and_apps_customer(
            **request_dict)
        self.assertDefaultResponseOK(api_response)
        self.method_for_metadata_property_check(api_response)

    def test_email_and_apps_signup_request_with_amex_credit_card_type(self):
        """
        Scenario: Create Email & Apps Account through SignUp Facade with
        AMEX Credit Card Type
        """
        default_payment_card = {
            'card_number': CreditCards.AMERICANEXPRESS_CARD_NUMBER,
            'card_type': CreditCards.AMERICANEXPRESS_CARD}

        request_dict = self.get_signup_request_dict(
            default_payment_card=default_payment_card)

        api_response = self.client.signup_new_email_and_apps_customer(
            **request_dict)
        self.assertDefaultResponseOK(api_response)
        self.method_for_metadata_property_check(api_response)

    def test_email_and_apps_signup_request_with_visa_credit_card_type(self):
        """
        Scenario: Create Email & Apps Account through SignUp Facade with
        VISA Credit Card Type
        """
        default_payment_card = {
            'card_number': CreditCards.VISA_CARD_NUMBER,
            'card_type': CreditCards.VISA_CARD}

        request_dict = self.get_signup_request_dict(
            default_payment_card=default_payment_card)

        api_response = self.client.signup_new_email_and_apps_customer(
            **request_dict)
        self.assertDefaultResponseOK(api_response)
        self.method_for_metadata_property_check(api_response)

    def test_email_apps_signup_request_with_master_card_credit_card_type(self):
        """
        Scenario: Create Email & Apps Account through SignUp Facade with
        MASTER CARD Credit Card Type
        """
        default_payment_card = {
            'card_number': CreditCards.MASTER_CARD_NUMBER,
            'card_type': CreditCards.MASTER_CARD}

        request_dict = self.get_signup_request_dict(
            default_payment_card=default_payment_card)

        api_response = self.client.signup_new_email_and_apps_customer(
            **request_dict)
        self.assertDefaultResponseOK(api_response)
        self.method_for_metadata_property_check(api_response)

    def test_email_apps_signup_request_with_discover_credit_card_type(self):
        """
        Scenario: Create Email & Apps Account through SignUp Facade with
        DISCOVER Credit Card Type
        """
        default_payment_card = {
            'card_number': CreditCards.DISCOVER_CARD_NUMBER,
            'card_type': CreditCards.DISCOVER_CARD}

        request_dict = self.get_signup_request_dict(
            default_payment_card=default_payment_card)

        api_response = self.client.signup_new_email_and_apps_customer(
            **request_dict)
        self.assertDefaultResponseOK(api_response)
        self.method_for_metadata_property_check(api_response)

    @attr('sharepoint_storage')
    def test_email_apps_request_sharepoint_with_all_domain_attributes(self):
        """
        Scenario: Create Email & Apps Account using SignUp Service with only
        SHAREPOINT_STORAGE in order along with domain attributes
        """
        order_items = [
            {"offering_id": "SHAREPOINT",
             "quantity": 30,
             "product_id": "SHAREPOINT_STORAGE"}]

        domain_value = self.domain_value()
        order_metadata = [
            {"key": "domainName",
             "value": domain_value},
            {"key": "domainRegistrationPrice",
             "value": '10'},
            {"key": "domainYears",
             "value": '1'},
            {"key": "dnsType",
             "value": "new"}]

        request_dict = self.get_signup_request_dict(
            order_items=order_items, order_metadata=order_metadata)
        account_type = Account_Type.Email_Apps

        api_response = self.signup_post_calls(request_dict, account_type)
        self.assertDefaultResponseOK(api_response)
        self.check_absence_of_domain_attributes(api_response)

    @attr('sharepoint_storage')
    def test_email_apps_request_sharepoint_without_all_domain_attributes(self):
        """
        Scenario: Create Email & Apps Account using SignUp Service with only
        SHAREPOINT_STORAGE in order without entire domain attributes
        """
        order_items = [
            {"offering_id": "SHAREPOINT",
             "quantity": 30,
             "product_id": "SHAREPOINT_STORAGE"}]
        order_metadata = []

        request_dict = self.get_signup_request_dict(
            order_items=order_items, order_metadata=order_metadata)
        account_type = Account_Type.Email_Apps

        api_response = self.signup_post_calls(request_dict, account_type)
        self.assertDefaultResponseOK(api_response)
        self.check_absence_of_domain_attributes(api_response)

    @attr('sharepoint_storage')
    def test_email_apps_request_sharepoint_with_empty_domain_name(self):
        """
        Scenario: Create Email & Apps Account using SignUp Service with only
        SHAREPOINT_STORAGE in order with empty value for domainName attribute
        """
        order_items = [
            {"offering_id": "SHAREPOINT",
             "quantity": 30,
             "product_id": "SHAREPOINT_STORAGE"}]

        order_metadata = [
            {"key": "domainName",
             "value": ""},
            {"key": "domainRegistrationPrice",
             "value": '10'},
            {"key": "domainYears",
             "value": '1'},
            {"key": "dnsType",
             "value": "new"}]

        request_dict = self.get_signup_request_dict(
            order_items=order_items, order_metadata=order_metadata)
        account_type = Account_Type.Email_Apps

        api_response = self.signup_post_calls(request_dict, account_type)
        self.assertDefaultResponseOK(api_response)
        self.check_absence_of_domain_attributes(api_response)

    @attr('sharepoint_storage')
    def test_email_apps_request_sharepoint_with_empty_domain_price(self):
        """
        Scenario: Create Email & Apps Account using SignUp Service with only
        SHAREPOINT_STORAGE in order with empty value for
        domainRegistrationPrice attribute
        """
        order_items = [
            {"offering_id": "SHAREPOINT",
             "quantity": 30,
             "product_id": "SHAREPOINT_STORAGE"}]

        domain_value = self.domain_value()
        order_metadata = [
            {"key": "domainName",
             "value": domain_value},
            {"key": "domainRegistrationPrice",
             "value": ""},
            {"key": "domainYears",
             "value": '1'},
            {"key": "dnsType",
             "value": "new"}]

        request_dict = self.get_signup_request_dict(
            order_items=order_items, order_metadata=order_metadata)
        account_type = Account_Type.Email_Apps

        api_response = self.signup_post_calls(request_dict, account_type)
        self.assertDefaultResponseOK(api_response)
        self.check_absence_of_domain_attributes(api_response)

    @attr('sharepoint_storage')
    def test_email_apps_request_sharepoint_with_empty_domain_years(self):
        """
        Scenario: Create Email & Apps Account using SignUp Service with only
        SHAREPOINT_STORAGE in order with empty value for domainYears attribute
        """
        order_items = [
            {"offering_id": "SHAREPOINT",
             "quantity": 30,
             "product_id": "SHAREPOINT_STORAGE"}]

        domain_value = self.domain_value()
        order_metadata = [
            {"key": "domainName",
             "value": domain_value},
            {"key": "domainRegistrationPrice",
             "value": "10"},
            {"key": "domainYears",
             "value": ""},
            {"key": "dnsType",
             "value": "new"}]

        request_dict = self.get_signup_request_dict(
            order_items=order_items, order_metadata=order_metadata)
        account_type = Account_Type.Email_Apps

        api_response = self.signup_post_calls(request_dict, account_type)
        self.assertDefaultResponseOK(api_response)
        self.check_absence_of_domain_attributes(api_response)

    @attr('sharepoint_storage')
    def test_email_apps_request_sharepoint_without_dns_type(self):
        """
        Scenario: Create Email & Apps Account using SignUp Service with only
        SHAREPOINT_STORAGE in order without complete dnsType attribute
        """
        order_items = [
            {"offering_id": "SHAREPOINT",
             "quantity": 30,
             "product_id": "SHAREPOINT_STORAGE"}]

        domain_value = self.domain_value()
        order_metadata = [
            {"key": "domainName",
             "value": domain_value},
            {"key": "domainRegistrationPrice",
             "value": "10"},
            {"key": "domainYears",
             "value": "1"}]

        request_dict = self.get_signup_request_dict(
            order_items=order_items, order_metadata=order_metadata)
        account_type = Account_Type.Email_Apps

        api_response = self.signup_post_calls(request_dict, account_type)
        self.assertDefaultResponseOK(api_response)
        self.check_absence_of_domain_attributes(api_response)

    @attr('sharepoint_storage')
    def test_email_apps_request_sharepoint_without_domain_years(self):
        """
        Scenario: Create Email & Apps Account using SignUp Service with only
        SHAREPOINT_STORAGE in order without complete domainYears attribute
        """
        order_items = [
            {"offering_id": "SHAREPOINT",
             "quantity": 30,
             "product_id": "SHAREPOINT_STORAGE"}]

        domain_value = self.domain_value()
        order_metadata = [
            {"key": "domainName",
             "value": domain_value},
            {"key": "domainRegistrationPrice",
             "value": "10"},
            {"key": "dnsType",
             "value": "new"}]

        request_dict = self.get_signup_request_dict(
            order_items=order_items, order_metadata=order_metadata)
        account_type = Account_Type.Email_Apps

        api_response = self.signup_post_calls(request_dict, account_type)
        self.assertDefaultResponseOK(api_response)
        self.check_absence_of_domain_attributes(api_response)

    @attr('sharepoint_storage')
    def test_email_apps_request_sharepoint_without_domain_price(self):
        """
        Scenario: Create Email & Apps Account using SignUp Service with only
        SHAREPOINT_STORAGE in order without complete domainRegistrationPrice
        attribute
        """
        order_items = [
            {"offering_id": "SHAREPOINT",
             "quantity": 30,
             "product_id": "SHAREPOINT_STORAGE"}]

        domain_value = self.domain_value()
        order_metadata = [
            {"key": "domainName",
             "value": domain_value},
            {"key": "domainYears",
             "value": "1"},
            {"key": "dnsType",
             "value": "new"}]

        request_dict = self.get_signup_request_dict(
            order_items=order_items, order_metadata=order_metadata)
        account_type = Account_Type.Email_Apps

        api_response = self.signup_post_calls(request_dict, account_type)
        self.assertDefaultResponseOK(api_response)
        self.check_absence_of_domain_attributes(api_response)

    @attr('sharepoint_storage')
    def test_email_apps_request_sharepoint_without_domain_name(self):
        """
        Scenario: Create Email & Apps Account using SignUp Service with only
        SHAREPOINT_STORAGE in order without complete domainName attribute
        """
        order_items = [
            {"offering_id": "SHAREPOINT",
             "quantity": 30,
             "product_id": "SHAREPOINT_STORAGE"}]

        order_metadata = [
            {"key": "domainRegistrationPrice",
             "value": ""},
            {"key": "domainYears",
             "value": '1'},
            {"key": "dnsType",
             "value": "new"}]

        request_dict = self.get_signup_request_dict(
            order_items=order_items, order_metadata=order_metadata)
        account_type = Account_Type.Email_Apps

        api_response = self.signup_post_calls(request_dict, account_type)
        self.assertDefaultResponseOK(api_response)
        self.check_absence_of_domain_attributes(api_response)
