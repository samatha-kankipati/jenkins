from ccengine.common.tools.datagen import rand_name
from testrepo.common.testfixtures.identity.v2_0.identity \
    import UserAdminFixture
from ccengine.common.decorators import attr


class RolesTest(UserAdminFixture):

    @classmethod
    def setUpClass(cls):
        super(RolesTest, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        pass

    @attr('smoke', type='positive')
    def test_list_user_global_roles_admin_user(self):
        normal_response_codes = [200, 203]
        list_roles = self.public_client.list_user_global_roles(
                userId=self.config.identity_api.id)

        self.assertIn(
                list_roles.status_code,
                normal_response_codes,
                msg='List user global roles expected {0} recieved {1}'.
                format(normal_response_codes, list_roles.status_code))

    @attr('smoke', type='positive')
    def test_list_user_global_roles_default_user(self):
        normal_response_codes = [200, 203]
        delete_code = 204
        username = rand_name("cctestname")
        email = '{0}@{1}'.format(username, 'supra.com')
        add_user = self.public_client.add_user(
                username=username,
                email=email,
                enabled=False,
                password="Gellpass8")
        list_roles = self.public_client.list_user_global_roles(
                userId=add_user.entity.id)

        self.assertIn(
                list_roles.status_code,
                normal_response_codes,
                msg='List roles expected {0} recieved {1}'.
                format(normal_response_codes, list_roles.status_code))

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
