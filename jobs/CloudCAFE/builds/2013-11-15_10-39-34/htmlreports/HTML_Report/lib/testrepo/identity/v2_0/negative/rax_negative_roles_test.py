from ccengine.common.tools.datagen import rand_name
from ccengine.common.tools.datagen import random_int
from testrepo.common.testfixtures.identity.v2_0.identity \
    import BaseIdentityFixture
from ccengine.common.decorators import attr


class RolesTest(BaseIdentityFixture):
    @classmethod
    def _add_user(cls, username, enabled=True, domain_id=None, token=None):
        username = rand_name(username)
        tmp_token = cls.admin_client.token
        if token:
            cls.admin_client.token = token

        user = cls.admin_client.add_user(
            username=username,
            email=cls.email_format_string.format(username, 'test.com'),
            enabled=enabled,
            domain_id=domain_id,
            password=cls.password).entity
        cls.admin_client.token = tmp_token
        return user

    @classmethod
    def _get_token(cls, username, password):
        return cls.service_client.authenticate_user_password(
            username,
            password).entity.token.id

    @classmethod
    def setUpClass(cls):
        super(RolesTest, cls).setUpClass()
        '''
        @sumamry: Create root users required by test suite
        '''

        cls.err_msg = 'Response received: {0}; Response expected: {1}'
        cls.email_format_string = '{0}@{1}'
        cls.password = 'Password1'
        cls.service_admin_token = cls._get_token(
            cls.config.identity_api.service_username,
            cls.config.identity_api.service_password)

        cls.domain_one = 'domain{0}'.format(random_int(10000, 1000000000))
        cls.identity_admin = cls._add_user('ccIdentityAdmin',
                                          token=cls.service_admin_token)
        cls.identity_admin_token = cls._get_token(cls.identity_admin.username,
                                                cls.password)

        cls.user_admin = cls._add_user('ccUserAdmin',
                                      domain_id=cls.domain_one,
                                      token=cls.identity_admin_token)
        cls.user_admin_token = cls._get_token(cls.user_admin.username,
                                            cls.password)

        cls.sub_user = cls._add_user('ccSubUser',
                                    token=cls.user_admin_token)
        cls.sub_user_token = cls._get_token(cls.sub_user.username,
                                          cls.password)

    @classmethod
    def tearDownClass(cls):
        cls.delete_user_permanently(user_id=cls.sub_user.id,
                                    client=cls.public_client)
        cls.delete_user_permanently(user_id=cls.user_admin.id,
                                    client=cls.admin_client)
        cls.delete_user_permanently(user_id=cls.identity_admin.id,
                                    client=cls.service_client)

    def _wrap_role_delete(self, role_id, token=None):
        """
        @summary: Wraps role deletion and handles the token
        swapping on the client.
        """
        if not token:
            token = self.service_admin_token
        tmp_token = self.admin_client.token
        self.admin_client.token = token

        response = self.admin_client.delete_role(role_id)
        self.admin_client.token = tmp_token
        return response

    @attr('regression', type='negative')
    def test_defaultUserRole_cannot_be_deleted_by_service_admin(self):
        """
        @summary: defaultUserRole cannot be deleted by service admin
        """

        response = self._wrap_role_delete(
            self.config.identity_api.defaultUserRoleId)
        self.assertEqual(response.status_code,
                         403,
                         msg=self.err_msg.format(response.status_code, 403))

    @attr('regression', type='negative')
    def test_userAdminRole_cannot_be_deleted_by_service_admin(self):
        """
        @summary: userAdminRole cannot be deleted by service admin
        """
        response = self._wrap_role_delete(
            self.config.identity_api.userAdminRoleId)
        self.assertEqual(response.status_code,
                         403,
                         msg=self.err_msg.format(response.status_code, 403))

    @attr('regression', type='negative')
    def test_identityAdminRole_cannot_be_deleted_by_service_admin(self):
        """
        @summary: identityAdminRole cannot be deleted by service admin
        """
        response = self._wrap_role_delete(
            self.config.identity_api.identityAdminRoleId)
        self.assertEqual(response.status_code,
                         403,
                         msg=self.err_msg.format(response.status_code, 403))

    @attr('regression', type='negative')
    def test_serviceAdminRole_cannot_be_deleted_by_service_admin(self):
        """
        @summary: serviceAdminRole cannot be deleted by service admin
        """
        response = self._wrap_role_delete(
            self.config.identity_api.serviceAdminRoleId)
        self.assertEqual(response.status_code,
                         403,
                         msg=self.err_msg.format(response.status_code, 403))

    @attr('regression', type='negative')
    def test_defaultUserRole_cannot_be_deleted_by_identity_admin(self):
        """
        @summary: test_defaultUserRole_cannot_be_deleted_by_identity_admin
        """
        response = self._wrap_role_delete(
            self.config.identity_api.defaultUserRoleId)
        self.assertEqual(response.status_code,
                         403,
                         msg=self.err_msg.format(response.status_code, 403))

    @attr('regression', type='negative')
    def test_userAdminRole_cannot_be_deleted_by_identity_admin(self):
        """
        @summary: userAdminRole cannot be deleted by identity admin
        """
        response = self._wrap_role_delete(
            self.config.identity_api.userAdminRoleId)
        self.assertEqual(response.status_code,
                         403,
                         msg=self.err_msg.format(response.status_code, 403))

    @attr('regression', type='negative')
    def test_identityAdminRole_cannot_be_deleted_by_identity_admin(self):
        """
        @summary: identityAdminRole cannot be deleted by identity admin
        """
        response = self._wrap_role_delete(
            self.config.identity_api.identityAdminRoleId)
        self.assertEqual(response.status_code,
                         403,
                         msg=self.err_msg.format(response.status_code, 403))

    @attr('regression', type='negative')
    def test_serviceAdminRole_cannot_be_deleted_by_identity_admin(self):
        """
        @summary: serviceAdminRole cannot be deleted by identity admin
        """
        response = self._wrap_role_delete(
            self.config.identity_api.serviceAdminRoleId)
        self.assertEqual(response.status_code,
                         403,
                         msg=self.err_msg.format(response.status_code, 403))

    @attr('regression', type='negative')
    def test_defaultUserRole_cannot_be_deleted_by_user_admin(self):
        """
        @summary: defaultUserRole cannot be deleted by user admin
        """
        response = self._wrap_role_delete(
            self.config.identity_api.defaultUserRoleId)
        self.assertEqual(response.status_code,
                         403,
                         msg=self.err_msg.format(response.status_code, 403))

    @attr('regression', type='negative')
    def test_userAdminRole_cannot_be_deleted_by_user_admin(self):
        """
        @summary: userAdminRole cannot be deleted by user admin
        """
        response = self._wrap_role_delete(
            self.config.identity_api.userAdminRoleId)
        self.assertEqual(response.status_code,
                         403,
                         msg=self.err_msg.format(response.status_code, 403))

    @attr('regression', type='negative')
    def test_identityAdminRole_cannot_be_deleted_by_user_admin(self):
        """
        @summary: identityAdminRole cannot be deleted by user admin
        """
        response = self._wrap_role_delete(
            self.config.identity_api.identityAdminRoleId)
        self.assertEqual(response.status_code,
                         403,
                         msg=self.err_msg.format(response.status_code, 403))

    @attr('regression', type='negative')
    def test_serviceAdminRole_cannot_be_deleted_by_user_admin(self):
        """
        @summary: serviceAdminRole cannot be deleted by user admin
        """
        response = self._wrap_role_delete(
            self.config.identity_api.serviceAdminRoleId)
        self.assertEqual(response.status_code,
                         403,
                         msg=self.err_msg.format(response.status_code, 403))

    @attr('regression', type='negative')
    def test_defaultUserRole_cannot_be_deleted_by_default_user(self):
        """
        @summary: defaultUserRole cannot be deleted by default user
        """
        response = self._wrap_role_delete(
            self.config.identity_api.defaultUserRoleId)
        self.assertEqual(response.status_code,
                         403,
                         msg=self.err_msg.format(response.status_code, 403))

    @attr('regression', type='negative')
    def test_userAdminRole_cannot_be_deleted_by_default_user(self):
        """
        @summary: userAdminRole cannot be deleted by default user
        """
        response = self._wrap_role_delete(
            self.config.identity_api.userAdminRoleId)
        self.assertEqual(response.status_code,
                         403,
                         msg=self.err_msg.format(response.status_code, 403))

    @attr('regression', type='negative')
    def test_identityAdminRole_cannot_be_deleted_by_default_user(self):
        """
        @summary: identityAdminRole cannot be deleted by default user
        """
        response = self._wrap_role_delete(
            self.config.identity_api.identityAdminRoleId)
        self.assertEqual(response.status_code,
                         403,
                         msg=self.err_msg.format(response.status_code, 403))

    @attr('regression', type='negative')
    def test_serviceAdminRole_cannot_be_deleted_by_default_user(self):
        """
        @summary: serviceAdminRole cannot be deleted by default user
        """
        response = self._wrap_role_delete(
            self.config.identity_api.serviceAdminRoleId)
        self.assertEqual(response.status_code,
                         403,
                         msg=self.err_msg.format(response.status_code, 403))
