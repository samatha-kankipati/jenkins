from testrepo.common.testfixtures.identity.v2_0.identity \
    import IdentityAdminFixture
from ccengine.common.decorators import attr
from ccengine.common.tools.datagen import rand_name
import unittest2
import time


class AdminImpersonationTest(IdentityAdminFixture):

    @classmethod
    def setUpClass(cls):
        super(AdminImpersonationTest, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        pass

    @attr('regression', type='positive')
    def test_admin_impersonate_user(self):
        imp_time = 30   # In seconds
        user_impersonate = self.admin_client.impersonate_user_expire_in(
                username=self.config.identity_api.username,
                expire_in_seconds=imp_time)

        self.assertTrue(user_impersonate.entity.token.id is not None,
                msg="apiKey is present")
        self.assertTrue(user_impersonate.entity.token.expires is not None,
                msg="apiKey is present")

    @unittest2.skip('Invalid test - needs to be fixed')
    @attr('regression', type='positive')
    def test_impersonation_token_expiration(self):
        username = rand_name("cctestname")
        email = '@'.join([username, 'supra.com'])
        domains = self.admin_client.get_domains().entity
        create_user = self.admin_client.add_user(
            username=username,
            email=email,
            enabled=False,
            password="Gellpass8",
            domainId=domains[0].id)
        self.addCleanup(self.service_client.delete_user_hard,
                        userId=create_user.entity.id)
        self.addCleanup(self.public_client.delete_user,
                        userId=create_user.entity.id)
        token_resp = self.admin_client.impersonate_user_expire_in(username, 10)
        token_check = self.admin_client.authenticate_tenantname_and_token(
            self.config.identity_api.tenant_id, token_resp.entity.token.id)
        self.assertEquals(token_check.status_code, 200)
        time.sleep(self.config.identity_api.wait_time)
        token_check = self.admin_client.authenticate_tenantid_and_token(
            create_user.entity.id, token_resp.entity.token.id)
        self.assertEquals(token_check.status_code, 200)
