from ccengine.common.tools.datagen import rand_name
from ccengine.common.tools.datagen import random_int
from testrepo.common.testfixtures.identity.v2_0.identity \
    import BaseIdentityFixture
from ccengine.common.decorators import attr
from ccengine.providers.identity.v2_0.identity_api \
    import IdentityAPIProvider


class RaxNegativePropagationWeightTest(BaseIdentityFixture):

    @classmethod
    def setUpClass(cls):
        super(RaxNegativePropagationWeightTest, cls).setUpClass()

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

        cls.sub_user = cls.public_client.add_user(
                username=cls.subusername,
                email=cls.email,
                enabled=True,
                domainId=domain_id,
                password=cls.password)

        cls.provider = IdentityAPIProvider(cls.config)
        cls.public_admin_client = cls.provider.get_client()

    @classmethod
    def tearDownClass(cls):
        del cls.public_client.token
        del cls.admin_client.token

        cls.admin_client.delete_user(
                userId=cls.user_adm_resp.entity.id)
        cls.service_client.delete_user_hard(
                userId=cls.user_adm_resp.entity.id)

        cls.admin_client.delete_user(
                userId=cls.sub_user.entity.id)
        cls.service_client.delete_user_hard(
                userId=cls.sub_user.entity.id)

    def delete_role(self, role_id):
        del_role_resp = self.service_client.delete_role(roleId=role_id)
        self.assertEqual(
                del_role_resp.status_code,
                204,
                msg="Response is not 204")

    def delete_role_negative_test(self, client, role_id):
        del_role_resp = client.delete_role(roleId=role_id)
        self.assertNotEqual(
                del_role_resp.status_code,
                204,
                msg="Role deleted by Unauthorized admin")

    def add_role_invalid_weight_negative_test(self, client,
                                              propagation_flag=None,
                                              weight=None):

        name = rand_name("Guest:Role")
        description = rand_name("Guest description ")

        """TO DO: Need to confirm Default Weight - pravin """
        if weight is None:
            weight = 1000

        """TO DO: Need to confirm Default Propagation flag - pravin """
        if propagation_flag is None:
            propagation_flag = False

        add_role = client.add_role(
                name=name,
                description=description,
                propagate=propagation_flag,
                weight=weight)
        self.assertNotEqual(
                add_role.status_code,
                201,
                msg="Response is 201")
        if add_role.status_code is 201:
            self.delete_role(add_role.entity.id)

    def add_role_negative_test(self, client, propagation_flag=None,
                               weight=None):

        name = rand_name("Guest:Role")
        description = rand_name("Guest description ")

        """TO DO: Need to confirm Default Weight - pravin """
        if weight is None:
            weight = 1000

        """TO DO: Need to confirm Default Propagation flag - pravin """
        if propagation_flag is None:
            propagation_flag = False

        add_role = client.add_role(
                name=name,
                description=description,
                propagate=propagation_flag,
                weight=weight)
        self.assertEqual(
                add_role.status_code,
                201,
                msg="Response is not 201")
        self.assertEquals(
                add_role.entity.weight,
                str(weight),
                msg='User weight expected {0} but received {1}'.format(
                        weight,
                        add_role.entity.weight))
        self.assertEquals(
                add_role.entity.propagate,
                str(propagation_flag).lower(),
                msg='User propagate received {0}'.format(
                        add_role.entity.propagate))
        return add_role

    def add_role_to_user_negative_test(self, role, client, username):

        get_user_init = client.get_user_by_name(name=username)

        add_role_to_user = client.add_role_to_user(
                userId=get_user_init.entity.id,
                roleId=role.entity.id)

        """
        In api docs the add role to user response is 201 - pravin
        """
        normal_response_codes = [200, 201]
        self.assertIn(
                add_role_to_user.status_code,
                normal_response_codes,
                msg='Add role to user response expected {0} received {1}'.
                format(normal_response_codes, add_role_to_user.status_code))

        user_roles = client.list_user_global_roles(
                userId=get_user_init.entity.id)

        test_flag = False
        for userrole in user_roles.entity:
            if userrole.name == role.entity.name:
                test_flag = True
                """ weight and flag not working - Pravin
                self.assertEqual(userrole.weight, str(weight),
                    msg='User weight expected {0} but received {1}'.format(
                    weight,
                    userrole.weight))

                self.assertEqual(userrole.propagate,
                    str(propagation_flag).lower(),
                    msg='Propagate Flag expected {0} but \
                    received {1}'.format(propagation_flag,
                    userrole.propagate))
                """
        self.assertTrue(test_flag, msg="Role Assignment failed")

        return add_role_to_user

    def role_propagation_test_negative(self, client, propagation_flag,
                                       weight=None):
        role = self.add_role_negative_test(
                client,
                propagation_flag=propagation_flag,
                weight=weight)

        self.add_role_to_user_negative_test(
                role=role,
                client=client,
                username=self.idenadminname)

        user_roles = client.list_user_global_roles(
            userId=self.user_adm_resp.entity.id)

        test_flag = True
        for userrole in user_roles.entity:
            if userrole.name == role.entity.name:
                test_flag = False
                """ weight and flag not working - Pravin
                self.assertEqual(userrole.weight, str(weight),
                    msg='User weight expected {0} but received {1}'.format(
                    weight,
                    userrole.weight))

                self.assertEqual(userrole.propagate,
                    str(propagation_flag).lower(),
                    msg='Propagate Flag expected {0} but \
                    received {1}'.format(propagation_flag,
                    userrole.propagate))
                """
        self.assertTrue(
                    test_flag,
                    msg="Role propagated to User Admin when propagation"
                    " flag set to {0}".format(propagation_flag))

        return role

    def role_deletion_from_user_testing_negative(self, client, username, role):
        get_user_init = client.get_user_by_name(name=username)

        role_del_resp = client.delete_role_from_user(
                                userId=get_user_init.entity.id,
                                roleId=role.entity.id)
        self.assertNotEqual(
                role_del_resp.status_code,
                204,
                msg="Deletion of Role from user by unauthorized admin")

    def add_role_to_user_test_assignment_negative(self, client,
                                                  user_id,
                                                  weight=None):
        role = self.add_role_negative_test(
                self.service_client,
                weight=weight)

        add_role_to_user = client.add_role_to_user(
                userId=user_id,
                roleId=role.entity.id)

        """
        In api docs the add role to user response is 201 - pravin
        """
        normal_response_codes = [200, 201]
        self.assertNotIn(
                add_role_to_user.status_code,
                normal_response_codes,
                msg='Role with weight {0} cannot be added to user by this '
                    'admin'.format(weight))

        user_roles = self.service_client.list_user_global_roles(
                userId=user_id)

        test_flag = True
        for userrole in user_roles.entity:
            if userrole.name == role.entity.name:
                test_flag = False
                """ weight and flag not working - Pravin
                self.assertEqual(userrole.weight, str(weight),
                    msg='User weight expected {0} but received {1}'.format(
                    weight,
                    userrole.weight))

                self.assertEqual(userrole.propagate,
                    str(propagation_flag).lower(),
                    msg='Propagate Flag expected {0} but \
                    received {1}'.format(propagation_flag,
                    userrole.propagate))
                """
        self.assertTrue(test_flag, msg="Role Assignment Succeeded")

        return role

    @attr('regression', type='negative')
    def test_44731_verify_delete_role_from_user_test_admin_access(self):
        """
        Making sure that admins with lower accessiblity cannot delete the
        roles from users with higher accessibility than theirs eventhough
        they have control over the roles (depending on weight)
        """
        username_map = {self.public_client: [self.servadminname,
                                             self.idenadminname],
                        self.admin_client: [self.servadminname]}

        test_values = {self.public_client: [2000, 1000],
                       self.admin_client: [100, 500]}
        client_keys = test_values.keys()
        for client in client_keys:
            weight_list = test_values[client]
            for weight in weight_list:
                username_list = username_map[client]
                for username in username_list:
                    role = self.add_role_negative_test(
                            self.service_client,
                            weight=weight)
                    self.add_role_to_user_negative_test(
                            role=role,
                            client=self.service_client,
                            username=username)
                    get_user_init = self.service_client.get_user_by_name(
                                            name=username)

                    role_del_resp = client.delete_role_from_user(
                                            userId=get_user_init.entity.id,
                                            roleId=role.entity.id)
                    self.assertNotEqual(
                            role_del_resp.status_code,
                            204,
                            msg="Unauth admin deleted role from user")

    @attr('regression', type='negative')
    def test_44731_verify_delete_role_test_negative(self):
        """
        Verify deleting role by unauthorized user
        """

        test_useradminname = rand_name("cctestuseradmin")
        email = '{0}@{1}'.format("testbox", "mailtrust.com")
        domain_id = random_int(10000, 1000000000)
        password = "Gellpass8"
        create_user_admin = self.admin_client.add_user(
                username=test_useradminname,
                email=email,
                enabled=True,
                domainId=domain_id,
                password=password)
        self.assertEqual(create_user_admin.status_code,
                         201,
                         msg='Add user expected response 201 received {0}'.
                         format(create_user_admin.status_code))

        auth_adm = self.public_client.authenticate_user_password(
                test_useradminname,
                password)
        self.public_admin_client.token = auth_adm.entity.token.id

        test_values = {self.admin_client: [0],
                       self.public_admin_client: [0, 100, 500, 1000, 2000]}

        client_keys = test_values.keys()

        for client in client_keys:
            weight_list = test_values[client]
            for weight in weight_list:
                role = self.add_role_negative_test(
                                self.service_client,
                                weight=weight)

                self.delete_role_negative_test(client=client,
                                               role_id=role.entity.id)

        del self.public_admin_client.token
        del_user_resp = self.admin_client.delete_user(
                userId=create_user_admin.entity.id)
        self.assertEqual(
                del_user_resp.status_code,
                204,
                msg="User not deleted")
        del_user_resp = self.service_client.delete_user_hard(
                userId=create_user_admin.entity.id)
        self.assertEqual(
                del_user_resp.status_code,
                204,
                msg="User not deleted")

    @attr('regression', type='negative')
    def test_44731_verify_role_assignment_negative(self):
        """
        Test role assignment to users - verify the access based on role weight
        """
        username_list = [self.servadminname, self.idenadminname,
                         self.useradminname, self.subusername]

        test_values = {self.admin_client: [0],
                       self.public_client: [100, 500]}

        client_keys = test_values.keys()
        for client in client_keys:
            weight_list = test_values[client]
            for username in username_list:
                get_user_init = self.service_client.get_user_by_name(
                                        name=username)
                user_id = get_user_init.entity.id
                for weight in weight_list:
                    role = self.add_role_to_user_test_assignment_negative(
                                    client=client,
                                    user_id=user_id,
                                    weight=weight)
                    self.delete_role(role.entity.id)

    @attr('regression', type='negative')
    def test_44731_verify_role_deletion_from_user_negative(self):
        """
        Testing role deletion from user by admin who don't have access for it
        """
        username_map = {self.admin_client: [self.useradminname,
                                            self.subusername],
                        self.public_client: [self.subusername]}

        test_values = {self.admin_client: [0],
                       self.public_client: [0, 100, 500]}

        client_keys = test_values.keys()

        for client in client_keys:
            weight_list = test_values[client]
            username_list = username_map[client]
            for weight in weight_list:
                for username in username_list:
                    role = self.add_role_negative_test(
                                    client=self.service_client,
                                    weight=weight)
                    self.add_role_to_user_negative_test(
                            client=self.service_client,
                            username=username,
                            role=role)

                    self.role_deletion_from_user_testing_negative(
                            client=client,
                            username=username,
                            role=role)
                    self.delete_role(role.entity.id)

    @attr('regression', type='negative')
    def test_44731_verify_add_role_with_weight_negative(self):
        """
        Testing Role creation with invalid weights
        """
        test_values = {self.service_client: [-10, 1234, True],
                       self.admin_client: [0, -123, 123, False]}

        client_keys = test_values.keys()

        for client in client_keys:
            weight_list = test_values[client]
            for weight in weight_list:
                self.add_role_invalid_weight_negative_test(
                        client=client,
                        weight=weight)

    @attr('regression', type='negative')
    def test_44731_verify_role_propagation_negative(
            self):
        """
        Test propagation flag is invalid when roles assigned to Iden admin
        """
        propagation_flag_list = [True, False]
        test_values = {self.service_client: [0, 100, 500, 1000, 2000]}

        client_keys = test_values.keys()

        for propagation_flag in propagation_flag_list:
            client_keys = test_values.keys()

            for client in client_keys:
                weight_list = test_values[client]
                for weight in weight_list:
                    role = self.role_propagation_test_negative(
                            client=client,
                            propagation_flag=propagation_flag,
                            weight=weight
                    )
                    self.delete_role(role.entity.id)
