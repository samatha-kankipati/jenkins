from testrepo.common.testfixtures.identity.v2_0.identity \
    import IdentityAdminFixture
from ccengine.common.decorators import attr


class AdminTokenTest(IdentityAdminFixture):

    @classmethod
    def setUpClass(cls):
        super(AdminTokenTest, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        pass

    @attr('smoke', type='positive')
    def test_validate_token(self):
        normal_response_codes = [200, 203]
        auth_resp = self.public_client.authenticate_user_apikey(
                self.config.identity_api.username,
                self.config.identity_api.api_key)

        self.assertEqual(auth_resp.status_code, 200,
                msg="Expected response 200 received response %s" %
                auth_resp.status_code)

        token = auth_resp.entity.token.id
        token_resp = self.admin_client.validate_token(
                tokenId=token)

        self.assertEqual(token_resp.status_code, 200,
                msg="Expected response 200 received response %s" %
                token_resp.status_code)

    @attr('smoke', type='positive')
    def test_validate_token_belongs_to(self):
        '''TODO: add belongs to'''
        normal_response_codes = [200, 203]
        auth_resp = self.public_client.authenticate_user_apikey(
                self.config.identity_api.username,
                self.config.identity_api.api_key)

        self.assertEqual(auth_resp.status_code, 200,
                msg="Expected response 200 received response %s" %
                auth_resp.status_code)

        token = auth_resp.entity.token.id
        token_resp = self.admin_client.validate_token(
                tokenId=token,
                belongsTo=self.config.identity_api.tenant_id)

        self.assertEqual(token_resp.status_code, 200,
                msg="Expected response 200 received response %s" %
                token_resp.status_code)

    @attr('smoke', type='positive')
    def test_check_token(self):
        auth_resp = self.public_client.authenticate_user_apikey(
                self.config.identity_api.username,
                self.config.identity_api.api_key)
        self.assertEqual(auth_resp.status_code, 200,
                msg="Expected response 200 received response %s" %
                auth_resp.status_code)
        token = auth_resp.entity.token.id
        token_resp = self.admin_client.check_token(
                tokenId=token)
        self.assertEqual(token_resp.status_code, 200,
                msg="Expected response 200 received response %s" %
                token_resp.status_code)

    @attr('smoke', type='positive')
    def test_list_endpoints_for_token(self):
        auth_resp = self.public_client.authenticate_user_apikey(
                self.config.identity_api.username,
                self.config.identity_api.api_key)
        self.assertEqual(auth_resp.status_code, 200,
                msg="Expected response 200 received response %s" %
                auth_resp.status_code)
        token = auth_resp.entity.token.id
        token_resp = \
                self.admin_client.list_endpoints_for_token(
                        tokenId=token)
        self.assertEqual(token_resp.status_code, 200,
                msg="Expected response 200 received response %s" %
                token_resp.status_code)
        self.assertTrue(token_resp.entity[0] is not None,
                msg="At least one role is present is present")
