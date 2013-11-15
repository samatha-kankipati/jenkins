"""Basic Negative Tests for Rax Auth"""
from ccengine.common.decorators import attr
from testrepo.common.testfixtures.identity.v2_0.identity \
    import UserAdminFixture


class AuthenticationNegativeTest(UserAdminFixture):
    """Basic Smoke Negative Tests - Check HTTP Resoponses"""

    @classmethod
    def setUpClass(cls):
        super(AuthenticationNegativeTest, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        super(AuthenticationNegativeTest, cls).tearDownClass()

    @attr('regression', type='negative')
    def test_base_authentication_username_and_apikey_false_api_key(self):
        auth_resp = self.public_client.authenticate_user_apikey(
                self.config.identity_api.username,
                self.config.identity_api.false_api_key)
        self.assertEqual(auth_resp.status_code, 401,
                msg="Expected response 401 but received  %s" %
                auth_resp.status_code)
        self.assertTrue('Username or api key is invalid.' in auth_resp.content,
                msg="Expecting 'Fault state-inv. api key' but received  %s" %
                auth_resp.content)

    @attr('regression', type='negative')
    def test_base_auth_username_and_apikey_and_tenant_id_false_api_key(self):
        auth_resp = self.public_client.authenticate_user_apikey_tenant_id(
                self.config.identity_api.username,
                self.config.identity_api.false_api_key,
                self.config.compute_api.tenant_id)
        self.assertEqual(auth_resp.status_code, 401,
                msg="Expected response 401 but received  %s" %
                auth_resp.status_code)
        self.assertTrue('Username or api key is invalid.' in auth_resp.content,
                msg="Expecting 'Fault state-inv. api key' but received  %s" %
                auth_resp.content)

    @attr('regression', type='negative')
    def test_base_auth_username_and_password_false_password(self):
        auth_resp = self.public_client.authenticate_user_password(
                self.config.identity_api.username,
                self.config.identity_api.false_password)
        self.assertEqual(auth_resp.status_code, 401,
                msg="Expected response 401 but received  %s" %
                auth_resp.status_code)
        self.assertTrue('Unable to authenticate user with credentials provided'
                in auth_resp.content,
                msg="Expecting 'Fault state-inv. password' but received  %s" %
                auth_resp.content)

    @attr('regression', type='negative')
    def test_base_auth_username_password_tenant_id_false_password(self):
        auth_resp = self.public_client.authenticate_user_password_tenant_id(
                self.config.identity_api.username,
                self.config.identity_api.false_password,
                self.config.compute_api.tenant_id)
        self.assertEqual(auth_resp.status_code, 401,
                msg="Expected response 401 but received  %s" %
                auth_resp.status_code)
        self.assertTrue('Unable to authenticate user with credentials provided'
                in auth_resp.content,
                msg="Expecting 'Fault state-inv. password' but received  %s" %
                auth_resp.content)

    @attr('regression', type='negative')
    def test_base_auth_tenant_id_and_token_false_token(self):
        auth_resp = self.public_client.authenticate_tenantid_and_token(
                self.config.identity_api.tenant_id,
                self.config.identity_api.false_token)
        self.assertEqual(auth_resp.status_code, 404,
                msg="Expected response 404 but received  %s" %
                auth_resp.status_code)
        self.assertTrue('Invalid Token, not found' in auth_resp.content,
                msg="Expecting 'Fault state-inv. token' but received  %s" %
                auth_resp.content)

    @attr('regression', type='negative')
    def test_base_auth_tenant_name_and_token_false_token(self):
        base_resp = self.public_client.get_tenants()
        sample_tenant = base_resp.entity[0]
        auth_resp = self.public_client.authenticate_tenantname_and_token(
                sample_tenant.name,
                self.config.identity_api.false_token)
        self.assertEqual(auth_resp.status_code, 404,
                msg="Expected response 404 but received  %s" %
                auth_resp.status_code)
        self.assertTrue('Invalid Token, not found' in auth_resp.content,
                msg="Expecting 'Fault state-inv. token' but received  %s" %
                auth_resp.content)
