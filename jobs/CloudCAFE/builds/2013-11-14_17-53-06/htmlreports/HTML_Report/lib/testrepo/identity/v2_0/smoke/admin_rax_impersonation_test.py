from ccengine.common.decorators import attr
from testrepo.common.testfixtures.identity.v2_0.identity \
    import IdentityAdminFixture


class AdminImpersonationTest(IdentityAdminFixture):
    @classmethod
    def setUpClass(cls):
        super(AdminImpersonationTest, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        pass

    @attr('smoke', type='positive')
    def test_admin_impersonate_user(self):
        imp_time = 30  # In seconds
        user_impersonate = self.admin_client.impersonate_user_expire_in(
            username=self.config.identity_api.username,
            expire_in_seconds=imp_time)

        self.assertEqual(
            user_impersonate.status_code,
            200,
            msg='Admin impersonate user response 200 received {0}'.format(
                user_impersonate.status_code))
