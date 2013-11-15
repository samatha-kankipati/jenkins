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
        @param cls: instance of class
        """
        super(AdminUsersTest, cls).setUpClass()
        cls.username = rand_name("ccuseradmin")
        cls.email = "{0}@{1}".format(cls.username, "mailtrust.com")
        cls.domain_id = random_int(10000, 1000000000)
        cls.default_region = cls.config.identity_api.default_region
        cls.password = "Gadmpass8"
        cls.created_user = cls.admin_client.add_user(
            default_region=cls.default_region,
            username=cls.username,
            domain_id=cls.domain_id,
            password=cls.password,
            email=cls.email,
            enabled=True)
        cls.user_id = cls.created_user.entity.id
        cls.public_client.token = cls.provider.get_token(
            username=cls.username,
            password=cls.password)
        cls.public_client.reset_user_api_key(user_id=cls.user_id)

    @classmethod
    def tearDownClass(cls):
        """
        Function to clean up the data after execution of all the tests
        completed. Execute once at the end of all the tests.
        @param cls: instance of class
        """
        cls.delete_user_permanently(user_id=cls.created_user.entity.id,
                                    client=cls.admin_client)

    def _add_user_by_identity_admin(self):
        """
        Function to add user admin using default data.
        @return Add User Response and User Info
        """
        username = rand_name("ccuseradmin")
        email = "{0}@{1}".format(username, "mailtrust.com")
        created_user = self.admin_client.add_user(
            default_region=self.default_region,
            username=username,
            domain_id=self.domain_id,
            password=self.password,
            email=email,
            enabled=True)
        self.assertEqual(created_user.status_code, 201,
                         msg="Response to create user admin is not 201.")
        return created_user

    @attr('regression', type='positive')
    def test_list_users_by_identity_admin(self):
        """
        Verifies that identity admin can get list of users
        """
        list_users = self.admin_client.list_users()
        self.assertEqual(list_users.status_code, 200,
                         msg="Response for list users by identity admin is not"
                             " 200.")
        self.assertGreaterEqual(len(list_users.entity), 0,
                                msg="List users call returned empty list.")
        self.assertIsNotNone(list_users.entity[0].id,
                             msg="Id for first user in list is None.")

    @attr('regression', type='positive')
    def test_get_user_by_name_using_identity_admin(self):
        """
        Verifies that identity admin can get user by username
        """
        get_user = self.admin_client.get_user_by_name(name=self.username)
        self.assertEqual(get_user.status_code, 200,
                         msg="Response for get user by name using identity "
                             "admin is not 200.")
        self.assertEqual(get_user.entity.username, self.username,
                         msg="Username did not match with username ({0}) used "
                             "for search.".format(self.username))
        self.assertTrue(get_user.entity.enabled,
                        msg="User is not in enabled state.")

    @attr('regression', type='positive')
    def test_get_user_by_id_using_identity_admin(self):
        """
        Verifies that identity admin can get user by ID
        """
        get_user = self.admin_client.get_user_by_id(user_id=self.user_id)
        self.assertEqual(get_user.status_code, 200,
                         msg="Response for get user by ID using identity "
                             "admin is not 200.")
        self.assertEqual(get_user.entity.id, self.user_id,
                         msg="User ID did not match with ID ({0}) used for "
                             "search.".format(self.user_id))
        self.assertTrue(get_user.entity.enabled,
                        msg="User is not in enabled state.")

    @attr('regression', type='positive')
    def test_create_user_admin_with_password(self):
        """
        Verifies that identity admin can create user admin
        """
        username = rand_name("ccuseradmin")
        email = "{0}@{1}".format(username, "mailtrust.com")
        created_user = self.admin_client.add_user(
            default_region=self.default_region,
            username=username,
            domain_id=self.domain_id,
            password=self.password,
            email=email,
            enabled=True)
        self.assertEqual(created_user.status_code, 201,
                         msg="Response to create user admin is not 201.")
        # Delete user after test completion
        self.addCleanup(self.delete_user_permanently,
                        user_id=created_user.entity.id,
                        client=self.admin_client)
        self.assertTrue(created_user.entity.enabled,
                        msg="User is not in enabled state.")
        self.assertEqual(created_user.entity.username, username,
                         msg="Username is not matched with the name "
                             "which was supplied while creating user.")
        self.assertEqual(created_user.entity.email, email,
                         msg="Email is not matched with the email "
                             "which was supplied while creating user.")
        self.assertEqual(created_user.entity.domainId, str(self.domain_id),
                         msg="Domain Id is not matched with the ID "
                             "which was supplied while creating user.")
        self.assertEqual(created_user.entity.defaultRegion,
                         self.default_region,
                         msg="Default region is not matched with the region "
                             "which was supplied while creating user.")

    @attr('regression', type='positive')
    def test_delete_user_using_identity_admin(self):
        """
        Verifies that identity admin can delete user admin
        """
        added_user = self._add_user_by_identity_admin()
        deleted_user = self.admin_client.delete_user(
            user_id=added_user.entity.id)
        self.assertEqual(deleted_user.status_code, 204,
                         msg="User admin is not delete by Identity admin.")
        self.service_client.delete_user_hard(user_id=added_user.entity.id)
        get_user = self.admin_client.get_user_by_id(
            user_id=added_user.entity.id)
        self.assertEqual(get_user.status_code, 404,
                         msg="Deleted user found in directory.")
        self.assertIn("User with id: '{0}' was not found"
                      .format(added_user.entity.id),
                      get_user.content,
                      msg="Error message in response of get deleted "
                          "user is not correct")

    @attr('regression', type='positive')
    def test_update_user_admin(self):
        """
        Verifies that identity admin can update user admin
        """
        created_user = self._add_user_by_identity_admin()
        # delete user after test completion
        self.addCleanup(self.delete_user_permanently,
                        user_id=created_user.entity.id,
                        client=self.admin_client)
        updated_email = "{0}_{1}".format("updated", created_user.entity.email)
        updated_username = "{0}_{1}".format("updated",
                                            created_user.entity.username)
        updated_user = self.admin_client.update_user(
            user_id=created_user.entity.id,
            username=updated_username,
            email=updated_email,
            enabled=False)
        self.assertEqual(updated_user.entity.username, updated_username,
                         msg="Username is not matched with the updated "
                             "username.")
        self.assertEqual(updated_user.entity.email, updated_email,
                         msg="Email is not matched with the updated email ID.")
        self.assertFalse(updated_user.entity.enabled,
                         msg="Updated user is not in disabled state.")

    @attr('regression', type='positive')
    def test_get_user_credentials_using_identity_admin(self):
        """
        Verifies that identity admin can get user credentials for users
        """

        list_credentials = self.admin_client.list_credentials(
            user_id=self.created_user.entity.id)
        self.assertIsNotNone(list_credentials.entity.apiKeyCredentials.apiKey,
                             msg="API key is not auto generated for "
                                 "user admin.")
        self.assertEqual(list_credentials.entity.apiKeyCredentials.username,
                         self.username,
                         msg="Username is not matched with the name '{0}'"
                             "which was supplied while creating "
                             "user.".format(self.username))

    @attr('regression', type='positive')
    def test_get_user_api_key_using_identity_admin(self):
        """
        Verifies that identity admin can get user api keys for user
        """
        get_credentials = self.admin_client.get_user_credentials(
            user_id=self.created_user.entity.id)
        self.assertIsNotNone(get_credentials.entity,
                             msg="No credential is available for the user. "
                                 "API key is not auto generated for user "
                                 "admin.")
        self.assertIsNotNone(get_credentials.entity.apiKey,
                             msg="API key is not auto generated for user "
                                 "admin.")
        self.assertEqual(get_credentials.entity.username,
                         self.username,
                         msg="Username is not matched with the name '{0}'"
                             "which was supplied while creating "
                             "user.".format(self.username))

    @attr('regression', type='positive')
    def test_add_user_credentials(self):
        updated_pass = "{0}{1}".format("updated", self.password)
        add_credentials = self.admin_client.add_user_credentials(
            user_id=self.created_user.entity.id,
            username=self.username,
            password=updated_pass)
        self.assertEqual(add_credentials.status_code, 201,
                         msg="Response for add credential to user is not 201.")
        self.assertEqual(add_credentials.entity.password, updated_pass,
                         msg="User password is not updated to {0}"
                         .format(updated_pass))
