from datetime import date, datetime
import re
import os
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
        To process the request and to check the response code
        """
        method.client = method.provider.get_default_client(
            deserialize_format='xml')
        api_response = method.client.signup_events_marker(params=params)

        method.assertEqual(api_response.status_code, expected_status_code,
                           'Returned a {0} but expected {1}'
                           .format(api_response.status_code,
                           expected_status_code))
        return api_response

    def verify_signup_id(method, signup_id, api_response):
        """
        To verify whether the newly created Signup ID is the Most Successful
        Recent Marker
        """
        api_response = '{0}'.format(method.common_positive_steps().content)

        method.assertIsNotNone(re.search(
            signup_id, api_response),
            "The New Signup Id is not the Most Recent Successful Marker")


class RaxSignupAPI_GetSignupEventsMarker_Positive(RaxSignupAPI_Common_Methods):

    def test_get_successful_signup_events_marker_default(self):
        """
        Scenario: Get the Most Recent Successful Marker
        """
        self.common_positive_steps()

    def test_get_successful_signup_events_marker_based_on_current_time(self):
        """
        Scenario: Get the Most Recent Successful Marker based on current time
        """
        #Setting Time Zone to Local Time in order to get Current Time
        os.environ['TZ'] = 'localtime'

        #Setting Current Time
        date_time = '{0}{1}'.format(date.strftime(datetime.now(),
                                    '%Y-%m-%dT%H:%M:%S.%f')[:-3], 'Z')
        params = {'datetime': date_time}

        #Making a POST Call in order to verify the newly created Signup ID
        #appears in the Get Successful Signup Events Marker Call
        request_dict = self.us_cloud_signup.get_signup_request_dict()
        account_type = Account_Type.Cloud

        api_response = self.signup_post_calls(request_dict, account_type)
        self.common_positive_steps(params=params)

    def test_get_successful_signup_events_marker_for_us_cloud_signup(self):
        """
        Scenario: Get the Most Recent Successful Marker and check whether it is
        the newly created US Cloud Signup ID
        """
        request_dict = self.us_cloud_signup.get_signup_request_dict()
        account_type = Account_Type.Cloud

        api_response = self.signup_post_calls(request_dict, account_type)
        signup_id = self.get_marker(api_response)

        self.verify_signup_id(signup_id=signup_id, api_response=api_response)

    def test_get_successful_signup_events_marker_for_uk_cloud_signup(self):
        """
        Scenario: Get the Most Recent Successful Marker and check whether it is
        the newly created UK Cloud Signup ID
        """
        request_dict = self.uk_cloud_signup.get_signup_request_dict()
        account_type = Account_Type.Cloud

        api_response = self.signup_post_calls(request_dict, account_type)
        signup_id = self.get_marker(api_response)

        self.verify_signup_id(signup_id=signup_id, api_response=api_response)

    def test_get_successful_signup_events_marker_for_us_trusted_cloud_signup(self):
        """
        Scenario: Get the Most Recent Successful Marker and check whether it is
        the newly created US Trusted Cloud Signup ID
        """
        request_dict = self.us_trusted_signup.get_signup_request_dict()
        account_type = Account_Type.Trusted_Cloud

        api_response = self.signup_post_calls(request_dict, account_type)
        signup_id = self.get_marker(api_response)

        self.verify_signup_id(signup_id=signup_id, api_response=api_response)

    def test_get_successful_signup_events_marker_for_uk_trusted_cloud_signup(self):
        """
        Scenario: Get the Most Recent Successful Marker and check whether it is
        the newly created UK Trusted Cloud Signup ID
        """
        request_dict = self.uk_trusted_signup.get_signup_request_dict()
        account_type = Account_Type.Trusted_Cloud

        api_response = self.signup_post_calls(request_dict, account_type)
        signup_id = self.get_marker(api_response)

        self.verify_signup_id(signup_id=signup_id, api_response=api_response)

    def test_get_successful_signup_events_marker_for_email_apps_signup(self):
        """
        Scenario: Get the Most Recent Successful Marker and check whether it is
        the newly created Email Apps Signup ID
        """
        request_dict = self.email_apps_signup.get_signup_request_dict()
        account_type = Account_Type.Email_Apps

        api_response = self.signup_post_calls(request_dict, account_type)
        signup_id = self.get_marker(api_response)

        self.verify_signup_id(signup_id=signup_id, api_response=api_response)
