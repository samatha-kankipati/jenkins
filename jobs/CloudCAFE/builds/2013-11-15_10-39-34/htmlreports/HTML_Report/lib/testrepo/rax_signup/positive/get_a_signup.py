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
        method.assert_time_format_for_get_calls(api_response)
        return api_response

    def generate_random_value(method):
        return time.time()

    def validation_for_status_of_signup(method, get_signup_response=None,
                                        status='COMPLETE'):
        """
        Common method to check whether the given signup is as mentioned,
        the default check is done for the status to be COMPLETE
        """
        status_regex = 'region\":\"(UK|US)\",.+\"status\":\"{0}\"'.format(
            status)
        method.assertIsNotNone(re.search(status_regex, get_signup_response),
                               "Status of SignUp is not {0}".format(status))

    def check_for_geography_attribute(method,
                                      get_signup_response=None,
                                      geography=None):
        """
        Common method to check whether the geography attribute is displayed
        in the response
        """
        geography_regex = 'region\":\"{0}\",.+\"geography\":\"{0}\"'.format(
            geography)
        method.assertIsNotNone(re.search(geography_regex, get_signup_response),
                               "Geography attribute is not present")

    def check_for_default_region_attribute(method,
                                           get_signup_response=None,
                                           default_region=None):
        """
        Common method to check whether the defaultRegion attribute is displayed
        in the response
        """
        exp_regex = 'geoLocation\":\"{0}\",\"defaultRegion\":\"{0}'.format(
            default_region)
        method.assertIsNotNone(re.search(exp_regex, get_signup_response),
                               "Default Region attribute is not present")


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

    @attr('geography')
    def test_get_a_us_cloud_signup_for_geography_attribute_check(self):
        """
        Scenario to check whether geography attribute is been displayed
        in the get a signup response
        """
        request_dict = self.us_cloud_signup.get_signup_request_dict()
        account_type = Account_Type.Cloud

        api_response = self.signup_post_calls(request_dict, account_type)
        signup_id = self.get_marker(api_response)

        get_signup_response = self.common_positive_steps(signup_id).content
        self.validation_for_status_of_signup(
            get_signup_response=get_signup_response)
        self.check_for_geography_attribute(
            get_signup_response=get_signup_response, geography="US")

    @attr('geography', 'default_region')
    def test_get_a_us_cloud_signup_for_geography_and_default_region_attribute_check(self):
        """
        Scenario to check whether geography and the default region attribute
        are been displayed in the get a signup response
        """
        geography = "US"
        default_region = "SYD"
        signup_request = {'default_region': default_region,
                          'geography': geography,
                          'region': None}
        request_dict = self.us_cloud_signup.get_signup_request_dict(
            signup_request=signup_request)
        account_type = Account_Type.Cloud

        api_response = self.signup_post_calls(request_dict, account_type)
        signup_id = self.get_marker(api_response)

        self.pause_in_seconds()
        get_signup_response = self.common_positive_steps(signup_id).content
        self.validation_for_status_of_signup(
            get_signup_response=get_signup_response)
        self.check_for_geography_attribute(
            get_signup_response=get_signup_response, geography=geography)
        self.check_for_default_region_attribute(
            get_signup_response=get_signup_response,
            default_region=default_region)

    @attr('geography')
    def test_get_a_us_trusted_cloud_signup_for_geography_attribute_check(self):
        """
        Scenario to check whether geography attribute is been displayed
        in the get a signup response
        """
        request_dict = self.us_trusted_signup.get_signup_request_dict()
        account_type = Account_Type.Trusted_Cloud

        api_response = self.signup_post_calls(request_dict, account_type)
        signup_id = self.get_marker(api_response)

        get_signup_response = self.common_positive_steps(signup_id).content
        self.validation_for_status_of_signup(
            get_signup_response=get_signup_response)
        self.check_for_geography_attribute(
            get_signup_response=get_signup_response, geography="US")

    @attr('geography', 'default_region')
    def test_get_a_us_trusted_cloud_signup_for_geography_and_default_region_attribute_check(self):
        """
        Scenario to check whether geography and the default region attribute
        are been displayed in the get a signup response
        """
        geography = "US"
        default_region = "SYD"
        signup_request = {'default_region': default_region,
                          'geography': geography,
                          'region': None}
        request_dict = self.us_trusted_signup.get_signup_request_dict(
            signup_request=signup_request)
        account_type = Account_Type.Trusted_Cloud

        api_response = self.signup_post_calls(request_dict, account_type)
        signup_id = self.get_marker(api_response)

        self.pause_in_seconds()
        get_signup_response = self.common_positive_steps(signup_id).content
        self.validation_for_status_of_signup(
            get_signup_response=get_signup_response)
        self.check_for_geography_attribute(
            get_signup_response=get_signup_response, geography=geography)
        self.check_for_default_region_attribute(
            get_signup_response=get_signup_response,
            default_region=default_region)

    @attr('geography')
    def test_get_a_signup_with_signup_id_of_uk_cloud_signup_for_geography(self):
        """
        Scenario: Get the details of Specific Signup with Signup ID of UK Cloud
        Signup
        """
        geography = "UK"
        signup_request = {'geography': geography, 'region': None}
        request_dict = self.uk_cloud_signup.get_signup_request_dict(
            signup_request=signup_request)
        account_type = Account_Type.Cloud

        api_response = self.signup_post_calls(request_dict, account_type)
        signup_id = self.get_marker(api_response)

        get_signup_response = self.common_positive_steps(signup_id).content
        self.validation_for_status_of_signup(
            get_signup_response=get_signup_response)
        self.check_for_geography_attribute(
            get_signup_response=get_signup_response, geography=geography)

    @attr('geography')
    def test_get_a_signup_with_signup_id_of_uk_trusted_cloud_signup_for_geography(self):
        """
        Scenario: Get the details of Specific Signup with Signup ID of UK
        Trusted Cloud Signup
        """
        geography = "UK"
        request_dict = self.uk_trusted_signup.get_signup_request_dict()
        account_type = Account_Type.Trusted_Cloud

        api_response = self.signup_post_calls(request_dict, account_type)
        signup_id = self.get_marker(api_response)

        get_signup_response = self.common_positive_steps(signup_id).content
        self.validation_for_status_of_signup(
            get_signup_response=get_signup_response)
        self.check_for_geography_attribute(
            get_signup_response=get_signup_response, geography=geography)

    @attr('geography')
    def test_get_a_signup_with_signup_id_of_email_apps_signup_for_geography(self):
        """
        Scenario: Get the details of Specific Signup with Signup ID of Email
        Apps Signup
        """
        geography = "US"
        signup_request = {'geography': geography, 'region': None}
        request_dict = self.email_apps_signup.get_signup_request_dict(
            signup_request=signup_request)
        account_type = Account_Type.Email_Apps

        api_response = self.signup_post_calls(request_dict, account_type)
        signup_id = self.get_marker(api_response)

        get_signup_response = self.common_positive_steps(signup_id).content
        self.validation_for_status_of_signup(
            get_signup_response=get_signup_response)
        self.check_for_geography_attribute(
            get_signup_response=get_signup_response, geography=geography)
