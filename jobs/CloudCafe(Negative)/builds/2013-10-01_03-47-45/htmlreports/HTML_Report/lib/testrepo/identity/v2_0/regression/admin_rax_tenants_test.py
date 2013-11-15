"""Basic Positive Tests for Rax Auth Tenants"""
from testrepo.common.testfixtures.identity.v2_0.identity \
    import IdentityAdminFixture
from ccengine.common.decorators import attr


class AdminTenantsTest(IdentityAdminFixture):
    """Basic Smoke Tests - Check HTTP Resoponses Tenants Admin"""

    @classmethod
    def setUpClass(cls):
        super(AdminTenantsTest, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        pass

    @attr('regression', type='positive')
    def test_get_tenants(self):
        auth_resp = self.public_client.get_tenants()
        self.assertEqual(auth_resp.status_code, 200,
                msg="Expected response 200 but received  %s" %
                auth_resp.status_code)
        self.assertTrue(auth_resp.entity[0].id is not None,
                msg="ID is present")
        self.assertGreaterEqual(len(auth_resp.entity), 0,
                msg="There is at least one child tenant")

    @attr('regression', type='positive')
    def test_get_tenant_by_name(self):
        auth_resp = self.public_client.get_tenants()
        self.assertEqual(auth_resp.status_code, 200,
                msg="Expected response 200 but received  %s" %
                auth_resp.status_code)
        tenant_info = self.admin_client.get_tenant_by_name(
                name=auth_resp.entity[0].name)
        self.assertEqual(tenant_info.status_code, 200,
                msg="Expected response 200 but received  %s" %
                tenant_info.status_code)
