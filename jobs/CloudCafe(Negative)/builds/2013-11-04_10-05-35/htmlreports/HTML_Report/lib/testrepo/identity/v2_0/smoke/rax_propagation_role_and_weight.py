from ccengine.common.tools.datagen import rand_name
from ccengine.common.tools.datagen import random_int
from testrepo.common.testfixtures.identity.v2_0.identity \
    import BaseIdentityFixture
from ccengine.common.decorators import attr
from ccengine.providers.identity.v2_0.identity_api \
    import IdentityAPIProvider


class RaxPropagationWeightTest(BaseIdentityFixture):

    @classmethod
    def setUpClass(cls):
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

    @attr('smoke', type='positive')
    def test_44731_verify_add_with_propagation(self):
        name = rand_name("Guest:Role")
        description = rand_name("Guest description ")
        propagation_flag = True
        add_role = self.admin_client.add_role(
                name=name,
                description=description,
                propagate=propagation_flag)
        self.assertEqual(
                add_role.status_code,
                201,
                msg="Response is not 201")
        delete_role = self.service_client.delete_role(add_role.entity.id)
        self.assertEqual(
                delete_role.status_code,
                204,
                msg="Response is not 204")

    @attr('smoke', type='positive')
    def test_44731_verify_add_role_with_weight(self):

        name = rand_name("Guest:Role")
        description = rand_name("Guest description ")
        weight = 500
        add_role = self.admin_client.add_role(
                name=name,
                description=description,
                weight=weight)
        self.assertEqual(
                add_role.status_code,
                201,
                msg="Response is not 201")
        delete_role = self.service_client.delete_role(add_role.entity.id)
        self.assertEqual(
                delete_role.status_code,
                204,
                msg="Response is not 204")

    @attr('smoke', type='positive')
    def test_44731_verify_add_role_with_weight_and_propagation(self):

        name = rand_name("Guest:Role")
        description = rand_name("Guest description ")
        propagation_flag = True
        weight = 500
        add_role = self.admin_client.add_role(
                name=name,
                description=description,
                propagate=propagation_flag,
                weight=weight)
        self.assertEqual(
                add_role.status_code,
                201,
                msg="Response is not 201")
        delete_role = self.service_client.delete_role(add_role.entity.id)
        self.assertEqual(
                delete_role.status_code,
                204,
                msg="Response is not 204")

    @attr('smoke', type='positive')
    def test_44731_verify_assigning_role_with_weight(self):

        name = rand_name("Guest:Role")
        description = rand_name("Guest description ")
        weight = 500
        add_role = self.admin_client.add_role(
                name=name,
                description=description,
                weight=weight)
        self.assertEqual(
                add_role.status_code,
                201,
                msg="Response is not 201")

        get_user_init = self.admin_client.get_user_by_name(
                name=self.useradminname)
        add_role_to_user = self.admin_client.add_role_to_user(
                userId=get_user_init.entity.id,
                roleId=add_role.entity.id)

        normal_response_codes = [200, 201]
        self.assertIn(
                add_role_to_user.status_code,
                normal_response_codes,
                msg='Add role to user response expected {0} received {1}'.
                format(normal_response_codes, add_role_to_user.status_code))

        delete_role = self.service_client.delete_role(add_role.entity.id)
        self.assertEqual(
                delete_role.status_code,
                204,
                msg="Response is not 204")

    @attr('smoke', type='positive')
    def test_44731_verify_assigning_role_with_propagation(self):

        name = rand_name("Guest:Role")
        description = rand_name("Guest description ")
        propagation_flag = True
        add_role = self.admin_client.add_role(
                name=name,
                description=description,
                propagate=propagation_flag)
        self.assertEqual(
                add_role.status_code,
                201,
                msg="Response is not 201")

        get_user_init = self.admin_client.get_user_by_name(
                name=self.useradminname)
        add_role_to_user = self.admin_client.add_role_to_user(
                userId=get_user_init.entity.id,
                roleId=add_role.entity.id)

        normal_response_codes = [200, 201]
        self.assertIn(
                add_role_to_user.status_code,
                normal_response_codes,
                msg='Add role to user response expected {0} received {1}'.
                format(normal_response_codes, add_role_to_user.status_code))

        delete_role = self.service_client.delete_role(add_role.entity.id)
        self.assertEqual(
                delete_role.status_code,
                204,
                msg="Response is not 204")

    @attr('smoke', type='positive')
    def test_44731_verify_assigning_role_with_weight_and_propagation(self):

        name = rand_name("Guest:Role")
        description = rand_name("Guest description ")
        weight = 500
        propagation_flag = True
        add_role = self.admin_client.add_role(
                name=name,
                description=description,
                weight=weight,
                propagate=propagation_flag)
        self.assertEqual(
                add_role.status_code,
                201,
                msg="Response is not 201")

        get_user_init = self.admin_client.get_user_by_name(
                name=self.useradminname)
        add_role_to_user = self.admin_client.add_role_to_user(
                userId=get_user_init.entity.id,
                roleId=add_role.entity.id)

        normal_response_codes = [200, 201]
        self.assertIn(
                add_role_to_user.status_code,
                normal_response_codes,
                msg='Add role to user response expected {0} received {1}'.
                format(normal_response_codes, add_role_to_user.status_code))

        delete_role = self.service_client.delete_role(add_role.entity.id)
        self.assertEqual(
                delete_role.status_code,
                204,
                msg="Response is not 204")

    @attr('smoke', type='positive')
    def test_44731_verify_delete_role_from_user_by_service_admin(self):

        name = rand_name("Guest:Role")
        description = rand_name("Guest description ")
        weight = 0
        client_name_list = [self.idenadminname,
                            self.useradminname]
        for client_name in client_name_list:
            propagation_flag_list = [False, True]
            for propagation_flag in propagation_flag_list:
                add_role = self.service_client.add_role(
                        name=name,
                        description=description,
                        weight=weight,
                        propagate=propagation_flag)
                self.assertEqual(
                        add_role.status_code,
                        201,
                        msg="Response is not 201")

                get_user_init = self.service_client.get_user_by_name(
                        name=client_name)
                add_role_to_user = self.service_client.add_role_to_user(
                        userId=get_user_init.entity.id,
                        roleId=add_role.entity.id)

                normal_response_codes = [200, 201]
                self.assertIn(
                        add_role_to_user.status_code,
                        normal_response_codes,
                        msg='Add role to user response expected {0} recv {1}'.
                        format(normal_response_codes,
                               add_role_to_user.status_code))

                delete_resp = self.service_client.delete_role_from_user(
                        userId=get_user_init.entity.id,
                        roleId=add_role.entity.id)

                self.assertEqual(
                        delete_resp.status_code,
                        204,
                        msg="Response is not 204")

                delete_role = self.service_client.delete_role(
                        add_role.entity.id)
                self.assertEqual(
                        delete_role.status_code,
                        204,
                        msg="Response is not 204")

    @attr('smoke', type='positive')
    def test_44731_verify_delete_role_from_user_by_identity_admin(self):

        name = rand_name("Guest:Role")
        description = rand_name("Guest description ")
        weight = 500
        propagation_flag_list = [False, True]
        for propagation_flag in propagation_flag_list:
            add_role = self.admin_client.add_role(
                    name=name,
                    description=description,
                    weight=weight,
                    propagate=propagation_flag)
            self.assertEqual(
                    add_role.status_code,
                    201,
                    msg="Response is not 201")

            get_user_init = self.admin_client.get_user_by_name(
                    name=self.useradminname)
            add_role_to_user = self.admin_client.add_role_to_user(
                    userId=get_user_init.entity.id,
                    roleId=add_role.entity.id)

            normal_response_codes = [200, 201]
            self.assertIn(
                    add_role_to_user.status_code,
                    normal_response_codes,
                    msg='Add role to user response expected {0} received {1}'.
                    format(normal_response_codes,
                           add_role_to_user.status_code))

            delete_role_from_user = self.admin_client.delete_role_from_user(
                    userId=get_user_init.entity.id,
                    roleId=add_role.entity.id)

            self.assertEqual(
                    delete_role_from_user.status_code,
                    204,
                    msg="Response is not 204")

            delete_role = self.service_client.delete_role(add_role.entity.id)
            self.assertEqual(
                    delete_role.status_code,
                    204,
                    msg="Response is not 204")

    @attr('smoke', type='positive')
    def test_44731_verify_delete_role_from_user_by_user_admin(self):

        name = rand_name("Guest:Role")
        description = rand_name("Guest description ")
        weight = 1000
        propagation_flag_list = [False, True]
        for propagation_flag in propagation_flag_list:
            add_role = self.admin_client.add_role(
                    name=name,
                    description=description,
                    weight=weight,
                    propagate=propagation_flag)
            self.assertEqual(
                    add_role.status_code,
                    201,
                    msg="Response is not 201")

            get_user_init = self.admin_client.get_user_by_name(
                    name=self.subusername)
            add_role_to_user = self.public_client.add_role_to_user(
                    userId=get_user_init.entity.id,
                    roleId=add_role.entity.id)

            normal_response_codes = [200, 201]
            self.assertIn(
                    add_role_to_user.status_code,
                    normal_response_codes,
                    msg='Add role to user response expected {0} received {1}'.
                    format(normal_response_codes,
                           add_role_to_user.status_code))

            delete_role_from_user = self.public_client.delete_role_from_user(
                    userId=get_user_init.entity.id,
                    roleId=add_role.entity.id)

            self.assertEqual(
                    delete_role_from_user.status_code,
                    204,
                    msg="Response is not 204")

            delete_role = self.service_client.delete_role(add_role.entity.id)
            self.assertEqual(
                    delete_role.status_code,
                    204,
                    msg="Response is not 204")

    @attr('smoke', type='positive')
    def test_44731_verify_delete_role_service_admin(self):

        name = rand_name("Guest:Role")
        description = rand_name("Guest description ")
        weight = 0
        propagation_flag_list = [False, True]
        for propagation_flag in propagation_flag_list:
            add_role = self.service_client.add_role(
                    name=name,
                    description=description,
                    weight=weight,
                    propagate=propagation_flag)
            self.assertEqual(
                    add_role.status_code,
                    201,
                    msg="Response is not 201")

            delete_role = self.service_client.delete_role(add_role.entity.id)
            self.assertEqual(
                    delete_role.status_code,
                    204,
                    msg="Response is not 204")

    @attr('smoke', type='positive')
    def test_44731_verify_delete_role_identity_admin(self):

        name = rand_name("Guest:Role")
        description = rand_name("Guest description ")
        weight = 1000
        propagation_flag_list = [False, True]
        for propagation_flag in propagation_flag_list:
            add_role = self.admin_client.add_role(
                    name=name,
                    description=description,
                    weight=weight,
                    propagate=propagation_flag)
            self.assertEqual(
                    add_role.status_code,
                    201,
                    msg="Response is not 201")

            delete_role = self.admin_client.delete_role(add_role.entity.id)
            self.assertEqual(
                    delete_role.status_code,
                    204,
                    msg="Response is not 204")

    @attr('smoke', type='negative')
    def test_44731_verify_add_role_test_identity_admin(self):
        """
        Making sure that admins with lower accessiblity cannot add the
        roles which requires higher access rights
        """
        name = rand_name("Guest:Role")
        description = rand_name("Guest description ")
        weight = 0
        propagation_flag_list = [True, False]
        for propagation_flag in propagation_flag_list:
            add_role = self.admin_client.add_role(
                    name=name,
                    description=description,
                    weight=weight,
                    propagate=propagation_flag)
            self.assertNotEqual(
                    add_role.status_code,
                    201,
                    msg="Response is not 201")

    @attr('smoke', type='negative')
    def test_44731_verify_add_role_test_user_admin(self):
        """
        Making sure that admins with lower accessiblity cannot add the
        roles which requires higher access rights
        """
        name = rand_name("Guest:Role")
        description = rand_name("Guest description ")
        weight_list = [500, 100]
        propagation_flag_list = [True, False]
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
        self.assertEqual(
                create_user_admin.status_code,
                201,
                msg='Add user expected response 201 received {0}'.format(
                    create_user_admin.status_code))

        auth_adm = self.public_client.authenticate_user_password(
                test_useradminname,
                password)
        self.public_admin_client.token = auth_adm.entity.token.id
        for propagation_flag in propagation_flag_list:
            for weight in weight_list:
                add_role = self.public_admin_client.add_role(
                        name=name,
                        description=description,
                        weight=weight,
                        propagate=propagation_flag)
                self.assertNotEqual(
                        add_role.status_code,
                        201,
                        msg="Response is not 201")

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

    @attr('smoke', type='negative')
    def test_44731_verify_delete_role_test_admin_access(self):
        """
        Making sure that admins with lower accessiblity cannot delete the
        roles which requires higher access rights
        """
        name = rand_name("Guest:Role")
        description = rand_name("Guest description ")
        weight = 0
        propagation_flag_list = [True, False]
        for propagation_flag in propagation_flag_list:

            add_role = self.service_client.add_role(
                    name=name,
                    description=description,
                    weight=weight,
                    propagate=propagation_flag)
            self.assertEqual(
                    add_role.status_code,
                    201,
                    msg="Response is not 201")

            delete_role = self.admin_client.delete_role(add_role.entity.id)
            self.assertNotEqual(
                    delete_role.status_code,
                    204,
                msg="Response is not 204")
            delete_role = self.service_client.delete_role(add_role.entity.id)
            self.assertEqual(
                    delete_role.status_code,
                    204,
                    msg="Response is not 204")

    @attr('smoke', type='negative')
    def test_44731_verify_delete_role_test_user_admin(self):
        """
        Making sure that admins with lower accessiblity cannot delete the
        roles which requires higher access rights
        """
        name = rand_name("Guest:Role")
        description = rand_name("Guest description ")
        weight_list = [0, 500, 100, 1000, 2000]
        propagation_flag_list = [True, False]
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
        self.assertEqual(
                create_user_admin.status_code,
                201,
                msg='Add user expected response 201 received {0}'.format(
                    create_user_admin.status_code))

        auth_adm = self.public_client.authenticate_user_password(
                test_useradminname,
                password)
        self.public_admin_client.token = auth_adm.entity.token.id
        for propagation_flag in propagation_flag_list:
            for weight in weight_list:
                add_role = self.service_client.add_role(
                        name=name,
                        description=description,
                        weight=weight,
                        propagate=propagation_flag)
                self.assertEqual(
                        add_role.status_code,
                        201,
                        msg="Response is not 201")
                delete_role = self.public_admin_client.delete_role(
                        add_role.entity.id)
                self.assertNotEqual(
                        delete_role.status_code,
                        204,
                        msg="Response is not 204")
                delete_role = self.service_client.delete_role(
                        add_role.entity.id)
                self.assertEqual(
                        delete_role.status_code,
                        204,
                        msg="Response is not 204")

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

    @attr('smoke', type='negative')
    def test_44731_verify_add_role_to_user_test_identity_admin(self):
        """
        Verifying Identity admin cannot add role to Service admin
        """
        name = rand_name("Guest:Role")
        description = rand_name("Guest description ")
        weight_list = [500, 100, 1000, 2000]
        propagation_flag_list = [True, False]
        get_user_init = self.service_client.get_user_by_name(
                name=self.servadminname)
        for propagation_flag in propagation_flag_list:
            for weight in weight_list:
                add_role = self.admin_client.add_role(
                        name=name,
                        description=description,
                        weight=weight,
                        propagate=propagation_flag)
                add_role_to_user = self.admin_client.add_role_to_user(
                        userId=get_user_init.entity.id,
                        roleId=add_role.entity.id)
                normal_response_codes = [200, 201]
                self.assertNotIn(
                        add_role_to_user.status_code,
                        normal_response_codes,
                        msg='Identity admin adding role to Service admin '
                            'status code received {0}'.
                        format(add_role_to_user.status_code))
                delete_role = self.admin_client.delete_role(add_role.entity.id)
                self.assertEqual(
                        delete_role.status_code,
                        204,
                        msg="Response is not 204")

    @attr('smoke', type='negative')
    def test_44731_verify_add_role_to_user_test_user_admin(self):
        """
        Verifying User admin cannot add role to the identity admin
        """
        name = rand_name("Guest:Role")
        description = rand_name("Guest description ")
        weight_list = [1000, 2000]
        client_name_list = [self.idenadminname, self.servadminname]
        for client_name in client_name_list:
            propagation_flag_list = [True, False]
            get_user_init = self.service_client.get_user_by_name(
                    name=client_name)
            for propagation_flag in propagation_flag_list:
                for weight in weight_list:
                    add_role = self.admin_client.add_role(
                            name=name,
                            description=description,
                            weight=weight,
                            propagate=propagation_flag)
                    add_role_to_user = self.public_client.add_role_to_user(
                            userId=get_user_init.entity.id,
                            roleId=add_role.entity.id)
                    normal_response_codes = [200, 201]
                    self.assertNotIn(
                            add_role_to_user.status_code,
                            normal_response_codes,
                            msg='User admin adding role to Identity admin '
                                'status code received {0}'.
                            format(add_role_to_user.status_code))
                    delete_role = self.admin_client.delete_role(
                            add_role.entity.id)
                    self.assertEqual(
                            delete_role.status_code,
                            204,
                            msg="Response is not 204")
