from ccengine.common.tools.datagen import rand_name
from ccengine.common.tools.datagen import random_int
from testrepo.common.testfixtures.identity.v2_0.identity \
    import UserAdminFixture
from ccengine.common.decorators import attr
from ccengine.domain.identity.v2_0.response.user import Users, User
from ccengine.domain.identity.v2_0.response.credentials \
    import Credentials
from ccengine.domain.identity.v2_0.response.credentials \
    import ApiKeyCredentials


class UsersTest(UserAdminFixture):

    @classmethod
    def setUpClass(cls):
        super(UsersTest, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        pass

    @attr('regression', type='positive')
    def test_rax_user_list_users(self):
        list_users = self.public_client.list_users()

        self.assertIsInstance(list_users.entity, Users)

        enabled_values = [True, False]
        try:
            for user in list_users.entity:
                self.assertIsInstance(
                        user,
                        User,
                        msg='list users expected a User obj '
                        'recieved {0}'.format(type(user)))

                self.assertIsNotNone(
                        user.id,
                        msg='User obj expected a user ID recieved '
                        '{0}'.format(user.id))

                self.assertIsNotNone(
                        user.username,
                        msg='User obj expected a username recieved '
                        '{0}'.format(user.username))
                self.assertIsNotNone(
                        user.enabled,
                        msg='User {0} expected enabled recieved '
                        '{1}'.format(user.username, user.enabled))

                self.assertIn(
                        user.enabled,
                        enabled_values,
                        msg='User obj expected enabled value to be in {0} '
                        'recieved {1}'.format(enabled_values, user.enabled))
        except TypeError:
            self.assertIsNotNone(
                    list_users.entity,
                    msg='list users expected User objects recieved {0}'.
                    format(type(list_users.entity)))

    @attr('regression', type='positive')
    def test_rax_user_get_user_by_name_generated_password_enabled_true(self):
        '''DOCS:>>> this call is returning extra members in the response'''
        delete_code = 204
        enabled_value = True
        enabled_values = [True, False]
        username = rand_name('cctestname')
        email = '{0}@foehammer.crom'.format(username)

        '''user added with generated password'''
        add_user = self.public_client.add_user(
                username=username,
                email=email,
                enabled=enabled_value)

        get_user = self.public_client.get_user_by_name(name=username)

        '''
        Refer to the docs:
        this call is returning extra members in the response
        username = cctestname662847
        updated = 2013-03-11T15:35:27.654-05:00
        domainId = 123456789
        display_name = None
        name = None
        roles = None
        created = 2013-03-11T15:35:27.645-05:00
        defaultRegion = SECJSON1360866441565
        enabled = False
        email = cctestname662847@foehammer.crom
        password = None
        id = 10075461
        '''
        self.assertIsInstance(
                get_user.entity,
                User,
                msg='Get user expected a User obj recieved {0}'.
                format(type(get_user.entity)))

        self.assertIsNotNone(
                get_user.entity.defaultRegion,
                msg='User obj expected a default region recieved {0}'.
                format(type(get_user.entity.defaultRegion)))

        self.assertIsNotNone(
                get_user.entity.id,
                msg='User obj expected an id recieved {0}'.
                format(type(get_user.entity.id)))

        self.assertEqual(
                get_user.entity.id,
                add_user.entity.id,
                msg='User obj expected an id {0} recieved {1}'.
                format(add_user.entity.id, get_user.entity.id))

        self.assertIsNotNone(
                get_user.entity.username,
                msg='User obj expected a username recieved {0}'.
                format(type(get_user.entity.username)))

        self.assertEqual(
                get_user.entity.username,
                add_user.entity.username,
                msg='User obj expected name {0} recieved {1}'.
                format(add_user.entity.name, get_user.entity.name))

        self.assertIsNotNone(
                get_user.entity.email,
                msg='User obj expected an email recieved {0}'.
                format(type(get_user.entity.email)))

        self.assertEqual(
                get_user.entity.email,
                add_user.entity.email,
                msg='User obj expected email {0} recieved {1}'.
                format(add_user.entity.email, get_user.entity.email))

        self.assertIsNotNone(
                get_user.entity.enabled,
                msg='User obj expected enabled T/F recieved {0}'.
                format(type(get_user.entity.enabled)))

        self.assertIn(
                get_user.entity.enabled,
                enabled_values,
                msg='User obj expected enabled {0} recieved {1}'.
                format(enabled_values, get_user.entity.enabled))

        delete_user = self.public_client.delete_user(
                userId=add_user.entity.id)

        self.assertEqual(
                delete_user.status_code,
                delete_code,
                msg='Delete user expected response {0} received {1}'.
                format(delete_code, delete_user.status_code))

        hard_delete_user = self.service_client.delete_user_hard(
                userId=add_user.entity.id)

        self.assertEqual(
                hard_delete_user.status_code,
                delete_code,
                msg='Hard delete user expected response {0} received {1}'.
                format(delete_code, hard_delete_user.status_code))

    @attr('regression', type='positive')
    def test_rax_user_get_user_by_name_with_password_enabled_true(self):
        '''DOCS:>>> this call is returning extra members in the response'''
        delete_code = 204
        enabled_value = True
        enabled_values = [True, False]
        username = rand_name('cctestname')
        pass_wd = 'Gellpass8'
        email = '{0}@foehammer.crom'.format(username)

        '''user added with password'''
        add_user = self.public_client.add_user(
                username=username,
                email=email,
                enabled=enabled_value,
                password=pass_wd)

        get_user = self.public_client.get_user_by_name(name=username)

        '''
        Refer to the docs:
        this call is returning extra members in the response
        username = cctestname662847
        updated = 2013-03-11T15:35:27.654-05:00
        domainId = 123456789
        display_name = None
        name = None
        roles = None
        created = 2013-03-11T15:35:27.645-05:00
        defaultRegion = SECJSON1360866441565
        enabled = False
        email = cctestname662847@foehammer.crom
        password = None
        id = 10075461
        '''
        self.assertIsInstance(
                get_user.entity,
                User,
                msg='Get user expected a User obj recieved {0}'.
                format(type(get_user.entity)))

        self.assertIsNotNone(
                get_user.entity.defaultRegion,
                msg='User obj expected a default region recieved {0}'.
                format(type(get_user.entity.defaultRegion)))

        self.assertIsNotNone(
                get_user.entity.id,
                msg='User obj expected an id recieved {0}'.
                format(type(get_user.entity.id)))

        self.assertEqual(
                get_user.entity.id,
                add_user.entity.id,
                msg='User obj expected an id {0} recieved {1}'.
                format(add_user.entity.id, get_user.entity.id))

        self.assertIsNotNone(
                get_user.entity.username,
                msg='User obj expected a username recieved {0}'.
                format(type(get_user.entity.username)))

        self.assertEqual(
                get_user.entity.username,
                add_user.entity.username,
                msg='User obj expected name {0} recieved {1}'.
                format(add_user.entity.name, get_user.entity.name))

        self.assertIsNotNone(
                get_user.entity.email,
                msg='User obj expected an email recieved {0}'.
                format(type(get_user.entity.email)))

        self.assertEqual(
                get_user.entity.email,
                add_user.entity.email,
                msg='User obj expected email {0} recieved {1}'.
                format(add_user.entity.email, get_user.entity.email))

        self.assertIsNotNone(
                get_user.entity.enabled,
                msg='User obj expected enabled T/F recieved {0}'.
                format(type(get_user.entity.enabled)))

        self.assertIn(
                get_user.entity.enabled,
                enabled_values,
                msg='User obj expected enabled {0} recieved {1}'.
                format(enabled_values, get_user.entity.enabled))

        delete_user = self.public_client.delete_user(
                userId=add_user.entity.id)

        self.assertEqual(
                delete_user.status_code,
                delete_code,
                msg='Delete user expected response {0} received {1}'.
                format(delete_code, delete_user.status_code))

        hard_delete_user = self.service_client.delete_user_hard(
                userId=add_user.entity.id)

        self.assertEqual(
                hard_delete_user.status_code,
                delete_code,
                msg='Hard delete user expected response {0} received {1}'.
                format(delete_code, hard_delete_user.status_code))

    @attr('regression', type='positive')
    def test_rax_user_get_user_by_name_generated_password_enabled_false(self):
        '''DOCS:>>> this call is returning extra members in the response'''
        delete_code = 204
        enabled_value = False
        enabled_values = [True, False]
        username = rand_name('cctestname')
        email = '{0}@foehammer.crom'.format(username)

        '''user added with generated password'''
        add_user = self.public_client.add_user(
                username=username,
                email=email,
                enabled=enabled_value)

        get_user = self.public_client.get_user_by_name(name=username)

        '''
        Refer to the docs:
        this call is returning extra members in the response
        username = cctestname662847
        updated = 2013-03-11T15:35:27.654-05:00
        domainId = 123456789
        display_name = None
        name = None
        roles = None
        created = 2013-03-11T15:35:27.645-05:00
        defaultRegion = SECJSON1360866441565
        enabled = False
        email = cctestname662847@foehammer.crom
        password = None
        id = 10075461
        '''
        self.assertIsInstance(
                get_user.entity,
                User,
                msg='Get user expected a User obj recieved {0}'.
                format(type(get_user.entity)))

        self.assertIsNotNone(
                get_user.entity.defaultRegion,
                msg='User obj expected a default region recieved {0}'.
                format(type(get_user.entity.defaultRegion)))

        self.assertIsNotNone(
                get_user.entity.id,
                msg='User obj expected an id recieved {0}'.
                format(type(get_user.entity.id)))

        self.assertEqual(
                get_user.entity.id,
                add_user.entity.id,
                msg='User obj expected an id {0} recieved {1}'.
                format(add_user.entity.id, get_user.entity.id))

        self.assertIsNotNone(
                get_user.entity.username,
                msg='User obj expected a username recieved {0}'.
                format(type(get_user.entity.username)))

        self.assertEqual(
                get_user.entity.username,
                add_user.entity.username,
                msg='User obj expected name {0} recieved {1}'.
                format(add_user.entity.name, get_user.entity.name))

        self.assertIsNotNone(
                get_user.entity.email,
                msg='User obj expected an email recieved {0}'.
                format(type(get_user.entity.email)))

        self.assertEqual(
                get_user.entity.email,
                add_user.entity.email,
                msg='User obj expected email {0} recieved {1}'.
                format(add_user.entity.email, get_user.entity.email))

        self.assertIsNotNone(
                get_user.entity.enabled,
                msg='User obj expected enabled T/F recieved {0}'.
                format(type(get_user.entity.enabled)))

        self.assertIn(
                get_user.entity.enabled,
                enabled_values,
                msg='User obj expected enabled {0} recieved {1}'.
                format(enabled_values, get_user.entity.enabled))

        delete_user = self.public_client.delete_user(
                userId=add_user.entity.id)

        self.assertEqual(
                delete_user.status_code,
                delete_code,
                msg='Delete user expected response {0} received {1}'.
                format(delete_code, delete_user.status_code))

        hard_delete_user = self.service_client.delete_user_hard(
                userId=add_user.entity.id)

        self.assertEqual(
                hard_delete_user.status_code,
                delete_code,
                msg='Hard delete user expected response {0} received {1}'.
                format(delete_code, hard_delete_user.status_code))

    @attr('regression', type='positive')
    def test_rax_user_get_user_by_name_with_password_enabled_false(self):
        '''DOCS:>>> this call is returning extra members in the response'''
        delete_code = 204
        enabled_value = False
        enabled_values = [True, False]
        username = rand_name('cctestname')
        pass_wd = 'Gellpass8'
        email = '{0}@foehammer.crom'.format(username)

        '''user added with password'''
        add_user = self.public_client.add_user(
                username=username,
                email=email,
                enabled=enabled_value,
                password=pass_wd)

        get_user = self.public_client.get_user_by_name(name=username)

        '''
        Refer to the docs:
        this call is returning extra members in the response
        username = cctestname662847
        updated = 2013-03-11T15:35:27.654-05:00
        domainId = 123456789
        display_name = None
        name = None
        roles = None
        created = 2013-03-11T15:35:27.645-05:00
        defaultRegion = SECJSON1360866441565
        enabled = False
        email = cctestname662847@foehammer.crom
        password = None
        id = 10075461
        '''
        self.assertIsInstance(
                get_user.entity,
                User,
                msg='Get user expected a User obj recieved {0}'.
                format(type(get_user.entity)))

        self.assertIsNotNone(
                get_user.entity.defaultRegion,
                msg='User obj expected a default region recieved {0}'.
                format(type(get_user.entity.defaultRegion)))

        self.assertIsNotNone(
                get_user.entity.id,
                msg='User obj expected an id recieved {0}'.
                format(type(get_user.entity.id)))

        self.assertEqual(
                get_user.entity.id,
                add_user.entity.id,
                msg='User obj expected an id {0} recieved {1}'.
                format(add_user.entity.id, get_user.entity.id))

        self.assertIsNotNone(
                get_user.entity.username,
                msg='User obj expected a username recieved {0}'.
                format(type(get_user.entity.username)))

        self.assertEqual(
                get_user.entity.username,
                add_user.entity.username,
                msg='User obj expected name {0} recieved {1}'.
                format(add_user.entity.name, get_user.entity.name))

        self.assertIsNotNone(
                get_user.entity.email,
                msg='User obj expected an email recieved {0}'.
                format(type(get_user.entity.email)))

        self.assertEqual(
                get_user.entity.email,
                add_user.entity.email,
                msg='User obj expected email {0} recieved {1}'.
                format(add_user.entity.email, get_user.entity.email))

        self.assertIsNotNone(
                get_user.entity.enabled,
                msg='User obj expected enabled T/F recieved {0}'.
                format(type(get_user.entity.enabled)))

        self.assertIn(
                get_user.entity.enabled,
                enabled_values,
                msg='User obj expected enabled {0} recieved {1}'.
                format(enabled_values, get_user.entity.enabled))

        delete_user = self.public_client.delete_user(
                userId=add_user.entity.id)

        self.assertEqual(
                delete_user.status_code,
                delete_code,
                msg='Delete user expected response {0} received {1}'.
                format(delete_code, delete_user.status_code))

        hard_delete_user = self.service_client.delete_user_hard(
                userId=add_user.entity.id)

        self.assertEqual(
                hard_delete_user.status_code,
                delete_code,
                msg='Hard delete user expected response {0} received {1}'.
                format(delete_code, hard_delete_user.status_code))

    @attr('regression', type='positive')
    def test_rax_user_get_user_by_id(self):
        '''DOCS:>>> this call is returning extra members in the response'''
        delete_code = 204
        enabled_values = [True, False]
        username = rand_name('cctestname')
        email = '{0}@foehammer.crom'.format(username)
        add_user = self.public_client.add_user(
                username=username,
                email=email,
                enabled=False)

        get_user = self.public_client.get_user_by_id(userId=add_user.entity.id)

        '''
        Refer to the docs:
        this call is returning extra members in the response
        username = cctestname662847
        updated = 2013-03-11T15:35:27.654-05:00
        domainId = 123456789
        display_name = None
        name = None
        roles = None
        created = 2013-03-11T15:35:27.645-05:00
        defaultRegion = SECJSON1360866441565
        enabled = False
        email = cctestname662847@foehammer.crom
        password = None
        id = 10075461
        '''
        self.assertIsInstance(
                get_user.entity,
                User,
                msg='Get user expected a User obj recieved {0}'.
                format(type(get_user.entity)))

        self.assertIsNotNone(
                get_user.entity.defaultRegion,
                msg='User obj expected a default region recieved {0}'.
                format(type(get_user.entity.defaultRegion)))

        self.assertIsNotNone(
                get_user.entity.id,
                msg='User obj expected an id recieved {0}'.
                format(type(get_user.entity.id)))

        self.assertEqual(
                get_user.entity.id,
                add_user.entity.id,
                msg='User obj expected an id {0} recieved {1}'.
                format(add_user.entity.id, get_user.entity.id))

        self.assertIsNotNone(
                get_user.entity.username,
                msg='User obj expected a username recieved {0}'.
                format(type(get_user.entity.username)))

        self.assertEqual(
                get_user.entity.username,
                add_user.entity.username,
                msg='User obj expected name {0} recieved {1}'.
                format(add_user.entity.name, get_user.entity.name))

        self.assertIsNotNone(
                get_user.entity.email,
                msg='User obj expected an email recieved {0}'.
                format(type(get_user.entity.email)))

        self.assertEqual(
                get_user.entity.email,
                add_user.entity.email,
                msg='User obj expected email {0} recieved {1}'.
                format(add_user.entity.email, get_user.entity.email))

        self.assertIsNotNone(
                get_user.entity.enabled,
                msg='User obj expected enabled T/F recieved {0}'.
                format(type(get_user.entity.enabled)))

        self.assertIn(
                get_user.entity.enabled,
                enabled_values,
                msg='User obj expected enabled {0} recieved {1}'.
                format(enabled_values, get_user.entity.enabled))

        delete_user = self.public_client.delete_user(
                userId=add_user.entity.id)

        self.assertEqual(
                delete_user.status_code,
                delete_code,
                msg='Delete user expected response {0} received {1}'.
                format(delete_code, delete_user.status_code))

        hard_delete_user = self.service_client.delete_user_hard(
                userId=add_user.entity.id)

        self.assertEqual(
                hard_delete_user.status_code,
                delete_code,
                msg='Hard delete user expected response {0} received {1}'.
                format(delete_code, hard_delete_user.status_code))

    @attr('regression', type='positive')
    def test_rax_user_add_user_enabled_true(self):
        delete_code = 204
        enabled_value = True
        username = rand_name('cctestname')
        email = '{0}@foehammer.crom'.format(username)
        password = 'Gellpass8'
        add_user = self.public_client.add_user(
                username=username,
                email=email,
                enabled=enabled_value,
                password=password)

        self.assertIsInstance(
                add_user.entity,
                User,
                msg='Get user expected a User obj recieved {0}'.
                format(type(add_user.entity)))

        self.assertIsNotNone(
                add_user.entity.defaultRegion,
                msg='User obj expected a default region recieved {0}'.
                format(type(add_user.entity.defaultRegion)))

        self.assertIsNotNone(
                add_user.entity.id,
                msg='User obj expected an id recieved {0}'.
                format(type(add_user.entity.id)))

        self.assertIsNotNone(
                add_user.entity.username,
                msg='User obj expected a username recieved {0}'.
                format(type(add_user.entity.username)))

        self.assertEqual(
                add_user.entity.username,
                username,
                msg='User obj expected name {0} recieved {1}'.
                format(add_user.entity.name, username))

        self.assertIsNotNone(
                add_user.entity.email,
                msg='User obj expected an email recieved {0}'.
                format(type(add_user.entity.email)))

        self.assertEqual(
                add_user.entity.email,
                email,
                msg='User obj expected email {0} recieved {1}'.
                format(add_user.entity.email, email))

        self.assertIsNotNone(
                add_user.entity.enabled,
                msg='User obj expected enabled T/F recieved {0}'.
                format(type(add_user.entity.enabled)))

        self.assertEqual(
                add_user.entity.enabled,
                enabled_value,
                msg='User obj expected enabled {0} recieved {1}'.
                format(str(enabled_value), add_user.entity.enabled))

        '''
        If an initial password is generated, it is included in a successful
        response to this request. After the user is created, the password
        cannot be retrieved by any means. Make note of the password in the
        response and supply that password to the user.
        '''

        self.assertIsNone(
                add_user.entity.password,
                msg='User obj as not expecting a password recieved {0}'.
                format(add_user.entity.password))

        delete_user = self.public_client.delete_user(
                userId=add_user.entity.id)

        self.assertEqual(
                delete_user.status_code,
                delete_code,
                msg='Delete user expected response {0} received {1}'.
                format(delete_code, delete_user.status_code))

        hard_delete_user = self.service_client.delete_user_hard(
                userId=add_user.entity.id)

        self.assertEqual(
                hard_delete_user.status_code,
                delete_code,
                msg='Hard delete user expected response {0} received {1}'.
                format(delete_code, hard_delete_user.status_code))

    @attr('regression', type='positive')
    def test_rax_user_add_user_enabled_false(self):
        delete_code = 204
        enabled_value = False
        username = rand_name('cctestname')
        email = '{0}@foehammer.crom'.format(username)
        password = 'Gellpass8'
        add_user = self.public_client.add_user(
                username=username,
                email=email,
                enabled=enabled_value,
                password=password)

        self.assertIsInstance(
                add_user.entity,
                User,
                msg='Get user expected a User obj recieved {0}'.
                format(type(add_user.entity)))

        self.assertIsNotNone(
                add_user.entity.defaultRegion,
                msg='User obj expected a default region recieved {0}'.
                format(type(add_user.entity.defaultRegion)))

        self.assertIsNotNone(
                add_user.entity.id,
                msg='User obj expected an id recieved {0}'.
                format(type(add_user.entity.id)))

        self.assertIsNotNone(
                add_user.entity.username,
                msg='User obj expected a username recieved {0}'.
                format(type(add_user.entity.username)))

        self.assertEqual(
                add_user.entity.username,
                username,
                msg='User obj expected name {0} recieved {1}'.
                format(add_user.entity.name, username))

        self.assertIsNotNone(
                add_user.entity.email,
                msg='User obj expected an email recieved {0}'.
                format(type(add_user.entity.email)))

        self.assertEqual(
                add_user.entity.email,
                email,
                msg='User obj expected email {0} recieved {1}'.
                format(add_user.entity.email, email))

        self.assertIsNotNone(
                add_user.entity.enabled,
                msg='User obj expected enabled T/F recieved {0}'.
                format(type(add_user.entity.enabled)))

        self.assertEqual(
                add_user.entity.enabled,
                enabled_value,
                msg='User obj expected enabled {0} recieved {1}'.
                format(str(enabled_value), add_user.entity.enabled))

        '''
        If an initial password is generated, it is included in a successful
        response to this request. After the user is created, the password
        cannot be retrieved by any means. Make note of the password in the
        response and supply that password to the user.
        '''

        self.assertIsNone(
                add_user.entity.password,
                msg='User obj as not expecting a password recieved {0}'.
                format(add_user.entity.password))

        delete_user = self.public_client.delete_user(
                userId=add_user.entity.id)

        self.assertEqual(
                delete_user.status_code,
                delete_code,
                msg='Delete user expected response {0} received {1}'.
                format(delete_code, delete_user.status_code))

        hard_delete_user = self.service_client.delete_user_hard(
                userId=add_user.entity.id)

        self.assertEqual(
                hard_delete_user.status_code,
                delete_code,
                msg='Hard delete user expected response {0} received {1}'.
                format(delete_code, hard_delete_user.status_code))

    @attr('regression', type='positive')
    def test_rax_user_add_user_generated_password_enabled_true(self):
        delete_code = 204
        enabled_value = True
        username = rand_name('cctestname')
        email = '{0}@foehammer.crom'.format(username)
        add_user = self.public_client.add_user(
                username=username,
                email=email,
                enabled=enabled_value)

        self.assertIsInstance(
                add_user.entity,
                User,
                msg='Get user expected a User obj recieved {0}'.
                format(type(add_user.entity)))

        self.assertIsNotNone(
                add_user.entity.defaultRegion,
                msg='User obj expected a default region recieved {0}'.
                format(type(add_user.entity.defaultRegion)))

        self.assertIsNotNone(
                add_user.entity.id,
                msg='User obj expected an id recieved {0}'.
                format(type(add_user.entity.id)))

        self.assertIsNotNone(
                add_user.entity.username,
                msg='User obj expected a username recieved {0}'.
                format(type(add_user.entity.username)))

        self.assertEqual(
                add_user.entity.username,
                username,
                msg='User obj expected name {0} recieved {1}'.
                format(add_user.entity.name, username))

        self.assertIsNotNone(
                add_user.entity.email,
                msg='User obj expected an email recieved {0}'.
                format(type(add_user.entity.email)))

        self.assertEqual(
                add_user.entity.email,
                email,
                msg='User obj expected email {0} recieved {1}'.
                format(add_user.entity.email, email))

        self.assertIsNotNone(
                add_user.entity.enabled,
                msg='User obj expected enabled T/F recieved {0}'.
                format(type(add_user.entity.enabled)))

        self.assertEqual(
                add_user.entity.enabled,
                enabled_value,
                msg='User obj expected enabled {0} recieved {1}'.
                format(str(enabled_value), add_user.entity.enabled))

        '''
        If an initial password is generated, it is included in a successful
        response to this request. After the user is created, the password
        cannot be retrieved by any means. Make note of the password in the
        response and supply that password to the user.
        '''

        self.assertIsNotNone(
                add_user.entity.password,
                msg='User obj expected a password recieved {0}'.
                format(add_user.entity.password))

        delete_user = self.public_client.delete_user(
                userId=add_user.entity.id)

        self.assertEqual(
                delete_user.status_code,
                delete_code,
                msg='Delete user expected response {0} received {1}'.
                format(delete_code, delete_user.status_code))

        hard_delete_user = self.service_client.delete_user_hard(
                userId=add_user.entity.id)

        self.assertEqual(
                hard_delete_user.status_code,
                delete_code,
                msg='Hard delete user expected response {0} received {1}'.
                format(delete_code, hard_delete_user.status_code))

    @attr('regression', type='positive')
    def test_rax_user_add_user_generated_password_enabled_false(self):
        delete_code = 204
        enabled_value = False
        username = rand_name('cctestname')
        email = '{0}@foehammer.crom'.format(username)
        add_user = self.public_client.add_user(
                username=username,
                email=email,
                enabled=enabled_value)

        self.assertIsInstance(
                add_user.entity,
                User,
                msg='Get user expected a User obj recieved {0}'.
                format(type(add_user.entity)))

        self.assertIsNotNone(
                add_user.entity.defaultRegion,
                msg='User obj expected a default region recieved {0}'.
                format(type(add_user.entity.defaultRegion)))

        self.assertIsNotNone(
                add_user.entity.id,
                msg='User obj expected an id recieved {0}'.
                format(type(add_user.entity.id)))

        self.assertIsNotNone(
                add_user.entity.username,
                msg='User obj expected a username recieved {0}'.
                format(type(add_user.entity.username)))

        self.assertEqual(
                add_user.entity.username,
                username,
                msg='User obj expected name {0} recieved {1}'.
                format(add_user.entity.name, username))

        self.assertIsNotNone(
                add_user.entity.email,
                msg='User obj expected an email recieved {0}'.
                format(type(add_user.entity.email)))

        self.assertEqual(
                add_user.entity.email,
                email,
                msg='User obj expected email {0} recieved {1}'.
                format(add_user.entity.email, email))

        self.assertIsNotNone(
                add_user.entity.enabled,
                msg='User obj expected enabled T/F recieved {0}'.
                format(type(add_user.entity.enabled)))

        self.assertEqual(
                add_user.entity.enabled,
                enabled_value,
                msg='User obj expected enabled {0} recieved {1}'.
                format(str(enabled_value), add_user.entity.enabled))

        '''
        If an initial password is generated, it is included in a successful
        response to this request. After the user is created, the password
        cannot be retrieved by any means. Make note of the password in the
        response and supply that password to the user.
        '''

        self.assertIsNotNone(
                add_user.entity.password,
                msg='User obj expected a password recieved {0}'.
                format(add_user.entity.password))

        delete_user = self.public_client.delete_user(
                userId=add_user.entity.id)

        self.assertEqual(
                delete_user.status_code,
                delete_code,
                msg='Delete user expected response {0} received {1}'.
                format(delete_code, delete_user.status_code))

        hard_delete_user = self.service_client.delete_user_hard(
                userId=add_user.entity.id)

        self.assertEqual(
                hard_delete_user.status_code,
                delete_code,
                msg='Hard delete user expected response {0} received {1}'.
                format(delete_code, hard_delete_user.status_code))

    @attr('regression', type='positive')
    def test_rax_user_update_user_email(self):
        delete_code = 204
        enabled_value = True
        username = rand_name('cctestname')
        email = '{0}@foehammer.crom'.format(username)
        upd_email = '{0}@wahoo.com'.format(username)
        add_user = self.public_client.add_user(
                username=username,
                email=email,
                enabled=enabled_value)

        self.assertIsInstance(
                add_user.entity,
                User,
                msg='Get user expected a User obj recieved {0}'.
                format(type(add_user.entity)))

        self.assertIsNotNone(
                add_user.entity.defaultRegion,
                msg='User obj expected a default region recieved {0}'.
                format(type(add_user.entity.defaultRegion)))

        self.assertIsNotNone(
                add_user.entity.id,
                msg='User obj expected an id recieved {0}'.
                format(type(add_user.entity.id)))

        self.assertIsNotNone(
                add_user.entity.username,
                msg='User obj expected a username recieved {0}'.
                format(type(add_user.entity.username)))

        self.assertEqual(
                add_user.entity.username,
                username,
                msg='User obj expected name {0} recieved {1}'.
                format(add_user.entity.name, username))

        self.assertIsNotNone(
                add_user.entity.email,
                msg='User obj expected an email recieved {0}'.
                format(type(add_user.entity.email)))

        self.assertEqual(
                add_user.entity.email,
                email,
                msg='User obj expected email {0} recieved {1}'.
                format(add_user.entity.email, email))

        self.assertIsNotNone(
                add_user.entity.enabled,
                msg='User obj expected enabled T/F recieved {0}'.
                format(type(add_user.entity.enabled)))

        self.assertEqual(
                add_user.entity.enabled,
                enabled_value,
                msg='User obj expected enabled {0} recieved {1}'.
                format(str(enabled_value), add_user.entity.enabled))

        self.assertIsNotNone(
                add_user.entity.password,
                msg='User obj expected a password recieved {0}'.
                format(add_user.entity.password))

        upd_user = self.public_client.update_user(
                add_user.entity.id,
                email=upd_email)

        self.assertIsInstance(
                upd_user.entity,
                User,
                msg='Get user expected a User obj recieved {0}'.
                format(type(upd_user.entity)))

        self.assertIsNotNone(
                upd_user.entity.defaultRegion,
                msg='User obj expected a default region recieved {0}'.
                format(type(upd_user.entity.defaultRegion)))

        self.assertIsNotNone(
                upd_user.entity.id,
                msg='User obj expected an id recieved {0}'.
                format(type(upd_user.entity.id)))

        self.assertIsNotNone(
                upd_user.entity.username,
                msg='User obj expected a username recieved {0}'.
                format(type(upd_user.entity.username)))

        self.assertEqual(
                upd_user.entity.username,
                username,
                msg='User obj expected name {0} recieved {1}'.
                format(upd_user.entity.name, username))

        self.assertIsNotNone(
                upd_user.entity.email,
                msg='User obj expected an email recieved {0}'.
                format(type(upd_user.entity.email)))

        self.assertEqual(
                upd_user.entity.email,
                upd_email,
                msg='User obj expected email {0} recieved {1}'.
                format(upd_user.entity.email, upd_email))

        self.assertIsNotNone(
                upd_user.entity.enabled,
                msg='User obj expected enabled T/F recieved {0}'.
                format(type(upd_user.entity.enabled)))

        self.assertEqual(
                upd_user.entity.enabled,
                enabled_value,
                msg='User obj expected enabled {0} recieved {1}'.
                format(str(enabled_value), upd_user.entity.enabled))

        '''Password is only returned in the initial add user response'''

        delete_user = self.public_client.delete_user(
                userId=add_user.entity.id)

        self.assertEqual(
                delete_user.status_code,
                delete_code,
                msg='Delete user expected response {0} received {1}'.
                format(delete_code, delete_user.status_code))

        hard_delete_user = self.service_client.delete_user_hard(
                userId=add_user.entity.id)

        self.assertEqual(
                hard_delete_user.status_code,
                delete_code,
                msg='Hard delete user expected response {0} received {1}'.
                format(delete_code, hard_delete_user.status_code))

    @attr('regression', type='positive')
    def test_rax_user_update_user_name(self):
        delete_code = 204
        enabled_value = True
        username = rand_name('cctestname')
        email = '{0}@foehammer.crom'.format(username)
        upd_username = rand_name('secretsquirrel')
        add_user = self.public_client.add_user(
                username=username,
                email=email,
                enabled=enabled_value)

        self.assertIsInstance(
                add_user.entity,
                User,
                msg='Get user expected a User obj recieved {0}'.
                format(type(add_user.entity)))

        self.assertIsNotNone(
                add_user.entity.defaultRegion,
                msg='User obj expected a default region recieved {0}'.
                format(type(add_user.entity.defaultRegion)))

        self.assertIsNotNone(
                add_user.entity.id,
                msg='User obj expected an id recieved {0}'.
                format(type(add_user.entity.id)))

        self.assertIsNotNone(
                add_user.entity.username,
                msg='User obj expected a username recieved {0}'.
                format(type(add_user.entity.username)))

        self.assertEqual(
                add_user.entity.username,
                username,
                msg='User obj expected name {0} recieved {1}'.
                format(add_user.entity.name, username))

        self.assertIsNotNone(
                add_user.entity.email,
                msg='User obj expected an email recieved {0}'.
                format(type(add_user.entity.email)))

        self.assertEqual(
                add_user.entity.email,
                email,
                msg='User obj expected email {0} recieved {1}'.
                format(add_user.entity.email, email))

        self.assertIsNotNone(
                add_user.entity.enabled,
                msg='User obj expected enabled T/F recieved {0}'.
                format(type(add_user.entity.enabled)))

        self.assertEqual(
                add_user.entity.enabled,
                enabled_value,
                msg='User obj expected enabled {0} recieved {1}'.
                format(str(enabled_value), add_user.entity.enabled))

        self.assertIsNotNone(
                add_user.entity.password,
                msg='User obj expected a password recieved {0}'.
                format(add_user.entity.password))

        upd_user = self.public_client.update_user(
                add_user.entity.id,
                username=upd_username)

        self.assertIsInstance(
                upd_user.entity,
                User,
                msg='Get user expected a User obj recieved {0}'.
                format(type(upd_user.entity)))

        self.assertIsNotNone(
                upd_user.entity.defaultRegion,
                msg='User obj expected a default region recieved {0}'.
                format(type(upd_user.entity.defaultRegion)))

        self.assertIsNotNone(
                upd_user.entity.id,
                msg='User obj expected an id recieved {0}'.
                format(type(upd_user.entity.id)))

        self.assertIsNotNone(
                upd_user.entity.username,
                msg='User obj expected a username recieved {0}'.
                format(type(upd_user.entity.username)))

        self.assertEqual(
                upd_user.entity.username,
                upd_username,
                msg='User obj expected name {0} recieved {1}'.
                format(upd_user.entity.name, upd_username))

        self.assertIsNotNone(
                upd_user.entity.email,
                msg='User obj expected an email recieved {0}'.
                format(type(upd_user.entity.email)))

        self.assertEqual(
                upd_user.entity.email,
                email,
                msg='User obj expected email {0} recieved {1}'.
                format(email, upd_user.entity.email))

        self.assertIsNotNone(
                upd_user.entity.enabled,
                msg='User obj expected enabled T/F recieved {0}'.
                format(type(upd_user.entity.enabled)))

        self.assertEqual(
                upd_user.entity.enabled,
                enabled_value,
                msg='User obj expected enabled {0} recieved {1}'.
                format(str(enabled_value), upd_user.entity.enabled))

        '''Password is only returned in the initial add user response'''

        delete_user = self.public_client.delete_user(
                userId=add_user.entity.id)

        self.assertEqual(
                delete_user.status_code,
                delete_code,
                msg='Delete user expected response {0} received {1}'.
                format(delete_code, delete_user.status_code))

        hard_delete_user = self.service_client.delete_user_hard(
                userId=add_user.entity.id)

        self.assertEqual(
                hard_delete_user.status_code,
                delete_code,
                msg='Hard delete user expected response {0} received {1}'.
                format(delete_code, hard_delete_user.status_code))

    @attr('regression', type='positive')
    def test_rax_user_update_user_password(self):
        '''Note:>>> need to define regression test'''
        pass

    @attr('regression', type='positive')
    def test_rax_user_update_user_status(self):
        delete_code = 204
        enabled_value = True
        upd_value = False
        username = rand_name('cctestname')
        email = '{0}@foehammer.crom'.format(username)
        add_user = self.public_client.add_user(
                username=username,
                email=email,
                enabled=enabled_value)

        self.assertIsInstance(
                add_user.entity,
                User,
                msg='Get user expected a User obj recieved {0}'.
                format(type(add_user.entity)))

        self.assertIsNotNone(
                add_user.entity.defaultRegion,
                msg='User obj expected a default region recieved {0}'.
                format(type(add_user.entity.defaultRegion)))

        self.assertIsNotNone(
                add_user.entity.id,
                msg='User obj expected an id recieved {0}'.
                format(type(add_user.entity.id)))

        self.assertIsNotNone(
                add_user.entity.username,
                msg='User obj expected a username recieved {0}'.
                format(type(add_user.entity.username)))

        self.assertEqual(
                add_user.entity.username,
                username,
                msg='User obj expected name {0} recieved {1}'.
                format(add_user.entity.name, username))

        self.assertIsNotNone(
                add_user.entity.email,
                msg='User obj expected an email recieved {0}'.
                format(type(add_user.entity.email)))

        self.assertEqual(
                add_user.entity.email,
                email,
                msg='User obj expected email {0} recieved {1}'.
                format(add_user.entity.email, email))

        self.assertIsNotNone(
                add_user.entity.enabled,
                msg='User obj expected enabled T/F recieved {0}'.
                format(type(add_user.entity.enabled)))

        self.assertEqual(
                add_user.entity.enabled,
                enabled_value,
                msg='User obj expected enabled {0} recieved {1}'.
                format(str(enabled_value), add_user.entity.enabled))

        self.assertIsNotNone(
                add_user.entity.password,
                msg='User obj expected a password recieved {0}'.
                format(add_user.entity.password))

        upd_user = self.public_client.update_user(
                add_user.entity.id,
                enabled=upd_value)

        self.assertIsInstance(
                upd_user.entity,
                User,
                msg='Get user expected a User obj recieved {0}'.
                format(type(upd_user.entity)))

        self.assertIsNotNone(
                upd_user.entity.defaultRegion,
                msg='User obj expected a default region recieved {0}'.
                format(type(upd_user.entity.defaultRegion)))

        self.assertIsNotNone(
                upd_user.entity.id,
                msg='User obj expected an id recieved {0}'.
                format(type(upd_user.entity.id)))

        self.assertIsNotNone(
                upd_user.entity.username,
                msg='User obj expected a username recieved {0}'.
                format(type(upd_user.entity.username)))

        self.assertEqual(
                upd_user.entity.username,
                username,
                msg='User obj expected name {0} recieved {1}'.
                format(username, upd_user.entity.name))

        self.assertIsNotNone(
                upd_user.entity.email,
                msg='User obj expected an email recieved {0}'.
                format(type(upd_user.entity.email)))

        self.assertEqual(
                upd_user.entity.email,
                email,
                msg='User obj expected email {0} recieved {1}'.
                format(email, upd_user.entity.email))

        self.assertIsNotNone(
                upd_user.entity.enabled,
                msg='User obj expected enabled T/F recieved {0}'.
                format(type(upd_user.entity.enabled)))

        self.assertEqual(
                upd_user.entity.enabled,
                upd_value,
                msg='User obj expected enabled {0} recieved {1}'.
                format(str(upd_value), upd_user.entity.enabled))

        '''Password is only returned in the initial add user response'''

        delete_user = self.public_client.delete_user(
                userId=add_user.entity.id)

        self.assertEqual(
                delete_user.status_code,
                delete_code,
                msg='Delete user expected response {0} received {1}'.
                format(delete_code, delete_user.status_code))

        hard_delete_user = self.service_client.delete_user_hard(
                userId=add_user.entity.id)

        self.assertEqual(
                hard_delete_user.status_code,
                delete_code,
                msg='Hard delete user expected response {0} received {1}'.
                format(delete_code, hard_delete_user.status_code))

    @attr('regression', type='positive')
    def test_rax_user_delete_user(self):
        delete_code = 204
        enabled_values = [True, False]
        username = rand_name('cctestname')
        email = '{0}@foehammer.crom'.format(username)
        add_user = self.public_client.add_user(
                username=username,
                email=email,
                enabled=False)

        get_user_by_id = self.public_client.get_user_by_id(
                userId=add_user.entity.id)

        self.assertIsInstance(
                get_user_by_id.entity,
                User,
                msg='Get user expected a User obj recieved {0}'.
                format(type(get_user_by_id.entity)))

        get_user_by_name = self.public_client.get_user_by_name(name=username)

        self.assertIsInstance(
                get_user_by_name.entity,
                User,
                msg='Get user expected a User obj recieved {0}'.
                format(type(get_user_by_name.entity)))

        delete_user = self.public_client.delete_user(
                userId=add_user.entity.id)

        get_user_by_id = self.public_client.get_user_by_id(
                userId=add_user.entity.id)

        self.assertIsNone(
                get_user_by_id.entity,
                msg='After Delete Get user expected None recieved {0}'.
                format(type(get_user_by_id.entity)))

        get_user_by_name = self.public_client.get_user_by_name(name=username)

        self.assertIsNone(
                get_user_by_name.entity,
                msg='After Delete Get user expected None recieved {0}'.
                format(type(get_user_by_name.entity)))

        hard_delete_user = self.service_client.delete_user_hard(
                userId=add_user.entity.id)

    @attr('regression', type='positive')
    def test_rax_user_list_credentials(self):
        list_users = self.public_client.list_users()
        userId = list_users.entity[0].id
        list_credentials = self.public_client.list_credentials(userId=userId)

        for cred in list_credentials.entity:
            self.assertIsInstance(
                    cred,
                    ApiKeyCredentials,
                    msg='Expected a ApiKeyCredentials obj recieved {0}'.
                    format(type(cred)))
            self.assertIsNotNone(
                    cred.username,
                    msg='Cred obj expected a username recieved {0}'.
                format(cred.username))
            self.assertIsNotNone(
                    cred.apiKey,
                    msg='Cred obj expected an api key recieved {0}'.
                    format(cred.apiKey))

    @attr('regression', type='positive')
    def test_rax_list_users_by_email(self):

        normal_response_codes = [200, 203]
        password = "Gusrpass8"

        client_map = {self.service_client: [self.service_client,
                                            self.admin_client,
                                            self.public_client],
                      self.admin_client: [self.public_client,
                                          self.admin_client],
                      self.public_client: [self.public_client]}

        client_keys = client_map.keys()
        for client in client_keys:
            creator_client_list = client_map[client]
            for creator_client in creator_client_list:
                emailhead = rand_name("listemailverfiy")
                email = '{0}@{1}'.format(emailhead + ".testbox",
                                         "mailtrust.com")
                username_list = []
                userid_list = []
                num_of_users = 0
                total_users = 5
                while num_of_users != total_users:
                    username = rand_name("ccuser")
                    username_list.append(username)
                    create_user_resp = creator_client.add_user(
                            username=username,
                            email=email,
                            enabled=True,
                            password=password)
                    num_of_users = num_of_users + 1
                    userid_list.append(create_user_resp.entity.id)

                list_users = client.list_users(email=email)
                self.assertIn(list_users.status_code, normal_response_codes,
                              msg='List users expected to return {0} '
                              'received {1}'.format(normal_response_codes,
                                                    list_users.status_code))

                user_count = 0
                for user in list_users.entity:
                    if user.username in username_list:
                        user_count = user_count + 1

                self.assertEqual(
                        user_count,
                        total_users,
                        msg='List users by email failed')

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

    @attr('regression', type='positive')
    def test_rax_user_get_credentials(self):
        pass
        #delete_code = 204
        #enabled_value = True
        #username = rand_name('cctestname')
        #email = '{0}@foehammer.crom'.format(username)
        #add_user = self.public_client.add_user(
        #        username=username,
        #        email=email,
        #        enabled=enabled_value)
        #
        #print add_user.entity
        #
        #cred = self.public_client.get_user_credentials(
        #        userId=add_user.entity.id)
        #
        #print type(cred.entity)

        #self.assertIsInstance(
        #        cred.entity,
        #        ApiKeyCredentials,
        #        msg='Expected a ApiKeyCredentials obj recieved {0}'.
        #        format(type(cred.entity)))
        #
        #self.assertIsNotNone(
        #    cred.entity.username,
        #    msg='Cred obj expected a username recieved {0}'.
        #    format(cred.username))
        #
        #self.assertIsNotNone(
        #    cred.apiKey,
        #    msg='Cred obj expected an api key recieved {0}'.
        #    format(cred.apiKey))
        #
        #delete_user = self.public_client.delete_user(
        #        userId=add_user.entity.id)
        #
        #self.assertEqual(
        #        delete_user.status_code,
        #        delete_code,
        #        msg='Delete user expected response {0} received {1}'.
        #        format(delete_code, delete_user.status_code))
        #
        #hard_delete_user = self.service_client.delete_user_hard(
        #        userId=add_user.entity.id)
        #
        #self.assertEqual(
        #        hard_delete_user.status_code,
        #        delete_code,
        #        msg='Hard delete user expected response {0} received {1}'.
        #        format(delete_code, hard_delete_user.status_code))
