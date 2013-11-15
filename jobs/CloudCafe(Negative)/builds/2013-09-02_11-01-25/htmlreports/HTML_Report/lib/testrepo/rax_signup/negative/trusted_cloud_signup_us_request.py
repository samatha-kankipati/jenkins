import re
from ccengine.common.decorators import attr
from testrepo.common.testfixtures.rax_signup import\
    RaxSignupAPI_TrustedCloudSignupFixture, CreditCards


class RaxSignupAPI_TrustedCloudSignupRequest_NegativeSmoke(
        RaxSignupAPI_TrustedCloudSignupFixture):

    us_trusted_signup = RaxSignupAPI_TrustedCloudSignupFixture
    account_type = "TRUSTED_CLOUD"

    assert_msg = "Test expected the string - '{0}' in the response body,"\
        " but not found"

    mandatory_details = "Payment card mandatory details missing!"\
        "CardHolderName, Number, ExpirationDate, Verification number"\
        " and card type is mandatory."

    def test_us_trusted_cloud_signup_without_region(self):
        """
        Scenario: Create US Trusted Cloud Account through SignUp Facade
        without Region
        """
        signup_request = {'region': None}
        request_dict = self.get_signup_request_dict(
            signup_request=signup_request)

        api_response = self.client.signup_new_trusted_cloud_customer(
            **request_dict)
        expected_status_code = 400
        self.assertEqual(api_response.status_code, expected_status_code,
                         'Returned a {0} but expected {1}'.format(
                         api_response.status_code, expected_status_code))

    def test_us_trusted_cloud_signup_without_account_name(self):
        """
        Scenario: Create US Trusted Cloud Account through SignUp Facade
        without Account Name
        """
        signup_request = {'account_name': None}
        request_dict = self.get_signup_request_dict(
            signup_request=signup_request)

        api_response = self.client.signup_new_trusted_cloud_customer(
            **request_dict)
        expected_status_code = 400
        self.assertEqual(api_response.status_code, expected_status_code,
                         'Returned a {0} but expected {1}'.format(
                         api_response.status_code, expected_status_code))

    def test_us_trusted_cloud_signup_without_accept_terms_and_conditions(self):
        """
        Scenario: Create US Trusted Cloud Account through SignUp Facade
        without Accept Terms and Conditions
        """
        signup_request = {'accept_terms_and_conditions': None}
        request_dict = self.get_signup_request_dict(
            signup_request=signup_request)

        api_response = self.client.signup_new_trusted_cloud_customer(
            **request_dict)
        expected_status_code = 400
        self.assertEqual(api_response.status_code, expected_status_code,
                         'Returned a {0} but expected {1}'.format(
                         api_response.status_code, expected_status_code))

    def test_us_trusted_cloud_signup_with_existing_username_details(self):
        """
        Scenario: Create US Trusted Cloud Account through SignUp Facade
        with Existing Username Details
        """
        request_dict = self.get_signup_request_dict()
        api_response = self.client.signup_new_trusted_cloud_customer(
            **request_dict)

        #Make initial request
        self.assertDefaultResponseOK(api_response)

        #Make second request with same user info
        username = api_response.request.entity.contacts[0].user.username

        #Begin negative test case
        user = {'username': username}

        api_response = self.client.signup_new_trusted_cloud_customer(
            **request_dict)
        expected_status_code = 400
        self.assertEqual(api_response.status_code, expected_status_code,
                         'Returned a {0} but expected {1}'.format(
                         api_response.status_code, expected_status_code))

    def test_us_trusted_cloud_signup_without_username(self):
        """
        Scenario: Create US Trusted Cloud Account through SignUp Facade
        without Username
        """
        user = {'username': None}
        request_dict = self.get_signup_request_dict(user=user)

        api_response = self.client.signup_new_trusted_cloud_customer(
            **request_dict)
        expected_status_code = 400
        self.assertEqual(api_response.status_code, expected_status_code,
                         'Returned a {0} but expected {1}'.format(
                         api_response.status_code, expected_status_code))

    def test_us_trusted_cloud_signup_without_password(self):
        """
        Scenario: Create US Trusted Cloud Account through SignUp Facade
        without Password
        """
        user = {'password': None}
        request_dict = self.get_signup_request_dict(user=user)

        api_response = self.client.signup_new_trusted_cloud_customer(
            **request_dict)
        expected_status_code = 400
        self.assertEqual(api_response.status_code, expected_status_code,
                         'Returned a {0} but expected {1}'.format(
                         api_response.status_code, expected_status_code))

    def test_us_trusted_cloud_signup_without_secret_question(self):
        """
        Scenario: Create US Trusted Cloud Account through SignUp Facade
        without Secret Question
        """
        secret_qa = {'question': None}
        request_dict = self.get_signup_request_dict(secret_qa=secret_qa)

        api_response = self.client.signup_new_trusted_cloud_customer(
            **request_dict)
        expected_status_code = 400
        self.assertEqual(api_response.status_code, expected_status_code,
                         'Returned a {0} but expected {1}'.format(
                         api_response.status_code, expected_status_code))

    def test_us_trusted_cloud_signup_without_secret_answer(self):
        """
        Scenario: Create US Trusted Cloud Account through SignUp Facade
        without Secret Answer
        """
        secret_qa = {'answer': None}
        request_dict = self.get_signup_request_dict(secret_qa=secret_qa)

        api_response = self.client.signup_new_trusted_cloud_customer(
            **request_dict)
        expected_status_code = 400
        self.assertEqual(api_response.status_code, expected_status_code,
                         'Returned a {0} but expected {1}'.format(
                         api_response.status_code, expected_status_code))

    def test_us_trusted_cloud_signup_without_complete_contact_details(self):
        """
        Scenario: Create US Trusted Cloud Account through SignUp Facade
        without Complete Contact Details
        """
        default_contact = {'first_name': None,
                           'last_name': None,
                           'suffix': None,
                           'title': None}
        request_dict = self.get_signup_request_dict(
            default_contact=default_contact)

        api_response = self.client.signup_new_trusted_cloud_customer(
            **request_dict)
        expected_status_code = 400
        self.assertEqual(api_response.status_code, expected_status_code,
                         'Returned a {0} but expected {1}'.format(
                         api_response.status_code, expected_status_code))

    def test_us_trusted_cloud_signup_with_missing_contact_address_details(self):
        """
        Scenario: Create US Trusted Cloud Account through SignUp Facade
        without Complete Contact Address Details
        """
        default_contact = {'addresses': None}
        request_dict = self.get_signup_request_dict(
            default_contact=default_contact)

        api_response = self.client.signup_new_trusted_cloud_customer(
            **request_dict)
        expected_status_code = 400
        self.assertEqual(api_response.status_code, expected_status_code,
                         'Returned a {0} but expected {1}'.format(
                         api_response.status_code, expected_status_code))

    def test_us_trusted_cloud_signup_with_missing_contact_email_address(self):
        """
        Scenario: Create US Trusted Cloud Account through SignUp Facade
        without Contact Email Address
        """
        default_contact = {'email_addresses': None}
        request_dict = self.get_signup_request_dict(
            default_contact=default_contact)

        api_response = self.client.signup_new_trusted_cloud_customer(
            **request_dict)
        expected_status_code = 400
        self.assertEqual(api_response.status_code, expected_status_code,
                         'Returned a {0} but expected {1}'.format(
                         api_response.status_code, expected_status_code))

    def test_us_trusted_cloud_signup_with_missing_contact_phone_number(self):
        """
        Scenario: Create US Trusted Cloud Account through SignUp Facade
        with missing Contact Phone Number
        """
        default_contact = {'phone_numbers': None}
        request_dict = self.get_signup_request_dict(
            default_contact=default_contact)

        api_response = self.client.signup_new_trusted_cloud_customer(
            **request_dict)
        expected_status_code = 400
        self.assertEqual(api_response.status_code, expected_status_code,
                         'Returned a {0} but expected {1}'.format(
                         api_response.status_code, expected_status_code))

    def test_us_trusted_cloud_signup_without_contact_first_name(self):
        """
        Scenario: Create US Trusted Cloud Account through SignUp Facade
        without Contact First Name
        """
        default_contact = {'first_name': None}
        request_dict = self.get_signup_request_dict(
            default_contact=default_contact)

        api_response = self.client.signup_new_trusted_cloud_customer(
            **request_dict)
        expected_status_code = 400
        self.assertEqual(api_response.status_code, expected_status_code,
                         'Returned a {0} but expected {1}'.format(
                         api_response.status_code, expected_status_code))

    def test_us_trusted_cloud_signup_without_contact_last_name(self):
        """
        Scenario: Create US Trusted Cloud Account through SignUp Facade
        without Contact Last Name
        """
        default_contact = {'last_name': None}
        request_dict = self.get_signup_request_dict(
            default_contact=default_contact)

        api_response = self.client.signup_new_trusted_cloud_customer(
            **request_dict)
        expected_status_code = 400
        self.assertEqual(api_response.status_code, expected_status_code,
                         'Returned a {0} but expected {1}'.format(
                         api_response.status_code, expected_status_code))

    def test_us_trusted_cloud_signup_without_contact_address_country(self):
        """
        Scenario: Create US Trusted Cloud Account through SignUp Facade
        without Contact Address Country
        """
        default_address = {'country': None}
        request_dict = self.get_signup_request_dict(
            default_address=default_address)

        api_response = self.client.signup_new_trusted_cloud_customer(
            **request_dict)
        expected_status_code = 400
        self.assertEqual(api_response.status_code, expected_status_code,
                         'Returned a {0} but expected {1}'.format(
                         api_response.status_code, expected_status_code))

    def test_us_trusted_cloud_signup_without_contact_address_primary(self):
        """
        Scenario: Create US Trusted Cloud Account through SignUp Facade
        without Contact Address Primary
        """
        default_address = {'primary': None}
        request_dict = self.get_signup_request_dict(
            default_address=default_address)

        api_response = self.client.signup_new_trusted_cloud_customer(
            **request_dict)
        expected_status_code = 400
        self.assertEqual(api_response.status_code, expected_status_code,
                         'Returned a {0} but expected {1}'.format(
                         api_response.status_code, expected_status_code))

    def test_us_trusted_cloud_signup_without_contact_address_street(self):
        """
        Scenario: Create US Trusted Cloud Account through SignUp Facade
        without Contact Address Street
        """
        default_address = {'street': None}
        request_dict = self.get_signup_request_dict(
            default_address=default_address)

        api_response = self.client.signup_new_trusted_cloud_customer(
            **request_dict)
        expected_status_code = 400
        self.assertEqual(api_response.status_code, expected_status_code,
                         'Returned a {0} but expected {1}'.format(
                         api_response.status_code, expected_status_code))

    def test_us_trusted_cloud_signup_without_contact_email_address(self):
        """
        Scenario: Create US Trusted Cloud Account through SignUp Facade
        without Contact Email Address
        """
        default_email_address = {'address': None}
        request_dict = self.get_signup_request_dict(
            default_email_address=default_email_address)

        api_response = self.client.signup_new_trusted_cloud_customer(
            **request_dict)
        expected_status_code = 400
        self.assertEqual(api_response.status_code, expected_status_code,
                         'Returned a {0} but expected {1}'.format(
                         api_response.status_code, expected_status_code))

    def test_us_trusted_cloud_signup_without_contact_email_address_primary(self):
        """
        Scenario: Create US Trusted Cloud Account through SignUp Facade
        without Contact Email Address Primary
        """
        default_email_address = {'primary': None}
        request_dict = self.get_signup_request_dict(
            default_email_address=default_email_address)

        api_response = self.client.signup_new_trusted_cloud_customer(
            **request_dict)
        expected_status_code = 400
        self.assertEqual(api_response.status_code, expected_status_code,
                         'Returned a {0} but expected {1}'.format(
                         api_response.status_code, expected_status_code))

    def test_us_trusted_cloud_signup_without_contact_phone_number_primary(self):
        """
        Scenario: Create US Trusted Cloud Account through SignUp Facade
        without Contact Phone Number Primary
        """
        default_phone_number = {'primary': None}
        request_dict = self.get_signup_request_dict(
            default_phone_number=default_phone_number)

        api_response = self.client.signup_new_trusted_cloud_customer(
            **request_dict)
        expected_status_code = 400
        self.assertEqual(api_response.status_code, expected_status_code,
                         'Returned a {0} but expected {1}'.format(
                         api_response.status_code, expected_status_code))

    def test_us_trusted_cloud_signup_without_contact_phone_number(self):
        """
        Scenario: Create US Trusted Cloud Account through SignUp Facade
        without Contact Phone Number
        """
        default_phone_number = {'number': None}
        request_dict = self.get_signup_request_dict(
            default_phone_number=default_phone_number)

        api_response = self.client.signup_new_trusted_cloud_customer(
            **request_dict)
        expected_status_code = 400
        self.assertEqual(api_response.status_code, expected_status_code,
                         'Returned a {0} but expected {1}'.format(
                         api_response.status_code, expected_status_code))

    def test_us_trusted_cloud_signup_without_contact_phone_number_country(self):
        """
        Scenario: Create US Trusted Cloud Account through SignUp Facade
        without Contact Phone Number Country
        """
        default_phone_number = {'country': None}
        request_dict = self.get_signup_request_dict(
            default_phone_number=default_phone_number)

        api_response = self.client.signup_new_trusted_cloud_customer(
            **request_dict)
        expected_status_code = 400
        self.assertEqual(api_response.status_code, expected_status_code,
                         'Returned a {0} but expected {1}'.format(
                         api_response.status_code, expected_status_code))

    @attr('failing', '500')
    def test_us_trusted_cloud_signup_without_contact_phone_number_category(self):
        """
        Scenario: Create US Trusted Cloud Account through SignUp Facade
        without Contact Phone Number Category
        """
        default_phone_number = {'category': None}
        request_dict = self.get_signup_request_dict(
            default_phone_number=default_phone_number)

        api_response = self.client.signup_new_trusted_cloud_customer(
            **request_dict)
        expected_status_code = 400
        self.assertEqual(api_response.status_code, expected_status_code,
                         'Returned a {0} but expected {1}'.format(
                         api_response.status_code, expected_status_code))

    def test_us_trusted_cloud_signup_with_all_payment_card_details_missing(self):
        """
        Scenario: Create US Trusted Cloud Account through SignUp Facade
        with all Payment Card Details missing
        """
        default_payment_card = {'card_holder_name': None,
                                'card_number': None,
                                'card_type': None,
                                'card_verification_number': None,
                                'expiration_date': None}
        request_dict = self.get_signup_request_dict(
            default_payment_card=default_payment_card)

        api_response = self.client.signup_new_trusted_cloud_customer(
            **request_dict)
        expected_status_code = 400
        self.assertEqual(api_response.status_code, expected_status_code,
                         'Returned a {0} but expected {1}'.format(
                         api_response.status_code, expected_status_code))

    def test_us_trusted_cloud_signup_without_card_expiration_date(self):
        """
        Scenario: Create US Trusted Cloud Account through SignUp Facade
        without Card Expiration Date
        """
        default_payment_card = {'expiration_date': None}
        request_dict = self.get_signup_request_dict(
            default_payment_card=default_payment_card)

        api_response = self.client.signup_new_trusted_cloud_customer(
            **request_dict)
        expected_status_code = 400
        self.assertEqual(api_response.status_code, expected_status_code,
                         'Returned a {0} but expected {1}'.format(
                         api_response.status_code, expected_status_code))

    def test_us_trusted_cloud_signup_without_card_type(self):
        """
        Scenario: Create US Trusted Cloud Account through SignUp Facade
        without Card Type
        """
        default_payment_card = {'card_type': None}
        request_dict = self.get_signup_request_dict(
            default_payment_card=default_payment_card)

        api_response = self.client.signup_new_trusted_cloud_customer(
            **request_dict)
        expected_status_code = 400
        self.assertEqual(api_response.status_code, expected_status_code,
                         'Returned a {0} but expected {1}'.format(
                         api_response.status_code, expected_status_code))

    def test_us_trusted_cloud_signup_without_card_verification_number(self):
        """
        Scenario: Create US Trusted Cloud Account through SignUp Facade
        without Card Verification Number
        """
        default_payment_card = {'card_verification_number': None}
        request_dict = self.get_signup_request_dict(
            default_payment_card=default_payment_card)

        api_response = self.client.signup_new_trusted_cloud_customer(
            **request_dict)
        expected_status_code = 400
        self.assertEqual(api_response.status_code, expected_status_code,
                         'Returned a {0} but expected {1}'.format(
                         api_response.status_code, expected_status_code))

    def test_us_trusted_cloud_signup_without_complete_payment_details(self):
        """
        Scenario: Create US Trusted Cloud Account through SignUp Facade
        with all Payment Method Info missing
        """
        payment_method = {}
        request_dict = self.get_signup_request_dict(
            payment_method=payment_method)

        api_response = self.client.signup_new_trusted_cloud_customer(
            **request_dict)
        expected_status_code = 400
        self.assertEqual(api_response.status_code, expected_status_code,
                         'Returned a {0} but expected {1}'.format(
                         api_response.status_code, expected_status_code))

    def test_us_trusted_cloud_signup_with_all_payment_method_info_missing(self):
        """
        Scenario: Create US Trusted Cloud Account through SignUp Facade
        with all Payment Method Info missing
        """
        payment_method = {'consolidated_invoice': None,
                          'payment_card': None}
        request_dict = self.get_signup_request_dict(
            payment_method=payment_method)

        api_response = self.client.signup_new_trusted_cloud_customer(
            **request_dict)
        expected_status_code = 400
        self.assertEqual(api_response.status_code, expected_status_code,
                         'Returned a {0} but expected {1}'.format(
                         api_response.status_code, expected_status_code))

    def test_us_trusted_cloud_signup_without_consolidated_invoice_and_payment_card(self):
        """
        Scenario: Create US Trusted Cloud Account through SignUp Facade
        without any Payment Method Type
        """
        payment_method = {'consolidated_invoice':
                         {'managed_account_number': None},
                          'payment_card': None}
        request_dict = self.get_signup_request_dict(
            payment_method=payment_method)

        api_response = self.client.signup_new_trusted_cloud_customer(
            **request_dict)
        expected_status_code = 400
        self.assertEqual(api_response.status_code, expected_status_code,
                         'Returned a {0} but expected {1}'.format(
                         api_response.status_code, expected_status_code))

    def test_us_trusted_cloud_signup_with_no_managed_account_number_in_ci_and_payment_card(self):
        """
        Scenario: Create US Trusted Cloud Account through SignUp Facade
        with Empty Value in Consolidated Invoice Account Number and Payment
        Card
        """
        payment_method = {'consolidated_invoice':
                         {'managed_account_number': ''},
                          'payment_card': None}
        request_dict = self.get_signup_request_dict(
            payment_method=payment_method)

        api_response = self.client.signup_new_trusted_cloud_customer(
            **request_dict)
        expected_status_code = 400
        self.assertEqual(api_response.status_code, expected_status_code,
                         'Returned a {0} but expected {1}'.format(
                         api_response.status_code, expected_status_code))

    def test_us_trusted_cloud_signup_request_without_complete_contact_roles(self):
        """
        Scenario: Create US Trusted Cloud Account through Signup Facade without
        Complete Contact Roles
        """
        default_contact = {'roles': None}
        request_dict = self.get_signup_request_dict(
            default_contact=default_contact)

        api_response = self.client.signup_new_trusted_cloud_customer(
            **request_dict)
        expected_status_code = 400
        self.assertEqual(api_response.status_code, expected_status_code,
                         'Returned a {0} but expected {1}'.format(
                         api_response.status_code, expected_status_code))

        failure_string = "Contact Role is missing!"
        self.assertIsNotNone(re.search(failure_string, api_response.content),
                             self.assert_msg.format(failure_string))

    def test_us_trusted_cloud_signup_request_without_contact_primary_role(self):
        """
        Scenario: Create US Trusted Cloud Account through Signup Facade without
        Contact Primary Role
        """
        roles = [{'role': 'BILLING'},
                 {'role': None}]
        request_dict = self.get_signup_request_dict(roles=roles)

        api_response = self.client.signup_new_trusted_cloud_customer(
            **request_dict)
        expected_status_code = 400
        self.assertEqual(api_response.status_code, expected_status_code,
                         'Returned a {0} but expected {1}'.format(
                         api_response.status_code, expected_status_code))

        failure_string = "PRIMARY -- Contact details not found!"
        self.assertIsNotNone(re.search(failure_string, api_response.content),
                             self.assert_msg.format(failure_string))

    def test_us_trusted_cloud_signup_request_without_contact_billing_role(self):
        """
        Scenario: Create US Trusted Cloud Account through Signup Facade without
        Contact Billing Role
        """
        roles = [{'role': None},
                 {'role': 'PRIMARY'}]
        request_dict = self.get_signup_request_dict(roles=roles)

        api_response = self.client.signup_new_trusted_cloud_customer(
            **request_dict)
        expected_status_code = 400
        self.assertEqual(api_response.status_code, expected_status_code,
                         'Returned a {0} but expected {1}'.format(
                         api_response.status_code, expected_status_code))

        failure_string = "BILLING -- Contact details not found!"
        self.assertIsNotNone(re.search(failure_string, api_response.content),
                             self.assert_msg.format(failure_string))

    def test_us_trusted_cloud_signup_request_without_both_contact_roles(self):
        """
        Scenario: Create US Trusted Cloud Account through Signup Facade without
        both Contact Roles
        """
        roles = [{'role': None},
                 {'role': None}]
        request_dict = self.get_signup_request_dict(roles=roles)

        api_response = self.client.signup_new_trusted_cloud_customer(
            **request_dict)
        expected_status_code = 400
        self.assertEqual(api_response.status_code, expected_status_code,
                         'Returned a {0} but expected {1}'.format(
                         api_response.status_code, expected_status_code))

        failure_string = "PRIMARY -- Contact details not found!"
        self.assertIsNotNone(re.search(failure_string, api_response.content),
                             self.assert_msg.format(failure_string))

    def test_us_trusted_cloud_signup_with_invalid_business_type(self):
        """
        Scenario: Create US Trusted Cloud Account through SignUp Facade
        with Invalid Business Type as INVALID
        """
        signup_request = {'business_type': 'INVALID'}
        request_dict = self.get_signup_request_dict(
            signup_request=signup_request)

        api_response = self.client.signup_new_trusted_cloud_customer(
            **request_dict)
        expected_status_code = 400
        self.assertEqual(api_response.status_code, expected_status_code,
                         'Returned a {0} but expected {1}'.format(
                         api_response.status_code, expected_status_code))

    def test_us_trusted_cloud_signup_with_invalid_terms_and_conditions(self):
        """
        Scenario: Create US Trusted Cloud Account through SignUp Facade
        with Invalid Terms and Conditions as UK
        """
        signup_request = {'terms_and_conditions': 'UK'}
        request_dict = self.get_signup_request_dict(
            signup_request=signup_request)

        api_response = self.client.signup_new_trusted_cloud_customer(
            **request_dict)
        expected_status_code = 400
        self.assertEqual(api_response.status_code, expected_status_code,
                         'Returned a {0} but expected {1}'.format(
                         api_response.status_code, expected_status_code))

    def test_us_trusted_cloud_signup_request_with_invalid_card_type(self):
        """
        Scenario: Create US Trusted Cloud Account through SignUp Facade
        with Invalid Card Type
        """
        default_payment_card = {'card_type': 'CARD'}
        request_dict = self.get_signup_request_dict(
            default_payment_card=default_payment_card)

        api_response = self.client.signup_new_trusted_cloud_customer(
            **request_dict)
        expected_status_code = 400
        self.assertEqual(api_response.status_code, expected_status_code,
                         'Returned a {0} but expected {1}'.format(
                         api_response.status_code, expected_status_code))

        failure_string = "No enum const class com.rackspacecloud.api.payment"\
                         ".v1.PaymentCardType.CARD"
        self.assertIsNotNone(re.search(failure_string, api_response.content),
                             self.assert_msg.format(failure_string))

    def test_us_trusted_cloud_signup_request_without_card_number(self):
        """
        Scenario: Create US Trusted Cloud Account through SignUp Facade
        without Card Number
        """
        default_payment_card = {'card_number': None}
        request_dict = self.us_trusted_signup.get_signup_request_dict(
            default_payment_card=default_payment_card)

        api_response = self.assertBadRequestCodeAndMessage(
            self.account_type, request_dict, self.mandatory_details)

    def test_us_trusted_cloud_signup_request_without_card_holder_name(self):
        """
        Scenario: Create US Trusted Cloud Account through SignUp Facade
        without Card Holder Name
        """
        default_payment_card = {'card_holder_name': None}
        request_dict = self.us_trusted_signup.get_signup_request_dict(
            default_payment_card=default_payment_card)

        api_response = self.assertBadRequestCodeAndMessage(
            self.account_type, request_dict, self.mandatory_details)

    def test_us_trusted_cloud_signup_request_with_mismatch_card_number_and_card_type(self):
        """
        Scenario: Create US Trusted Cloud Account through SignUp Facade
        with Mismatch Card Number and Card Type
        """
        default_payment_card = {'card_number': CreditCards.VISA_CARD_NUMBER,
                                'card_type': CreditCards.AMERICANEXPRESS_CARD}
        request_dict = self.us_trusted_signup.get_signup_request_dict(
            default_payment_card=default_payment_card)

        failure_string = "paymentCard.cardNumber-This credit card number "\
                         "does not match to the type of card"
        api_response = self.assertBadRequestCodeAndMessage(
            self.account_type, request_dict, failure_string)

    def test_us_trusted_cloud_signup_request_with_no_card_expiration_date(self):
        """
        Scenario: Create US Trusted Cloud Account through SignUp Facade with
        Empty Value in Card Expiration Date
        """
        default_payment_card = {'expiration_date': ''}
        request_dict = self.us_trusted_signup.get_signup_request_dict(
            default_payment_card=default_payment_card)

        api_response = self.assertBadRequestCodeAndMessage(
            self.account_type, request_dict, self.mandatory_details)

    def test_us_trusted_cloud_signup_request_with_incorrect_card_expiration_date(self):
        """
        Scenario: Create US Trusted Cloud Account through SignUp Facade with
        Incorrect Value in Card Expiration Date
        """
        default_payment_card = {'expiration_date': '01/2013'}
        request_dict = self.us_trusted_signup.get_signup_request_dict(
            default_payment_card=default_payment_card)

        failure_string = "paymentCard.expirationDate-Card is expired"
        api_response = self.assertBadRequestCodeAndMessage(
            self.account_type, request_dict, failure_string)

    def test_us_trusted_cloud_signup_request_with_improper_card_expiration_date_format(self):
        """
        Scenario: Create US Trusted Cloud Account through SignUp Facade with
        Improper format Value in Card Expiration Date
        """
        default_payment_card = {'expiration_date': '012013'}
        request_dict = self.us_trusted_signup.get_signup_request_dict(
            default_payment_card=default_payment_card)

        failure_string = "Payment Expiration not in proper format"
        api_response = self.assertBadRequestCodeAndMessage(
            self.account_type, request_dict, failure_string)

    def test_us_trusted_cloud_signup_request_with_no_card_number(self):
        """
        Scenario: Create US Trusted Cloud Account through SignUp Facade with
        Empty Value in Card Number
        """
        default_payment_card = {'card_number': ''}
        request_dict = self.us_trusted_signup.get_signup_request_dict(
            default_payment_card=default_payment_card)

        api_response = self.assertBadRequestCodeAndMessage(
            self.account_type, request_dict, self.mandatory_details)

    def test_us_trusted_cloud_signup_request_with_improper_card_number_format(self):
        """
        Scenario: Create US Trusted Cloud Account through SignUp Facade with
        Improper format value in Card Number
        """
        default_payment_card = {'card_number': 'INVALID123456789'}
        request_dict = self.us_trusted_signup.get_signup_request_dict(
            default_payment_card=default_payment_card)

        failure_string = "Payment card number not in proper format"
        api_response = self.assertBadRequestCodeAndMessage(
            self.account_type, request_dict, failure_string)

    def test_us_trusted_cloud_signup_request_with_invalid_card_number(self):
        """
        Scenario: Create US Trusted Cloud Account through SignUp Facade with
        Invalid Value in Card Number
        """
        default_payment_card = {'card_number': '1234567890123456'}
        request_dict = self.us_trusted_signup.get_signup_request_dict(
            default_payment_card=default_payment_card)

        failure_string = "paymentCard.cardNumber-Invalid credit card "\
            "numberpaymentCard.cardNumber-This credit card number does "\
            "not match to the type of card"
        api_response = self.assertBadRequestCodeAndMessage(
            self.account_type, request_dict, failure_string)

    def test_us_trusted_cloud_signup_request_with_no_card_type(self):
        """
        Scenario: Create US Trusted Cloud Account through SignUp Facade with
        Empty Value in Card Type
        """
        default_payment_card = {'card_type': ''}
        request_dict = self.us_trusted_signup.get_signup_request_dict(
            default_payment_card=default_payment_card)

        failure_string = "Pls. provide card type.  Supported Card types are "\
                         "VISA, MASTERCARD, AMEX, DISCOVER"
        api_response = self.assertBadRequestCodeAndMessage(
            self.account_type, request_dict, failure_string)

    def test_us_trusted_cloud_signup_request_with_card_type_in_lower_case_format(self):
        """
        Scenario: Create US Trusted Cloud Account through SignUp Facade with
        Card Type Value in Lower Case Format
        """
        default_payment_card = {'card_type': 'visa'}
        request_dict = self.us_trusted_signup.get_signup_request_dict(
            default_payment_card=default_payment_card)

        failure_string = "No enum const class "\
            "com.rackspacecloud.api.payment.v1.PaymentCardType.visa"
        api_response = self.assertBadRequestCodeAndMessage(
            self.account_type, request_dict, failure_string)

    def test_us_trusted_cloud_signup_request_with_card_type_in_camel_case_format(self):
        """
        Scenario: Create US Trusted Cloud Account through SignUp Facade with
        Card Type Value in Camel Case Format
        """
        default_payment_card = {'card_type': 'Visa'}
        request_dict = self.us_trusted_signup.get_signup_request_dict(
            default_payment_card=default_payment_card)

        failure_string = "No enum const class "\
            "com.rackspacecloud.api.payment.v1.PaymentCardType.Visa"
        api_response = self.assertBadRequestCodeAndMessage(
            self.account_type, request_dict, failure_string)

    def test_us_trusted_cloud_signup_request_with_no_card_verification_number(self):
        """
        Scenario: Create US Trusted Cloud Account through SignUp Facade with
        Empty Value in Card Verification Number
        """
        default_payment_card = {'card_verification_number': ''}
        request_dict = self.us_trusted_signup.get_signup_request_dict(
            default_payment_card=default_payment_card)

        api_response = self.assertBadRequestCodeAndMessage(
            self.account_type, request_dict, self.mandatory_details)

    def test_us_trusted_cloud_signup_request_with_improper_length_for_card_verification_number(self):
        """
        Scenario: Create US Trusted Cloud Account through SignUp Facade with
        Improper Length Value in Card Verification Number
        """
        default_payment_card = {'card_verification_number': '12345'}
        request_dict = self.us_trusted_signup.get_signup_request_dict(
            default_payment_card=default_payment_card)

        failure_string = "Payment Card Verification Number Length Exceeded.+"\
            " Max Length should be 4"
        api_response = self.assertBadRequestCodeAndMessage(
            self.account_type, request_dict, failure_string)

    def test_us_trusted_cloud_signup_request_with_invalid_card_verification_number(self):
        """
        Scenario: Create US Trusted Cloud Account through SignUp Facade with
        Invalid Value in Card Verification Number
        """
        default_payment_card = {'card_verification_number': 'abc'}
        request_dict = self.us_trusted_signup.get_signup_request_dict(
            default_payment_card=default_payment_card)

        failure_string = "paymentCard.cardVerificationNumber-"\
            "Invalid CVV format"
        api_response = self.assertBadRequestCodeAndMessage(
            self.account_type, request_dict, failure_string)

    def test_us_trusted_cloud_signup_request_with_no_card_holder_name(self):
        """
        Scenario: Create US Trusted Cloud Account through SignUp Facade with
        Empty Value in Card Holder Name
        """
        default_payment_card = {'card_holder_name': ''}
        request_dict = self.us_trusted_signup.get_signup_request_dict(
            default_payment_card=default_payment_card)

        api_response = self.assertBadRequestCodeAndMessage(
            self.account_type, request_dict, self.mandatory_details)
