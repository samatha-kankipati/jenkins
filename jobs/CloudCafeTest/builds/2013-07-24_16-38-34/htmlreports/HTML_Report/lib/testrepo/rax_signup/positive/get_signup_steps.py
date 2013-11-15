import re
from testrepo.common.testfixtures.rax_signup import\
    RaxSignupAPI_BaseFixture, RaxSignupAPI_EmailAndAppsSignupFixture
from testrepo.common.testfixtures.rax_signup import\
    RaxSignupAPI_CloudSignupFixture, RaxSignupAPI_CloudSignupFixture_UK
from testrepo.common.testfixtures.rax_signup import\
    RaxSignupAPI_TrustedCloudSignupFixture,\
    RaxSignupAPI_TrustedCloudSignupFixture_UK, Account_Type


class RaxSignupAPI_GetSignupSteps_Positive(RaxSignupAPI_BaseFixture):

    us_cloud_signup = RaxSignupAPI_CloudSignupFixture
    uk_cloud_signup = RaxSignupAPI_CloudSignupFixture_UK
    us_trusted_signup = RaxSignupAPI_TrustedCloudSignupFixture
    uk_trusted_signup = RaxSignupAPI_TrustedCloudSignupFixture_UK
    email_apps_signup = RaxSignupAPI_EmailAndAppsSignupFixture

    def common_positive_steps(self, signup_id, params,
                              expected_status_code=200):
        """
        To process the request based on the parameters passed and to check the
        response code
        """
        api_response = self.client.signup_steps(signup_id=signup_id,
                                                params=params)
        self.assertEqual(api_response.status_code, expected_status_code,
                         'Returned a {0} but expected {1}'.format(
                         api_response.status_code, expected_status_code))
        return api_response

    def test_get_signup_steps_with_signup_id_of_us_cloud_signup(self):
        """
        Scenario: Get the details of Signup Steps with Signup ID of US Cloud
        Signup
        """
        request_dict = self.us_cloud_signup.get_signup_request_dict()
        account_type = Account_Type.Cloud

        api_response = self.signup_post_calls(request_dict, account_type)
        signup_id = self.get_marker(api_response)
        params = None

        self.common_positive_steps(signup_id, params)

    def test_get_signup_steps_with_signup_id_of_uk_cloud_signup(self):
        """
        Scenario: Get the details of Signup Steps with Signup ID of UK Cloud
        Signup
        """
        request_dict = self.uk_cloud_signup.get_signup_request_dict()
        account_type = Account_Type.Cloud

        api_response = self.signup_post_calls(request_dict, account_type)
        signup_id = self.get_marker(api_response)
        params = None

        self.common_positive_steps(signup_id, params)

    def test_get_signup_steps_with_signup_id_of_us_trusted_cloud_signup(self):
        """
        Scenario: Get the details of Signup Steps with Signup ID of US Trusted
        Cloud Signup
        """
        request_dict = self.us_trusted_signup.get_signup_request_dict()
        account_type = Account_Type.Trusted_Cloud

        api_response = self.signup_post_calls(request_dict, account_type)
        signup_id = self.get_marker(api_response)
        params = None

        self.common_positive_steps(signup_id, params)

    def test_get_signup_steps_with_signup_id_of_uk_trusted_cloud_signup(self):
        """
        Scenario: Get the details of Signup Steps with Signup ID of UK Trusted
        Cloud Signup
        """
        request_dict = self.uk_trusted_signup.get_signup_request_dict()
        account_type = Account_Type.Trusted_Cloud

        api_response = self.signup_post_calls(request_dict, account_type)
        signup_id = self.get_marker(api_response)
        params = None

        self.common_positive_steps(signup_id, params)

    def test_get_signup_steps_with_signup_id_of_email_apps_signup(self):
        """
        Scenario: Get the details of Signup Steps with Signup ID of Email Apps
        Signup
        """
        request_dict = self.email_apps_signup.get_signup_request_dict()
        account_type = Account_Type.Email_Apps

        api_response = self.signup_post_calls(request_dict, account_type)
        signup_id = self.get_marker(api_response)
        params = None

        self.common_positive_steps(signup_id, params)

    def test_get_signup_steps_with_signup_id_of_us_cloud_signup_based_on_async_as_true(self):
        """
        Scenario: Get the details of Signup Steps with Signup ID of US Cloud
        Signup based on Async as True
        """
        request_dict = self.us_cloud_signup.get_signup_request_dict()
        account_type = Account_Type.Cloud

        api_response = self.signup_post_calls(request_dict, account_type)
        signup_id = self.get_marker(api_response)
        params = {'async': True}

        self.common_positive_steps(signup_id, params)

    def test_get_signup_steps_with_signup_id_of_us_cloud_signup_based_on_async_as_false(self):
        """
        Scenario: Get the details of Signup Steps with Signup ID of US Cloud
        Signup based on Async as False
        """
        request_dict = self.us_cloud_signup.get_signup_request_dict()
        account_type = Account_Type.Cloud

        api_response = self.signup_post_calls(request_dict, account_type)
        signup_id = self.get_marker(api_response)
        params = {'async': False}

        self.common_positive_steps(signup_id, params)

    def test_get_signup_steps_with_signup_id_of_uk_cloud_signup_based_on_async_as_true(self):
        """
        Scenario: Get the details of Signup Steps with Signup ID of UK Cloud
        Signup based on Async as True
        """
        request_dict = self.uk_cloud_signup.get_signup_request_dict()
        account_type = Account_Type.Cloud

        api_response = self.signup_post_calls(request_dict, account_type)
        signup_id = self.get_marker(api_response)
        params = {'async': True}

        self.common_positive_steps(signup_id, params)

    def test_get_signup_steps_with_signup_id_of_uk_cloud_signup_based_on_async_as_false(self):
        """
        Scenario: Get the details of Signup Steps with Signup ID of UK Cloud
        Signup based on Async as False
        """
        request_dict = self.uk_cloud_signup.get_signup_request_dict()
        account_type = Account_Type.Cloud

        api_response = self.signup_post_calls(request_dict, account_type)
        signup_id = self.get_marker(api_response)
        params = {'async': False}

        self.common_positive_steps(signup_id, params)

    def test_get_signup_steps_with_signup_id_of_us_trusted_cloud_signup_based_on_async_as_true(self):
        """
        Scenario: Get the details of Signup Steps with Signup ID of US Trusted
        Cloud Signup based on Async as True
        """
        request_dict = self.us_trusted_signup.get_signup_request_dict()
        account_type = Account_Type.Trusted_Cloud

        api_response = self.signup_post_calls(request_dict, account_type)
        signup_id = self.get_marker(api_response)
        params = {'async': True}

        self.common_positive_steps(signup_id, params)

    def test_get_signup_steps_with_signup_id_of_us_trusted_cloud_signup_based_on_async_as_false(self):
        """
        Scenario: Get the details of Signup Steps with Signup ID of US Trusted
        Cloud Signup based on Async as False
        """
        request_dict = self.us_trusted_signup.get_signup_request_dict()
        account_type = Account_Type.Trusted_Cloud

        api_response = self.signup_post_calls(request_dict, account_type)
        signup_id = self.get_marker(api_response)
        params = {'async': False}

        self.common_positive_steps(signup_id, params)

    def test_get_signup_steps_with_signup_id_of_uk_trusted_cloud_signup_based_on_async_as_true(self):
        """
        Scenario: Get the details of Signup Steps with Signup ID of UK Trusted
        Cloud Signup based on Async as True
        """
        request_dict = self.uk_trusted_signup.get_signup_request_dict()
        account_type = Account_Type.Trusted_Cloud

        api_response = self.signup_post_calls(request_dict, account_type)
        signup_id = self.get_marker(api_response)
        params = {'async': True}

        self.common_positive_steps(signup_id, params)

    def test_get_signup_steps_with_signup_id_of_uk_trusted_cloud_signup_based_on_async_as_false(self):
        """
        Scenario: Get the details of Signup Steps with Signup ID of UK Trusted
        Cloud Signup based on Async as False
        """
        request_dict = self.uk_trusted_signup.get_signup_request_dict()
        account_type = Account_Type.Trusted_Cloud

        api_response = self.signup_post_calls(request_dict, account_type)
        signup_id = self.get_marker(api_response)
        params = {'async': False}

        self.common_positive_steps(signup_id, params)

    def test_get_signup_steps_with_signup_id_of_email_apps_signup_based_on_async_as_true(self):
        """
        Scenario: Get the details of Signup Steps with Signup ID of Email Apps
        Signup based on Async as True
        """
        request_dict = self.email_apps_signup.get_signup_request_dict()
        account_type = Account_Type.Email_Apps

        api_response = self.signup_post_calls(request_dict, account_type)
        signup_id = self.get_marker(api_response)
        params = {'async': True}

        self.common_positive_steps(signup_id, params)

    def test_get_signup_steps_with_signup_id_of_email_apps_signup_based_on_async_as_false(self):
        """
        Scenario: Get the details of Signup Steps with Signup ID of Email Apps
        Signup based on Async as False
        """
        request_dict = self.email_apps_signup.get_signup_request_dict()
        account_type = Account_Type.Email_Apps

        api_response = self.signup_post_calls(request_dict, account_type)
        signup_id = self.get_marker(api_response)
        params = {'async': False}

        self.common_positive_steps(signup_id, params)
