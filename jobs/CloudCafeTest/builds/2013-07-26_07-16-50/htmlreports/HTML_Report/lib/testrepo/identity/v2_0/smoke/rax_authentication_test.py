from testrepo.common.testfixtures.identity.v2_0.identity \
    import BaseIdentityFixture
from ccengine.common.decorators import attr


class AuthenticationTest(BaseIdentityFixture):

    @classmethod
    def setUpClass(cls):
        super(AuthenticationTest, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        pass

    @attr('smoke', type='positive')
    def test_base_authentication_username_and_api_key(self):
        normal_response_codes = [200, 203]
        auth_resp = self.public_client.authenticate_user_apikey(
                self.config.identity_api.username,
                self.config.identity_api.api_key)

        self.assertIn(
                auth_resp.status_code,
                normal_response_codes,
                msg="Expected response {0} received response {1}".
                format(normal_response_codes, auth_resp.status_code))

    @attr('smoke', type='positive')
    def test_base_authentication_username_api_key_and_tenant_id(self):
        normal_response_codes = [200, 203]
        auth_resp = self.public_client.authenticate_user_apikey_tenant_id(
                self.config.identity_api.username,
                self.config.identity_api.api_key,
                self.config.compute_api.tenant_id)

        self.assertIn(
                auth_resp.status_code,
                normal_response_codes, 
                msg="Expected response {0} received response {1}".
                format(normal_response_codes, auth_resp.status_code))

    @attr('smoke', type='positive')
    def test_base_authentication_username_and_password(self):
        normal_response_codes = [200, 203]
        auth_resp = self.public_client.authenticate_user_password(
                self.config.identity_api.username,
                self.config.identity_api.password)

        self.assertIn(
                auth_resp.status_code,
                normal_response_codes, 
                msg="Expected response {0} received response {1}".
                format(normal_response_codes, auth_resp.status_code))

    @attr('smoke', type='positive')
    def test_base_authentication_username_password_and_tenant_id(self):
        normal_response_codes = [200, 203]
        auth_resp = self.public_client.authenticate_user_password_tenant_id(
                self.config.identity_api.username,
                self.config.identity_api.password,
                self.config.compute_api.tenant_id)

        self.assertIn(
                auth_resp.status_code,
                normal_response_codes, 
                msg="Expected response {0} received response {1}".
                format(normal_response_codes, auth_resp.status_code))

    @attr('smoke', type='positive')
    def test_base_authentication_tenant_id_and_token(self):
        normal_response_codes = [200, 203]
        base_resp = self.public_client.authenticate_user_apikey(
                self.config.identity_api.username,
                self.config.identity_api.api_key)

        auth_resp = self.public_client.authenticate_tenantid_and_token(
                self.config.identity_api.tenant_id,
                base_resp.entity.token.id)

        self.assertIn(
                auth_resp.status_code,
                normal_response_codes, 
                msg="Expected response {0} received response {1}".
                format(normal_response_codes, auth_resp.status_code))

    @attr('smoke', type='positive')
    def test_base_authentication_tenant_name_and_token(self):
        normal_response_codes = [200, 203]
        token_resp = self.public_client.authenticate_user_apikey(
                self.config.identity_api.username,
                self.config.identity_api.api_key)
        self.public_client.token = token_resp.entity.token.id
        base_resp = self.public_client.get_tenants()
        del self.public_client.token
        sample_tenant = base_resp.entity[0]

        auth_resp = self.public_client.authenticate_tenantname_and_token(
                sample_tenant.name,
                token_resp.entity.token.id)

        self.assertIn(
                auth_resp.status_code,
                normal_response_codes,
                msg="Expected response {0} received response {1}".
                format(normal_response_codes, auth_resp.status_code))
