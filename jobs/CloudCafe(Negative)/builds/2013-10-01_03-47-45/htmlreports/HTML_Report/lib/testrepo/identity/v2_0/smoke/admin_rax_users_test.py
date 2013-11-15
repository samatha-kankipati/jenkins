from ccengine.common.tools.datagen import rand_name
from testrepo.common.testfixtures.identity.v2_0.identity \
        import IdentityAdminFixture
from ccengine.common.decorators import attr


class AdminUsersTest(IdentityAdminFixture):

    @classmethod
    def setUpClass(cls):
        super(AdminUsersTest, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        pass

    @attr('smoke', type='positive')
    def test_admin_list_users(self):
        normal_response_codes = [200, 203]
        list_users = self.public_client.list_users()

        self.assertIn(
                list_users.status_code,
                normal_response_codes,
                msg='Admin list users expected {0} recieved {1}'.
                format(normal_response_codes, list_users.status_code))

    @attr('smoke', type='positive')
    def test_admin_get_user_by_name(self):
        normal_response_codes = [200, 203]
        list_users = self.public_client.list_users()
        username = list_users.entity[0].username
        get_user = self.public_client.get_user_by_name(name=username)

        self.assertIn(
                get_user.status_code,
                normal_response_codes,
                msg='Admin get user by name expected {0} recieved {1}'.
                format(normal_response_codes, get_user.status_code))

    @attr('smoke', type='positive')
    def test_admin_get_user_by_id(self):
        normal_response_codes = [200, 203]
        list_users = self.public_client.list_users()
        userId = list_users.entity[0].id
        get_user = self.public_client.get_user_by_id(userId=userId)

        self.assertIn(
                get_user.status_code,
                normal_response_codes,
                msg='Admin get user by id expected {0} recieved {1}'.
                format(normal_response_codes, get_user.status_code))

    @attr('smoke', type='positive')
    def test_admin_add_user(self):
        username = rand_name('ccadminname')
        email = '{0}@{1}'.format(username, 'supra.com')
        domainId = '421342'
        create_user = self.admin_client.add_user(
                username=username,
                email=email,
                enabled=True,
                domainId=domainId,
                password='Gadmpass8')

        self.assertEqual(
                create_user.status_code,
                201,
                msg='Admin add user with passwd expected response 201'
                ' received {0}'.format(create_user.status_code))

        self.addCleanup(
                self.service_client.delete_user_hard,
                userId=create_user.entity.id)

        self.addCleanup(
                self.public_client.delete_user,
                userId=create_user.entity.id)

    @attr('smoke', type='positive')
    def test_admin_add_user_generated_password(self):
        username = rand_name('ccadminname')
        email = '{0}@{1}'.format(username, 'supra.com')
        domainId = '421342'

        '''Docs 4.1.4 if a password is not provided when
        the user is added, one is generated for the user'''
        create_user = self.admin_client.add_user(
                username=username,
                email=email,
                enabled=True,
                domainId=domainId)

        self.assertEqual(
                create_user.status_code,
                201,
                msg='Admin add user expected response 201 received %s'.
                format(create_user.status_code))

        self.addCleanup(
                self.service_client.delete_user_hard,
                userId=create_user.entity.id)

        self.addCleanup(
                self.public_client.delete_user,
                userId=create_user.entity.id)

    @attr('smoke', type='positive')
    def test_admin_update_user_email(self):
        default_username = rand_name('ccadminname')
        default_email = '{0}@{1}'.format(default_username, 'supra.com')
        default_domain_ID = '421342'
        default_region = 'DFW'
        default_status = True
        updated_email = 'example@hotmail.com'
        create_user = self.admin_client.add_user(
                username=default_username,
                email=default_email,
                enabled=default_status,
                domainId=default_domain_ID,
                password='Gadmpass8')

        self.assertEqual(
                create_user.status_code,
                201,
                msg='Admin add user with passwd expected response 201'
                ' received {0}'.format(create_user.status_code))

        update_user = self.public_client.update_user(
                userId=create_user.entity.id,
                username=default_username,
                email=updated_email,
                defaultRegion=default_region,
                enabled=default_status)

        self.assertEqual(
                update_user.status_code,
                200,
                msg='Admin update user email expected response 200'
                ' received {0}'.format(update_user.status_code))

        self.addCleanup(
                self.service_client.delete_user_hard,
                userId=create_user.entity.id)

        self.addCleanup(
                self.public_client.delete_user,
                userId=create_user.entity.id)

    @attr('smoke', type='positive')
    def test_admin_update_user_username(self):
        default_username = rand_name('ccadminname')
        default_email = '{0}@{1}'.format(default_username, 'supra.com')
        default_domain_ID = '421342'
        default_region = 'DFW'
        default_status = True
        updated_username = rand_name('upduser')
        create_user = self.admin_client.add_user(
                username=default_username,
                email=default_email,
                enabled=default_status,
                domainId=default_domain_ID,
                password='Gadmpass8')

        self.assertEqual(
                create_user.status_code,
                201,
                msg='Admin add user with passwd expected response 201'
                ' received {0}'.format(create_user.status_code))

        update_user = self.public_client.update_user(
                userId=create_user.entity.id,
                username=updated_username,
                email=default_email,
                defaultRegion=default_region,
                enabled=default_status)

        self.assertEqual(
                update_user.status_code,
                200,
                msg='Admin update user username expected response 200'
                ' received {0}'.format(update_user.status_code))

        self.addCleanup(
                self.service_client.delete_user_hard,
                userId=create_user.entity.id)

        self.addCleanup(
                self.public_client.delete_user,
                userId=create_user.entity.id)

    @attr('smoke', type='positive')
    def test_admin_update_user_status(self):
        default_username = rand_name('ccadminname')
        default_email = '{0}@{1}'.format(default_username, 'supra.com')
        default_domain_ID = '421342'
        default_region = 'DFW'
        default_status = True
        updated_status = False
        create_user = self.admin_client.add_user(
                username=default_username,
                email=default_email,
                enabled=default_status,
                domainId=default_domain_ID,
                password='Gadmpass8')

        self.assertEqual(
                create_user.status_code,
                201,
                msg='Admin add user with passwd expected response 201'
                ' received {0}'.format(create_user.status_code))

        update_user = self.public_client.update_user(
                userId=create_user.entity.id,
                username=default_username,
                email=default_email,
                defaultRegion=default_region,
                enabled=updated_status)

        self.assertEqual(
                update_user.status_code,
                200,
                msg='Admin update user status expected response 200'
                ' received {0}'.format(update_user.status_code))

        self.addCleanup(
                self.service_client.delete_user_hard,
                userId=create_user.entity.id)

        self.addCleanup(
                self.public_client.delete_user,
                userId=create_user.entity.id)

    @attr('smoke', type='positive')
    def test_admin_update_user_email_username_status(self):
        default_username = rand_name('ccadminname')
        default_email = '{0}@{1}'.format(default_username, 'supra.com')
        default_domain_ID = '421342'
        default_region = 'DFW'
        default_status = True
        updated_email = 'example@hotmail.com'
        updated_username = rand_name('upduser')
        updated_status = False
        create_user = self.admin_client.add_user(
                username=default_username,
                email=default_email,
                enabled=default_status,
                domainId=default_domain_ID,
                password='Gadmpass8')

        self.assertEqual(
                create_user.status_code,
                201,
                msg='Admin add user with passwd expected response 201'
                ' received {0}'.format(create_user.status_code))

        update_user = self.public_client.update_user(
                userId=create_user.entity.id,
                username=updated_username,
                email=updated_email,
                defaultRegion=default_region,
                enabled=updated_status)

        self.assertEqual(
                update_user.status_code,
                200,
                msg='Admin update user email, username, and status'
                ' expected response 200 received {0}'.
                format(update_user.status_code))

        self.addCleanup(
                self.service_client.delete_user_hard,
                userId=create_user.entity.id)

        self.addCleanup(
                self.public_client.delete_user,
                userId=create_user.entity.id)

    @attr('smoke', type='positive')
    def test_admin_delete_user(self):
        username = rand_name('ccadminname')
        email = '{0}@{1}'.format(username, 'supra.com')
        domainId = '421342'
        create_user = self.admin_client.add_user(
                username=username,
                email=email,
                enabled=True,
                domainId=domainId,
                password='Gadmpass8')

        self.assertEqual(
                create_user.status_code,
                201,
                msg='Admin add user with passwd expected response 201'
                ' received {0}'.format(create_user.status_code))

        self.addCleanup(
                self.service_client.delete_user_hard,
                userId=create_user.entity.id)

        self.addCleanup(
                self.public_client.delete_user,
                userId=create_user.entity.id)

    @attr('smoke', type='positive')
    def test_admin_get_accessible_domains(self):
        username = rand_name('ccadminname')
        email = '{0}@{1}'.format(username, 'supra.com')
        domainId = '421342'
        create_user = self.admin_client.add_user(
                username=username,
                email=email,
                enabled=True,
                domainId=domainId,
                password='Gadmpass8')

        self.assertEqual(
                create_user.status_code,
                201,
                msg='Admin add user with passwd expected response 201'
                ' received {0}'.format(create_user.status_code))

        resp = self.public_client.get_accessible_domains(
                userId=create_user.entity.id)

        self.assertEqual(
                resp.status_code,
                200,
                msg='Admin get accessible domains expected 200 recieved {0}'.
                format(resp.status_code))

        self.addCleanup(
                self.service_client.delete_user_hard,
                userId=create_user.entity.id)

        self.addCleanup(
                self.public_client.delete_user,
                userId=create_user.entity.id)

    @attr('smoke', type='positive')
    def test_admin_get_accessible_domain_endpoints(self):
        username = rand_name('ccadminname')
        email = '{0}@{1}'.format(username, 'supra.com')
        domainId = '421342'
        create_user = self.admin_client.add_user(
                username=username,
                email=email,
                enabled=True,
                domainId=domainId,
                password='Gadmpass8')

        self.assertEqual(
                create_user.status_code,
                201,
                msg='Admin add user with passwd expected response 201'
                'received {0}'.format(create_user.status_code))

        add_user_dom = self.admin_client.add_user_to_domain(
                userId=create_user.entity.id,
                domainId=domainId)

        self.assertEqual(
                add_user_dom.status_code,
                204,
                msg='Expected response 204 received {0}'.
                format(add_user_dom.status_code))

        add_ten_dom = self.admin_client.add_tenant_to_domain(
                domainId=domainId,
                tenantId=self.config.identity_api.tenant_id)

        self.assertEqual(
                add_ten_dom.status_code,
                204,
                msg='Expected response 204 received {0}'.
                format(add_ten_dom.status_code))

        resp = self.admin_client.get_accessible_domain_endpoints(
                userId=create_user.entity.id,
                domainId=create_user.entity.domainId)

        self.assertEqual(
                resp.status_code,
                200,
                msg='Admin get accessible domain endpoints expected 200'
                    ' recieved {0}'.format(resp.status_code))

        self.addCleanup(
                self.service_client.delete_user_hard,
                userId=create_user.entity.id)

        self.addCleanup(
                self.public_client.delete_user,
                userId=create_user.entity.id)

    @attr('smoke', type='positive')
    def test_admin_add_credential_to_user(self):
        username = rand_name('ccadminname')
        email = '{0}@{1}'.format(username, 'supra.com')
        domainId = '421342'
        updated_pass = rand_name('Password')
        create_user = self.admin_client.add_user(
                username=username,
                email=email,
                enabled=True,
                domainId=domainId,
                password='Gadmpass8')

        self.assertEqual(
                create_user.status_code,
                201,
                msg='Admin add user with passwd expected response 201'
                ' received {0}'.format(create_user.status_code))

        add_credentials = self.admin_client.add_user_credentials(
                userId=create_user.entity.id,
                username=username,
                password=updated_pass)

        self.assertEqual(
                add_credentials.status_code,
                201,
                msg='Admin add credential to user expected 201 recieved {0}'.
                format(add_credentials.status_code))

        self.addCleanup(
                self.service_client.delete_user_hard,
                userId=create_user.entity.id)

        self.addCleanup(
                self.public_client.delete_user,
                userId=create_user.entity.id)

    @attr('smoke', type='positive')
    def test_admin_list_credentials(self):
        list_users = self.public_client.list_users()
        userId = list_users.entity[0].id
        list_credentials = self.public_client.list_credentials(userId=userId)

        self.assertEqual(
                list_credentials.status_code,
                200,
                msg='Admin list credentials expected 200 recieved {0}'.
                format(list_credentials.status_code))

    @attr('smoke', type='positive')
    def test_admin_update_user_credentials(self):
        '''NOTE:>>> I-06703 Issue because document states 200 response only'''
        normal_response_codes = [200, 201]
        list_users = self.public_client.list_users()
        userId = list_users.entity[0].id
        username = list_users.entity[0].username
        updated_apiKey = 'aaaaa-bbbbb-ccccc-12345678'
        list_credentials = self.public_client.list_credentials(userId=userId)
        update_credentials = self.admin_client.update_user_credentials(
                userId=userId,
                username=username,
                apiKey=updated_apiKey)

        self.assertIn(
            update_credentials.status_code,
            normal_response_codes,
            msg='Admin update credientials expected %s recieved {0}'.
            format(normal_response_codes, update_credentials.status_code))

    @attr('smoke', type='positive')
    def test_admin_delete_user_credentials(self):
        '''NOTE:>>> I-06703 Issue because document states 200 response only'''
        normal_response_codes = [200, 201]
        username = rand_name('ccadminname')
        email = '{0}@{1}'.format(username, 'supra.com')
        domainId = '421342'
        updated_pass = rand_name('Password')
        updated_apiKey = 'aaaaa-bbbbb-ccccc-12345678'
        create_user = self.admin_client.add_user(
                username=username,
                email=email,
                enabled=True,
                domainId=domainId,
                password='Gadmpass8')

        self.assertEqual(
                create_user.status_code,
                201,
                msg='Admin add user with passwd expected response 201'
                ' received {0}'.format(create_user.status_code))

        update_credentials = self.admin_client.update_user_credentials(
                userId=create_user.entity.id,
                username=username,
                apiKey=updated_apiKey)

        self.assertIn(
            update_credentials.status_code,
            normal_response_codes,
            msg='Admin update credientials expected %s recieved {0}'.
            format(normal_response_codes, update_credentials.status_code))

        delete_user_creds = self.admin_client.delete_user_credentials(
                userId=create_user.entity.id)

        self.assertEqual(
                delete_user_creds.status_code,
                204,
                msg='Admin delete user credentials expected 204 recieved {0}'.
                format(delete_user_creds.status_code))

        self.addCleanup(
                self.service_client.delete_user_hard,
                userId=create_user.entity.id)

        self.addCleanup(
                self.public_client.delete_user,
                userId=create_user.entity.id)

    @attr('smoke', type='positive')
    def test_admin_get_user_credentials(self):
        list_users = self.public_client.list_users()
        userId = list_users.entity[0].id
        get_credentials = self.admin_client.get_user_credentials(userId=userId)

        self.assertEqual(
                get_credentials.status_code,
                200,
                msg='Admin get credentials expected 200 recieved {0}'.
                format(get_credentials.status_code))

    @attr('smoke', type='positive')
    def test_admin_reset_user_api_key(self):
        list_users = self.public_client.list_users()
        userId = list_users.entity[0].id
        reset_api_key = self.public_client.reset_user_api_key(userId=userId)

        self.assertEqual(
                reset_api_key.status_code,
                200,
                msg='Admin reset user api key expected 200 recieved {0}'.
                format(reset_api_key.status_code))
