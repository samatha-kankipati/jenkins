from ccengine.common.decorators import attr
from ccengine.common.tools.datagen import rand_name
from ccengine.common.tools.datagen import random_int
from testrepo.common.testfixtures.identity.v2_0.identity \
    import BaseIdentityFixture, IdentityAdminFixture


class RaxIdentityUserManageRoleTest(BaseIdentityFixture):
    @classmethod
    def setUpClass(cls):
        """
        Function to create test bed for all the test. Execute once at the
        beginning of class
        @param cls: instance of class
        """
        super(RaxIdentityUserManageRoleTest, cls).setUpClass()

        cls.identity_admin_name = rand_name("ccidenadmin")
        cls.user_admin_name = rand_name("ccuseradmin")
        cls.sub_user_name = rand_name("ccsubuser")
        cls.email = '{0}@{1}'.format("testbox", "mailtrust.com")
        cls.password = "CCPassword1"
        cls.domain_id = random_int(10000, 1000000000)
        cls.identity_admin_resp = cls.service_client.add_user(
            email=cls.email,
            username=cls.identity_admin_name,
            enabled=True,
            password=cls.password)
        cls.admin_client.token = cls.provider.get_token(
            username=cls.identity_admin_name, password=cls.password)

        cls.user_adm_resp = cls.admin_client.add_user(
            username=cls.user_admin_name,
            email=cls.email,
            enabled=True,
            domain_id=cls.domain_id,
            password=cls.password)
        cls.public_client.token = cls.provider.get_token(
            username=cls.user_admin_name,
            password=cls.password)

        cls.sub_user_resp = cls.public_client.add_user(
            username=cls.sub_user_name,
            email=cls.email,
            enabled=True,
            password=cls.password)
        cls.default_client = cls.provider.get_client()
        cls.default_client.token = cls.provider.get_token(
            username=cls.sub_user_name,
            password=cls.password)

        cls.role_info = cls.service_client.get_role(
            role_id=cls.config.identity_api.user_manage_role_id)

    @classmethod
    def tearDownClass(cls):
        """
        Function to clean up the data after execution of all the tests
        completed. Execute once at the end of all the tests.
        @param cls: instance of class
        """
        cls.delete_user_permanently(user_id=cls.sub_user_resp.entity.id,
                                    client=cls.public_client)
        cls.delete_user_permanently(user_id=cls.user_adm_resp.entity.id,
                                    client=cls.admin_client)
        cls.delete_user_permanently(user_id=cls.identity_admin_resp.entity.id,
                                    client=cls.service_client)

    def assign_user_manage_role_to_default_sub_user(self):
        """
        Function to assign user manager role to default sub user
        @return: response of add role to user
        """
        add_role_to_sub_user = self.admin_client.add_role_to_user(
            user_id=self.sub_user_resp.entity.id,
            role_id=self.role_info.entity.id)
        normal_response_codes = [200, 201]
        self.assertIn(add_role_to_sub_user.status_code,
                      normal_response_codes,
                      msg="Response for Add role to user is not as "
                          "expected.")
        return add_role_to_sub_user

    def create_sub_user_and_assign_user_manage_role(self, client):
        """
        Function to create sub user and assign user manage role to it.
        """
        sub_user_name = rand_name("ccsubuser")
        email = '{0}@{1}'.format(sub_user_name, "mailtrust.com")
        password = "CCPassword1"
        create_sub_user_resp = client.add_user(
            username=sub_user_name,
            email=email,
            password=password,
            enabled=True)
        self.assertEqual(create_sub_user_resp.status_code, 201,
                         msg="Response for add sub user is not 201.")
        # addCleanup works as stack, First in Last out
        self.addCleanup(self.delete_user_permanently,
                        user_id=create_sub_user_resp.entity.id,
                        client=client)

        add_role_to_sub_user = client.add_role_to_user(
            user_id=create_sub_user_resp.entity.id,
            role_id=self.role_info.entity.id)
        normal_response_codes = [200, 201]
        self.assertIn(add_role_to_sub_user.status_code,
                      normal_response_codes,
                      msg="Response for Add role to sub user is not as "
                          "expected.")
        default_client_with_um = self.provider.get_client(
            username=sub_user_name,
            password=password)
        return default_client_with_um

    def assign_user_manage_role_to_admin_user_with(self, client, client_type,
                                                   user, user_type):
        """
        Function to assign user manage role to given User with specific client
        @param client: Client to add role to user
        @param client_type: Name of the Client
        @param user: User
        @param user_type: Type of the user ex. User Admin, Identity Admin etc
        """
        add_role_to_user = client.add_role_to_user(
            user_id=user.entity.id,
            role_id=self.role_info.entity.id)
        self.assertEqual(add_role_to_user.status_code, 400,
                         msg="Response for Add role to {0} is not"
                             " 400. Using {1}".format(user_type,
                                                      client_type))
        user_roles = client.list_user_global_roles(
            user_id=user.entity.id)
        has_user_manage_role = False
        for user_role in user_roles.entity:
            if user_role.id == self.role_info.entity.id:
                has_user_manage_role = True
                break
        self.assertFalse(has_user_manage_role,
                         msg="User manage role is added to {0} "
                             "using {1}".format(user_type,
                                                client_type))

    def sub_user_add_and_remove_user_manage_role(self, client, client_type):
        """
        Function to add user manage role to user and remove the same
        @param client: Client to add or remove role from user
        @param client_type: Name of the client
        @type String
        """
        add_role_to_sub_user = client.add_role_to_user(
            user_id=self.sub_user_resp.entity.id,
            role_id=self.role_info.entity.id)
        # In api docs the add role to user response is 201
        normal_response_codes = [200, 201]
        self.assertIn(add_role_to_sub_user.status_code, normal_response_codes,
                      msg="Response for Add role to user is not as expected. "
                          "Using {0}".format(client_type))
        sub_user_roles = client.list_user_global_roles(
            user_id=self.sub_user_resp.entity.id)
        has_user_manage_role = False
        for sub_user_role in sub_user_roles.entity:
            if sub_user_role.id == self.role_info.entity.id:
                has_user_manage_role = True
                break
        self.assertTrue(has_user_manage_role,
                        msg="User manage role is not added to sub user. "
                            "Using {0}".format(client_type))
        delete_role_from_sub_user = client.delete_role_from_user(
            user_id=self.sub_user_resp.entity.id,
            role_id=self.role_info.entity.id)
        self.assertEqual(delete_role_from_sub_user.status_code, 204,
                         msg="Response for delete role of sub user is not "
                             "204. Using {0}".format(client_type))
        sub_user_roles = client.list_user_global_roles(
            user_id=self.sub_user_resp.entity.id)
        for sub_user_role in sub_user_roles.entity:
            self.assertNotEqual(sub_user_role.id, self.role_info.entity.id,
                                msg="Role deletion from sub user is failed"
                                    "using {0}".format(client_type))

    @attr('smoke', type='positive')
    def test_add_user_manage_role_to_sub_user_using_service_admin(self):
        """
        Verifies that service admin should be able to add User Manage Role
        to sub user.
        """
        self.sub_user_add_and_remove_user_manage_role(self.service_client,
                                                      "Service Admin Client")

    @attr('smoke', type='positive')
    def test_add_user_manage_role_to_sub_user_using_identity_admin(self):
        """
        Verifies that identity admin should be able to add User Manage Role
        to sub user.
        """

        self.sub_user_add_and_remove_user_manage_role(self.admin_client,
                                                      "Identity Admin Client")

    @attr('smoke', type='positive')
    def test_add_user_manage_role_to_sub_user_using_user_admin(self):
        """
        Verifies that user admin should be able to add User Manage Role
        to sub user.
        """
        self.sub_user_add_and_remove_user_manage_role(self.public_client,
                                                      "User Admin Client")

    @attr('regression', type='negative')
    def test_add_user_manage_role_to_admins_using_service_admin(self):
        """
        Verifies that service admin should not be able to add User Manage role
        to Service admin, Identity Admin or User admin
        """
        service_admin_resp = self.service_client.get_user_by_name(
            name=self.config.identity_api.service_username)
        user_dict = {"Identity Admin": self.identity_admin_resp,
                     "User Admin": self.user_adm_resp}
        # Iterating over client and users to validate UM role addition
        for user_type, user in user_dict.iteritems():
            self.assign_user_manage_role_to_admin_user_with(
                client=self.service_client,
                client_type="Service Admin Client",
                user=user,
                user_type=user_type)

    @attr('regression', type='negative')
    def test_add_user_manage_role_to_user_admin_using_identity_admin(self):
        """
        Verifies that Identity admin should not be able to add User Manage
        role to Identity Admin or User admin
        """
        self.assign_user_manage_role_to_admin_user_with(
            client=self.admin_client,
            client_type="Identity Admin Client",
            user=self.user_adm_resp,
            user_type="User Admin")

    @attr('regression', type='negative')
    def test_add_user_manage_role_to_admins_using_identity_admin(self):
        """
        Verifies that Identity admin should not be able to add User Manage
        role to Service Admin or himself
        """
        service_admin_resp = self.service_client.get_user_by_name(
            name=self.config.identity_api.service_username)
        user_dict = {"Identity Admin": self.identity_admin_resp,
                     "Service Admin": service_admin_resp}
        # Iterating over client and users to validate UM role addition
        for user_type, user in user_dict.iteritems():
            add_role_to_user = self.admin_client.add_role_to_user(
                user_id=user.entity.id,
                role_id=self.role_info.entity.id)
            self.assertEqual(
                add_role_to_user.status_code, 403,
                msg="Response for Add role to {0} is not 403. Using Identity "
                    "Admin Client".format(user_type))

    @attr('regression', type='negative')
    def test_add_user_manage_role_to_user_admin_using_user_admin(self):
        """
        Verifies that user admin should not be able to add User Manage
        role to user Admin
        """
        self.assign_user_manage_role_to_admin_user_with(
            client=self.admin_client,
            client_type="User Admin Client",
            user=self.user_adm_resp,
            user_type="User Admin")

    @attr('regression', type='negative')
    def test_add_user_manage_role_to_admins_using_user_admin(self):
        """
        Verifies that user admin should not be able to add User
        Manage role to Service admin or Identity Admin
        """
        service_admin_resp = self.service_client.get_user_by_name(
            name=self.config.identity_api.service_username)

        user_dict = {"Identity Admin": self.identity_admin_resp,
                     "Service Admin": service_admin_resp}
        for user_type, user in user_dict.iteritems():
            add_role_to_user = self.public_client.add_role_to_user(
                user_id=user.entity.id,
                role_id=self.role_info.entity.id)
            self.assertEqual(add_role_to_user.status_code, 403,
                             msg="Response for Add role to {0} is not 403. "
                                 "Using User Admin Client".format(user_type))

    @attr('regression', type='negative')
    def test_add_user_manage_role_to_admins_using_sub_user(self):
        """
        Verifies that sub user should not be able to add User
        Manage role to Service admin, Identity Admin, User admin or sub user
        """
        service_admin_resp = self.service_client.get_user_by_name(
            name=self.config.identity_api.service_username)
        sub_user_name = rand_name("CCsubuser")
        sub_user_resp = self.public_client.add_user(
            username=sub_user_name,
            email="{0}@{1}".format(sub_user_name, "mailtrust.com"),
            enabled=True,
            password=self.password)
        self.assertEqual(sub_user_resp.status_code, 201,
                         msg="Response for add sub user is not 201.")
        # addCleanup works as stack, First in Last out
        self.addCleanup(self.delete_user_permanently,
                        user_id=sub_user_resp.entity.id,
                        client=self.public_client)

        default_client = self.provider.get_client()
        default_client.token = self.provider.get_token(
            username=sub_user_name,
            password=self.password)
        user_dict = {"Service Admin": service_admin_resp,
                     "Identity Admin": self.identity_admin_resp,
                     "User Admin": self.user_adm_resp,
                     "Sub User": self.sub_user_resp}
        for user_type, user in user_dict.iteritems():
            add_role_to_user = default_client.add_role_to_user(
                user_id=user.entity.id,
                role_id=self.role_info.entity.id)
            self.assertEqual(add_role_to_user.status_code, 403,
                             msg="Response for Add role to {0} is not 403. "
                                 "Using Sub user client".format(user_type))

    @attr('regression', type='negative')
    def test_add_user_manage_role_to_admins_using_sub_user_with_um(self):
        """
        Verifies that Sub user with User manage Role should not be able to add
        UserManage role to Service admin, Identity Admin or User admin
        """
        service_admin_resp = self.service_client.get_user_by_name(
            name=self.config.identity_api.service_username)

        default_client_with_um = \
            self.create_sub_user_and_assign_user_manage_role(
                client=self.public_client)
        user_dict = {"Service Admin": service_admin_resp,
                     "Identity Admin": self.identity_admin_resp,
                     "User Admin": self.user_adm_resp}
        for user_type, user in user_dict.iteritems():
            add_role_to_user = default_client_with_um.add_role_to_user(
                user_id=user.entity.id,
                role_id=self.role_info.entity.id)
            self.assertEqual(add_role_to_user.status_code, 403,
                             msg="Response for Add role to {0} is not 403. "
                                 "Using Sub user client with User manage "
                                 "Role".format(user_type))

    @attr("regression", type="positive")
    def test_manage_sub_user_by_sub_user_with_UM_role(self):
        """
        Verifies that Sub user with User Manage role can create, update,
        read and delete sub user.
        """
        common_err_msg = " Using: Sub user with User manager role."
        self.assign_user_manage_role_to_default_sub_user()
        # Adding for clean up
        self.addCleanup(self.public_client.delete_role_from_user,
                        user_id=self.sub_user_resp.entity.id,
                        role_id=self.role_info.entity.id)

        sub_user_name = rand_name("ccsubuser")
        email = '{0}@{1}'.format(sub_user_name, "mailtrust.com")
        password = "CCPassword1"
        create_sub_user_resp = self.default_client.add_user(
            username=sub_user_name,
            email=email,
            password=password,
            enabled=True)
        self.assertEqual(create_sub_user_resp.status_code, 201,
                         msg="Response for add sub user is not 201. {0}".
                         format(common_err_msg))
        # Delete User after test completion
        self.addCleanup(self.delete_user_permanently,
                        user_id=create_sub_user_resp.entity.id,
                        client=self.admin_client)

        updated_email = "{0}_{1}".format("updated", email)
        update_sub_user_resp = self.default_client.update_user(
            user_id=create_sub_user_resp.entity.id, email=updated_email)
        self.assertEqual(update_sub_user_resp.status_code, 200,
                         msg="Response for update sub user is not 200. {0}".
                         format(common_err_msg))
        updated_sub_user_resp = self.default_client.get_user_by_id(
            create_sub_user_resp.entity.id)
        self.assertEqual(updated_sub_user_resp.status_code, 200,
                         msg="Response for get sub user is not 200. {0}".
                         format(common_err_msg))
        self.assertEqual([create_sub_user_resp.entity.id,
                          create_sub_user_resp.entity.username,
                          create_sub_user_resp.entity.enabled,
                          updated_email],
                         [updated_sub_user_resp.entity.id,
                          updated_sub_user_resp.entity.username,
                          updated_sub_user_resp.entity.enabled,
                          updated_sub_user_resp.entity.email],
                         msg="Sub User email is not updated. {0}".
                         format(common_err_msg))

        user_by_email = self.default_client.get_users_by_email(
            email=updated_email)
        self.assertEqual(user_by_email.status_code, 200,
                         msg="Response for get sub user by email is not 200. "
                             "{0}".format(common_err_msg))
        self.assertEqual(user_by_email.entity[0].id,
                         create_sub_user_resp.entity.id,
                         msg="User Id is not correct for user by email ID.")

        sub_user_client = self.provider.get_client(username=sub_user_name,
                                                   password=password)
        reset_api_key = sub_user_client.reset_user_api_key(
            user_id=create_sub_user_resp.entity.id)
        self.assertEqual(reset_api_key.status_code, 200,
                         msg="Response for reset sub user api key is not 200.")
        user_api_key = self.default_client.get_user_credentials(
            user_id=create_sub_user_resp.entity.id)
        self.assertEqual(user_api_key.status_code, 200,
                         msg="Response for get sub user api key is not 200. "
                             "{0}".format(common_err_msg))
        user_credentials = self.default_client.list_credentials(
            user_id=create_sub_user_resp.entity.id)
        self.assertEqual(user_credentials.status_code, 403,
                         msg="Response for get sub user credentials is not "
                             "403. {0}".format(common_err_msg))

        delete_sub_user_resp = self.default_client.delete_user(
            user_id=create_sub_user_resp.entity.id)
        self.assertEqual(delete_sub_user_resp.status_code, 204,
                         msg="Response for delete sub user is not 204. {0}".
                         format(common_err_msg))

    @attr("regression", type="negative")
    def test_manage_sub_user_by_sub_user_revoked_UM_role(self):
        """
        Verifies that Sub user with revoked User Manage role can not create,
        update, read or delete sub user.
        """
        common_err_msg = " Using: Sub user with revoked User manager role."
        self.assign_user_manage_role_to_default_sub_user()

        delete_role_from_sub_user = self.public_client \
            .delete_role_from_user(user_id=self.sub_user_resp.entity.id,
                                   role_id=self.role_info.entity.id)
        self.assertEqual(delete_role_from_sub_user.status_code, 204,
                         msg="Response for delete role of sub user is not"
                             " 204.")

        sub_user_name = rand_name("ccsubuser")
        email = '{0}@{1}'.format(sub_user_name, "mailtrust.com")
        password = "CCPassword1"
        create_sub_user_resp = self.default_client.add_user(
            username=sub_user_name,
            email=email,
            password=password,
            enabled=True)
        self.assertEqual(create_sub_user_resp.status_code, 403,
                         msg="Response for add sub user is not 403. {0}".
                         format(common_err_msg))

        create_sub_user_resp = self.public_client.add_user(
            username=sub_user_name,
            email=email,
            password=password,
            enabled=True)
        self.assertEqual(create_sub_user_resp.status_code, 201,
                         msg="Response for add sub user is not 201.")
        # addCleanup works as stack, First in Last out
        self.addCleanup(self.delete_user_permanently,
                        user_id=create_sub_user_resp.entity.id,
                        client=self.public_client)

        updated_email = "{0}_{1}".format("updated", email)
        update_sub_user_resp = self.default_client.update_user(
            user_id=create_sub_user_resp.entity.id, email=updated_email)
        self.assertEqual(update_sub_user_resp.status_code, 403,
                         msg="Response for update sub user is not 403.")

        delete_sub_user_resp = self.default_client.delete_user(
            user_id=create_sub_user_resp.entity.id)
        self.assertEqual(delete_sub_user_resp.status_code, 403,
                         msg="Response for delete sub user is not 403. {0}".
                         format(common_err_msg))

    @attr("regression", type="negative")
    def test_manage_sub_user_of_diff_domain_by_sub_user_UM_role(self):
        """
        Verifies that Sub user with User Manage role can not assign User Manage
        role to sub user of different domain
        """
        common_err_msg = " Using: Sub user with User manager role."
        self.assign_user_manage_role_to_default_sub_user()
        # Adding for clean up
        self.addCleanup(self.public_client.delete_role_from_user,
                        user_id=self.sub_user_resp.entity.id,
                        role_id=self.role_info.entity.id)

        user_admin_name_domain2 = rand_name("ccuseradmin2")
        email = '{0}@{1}'.format(user_admin_name_domain2, "mailtrust.com")
        password = "CCPassword1"
        domain_id = random_int(10000, 1000000000)

        user_admin_resp = self.admin_client.add_user(
            username=user_admin_name_domain2,
            email=email,
            enabled=True,
            domain_id=domain_id,
            password=password)
        self.assertEqual(user_admin_resp.status_code, 201,
                         msg="Response for add user admin is not 201.")
        # addCleanup works as stack, First in Last out
        self.addCleanup(self.delete_user_permanently,
                        user_id=user_admin_resp.entity.id,
                        client=self.admin_client)

        self.public_client2 = self.provider.get_client()
        self.public_client2.token = self.provider.get_token(
            username=user_admin_name_domain2,
            password=password)

        sub_user_name = rand_name("ccsubuser")
        email = '{0}@{1}'.format(sub_user_name, "mailtrust.com")
        password = "CCPassword1"
        create_sub_user_domain2_resp = self.public_client2.add_user(
            username=sub_user_name,
            email=email,
            password=password,
            enabled=True)
        self.assertEqual(create_sub_user_domain2_resp.status_code, 201,
                         msg="Response for add sub user is not 201.")
        # addCleanup works as stack, First in Last out
        self.addCleanup(self.delete_user_permanently,
                        user_id=create_sub_user_domain2_resp.entity.id,
                        client=self.admin_client)

        # Adding user manage role using user manager token
        add_role_to_sub_user = self.default_client.add_role_to_user(
            user_id=create_sub_user_domain2_resp.entity.id,
            role_id=self.role_info.entity.id)
        self.assertEqual(add_role_to_sub_user.status_code, 403,
                         msg="Response for Add role to sub user in different "
                             "domain is not 403. {0}".format(common_err_msg))


class UserAdminAndSubUserWithUMRoleTest(IdentityAdminFixture):
    """
    Class to verify that Sub user with user manage role can not administrate
    user admin.
    """
    @classmethod
    def setUpClass(cls):
        """
        Function to create test bed for all the test. Execute once at the
        beginning of class
        @param cls: instance of class
        """
        super(UserAdminAndSubUserWithUMRoleTest, cls).setUpClass()
        cls.common_err_msg = " Using: Sub user with User manager role."
        user_admin_name = rand_name("ccuseradmin")
        cls.email = '{0}@{1}'.format(user_admin_name, "mailtrust.com")
        password = "CCPassword1"
        domain_id = random_int(10000, 1000000000)
        cls.create_user_admin_resp = cls.admin_client.add_user(
            username=user_admin_name,
            email=cls.email,
            password=password,
            domain_id=domain_id,
            enabled=True)
        cls.public_client.token = cls.provider.get_token(
            username=user_admin_name,
            password=password)

        sub_user_name = rand_name("ccsubuser")
        email = '{0}@{1}'.format(sub_user_name, "mailtrust.com")
        password = "CCPassword1"
        cls.create_sub_user_resp = cls.public_client.add_user(
            username=sub_user_name,
            email=email,
            password=password,
            enabled=True)
        add_role_to_user = cls.admin_client.add_role_to_user(
            user_id=cls.create_sub_user_resp.entity.id,
            role_id=cls.config.identity_api.user_manage_role_id)
        assert add_role_to_user.status_code == 200,\
            "Response for Add role to user is not 200. Actual is {0}."\
            .format(add_role_to_user.status_code)
        cls.default_client_with_um = cls.provider.get_client(
            username=sub_user_name,
            password=password)

    @classmethod
    def tearDownClass(cls):
        """
        Function to clean up the data after execution of all the tests
        completed. Execute once at the end of all the tests.
        @param cls: instance of class
        """
        cls.public_client.delete_user(
            user_id=cls.create_sub_user_resp.entity.id)
        cls.service_client.delete_user_hard(
            user_id=cls.create_sub_user_resp.entity.id)

        cls.admin_client.delete_user(
            user_id=cls.create_user_admin_resp.entity.id)
        cls.service_client.delete_user_hard(
            user_id=cls.create_user_admin_resp.entity.id)

    @attr("regression", type="negative")
    def test_update_user_admin_by_sub_user_with_user_manage_role(self):
        """
        Verifies that Sub user with User Manage role can not update
        user admin info
        """
        updated_email = "{0}_{1}".format("updated", self.email)
        update_sub_user_resp = self.default_client_with_um.update_user(
            user_id=self.create_user_admin_resp.entity.id,
            email=updated_email,
            enabled=False)
        self.assertEqual(update_sub_user_resp.status_code, 403,
                         msg="Response for update user admin is not "
                             "403. {0}".format(self.common_err_msg))

    @attr("regression", type="negative")
    def test_get_user_admin_by_id_sub_user_with_user_manage_role(self):
        """
        Verifies that Sub user with User Manage role can get user admin by Id
        """
        user_by_id = self.default_client_with_um.get_user_by_id(
            self.create_user_admin_resp.entity.id)
        self.assertEqual(user_by_id.status_code, 200,
                         msg="Response for get user admin by id is not 200. "
                             "{0}".format(self.common_err_msg))

    @attr("regression", type="negative")
    def test_get_user_admin_by_email_sub_user_with_user_manage_role(self):
        """
        Verifies that Sub user with User Manage role can get user admin by
        email Id
        """
        user_by_email = self.default_client_with_um.get_users_by_email(
            email=self.email)
        self.assertEqual(user_by_email.status_code, 200,
                         msg="Response for get user admin by email is not 200"
                             ". {0}".format(self.common_err_msg))

    @attr("regression", type="negative")
    def test_get_user_admin_api_key_by_sub_user_with_user_manage_role(self):
        """
        Verifies that Sub user with User Manage role can not get user admin
        api key
        """
        reset_api_key = self.public_client.reset_user_api_key(
            user_id=self.create_user_admin_resp.entity.id)
        self.assertEqual(reset_api_key.status_code, 200,
                         msg="Response for reset user admin api "
                             "key is not 200.")

        user_api_key = self.default_client_with_um.get_user_credentials(
            user_id=self.create_user_admin_resp.entity.id)
        self.assertEqual(user_api_key.status_code, 403,
                         msg="Response for get user admin api key is not 403. "
                             "{0}".format(self.common_err_msg))

    @attr("regression", type="negative")
    def test_get_user_admin_credential_by_sub_user_with_user_manage_role(self):
        """
        Verifies that Sub user with User Manage role can not get user admin
        credentials
        """
        user_credentials = self.default_client_with_um.list_credentials(
            user_id=self.create_user_admin_resp.entity.id)
        self.assertEqual(user_credentials.status_code, 403,
                         msg="Response for get sub user credentials is not "
                             "403. {0}".format(self.common_err_msg))
