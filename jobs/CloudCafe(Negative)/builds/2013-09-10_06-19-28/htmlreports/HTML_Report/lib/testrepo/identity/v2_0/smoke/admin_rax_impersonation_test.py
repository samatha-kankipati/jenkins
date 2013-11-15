from testrepo.common.testfixtures.identity.v2_0.identity \
        import IdentityAdminFixture
from ccengine.common.decorators import attr


class AdminImpersonationTest(IdentityAdminFixture):

    @classmethod
    def setUpClass(cls):
        super(AdminImpersonationTest, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        pass

    @attr('smoke', type='positive')
    def test_admin_impersonate_user(self):
        imp_time = 30   # In seconds
        user_impersonate = self.admin_client.impersonate_user(
                username=self.config.identity_api.username,
                expire_in_seconds=imp_time)

        self.assertEqual(user_impersonate.status_code, 200,
                msg="Admin impersonate user expected response 200 received %s"
                % user_impersonate.status_code)
