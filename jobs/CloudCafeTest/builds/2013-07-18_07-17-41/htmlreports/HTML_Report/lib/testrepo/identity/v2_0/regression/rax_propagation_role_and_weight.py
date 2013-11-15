from ccengine.common.tools.datagen import rand_name
from ccengine.common.tools.datagen import random_int
from testrepo.common.testfixtures.identity.v2_0.identity \
    import BaseIdentityFixture
from ccengine.common.decorators import attr


class RaxPropagationWeightTest(BaseIdentityFixture):
    @classmethod
    def setUpClass(cls):
        """
        Function to create test bed for all the test. Execute once at the
        beginning of class
        @param cls: instance of class
        """
        super(RaxPropagationWeightTest, cls).setUpClass()

        cls.useradminname = rand_name("ccuseradmin")
        cls.subusername = rand_name("ccsubuser")
        cls.email = '{0}@{1}'.format("testbox", "mailtrust.com")
        cls.password = "Gsubusrpass8"
        domain_id = random_int(10000, 1000000000)
        cls.auth_iden_adm_resp = cls.service_client.authenticate_user_password(
            cls.config.identity_api.admin_username,
            cls.config.identity_api.admin_password)
        cls.admin_client.token = cls.auth_iden_adm_resp.entity.token.id

        cls.servadminname = cls.config.identity_api.service_username
        cls.idenadminname = cls.config.identity_api.admin_username

        cls.user_adm_resp = cls.admin_client.add_user(
            username=cls.useradminname,
            email=cls.email,
            enabled=True,
            domainId=domain_id,
            password=cls.password)

        cls.auth_usr_adm_resp = cls.public_client.authenticate_user_password(
            cls.useradminname,
            cls.password)
        cls.public_client.token = cls.auth_usr_adm_resp.entity.token.id

        cls.sub_user = cls.public_client.add_user(username=cls.subusername,
                                                  email=cls.email,
                                                  enabled=True,
                                                  domainId=domain_id,
                                                  password=cls.password)

    @classmethod
    def tearDownClass(cls):
        """
        Function to clean up the data after execution of all the tests
        completed. Execute once at the end of all the tests.
        @param cls: instance of class
        """
        cls.admin_client.delete_user(userId=cls.sub_user.entity.id)
        cls.service_client.delete_user_hard(userId=cls.sub_user.entity.id)

        cls.admin_client.delete_user(userId=cls.user_adm_resp.entity.id)
        cls.service_client.delete_user_hard(userId=cls.user_adm_resp.entity.id)

        del cls.public_client.token
        del cls.admin_client.token

    def delete_role(self, role_id):
        del_role_resp = self.service_client.delete_role(roleId=role_id)
        self.assertEqual(del_role_resp.status_code,
                         204,
                         msg="Response is not 204")

    def role_deletion_from_user_testing_with_weight(self, client, username,
                                                    role):
        get_user_init = client.get_user_by_name(name=username)
        delete_role_from_user = client.delete_role_from_user(
            userId=get_user_init.entity.id,
            roleId=role.entity.id)
        self.assertEqual(delete_role_from_user.status_code,
                         204,
                         msg="Response is not 204")

        user_roles = client.list_user_global_roles(
            userId=get_user_init.entity.id)
        for user_role in user_roles.entity:
            self.assertNotEqual(user_role.name, role.entity.name,
                                msg="Role deletion from user failed")

    def role_deletion_from_user_testing_propagation(self, client, role,
                                                    propagation_flag):
        """
        Function to delete role from user and check propagation
        @param client: Admin or Service Client
        @param role: role object
        @param propagation_flag: True or False
        @return: None
        """
        get_user_init = client.get_user_by_name(name=self.useradminname)
        delete_role_from_user = client.delete_role_from_user(
            userId=get_user_init.entity.id,
            roleId=role.entity.id)
        self.assertEqual(delete_role_from_user.status_code,
                         204,
                         msg="Response code for role deletion from user is "
                             "not 204")

        user_roles = client.list_user_global_roles(
            userId=get_user_init.entity.id)
        for user_role in user_roles.entity:
            self.assertNotEqual(user_role.name, role.entity.name,
                                msg="Role deletion from user admin failed.")

        get_user_default_init = client.get_user_by_name(name=self.subusername)
        user_roles = client.list_user_global_roles(
            userId=get_user_default_init.entity.id)

        role_deleted = True
        for user_role in user_roles.entity:
            if user_role.name == role.entity.name:
                role_deleted = False

        self.assertEqual(role_deleted, propagation_flag,
                         msg="Role deletion should {0} for sub-user. However, "
                             "propagation flag is set as {0}".format(
                             role_deleted, propagation_flag))

    def role_assignment_with_weight_test_user_access(self, client, weight,
                                                     username,
                                                     propagation_flag=False):
        if client == self.public_client:
            # Roles cannot be created by User Admin's, so client overwritten
            role = self.add_role_test(client=self.admin_client,
                                      propagation_flag=propagation_flag,
                                      weight=weight)
        else:
            role = self.add_role_test(client,
                                      propagation_flag=propagation_flag,
                                      weight=weight)
        self.add_role_to_user_test(role=role,
                                   client=client,
                                   username=username)
        return role

    def add_role_test(self, client, propagation_flag=False, weight=1000):
        name = rand_name("Guest:Role")
        description = rand_name("Guest description ")
        add_role = client.add_role(name=name,
                                   description=description,
                                   propagate=propagation_flag,
                                   weight=weight)
        self.assertEqual(add_role.status_code,
                         201,
                         msg="Response for add role is not 201")
        # Delete role at the end of test, not depend on failure in test
        self.addCleanup(self.delete_role, add_role.entity.id)
        self.assertEquals(add_role.entity.weight,
                          str(weight),
                          msg='User weight expected {0} but received {1}'.
                          format(weight, add_role.entity.weight))
        self.assertEquals(add_role.entity.propagate,
                          str(propagation_flag).lower(),
                          msg='User propagate received {0}'.format(
                              add_role.entity.propagate))
        return add_role

    def add_role_to_user_test(self, role, client, username):
        get_user_init = client.get_user_by_name(name=username)
        add_role_to_user = client.add_role_to_user(
            userId=get_user_init.entity.id,
            roleId=role.entity.id)

        # In api docs the add role to user response is 201 - pravin
        normal_response_codes = [200, 201]
        self.assertIn(
            add_role_to_user.status_code,
            normal_response_codes,
            msg='Add role to user response expected {0} received {1}'.
            format(normal_response_codes, add_role_to_user.status_code))

        user_roles = client.list_user_global_roles(
            userId=get_user_init.entity.id)
        role_added_to_user = False
        for user_role in user_roles.entity:
            if user_role.name == role.entity.name:
                role_added_to_user = True
        self.assertTrue(role_added_to_user, msg="Role Assignment to {0} "
                                                "failed".format(username))
        return add_role_to_user

    def role_propagation_test_assigning(self, client, propagation_flag,
                                        weight=None):
        role = self.add_role_test(client,
                                  propagation_flag=propagation_flag,
                                  weight=weight)
        self.add_role_to_user_test(role=role,
                                   client=client,
                                   username=self.useradminname)
        user_roles = client.list_user_global_roles(
            userId=self.sub_user.entity.id)

        role_added_to_user = False
        for user_role in user_roles.entity:
            if user_role.name == role.entity.name:
                role_added_to_user = True

        if propagation_flag is True:
            self.assertTrue(role_added_to_user,
                            msg="Role not propagated to sub user when "
                                "propagation flag set to {0}".
                            format(propagation_flag))
        else:
            self.assertFalse(role_added_to_user,
                             msg="Role propagated to sub user when "
                                 "propagation flag set to {0}".
                             format(propagation_flag))

            self.add_role_to_user_test(role=role,
                                       client=client,
                                       username=self.subusername)

        return role

    @attr('regression', type='positive')
    def test_44731_verify_delete_role_test_propagation_flag_not_valid(self):
        """
        Verifying deleting a role removes the role from all the assigned user
        and also make sure that setting propagation flag = False not affects
        the removal of role from the sub-users
        """
        username_list = [self.subusername, self.useradminname,
                         self.idenadminname, self.servadminname]
        weight_list = [0, 100, 500, 1000, 2000]
        for weight in weight_list:
            propagation_flag_list = [True, False]
            for propagation_flag in propagation_flag_list:
                for username in username_list:
                    role = self.add_role_test(
                        client=self.service_client,
                        propagation_flag=propagation_flag,
                        weight=weight)
                    self.add_role_to_user_test(role=role,
                                               client=self.service_client,
                                               username=username)
                role_name = role.entity.name
                self.delete_role(role_id=role.entity.id)
                for username in username_list:
                    get_user_init = self.service_client.get_user_by_name(
                        name=username)
                    user_roles = self.service_client.list_user_global_roles(
                        userId=get_user_init.entity.id)
                    for user_role in user_roles.entity:
                        self.assertNotEqual(user_role.name, role_name,
                                            msg="Role not removed from user")
                # Remove added clean up from _cleanups as deletion of
                #  role is successful
                self._cleanups.pop(-1)

    @attr('regression', type='positive')
    def test_44731_verify_add_role_with_weight(self):

        test_values = {self.service_client: [0, 100, 500, 1000, 2000],
                       self.admin_client: [100, 500, 1000, 2000]}

        client_keys = test_values.keys()
        for client in client_keys:
            weight_list = test_values[client]
            for weight in weight_list:
                self.add_role_test(client=client,
                                   weight=weight)

    @attr('regression', type='positive')
    def test_44731_verify_add_role_with_weight_and_propagation(self):
        propagation_flag_list = [True, False]
        test_values = {self.service_client: [0, 100, 500, 1000, 2000],
                       self.admin_client: [100, 500, 1000, 2000]}

        for propagation_flag in propagation_flag_list:
            client_keys = test_values.keys()

            for client in client_keys:
                weight_list = test_values[client]
                for weight in weight_list:
                    self.add_role_test(client=client,
                                       weight=weight,
                                       propagation_flag=propagation_flag)

    @attr('regression', type='positive')
    def test_44731_verify_assigning_role_with_propagation(self):
        test_values = {self.service_client: [True, False],
                       self.admin_client: [True, False]}

        client_keys = test_values.keys()
        for client in client_keys:
            prop_flag_list = test_values[client]
            for propagation_flag in prop_flag_list:
                self.role_propagation_test_assigning(
                    client=client,
                    propagation_flag=propagation_flag,
                    weight=500)

    @attr('regression', type='positive')
    def test_44731_verify_assigning_and_deleting_role_with_weight(self):
        client_list = [self.service_client,
                       self.admin_client,
                       self.public_client]
        test_values = {0: [self.idenadminname,
                           self.useradminname,
                           self.subusername],
                       100: [self.useradminname,
                             self.subusername],
                       500: [self.useradminname,
                             self.subusername],
                       1000: [self.subusername],
                       2000: [self.subusername]}

        for client in client_list:
            # Don't change this sequence and client_list
            if client == self.admin_client:
                test_values.pop(0)
            if client == self.public_client:
                test_values.pop(100)
                test_values.pop(500)
            weight_list = test_values.keys()

            for weight in weight_list:
                users_list = test_values[weight]
                for username in users_list:
                    role = self.role_assignment_with_weight_test_user_access(
                        client=client,
                        weight=weight,
                        username=username)

                    # User Admin clients are hard coded with Admin Clients
                    # because User admins cannot delete role from the user
                    if client == self.public_client:
                        self.role_deletion_from_user_testing_with_weight(
                            client=self.admin_client,
                            username=username,
                            role=role)
                    else:
                        self.role_deletion_from_user_testing_with_weight(
                            client=client,
                            username=username,
                            role=role)

    @attr('regression', type='positive')
    def test_44731_verify_delete_role_from_user_testing_propagation(self):
        test_values = {self.service_client: [True, False],
                       self.admin_client: [True, False]}

        client_keys = test_values.keys()
        for client in client_keys:
            prop_flag_list = test_values[client]
            for propagation_flag in prop_flag_list:
                role = self.role_propagation_test_assigning(
                    client=client,
                    propagation_flag=propagation_flag,
                    weight=500)

                # User Admin clients are hard coded with Admin Clients
                # because User admins cannot delete role from the user
                if client == self.public_client:
                    self.role_deletion_from_user_testing_propagation(
                        client=self.admin_client,
                        role=role,
                        propagation_flag=propagation_flag)
                else:
                    self.role_deletion_from_user_testing_propagation(
                        client=client,
                        role=role,
                        propagation_flag=propagation_flag)

    @attr('regression', type='positive')
    def test_44731_verify_delete_role(self):
        """
        Test for creating/deleting role with different weight,
        client and propagation
        """
        test_values = {self.service_client: [0, 100, 500, 1000, 2000],
                       self.admin_client: [100, 500, 1000, 2000]}
        failures = []
        propagation_flag_list = [True, False]
        for propagation_flag in propagation_flag_list:
            client_keys = test_values.keys()

            for client in client_keys:
                weight_list = test_values[client]
                for weight in weight_list:
                    role = self.add_role_test(
                        client=client,
                        weight=weight,
                        propagation_flag=propagation_flag)
                    delete_role = client.delete_role(role.entity.id)
                    if delete_role.status_code != 204:
                        failures.append("Role deletion failed with client="
                                        "{0}, weight={1} and propagation="
                                        "{2}".format(client,
                                                     weight,
                                                     propagation_flag))
                    else:
                        # Remove added clean up from _cleanups as deletion of
                        #  role is successful
                        self._cleanups.pop(-1)
        self.assertListEqual(failures, [], msg="Role deletion failed.")
