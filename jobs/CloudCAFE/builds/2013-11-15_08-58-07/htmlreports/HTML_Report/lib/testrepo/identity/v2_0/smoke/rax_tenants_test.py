from testrepo.common.testfixtures.identity.v2_0.identity \
    import UserAdminFixture
from ccengine.common.decorators import attr


class TenantsTest(UserAdminFixture):
    @classmethod
    def setUpClass(cls):
        super(TenantsTest, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        pass

    @attr('smoke', type='positive')
    def test_get_tenants(self):
        normal_response_codes = [200, 203]
        tenant_resp = self.public_client.get_tenants()

        self.assertIn(
            tenant_resp.status_code, normal_response_codes,
            msg='Get tenants expected {0} recieved {1}'.format(
                normal_response_codes, tenant_resp.status_code))
