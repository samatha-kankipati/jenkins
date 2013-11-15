import time
import re
from ccengine.providers.rax_signup.rax_signup_api import RaxSignupProvider
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

    @classmethod
    def setUpClass(cls):
        super(RaxSignupAPI_Common_Methods, cls).setUpClass()
        cls.provider = RaxSignupProvider(cls.config)
        cls.client = cls.provider.get_default_client()

    def common_positive_steps(method, params=None, expected_status_code=200):
        """
        To process the request based on the parameters passed and to check the
        response code
        """
        method.client = method.provider.get_default_client(
            deserialize_format='xml')
        api_response = method.client.signup_events(params=params)
        method.assertEqual(api_response.status_code, expected_status_code,
                           'Returned a {0} but expected {1}'
                           .format(api_response.status_code,
                           expected_status_code))
        return api_response

    def generate_random_value(method):
        return time.time()

    def verify_signup_id(method, signup_id, api_response):
        """
        To verify whether the newly created Signup ID is present
        """
        api_response = '{0}'.format(method.common_positive_steps().content)
        method.assertIsNotNone(re.search(signup_id, api_response),
                               "The new signup id is not present")


class RaxSignupAPI_GetSignupEvents_Positive(RaxSignupAPI_Common_Methods):
        # Only the response is being checked as of now
    def test_get_successful_signup_events_default(self):
        """
        Scenario: Get the details of Successful Signup Events
        """
        self.common_positive_steps()

    def test_get_successful_signup_events_with_marker(self):
        """
        Scenario: Get Successful Signup Events based on Marker
        """
        api_response = '{0}'.format(self.common_positive_steps().content)
        marker = re.search("success\?marker=(.+?)?&", api_response).group(1)
        params = {'marker': marker}
        self.common_positive_steps(params)

    def test_get_successful_signup_events_with_direction_forward(self):
        """
        Scenario: Get Successful Signup Events based on Direction as Forward
        """
        params = {'direction': 'forward'}
        self.common_positive_steps(params)

    def test_get_successful_signup_events_with_direction_backward(self):
        """
        Scenario: Get Successful Signup Events based on Direction as Backward
        """
        params = {'direction': 'backward'}
        self.common_positive_steps(params)

    def test_get_successful_signup_events_with_limit(self):
        """
        Scenario: Get Successful Signup Events based on Limit
        """
        params = {'limit': 110}
        self.common_positive_steps(params)

    def test_get_successful_signup_events_with_limit_marker_direction(self):
        """
        Scenario: Get Successful Signup Events based on Limit, Marker and
        Direction as parameters
        """
        api_response = '{0}'.format(self.common_positive_steps().content)
        marker = re.search("success\?marker=(.+?)?&", api_response).group(1)
        params = {'limit': 20, 'marker': marker, 'direction': 'backward'}
        self.common_positive_steps(params)

    def test_get_successful_signup_events_to_check_whether_us_cloud_signup_is_present(self):
        """
        Scenario: Get Successful Signup Events to check whether the recent
        US Cloud Signup Id is listed in the Feeds
        """
        request_dict = self.us_cloud_signup.get_signup_request_dict()
        account_type = Account_Type.Cloud

        api_response = self.signup_post_calls(request_dict, account_type)
        signup_id = self.get_marker(api_response)

        self.verify_signup_id(signup_id=signup_id, api_response=api_response)

    def test_get_successful_signup_events_to_check_whether_uk_cloud_signup_is_present(self):
        """
        Scenario: Get Successful Signup Events to check whether the recent
        UK Cloud Signup Id is listed in the Feeds
        """
        request_dict = self.uk_cloud_signup.get_signup_request_dict()
        account_type = Account_Type.Cloud

        api_response = self.signup_post_calls(request_dict, account_type)
        signup_id = self.get_marker(api_response)

        self.verify_signup_id(signup_id=signup_id, api_response=api_response)

    def test_get_successful_signup_events_to_check_whether_us_trusted_cloud_signup_is_present(self):
        """
        Scenario: Get Successful Signup Events to check whether the recent
        US Trusted Cloud Signup Id is listed in the Feeds
        """
        request_dict = self.us_trusted_signup.get_signup_request_dict()
        account_type = Account_Type.Trusted_Cloud

        api_response = self.signup_post_calls(request_dict, account_type)
        signup_id = self.get_marker(api_response)

        self.verify_signup_id(signup_id=signup_id, api_response=api_response)

    def test_get_successful_signup_events_to_check_whether_uk_trusted_cloud_signup_is_present(self):
        """
        Scenario: Get Successful Signup Events to check whether the recent
        UK Trusted Cloud Signup Id is listed in the Feeds
        """
        request_dict = self.uk_trusted_signup.get_signup_request_dict()
        account_type = Account_Type.Trusted_Cloud

        api_response = self.signup_post_calls(request_dict, account_type)
        signup_id = self.get_marker(api_response)

        self.verify_signup_id(signup_id=signup_id, api_response=api_response)

    def test_get_successful_signup_events_to_check_whether_uk_email_apps_signup_is_present(self):
        """
        Scenario: Get Successful Signup Events to check whether the recent
        Email Apps Signup Id is listed in the Feeds
        """
        request_dict = self.email_apps_signup.get_signup_request_dict()
        account_type = Account_Type.Email_Apps

        api_response = self.signup_post_calls(request_dict, account_type)
        signup_id = self.get_marker(api_response)

        self.verify_signup_id(signup_id=signup_id, api_response=api_response)
