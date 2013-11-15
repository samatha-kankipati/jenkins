from testrepo.common.testfixtures.loggingaas import TenantFixture


class CreateTenantSmokeTests(TenantFixture):

    @classmethod
    def setUpClass(cls):
        super(CreateTenantSmokeTests, cls).setUpClass()

    def test_create_tenant(self):
        tenant_req = self.provider.create_tenant()
        self.assertEqual(201, tenant_req.status_code,
                         'status code should have been 201 created')

    def test_get_tenant(self):
        tenant_req = self.provider.create_tenant()
        tenant_url = tenant_req.headers.get('location')
        tenantobj = self.provider.get_tenant(tenant_url=tenant_url)
        self.assertEqual(self.provider.config.loggingaas.tenant_id,
                         tenantobj[0].tenant_id)
