from ccengine.common.tools.datagen import rand_name, random_int
from testrepo.common.testfixtures.identity.v2_0.identity \
    import IdentityAdminFixture
from ccengine.common.decorators import attr


class AdminUsersTest(IdentityAdminFixture):
    @classmethod
    def setUpClass(cls):
        """
        Function to create test bed for all the test. Execute once at the
        beginning of class
        @param cls: class
        """
        super(AdminUsersTest, cls).setUpClass()
        cls.default_username = rand_name('ccadminname')
        cls.default_email = '{0}@{1}'.format(cls.default_username,
                                             'mailtrust.com')
        cls.default_domain_ID = random_int(min_int=100000, max_int=999999)
        cls.default_region = cls.config.identity_api.default_region
        cls.default_status = True
        cls.password = 'Gadmpass8'
        cls.created_user = cls.admin_client.add_user(
            username=cls.default_username,
            email=cls.default_email,
            enabled=cls.default_status,
            domain_id=cls.default_domain_ID,
            password=cls.password,
            default_region=cls.default_region)
        cls.user_id = cls.created_user.entity.id
        cls.public_client.reset_user_api_key(user_id=cls.user_id)

    @classmethod
    def tearDownClass(cls):
        """
        Function to clean up the data after execution of all the tests
        completed. Execute once at the end of all the tests.
        @param cls: class
        """
        cls.admin_client.delete_user(user_id=cls.created_user.entity.id)
        cls.service_client.delete_user_hard(user_id=cls.created_user.entity.id)

    @attr('smoke', type='positive')
    def test_admin_list_users(self):
        """
        Verifies that identity admin can get the list of users
        """
        normal_response_codes = [200, 203]
        list_users = self.public_client.list_users()
        self.assertIn(list_users.status_code, normal_response_codes,
                      msg="Response for list users by Identity admin is not "
                          "in {0}".format(normal_response_codes))

    @attr('smoke', type='positive')
    def test_admin_get_user_by_name(self):
        """
        Verifies that identity admin can get user by username
        """
        normal_response_codes = [200, 203]
        get_user = self.public_client.get_user_by_name(
            name=self.default_username)
        self.assertIn(get_user.status_code, normal_response_codes,
                      msg="Response for get user by name is not in "
                          "{0}".format(normal_response_codes))

    @attr('smoke', type='positive')
    def test_admin_get_user_by_id(self):
        """
        Verifies that identity admin can get user by user ID
        """
        normal_response_codes = [200, 203]
        get_user = self.public_client.get_user_by_id(user_id=self.user_id)
        self.assertIn(get_user.status_code, normal_response_codes,
                      msg="Response for get user by ID is not in "
                          "{0}".format(normal_response_codes))

    @attr('smoke', type='positive')
    def test_admin_add_user_generated_password(self):
        """
        Verifies auto generation of password when no password is provide
        while user creation
        """
        username = rand_name('ccadminname')
        email = '{0}@{1}'.format(username, 'mailtrust.com')
        create_user = self.admin_client.add_user(
            username=username,
            email=email,
            enabled=True,
            domain_id=self.default_domain_ID)
        self.assertEqual(create_user.status_code, 201,
                         msg="Response for add user without password is not "
                             "201.")
        # Delete user after test completion
        self.addCleanup(self.delete_user_permanently,
                        user_id=create_user.entity.id,
                        client=self.admin_client)

    @attr('smoke', type='positive')
    def test_admin_update_user_email(self):
        """
        Verifies that identity admin can update email of user admin
        """
        updated_email = "{0}_{1}".format("updated", self.default_email)
        update_user = self.public_client.update_user(
            user_id=self.user_id,
            username=self.default_username,
            email=updated_email,
            default_region=self.default_region,
            enabled=self.default_status)
        self.assertEqual(update_user.status_code, 200,
                         msg="Response for update user with email is not 200.")
        self.default_email = updated_email

    @attr('smoke', type='positive')
    def test_admin_update_user_username(self):
        """
        Verifies that identity admin can update username of user admin
        """
        updated_username = "{0}_{1}".format("updated", self.default_username)
        update_user = self.public_client.update_user(
            user_id=self.user_id,
            username=updated_username,
            email=self.default_email,
            default_region=self.default_region,
            enabled=self.default_status)
        self.assertEqual(update_user.status_code, 200,
                         msg="Response for update user with username is not "
                             "200.")
        self.default_username = updated_username

    @attr('smoke', type='positive')
    def test_admin_update_user_status(self):
        """
        Verifies that identity admin can update status of user admin
        """
        updated_status = not self.default_status
        update_user = self.public_client.update_user(
            user_id=self.user_id,
            username=self.default_username,
            email=self.default_email,
            default_region=self.default_region,
            enabled=updated_status)
        self.assertEqual(update_user.status_code, 200,
                         msg="Response for update user with status is not 200")
        self.default_status = updated_status

    @attr('smoke', type='positive')
    def test_admin_update_user_email_username_status(self):
        """
        Verifies that identity admin can update username, email and status of
        user admin in one call
        """
        updated_username = "{0}_{1}".format("updated", self.default_username)
        updated_email = "{0}_{1}".format("updated", self.default_email)
        updated_status = not self.default_status
        update_user = self.public_client.update_user(
            user_id=self.user_id,
            username=updated_username,
            email=updated_email,
            default_region=self.default_region,
            enabled=updated_status)
        self.assertEqual(update_user.status_code, 200,
                         msg="Response for update user with username, "
                             "email and status is not 200.")
        self.default_username = updated_username
        self.default_email = updated_email
        self.default_status = updated_status

    @attr('smoke', type='positive')
    def test_admin_create_and_delete_user(self):
        """
        Verifies that user admin can add and delete sub user (default user)
        """
        username = rand_name('ccuseradmin')
        email = '{0}@{1}'.format(username, 'mailtrust.com')
        create_user = self.public_client.add_user(
            username=username,
            email=email,
            enabled=True,
            domain_id=self.default_domain_ID)
        self.assertEqual(create_user.status_code, 201,
                         msg="Response for add user is not 201.")
        delete_user = self.public_client.delete_user(
            user_id=create_user.entity.id)
        self.assertEqual(delete_user.status_code, 204,
                         msg="Response for delete user is not 204.")
        delete_user_hard = self.service_client.delete_user_hard(
            user_id=create_user.entity.id)
        self.assertEqual(delete_user_hard.status_code, 204,
                         msg="Response for delete user hard is not 204.")

    @attr('smoke', type='positive')
    def test_admin_get_accessible_domains(self):
        """
        Verifies that identity admin can get all the accessible domain
        """
        accessible_domains = self.public_client.get_accessible_domains(
            user_id=self.user_id)
        self.assertEqual(accessible_domains.status_code, 200,
                         msg="Response for get accessible domains is not 200.")

    @attr('smoke', type='positive')
    def test_admin_get_accessible_domain_endpoints(self):
        """
        Verifies that identity admin can get endpoints for a domain and user
        """
        add_user_dom = self.admin_client.add_user_to_domain(
            user_id=self.user_id,
            domain_id=self.default_domain_ID)
        self.assertEqual(add_user_dom.status_code, 204,
                         msg="Response for add user to domain is not 204.")

        add_ten_dom = self.admin_client.add_tenant_to_domain(
            domain_id=self.default_domain_ID,
            tenant_id=self.config.identity_api.tenant_id)
        self.assertEqual(add_ten_dom.status_code, 204,
                         msg="Response for add tenant to domain is not 204.")

        domain_endpoints_resp = \
            self.admin_client.get_accessible_domain_endpoints(
                user_id=self.user_id,
                domain_id=self.created_user.entity.domainId)
        self.assertEqual(domain_endpoints_resp.status_code, 200,
                         msg="Response for get accessible domain endpoints "
                             "is not 200.")

    @attr('smoke', type='positive')
    def test_admin_add_credential_to_user(self):
        """
        Verifies that identity admin can add credential to user
        """
        updated_pass = "{0}{1}".format("updated", self.password)
        add_credentials = self.admin_client.add_user_credentials(
            user_id=self.user_id,
            username=self.default_username,
            password=updated_pass)
        self.assertEqual(add_credentials.status_code, 201,
                         msg="Response for add credential to user is not 200.")
        self.password = updated_pass

    @attr('smoke', type='positive')
    def test_admin_list_credentials(self):
        """
        Verifies that identity admin can list all the credentials of user
        """
        list_credentials = self.public_client.list_credentials(
            user_id=self.user_id)
        self.assertEqual(list_credentials.status_code, 200,
                         msg="Response for list credentials for user is not "
                             "200.")
        self.assertIsNotNone(
            list_credentials.entity.apiKeyCredentials.apiKey,
            msg="APIKey is not present in list of credentials.")
        self.assertIsNotNone(
            list_credentials.entity.apiKeyCredentials.username,
            msg="Username is not present in list of credentials.")

    @attr('smoke', type='positive')
    def test_admin_update_and_delete_user_credentials(self):
        """
        Verifies that identity admin can update and delete credential of a user
        """
        username = rand_name('ccadminname')
        email = '{0}@{1}'.format(username, 'mailtrust.com')
        create_user = self.admin_client.add_user(
            username=username,
            email=email,
            enabled=True,
            domain_id=self.default_domain_ID)
        self.assertEqual(create_user.status_code, 201,
                         msg="Response for add user is not 201.")
        # Delete user after test completion
        self.addCleanup(self.delete_user_permanently,
                        user_id=create_user.entity.id,
                        client=self.admin_client)
        updated_api_key = 'aaaaa-bbbbb-ccccc-12345678'
        update_credentials = self.admin_client.update_user_credentials(
            user_id=create_user.entity.id,
            username=username,
            api_key=updated_api_key)
        self.assertEqual(update_credentials.status_code, 200,
                         msg="Response for update user's APIKey is not 200.")
        self.assertEqual(update_credentials.entity.apiKey, updated_api_key,
                         msg="User APIKey is not updated to "
                             "{0}".format(updated_api_key))
        delete_credentials = self.admin_client.delete_user_credentials(
            user_id=self.user_id)
        self.assertEqual(delete_credentials.status_code, 204,
                         msg="Response for delete user's APIKey is not 204.")

    @attr('smoke', type='positive')
    def test_admin_get_user_credentials(self):
        """
        Verifies that identity admin can get credential of a user
        """
        get_credentials = self.admin_client.get_user_credentials(
            user_id=self.user_id)
        self.assertEqual(get_credentials.status_code, 200,
                         msg="Response for get user credentials is not 200.")

    @attr('smoke', type='positive')
    def test_admin_reset_user_api_key(self):
        """
        Verifies that identity admin can reset user admins api_key
        """
        reset_api_key = self.public_client.reset_user_api_key(
            user_id=self.user_id)
        self.assertEqual(reset_api_key.status_code, 200,
                         msg="Response for reset user api_key is not 200.")
