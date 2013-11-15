from ccengine.common.decorators import attr
from ccengine.common.tools.datagen import rand_name, random_int
from testrepo.common.testfixtures.identity.v2_0.identity \
    import IdentityAdminFixture


class AdminNegativeRolesTest(IdentityAdminFixture):
    @classmethod
    def setUpClass(cls):
        """
        Function to create test bed for all the test. Execute once at the
        beginning of class
        @param cls: class
        """
        super(AdminNegativeRolesTest, cls).setUpClass()
        cls.domain_id = random_int(10000, 90000)
        password = cls.config.identity_api.password
        user_admin_name = rand_name("ccuseradmin")
        cls.user_admin = cls.get_test_user_v2_0(
            client=cls.admin_client,
            username=user_admin_name,
            password=password,
            domain_id=cls.domain_id)
        cls.user_admin_client = cls.provider.get_client(
            username=user_admin_name,
            password=password)

    @classmethod
    def tearDownClass(cls):
        """
        Function to clean up the data after execution of all the tests
        completed. Execute once at the end of all the tests.
        @param cls: class
        """
        cls.delete_user_permanently(user_id=cls.user_admin.entity.id,
                                    client=cls.admin_client)
        cls.service_client.delete_domain(domain_id=cls.domain_id)

    @attr('regression', type='negative')
    def test_list_identity_admin_roles_with_user_admin_token(self):
        """
        Verifies that user admin can not list identity admin roles
        @return:
        """
        identity_user_id = self.service_client.get_user_by_name(
            name=self.config.identity_api.admin_username).entity.id
        iden_global_roles = self.user_admin_client.list_user_global_roles(
            user_id=identity_user_id)
        self.assertEqual(
            iden_global_roles.status_code, 403,
            msg="User admin is able to get global role for identity admin.")
