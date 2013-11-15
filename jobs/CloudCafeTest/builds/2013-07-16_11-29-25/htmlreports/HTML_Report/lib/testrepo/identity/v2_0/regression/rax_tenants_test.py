from testrepo.common.testfixtures.identity.v2_0.identity \
    import UserAdminFixture
from ccengine.common.decorators import attr
from ccengine.domain.identity.v2_0.response.tenant import Tenants, Tenant


class TenantsTest(UserAdminFixture):

    @classmethod
    def setUpClass(cls):
        super(TenantsTest, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        pass

    @attr('regression', type='positive')
    def test_get_tenants(self):
        '''NOTE:>>> this call returns members ! in the docs'''
        tenant_resp = self.public_client.get_tenants()

        self.assertIsInstance(
                tenant_resp.entity,
                Tenants,
                msg='Get tenants expected a Tenants obj recieved {0}'.
                format(tenant_resp.entity))

        for tenant in tenant_resp.entity:
            self.assertIsInstance(
                    tenant,
                    Tenant)
            self.assertIsNotNone(
                    tenant.id,
                    msg='Tenant obj expected an id recieved'.
                    format(type(tenant.id)))
            self.assertIsNotNone(
                    tenant.name,
                    msg='Tenant obj expected a name recieved'.
                    format(type(tenant.name)))
            self.assertIsNotNone(
                    tenant.enabled,
                    msg='Tenant obj expected enabled recieved'.
                    format(type(tenant.enabled)))
