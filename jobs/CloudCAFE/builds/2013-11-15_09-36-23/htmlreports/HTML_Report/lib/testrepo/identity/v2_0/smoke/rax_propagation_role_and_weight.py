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
            domain_id=domain_id,
            password=cls.password)

        cls.auth_usr_adm_resp = cls.public_client.authenticate_user_password(
            cls.useradminname,
            cls.password)
        cls.public_client.token = cls.auth_usr_adm_resp.entity.token.id

        cls.sub_user = cls.public_client.add_user(
            username=cls.subusername,
            email=cls.email,
            enabled=True,
            domain_id=domain_id,
            password=cls.password)
        cls.provider = IdentityAPIProvider(cls.config)
        cls.public_admin_client = cls.provider.get_client()

    @classmethod
    def tearDownClass(cls):
        cls.delete_user_permanently(user_id=cls.sub_user.entity.id,
                                    client=cls.public_client)
        cls.delete_user_permanently(user_id=cls.user_adm_resp.entity.id,
                                    client=cls.admin_client)

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
            add_role.status_code, 201, msg="Response for add role is not 201.")
        # Delete role after test completion, even if any verification fails
        self.addCleanup(self.admin_client.delete_role,
                        role_id=add_role.entity.id)

    @attr('smoke', type='positive')
    def test_44731_verify_create_role(self):
        clients = [self.service_client, self.admin_client]
        for client in clients:
            name = rand_name("Guest:Role")
            description = rand_name("Guest description ")
            add_role = self.admin_client.add_role(
                name=name,
                description=description)
            self.assertEqual(add_role.status_code, 201,
                             msg="Response for add role is not 201.")
            self.addCleanup(self.admin_client.delete_role,
                            role_id=add_role.entity.id)

    @attr('smoke', type='positive')
    def test_44731_verify_add_role_with_propagation(self):

        name = rand_name("Guest:Role")
        description = rand_name("Guest description ")
        propagation_flag = True
        add_role = self.admin_client.add_role(
            name=name,
            description=description,
            propagate=propagation_flag)
        self.assertEqual(
            add_role.status_code, 201, msg="Response for add role is not 201.")
        self.addCleanup(self.admin_client.delete_role,
                        role_id=add_role.entity.id)

    @attr('smoke', type='positive')
    def test_44731_verify_assigning_role(self):

        name = rand_name("Guest:Role")
        description = rand_name("Guest description ")
        add_role = self.admin_client.add_role(
            name=name,
            description=description)
        self.assertEqual(
            add_role.status_code, 201, msg="Response for add role is not 201.")
        self.addCleanup(self.admin_client.delete_role,
                        role_id=add_role.entity.id)
        get_user_init = self.admin_client.get_user_by_name(
            name=self.useradminname)
        add_role_to_user = self.admin_client.add_role_to_user(
            user_id=get_user_init.entity.id,
            role_id=add_role.entity.id)

        normal_response_codes = [200, 201]
        self.assertIn(add_role_to_user.status_code, normal_response_codes,
                      msg='Add role to user response expected {0} received '
                          '{1}'.format(normal_response_codes,
                                       add_role_to_user.status_code))

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
            add_role.status_code, 201, msg="Response for add role is not 201.")
        self.addCleanup(self.admin_client.delete_role,
                        role_id=add_role.entity.id)
        get_user_init = self.admin_client.get_user_by_name(
            name=self.useradminname)
        add_role_to_user = self.admin_client.add_role_to_user(
            user_id=get_user_init.entity.id,
            role_id=add_role.entity.id)

        normal_response_codes = [200, 201]
        self.assertIn(add_role_to_user.status_code, normal_response_codes,
                      msg='Add role to user response expected {0} received '
                          '{1}'.format(normal_response_codes,
                                       add_role_to_user.status_code))

    def test_44731_verify_delete_role_service_admin(self):

        description = rand_name("Guest description ")
        propagation_flag_list = [False, True]
        for propagation_flag in propagation_flag_list:
            name = rand_name("Guest:Role")
            add_role = self.service_client.add_role(
                name=name,
                description=description,
                propagate=propagation_flag)
            self.assertEqual(
                add_role.status_code,
                201,
                msg="Response is not 201")
            delete_role = self.service_client.delete_role(
                role_id=add_role.entity.id)
            self.assertEqual(
                delete_role.status_code, 204,
                msg="Response for delete user is not 204")

    @attr('smoke', type='positive')
    def test_44731_verify_delete_role_identity_admin(self):

        name = rand_name("Guest:Role")
        description = rand_name("Guest description ")
        propagation_flag_list = [False, True]
        for propagation_flag in propagation_flag_list:
            add_role = self.admin_client.add_role(
                name=name,
                description=description,
                propagate=propagation_flag)
            self.assertEqual(
                add_role.status_code,
                201,
                msg="Response is not 201")
            delete_role = self.admin_client.delete_role(
                role_id=add_role.entity.id)
            self.assertEqual(
                delete_role.status_code, 204,
                msg="Response for delete role is not 204.")
