from testrepo.common.testfixtures.identity.v2_0.identity \
    import IdentityAdminFixture
from ccengine.common.decorators import attr


class AdminTenantsTest(IdentityAdminFixture):

    @classmethod
    def setUpClass(cls):
        super(AdminTenantsTest, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        pass

    @attr('smoke', type='positive')
    def test_admin_get_tenants(self):
        normal_response_codes = [200, 203]
        get_tenants = \
                self.public_client.get_tenants()

        self.assertIn(get_tenants.status_code, normal_response_codes,
                msg='Admin get tenants expected %s recieved %s' %
                (normal_response_codes, get_tenants.status_code))

    @attr('smoke', type='positive')
    def test_admin_get_tenant_by_name(self):
        normal_response_codes = [200, 203]
        auth_resp = self.public_client.get_tenants()
        tenant_info = self.admin_client.get_tenant_by_name(
                name=auth_resp.entity[0].name)

        self.assertIn(tenant_info.status_code, normal_response_codes,
                msg='Admin get tenants by name expected %s recieved %s' %
                (normal_response_codes, tenant_info.status_code))

    @attr('smoke', type='positive')
    def test_admin_get_tenant_by_id(self):
        normal_response_codes = [200, 203]
        auth_resp = self.public_client.get_tenants()
        tenant_info = self.admin_client.get_tenant_by_id(
                tenantId=auth_resp.entity[0].id)

        self.assertIn(tenant_info.status_code, normal_response_codes,
                msg='Admin get tenants by id expected %s recieved %s' %
                (normal_response_codes, tenant_info.status_code))

    @attr('smoke', type='positive')
    def test_admin_list_roles_for_user_on_tenant(self):
        normal_response_codes = [200, 203]
        get_user = \
                self.public_client.get_user_by_name(
                        name=self.config.identity_api.username)
        user_roles = \
                self.admin_client.list_roles_for_user_on_tenant(
                        tenantId=self.config.identity_api.tenant_id,
                        userId=get_user.entity.id)

        self.assertIn(user_roles.status_code, normal_response_codes,
                msg='Admin list roles for user on tenant expected' + \
                '%s recieved %s' %
                (normal_response_codes, user_roles.status_code))
