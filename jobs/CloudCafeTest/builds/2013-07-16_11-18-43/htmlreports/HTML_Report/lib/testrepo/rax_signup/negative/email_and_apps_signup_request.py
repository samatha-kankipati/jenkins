import re
import time
from ccengine.common.decorators import attr
from testrepo.common.testfixtures.rax_signup import \
    RaxSignupAPI_EmailAndAppsSignupFixture


class RaxSignupAPI_EmailAndAppsSignupRequest_NegativeSmoke(
        RaxSignupAPI_EmailAndAppsSignupFixture):

    assert_msg = "Test expected the string - '{0}' in the response body,"\
        " but not found"

    def test_email_and_apps_signup_request_without_region(self):
        """
        Scenario: Create Email & Apps Account through SignUp Facade without
        Region
        """
        order_items = [{"offering_id": "RACKSPACE_EMAIL",
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

        signup_request = {'region': None}
        request_dict = self.get_signup_request_dict(
            order_items=order_items, signup_request=signup_request)

        api_response = self.client.signup_new_email_and_apps_customer(
            **request_dict)
        expected_status_code = 400
        self.assertEqual(api_response.status_code, expected_status_code,
                         'Returned a {0} but expected {1}'.format(
                         api_response.status_code, expected_status_code))

        #We may not want to include checks for the failure messages, since
        #they could be different between xml and json.  BUT, if you
        #want to, this would be a good way to do it so that it works for both
        #types of responses.
        failure_string = "Region value missing on request! Only Region -- "\
                         "US and UK is supported!"
        self.assertIsNotNone(re.search(failure_string, api_response.content),
                             self.assert_msg.format(failure_string))

    def test_email_and_apps_signup_request_without_account_name(self):
        """
        Scenario: Create Email & Apps Account through SignUp Facade without
        Account Name
        """
        signup_request = {'account_name': None}
        request_dict = self.get_signup_request_dict(
            signup_request=signup_request)

        api_response = self.client.signup_new_email_and_apps_customer(
            **request_dict)
        expected_status_code = 400
        self.assertEqual(api_response.status_code, expected_status_code,
                         'Returned a {0} but expected {1}'.format(
                         api_response.status_code, expected_status_code))

        failure_string = "Account Name missing on request!"
        self.assertIsNotNone(re.search(failure_string, api_response.content),
                             '{0} not found'.format(failure_string))

    def test_email_and_apps_signup_request_invalid_accept_terms_and_conditions(self):
        """
        Scenario: Create Email & Apps Account through SignUp Facade with
        Invalid terms and conditions
        """
        signup_request = {'accept_terms_and_conditions': 'FAKE'}
        request_dict = self.get_signup_request_dict(
            signup_request=signup_request)

        api_response = self.client.signup_new_email_and_apps_customer(
            **request_dict)
        expected_status_code = 400
        self.assertEqual(api_response.status_code, expected_status_code,
                         'Returned a {0} but expected {1}'.format(
                         api_response.status_code, expected_status_code))

        failure_string = "Can not construct instance of boolean from String"
        self.assertIsNotNone(re.search(failure_string, api_response.content),
                             '{0} not found'.format(failure_string))

    # Not Implemented Until After Sydney Datacenter Is Up
    #def test_email_and_apps_signup_request_without_business_type(self):
    #    """
    #    Scenario: Create Account using SignUp Facade for Email and Apps
    #    without account type
    #    """
    #    signup_request = {'business_type': None}
    #    request_dict = self.get_signup_request_dict(
    #            signup_request=signup_request)
    #    api_response = self.client.signup_new_email_and_apps_customer(
    #        **request_dict)
    #    expected_status_code = 201
    #    self.assertEqual(api_response.status_code, expected_status_code,
    #            'Returned a {0} but expected {1}'.format(
    #            api_response.status_code,
    #            expected_status_code))

    def test_email_and_apps_signup_request_without_payment_details_complete(self):
        """
        Scenario: Create Email & Apps account through SignUp Facade without
        providing Complete Payment Details
        """
        payment_method = {}
        request_dict = self.get_signup_request_dict(
            payment_method=payment_method)

        api_response = self.client.signup_new_email_and_apps_customer(
            **request_dict)
        expected_status_code = 400
        self.assertEqual(api_response.status_code, expected_status_code,
                         'Returned a {0} but expected {1}'.format(
                         api_response.status_code, expected_status_code))

        failure_string = "Payment card details missing!"
        self.assertIsNotNone(re.search(failure_string, api_response.content),
                             self.assert_msg.format(failure_string))

    def test_email_and_apps_signup_request_without_any_payment_details(self):
        """
        Scenario: Create Email & Apps Account through SignUp Facade without
        providing Any Payment Details
        """
        default_payment_card = {'card_holder_name': None,
                                'card_number': None,
                                'card_type': None,
                                'card_verification_number': None,
                                'expiration_date': None}
        request_dict = self.get_signup_request_dict(
            default_payment_card=default_payment_card)

        api_response = self.client.signup_new_email_and_apps_customer(
            **request_dict)
        expected_status_code = 400
        self.assertEqual(api_response.status_code, expected_status_code,
                         'Returned a {0} but expected {1}'.format(
                         api_response.status_code, expected_status_code))

        failure_string = "Payment card mandatory details missing!"\
                         "CardHolderName, Number, ExpirationDate, "\
                         "Verification number and card type is mandatory."
        self.assertIsNotNone(re.search(failure_string, api_response.content),
                             self.assert_msg.format(failure_string))

    def test_email_and_apps_signup_request_without_payment_details_card_number(self):
        """
        Scenario: Create Email & Apps Account through SignUp Facade without
        Card Number
        """
        default_payment_card = {'card_number': None}
        request_dict = self.get_signup_request_dict(
            default_payment_card=default_payment_card)

        api_response = self.client.signup_new_email_and_apps_customer(
            **request_dict)
        expected_status_code = 400
        self.assertEqual(api_response.status_code, expected_status_code,
                         'Returned a {0} but expected {1}'.format(
                         api_response.status_code, expected_status_code))

        failure_string = "Payment card mandatory details missing!"\
                         "CardHolderName, Number, ExpirationDate, "\
                         "Verification number and card type is mandatory."
        self.assertIsNotNone(re.search(failure_string, api_response.content),
                             self.assert_msg.format(failure_string))

    def test_email_and_apps_signup_request_without_card_holder_name(self):
        """
        Scenario: Create Email & Apps Account through SignUp Facade without
        Card Holder Name
        """
        default_payment_card = {'card_holder_name': None}
        request_dict = self.get_signup_request_dict(
            default_payment_card=default_payment_card)

        api_response = self.client.signup_new_email_and_apps_customer(
            **request_dict)
        expected_status_code = 400
        self.assertEqual(api_response.status_code, expected_status_code,
                         'Returned a {0} but expected {1}'.format(
                         api_response.status_code, expected_status_code))

        failure_string = "Payment card mandatory details missing!"\
                         "CardHolderName, Number, ExpirationDate, "\
                         "Verification number and card type is mandatory."
        self.assertIsNotNone(re.search(failure_string, api_response.content),
                             self.assert_msg.format(failure_string))

    def test_email_and_apps_signup_request_without_expiration_date(self):
        """
        Scenario: Create Email & Apps Account through SignUp Facade without
        Card Expration Date
        """
        default_payment_card = {'expiration_date': None}
        request_dict = self.get_signup_request_dict(
            default_payment_card=default_payment_card)

        api_response = self.client.signup_new_email_and_apps_customer(
            **request_dict)
        expected_status_code = 400
        self.assertEqual(api_response.status_code, expected_status_code,
                         'Returned a {0} but expected {1}'.format(
                         api_response.status_code, expected_status_code))

        failure_string = "Payment card mandatory details missing!"\
                         "CardHolderName, Number, ExpirationDate, "\
                         "Verification number and card type is mandatory."
        self.assertIsNotNone(re.search(failure_string, api_response.content),
                             self.assert_msg.format(failure_string))

    def test_email_and_apps_signup_request_without_payment_details_card_type(self):
        """
        Scenario: Create Email & Apps Account through SignUp Facade without
        Card Type
        """
        default_payment_card = {'card_type': None}
        request_dict = self.get_signup_request_dict(
            default_payment_card=default_payment_card)

        api_response = self.client.signup_new_email_and_apps_customer(
            **request_dict)
        expected_status_code = 400
        self.assertEqual(api_response.status_code, expected_status_code,
                         'Returned a {0} but expected {1}'.format(
                         api_response.status_code, expected_status_code))

        failure_string = "Pls. provide card type.  Supported Card types are"\
                         " VISA, MASTERCARD, AMEX, DISCOVER"
        self.assertIsNotNone(re.search(failure_string, api_response.content),
                             self.assert_msg.format(failure_string))

    def test_email_and_apps_signup_request_without_card_vrfn_number(self):
        """
        Scenario: Create Email & Apps Account using SignUp Facade without
        Card Verification Number
        """
        default_payment_card = {'card_verification_number': None}
        request_dict = self.get_signup_request_dict(
            default_payment_card=default_payment_card)

        api_response = self.client.signup_new_email_and_apps_customer(
            **request_dict)
        expected_status_code = 400
        self.assertEqual(api_response.status_code, expected_status_code,
                         'Returned a {0} but expected {1}'.format(
                         api_response.status_code, expected_status_code))

        failure_string = "Payment card mandatory details missing!"\
                         "CardHolderName, Number, ExpirationDate, "\
                         "Verification number and card type is mandatory."
        self.assertIsNotNone(re.search(failure_string, api_response.content),
                             self.assert_msg.format(failure_string))

    def test_email_and_apps_signup_request_with_invalid_payment_details(self):
        """
        Scenario: Create Email & Apps Account through SignUp Facade by
        providing Invalid Card Payment Details - Card Number and Type Mismatch
        """
        #DETAILS IN RESPONSE EXPLAINS ABOUT TYPE MISMATCH
        default_payment_card = {'card_number': '378282246310005',
                                'card_type': 'VISA'}
        request_dict = self.get_signup_request_dict(
            default_payment_card=default_payment_card)

        api_response = self.client.signup_new_email_and_apps_customer(
            **request_dict)
        expected_status_code = 400
        self.assertEqual(api_response.status_code, expected_status_code,
                         'Returned a {0} but expected {1}'.format(
                         api_response.status_code, expected_status_code))

        failure_string = "validation errors"
        self.assertIsNotNone(re.search(failure_string, api_response.content),
                             self.assert_msg.format(failure_string))

    def test_email_and_apps_signup_request_with_no_expiration_date(self):
        """
        Scenario: Create Email & Apps Account through SignUp Facade with
        No Value for Expiration Date
        """
        default_payment_card = {'expiration_date': ''}
        request_dict = self.get_signup_request_dict(
            default_payment_card=default_payment_card)

        api_response = self.client.signup_new_email_and_apps_customer(
            **request_dict)
        expected_status_code = 400
        self.assertEqual(api_response.status_code, expected_status_code,
                         'Returned a {0} but expected {1}'.format(
                         api_response.status_code, expected_status_code))

        failure_string = "Payment card mandatory details missing!"\
                         "CardHolderName, Number, ExpirationDate, "\
                         "Verification number and card type is mandatory."
        self.assertIsNotNone(re.search(failure_string, api_response.content),
                             self.assert_msg.format(failure_string))

    def test_email_and_apps_signup_request_with_incorrect_exp_date(self):
        """
        Scenario: Create Email & Apps Account through SignUp Facade with
        Incorrect Expiry date given (Past Year Expiry Date)
        """
        #print "\n\n <<<DETAILS IN RESPONSE GIVES DETAILS ABOUT DATE"
        default_payment_card = {'expiration_date': '02/2013'}
        request_dict = self.get_signup_request_dict(
            default_payment_card=default_payment_card)

        api_response = self.client.signup_new_email_and_apps_customer(
            **request_dict)
        expected_status_code = 400
        self.assertEqual(api_response.status_code, expected_status_code,
                         'Returned a {0} but expected {1}'.format(
                         api_response.status_code, expected_status_code))

        failure_string = "validation errors"
        self.assertIsNotNone(re.search(failure_string, api_response.content),
                             self.assert_msg.format(failure_string))

    def test_email_and_apps_signup_request_with_unformatted_exp_date(self):
        """
        Scenario: Create Email & Apps Account through SignUp Facade with
        Alphabets given in Expiry Date
        """
        #DETAILS IN RESPONSE GIVES DETAILS ABOUT DATE
        default_payment_card = {'expiration_date': '02/2k14'}
        request_dict = self.get_signup_request_dict(
            default_payment_card=default_payment_card)

        api_response = self.client.signup_new_email_and_apps_customer(
            **request_dict)
        expected_status_code = 400
        self.assertEqual(api_response.status_code, expected_status_code,
                         'Returned a {0} but expected {1}'.format(
                         api_response.status_code, expected_status_code))

        failure_string = "Payment Expiration not in proper format"
        self.assertIsNotNone(re.search(failure_string, api_response.content),
                             self.assert_msg.format(failure_string))

    def test_email_and_apps_signup_request_with_no_card_number(self):
        """
        Scenario: Create Email & Apps Account through SignUp Facade with
        No value for Card Number
        """
        default_payment_card = {'card_number': ''}
        request_dict = self.get_signup_request_dict(
            default_payment_card=default_payment_card)

        api_response = self.client.signup_new_email_and_apps_customer(
            **request_dict)
        expected_status_code = 400
        self.assertEqual(api_response.status_code, expected_status_code,
                         'Returned a {0} but expected {1}'.format(
                         api_response.status_code, expected_status_code))

        failure_string = "Payment card mandatory details missing!"\
                         "CardHolderName, Number, ExpirationDate, "\
                         "Verification number and card type is mandatory."
        self.assertIsNotNone(re.search(failure_string, api_response.content),
                             self.assert_msg.format(failure_string))

    def test_email_and_apps_signup_request_with_unformatted_card_number(self):
        """
        Scenario: Create Email & Apps Account through SignUp Facade for with
        Invalid value for Card Number - with Alphabets
        """
        default_payment_card = {'card_number': 'INVALID123'}
        request_dict = self.get_signup_request_dict(
            default_payment_card=default_payment_card)

        api_response = self.client.signup_new_email_and_apps_customer(
            **request_dict)
        expected_status_code = 400
        self.assertEqual(api_response.status_code, expected_status_code,
                         'Returned a {0} but expected {1}'.format(
                         api_response.status_code, expected_status_code))

        failure_string = "Payment card number not in proper format"
        self.assertIsNotNone(re.search(failure_string, api_response.content),
                             self.assert_msg.format(failure_string))

    def test_email_and_apps_signup_request_with_invalid_card_number(self):
        """
        Scenario: Create Email & Apps Account through SignUp Facade with
        Invalid value for Card Number
        """
        default_payment_card = {'card_number': '1234567890123456'}
        request_dict = self.get_signup_request_dict(
            default_payment_card=default_payment_card)

        api_response = self.client.signup_new_email_and_apps_customer(
            **request_dict)
        expected_status_code = 400
        self.assertEqual(api_response.status_code, expected_status_code,
                         'Returned a {0} but expected {1}'.format(
                         api_response.status_code, expected_status_code))

        failure_string = "validation errors"
        self.assertIsNotNone(re.search(failure_string, api_response.content),
                             self.assert_msg.format(failure_string))

    def test_email_and_apps_signup_request_with_no_card_type(self):
        """
        Scenario: Create Email & Apps Account through SignUp Facade without
        Card Type
        """
        default_payment_card = {'card_type': ''}
        request_dict = self.get_signup_request_dict(
            default_payment_card=default_payment_card)

        api_response = self.client.signup_new_email_and_apps_customer(
            **request_dict)
        expected_status_code = 400
        self.assertEqual(api_response.status_code, expected_status_code,
                         'Returned a {0} but expected {1}'.format(
                         api_response.status_code, expected_status_code))

        failure_string = "Pls. provide card type.  Supported Card types are"\
                         " VISA, MASTERCARD, AMEX, DISCOVER"
        self.assertIsNotNone(re.search(failure_string, api_response.content),
                             self.assert_msg.format(failure_string))

    def test_email_and_apps_signup_request_with_invalid_card_type(self):
        """
        Scenario: Create Email & Apps Account through SignUp Facade with
        Invalid value for Card Type
        """
        #DETAILS IN RESPONSE GIVES INFO ABOUT THE METHOD
        default_payment_card = {'card_type': 'FAKE'}
        request_dict = self.get_signup_request_dict(
            default_payment_card=default_payment_card)

        api_response = self.client.signup_new_email_and_apps_customer(
            **request_dict)
        expected_status_code = 400
        self.assertEqual(api_response.status_code, expected_status_code,
                         'Returned a {0} but expected {1}'.format(
                         api_response.status_code, expected_status_code))

        failure_string = "PaymentCardType"
        self.assertIsNotNone(re.search(failure_string, api_response.content),
                             self.assert_msg.format(failure_string))

    def test_email_and_apps_signup_request_with_lower_case_card_type(self):
        """
        Scenario: Create Email & Apps Account through SignUp Facade with
        Value of Card Type in Lowercase
        """
        #DETAILS IN RESPONSE GIVES INFO ABOUT THE METHOD
        default_payment_card = {'card_type': 'visa'}
        request_dict = self.get_signup_request_dict(
            default_payment_card=default_payment_card)

        api_response = self.client.signup_new_email_and_apps_customer(
            **request_dict)
        expected_status_code = 400
        self.assertEqual(api_response.status_code, expected_status_code,
                         'Returned a {0} but expected {1}'.format(
                         api_response.status_code, expected_status_code))

        failure_string = "PaymentCardType"
        self.assertIsNotNone(re.search(failure_string, api_response.content),
                             self.assert_msg.format(failure_string))

    def test_email_and_apps_signup_request_with_no_card_verification_number(self):
        """
        Scenario: Create Email & Apps Account through SignUp Facade with
        Empty Value in Card Verification Number
        """
        default_payment_card = {'card_verification_number': ''}
        request_dict = self.get_signup_request_dict(
            default_payment_card=default_payment_card)

        api_response = self.client.signup_new_email_and_apps_customer(
            **request_dict)
        expected_status_code = 400
        self.assertEqual(api_response.status_code, expected_status_code,
                         'Returned a {0} but expected {1}'.format(
                         api_response.status_code, expected_status_code))

        failure_string = "Payment card mandatory details missing!"\
                         "CardHolderName, Number, ExpirationDate, "\
                         "Verification number and card type is mandatory."
        self.assertIsNotNone(re.search(failure_string, api_response.content),
                             self.assert_msg.format(failure_string))

    def test_email_and_apps_signup_request_with_invalid_card_vrfn_number(self):
        """
        Scenario: Create Email & Apps Account through SignUp Facade with
        Invalid Card Verification Number
        """
        default_payment_card = {'card_verification_number': '12324'}
        request_dict = self.get_signup_request_dict(
            default_payment_card=default_payment_card)

        api_response = self.client.signup_new_email_and_apps_customer(
            **request_dict)
        expected_status_code = 400
        self.assertEqual(api_response.status_code, expected_status_code,
                         'Returned a {0} but expected {1}'.format(
                         api_response.status_code, expected_status_code))

        #Payment Card Verification Number Length Exceeded.
        #Max Length should be 4
        failure_string = "Payment Card Verification Number Length Exceeded.+"\
                         " Max Length should be 4"
        #The error message displayed is "Payment Card Verification Number
        #Length Exceeded. Max Length should be 4" '+' is added for
        #regex search
        self.assertIsNotNone(re.search(failure_string, api_response.content),
                             self.assert_msg.format(failure_string))

    def test_email_and_apps_signup_request_without_complete_contact_roles(self):
        """
        Scenario: Create Email & Apps Account using SignUp Facade without
        Complete Contact Roles
        """
        default_contact = {'roles': None}
        request_dict = self.get_signup_request_dict(
            default_contact=default_contact)

        api_response = self.client.signup_new_email_and_apps_customer(
            **request_dict)
        expected_status_code = 400
        self.assertEqual(api_response.status_code, expected_status_code,
                         'Returned a {0} but expected {1}'.format(
                         api_response.status_code, expected_status_code))

        failure_string = "Contact Role is missing!"
        self.assertIsNotNone(re.search(failure_string, api_response.content),
                             self.assert_msg.format(failure_string))

    def test_email_and_apps_signup_request_without_contact_primary_role(self):
        """
        Scenario: Create Email & Apps Account using SignUp Facade without
        Contact Primary Role
        """
        roles = [{'role': 'BILLING'},
                 {'role': None}]
        request_dict = self.get_signup_request_dict(roles=roles)

        api_response = self.client.signup_new_email_and_apps_customer(
            **request_dict)
        expected_status_code = 400
        self.assertEqual(api_response.status_code, expected_status_code,
                         'Returned a {0} but expected {1}'.format(
                         api_response.status_code, expected_status_code))

        failure_string = "PRIMARY -- Contact details not found!"
        self.assertIsNotNone(re.search(failure_string, api_response.content),
                             self.assert_msg.format(failure_string))

    def test_email_and_apps_signup_request_without_contact_billing_role(self):
        """
        Scenario: Create Email & Apps Account using SignUp Facade without
        Contact Billing Role
        """
        roles = [{'role': None},
                 {'role': 'Primary'}]
        request_dict = self.get_signup_request_dict(roles=roles)

        api_response = self.client.signup_new_email_and_apps_customer(
            **request_dict)
        expected_status_code = 400
        self.assertEqual(api_response.status_code, expected_status_code,
                         'Returned a {0} but expected {1}'.format(
                         api_response.status_code, expected_status_code))

    def test_email_and_apps_signup_request_without_both_contact_roles(self):
        """
        Scenario: Create Email & Apps Account using SignUp Facade without
        both Contact Roles
        """
        roles = [{'role': None},
                 {'role': None}]
        request_dict = self.get_signup_request_dict(roles=roles)

        api_response = self.client.signup_new_email_and_apps_customer(
            **request_dict)
        expected_status_code = 400
        self.assertEqual(api_response.status_code, expected_status_code,
                         'Returned a {0} but expected {1}'.format(
                         api_response.status_code, expected_status_code))

        failure_string = "PRIMARY -- Contact details not found!"
        self.assertIsNotNone(re.search(failure_string, api_response.content),
                             self.assert_msg.format(failure_string))

    def test_email_and_apps_signup_request_without_contact_first_name(self):
        """
        Scenario: Create Email & Apps Account using SignUp Facade without
        Contact First Name
        """
        default_contact = {'first_name': None}
        request_dict = self.get_signup_request_dict(
            default_contact=default_contact)

        api_response = self.client.signup_new_email_and_apps_customer(
            **request_dict)
        expected_status_code = 400
        self.assertEqual(api_response.status_code, expected_status_code,
                         'Returned a {0} but expected {1}'.format(
                         api_response.status_code, expected_status_code))

        failure_string = "Contact Name is missing!"
        self.assertIsNotNone(re.search(failure_string, api_response.content),
                             self.assert_msg.format(failure_string))

    def test_email_and_apps_signup_request_without_contact_last_name(self):
        """
        Scenario: Create Email & Apps Account using SignUp Facade without
        Contact First Name
        """
        default_contact = {'last_name': None}
        request_dict = self.get_signup_request_dict(
            default_contact=default_contact)

        api_response = self.client.signup_new_email_and_apps_customer(
            **request_dict)
        expected_status_code = 400
        self.assertEqual(api_response.status_code, expected_status_code,
                         'Returned a {0} but expected {1}'.format(
                         api_response.status_code, expected_status_code))

        failure_string = "Contact Name is missing!"
        self.assertIsNotNone(re.search(failure_string, api_response.content),
                             self.assert_msg.format(failure_string))

    def test_email_and_apps_signup_request_without_contact_username(self):
        """
        Scenario: Create Email & Apps Account using SignUp Facade without
        Contact User Name
        """
        user = {'username': None}
        request_dict = self.get_signup_request_dict(user=user)

        api_response = self.client.signup_new_email_and_apps_customer(
            **request_dict)
        expected_status_code = 400
        self.assertEqual(api_response.status_code, expected_status_code,
                         'Returned a {0} but expected {1}'.format(
                         api_response.status_code, expected_status_code))

        failure_string = "User name missing on request!"
        self.assertIsNotNone(re.search(failure_string, api_response.content),
                             self.assert_msg.format(failure_string))

    def test_email_and_apps_signup_request_without_contact_password(self):
        """
        Scenario: Create Email & Apps Account using SignUp Facade without
        Contact Password
        """
        user = {'password': None}
        request_dict = self.get_signup_request_dict(user=user)

        api_response = self.client.signup_new_email_and_apps_customer(
            **request_dict)
        expected_status_code = 400
        self.assertEqual(api_response.status_code, expected_status_code,
                         'Returned a {0} but expected {1}'.format(
                         api_response.status_code, expected_status_code))

        failure_string = "User - Password missing on request!"
        self.assertIsNotNone(re.search(failure_string, api_response.content),
                             self.assert_msg.format(failure_string))

    def test_email_and_apps_signup_request_without_secret_question(self):
        """
        Scenario: Create Email & Apps Account using SignUp Facade without
        Secret Question
        """
        secret_qa = {'question': None}
        request_dict = self.get_signup_request_dict(secret_qa=secret_qa)

        api_response = self.client.signup_new_email_and_apps_customer(
            **request_dict)
        expected_status_code = 400
        self.assertEqual(api_response.status_code, expected_status_code,
                         'Returned a {0} but expected {1}'.format(
                         api_response.status_code, expected_status_code))

        failure_string = "Secret Q/A shouldn't be empty!"
        self.assertIsNotNone(re.search(failure_string, api_response.content),
                             self.assert_msg.format(failure_string))

    def test_email_and_apps_signup_request_without_secret_answer(self):
        """
        Scenario: Create Email & Apps Account using SignUp Facade without
        Secret Answer
        """
        secret_qa = {'answer': None}
        request_dict = self.get_signup_request_dict(secret_qa=secret_qa)

        api_response = self.client.signup_new_email_and_apps_customer(
            **request_dict)
        expected_status_code = 400
        self.assertEqual(api_response.status_code, expected_status_code,
                         'Returned a {0} but expected {1}'.format(
                         api_response.status_code, expected_status_code))

        failure_string = "Secret Q/A shouldn't be empty!"
        self.assertIsNotNone(re.search(failure_string, api_response.content),
                             self.assert_msg.format(failure_string))

    def test_email_and_apps_signup_request_without_contact_address_country(self):
        """
        Scenario: Create Email & Apps Account using SignUp Facade without
        Contact Address Country
        """
        default_address = {'country': None}
        request_dict = self.get_signup_request_dict(
            default_address=default_address)

        api_response = self.client.signup_new_email_and_apps_customer(
            **request_dict)
        expected_status_code = 400
        self.assertEqual(api_response.status_code, expected_status_code,
                         'Returned a {0} but expected {1}'.format(
                         api_response.status_code, expected_status_code))

        failure_string = "Address - Country shouldn't be empty"
        self.assertIsNotNone(re.search(failure_string, api_response.content),
                             self.assert_msg.format(failure_string))

    def test_email_and_apps_signup_request_without_contact_address_primary(self):
        """
        Scenario: Create Email & Apps Account using SignUp Facade without
        Contact Address Primary
        """
        default_address = {'primary': None}
        request_dict = self.get_signup_request_dict(
            default_address=default_address)

        api_response = self.client.signup_new_email_and_apps_customer(
            **request_dict)
        expected_status_code = 400
        self.assertEqual(api_response.status_code, expected_status_code,
                         'Returned a {0} but expected {1}'.format(
                         api_response.status_code, expected_status_code))

        failure_string = "Contact -- Primary address not found"
        self.assertIsNotNone(re.search(failure_string, api_response.content),
                             self.assert_msg.format(failure_string))

    def test_email_and_apps_signup_request_without_contact_address_street(self):
        """
        Scenario: Create Email & Apps Account using SignUp Facade without
        Contact Address Street
        """
        default_address = {'street': None}
        request_dict = self.get_signup_request_dict(
            default_address=default_address)

        api_response = self.client.signup_new_email_and_apps_customer(
            **request_dict)
        expected_status_code = 400
        self.assertEqual(api_response.status_code, expected_status_code,
                         'Returned a {0} but expected {1}'.format(
                         api_response.status_code, expected_status_code))

        failure_string = "Address - Street shouldn't be empty"
        self.assertIsNotNone(re.search(failure_string, api_response.content),
                             self.assert_msg.format(failure_string))

    def test_email_and_apps_signup_request_without_contact_email_address(self):
        """
        Scenario: Create Email & Apps Account using SignUp Facade without
        Contact Email Address
        """
        default_email_address = {'address': None}
        request_dict = self.get_signup_request_dict(
            default_email_address=default_email_address)

        api_response = self.client.signup_new_email_and_apps_customer(
            **request_dict)
        expected_status_code = 400
        self.assertEqual(api_response.status_code, expected_status_code,
                         'Returned a {0} but expected {1}'.format(
                         api_response.status_code, expected_status_code))

        failure_string = "Contact Email Address shouldn't be empty"
        self.assertIsNotNone(re.search(failure_string, api_response.content),
                             self.assert_msg.format(failure_string))

    def test_email_and_apps_signup_request_without_contact_email_address_primary(self):
        """
        Scenario: Create Email & Apps Account using SignUp Facade without
        Contact Email Address Primary
        """
        default_email_address = {'primary': None}
        request_dict = self.get_signup_request_dict(
            default_email_address=default_email_address)

        api_response = self.client.signup_new_email_and_apps_customer(
            **request_dict)
        expected_status_code = 400
        self.assertEqual(api_response.status_code, expected_status_code,
                         'Returned a {0} but expected {1}'.format(
                         api_response.status_code, expected_status_code))

        failure_string = "Contact -- Primary Email address not found"
        self.assertIsNotNone(re.search(failure_string, api_response.content),
                             self.assert_msg.format(failure_string))

    def test_email_and_apps_signup_request_with_invalid_contact_email_address(self):
        """
        Scenario: Create Email & Apps Account using SignUp Facade with Invalid
        Contact Email Address
        """
        default_email_address = {'address': 'testmail.com'}
        request_dict = self.get_signup_request_dict(
            default_email_address=default_email_address)

        api_response = self.client.signup_new_email_and_apps_customer(
            **request_dict)
        expected_status_code = 400
        self.assertEqual(api_response.status_code, expected_status_code,
                         'Returned a {0} but expected {1}'.format(
                         api_response.status_code, expected_status_code))

        failure_string = "Contact Email Address not in proper format"
        self.assertIsNotNone(re.search(failure_string, api_response.content),
                             self.assert_msg.format(failure_string))

    def test_email_and_apps_signup_request_without_contact_phone_number(self):
        """
        Scenario: Create Email & Apps Account using SignUp Facade without
        Contact Phone Number
        """
        default_phone_number = {'number': None}
        request_dict = self.get_signup_request_dict(
            default_phone_number=default_phone_number)

        api_response = self.client.signup_new_email_and_apps_customer(
            **request_dict)
        expected_status_code = 400
        self.assertEqual(api_response.status_code, expected_status_code,
                         'Returned a {0} but expected {1}'.format(
                         api_response.status_code, expected_status_code))

        failure_string = "Contact -- Phone number is empty!"
        self.assertIsNotNone(re.search(failure_string, api_response.content),
                             self.assert_msg.format(failure_string))

    def test_email_and_apps_signup_request_without_contact_phone_number_country(self):
        """
        Scenario: Create Email & Apps Account using SignUp Facade without
        Contact Phone Number Country
        """
        default_phone_number = {'country': None}
        request_dict = self.get_signup_request_dict(
            default_phone_number=default_phone_number)

        api_response = self.client.signup_new_email_and_apps_customer(
            **request_dict)
        expected_status_code = 400
        self.assertEqual(api_response.status_code, expected_status_code,
                         'Returned a {0} but expected {1}'.format(
                         api_response.status_code, expected_status_code))

        failure_string = "Contact -- Phone Country code is empty!"
        self.assertIsNotNone(re.search(failure_string, api_response.content),
                             self.assert_msg.format(failure_string))

    def test_email_and_apps_signup_request_without_contact_phone_number_primary(self):
        """
        Scenario: Create Email & Apps Account using SignUp Facade without
        Contact Phone Number Primary
        """
        default_phone_number = {'primary': None}
        request_dict = self.get_signup_request_dict(
            default_phone_number=default_phone_number)

        api_response = self.client.signup_new_email_and_apps_customer(
            **request_dict)
        expected_status_code = 400
        self.assertEqual(api_response.status_code, expected_status_code,
                         'Returned a {0} but expected {1}'.format(
                         api_response.status_code, expected_status_code))

        failure_string = "Contact -- Primary phone number not found"
        self.assertIsNotNone(re.search(failure_string, api_response.content),
                             self.assert_msg.format(failure_string))

    @attr('failing', '201')
    def test_email_and_apps_signup_request_without_contact_phone_number_category(self):
        """
        Scenario: Create Email & Apps Account using SignUp Facade without
        Contact Phone Number Primary
        """
        default_phone_number = {'category': None}
        request_dict = self.get_signup_request_dict(
            default_phone_number=default_phone_number)

        api_response = self.client.signup_new_email_and_apps_customer(
            **request_dict)
        expected_status_code = 400
        self.assertEqual(api_response.status_code, expected_status_code,
                         'Returned a {0} but expected {1}'.format(
                         api_response.status_code, expected_status_code))

        failure_string = "Contact -- Primary phone number not found"
        self.assertIsNotNone(re.search(failure_string, api_response.content),
                             self.assert_msg.format(failure_string))

    def test_email_and_apps_signup_request_without_complete_contact_details(self):
        """
        Scenario: Create Email & Apps Account using SignUp Facade with Complete
        Contact Details
        """
        signup_request = {'contacts': None}
        request_dict = self.get_signup_request_dict(
            signup_request=signup_request)

        api_response = self.client.signup_new_email_and_apps_customer(
            **request_dict)
        expected_status_code = 400
        self.assertEqual(api_response.status_code, expected_status_code,
                         'Returned a {0} but expected {1}'.format(
                         api_response.status_code, expected_status_code))

        failure_string = "Contacts shouldn't be empty"
        self.assertIsNotNone(re.search(failure_string, api_response.content),
                             self.assert_msg.format(failure_string))

    def test_email_and_apps_signup_request_without_complete_contact_address_details(self):
        """
        Scenario: Create Email & Apps Account using SignUp Facade with Complete
        Contact Address Details
        """
        default_contact = {'addresses': None}
        request_dict = self.get_signup_request_dict(
            default_contact=default_contact)

        api_response = self.client.signup_new_email_and_apps_customer(
            **request_dict)
        expected_status_code = 400
        self.assertEqual(api_response.status_code, expected_status_code,
                         'Returned a {0} but expected {1}'.format(
                         api_response.status_code, expected_status_code))

        failure_string = "Contact Address details missing!"
        self.assertIsNotNone(re.search(failure_string, api_response.content),
                             self.assert_msg.format(failure_string))

    def test_email_and_apps_signup_request_without_complete_contact_email_address_details(self):
        """
        Scenario: Create Email & Apps Account using SignUp Facade with Complete
        Contact Email Address Details
        """
        default_contact = {'email_addresses': None}
        request_dict = self.get_signup_request_dict(
            default_contact=default_contact)

        api_response = self.client.signup_new_email_and_apps_customer(
            **request_dict)
        expected_status_code = 400
        self.assertEqual(api_response.status_code, expected_status_code,
                         'Returned a {0} but expected {1}'.format(
                         api_response.status_code, expected_status_code))

        failure_string = "Contact Email Address is missing!"
        self.assertIsNotNone(re.search(failure_string, api_response.content),
                             self.assert_msg.format(failure_string))

    def test_email_and_apps_signup_request_without_complete_contact_phone_number_details(self):
        """
        Scenario: Create Email & Apps Account using SignUp Facade with Complete
        Contact Phone Number Details
        """
        default_contact = {'phone_numbers': None}
        request_dict = self.get_signup_request_dict(
            default_contact=default_contact)

        api_response = self.client.signup_new_email_and_apps_customer(
            **request_dict)
        expected_status_code = 400
        self.assertEqual(api_response.status_code, expected_status_code,
                         'Returned a {0} but expected {1}'.format(
                         api_response.status_code, expected_status_code))

        failure_string = "Contact Phone detail is missing!"
        self.assertIsNotNone(re.search(failure_string, api_response.content),
                             self.assert_msg.format(failure_string))

    def test_email_and_apps_signup_request_without_complete_contact_user_details(self):
        """
        Scenario: Create Email & Apps Account using SignUp Facade with Complete
        Contact User Details
        """
        default_contact = {'user': None}
        request_dict = self.get_signup_request_dict(
            default_contact=default_contact)

        api_response = self.client.signup_new_email_and_apps_customer(
            **request_dict)
        expected_status_code = 400
        self.assertEqual(api_response.status_code, expected_status_code,
                         'Returned a {0} but expected {1}'.format(
                         api_response.status_code, expected_status_code))

        failure_string = "Secret Q/A shouldn't be empty!"
        self.assertIsNotNone(re.search(failure_string, api_response.content),
                             self.assert_msg.format(failure_string))

    def test_email_and_apps_signup_request_without_complete_order_details(self):
        """
        Scenario: Create Email & Apps Account using SignUp Facade with Complete
        Contact Order Details
        """
        signup_request = {'order': None}
        request_dict = self.get_signup_request_dict(
            signup_request=signup_request)

        api_response = self.client.signup_new_email_and_apps_customer(
            **request_dict)
        expected_status_code = 400
        self.assertEqual(api_response.status_code, expected_status_code,
                         'Returned a {0} but expected {1}'.format(
                         api_response.status_code, expected_status_code))

        failure_string = "dnsType,domainRegistrationPrice,domainYears "\
                         "should not be empty."
        self.assertIsNotNone(re.search(failure_string, api_response.content),
                             self.assert_msg.format(failure_string))
