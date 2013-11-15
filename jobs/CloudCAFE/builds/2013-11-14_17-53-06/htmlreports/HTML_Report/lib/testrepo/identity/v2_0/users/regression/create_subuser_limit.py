from ccengine.common.decorators import attr
from ccengine.common.tools.datagen import rand_name, random_int
from ccengine.providers.identity.v2_0.identity_api \
    import IdentityClientTypes
from testrepo.common.testfixtures.identity.v2_0.identity \
    import BaseIdentityFixture


class CreateSubuserLimit(BaseIdentityFixture):
    """
    @summary: Test to verify that user admin can create only 100 subusers
    """
    @classmethod
    def setUpClass(cls):
        """
        Function to create test bed for all the test. Execute once at the
        beginning of class
        @param cls: instance of class

        """
        super(CreateSubuserLimit, cls).setUpClass()
        cls.serv_admin_name = cls.config.identity_api.service_username
        cls.serv_admin_password = cls.config.identity_api.service_password
        cls.identity_admin_name = rand_name("ccidentityadmin")
        cls.user_admin_name = rand_name("ccuseradmin")
        cls.password = "CCPassword1"
        cls.domain_id = random_int(10000, 1000000000)
        cls.user_admin_name_v1_1 = rand_name("ccuseradmin11")
        cls.key = 'asdasdasd-adsasdads-asdasdasd-adsadsasd'
        cls.mosso_id = random_int(1000000, 9000000)
        cls.subuser_limit = int(cls.config.identity_api.subuser_limit)

        service_admin_client = cls.set_client(
            username=cls.serv_admin_name, password=cls.serv_admin_password,
            user_type=IdentityClientTypes.SERVICE)
        cls.create_iden_adm_resp = cls.get_test_user_v2_0(
            client=service_admin_client, username=cls.identity_admin_name,
            password=cls.password, domain_id=None, enabled=True)

        iden_admin_client = cls.set_client(
            username=cls.identity_admin_name, password=cls.password,
            user_type=IdentityClientTypes.ADMIN)
        cls.admin_client.token = iden_admin_client.token
        cls.create_usr_adm_resp_v2_0 = cls.get_test_user_v2_0(
            client=cls.admin_client, username=cls.user_admin_name,
            password=cls.password, domain_id=cls.domain_id, enabled=True)

        cls.create_usr_adm_resp_v1_1 = cls.get_test_user_v1_1(
            client=cls.admin_client, user_id=cls.user_admin_name_v1_1,
            api_key=cls.key, mosso_id=cls.mosso_id, enabled=True)
        cls.get_user_id = cls.admin_client.get_user_by_name(
            name=cls.user_admin_name_v1_1)
        cls.list_credentials = cls.service_client.list_credentials(
            cls.get_user_id.entity.id)
        cls.subuser_list = []

    @classmethod
    def tearDownClass(cls):
        """
        Function to clean up the data after execution of all the tests
        completed. Execute once at the end of all the tests.
        @param cls: instance of class

        """
        cls.delete_user_permanently(
            user_id=cls.create_usr_adm_resp_v2_0.entity.id,
            client=cls.admin_client)
        cls.delete_user_permanently(
            user_id=cls.get_user_id.entity.id, client=cls.admin_client)

        cls.admin_client.delete_domain(domain_id=cls.domain_id)

        cls.delete_user_permanently(
            user_id=cls.create_iden_adm_resp.entity.id,
            client=cls.service_client)

    @attr('regression', type='positive')
    def test_create_subuser(self):
        """
        @summary: RBAC related test. Test to verify a user admin can create
         only the number the number of sub users specified in the config file
         """
        normal_response_codes = [201, 400]
        client_list = []
        client_1 = {'username': self.user_admin_name,
                    'password': self.password}
        password_11 = self.list_credentials.entity.passwordCredentials.password
        client_2 = {'username': self.user_admin_name_v1_1,
                    'password': password_11}
        client_list = [client_1, client_2]

        for client in client_list:
            client_obj = self.set_client(
                username=client['username'], password=client['password'],
                user_type=IdentityClientTypes.DEFAULT)
            usercount = 0
            max_users_limit_not_reached = True

            user_name = rand_name("ccsubuser")
            while (max_users_limit_not_reached and
                    usercount < (self.subuser_limit + 1)):
                sub_user_name = '{0}_{1}'.format(user_name, usercount)
                create_sub_usr_resp = self.get_test_user_v2_0(
                    client=client_obj, username=sub_user_name,
                    email="{0}@mailtrust.com".format(user_name),
                    password=self.password)
                if create_sub_usr_resp.status_code == 201:
                    usercount += 1
                    self.addCleanup(
                        self.delete_user_permanently,
                        client=self.service_client,
                        user_id=create_sub_usr_resp.entity.id)
                    self.assertLess(
                        usercount, self.subuser_limit,
                        "User cannot create more than {0} users in an account."
                        .format(self.subuser_limit))

                elif create_sub_usr_resp.status_code == 400:
                    max_users_limit_not_reached = False
                    resp_msg = ("User cannot create more than {0} users in an "
                                "account.".format(self.subuser_limit))
                    self.assertIn(
                        resp_msg, create_sub_usr_resp.content,
                        msg="Error message is incorrect in response.")
                    # There is defect, according to which user creation limit
                    # is limit_specified_in_config - 1. Once the defect is
                    # fixed, we don't need to do -1 from limit.
                    self.assertEqual(
                        usercount, self.subuser_limit - 1, msg=resp_msg)
                else:
                    self.assertIn(
                        create_sub_usr_resp.status_code, normal_response_codes,
                        msg='Create subuser response expected {0} received {1}'
                        .format(normal_response_codes,
                                create_sub_usr_resp.status_code))

            # There is defect, according to which user creation limit
            # is limit_specified_in_config - 1. Once the defect is
            # fixed, we don't need to do -1 from limit.
            self.assertEqual(usercount, self.subuser_limit - 1,
                             msg="Created {0} users!!".format(usercount))
