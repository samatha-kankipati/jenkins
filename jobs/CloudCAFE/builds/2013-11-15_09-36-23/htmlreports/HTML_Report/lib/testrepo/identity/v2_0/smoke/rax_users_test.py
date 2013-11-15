from ccengine.common.tools.datagen import rand_name
from testrepo.common.testfixtures.identity.v2_0.identity \
    import UserAdminFixture
from ccengine.common.decorators import attr


class UsersTest(UserAdminFixture):
    @classmethod
    def setUpClass(cls):
        super(UsersTest, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        pass

    @attr('smoke', type='positive')
    def test_rax_user_list_users(self):
        normal_response_codes = [200, 203]
        list_users = self.public_client.list_users()

        self.assertIn(
            list_users.status_code, normal_response_codes,
            msg='List users expected {0} recieved {1}'.format(
                normal_response_codes, list_users.status_code))

    @attr('smoke', type='positive')
    def test_rax_user_list_users_limit(self):
        normal_response_codes = [200, 203]
        list_users = self.public_client.list_users(limit=10)

        self.assertIn(
            list_users.status_code, normal_response_codes,
            msg='List users expected {0} recieved {1}'.format(
                normal_response_codes, list_users.status_code))

    @attr('smoke', type='positive')
    def test_rax_user_list_users_marker(self):
        normal_response_codes = [200, 203]
        list_users = self.public_client.list_users(marker=10)

        self.assertIn(
            list_users.status_code, normal_response_codes,
            msg='List users expected {0} recieved {1}'.format(
                normal_response_codes, list_users.status_code))

    @attr('smoke', type='positive')
    def test_rax_user_list_users_limit_marker(self):
        normal_response_codes = [200, 203]
        list_users = self.public_client.list_users(marker=2, limit=10)

        self.assertIn(
            list_users.status_code, normal_response_codes,
            msg='List users expected {0} recieved {1}'.format(
                normal_response_codes, list_users.status_code))

    @attr('smoke', type='positive')
    def test_rax_user_list_users_email(self):
        normal_response_codes = [200, 203]
        email = "testbox@mailtrust.com"
        list_users = self.public_client.list_users(email=email)

        self.assertIn(
            list_users.status_code, normal_response_codes,
            msg='List users expected {0} recieved {1}'.format(
                normal_response_codes, list_users.status_code))

    @attr('smoke', type='positive')
    def test_rax_user_list_users_limit_email(self):
        normal_response_codes = [200, 203]
        email = "testbox@mailtrust.com"
        list_users = self.public_client.list_users(limit=10, email=email)

        self.assertIn(
            list_users.status_code, normal_response_codes,
            msg='List users expected {0} recieved {1}'.format(
                normal_response_codes, list_users.status_code))

    @attr('smoke', type='positive')
    def test_rax_user_list_users_marker_email(self):
        normal_response_codes = [200, 203]
        email = "testbox@mailtrust.com"
        list_users = self.public_client.list_users(marker=10, email=email)

        self.assertIn(
            list_users.status_code, normal_response_codes,
            msg='List users expected {0} recieved {1}'.format(
                normal_response_codes, list_users.status_code))

    @attr('smoke', type='positive')
    def test_rax_user_list_users_limit_marker_email(self):
        normal_response_codes = [200, 203]
        email = "testbox@mailtrust.com"
        list_users = self.public_client.list_users(
            marker=2,
            limit=10,
            email=email)

        self.assertIn(
            list_users.status_code, normal_response_codes,
            msg='List users expected {0} recieved {1}'.format(
                normal_response_codes, list_users.status_code))

    @attr('smoke', type='positive')
    def test_rax_user_get_user_by_name(self):
        normal_response_codes = [200, 203]
        list_users = self.public_client.list_users()
        username = list_users.entity[0].username
        get_user = self.public_client.get_user_by_name(name=username)

        self.assertIn(
            get_user.status_code, normal_response_codes,
            msg='Get user expected {0} recieved {1}'.format(
                normal_response_codes, get_user.status_code))

    @attr('smoke', type='positive')
    def test_rax_user_get_user_by_id(self):
        '''Modified test, returned object shouldn't be list'''
        normal_response_codes = [200, 203]
        list_users = self.public_client.list_users()
        user_id = list_users.entity[0].id
        get_user = self.public_client.get_user_by_id(user_id=user_id)

        self.assertIn(
            get_user.status_code, normal_response_codes,
            msg='Get user by id expected %s recieved %s'.format(
                normal_response_codes, get_user.status_code))

    @attr('smoke', type='positive')
    def test_rax_user_add_user_generated_password(self):
        normal_response_code = 201
        delete_code = 204
        username = rand_name('cctestname')
        email = '{0}@foehammer.crom'.format(username)
        add_user = self.public_client.add_user(
            username=username,
            email=email,
            enabled=False)

        self.assertEqual(
            add_user.status_code, normal_response_code,
            msg='Add user expected response {0} received {1}'.format(
                normal_response_code, add_user.status_code))

        self.delete_user_permanently(
            user_id=add_user.entity.id,
            client=self.public_client)

    @attr('smoke', type='positive')
    def test_rax_user_add_user_with_password(self):
        normal_response_code = 201
        delete_code = 204
        username = rand_name('cctestname')
        email = '{0}@foehammer.crom'.format(username)
        add_user = self.public_client.add_user(
            username=username,
            email=email,
            enabled=False,
            password='Gellpass8')

        self.assertEqual(
            add_user.status_code, normal_response_code,
            msg='Add user w/o passwd expected response {0} received '
                '{1}'.format(normal_response_code, add_user.status_code))

        self.delete_user_permanently(
            user_id=add_user.entity.id,
            client=self.public_client)

    @attr('smoke', type='positive')
    def test_rax_user_update_user_password(self):
        username = rand_name('cctestpassword')
        email = '{0}@foehammer.crom'.format(username)

        add_user = self.public_client.add_user(
            username=username,
            email=email,
            enabled=False,
            password='Password1')
        self.assertEqual(
            add_user.status_code, 201,
            msg="Response for add user is not 201.")
        # Delete user after test completion
        self.addCleanup(
            self.delete_user_permanently,
            user_id=add_user.entity.id,
            client=self.public_client)
        update_user = self.public_client.update_user(
            user_id=add_user.entity.id,
            username=add_user.entity.username,
            password='passworD1')
        self.assertEqual(
            update_user.status_code, 200,
            msg='Update user expected response {0} received '
                '{1}'.format(200, update_user.status_code))

    @attr('smoke', type='positive')
    def test_rax_user_delete_user(self):
        delete_code = 204
        username = rand_name('cctestname')
        email = '{0}@foehammer.crom'.format(username)
        add_user = self.public_client.add_user(
            username=username,
            email=email,
            enabled=False,
            password='Gellpass8')
        delete_user = self.public_client.delete_user(
            user_id=add_user.entity.id)

        self.assertEqual(
            delete_user.status_code, delete_code,
            msg='Delete user expected response {0} received {1}'.format(
                delete_code, delete_user.status_code))
        self.service_client.delete_user_hard(user_id=add_user.entity.id)

    @attr('smoke', type='positive')
    def test_rax_user_list_credentials(self):
        normal_response_codes = [200, 203]
        list_users = self.public_client.list_users()
        user_id = list_users.entity[0].id
        list_credentials = self.public_client.list_credentials(user_id=user_id)

        self.assertIn(
            list_credentials.status_code, normal_response_codes,
            msg='List credentials expected {0} recieved {1}'.format(
                normal_response_codes, list_credentials.status_code))

    @attr('smoke', type='positive')
    def test_rax_user_get_credentials(self):
        normal_response_codes = [200, 203]
        list_users = self.public_client.list_users()
        user_id = list_users.entity[0].id
        get_credentials = self.public_client.get_user_credentials(
            user_id=user_id)

        self.assertIn(
            get_credentials.status_code, normal_response_codes,
            msg='Get credentials expected {0} recieved {1}'.format(
                normal_response_codes, get_credentials.status_code))
