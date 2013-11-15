# for vim, xgettext and similar utilities to recognize character encodings
# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8
from ccengine.common.decorators import attr
from ccengine.common.tools.datagen import rand_name, random_int
from testrepo.common.testfixtures.identity.v2_0.identity \
    import BaseIdentityFixture
from ccengine.common.constants.identity import HTTPResponseCodes

class TokenValidationTests(BaseIdentityFixture):
    @classmethod
    def setUpClass(cls):
        """
        Unittest method to setup the testbed before actual test begin
        """
        super(TokenValidationTests, cls).setUpClass()
        cls.identity_admin_username = rand_name("ccidentityadmin")
        identity_admin_email = "{0}@{1}".format(cls.identity_admin_username,
                                                "mailtrust.com")
        cls.password = "Gellpass8"
        cls.create_iden_admin_resp = cls.service_client.add_user(
            username=cls.identity_admin_username, password=cls.password,
            email=identity_admin_email, enabled=True)
        cls.admin_client.token = cls.provider.get_token(
            username=cls.identity_admin_username,
            password=cls.password)

        # Creating user admin
        domain_id = random_int(10000, 1000000)
        cls.user_admin_username = rand_name("ccuseradmin")
        user_admin_email = "{0}@{1}".format(cls.user_admin_username,
                                            "mailtrust.com")
        cls.create_user_admin_resp = cls.admin_client.add_user(
            username=cls.user_admin_username, password=cls.password,
            email=user_admin_email, enabled=True, domain_id=domain_id)
        cls.public_client.token = cls.provider.get_token(
            username=cls.user_admin_username,
            password=cls.password)
        del cls.admin_client.token

        # Creating Sub User
        cls.sub_user_username = rand_name("ccsubusername")
        sub_user_email = "{0}@{1}".format(cls.sub_user_username,
                                          "mailtrust.com")
        cls.create_sub_user_resp = cls.public_client.add_user(
            username=cls.sub_user_username, password=cls.password,
            email=sub_user_email, enabled=True)
        del cls.public_client.token

    @classmethod
    def tearDownClass(cls):
        """
        Unittest method to teardown the testbed after test execution
        """
        cls.service_client.delete_user(cls.create_sub_user_resp.entity.id)
        cls.service_client.delete_user_hard(
            cls.create_sub_user_resp.entity.id)
        cls.service_client.delete_user(cls.create_user_admin_resp.entity.id)
        cls.service_client.delete_user_hard(
            cls.create_user_admin_resp.entity.id)
        cls.service_client.delete_user(cls.create_iden_admin_resp.entity.id)
        cls.service_client.delete_user_hard(
            cls.create_iden_admin_resp.entity.id)

    @attr("regression", type="negative")
    def test_token_validation_with_invalid_identity_token(self):
        """
        Verifies that Identity admin with invalid token,
        can not validate active token of User Admin
        """
        iden_admin_token = self.provider.get_token(
            username=self.identity_admin_username,
            password=self.password)
        # Adding token for clean up
        self.addCleanup(self.service_client.revoke_token,
                        token_id=iden_admin_token)
        self.admin_client.token = iden_admin_token

        user_admin_token = self.provider.get_token(
            username=self.user_admin_username,
            password=self.password)
        # Adding token for clean up
        self.addCleanup(self.service_client.revoke_token,
                        token_id=user_admin_token)
        self.admin_client.token = "Invalidtoken1234"

        validate_user_admin_token_resp = self.admin_client.validate_token(
            token_id=user_admin_token)
        self.assertEqual(validate_user_admin_token_resp.status_code,
                         HTTPResponseCodes.INVALID_TOKEN,
                         msg="Response for validate token with invalid "
                             "identity admin token is not {0}.".format(
                             HTTPResponseCodes.INVALID_TOKEN))
        self.assertIn('"message":"No valid token provided. Please use the '
                      '\'X-Auth-Token\' header with a valid token."',
                      validate_user_admin_token_resp._content)

    @attr("regression", type="negative")
    def test_token_validation_with_valid_expired_identity_token(self):
        """
        Verifies that Identity admin with expired token,
        can not validate active token of User Admin
        """
        iden_admin_token = self.provider.get_token(
            username=self.identity_admin_username,
            password=self.password)
        self.admin_client.token = iden_admin_token
        user_admin_token = self.provider.get_token(
            username=self.user_admin_username,
            password=self.password)
        # Adding token for clean up
        self.addCleanup(self.service_client.revoke_token,
                        token_id=user_admin_token)
        revoke_identity_admin_token_resp = self.service_client.revoke_token(
            token_id=iden_admin_token)
        self.assertEqual(revoke_identity_admin_token_resp.status_code,
                         HTTPResponseCodes.UPDATE_SUCCESSFUL,
                         msg="Response for revoke token is not {0}.".format(
                             HTTPResponseCodes.UPDATE_SUCCESSFUL))
        validate_user_admin_token_resp = self.admin_client.validate_token(
            token_id=user_admin_token)
        self.assertEqual(validate_user_admin_token_resp.status_code,
                         HTTPResponseCodes.UNAUTHORIZED,
                         msg="Response for validate token with expired "
                             "identity admin token is not {0}.".format(
                             HTTPResponseCodes.UNAUTHORIZED))
        self.assertIn('"message":"No valid token provided',
                      validate_user_admin_token_resp._content)

    @attr("regression", type="positive")
    def test_token_validation_for_valid_sub_user_token(self):
        """
        Verifies that Identity Admin with valid token should get the positive
        (200) response for valid sub user token
        """
        iden_admin_token = self.provider.get_token(
            username=self.identity_admin_username,
            password=self.password)
        self.admin_client.token = iden_admin_token
        # Adding token for clean up
        self.addCleanup(self.service_client.revoke_token,
                        token_id=iden_admin_token)

        sub_user_token = self.provider.get_token(
            username=self.sub_user_username,
            password=self.password)
        # Adding token for clean up
        self.addCleanup(self.service_client.revoke_token,
                        token_id=sub_user_token)

        validate_sub_user_token_resp = self.admin_client.validate_token(
            token_id=sub_user_token)
        self.assertEqual(validate_sub_user_token_resp.status_code,
                         HTTPResponseCodes.SUCCESS,
                         msg="Response for validate token with valid "
                             "identity admin token is not {0}.".format(
                             HTTPResponseCodes.SUCCESS))

    @attr("regression", type="positive")
    def test_token_validation_for_invalid_sub_user_token(self):
        """
        Verifies that Identity Admin with valid token should get the negative
        (404) response for invalid sub user token
        """
        iden_admin_token = self.provider.get_token(
            username=self.identity_admin_username,
            password=self.password)
        self.admin_client.token = iden_admin_token
        # Adding token for clean up
        self.addCleanup(self.service_client.revoke_token,
                        token_id=iden_admin_token)

        sub_user_token = "invalidtoken1234"
        validate_sub_user_token_resp = self.admin_client.validate_token(
            token_id=sub_user_token)
        self.assertEqual(validate_sub_user_token_resp.status_code,
                         HTTPResponseCodes.NOT_FOUND,
                         msg="Response for validate invalid token with valid "
                             "identity admin token is not {0}.".format(
                             HTTPResponseCodes.NOT_FOUND))
        self.assertIn('"message":"Token not found."',
                      validate_sub_user_token_resp._content)

    @attr("regression", type="positive")
    def test_token_validation_for_expired_sub_user_token(self):
        """
        Verifies that Identity Admin with valid token should get the negative
        (404) response for expired sub user token
        """
        iden_admin_token = self.provider.get_token(
            username=self.identity_admin_username,
            password=self.password)
        self.admin_client.token = iden_admin_token
        # Adding token for clean up
        self.addCleanup(self.service_client.revoke_token,
                        token_id=iden_admin_token)

        sub_user_token = self.provider.get_token(
            username=self.sub_user_username,
            password=self.password)
        revoke_sub_user_token_resp = self.admin_client.revoke_token(
            token_id=sub_user_token)
        self.assertEqual(revoke_sub_user_token_resp.status_code,
                         HTTPResponseCodes.UPDATE_SUCCESSFUL,
                         msg="Response for revoke token is not {0}.".format(
                             HTTPResponseCodes.UPDATE_SUCCESSFUL))
        validate_sub_user_token_resp = self.admin_client.validate_token(
            token_id=sub_user_token)
        self.assertEqual(validate_sub_user_token_resp.status_code,
                         HTTPResponseCodes.NOT_FOUND,
                         msg="Response for validate expired token with valid "
                             "identity admin token is not {0}.".format(
                             HTTPResponseCodes.NOT_FOUND))
        self.assertIn('"message":"Token not found"',
                      validate_sub_user_token_resp._content)
