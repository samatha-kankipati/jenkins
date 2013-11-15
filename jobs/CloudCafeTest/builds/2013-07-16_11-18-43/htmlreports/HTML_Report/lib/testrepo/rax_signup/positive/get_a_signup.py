import time
import re
from ccengine.common.decorators import attr
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

    def common_positive_steps(method, signup_id, expected_status_code=200):
        """
        To process the request based on the parameters passed and to check the
        response code
        """
        api_response = method.client.get_a_signup(signup_id=signup_id)
        method.assertEqual(api_response.status_code, expected_status_code,
                           'Returned a {0} but expected {1}'.format(
                           api_response.status_code, expected_status_code))
        return api_response

    def generate_random_value(method):
        return time.time()

    def validation_for_status_of_signup(method, get_signup_response=None,
                                        status='COMPLETE'):
        """
        Common method to check whether the given signup is as mentioned,
        the default check is done for the status to be COMPLETE
        """
        get_signup_response = "{0}".format(get_signup_response)
        status_regex = 'region\":\"(UK|US)\",\"status\":\"{0}\"'.format(status)
        method.assertIsNotNone(re.search(status_regex, get_signup_response),
                               "Status of SignUp is not {0}".format(status))


class RaxSignupAPI_GetASignup_US_Cloud(RaxSignupAPI_Common_Methods):

    def test_get_a_signup_with_signup_id_of_us_cloud_signup(self):
        """
        Scenario: Get the details of Specific Signup with Signup ID of US Cloud
        Signup
        """
        request_dict = self.us_cloud_signup.get_signup_request_dict()
        account_type = Account_Type.Cloud

        api_response = self.signup_post_calls(request_dict, account_type)
        signup_id = self.get_marker(api_response)
        params = None

        get_signup_response = self.common_positive_steps(signup_id).content
        self.validation_for_status_of_signup(
            get_signup_response=get_signup_response)

    def test_get_a_signup_with_signup_id_of_uk_cloud_signup(self):
        """
        Scenario: Get the details of Specific Signup with Signup ID of UK Cloud
        Signup
        """
        request_dict = self.uk_cloud_signup.get_signup_request_dict()
        account_type = Account_Type.Cloud

        api_response = self.signup_post_calls(request_dict, account_type)
        signup_id = self.get_marker(api_response)
        params = None

        get_signup_response = self.common_positive_steps(signup_id).content
        self.validation_for_status_of_signup(
            get_signup_response=get_signup_response)

    def test_get_a_signup_with_signup_id_of_us_trusted_cloud_signup(self):
        """
        Scenario: Get the details of Specific Signup with Signup ID of US
        Trusted Cloud Signup
        """
        request_dict = self.us_trusted_signup.get_signup_request_dict()
        account_type = Account_Type.Trusted_Cloud

        api_response = self.signup_post_calls(request_dict, account_type)
        signup_id = self.get_marker(api_response)
        params = None

        get_signup_response = self.common_positive_steps(signup_id).content
        self.validation_for_status_of_signup(
            get_signup_response=get_signup_response)

    def test_get_a_signup_with_signup_id_of_uk_trusted_cloud_signup(self):
        """
        Scenario: Get the details of Specific Signup with Signup ID of UK
        Trusted Cloud Signup
        """
        request_dict = self.uk_trusted_signup.get_signup_request_dict()
        account_type = Account_Type.Trusted_Cloud

        api_response = self.signup_post_calls(request_dict, account_type)
        signup_id = self.get_marker(api_response)
        params = None

        get_signup_response = self.common_positive_steps(signup_id).content
        self.validation_for_status_of_signup(
            get_signup_response=get_signup_response)

    def test_get_a_signup_with_signup_id_of_email_apps_signup(self):
        """
        Scenario: Get the details of Specific Signup with Signup ID of Email
        Apps Signup
        """
        request_dict = self.email_apps_signup.get_signup_request_dict()
        account_type = Account_Type.Email_Apps

        api_response = self.signup_post_calls(request_dict, account_type)
        signup_id = self.get_marker(api_response)
        params = None

        get_signup_response = self.common_positive_steps(signup_id).content
        self.validation_for_status_of_signup(
            get_signup_response=get_signup_response)
