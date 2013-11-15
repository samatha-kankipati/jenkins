from ccengine.common.tools.datagen import rand_name
from testrepo.common.testfixtures.identity.v2_0.identity \
    import UserAdminFixture
from ccengine.domain.identity.v2_0.response.role import Role
from ccengine.common.decorators import attr


class RolesTest(UserAdminFixture):
    @classmethod
    def setUpClass(cls):
        """
        Function to create test bed for all the test. Execute once at the
        beginning of class
        @param cls: instance of class
        """
        super(RolesTest, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        """
        Function to clean up the data after execution of all the tests
        completed. Execute once at the end of all the tests.
        @param cls: instance of class
        """
        pass

    @attr('smoke', type='positive')
    def test_list_user_global_roles_admin_user(self):
        """
        Verifies global roles of admin user
        """
        normal_response_codes = [200, 203]
        list_roles = self.public_client.list_user_global_roles(
            user_id=self.config.identity_api.id)

        self.assertIn(list_roles.status_code,
                      normal_response_codes,
                      msg="Response for List user's global roles expected "
                          "{0}".format(normal_response_codes))
        for role in list_roles.entity:
            self.assertIsInstance(role, Role)

    @attr('smoke', type='positive')
    def test_list_user_global_roles_default_user(self):
        """
        Verifies global roles of default user
        """
        normal_response_codes = [200, 203]
        username = rand_name("cctestname")
        email = '{0}@{1}'.format(username, 'mailtrust.com')
        add_user = self.public_client.add_user(username=username,
                                               email=email,
                                               enabled=False,
                                               password="Gellpass8")
        self.assertEqual(add_user.status_code, 201,
                         msg="Response for Add user is not 201.")
        # delete user after test completion
        self.addCleanup(self.delete_user_permanently,
                        user_id=add_user.entity.id,
                        client=self.public_client)

        list_roles = self.public_client.list_user_global_roles(
            user_id=add_user.entity.id)

        self.assertIn(list_roles.status_code,
                      normal_response_codes,
                      msg="Response for list roles is not in "
                          "{0}".format(normal_response_codes))
        for role in list_roles.entity:
            self.assertIsInstance(role, Role)
