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

    @attr('regression', type='positive')
    def test_list_admin_users(self):
        list_users = self.public_client.list_users()

        self.assertTrue(
                list_users.entity[0].id is not None,
                msg="ID is present")
        self.assertGreaterEqual(
                len(list_users.entity),
                0,
                msg="There is at least one child tenant")

    @attr('regression', type='positive')
    def test_get_user_by_name_admin(self):
        list_users = self.public_client.list_users()
        username = list_users.entity[0].username
        get_user = self.public_client.get_user_by_name(
                name=username)

        self.assertFalse(
                type(get_user.entity) is list,
                msg="Received list object instead of single one")

        self.assertTrue(
                get_user.entity.enabled is not None,
                msg="Enabled field present")
        self.assertEqual(
                get_user.entity.username, username,
                msg="User Id match")

    @attr('regression', type='positive')
    def test_get_user_by_id_admin(self):
        list_users = self.public_client.list_users()
        userId = list_users.entity[0].id
        get_user = self.public_client.get_user_by_id(
                userId=userId)

        self.assertTrue(
                get_user.entity.enabled is not None,
                msg="Enabled field present")
        self.assertEqual(
                get_user.entity.id, userId,
                msg="User Id match")

    @attr('regression', type='positive')
    def test_create_user_admin_with_password(self):
        username = rand_name("ccadminname_password")
        email = username + "@supra.com"
        domainId = "421342654"
        defaultRegion = "DFW"
        create_user = self.admin_client.add_user(
                username=username,
                email=email,
                enabled=True,
                defaultRegion=defaultRegion,
                domainId=domainId,
                password="Gadmpass8")

        self.assertTrue(
                create_user.entity.enabled is not None,
                msg="Enabled state not none but received  %s" %
                create_user.entity.enabled)
        self.assertEqual(
                create_user.entity.username, username,
                msg="Expected username is %s but received  %s" %
                (username, create_user.entity.username))
        self.assertEqual(
                create_user.entity.email, email,
                msg="Expected email is %s but received  %s" %
                (email, create_user.entity.email))
        self.assertEqual(
                create_user.entity.domainId, domainId,
                msg="Expected domain Id is %s but received  %s" %
                (domainId, create_user.entity.domainId))
        self.assertEqual(
                create_user.entity.defaultRegion, defaultRegion,
                msg="Expected default Region is %s but received  %s" %
                (defaultRegion, create_user.entity.defaultRegion))
        delete_user = self.public_client.delete_user(
                userId=create_user.entity.id)
        self.assertEqual(
                delete_user.status_code, 204,
                msg="Expected response 204 but received  %s" %
                delete_user.status_code)

        self.addCleanup(
                self.service_client.delete_user_hard,
                userId=create_user.entity.id)

    @attr('regression', type='positive')
    def test_delete_user_admin(self):
        username = rand_name("ccadminname_delete")
        email = username + "@supra.com"
        domainId = "421342987"
        defaultRegion = "DFW"
        create_user = self.admin_client.add_user(
                username=username,
                email=email,
                enabled=True,
                defaultRegion=defaultRegion,
                domainId=domainId,
                password="Gadmpass8")
        delete_user = self.public_client.delete_user(
                userId=create_user.entity.id)

        get_user = self.public_client.get_user_by_id(
                userId=create_user.entity.id)
        self.assertEqual(
                get_user.status_code, 404,
                msg="Response is not 404")
        self.assertTrue(
                'was not found.' in get_user.content,
                msg="Expecting 'There is no such a user' received %s" %
                get_user.content)

        self.addCleanup(
                self.service_client.delete_user_hard,
                userId=create_user.entity.id)

    @attr('regression', type='positive')
    def test_update_user_admin(self):
        username = rand_name("ccadminname_update")
        email = username + "@supra.com"
        domainId = "421342147"
        defaultRegion = "DFW"
        updated_username = rand_name("upduser")
        updated_email = "example@hotmail.com"
        create_user = self.admin_client.add_user(
                username=username,
                email=email,
                enabled=True,
                defaultRegion=defaultRegion,
                domainId=domainId,
                password="Gadmpass8")
        update_user = self.public_client.update_user(
                userId=create_user.entity.id,
                username=updated_username,
                email=updated_email,
                enabled=False)

        self.assertEqual(
                update_user.entity.username,
                updated_username,
                msg="Expected username is %s received %s" %
                (updated_username, update_user.entity.username))
        self.assertEqual(
                update_user.entity.email,
                updated_email,
                msg="Expected email is %s received %s" %
                (updated_email, update_user.entity.email))
        delete_user = self.public_client.delete_user(
                userId=create_user.entity.id)
        self.assertEqual(
                delete_user.status_code,
                204,
                msg="Expected response 204 received %s" %
                delete_user.status_code)

        self.addCleanup(
                self.service_client.delete_user_hard,
                userId=create_user.entity.id)

    @attr('regression', type='positive')
    def test_get_user_credentials(self):
        list_users = self.public_client.list_users()
        userId = list_users.entity[0].id
        get_credentials = self.admin_client.get_user_credentials(
                userId=userId)

        self.assertTrue(
                get_credentials.entity.apiKey is not None,
                msg="apiKey is present")
        self.assertTrue(
                get_credentials.entity.username is not None,
                msg="username is present")

    @attr('regression', type='positive')
    def test_add_user_credentials(self):
        username = rand_name("ccadminupdatecred")
        email = username + "@supra.com"
        domainId = "421342123"
        defaultRegion = "DFW"
        updated_pass = rand_name("Password")
        create_user = self.admin_client.add_user(
                username=username,
                email=email,
                enabled=True,
                defaultRegion=defaultRegion,
                domainId=domainId,
                password="Gadmpass8")
        add_credentials = self.admin_client.add_user_credentials(
                userId=create_user.entity.id,
                username=username,
                password=updated_pass)

        self.assertEqual(
                add_credentials.entity.username, username,
                msg="Expected username is %s received %s" %
                (username, add_credentials.entity.username))
        self.assertEqual(
                add_credentials.entity.password, updated_pass,
                msg="Expected password is %s received %s" %
                (updated_pass, add_credentials.entity.password))
        delete_user = self.public_client.delete_user(
                userId=create_user.entity.id)
        self.assertEqual(
                delete_user.status_code,
                204,
                msg="Expected response 204 received %s" %
                delete_user.status_code)

        self.addCleanup(
                self.service_client.delete_user_hard,
                userId=create_user.entity.id)

    @attr('regression', type='positive')
    def test_list_credentials(self):
        list_users = self.public_client.list_users()
        userId = list_users.entity[0].id
        list_credentials = self.public_client.list_credentials(
                userId=userId)

        self.assertTrue(
                list_credentials.entity[0].apiKey is not None,
                msg="apiKey is present")
        self.assertTrue(
                list_credentials.entity[0].username is not None,
                msg="username is present")

    @attr('regression', type='positive')
    def test_update_user_credentials(self):
        list_users = self.public_client.list_users()
        userId = list_users.entity[0].id
        username = list_users.entity[0].username
        updated_apiKey = "aaaaa-bbbbb-ccccc-12345678"
        list_credentials = self.public_client.list_credentials(
                userId=userId)
        update_credentials = self.admin_client.update_user_credentials(
                userId=userId,
                username=username,
                apiKey=updated_apiKey)

        self.assertEqual(
                update_credentials.entity.username,
                username,
                msg="Expected username is %s received %s" %
                (username, update_credentials.entity.username))
        self.assertEqual(
                update_credentials.entity.apiKey,
                updated_apiKey,
                msg="Expected password is %s received %s" %
                (updated_apiKey, update_credentials.entity.apiKey))

    @attr('regression', type='positive')
    def test_delete_user_credentials(self):
        '''TODO: add tests for admin delete user credentials'''

    @attr('regression', type='positive')
    def test_admin_get_user_credentials(self):
        '''TODO: add tests for admin get user credentials'''

    @attr('regression', type='positive')
    def test_admin_reset_user_api_key(self):
        '''TODO: add tests for reset user api key'''
