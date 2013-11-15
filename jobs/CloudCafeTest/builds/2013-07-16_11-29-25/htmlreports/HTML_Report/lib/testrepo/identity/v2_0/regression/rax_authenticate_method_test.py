from ccengine.common.tools.datagen import rand_name
from ccengine.common.tools.datagen import random_int
from testrepo.common.testfixtures.identity.v2_0.identity \
        import BaseIdentityFixture
from ccengine.common.decorators import attr


class AuthenticationMethodTest(BaseIdentityFixture):

    @classmethod
    def _add_user(cls, username, enabled=True, domainId=None, token=None):
        '''
        @sumamry: Wraps the add_user method to handle token swapping.
        Ensures that token is always the same pre and post method call
        regardless of token used.
        '''
        username = rand_name(username)

        tmpToken = cls.admin_client.token
        if token:
            cls.admin_client.token = token

        user = cls.admin_client.add_user(
                username=username,
                email=cls.email_format_string.format(username, 'test.com'),
                enabled=enabled,
                domainId=domainId,
                password=cls.password).entity

        cls.admin_client.token = tmpToken
        return user

    @classmethod
    def _get_token(cls, username, password):
        return cls.service_client.authenticate_user_password(
                username,
                password).entity.token.id

    @classmethod
    def setUpClass(cls):
        super(AuthenticationMethodTest, cls).setUpClass()
        '''
        @sumamry: Create root users required by test suite
        '''

        cls.email_format_string = '{0}@{1}'
        cls.password = 'Password1'
        cls.err_msg = 'AuthenticatedBy - Received: {0}, Expected: {1}'
        cls.apikey = 'thisisanapikey'

        cls.serviceAdminToken = cls._get_token(
            cls.config.identity_api.service_username,
            cls.config.identity_api.service_password)
        cls.service_client.token = cls.serviceAdminToken

        cls.identityAdmin = cls._add_user('ccIdentityAdmin', token=cls.serviceAdminToken)
        cls.service_client.update_user_credentials(cls.identityAdmin.id,
                                                    cls.identityAdmin.username,
                                                    cls.apikey)

    @classmethod
    def _destroy_user(cls, userId):
        cls.admin_client.delete_user(userId=userId)
        cls.service_client.delete_user_hard(userId=userId)

    @classmethod
    def tearDownClass(cls):
        cls._destroy_user(cls.identityAdmin.id)


    def _revoke_token(self):
        token = self.admin_client.authenticate_user_password(
                self.identityAdmin.username,
                self.password).entity.token.id

        self.service_client.revoke_token(token)

    @attr('regression', type='positive')
    def test_verify_password_authentication_method_in_auth_response(self):
        '''
        @summary: verify password authentication method in auth response
        '''
        self._revoke_token()
        auth_by = self.admin_client.authenticate_user_password(
            self.identityAdmin.username,
            self.password).entity.token.authenticatedBy
        self.assertEqual(auth_by[0],
                         'PASSWORD',
                         msg=self.err_msg.format(auth_by[0], 'PASSWORD'))

    @attr('regression', type='positive')
    def test_verify_password_authentication_method_in_validate_response(self):
        '''
        @summary: verify password authentication method in validate response
        '''
        self._revoke_token()
        token = self.admin_client.authenticate_user_password(
                self.identityAdmin.username,
                self.password).entity.token.id

        auth_by = self.service_client.validate_token(token).entity.token.authenticatedBy
        self.assertEqual(auth_by[0],
                         'PASSWORD',
                         msg=self.err_msg.format(auth_by[0], 'PASSWORD'))

    @attr('regression', type='positive')
    def test_verify_apikey_authentication_method_in_auth_response(self):
        '''
        @summary: verify apikey authentication method in auth response
        '''
        self._revoke_token()
        auth_by = self.admin_client.authenticate_user_apikey(
                self.identityAdmin.username,
                self.apikey).entity.token.authenticatedBy
        self.assertEqual(auth_by[0],
                         'APIKEY',
                         msg=self.err_msg.format(auth_by[0], 'APIKEY'))

    @attr('regression', type='positive')
    def test_verify_apikey_authentication_method_in_validate_response(self):
        '''
        @summary: verify apikey authentication method in validate response
        '''
        self._revoke_token()
        token = self.admin_client.authenticate_user_apikey(
                self.identityAdmin.username,
                self.apikey).entity.token.id

        auth_by = self.service_client.validate_token(token).entity.token.authenticatedBy
        self.assertEqual(auth_by[0],
                         'APIKEY',
                         msg=self.err_msg.format(auth_by[0], 'APIKEY'))

