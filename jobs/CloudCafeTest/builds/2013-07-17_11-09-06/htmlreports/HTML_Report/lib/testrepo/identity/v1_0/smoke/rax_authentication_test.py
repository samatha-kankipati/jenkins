from testrepo.common.testfixtures.identity.v1_0.identity \
    import BaseIdentityFixture
from ccengine.common.decorators import attr


class AuthenticationTest(BaseIdentityFixture):

    @classmethod
    def setUpClass(cls):
        super(AuthenticationTest, cls).setUpClass()
        #cls.datetime = datetime
        #cls.default_token_length = 32
        cls.username = cls.config.identity_api.username
        cls.api_key = cls.config.identity_api.api_key

    @classmethod
    def tearDownClass(cls):
        pass

    @attr('smoke', type='positive')
    def test_base_authentication_username_and_key(self):
        normal_response_codes = [200, 204]
        auth_resp = self.client.authenticate(
            x_auth_user=self.username,
            x_auth_key=self.api_key)

        self.assertIn(auth_resp.status_code, normal_response_codes,
            msg= 'Get base URLs expected {0} received {1}'.format(
                normal_response_codes, 
                auth_resp.status_code))
    
    @attr('smoke', type='positive')
    def test_base_authentication_username_and_key_storage(self):
        normal_response_codes = [200, 204]
        auth_resp = self.client.authenticate_storage(
            x_storage_user=self.username,
            x_storage_pass=self.api_key)

        self.assertIn(auth_resp.status_code, normal_response_codes,
            msg= 'Get base URLs expected {0} received {1}'.format(
                normal_response_codes, 
                auth_resp.status_code))