from ccengine.clients.identity.v2_0.rax_auth_api import IdentityClient
from ccengine.common.decorators import attr
from ccengine.common.tools.datagen import rand_name
from ccengine.common.tools.datagen import random_int
from testrepo.common.testfixtures.identity.v2_0.identity \
    import IdentityAdminFixture


class AdminRolesTest(IdentityAdminFixture):
    """
    This test class is for test related to Admin roles.
    """

    @classmethod
    def setUpClass(cls):
        """
        Function to create test bed for all the test. Execute once at the
        beginning of class
        @param cls: instance of class
        """
        super(AdminRolesTest, cls).setUpClass()
        username = cls.config.identity_api.username
        api_key = cls.config.identity_api.api_key
        user_admin_auth = cls.public_client.authenticate_user_apikey(
            username=username, api_key=api_key).entity
        endpoint = cls.config.identity_api.authentication_endpoint
        serializer = cls.config.misc.serializer
        deserializer = cls.config.misc.deserializer
        cls.user_admin_client = IdentityClient(
            url=endpoint,
            serialize_format=serializer,
            deserialize_format=deserializer,
            auth_token=user_admin_auth.token.id)

        name = rand_name("Guest:Role")
        description = rand_name("Guest description ")
        cls.add_roles = cls.admin_client.add_role(name=name,
                                                  description=description)

        user_name = rand_name('ccadminname')
        email = cls.config.identity_api.default_email
        cls.domain_id = random_int(10000, 90000)
        cls.create_user = cls.admin_client.add_user(
            username=user_name,
            email=email,
            enabled=True,
            domain_id=cls.domain_id,
            password='Gadmpass8')

    @classmethod
    def tearDownClass(cls):
        """
        Function to clean up the data after execution of all the tests
        completed. Execute once at the end of all the tests.
        @param cls: instance of class
        """
        cls.admin_client.delete_role(role_id=cls.add_roles.entity.id)
        cls.delete_user_permanently(user_id=cls.create_user.entity.id,
                                    client=cls.admin_client)
        cls.admin_client.delete_domain(domain_id=cls.domain_id)

    @attr('smoke', type='positive')
    def test_identity_admin_list_roles(self):
        """
        Test for get the role list as identity admin
        """
        list_roles = self.admin_client.list_roles()
        self.assertEqual(list_roles.status_code,
                         200,
                         msg="Response is not 200")

    @attr('smoke', type='positive')
    def test_identity_admin_list_roles_limit(self):
        """
        Test for get the role list using limit as identity admin
        """
        list_roles = self.admin_client.list_roles(limit=5)
        self.assertEqual(list_roles.status_code,
                         200,
                         msg="Response is not 200")

    @attr('smoke', type='positive')
    def test_identity_admin_list_roles_marker(self):
        """
        Test for get the role list using marker as identity admin
        """
        list_roles = self.admin_client.list_roles(marker='5')
        self.assertEqual(list_roles.status_code,
                         200,
                         msg="Response is not 200")

    @attr('smoke', type='positive')
    def test_identity_admin_list_roles_service_id(self):
        """
        Test for get the role list using service id as identity admin
        """
        list_roles = self.admin_client.list_roles(service_id='a')
        self.assertEqual(list_roles.status_code,
                         200,
                         msg="Response is not 200")

    @attr('smoke', type='positive')
    def test_identity_admin_list_roles_limit_marker(self):
        """
        Test for get the role list using limit and marker as identity admin
        """
        list_roles = self.admin_client.list_roles(limit=5, marker=5)
        self.assertEqual(list_roles.status_code,
                         200,
                         msg="Response is not 200")

    @attr('smoke', type='positive')
    def test_identity_admin_list_roles_limit_marker_service_id(self):
        """
        Test for get the role list using limit, marker and service id as
        identity admin
        """
        list_roles = self.admin_client.list_roles(limit=5,
                                                  marker=5,
                                                  service_id='a')
        self.assertEqual(list_roles.status_code,
                         200,
                         msg="Response is not 200")

    @attr('smoke', type='positive')
    def test_identity_admin_add_and_delete_role(self):
        """
        Test for add and delete role as identity admin
        """
        name = rand_name("Guest:Role")
        description = rand_name("Guest description ")
        add_roles = self.admin_client.add_role(name=name,
                                               description=description)
        self.assertEqual(add_roles.status_code, 201, msg="Response is not 201")

        delete_role = self.admin_client.delete_role(
            role_id=add_roles.entity.id)
        self.assertEqual(delete_role.status_code,
                         204,
                         msg="Response is not 204")

    @attr('smoke', type='positive')
    def test_identity_admin_get_role(self):
        """
        Test for get role by id using identity admin
        """
        self.assertEqual(
            self.add_roles.status_code, 201,
            msg="Response is not 201")

        get_role = self.admin_client.get_role(
            role_id=self.add_roles.entity.id)
        self.assertEqual(get_role.status_code,
                         200,
                         msg="Response is not 200")

    @attr('smoke', type='positive')
    def test_identity_admin_add_and_delete_global_role_to_user(self):
        """
        Test for adding and deleting global role from user as identity admin
        """
        self.assertEqual(
            self.add_roles.status_code, 201,
            msg="Response is not 201")
        role_id = self.add_roles.entity.id

        self.assertEqual(
            self.create_user.status_code, 201,
            msg='Create user expected response 201, received {0}'.format(
                self.create_user.status_code))

        user_id = self.create_user.entity.id
        add_global_role = self.admin_client.add_role_to_user(user_id=user_id,
                                                             role_id=role_id)
        self.assertEqual(add_global_role.status_code,
                         200,
                         msg="Response is not 200")
        # delete role from user after test completion
        self.addCleanup(self.admin_client.delete_role_from_user,
                        user_id=user_id,
                        role_id=role_id)

        list_user_role = self.admin_client.list_user_global_roles(
            user_id=user_id)
        self.assertEqual(list_user_role.status_code,
                         200,
                         msg="Response is not 200")

        delete_user_role = self.admin_client.delete_role_from_user(
            user_id=user_id,
            role_id=role_id)
        self.assertEqual(delete_user_role.status_code,
                         204,
                         msg="Response is not 204")

    @attr('smoke', type='positive')
    def test_identity_admin_list_user_global_roles(self):
        """
        Test for get global role functionality of identity admin
        """
        self.assertEqual(
            self.create_user.status_code, 201,
            msg='Create user expected response 201, received {0}'.format(
                self.create_user.status_code))

        user_id = self.create_user.entity.id
        list_user_role = self.admin_client.list_user_global_roles(
            user_id=user_id)
        self.assertEqual(list_user_role.status_code,
                         200,
                         msg="Response is not 200")
        self.assertTrue(list_user_role.entity[0].name is not None,
                        msg="name is not present")
