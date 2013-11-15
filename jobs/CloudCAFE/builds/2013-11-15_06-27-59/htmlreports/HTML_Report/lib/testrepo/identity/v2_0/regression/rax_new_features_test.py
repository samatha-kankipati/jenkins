from ccengine.common.tools.datagen import rand_name
from ccengine.common.tools.datagen import random_int
from testrepo.common.testfixtures.identity.v2_0.identity \
    import BaseIdentityFixture
from ccengine.common.decorators import attr


class UsersTest(BaseIdentityFixture):
    @classmethod
    def setUpClass(cls):
        super(UsersTest, cls).setUpClass()
        username_uniq = rand_name("ccadminname")
        cls.username_one = rand_name("ccadminnameone")
        cls.username_sec = rand_name("ccadminnamesec")
        cls.email = '{0}@{1}'.format(username_uniq, "mailtrust.com")
        domain_id = random_int(10000, 1000000000)
        domain_id_sec = random_int(10000, 1000000000)
        cls.password = "Gadmpass8"
        auth_adm_resp = cls.public_client.authenticate_user_password(
            cls.config.identity_api.admin_username,
            cls.config.identity_api.admin_password)
        cls.admin_client.token = auth_adm_resp.entity.token.id
        auth_usr_resp = cls.public_client.authenticate_user_apikey(
            cls.config.identity_api.username,
            cls.config.identity_api.api_key)
        cls.public_client.token = auth_usr_resp.entity.token.id
        cls.adm_user_uniq = cls.admin_client.add_user(username=username_uniq,
                                                      email=cls.email,
                                                      enabled=True,
                                                      domain_id=domain_id,
                                                      password=cls.password)
        cls.adm_user_one = cls.admin_client.add_user(username=cls.username_one,
                                                     email=cls.email,
                                                     enabled=True,
                                                     domain_id=domain_id_sec,
                                                     password=cls.password)
        cls.adm_user_sec = cls.admin_client.add_user(username=cls.username_sec,
                                                     email=cls.email,
                                                     enabled=True,
                                                     domain_id=domain_id_sec,
                                                     password=cls.password)

    @classmethod
    def tearDownClass(cls):
        # Deleting Admin Users
        cls.admin_client.delete_user(user_id=cls.adm_user_uniq.entity.id)
        cls.service_client.delete_user_hard(user_id=cls.adm_user_uniq.entity.id)
        cls.admin_client.delete_user(user_id=cls.adm_user_one.entity.id)
        cls.service_client.delete_user_hard(user_id=cls.adm_user_one.entity.id)
        cls.admin_client.delete_user(user_id=cls.adm_user_sec.entity.id)
        cls.service_client.delete_user_hard(user_id=cls.adm_user_sec.entity.id)

    @attr('regression', type='positive')
    def test_b42637_show_account_admin(self):
        """
        show account admins new feature
        """
        normal_response_codes = [200, 203]
        username = rand_name("cctestname")
        email = '{0}@{1}'.format(username, 'mailtrust.com')
        create_user = self.public_client.add_user(username=username,
                                                  email=email,
                                                  enabled=False,
                                                  password="Gellpass8")

        self.assertEqual(create_user.status_code, 201,
                         msg='Add user expected response 201 received {0}'.
                         format(create_user.status_code))
        # delete user after test completion
        self.addCleanup(self.delete_user_permanently,
                        client=self.public_client,
                        user_id=create_user.entity.id)

        get_admins = self.public_client.show_account_admins(
            user_id=create_user.entity.id)
        self.assertIn(get_admins.status_code, normal_response_codes,
                      msg='List users admins expected {0} recieved {1}'.format(
                          normal_response_codes, get_admins.status_code))

    @attr('regression', type='positive')
    def test_b40426_automatic_subusers_disable(self):
        """
        User Admin Disabled / Disabled Sub Users
        Presently the test case is failing
        """
        auth_usr_one = self.public_client.authenticate_user_password(
            self.adm_user_one.entity.username,
            self.password)
        self.public_client.token = auth_usr_one.entity.token.id

        username = rand_name("cctestnameord")
        email = '{0}@{1}'.format(username, 'mailtrust.com')
        self.create_user_def = self.public_client.add_user(username=username,
                                                           email=email,
                                                           enabled=True,
                                                           password=
                                                           self.password)
        self.assertEqual(self.create_user_def.status_code, 201,
                         msg='Add user expected response 201 received {0}'.
                         format(self.create_user_def.status_code))
        # Delete user after test completion
        self.addCleanup(self.delete_user_permanently,
                        user_id=self.create_user_def.entity.id,
                        client=self.public_client)
        get_user_init = self.admin_client.get_user_by_name(name=username)
        self.assertEqual(get_user_init.entity.enabled, True,
                         msg="Enabled is True")

        update_user_one = self.admin_client.update_user(
            user_id=self.adm_user_one.entity.id,
            username=self.username_one,
            email=self.email,
            enabled=False)
        self.assertEqual(update_user_one.status_code, 200,
                         msg="Admin upd user status expected response 200"
                             " received %s" % update_user_one.status_code)
        get_user_sec = self.admin_client.get_user_by_name(name=username)
        self.assertEqual(get_user_sec.entity.enabled, True,
                         msg="Enabled is True")
        update_user_two = \
            self.admin_client.update_user(
                user_id=self.adm_user_sec.entity.id,
                username=self.username_sec,
                email=self.email,
                enabled=False)
        self.assertEqual(update_user_two.status_code, 200,
                         msg="Admin upd user status expected response 200"
                             " received %s" % update_user_two.status_code)
        get_user_thd = self.admin_client.get_user_by_name(name=username)
        self.assertEqual(get_user_thd.entity.enabled, False,
                         msg="Enabled should be False")
        update_user_one_undo = self.admin_client.update_user(
            user_id=self.adm_user_one.entity.id,
            username=self.username_one,
            email=self.email,
            enabled=True)
        self.assertEqual(update_user_one_undo.status_code, 200,
                         msg="Admin upd user status expected response 200"
                             " received %s" % update_user_one_undo.status_code)

    @attr('regression', type='negative')
    def test_b40522_duplicate_groups(self):
        """
        Group with same name should not be created
        Technical Debt:remove Duplicate Groups
        """
        name = 'Static_Name'
        description = 'static Description'
        add_group = self.admin_client.add_group(name=name,
                                                description=description)
        self.assertEqual(add_group.status_code, 201,
                         msg="Response is not 201")
        add_group_neg = self.admin_client.add_group(name=name,
                                                    description=description)
        self.assertEqual(add_group_neg.status_code, 409,
                         msg="Expected response 409 but received  %s" %
                             add_group_neg.status_code)
        self.assertTrue('{0} already exists'.format(name) in
                        add_group_neg.content,
                        msg='Expecting Group already exist')
        # delete group after test completion
        self.addCleanup(self.admin_client.delete_group,
                        group_id=add_group.entity.id)

    @attr('regression', type='negative')
    def test_b40475_direct_group_assignment_to_sub_user(self):
        """
        This test is to verify that when Identity admin tries to assign a
        group directly to sub user then he should get the error code 400
        """

        auth_usr_one = self.public_client.authenticate_user_password(
            self.adm_user_one.entity.username,
            self.password)
        self.public_client.token = auth_usr_one.entity.token.id

        username = rand_name("ccsubuser")
        email = '{0}@{1}'.format(username, 'mailtrust.com')
        created_sub_user = self.public_client.add_user(username=username,
                                                       email=email,
                                                       enabled=False,
                                                       password="Gellpass8")
        self.assertEqual(created_sub_user.status_code, 201,
                         msg='Add user expected response 201 received {0}'.
                         format(created_sub_user.status_code))
        # delete user after test completion
        self.addCleanup(self.public_client.delete_user,
                        user_id=created_sub_user.entity.id)

        name_group = rand_name("ccgroupname")
        description = "Test Group to validate add group functionality"
        add_group = self.admin_client.add_group(name=name_group,
                                                description=description)
        self.assertEqual(add_group.status_code, 201,
                         msg="Response for adding a new group is not 201")
        # delete group after test completion
        self.addCleanup(self.admin_client.delete_group,
                        group_id=add_group.entity.id)
        group_assignment_response = self.admin_client.add_user_to_group(
            user_id=created_sub_user.entity.id,
            group_id=add_group.entity.id)
        self.assertEqual(group_assignment_response.status_code, 400,
                         msg="Response for direct group assignment to "
                             "sub user is not 400.")

    @attr('regression', type='positive')
    def test_b40475_group_association_disassociation_and_inheritance(self):
        """
        Test to validate:
        1. When a user-admin is assigned to  a new [Group], then the sub-users
        of the same domain are assigned to the same group.
        2. Sub-users inherit the collective of groups assigned to users
        of the same account upon creation
        3. When a user-admin is disassociated/removed from a [Group],
        then the sub-users of the same domain are disassociated/removed
        from the group
        """
        user_admin1_domain2 = self.public_client.authenticate_user_password(
            self.adm_user_one.entity.username,
            self.password)
        self.public_client.token = user_admin1_domain2.entity.token.id

        first_group_name = rand_name("cctestgroup1")
        description = 'Group for testing Association/disassociation'
        first_group_resp = self.admin_client.add_group(
            name=first_group_name,
            description=description)
        self.assertEqual(first_group_resp.status_code, 201,
                         msg="Add group response is not 201.")
        # Delete group after test completion
        self.addCleanup(self.admin_client.delete_group,
                        group_id=first_group_resp.entity.id)

        add_admin1_in_group = self.admin_client.add_user_to_group(
            group_id=first_group_resp.entity.id,
            user_id=self.adm_user_one.entity.id)
        self.assertEqual(add_admin1_in_group.status_code, 204,
                         msg="Add user to group response is not 204.")
        # Remove user from group after test completion
        self.addCleanup(self.admin_client.remove_user_from_group,
                        user_id=self.adm_user_one.entity.id,
                        group_id=first_group_resp.entity.id)

        second_group_name = rand_name("cctestgroup2")
        second_group_resp = self.admin_client.add_group(
            name=second_group_name,
            description=description)
        self.assertEqual(second_group_resp.status_code, 201,
                         msg="Add group response is not 201.")
        # Delete group after test completion
        self.addCleanup(self.admin_client.delete_group,
                        group_id=second_group_resp.entity.id)

        add_admin2_in_group = self.admin_client.add_user_to_group(
            group_id=second_group_resp.entity.id,
            user_id=self.adm_user_sec.entity.id)
        self.assertEqual(add_admin2_in_group.status_code, 204,
                         msg="Add user to group response is not 204.")
        # Remove user from group after test completion
        self.addCleanup(self.admin_client.remove_user_from_group,
                        user_id=self.adm_user_sec.entity.id,
                        group_id=second_group_resp.entity.id)

        sub_user_username = rand_name("ccsubuser")
        email = '{0}@{1}'.format(sub_user_username, 'mailtrust.com')
        sub_user_domain2 = self.public_client.add_user(
            username=sub_user_username,
            email=email,
            enabled=False,
            password=self.password)
        self.assertEqual(sub_user_domain2.status_code, 201,
                         msg='Add sub user response status is not 201.')
        # delete sub user after test completion
        self.addCleanup(self.delete_user_permanently,
                        client=self.public_client,
                        user_id=sub_user_domain2.entity.id)

        sub_user_group_list = self.admin_client.list_groups_for_user(
            user_id=sub_user_domain2.entity.id)
        group_names = []
        for group in sub_user_group_list.entity:
            group_names.append(group.name)
        self.assertTrue(set(group_names).issubset(set([first_group_name,
                                                       second_group_name])),
                        msg="All the groups are not assigned to sub-user.")

        third_group_name = rand_name("cctestgroup3")
        third_group_resp = self.admin_client.add_group(name=third_group_name,
                                                       description=description)
        self.assertEqual(third_group_resp.status_code, 201,
                         msg="Add group response is not 201.")
        # Delete group after test completion
        self.addCleanup(self.admin_client.delete_group,
                        group_id=third_group_resp.entity.id)

        add_admin2_in_group = self.admin_client.add_user_to_group(
            group_id=third_group_resp.entity.id,
            user_id=self.adm_user_one.entity.id)
        self.assertEqual(add_admin2_in_group.status_code, 204,
                         msg="Add user to group response is not 204.")
        # Remove user from group after test completion
        self.addCleanup(self.admin_client.remove_user_from_group,
                        user_id=self.adm_user_one.entity.id,
                        group_id=third_group_resp.entity.id)

        # Sub user should automatically add into the group as admin is assigned
        sub_user_group_list = self.admin_client.list_groups_for_user(
            user_id=sub_user_domain2.entity.id)
        group_names = []
        for group in sub_user_group_list.entity:
            group_names.append(group.name)
        expected_groups = [first_group_name, second_group_name,
                           third_group_name]
        self.assertTrue(set(group_names).issubset(set(expected_groups)),
                        msg="All the groups are not assigned to sub-user.")

        remove_admin1_from_group = self.admin_client.remove_user_from_group(
            user_id=self.adm_user_one.entity.id,
            group_id=first_group_resp.entity.id)
        self.assertEqual(remove_admin1_from_group.status_code, 204,
                         msg="Response for removal of user from group is not "
                             "204")

        sub_user_group_list = self.admin_client.list_groups_for_user(
            user_id=sub_user_domain2.entity.id)
        group_names = []
        for group in sub_user_group_list.entity:
            group_names.append(group.name)
        self.assertFalse(first_group_name in group_names,
                         msg="Groups is assigned to sub-user even after "
                             "removing from user admin.")

        remove_admin2_from_group = self.admin_client.remove_user_from_group(
            user_id=self.adm_user_sec.entity.id,
            group_id=second_group_resp.entity.id)
        self.assertEqual(remove_admin2_from_group.status_code, 204,
                         msg="Response for removal of user from group is not "
                             "204")

        sub_user_group_list = self.admin_client.list_groups_for_user(
            user_id=sub_user_domain2.entity.id)
        group_names = []
        for group in sub_user_group_list.entity:
            group_names.append(group.name)
        self.assertFalse(second_group_name in group_names,
                         msg="Groups is assigned to sub-user even after "
                             "removing from user admin.")

    @attr('regression', type='positive')
    def test_44731_propagating_roles_without_attr(self):
        """
        Test for adding role with out any attribute
        """
        name = rand_name("Guest:Role")
        description = rand_name("Guest description ")
        add_role = self.admin_client.add_role(name=name,
                                              description=description)
        self.assertEqual(add_role.status_code, 201,
                         msg="Response for add role is not 201.")
        # delete role after test completion
        self.addCleanup(self.admin_client.delete_role,
                        role_id=add_role.entity.id)
        self.assertFalse(add_role.entity.propagate,
                          msg='Default value for role propagate is not False')

    @attr('regression', type='positive')
    def test_44731_propagating_roles_attr_assigned(self):
        """
        Test for Two new attributes - smoke test for rsWeight and propagate
        """
        name = rand_name("Guest:Role")
        description = rand_name("Guest description ")
        add_role = self.admin_client.add_role(name=name,
                                              description=description,
                                              propagate=True)
        # delete role after test completion
        self.addCleanup(self.admin_client.delete_role,
                        role_id=add_role.entity.id)
        self.assertEqual(add_role.status_code, 201,
                         msg="Response for add role is not 201.")
        self.assertTrue(add_role.entity.propagate,
                          msg='Role propagate value is not True')
