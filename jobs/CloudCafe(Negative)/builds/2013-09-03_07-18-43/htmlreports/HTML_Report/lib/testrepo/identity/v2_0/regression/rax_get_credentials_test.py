from ccengine.common.decorators import attr
from ccengine.common.tools.datagen import rand_name
from ccengine.common.tools.datagen import random_int
from ccengine.providers.identity.v2_0.identity_api \
    import IdentityAPIProvider
from testrepo.common.testfixtures.identity.v2_0.identity \
    import BaseIdentityFixture


class RaxGetCredentialsTest(BaseIdentityFixture):

    @classmethod
    def setUpClass(cls):
        super(RaxGetCredentialsTest, cls).setUpClass()

        # Get service admin userId
        cls.serv_admin_name = cls.config.identity_api.service_username
        cls.serv_admin_password = cls.config.identity_api.service_password
        get_service_info = cls.service_client.get_user_by_name(
            name=cls.serv_admin_name)
        cls.serv_adm_id = get_service_info.entity.id

        # Creating identity admin
        cls.identity_admin_username = rand_name("ccidentityadmin")
        identity_admin_email = "{0}@{1}".format(cls.identity_admin_username,
                                                "mailtrust.com")
        cls.password = "Password1"
        cls.create_iden_admin_resp = cls.service_client.add_user(
            username=cls.identity_admin_username, password=cls.password,
            email=identity_admin_email, enabled=True)
        cls.auth_iden_adm_resp = cls.service_client.authenticate_user_password(
            cls.identity_admin_username,
            cls.password)
        cls.admin_client.token = cls.auth_iden_adm_resp.entity.token.id

        # Creating user admin
        domain_id = random_int(10000, 1000000)
        cls.user_admin_username = rand_name("ccuseradmin")
        user_admin_email = "{0}@{1}".format(cls.user_admin_username,
                                            "mailtrust.com")
        cls.create_user_admin_resp = cls.admin_client.add_user(
            username=cls.user_admin_username, password=cls.password,
            email=user_admin_email, enabled=True, domainId=domain_id)

        cls.provider = IdentityAPIProvider(cls.config)
        cls.public_client = cls.provider.get_client()

        cls.auth_user_adm_resp = cls.public_client.authenticate_user_password(
            cls.user_admin_username,
            cls.password)
        cls.public_client.token = cls.auth_user_adm_resp.entity.token.id

        # Creating Sub User
        cls.sub_user_username = rand_name("ccsubusername")
        sub_user_email = "{0}@{1}".format(cls.sub_user_username,
                                          "mailtrust.com")
        cls.create_sub_user_resp = cls.public_client.add_user(
            username=cls.sub_user_username, password=cls.password,
            email=sub_user_email, enabled=True)
        cls.auth_sub_user_resp = cls.public_client.authenticate_user_password(
            cls.sub_user_username,
            cls.password)

        cls.default_client = cls.provider.get_client()
        cls.default_client.token = cls.auth_sub_user_resp.entity.token.id

        cls.iden_adm_id = cls.create_iden_admin_resp.entity.id
        cls.user_adm_id = cls.create_user_admin_resp.entity.id
        cls.sub_user_id = cls.create_sub_user_resp.entity.id

    @classmethod
    def tearDownClass(cls):

        del cls.default_client.token
        cls.public_client.delete_user(
            userId=cls.sub_user_id)
        cls.service_client.delete_user_hard(
            userId=cls.sub_user_id)

        del cls.public_client.token
        cls.admin_client.delete_user(
            userId=cls.user_adm_id)
        cls.service_client.delete_user_hard(
            userId=cls.user_adm_id)

        del cls.admin_client.token
        cls.service_client.delete_user(
            userId=cls.iden_adm_id)
        cls.service_client.delete_user_hard(
            userId=cls.iden_adm_id)

    @attr('regression', type='positive')
    def test_get_password_credentials(self):
        """
        Test to verify only the service admin can retreive password credentials

        """
        test_values = {self.service_client: [self.serv_adm_id,
                                             self.iden_adm_id,
                                             self.user_adm_id,
                                             self.sub_user_id]}

        client_keys = test_values.keys()
        normal_response_codes = [200]

        for client in client_keys:
            user_id_list = test_values[client]
            for user_id in user_id_list:
                get_pass_credentials = client.get_user_credentials_password(
                    userId=user_id)
                get_user = self.service_client.get_user_by_id(userId=user_id)

                self.assertIn(
                    get_user.status_code,
                    normal_response_codes,
                    msg='Get user by id expected %s recieved %s'.
                    format(normal_response_codes, get_user.status_code))
                self.assertTrue(
                    get_pass_credentials.entity.username is not None,
                    msg="username is not present")
                self.assertEqual(
                    get_user.entity.username,
                    get_pass_credentials.entity.username,
                    msg='User name expected response {0} received {1}'.
                    format(get_user.entity.username,
                        get_pass_credentials.entity.username))
                self.assertTrue(
                    get_pass_credentials.entity.password is not None,
                    msg="password is not present")

                if (get_user.entity.username == self.serv_admin_name):
                    self.assertEqual(
                        self.serv_admin_password,
                        get_pass_credentials.entity.password,
                        msg='Password expected response {0} received {1}'.
                        format(self.serv_admin_password,
                               get_pass_credentials.entity.password))
                else:
                    self.assertEqual(
                        self.password,
                        get_pass_credentials.entity.password,
                        msg='Password expected response {0} received {1}'.
                        format(self.password,
                               get_pass_credentials.entity.password))

    @attr('regression', type='positive')
    def test_get_password_credentials_neg(self):

        test_values = {self.admin_client: [self.serv_adm_id,
                                           self.iden_adm_id,
                                           self.user_adm_id,
                                           self.sub_user_id],
                       self.public_client: [self.serv_adm_id,
                                            self.iden_adm_id,
                                            self.user_adm_id,
                                            self.sub_user_id],
                       self.default_client: [self.serv_adm_id,
                                             self.iden_adm_id,
                                             self.user_adm_id,
                                             self.sub_user_id]}

        client_keys = test_values.keys()
        normal_response_codes = [403]

        for client in client_keys:
            user_id_list = test_values[client]
            for user_id in user_id_list:
                get_pass_credentials = client.get_user_credentials_password(
                    userId=user_id)

                self.assertEqual(
                    get_pass_credentials.status_code,
                    normal_response_codes,
                    msg='Get password credentials expects {0} received {1}'.
                    format(normal_response_codes,
                           get_pass_credentials.status_code))
