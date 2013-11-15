#import re
from ccengine.common.decorators import attr
from datetime import date, datetime
import time
import os
import re
from testrepo.common.testfixtures.rax_signup import\
    RaxSignupAPI_BaseFixture, RaxSignupAPI_EmailAndAppsSignupFixture
from testrepo.common.testfixtures.rax_signup import\
    RaxSignupAPI_CloudSignupFixture, RaxSignupAPI_CloudSignupFixture_UK
from testrepo.common.testfixtures.rax_signup import\
    RaxSignupAPI_TrustedCloudSignupFixture,\
    RaxSignupAPI_TrustedCloudSignupFixture_UK, Account_Type


class RaxSignupAPI_Common_Methods(RaxSignupAPI_BaseFixture):

    us_cloud_signup = RaxSignupAPI_CloudSignupFixture
    uk_cloud_signup = RaxSignupAPI_CloudSignupFixture_UK
    us_trusted_signup = RaxSignupAPI_TrustedCloudSignupFixture
    uk_trusted_signup = RaxSignupAPI_TrustedCloudSignupFixture_UK
    email_apps_signup = RaxSignupAPI_EmailAndAppsSignupFixture

    def common_positive_steps(method, params, expected_status_code=200):
        """
        To process the request based on the parameters passed and to check the
        response code
        """
        api_response = method.client.list_signups(params=params)
        method.assertEqual(api_response.status_code, expected_status_code,
                           'Returned a {0} but expected {1}'.format(
                           api_response.status_code, expected_status_code))
        return api_response

    def generate_random_value(method):
        return time.time()


class RaxSignupAPI_GetSignupLists_Positive(RaxSignupAPI_Common_Methods):
        #Only the response is being checked as of now
    def test_get_list_of_signups_with_status_as_complete(self):
        """
        Scenario: Get the List of Signups based on Status as COMPLETE
        """
        params = {'status': 'COMPLETE'}
        self.common_positive_steps(params)

    def test_get_list_of_signups_with_status_as_in_progress(self):
        """
        Scenario: Get the List of Signups based on Status as IN_PROGRESS
        """
        params = {'status': 'IN_PROGRESS'}
        self.common_positive_steps(params)

    def test_get_list_of_signups_with_status_as_error(self):
        """
        Scenario: Get the List of Signups based on Status as ERROR
        """
        params = {'status': 'ERROR'}
        self.common_positive_steps(params)

    def test_get_list_of_signups_with_status_as_complete_in_lower_case_format(self):
        """
        Scenario: Get the List of Signups based on Status as complete in Lower
        Case Format
        """
        params = {'status': 'complete'}
        self.common_positive_steps(params)

    def test_get_list_of_signups_with_status_as_in_progress_in_camel_case_format(self):
        """
        Scenario: Get the List of Signups based on Status as In_PrOgReSs in
        Camel Case Format
        """
        params = {'status': 'In_PrOgReSs'}
        self.common_positive_steps(params)

    def test_get_list_of_signups_with_default_limit_equal_to_50(self):
        """
        Scenario: Get the List of Signups based with Default Limit value
        equal to 50
        """
        params = {}
        self.common_positive_steps(params)

    def test_get_list_of_signups_with_limit_10(self):
        """
        Scenario: Get the List of Signups based on limit
        """
        params = {'limit': '10'}
        self.common_positive_steps(params)

    def test_get_list_of_signups_with_maximum_limit_equal_to_1000(self):
        """
        Scenario: Get the List of Signups based with Maximum Limit value
        equal to 1000
        """
        params = {'limit': '1000'}
        self.common_positive_steps(params)

    def test_get_list_of_signups_with_limit_and_status(self):
        """
        Scenario: Get the List of Signups based on Status and results limited
        to 10
        """
        params = {
            'limit': '10',
            'status': 'COMPLETE'}
        self.common_positive_steps(params)

    def test_get_list_of_signups_with_account_type_as_email_and_apps(self):
        """
        Scenario: Get the List of Signups based on Account Type as Email & Apps
        """
        params = {'type': 'EMAIL_APPS'}
        self.common_positive_steps(params)

    def test_get_list_of_signups_with_account_type_as_trusted_cloud_in_camel_case_format(self):
        """
        Scenario: Get the List of Signups based on Account Type as
        TrUsTeD_ClOuD in Camel Case Format
        """
        params = {'type': 'TrUsTeD_ClOuD'}
        self.common_positive_steps(params)

    def test_get_list_of_signups_with_account_type_as_cloud(self):
        """
        Scenario: Get the List of Signups based on Account Type as Cloud
        """
        params = {'type': 'CLOUD'}
        self.common_positive_steps(params)

    def test_get_list_of_signups_with_account_type_as_trusted_cloud(self):
        """
        Scenario: Get the List of Signups based on Account Type as
        Trusted Cloud
        """
        params = {'type': 'TRUSTED_CLOUD'}
        self.common_positive_steps(params)

    def test_get_list_of_signups_with_account_type_as_email_and_apps_in_lower_case_format(self):
        """
        Scenario: Get the List of Signups based on Account Type as email_apps
        in Lower Case Format
        """
        params = {'type': 'email_apps'}
        self.common_positive_steps(params)

    def test_get_list_of_signups_with_region_as_us(self):
        """
        Scenario: Get the List of Signups based on Region as US
        """
        params = {'region': 'US'}
        self.common_positive_steps(params)

    def test_get_list_of_signups_with_region_as_uk(self):
        """
        Scenario: Get the List of Signups based on Region as UK
        """
        params = {'region': 'UK'}
        self.common_positive_steps(params)

    def test_get_list_of_signups_with_region_as_us_in_lower_case_format(self):
        """
        Scenario: Get the List of Signups based on Region as US in Lower Case
        Format
        """
        params = {'region': 'us'}
        self.common_positive_steps(params)

    def test_get_list_of_signups_with_region_as_uk_in_lower_case_format(self):
        """
        Scenario: Get the List of Signups based on Region as uK in Lower Case
        Format
        """
        params = {'region': 'uK'}
        self.common_positive_steps(params)

    def test_get_list_of_signups_with_after_datetime_as_current_time(self):
        """
        Scenario: Get the List of Signups with after_datetime as Current Time
        """
        #Setting Time Zone to Local Time in order to get Current Time
        os.environ['TZ'] = 'localtime'

        #Setting Current Time
        after_datetime = date.strftime(datetime.now(), '%Y-%m-%dT%H:%M:%S')
        print after_datetime
        params = {'after_datetime': after_datetime}

        #Making a POST Call in order to verify the newly created Signup ID
        #appears in the Get List of Signups
        request_dict = self.us_cloud_signup.get_signup_request_dict()
        account_type = Account_Type.Cloud

        api_response = self.signup_post_calls(request_dict, account_type)
        print api_response.content
        self.common_positive_steps(params=params)

    def test_get_list_of_signups_with_reference_entity_id_of_us_cloud_signup(self):
        """
        Scenario: Get the List of Signups based on Reference Entity ID of
        US Cloud Signup
        """
        request_dict = self.us_cloud_signup.get_signup_request_dict()
        account_type = Account_Type.Cloud

        api_response = self.signup_post_calls(request_dict, account_type)
        reference_entity_id = self.get_reference_entity_id(api_response)

        params = {'reference_entity_id': reference_entity_id}
        self.common_positive_steps(params)

    def test_get_list_of_signups_with_reference_entity_id_of_uk_cloud_signup(self):
        """
        Scenario: Get the List of Signups based on Reference Entity ID of
        UK Cloud Signup
        """
        request_dict = self.uk_cloud_signup.get_signup_request_dict()
        account_type = Account_Type.Cloud

        api_response = self.signup_post_calls(request_dict, account_type)
        reference_entity_id = self.get_reference_entity_id(api_response)

        params = {'reference_entity_id': reference_entity_id}
        self.common_positive_steps(params)

    def test_get_list_of_signups_with_reference_entity_id_of_us_trusted_cloud_signup(self):
        """
        Scenario: Get the List of Signups based on Reference Entity ID of
        US Trusted Cloud Signup
        """
        request_dict = self.us_trusted_signup.get_signup_request_dict()
        account_type = Account_Type.Trusted_Cloud

        api_response = self.signup_post_calls(request_dict, account_type)
        reference_entity_id = self.get_reference_entity_id(api_response)

        params = {'reference_entity_id': reference_entity_id}
        self.common_positive_steps(params)

    def test_get_list_of_signups_with_reference_entity_id_of_uk_trusted_cloud_signup(self):
        """
        Scenario: Get the List of Signups based on Reference Entity ID of
        UK Trusted Cloud Signup
        """
        request_dict = self.uk_trusted_signup.get_signup_request_dict()
        account_type = Account_Type.Trusted_Cloud

        api_response = self.signup_post_calls(request_dict, account_type)
        reference_entity_id = self.get_reference_entity_id(api_response)

        params = {'reference_entity_id': reference_entity_id}
        self.common_positive_steps(params)

    def test_get_list_of_signups_with_reference_entity_id_of_email_apps_signup(self):
        """
        Scenario: Get the List of Signups based on Reference Entity ID of
        Email & Apps Signup
        """
        request_dict = self.email_apps_signup.get_signup_request_dict()
        account_type = Account_Type.Email_Apps

        api_response = self.signup_post_calls(request_dict, account_type)
        reference_entity_id = self.get_reference_entity_id(api_response)

        params = {'reference_entity_id': reference_entity_id}
        self.common_positive_steps(params)

    def test_get_list_of_signups_with_marker_of_us_cloud_signup(self):
        """
        Scenario: Get the List of Signups based on marker of US Cloud Signup
        """
        request_dict = self.us_cloud_signup.get_signup_request_dict()
        account_type = Account_Type.Cloud

        api_response = self.signup_post_calls(request_dict, account_type)
        marker = self.get_marker(api_response)

        params = {'marker': marker}
        self.common_positive_steps(params)

    def test_get_list_of_signups_with_marker_of_uk_cloud_signup(self):
        """
        Scenario: Get the List of Signups based on marker of UK Cloud Signup
        """
        request_dict = self.uk_cloud_signup.get_signup_request_dict()
        account_type = Account_Type.Cloud

        api_response = self.signup_post_calls(request_dict, account_type)
        marker = self.get_marker(api_response)

        params = {'marker': marker}
        self.common_positive_steps(params)

    def test_get_list_of_signups_with_marker_of_us_trusted_cloud_signup(self):
        """
        Scenario: Get the List of Signups based on Marker of US Trusted Cloud
        Signup
        """
        request_dict = self.us_trusted_signup.get_signup_request_dict()
        account_type = Account_Type.Trusted_Cloud

        api_response = self.signup_post_calls(request_dict, account_type)
        marker = self.get_marker(api_response)

        params = {'marker': marker}
        self.common_positive_steps(params)

    def test_get_list_of_signups_with_marker_of_uk_trusted_cloud_signup(self):
        """
        Scenario: Get the List of Signups based on Marker of UK Trusted Cloud
        Signup
        """
        request_dict = self.uk_trusted_signup.get_signup_request_dict()
        account_type = Account_Type.Trusted_Cloud

        api_response = self.signup_post_calls(request_dict, account_type)
        marker = self.get_marker(api_response)

        params = {'marker': marker}
        self.common_positive_steps(params)

    def test_get_list_of_signups_with_marker_of_email_apps_signup(self):
        """
        Scenario: Get the List of Signups based on Marker of Email & Apps
        Signup
        """
        request_dict = self.email_apps_signup.get_signup_request_dict()
        account_type = Account_Type.Email_Apps

        api_response = self.signup_post_calls(request_dict, account_type)
        marker = self.get_marker(api_response)

        params = {'marker': marker}
        self.common_positive_steps(params)


#To test that the uk cloud signups failed due to payment details are not listed
class RaxSignupAPI_GetSignupLists_UK_Cloud(RaxSignupAPI_CloudSignupFixture_UK,
                                           RaxSignupAPI_Common_Methods):

    def test_get_list_of_signups_to_check_payment_failed_card_type_uk_cloud_signup_is_not_listed(self):
        """
        Scenario: Get the list of signups with status as error, check that the
        uk cloud signup which failed due to payment method - card type should
        not be listed
        """
        default_payment_card = {'card_type': 'amex'}
        description = "Description for invalid credit card {0}".format(
            self.generate_random_value())
        signup_request = {'description': description}
        request_dict = self.get_signup_request_dict(
            default_payment_card=default_payment_card,
            signup_request=signup_request)

        api_response = self.client.signup_new_cloud_customer(**request_dict)
        params = {'limit': '10', 'status': 'ERROR'}
        self.assertEqual(api_response.status_code, 400,
                         'Returned a {0} but expected {1}'.format(
                         api_response.status_code, 400))

        api_response1 = "{0}".format(self.common_positive_steps(params)
                             .content)
        self.assertFalse(re.search(description, api_response1),
                         "The failed signup is present in signup lists")

    def test_get_list_of_signups_to_check_payment_failed_uk_cloud_signup_is_not_listed(self):
        """
        Scenario: Get the list of signups with status as error, check that the
        uk cloud signup which failed due to payment method - card number should
        not be listed
        """
        print "Known issue : UK cloud signup passes with invalid credit card"
        default_payment_card = {'card_number': '4111111111111111'}
        description = "Description for invalid credit card {0}".format(
            self.generate_random_value())
        signup_request = {'description': description}
        request_dict = self.get_signup_request_dict(
            default_payment_card=default_payment_card,
            signup_request=signup_request)

        api_response = self.client.signup_new_cloud_customer(**request_dict)
        params = {'limit': '10', 'status': 'ERROR'}
        self.assertEqual(api_response.status_code, 400,
                         'Returned a {0} but expected {1}'.format(
                         api_response.status_code, 400))

        api_response1 = "{0}".format(self.common_positive_steps(params)
                             .content)
        self.assertFalse(re.search(description, api_response1),
                         "The failed signup is present in signup lists")

    def test_get_list_of_signups_to_check_payment_failed_vrfn_code_uk_cloud_signup_is_not_listed(self):
        """
        Scenario: Get the list of signups with status as error, check that the
        uk cloud signup which failed due to payment method - card verification
        number should not be listed
        """
        default_payment_card = {'card_verification_number': 'abcd'}
        description = "Description for invalid credit card {0}".format(
            self.generate_random_value())
        signup_request = {'description': description}
        request_dict = self.get_signup_request_dict(
            default_payment_card=default_payment_card,
            signup_request=signup_request)

        api_response = self.client.signup_new_cloud_customer(**request_dict)
        params = {'limit': '10', 'status': 'ERROR'}
        if (api_response.status_code == 201):
            print "\n\n Known issue:UK cloud signup with invalid vrfn code\
               \b will return 201"
        self.assertEqual(api_response.status_code, 400,
                         'Returned a {0} but expected {1}'.format(
                         api_response.status_code, 400))

        api_response1 = "{0}".format(self.common_positive_steps(params)
                             .content)
        self.assertFalse(re.search(description, api_response1),
                         "The failed signup is present in signup lists")


#To test that the us cloud signups failed due to payment details are not listed
class RaxSignupAPI_GetSignupLists_US_Cloud(RaxSignupAPI_CloudSignupFixture,
                                           RaxSignupAPI_Common_Methods):

    def test_get_signups_list_to_check_payment_failed_invalid_vrfn_code_us_cloud_signup_is_not_listed(self):
        """
        Scenario: Get the list of signups with status as error, check that the
        us cloud signup which failed due to invalid card verification code in
        payment method should not be listed
        """
        default_payment_card = {'card_verification_number': 'abcd'}
        description = "Description for invalid credit card {0}".format(
            self.generate_random_value())
        signup_request = {'description': description}
        request_dict = self.get_signup_request_dict(
            default_payment_card=default_payment_card,
            signup_request=signup_request)

        api_response = self.client.signup_new_cloud_customer(**request_dict)
        params = {'limit': '10', 'status': 'ERROR'}
        self.assertEqual(api_response.status_code, 400,
                         'Returned a {0} but expected {1}'.format(
                         api_response.status_code, 400))

        api_response1 = "{0}".format(self.common_positive_steps(params)
                             .content)
        self.assertFalse(re.search(description, api_response1),
                         "The failed signup is present in signup lists")

    def test_get_signups_list_to_check_payment_failed_invalid_card_number_us_cloud_signup_is_not_listed(self):
        """
        Scenario: Get the list of signups with status as error, check that the
        us cloud signup which failed due to invalid card number in
        payment method should not be listed
        """
        default_payment_card = {'card_number': '4111111111111111'}
        description = "Description for invalid credit card {0}".format(
            self.generate_random_value())
        signup_request = {'description': description}
        request_dict = self.get_signup_request_dict(
            default_payment_card=default_payment_card,
            signup_request=signup_request)

        api_response = self.client.signup_new_cloud_customer(**request_dict)
        params = {'limit': '10', 'status': 'ERROR'}
        self.assertEqual(api_response.status_code, 400,
                         'Returned a {0} but expected {1}'.format(
                         api_response.status_code, 400))

        api_response1 = "{0}".format(self.common_positive_steps(params)
                             .content)
        self.assertFalse(re.search(description, api_response1),
                         "The failed signup is present in signup lists")


#For us trusted cloud
class RaxSignupAPI_GetSignupLists_US_Trusted_Cloud(
        RaxSignupAPI_TrustedCloudSignupFixture,
        RaxSignupAPI_Common_Methods):

    def test_get_signups_list_to_check_payment_failed_invalid_card_us_trusted_cloud_signup_is_not_listed(self):
        """
        Scenario: Get the list of signups with status as error, check that the
        us trusted cloud signup which failed due to payment method should
        not be listed
        """
        default_payment_card = {'card_number': '4111111111111111'}
        description = "Description for invalid credit card {0}".format(
            self.generate_random_value())
        signup_request = {'description': description,
                          'type_': 'TRUSTED_CLOUD'}
        request_dict = self.get_signup_request_dict(
            default_payment_card=default_payment_card,
            signup_request=signup_request)

        api_response = self.client.signup_new_trusted_cloud_customer(
            **request_dict)
        params = {'limit': '10', 'status': 'ERROR'}
        self.assertEqual(api_response.status_code, 400,
                         'Returned a {0} but expected {1}'.format(
                         api_response.status_code, 400))

        api_response1 = "{0}".format(self.common_positive_steps(params)
                             .content)
        self.assertFalse(re.search(description, api_response1),
                         "The failed signup is present in signup lists")


#For uk trusted cloud
class RaxSignupAPI_GetSignupLists_UK_Trusted_Cloud(
        RaxSignupAPI_TrustedCloudSignupFixture_UK,
        RaxSignupAPI_Common_Methods):
    def test_get_signups_list_to_check_payment_failed_invalid_card_uk_trusted_cloud_signup_is_not_listed(self):
        """
        Scenario: Get the list of signups with status as error, check that the
        uk trusted cloud signup which failed due to payment method should
        not be listed
        """

        default_payment_card = {'card_number': '4111111111111111'}
        description = "Description for invalid credit card {0}".format(
            self.generate_random_value())
        signup_request = {'description': description}
        request_dict = self.get_signup_request_dict(
            default_payment_card=default_payment_card,
            signup_request=signup_request)

        api_response = self.client.signup_new_trusted_cloud_customer(
            **request_dict)
        params = {'limit': '10', 'status': 'ERROR'}
        self.assertEqual(api_response.status_code, 400,
                         'Returned a {0} but expected {1}'.format(
                         api_response.status_code, 400))

        api_response1 = "{0}".format(self.common_positive_steps(params)
                             .content)
        self.assertFalse(re.search(description, api_response1),
                         "The failed signup is present in signup lists")
