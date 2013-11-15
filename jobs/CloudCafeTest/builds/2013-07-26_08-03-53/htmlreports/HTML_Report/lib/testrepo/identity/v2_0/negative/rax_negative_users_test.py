"""Basic Negative Tests for Rax Users"""
from ccengine.common.tools.datagen import random_int
from ccengine.common.decorators import attr
from testrepo.common.testfixtures.identity.v2_0.identity \
    import UserAdminFixture
from ccengine.common.tools.datagen import rand_name


class UsersNegativeTest(UserAdminFixture):
    """Basic Smoke Negative Tests - Check HTTP Resoponses"""

    @classmethod
    def setUpClass(cls):
        super(UsersNegativeTest, cls).setUpClass()
        cls.false_creds = []
        cls.false_creds.append({"password": '00000000',
                                "username": '@1234567'})
        cls.false_creds.append({"password": '', "username": ''})
        cls.false_creds.append({"password": 'Pass1', "username": '@'})
        cls.false_creds.append({"password": '!@#$%^&*()',
                                "username": ' 1Afarsf'})
        cls.false_creds.append({"password": '102102101031013010311031',
                                "username": 'Ricardo0000000000000!'})

    @classmethod
    def tearDownClass(cls):
        super(UsersNegativeTest, cls).tearDownClass()

    @attr('regression', type='negative')
    def test_add_user_false_password(self):
        '''Add user with false passwords'''
        username = rand_name("cctestname")
        email = username + "@mailtrust.com"
        for false_cred in self.false_creds:
            cr_user = self.public_client.\
                    add_user(username=username,
                             email=email,
                             enabled=False,
                             password=false_cred['password'])
            self.assertEqual(cr_user.status_code, 400,
                             msg="Expected response 400 but received %s. "
                             "Attempted password of %s" %
                             (cr_user.status_code, false_cred['password']))
            self.assertTrue('Password must be at least 8 char' in
                            cr_user.content, msg="Expecting 'Fault state-inv. "
                            "password' but received  %s. Attempted password "
                            "of %s" % (cr_user.content,
                                       false_cred['password']))

    @attr('regression', type='negative')
    def test_add_user_false_username(self):
        '''Add user wiht false usernames.'''
        email = rand_name("cctestname") + "@mailtrust.com"
        for false_cred in self.false_creds:
            cr_user = self.public_client.\
                    add_user(username=false_cred['username'],
                             email=email,
                             enabled=False,
                             password="Gellpass8")
            self.assertEqual(cr_user.status_code, 400,
                             msg="Expected response 400 but received  %s. "
                             "Attempted username of %s" %
                             (cr_user.status_code, false_cred['username']))
            self.assertTrue('Expecting username' in cr_user.content or
                            'Username has invalid characters' in
                            cr_user.content or 'Username must begin' in
                            cr_user.content or 'Username should not' in
                            cr_user.content, msg="Expecting 'Fault state-inv. "
                            "username' but received  %s. Attempted username "
                            "of %s" % (cr_user.content,
                                       false_cred['username']))

    @attr('regression', type='negative')
    def test_rax_list_users_by_email_test_user_access(self):

        normal_response_codes = [200, 203]
        password = "Gusrpass8"

        client_map = {self.public_client: [self.service_client]}

        for client, creator_client_list in client_map.iteritems():
            for creator_client in creator_client_list:
                emailhead = rand_name("listemailverfiy")
                email = '{0}.testbox@{1}'.format(emailhead,
                                                 "mailtrust.com")
                username_list = []
                userid_list = []
                total_users = 3
                for _ in range(total_users):
                    username = rand_name("ccuser")
                    username_list.append(username)
                    create_user_resp = creator_client.add_user(
                            username=username,
                            email=email,
                            enabled=True,
                            password=password)
                    userid_list.append(create_user_resp.entity.id)

                list_users = client.list_users(email=email)
                self.assertIn(list_users.status_code, normal_response_codes,
                              msg='List users expected to return {0}'
                              'received {1}'.format(normal_response_codes,
                                                    list_users.status_code))

                for user in list_users.entity:
                    self.assertFalse(user.username in username_list,
                                     msg="User found in list user call")

                for user_id in userid_list:
                    del_user_resp = self.service_client.delete_user(
                            userId=user_id)
                    self.assertEqual(
                        del_user_resp.status_code,
                        204,
                        msg='Delete user failed, expected {0} returned {1}'.
                        format(204, del_user_resp.status_code))

                    hard_del_resp = self.service_client.delete_user_hard(
                            userId=user_id)
                    self.assertEqual(
                        hard_del_resp.status_code,
                        204,
                        msg='Delete user failed, expected {0} returned {1}'.
                        format(204, hard_del_resp.status_code))

    @attr('regression', type='negative')
    def test_rax_list_users_by_email_test_domain_access(self):
        """
        This test case is to test that the users present in different domain
        cannot be listed by admin in different domain by calling list users
        by email
        """

        admin_client_test = self.provider.get_client()
        public_client_test = self.provider.get_client()

        username_list = []
        userid_list = []
        normal_response_codes = [200, 203]

        iden_admin_name = rand_name("ccidenadmin")
        user_admin_name = rand_name("ccuseradmin")
        sub_user_name = rand_name("ccsubuser")
        emailhead = rand_name("listemailverfiy")
        email = '{0}.testbox@{1}'.format(emailhead, "mailtrust.com")
        password = "Gsubusrpass8"
        domain_id = random_int(10000, 1000000000)

        create_iden_admin = self.service_client.add_user(
                username=iden_admin_name,
                email=email,
                enabled=True,
                password=password)

        auth_iden_adm_resp = self.service_client.authenticate_user_password(
                iden_admin_name,
                password)

        username_list.append(iden_admin_name)
        userid_list.append(create_iden_admin.entity.id)

        admin_client_test.token = auth_iden_adm_resp.entity.token.id

        create_user_admin = admin_client_test.add_user(
                username=user_admin_name,
                email=email,
                enabled=True,
                domainId=domain_id,
                password=password)
        auth_user_adm_resp = admin_client_test.authenticate_user_password(
                user_admin_name,
                password)

        username_list.append(user_admin_name)
        userid_list.append(create_user_admin.entity.id)

        """
        Creating a new user-admin under different domain and assigning the
        token to public_client_test, so that the sub-user created with this
        token will fall under different domain than the user-admin
        in public_client object
        """
        public_client_test.token = auth_user_adm_resp.entity.token.id

        create_sub_user = public_client_test.add_user(
                username=sub_user_name,
                email=email,
                enabled=True,
                domainId=domain_id,
                password=password)

        username_list.append(sub_user_name)
        userid_list.append(create_sub_user.entity.id)

        """
        Sub-users are created in different domain and tried to verify
        the access from admins in different domain
        """
        client_list = [self.admin_client, self.public_client]
        for client in client_list:
            list_users = client.list_users(email=email)
            self.assertIn(list_users.status_code, normal_response_codes,
                          msg='List users expected to return {0}'
                              'received {1}'.format(normal_response_codes,
                                                    list_users.status_code))

            for user in list_users.entity:
                    self.assertFalse(user.username in username_list,
                                     msg="User found in list user call")

        del admin_client_test.token
        del public_client_test.token

        """
        Reversing the user list, because user admin cannot be deleted
        without removing the sub-users.  Sub users are appended last
        in the list
        """
        userid_list.reverse()
        for user_id in userid_list:
            del_user_resp = self.service_client.delete_user(
                    userId=user_id)
            self.assertEqual(
                del_user_resp.status_code,
                204,
                msg='Delete user failed, expected {0} returned {1}'.
                format(204, del_user_resp.status_code))

            hard_del_resp = self.service_client.delete_user_hard(
                    userId=user_id)
            self.assertEqual(
                hard_del_resp.status_code,
                204,
                msg='Delete user failed, expected {0} returned {1}'.
                format(204, hard_del_resp.status_code))

    @attr('regression', type='negative')
    def test_rax_list_users_marker_limit_invalid_email(self):
        """
        Returs 501 when the routing flag is set as true.  Try to route to
        cloud auth where the api is not implemented so it returns 501
        """
        normal_response_codes = [501]
        password = "Gusrpass8"
        emailhead = rand_name("listemailverfiy")
        email = '{0}.testbox@{1}'.format(emailhead, "mailtrust.com")
        userid_list = []

        total_users = 5
        for _ in range(total_users):
            username = rand_name("ccuser")
            create_user_resp = self.admin_client.add_user(
                    username=username,
                    email=email,
                    enabled=True,
                    password=password)
            userid_list.append(create_user_resp.entity.id)

        test_emailhead = rand_name("listemailverfiy")
        test_emailhead = rand_name(test_emailhead)
        test_email = '{0}@{1}'.format(test_emailhead, "mailtrust.com")
        list_users = self.public_client.list_users(marker=1,
                                                   limit=2,
                                                   email=test_email)

        self.assertIn(list_users.status_code, normal_response_codes,
                      msg='List users expected to return {0} received {1}'.
                      format(normal_response_codes,
                             list_users.status_code))

        for user_id in userid_list:
            del_user_resp = self.service_client.delete_user(
                    userId=user_id)
            self.assertEqual(
                del_user_resp.status_code,
                204,
                msg='Delete user failed, expected {0} returned {1}'.
                format(204, del_user_resp.status_code))

            hard_del_resp = self.service_client.delete_user_hard(
                    userId=user_id)
            self.assertEqual(
                hard_del_resp.status_code,
                204,
                msg='Delete user failed, expected {0} returned {1}'.
                format(204, hard_del_resp.status_code))
