import re
import time
from ccengine.common.decorators import attr
from testrepo.common.testfixtures.rax_signup import\
    RaxSignupAPI_CloudSignupFixture, CreditCards


class RaxSignupAPI_CloudSignupRequest_NegativeSmoke(
        RaxSignupAPI_CloudSignupFixture):

    us_cloud_signup = RaxSignupAPI_CloudSignupFixture
    account_type = "CLOUD"

    assert_msg = "Test expected the string - '{0}' in the response body,"\
        " but not found"

    mandatory_details = "Payment card mandatory details missing!"\
        "CardHolderName, Number, ExpirationDate, Verification number"\
        " and card type is mandatory."

    def test_us_cloud_signup_request_without_region(self):
        """
        Scenario: Create US Cloud Account through SignUp Facade without Region
        """
        signup_request = {'region': None}
        request_dict = self.get_signup_request_dict(
            signup_request=signup_request)

        api_response = self.client.signup_new_cloud_customer(**request_dict)
        expected_status_code = 400
        self.assertEqual(api_response.status_code, expected_status_code,
                         'Returned a {0} but expected {1}'.format(
                         api_response.status_code, expected_status_code))

        #We may not want to include checks for the failure messages, since
        #they could be different between xml and json.  BUT, if you
        #want to, this would be a good way to do it so that it works for both
        #types of responses.
        failure_string = "Cloud - Invalid Region!"
        self.assertIsNotNone(re.search(failure_string, api_response.content),
                             '{0} not found'.format(failure_string))

    def test_us_cloud_signup_request_without_account_name(self):
        """
        Scenario: Create US Cloud Account through SignUp Facade without
        Account Name
        """
        signup_request = {'account_name': None}
        request_dict = self.get_signup_request_dict(
            signup_request=signup_request)

        api_response = self.client.signup_new_cloud_customer(**request_dict)
        expected_status_code = 400
        self.assertEqual(api_response.status_code, expected_status_code,
                         'Returned a {0} but expected {1}'.format(
                         api_response.status_code, expected_status_code))

        failure_string = "Account Name missing on request!"
        self.assertIsNotNone(re.search(failure_string, api_response.content),
                             '{0} not found'.format(failure_string))

    def test_us_cloud_signup_request_with_invalid_accept_terms_and_conditions(self):
        """
        Scenario: Create US Cloud Account through SignUp Facade with
        Invalid Accept Terms and Conditions
        """
        signup_request = {'accept_terms_and_conditions': 'FAKE'}
        request_dict = self.get_signup_request_dict(
            signup_request=signup_request)

        api_response = self.client.signup_new_cloud_customer(**request_dict)
        expected_status_code = 400
        self.assertEqual(api_response.status_code, expected_status_code,
                         'Returned a {0} but expected {1}'.format(
                         api_response.status_code, expected_status_code))

        failure_string = "Can not construct instance of boolean from String"
        "value \'{0}\'".format(signup_request['accept_terms_and_conditions'])
        self.assertIsNotNone(re.search(failure_string, api_response.content),
                             '{0} not found'.format(failure_string))

    # Will only be implemented with Sydney Datacenter
    #def test_us_cloud_signup_request_without_business_type(self):
    #    """
    #    Scenario: Create US Cloud Account through SignUp Facade for Cloud
    #    without account type
    #    """
    #    signup_request = {'business_type': None}
    #    request_dict = self.get_signup_request_dict(
    #    signup_request=signup_request)
    #    api_response = self.client.signup_new_cloud_customer(**request_dict)
    #    expected_status_code = 400
    #    self.assertEqual(api_response.status_code, expected_status_code,
    #            'Returned a {0} but expected {1}'.format(
    #            api_response.status_code,
    #            expected_status_code))

    def test_us_cloud_signup_request_without_username(self):
        """
        Scenario: Create US Cloud Account through SignUp Facade without
        Username
        """
        user = {'username': None}
        request_dict = self.get_signup_request_dict(user=user)

        api_response = self.client.signup_new_cloud_customer(**request_dict)
        expected_status_code = 400
        self.assertEqual(api_response.status_code, expected_status_code,
                         'Returned a {0} but expected {1}'.format(
                         api_response.status_code, expected_status_code))

        # need to check the error message
        failure_string = "User name missing on request!"
        self.assertIsNotNone(re.search(failure_string, api_response.content),
                             '{0} not found'.format(failure_string))

    def test_us_cloud_signup_request_without_password(self):
        """
        Scenario: Create US Cloud Account through SignUp Facade without
        Password
        """
        user = {'password': None}
        request_dict = self.get_signup_request_dict(user=user)

        api_response = self.client.signup_new_cloud_customer(**request_dict)
        expected_status_code = 400
        self.assertEqual(api_response.status_code, expected_status_code,
                         'Returned a {0} but expected {1}'.format(
                         api_response.status_code, expected_status_code))

        failure_string = "User - Password missing on request!"
        self.assertIsNotNone(re.search(failure_string, api_response.content),
                             '{0} not found'.format(failure_string))

    def test_us_cloud_signup_request_without_secret_question(self):
        """
        Scenario: Create US Cloud Account through SignUp Facade without
        Secret Question
        """
        secret_qa = {'question': None}
        request_dict = self.get_signup_request_dict(secret_qa=secret_qa)

        api_response = self.client.signup_new_cloud_customer(**request_dict)
        expected_status_code = 400
        self.assertEqual(api_response.status_code, expected_status_code,
                         'Returned a {0} but expected {1}'.format(
                         api_response.status_code, expected_status_code))

        failure_string = "Secret Q/A shouldn't be empty!"
        self.assertIsNotNone(re.search(failure_string, api_response.content),
                             self.assert_msg.format(failure_string))

    def test_us_cloud_signup_request_without_secret_answer(self):
        """
        Scenario: Create US Cloud Account through SignUp Facade without
        Secret Answer
        """
        secret_qa = {'answer': None}
        request_dict = self.get_signup_request_dict(secret_qa=secret_qa)

        api_response = self.client.signup_new_cloud_customer(**request_dict)
        expected_status_code = 400
        self.assertEqual(api_response.status_code, expected_status_code,
                         'Returned a {0} but expected {1}'.format(
                         api_response.status_code, expected_status_code))

        failure_string = "Secret Q/A shouldn't be empty!"
        self.assertIsNotNone(re.search(failure_string, api_response.content),
                             '{0} not found'.format(failure_string))

    def test_us_cloud_signup_request_without_contacts_tag(self):
        """
        Scenario: Create US Cloud Account through SignUp Facade without
        providing Complete Contact Details
        """
        contacts = []
        request_dict = self.get_signup_request_dict(contacts=contacts)

        api_response = self.client.signup_new_cloud_customer(**request_dict)
        expected_status_code = 400
        self.assertEqual(api_response.status_code, expected_status_code,
                         'Returned a {0} but expected {1}'.format(
                         api_response.status_code, expected_status_code))

        failure_string = "Contacts shouldn't be empty"
        self.assertIsNotNone(re.search(failure_string, api_response.content),
                             self.assert_msg.format(failure_string))

    def test_us_cloud_signup_request_without_address_tag(self):
        """
        Scenario: Create US Cloud Account through SignUp Facade without
        providing Complete Contact Address Details
        """
        addresses = []
        request_dict = self.get_signup_request_dict(addresses=addresses)

        api_response = self.client.signup_new_cloud_customer(**request_dict)
        expected_status_code = 400
        self.assertEqual(api_response.status_code, expected_status_code,
                         'Returned a {0} but expected {1}'.format(
                         api_response.status_code, expected_status_code))

        failure_string = "Contact Address details missing!"
        self.assertIsNotNone(re.search(failure_string, api_response.content),
                             self.assert_msg.format(failure_string))

    def test_us_cloud_signup_request_without_contact_first_name(self):
        """
        Scenario: Create US Cloud Account through SignUp Facade without Contact
        First Name
        """
        default_contact = {'first_name': None}
        request_dict = self.get_signup_request_dict(
            default_contact=default_contact)

        api_response = self.client.signup_new_cloud_customer(**request_dict)
        expected_status_code = 400
        self.assertEqual(api_response.status_code, expected_status_code,
                         'Returned a {0} but expected {1}'.format(
                         api_response.status_code, expected_status_code))

        failure_string = "Contact Name is missing!"
        self.assertIsNotNone(re.search(failure_string, api_response.content),
                             self.assert_msg.format(failure_string))

    def test_us_cloud_signup_request_without_contact_last_name(self):
        """
        Scenario: Create US Cloud Account through SignUp Facade without Contact
        Last Name
        """
        default_contact = {'last_name': None}
        request_dict = self.get_signup_request_dict(
            default_contact=default_contact)

        api_response = self.client.signup_new_cloud_customer(**request_dict)
        expected_status_code = 400
        self.assertEqual(api_response.status_code, expected_status_code,
                         'Returned a {0} but expected {1}'.format(
                         api_response.status_code, expected_status_code))

        failure_string = "Contact Name is missing!"
        self.assertIsNotNone(re.search(failure_string, api_response.content),
                             self.assert_msg.format(failure_string))

    def test_us_cloud_signup_request_without_country(self):
        """
        Scenario: Create US Cloud Account through SignUp Facade without Contact
        Address Country
        """
        default_address = {'country': None}
        request_dict = self.get_signup_request_dict(
            default_address=default_address)

        api_response = self.client.signup_new_cloud_customer(**request_dict)
        expected_status_code = 400
        self.assertEqual(api_response.status_code, expected_status_code,
                         'Returned a {0} but expected {1}'.format(
                         api_response.status_code, expected_status_code))

        failure_string = "Address - Country shouldn't be empty"
        self.assertIsNotNone(re.search(failure_string, api_response.content),
                             self.assert_msg.format(failure_string))

    def test_us_cloud_signup_request_without_address_primary(self):
        """
        Scenario: Create US Cloud Account through SignUp Facade without Contact
        Address Primary
        """
        default_address = {'primary': None}
        request_dict = self.get_signup_request_dict(
            default_address=default_address)

        api_response = self.client.signup_new_cloud_customer(**request_dict)
        expected_status_code = 400
        self.assertEqual(api_response.status_code, expected_status_code,
                         'Returned a {0} but expected {1}'.format(
                         api_response.status_code, expected_status_code))

        failure_string = "Contact -- Primary address not found"
        self.assertIsNotNone(re.search(failure_string, api_response.content),
                             self.assert_msg.format(failure_string))

    def test_us_cloud_signup_request_without_address_street(self):
        """
        Scenario: Create US Cloud Account through SignUp Facade without Contact
        Address Street
        """
        default_address = {'street': None}
        request_dict = self.get_signup_request_dict(
            default_address=default_address)

        api_response = self.client.signup_new_cloud_customer(**request_dict)
        expected_status_code = 400
        self.assertEqual(api_response.status_code, expected_status_code,
                         'Returned a {0} but expected {1}'.format(
                         api_response.status_code, expected_status_code))

        failure_string = "Address - Street shouldn't be empty"
        self.assertIsNotNone(re.search(failure_string, api_response.content),
                             self.assert_msg.format(failure_string))

    def test_us_cloud_signup_request_without_contact_email_address(self):
        """
        Scenario: Create US Cloud Account through SignUp Facade without Contact
        Email Address
        """
        default_email_address = {'address': None}
        request_dict = self.get_signup_request_dict(
            default_email_address=default_email_address)

        api_response = self.client.signup_new_cloud_customer(**request_dict)
        expected_status_code = 400
        self.assertEqual(api_response.status_code, expected_status_code,
                         'Returned a {0} but expected {1}'.format(
                         api_response.status_code, expected_status_code))

        failure_string = "Contact Email Address shouldn't be empty"
        self.assertIsNotNone(re.search(failure_string, api_response.content),
                             self.assert_msg.format(failure_string))

    def test_us_cloud_signup_request_without_email_address_primary(self):
        """
        Scenario: Create US Cloud Account through SignUp Facade without Contact
        Email Address Primary
        """
        default_email_address = {'primary': None}
        request_dict = self.get_signup_request_dict(
            default_email_address=default_email_address)

        api_response = self.client.signup_new_cloud_customer(**request_dict)
        expected_status_code = 400
        self.assertEqual(api_response.status_code, expected_status_code,
                         'Returned a {0} but expected {1}'.format(
                         api_response.status_code, expected_status_code))

        failure_string = "Contact -- Primary Email address not found"
        self.assertIsNotNone(re.search(failure_string, api_response.content),
                             self.assert_msg.format(failure_string))

    def test_us_cloud_signup_request_without_contact_phone_number_primary(self):
        """
        Scenario: Create US Cloud Account through SignUp Facade without
        Contact Phone Number Primary
        """
        default_phone_number = {'primary': None}
        request_dict = self.get_signup_request_dict(
            default_phone_number=default_phone_number)

        api_response = self.client.signup_new_cloud_customer(**request_dict)
        expected_status_code = 400
        self.assertEqual(api_response.status_code, expected_status_code,
                         'Returned a {0} but expected {1}'.format(
                         api_response.status_code, expected_status_code))

        failure_string = "Contact -- Primary phone number not found"
        self.assertIsNotNone(re.search(failure_string, api_response.content),
                             self.assert_msg.format(failure_string))

    def test_us_cloud_signup_request_without_contact_phone_number(self):
        """
        Scenario: Create US Cloud Account through SignUp Facade without Contact
        Phone Number
        """
        default_phone_number = {'number': None}
        request_dict = self.get_signup_request_dict(
            default_phone_number=default_phone_number)

        api_response = self.client.signup_new_cloud_customer(**request_dict)
        expected_status_code = 400
        self.assertEqual(api_response.status_code, expected_status_code,
                         'Returned a {0} but expected {1}'.format(
                         api_response.status_code, expected_status_code))

        failure_string = "Contact -- Phone number is empty!"
        self.assertIsNotNone(re.search(failure_string, api_response.content),
                             self.assert_msg.format(failure_string))

    def test_us_cloud_signup_request_without_contact_phone_number_country(self):
        """
        Scenario: Create US Cloud Account through SignUp Facade without Contact
        Phone Number Country
        """
        default_phone_number = {'country': None}
        request_dict = self.get_signup_request_dict(
            default_phone_number=default_phone_number)

        api_response = self.client.signup_new_cloud_customer(**request_dict)
        expected_status_code = 400
        self.assertEqual(api_response.status_code, expected_status_code,
                         'Returned a {0} but expected {1}'.format(
                         api_response.status_code, expected_status_code))

        failure_string = "Contact -- Phone Country code is empty!"
        self.assertIsNotNone(re.search(failure_string, api_response.content),
                             self.assert_msg.format(failure_string))

    @attr('failing', '500')
    def test_us_cloud_signup_without_contact_phone_number_category(self):
        """
        Scenario: Create US Cloud Account through SignUp Facade without Contact
        Phone Number Category
        """
        default_phone_number = {'category': None}
        request_dict = self.get_signup_request_dict(
            default_phone_number=default_phone_number)

        api_response = self.client.signup_new_cloud_customer(**request_dict)
        expected_status_code = 400
        self.assertEqual(api_response.status_code, expected_status_code,
                         'Returned a {0} but expected {1}'.format(
                         api_response.status_code, expected_status_code))

        failure_string = "Contact -- Phone Country code is empty!"
        self.assertIsNotNone(re.search(failure_string, api_response.content),
                             self.assert_msg.format(failure_string))

    def test_us_cloud_signup_request_without_contact_phone_number_complete(self):
        """
        Scenario: Create US Cloud Account through SignUp Facade without
        providing Complete Contact Phone Number Details
        """
        phone_numbers = []
        request_dict = self.get_signup_request_dict(
            phone_numbers=phone_numbers)

        api_response = self.client.signup_new_cloud_customer(**request_dict)
        expected_status_code = 400
        self.assertEqual(api_response.status_code, expected_status_code,
                         'Returned a {0} but expected {1}'.format(
                         api_response.status_code, expected_status_code))

        failure_string = "Contact Phone detail is missing!"
        self.assertIsNotNone(re.search(failure_string, api_response.content),
                             self.assert_msg.format(failure_string))

        #Responds with 201 hence error message not added
    def test_us_cloud_signup_request_without_order_details(self):
        """
        Scenario: Create US Cloud Account through SignUp Facade without Order
        Details
        """
        signup_request = {'order': None}
        request_dict = self.get_signup_request_dict(
            signup_request=signup_request)

        api_response = self.client.signup_new_cloud_customer(**request_dict)
        expected_status_code = 400
        self.assertEqual(api_response.status_code, expected_status_code,
                         'Returned a {0} but expected {1}'.format(
                         api_response.status_code, expected_status_code))

        failure_string = "order item should not be empty."
        self.assertIsNotNone(re.search(failure_string, api_response.content),
                             self.assert_msg.format(failure_string))

    def test_us_cloud_signup_request_with_existing_username(self):
        """
        Scenario: Create US Cloud Account through SignUp Facade with Existing
        Username
        """
        request_dict = self.get_signup_request_dict()
        api_response = self.client.signup_new_cloud_customer(
            **request_dict)

        #Make initial request
        self.assertDefaultResponseOK(api_response)

        #Make second request with same user info
        username = api_response.request.entity.contacts[0].user.username

        #Begin negative test case
        user = {'username': username}

        api_response = self.client.signup_new_cloud_customer(
            **request_dict)
        expected_status_code = 400
        self.assertEqual(api_response.status_code, expected_status_code,
                         'Returned a {0} but expected {1}'.format(
                         api_response.status_code, expected_status_code))

    def test_us_cloud_signup_request_without_complete_contact_roles(self):
        """
        Scenario: Create US Cloud Account through Signup Facade without
        Complete Contact Roles
        """
        default_contact = {'roles': None}
        request_dict = self.get_signup_request_dict(
            default_contact=default_contact)

        api_response = self.client.signup_new_cloud_customer(**request_dict)
        expected_status_code = 400
        self.assertEqual(api_response.status_code, expected_status_code,
                         'Returned a {0} but expected {1}'.format(
                         api_response.status_code, expected_status_code))

        failure_string = "Contact Role is missing!"
        self.assertIsNotNone(re.search(failure_string, api_response.content),
                             self.assert_msg.format(failure_string))

    def test_us_cloud_signup_request_without_contact_primary_role(self):
        """
        Scenario: Create US Cloud Account through Signup Facade without Contact
        Primary Role
        """
        roles = [{'role': 'BILLING'},
                 {'role': None}]
        request_dict = self.get_signup_request_dict(roles=roles)

        api_response = self.client.signup_new_cloud_customer(**request_dict)
        expected_status_code = 400
        self.assertEqual(api_response.status_code, expected_status_code,
                         'Returned a {0} but expected {1}'.format(
                         api_response.status_code, expected_status_code))

        failure_string = "PRIMARY -- Contact details not found!"
        self.assertIsNotNone(re.search(failure_string, api_response.content),
                             self.assert_msg.format(failure_string))

    def test_us_cloud_signup_request_without_contact_billing_role(self):
        """
        Scenario: Create US Cloud Account through Signup Facade without Contact
        Billing Role
        """
        roles = [{'role': None},
                 {'role': 'PRIMARY'}]
        request_dict = self.get_signup_request_dict(roles=roles)

        api_response = self.client.signup_new_cloud_customer(**request_dict)
        expected_status_code = 400
        self.assertEqual(api_response.status_code, expected_status_code,
                         'Returned a {0} but expected {1}'.format(
                         api_response.status_code, expected_status_code))

        failure_string = "BILLING -- Contact details not found!"
        self.assertIsNotNone(re.search(failure_string, api_response.content),
                             self.assert_msg.format(failure_string))

    def test_us_cloud_signup_request_without_both_contact_roles(self):
        """
        Scenario: Create US Cloud Account through Signup Facade without both
        Contact Roles
        """
        roles = [{'role': None},
                 {'role': None}]
        request_dict = self.get_signup_request_dict(roles=roles)

        api_response = self.client.signup_new_cloud_customer(**request_dict)
        expected_status_code = 400
        self.assertEqual(api_response.status_code, expected_status_code,
                         'Returned a {0} but expected {1}'.format(
                         api_response.status_code, expected_status_code))

        failure_string = "PRIMARY -- Contact details not found!"
        self.assertIsNotNone(re.search(failure_string, api_response.content),
                             self.assert_msg.format(failure_string))

    def test_us_cloud_signup_request_with_invalid_business_type(self):
        """
        Scenario: Create US Cloud Account through Signup Facade with Invalid
        Business Type as INVALID
        """
        signup_request = {'business_type': 'INVALID'}
        request_dict = self.get_signup_request_dict(
            signup_request=signup_request)

        api_response = self.client.signup_new_cloud_customer(**request_dict)
        expected_status_code = 400
        self.assertEqual(api_response.status_code, expected_status_code,
                         'Returned a {0} but expected {1}'.format(
                         api_response.status_code, expected_status_code))

    def test_us_cloud_signup_request_with_invalid_terms_and_conditions(self):
        """
        Scenario: Create US Cloud Account through Signup Facade with Invalid
        Terms and Conditions as UK
        """
        signup_request = {'terms_and_conditions': 'UK'}
        request_dict = self.get_signup_request_dict(
            signup_request=signup_request)

        api_response = self.client.signup_new_cloud_customer(**request_dict)
        expected_status_code = 400
        self.assertEqual(api_response.status_code, expected_status_code,
                         'Returned a {0} but expected {1}'.format(
                         api_response.status_code, expected_status_code))

    def test_us_cloud_signup_request_with_cloud_sites_qty_greater_than_one(self):
        """
        Scenario: Create US Cloud Account through Signup Facade with Cloud
        Sites Quantity greater than one
        """
        default_order_item = {'offering_id': 'CLOUD_SITES',
                              'product_id': 'CLOUD_SITES',
                              'quantity': '5'}
        request_dict = self.get_signup_request_dict(
            default_order_item=default_order_item)

        api_response = self.client.signup_new_cloud_customer(**request_dict)
        expected_status_code = 400
        self.assertEqual(api_response.status_code, expected_status_code,
                         'Returned a {0} but expected {1}'.format(
                         api_response.status_code, expected_status_code))

        failure_string = "CLOUD_SITES order item quantity should not be "\
                         "greater than 1."
        self.assertIsNotNone(re.search(failure_string, api_response.content),
                             '{0} not found'.format(failure_string))

    def test_us_cloud_signup_request_without_order_items(self):
        """
        Scenario: Create US Cloud Account through SignUp Facade without Order
        Items
        """
        metadata = [{"key": "cloudSitesPurchased",
                     "value": "true"},
                    {"key": "cloudFilesPurchased",
                     "value": "true"},
                    {"key": "cloudServersPurchased",
                     "value": "true"},
                    {"key": "loadBalancersPurchased",
                     "value": "false"},
                    {"key": "ipAddress",
                     "value": "10.186.125.23"},
                    {"key": "rackUID",
                     "value": "277298293"},
                    {"key": "deviceFingerPrint",
                     "value": "134.288-8901"}]

        order_items = []
        order = {'id_': None,
                 'order_items': order_items,
                 'metadata': metadata}

        request_dict = self.get_signup_request_dict(
            order=order)

        api_response = self.client.signup_new_cloud_customer(**request_dict)
        expected_status_code = 400
        self.assertEqual(api_response.status_code, expected_status_code,
                         'Returned a {0} but expected {1}'.format(
                         api_response.status_code, expected_status_code))

        failure_string = "order item should not be empty."
        self.assertIsNotNone(re.search(failure_string, api_response.content),
                             self.assert_msg.format(failure_string))

    def test_us_cloud_signup_request_without_payment_details_complete(self):
        """
        Scenario: Create US Cloud Account through SignUp Facade for Cloud without
        providing Complete Payment Details
        """
        payment_method = {}
        us_request_dict = self.us_cloud_signup.get_signup_request_dict(
            payment_method=payment_method)

        failure_string = "Payment card details missing!"
        us_api_response = self.assertBadRequestCodeAndMessage(
            self.account_type, us_request_dict, failure_string)

    def test_us_cloud_signup_request_without_payment_details_card_number(self):
        """
        Scenario: Create US Cloud Account through SignUp Facade without Card
        Number
        """
        default_payment_card = {'card_number': None}
        us_request_dict = self.us_cloud_signup.get_signup_request_dict(
            default_payment_card=default_payment_card)

        us_api_response = self.assertBadRequestCodeAndMessage(
            self.account_type, us_request_dict, self.mandatory_details)

    def test_us_cloud_signup_request_without_payment_details_card_holder_name(self):
        """
        Scenario: Create US Cloud Account through SignUp Facade without Card
        Holder Name
        """
        default_payment_card = {'card_holder_name': None}
        us_request_dict = self.us_cloud_signup.get_signup_request_dict(
            default_payment_card=default_payment_card)

        us_api_response = self.assertBadRequestCodeAndMessage(
            self.account_type, us_request_dict, self.mandatory_details)

    def test_us_cloud_signup_request_without_payment_details_expiration_date(self):
        """
        Scenario: Create US Cloud Account through SignUp Facade without Card
        Expration Date
        """
        default_payment_card = {'expiration_date': None}
        us_request_dict = self.us_cloud_signup.get_signup_request_dict(
            default_payment_card=default_payment_card)

        us_api_response = self.assertBadRequestCodeAndMessage(
            self.account_type, us_request_dict, self.mandatory_details)

    def test_us_cloud_signup_request_without_payment_details_card_type(self):
        """
        Scenario: Create US Cloud Account through SignUp Facade without Card
        Type
        """
        default_payment_card = {'card_type': None}
        failure_string = "Pls. provide card type.  Supported Card types are"\
            " VISA, MASTERCARD, AMEX, DISCOVER"

        us_request_dict = self.us_cloud_signup.get_signup_request_dict(
            default_payment_card=default_payment_card)
        us_api_response = self.assertBadRequestCodeAndMessage(
            self.account_type, us_request_dict, failure_string)

    def test_us_cloud_signup_request_without_payment_details_card_vrfn_number(self):
        """
        Scenario: Create US Cloud Account through SignUp Facade without Card
        Verification Number
        """
        default_payment_card = {'card_verification_number': None}
        us_request_dict = self.us_cloud_signup.get_signup_request_dict(
            default_payment_card=default_payment_card)

        us_api_response = self.assertBadRequestCodeAndMessage(
            self.account_type, us_request_dict, self.mandatory_details)

    def test_us_cloud_signup_request_with_invalid_card_type(self):
        """
        Scenario: Create US Cloud Account through SignUp Facade with Invalid
        Card Type
        """
        default_payment_card = {'card_type': 'CARD'}
        us_request_dict = self.us_cloud_signup.get_signup_request_dict(
            default_payment_card=default_payment_card)

        failure_string = "No enum const class com.rackspacecloud.api.payment"\
            ".v1.PaymentCardType.CARD"
        us_api_response = self.assertBadRequestCodeAndMessage(
            self.account_type, us_request_dict, failure_string)

    def test_us_cloud_signup_request_without_any_payment_details(self):
        """
        Scenario: Create US Cloud Account through SignUp Facade without
        providing Any Payment Details
        """
        default_payment_card = {'card_holder_name': None,
                                'card_number': None,
                                'card_type': None,
                                'card_verification_number': None,
                                'expiration_date': None}
        us_request_dict = self.us_cloud_signup.get_signup_request_dict(
            default_payment_card=default_payment_card)

        us_api_response = self.assertBadRequestCodeAndMessage(
            self.account_type, us_request_dict, self.mandatory_details)

    def test_us_cloud_signup_request_with_no_card_holder_name(self):
        """
        Scenario: Create US Cloud Account through SignUp Facade with Empty
        Value in Card Holder Name
        """
        default_payment_card = {'card_holder_name': ''}
        us_request_dict = self.us_cloud_signup.get_signup_request_dict(
            default_payment_card=default_payment_card)

        us_api_response = self.assertBadRequestCodeAndMessage(
            self.account_type, us_request_dict, self.mandatory_details)

    def test_us_cloud_signup_request_with_no_card_number(self):
        """
        Scenario: Create US Cloud Account through SignUp Facade with Empty
        Value in Card Number
        """
        default_payment_card = {'card_number': ''}
        us_request_dict = self.us_cloud_signup.get_signup_request_dict(
            default_payment_card=default_payment_card)

        us_api_response = self.assertBadRequestCodeAndMessage(
            self.account_type, us_request_dict, self.mandatory_details)

    def test_us_cloud_signup_request_with_no_card_type(self):
        """
        Scenario: Create US Cloud Account through SignUp Facade with Empty
        Value in Card Type
        """
        default_payment_card = {'card_type': ''}
        us_request_dict = self.us_cloud_signup.get_signup_request_dict(
            default_payment_card=default_payment_card)

        failure_string = "Pls. provide card type.  "\
            "Supported Card types are VISA, MASTERCARD, AMEX, DISCOVER"
        us_api_response = self.assertBadRequestCodeAndMessage(
            self.account_type, us_request_dict, failure_string)

    def test_us_cloud_signup_request_with_no_card_verification_number(self):
        """
        Scenario: Create US Cloud Account through SignUp Facade with Empty
        Value in Card Verfication Number
        """
        default_payment_card = {'card_verification_number': ''}
        us_request_dict = self.us_cloud_signup.get_signup_request_dict(
            default_payment_card=default_payment_card)

        us_api_response = self.assertBadRequestCodeAndMessage(
            self.account_type, us_request_dict, self.mandatory_details)

    def test_us_cloud_signup_request_with_no_card_expiration_date(self):
        """
        Scenario: Create US Cloud Account through SignUp Facade with Empty
        Value in Card Expiration Date
        """
        default_payment_card = {'expiration_date': ''}
        us_request_dict = self.us_cloud_signup.get_signup_request_dict(
            default_payment_card=default_payment_card)

        us_api_response = self.assertBadRequestCodeAndMessage(
            self.account_type, us_request_dict, self.mandatory_details)

    def test_us_cloud_signup_request_with_incorrect_expiration_date(self):
        """
        Scenario: Create US Cloud Account through SignUp Facade with Incorrect
        Expiry date given (Past Year Expiry Date)
        """
        default_payment_card = {'expiration_date': '01/2013'}
        us_request_dict = self.us_cloud_signup.get_signup_request_dict(
            default_payment_card=default_payment_card)

        failure_string = "paymentCard.expirationDate-Card is expired"
        us_api_response = self.assertBadRequestCodeAndMessage(
            self.account_type, us_request_dict, failure_string)

    def test_us_cloud_signup_request_with_improper_card_expiration_date_format(self):
        """
        Scenario: Create US Cloud Account through SignUp Facade with Improper
        Format Value in Card Expiration Date
        """
        default_payment_card = {'expiration_date': '102020'}
        us_request_dict = self.us_cloud_signup.get_signup_request_dict(
            default_payment_card=default_payment_card)

        failure_string = "paymentCard.expirationDate-Card is expired"
        us_api_response = self.assertBadRequestCodeAndMessage(
            self.account_type, us_request_dict, failure_string)

    def test_us_cloud_signup_request_with_invalid_card_number(self):
        """
        Scenario: Create US Cloud Account through SignUp Facade with Invalid
        Card Number
        """
        default_payment_card = {'card_number': '1234567890123456'}
        us_request_dict = self.us_cloud_signup.get_signup_request_dict(
            default_payment_card=default_payment_card)

        failure_string = "paymentCard.cardNumber-Invalid credit card "\
            "numberpaymentCard.cardNumber-This credit card number does "\
            "not match to the type of card"
        us_api_response = self.assertBadRequestCodeAndMessage(
            self.account_type, us_request_dict, failure_string)

    def test_us_cloud_signup_request_with_improper_card_number_format(self):
        """
        Scenario: Create US Cloud Account through SignUp Facade with Improper
        Format Value in Card Number
        """
        default_payment_card = {'card_number': 'INVALID123456789'}
        us_request_dict = self.us_cloud_signup.get_signup_request_dict(
            default_payment_card=default_payment_card)

        failure_string = "Payment card number not in proper format"
        us_api_response = self.assertBadRequestCodeAndMessage(
            self.account_type, us_request_dict, failure_string)

    def test_us_cloud_signup_request_with_card_type_in_lower_case_format(self):
        """
        Scenario: Create US Cloud Account through SignUp Facade with
        Card Type in Lower Case Format
        """
        default_payment_card = {'card_type': 'visa'}
        us_request_dict = self.us_cloud_signup.get_signup_request_dict(
            default_payment_card=default_payment_card)

        failure_string = "No enum const class "\
            "com.rackspacecloud.api.payment.v1.PaymentCardType.visa"
        us_api_response = self.assertBadRequestCodeAndMessage(
            self.account_type, us_request_dict, failure_string)

    def test_us_cloud_signup_request_with_card_type_in_camel_case_format(self):
        """
        Scenario: Create US Cloud Account through SignUp Facade with
        Card Type in Camel Case Format
        """
        default_payment_card = {'card_type': 'Visa'}
        us_request_dict = self.us_cloud_signup.get_signup_request_dict(
            default_payment_card=default_payment_card)

        failure_string = "No enum const class "\
            "com.rackspacecloud.api.payment.v1.PaymentCardType.Visa"
        us_api_response = self.assertBadRequestCodeAndMessage(
            self.account_type, us_request_dict, failure_string)

    def test_us_cloud_signup_request_with_mismatch_card_type_and_card_number(self):
        """
        Scenario: Create US Cloud Account through SignUp Facade with Mismatch
        Card Number and Card Type
        """
        default_payment_card = {'card_number': CreditCards.VISA_CARD_NUMBER,
                                'card_type': CreditCards.AMERICANEXPRESS_CARD}
        us_request_dict = self.us_cloud_signup.get_signup_request_dict(
            default_payment_card=default_payment_card)

        failure_string = "paymentCard.cardNumber-This credit card number "\
                         "does not match to the type of card"
        us_api_response = self.assertBadRequestCodeAndMessage(
            self.account_type, us_request_dict, failure_string)

    def test_us_cloud_signup_request_with_improper_length_for_card_vrfn_number(self):
        """
        Scenario: Create US Cloud Account through SignUp Facade with Improper
        Length for Card Verfication Number
        """
        default_payment_card = {'card_verification_number': '12345'}
        us_request_dict = self.us_cloud_signup.get_signup_request_dict(
            default_payment_card=default_payment_card)

        failure_string = "Payment Card Verification Number Length Exceeded.+"\
            " Max Length should be 4"
        us_api_response = self.assertBadRequestCodeAndMessage(
            self.account_type, us_request_dict, failure_string)

    def test_us_cloud_signup_request_with_invalid_card_verification_number(self):
        """
        Scenario: Create US Cloud Account through SignUp Facade with Invalid
        Card Verification Number
        """
        default_payment_card = {'card_verification_number': 'ABC'}
        us_request_dict = self.us_cloud_signup.get_signup_request_dict(
            default_payment_card=default_payment_card)

        failure_string = "paymentCard.cardVerificationNumber-"\
            "Invalid CVV format"
        us_api_response = self.assertBadRequestCodeAndMessage(
            self.account_type, us_request_dict, failure_string)

#Scenario: Create US Cloud Account through SignUp Facade for Cloud without
#skip fraud check - only present in trusted cloud
#Scenario: Create US Cloud Account through SignUp Facade for Cloud without
#managed account number in cloud signup request body - present only in tru
#Scenario: Create US Cloud Account through SignUp Facade for Cloud without
#contact phone number  extension- not in contract
