"""Basic Positive Tests for Rax Auth Tenants"""
from ccengine.common.tools.datagen import rand_name, random_int
from testrepo.common.testfixtures.identity.v2_0.identity \
    import IdentityAdminFixture
from ccengine.common.decorators import attr


class AdminTenantsTest(IdentityAdminFixture):
    """Basic Smoke Tests - Check HTTP Responses Tenants Admin"""

    @classmethod
    def setUpClass(cls):
        """
        Function to create test bed for all the test. Execute once at the
        beginning of class
        @param cls: class
        """
        super(AdminTenantsTest, cls).setUpClass()
        cls.password = cls.config.identity_api.password
        cls.tenant_name = rand_name("cctenant")
        cls.created_tenant = cls.admin_client.add_tenant(
            name=cls.tenant_name,
            description="Tenant for testing",
            enabled=True)
        cls.tenant_id = cls.created_tenant.entity.id

    @classmethod
    def tearDownClass(cls):
        """
        Function to clean up the data after execution of all the tests
        completed. Execute once at the end of all the tests.
        @param cls: class
        """
        cls.admin_client.delete_tenant(tenant_id=cls.tenant_id)

    def _create_user_for_test(self):
        """
        Create user for testing and delete after testing is complete
        @return add_user response object
        """
        username = rand_name("ccuseradmin")
        email = "{0}@{1}".format(username, "mailtrust.com")
        domain_id = random_int(10000, 1000000000)
        default_region = self.config.identity_api.default_region
        created_user = self.admin_client.add_user(
            default_region=default_region, username=username,
            domain_id=domain_id,
            password=self.password,
            email=email,
            enabled=True)
        self.assertEqual(created_user.status_code, 201,
                         msg="Response for create user admin is not 201.")
        # Delete user after test completion, even if any verification fails
        self.addCleanup(self.delete_user_permanently,
                        user_id=created_user.entity.id,
                        client=self.admin_client)
        return created_user

    def _create_role_for_test(self):
        """
        Create role for testing and delete after testing is complete
        @return add_role response object
        """
        name = rand_name("ccrole")
        description = "Role for testing"
        add_role = self.admin_client.add_role(
            name=name,
            description=description)
        self.assertEqual(add_role.status_code, 201,
                         msg="Response for add role is not 201.")
        # Delete role after test completion, even if any verification fails
        self.addCleanup(self.admin_client.delete_role,
                        role_id=add_role.entity.id)
        return add_role

    def _create_endpoint_template(self):
        """
        Create endpoint template for test and delete after test is complete
        @return endpoint_template response object
        """
        endpoint_template_id = random_int(10000, 1000000000)
        endpoint_template_name = rand_name("testEndpoint")
        endpoint_template = self.admin_client.add_endpoint_template(
            id=endpoint_template_id,
            name=endpoint_template_name,
            type="MOSSO",
            region="ORD",
            enabled=True,
            public_url="https://service-public.com/v1",
            internal_url="https://service-internal.com/v1",
            admin_url="https://service-admin.com/v1")
        self.assertEqual(endpoint_template.status_code, 201,
                         msg="Response for add endpoint template is not 201.")
        self.addCleanup(self.admin_client.delete_endpoint_template,
                        endpoint_template_id=endpoint_template_id)
        return endpoint_template

    def _check_for_duplicate_endpoints(self, service_catalog):
        """
        Check that endpoint should not be duplicate in the service catalog
        for same tenant
        """
        no_of_endpoints = len(service_catalog.endpoints)
        if no_of_endpoints > 1:
            for index1 in range(no_of_endpoints - 1):
                for index2 in range(index1 + 1, no_of_endpoints):
                    self.assertNotEqual(
                        vars(service_catalog.endpoints[index1]),
                        vars(service_catalog.endpoints[index2]),
                        msg="There are duplicate endpoints.")

    @attr('regression', type='positive')
    def test_get_tenants(self):
        """
        Verifies that identity admin can get tenants list
        """
        auth_resp = self.public_client.get_tenants()
        self.assertEqual(auth_resp.status_code, 200,
                         msg="Response to get tenants is not 200.")
        self.assertIsNotNone(auth_resp.entity[0].id,
                             msg="Tenant ID is None for first tenant.")
        self.assertGreaterEqual(len(auth_resp.entity), 1,
                                msg="There is no tenant in the system.")

    @attr('regression', type='positive')
    def test_get_tenant_by_name(self):
        """
        Verifies that identity admin can get tenant by name
        """
        tenant_info = self.admin_client.get_tenant_by_name(
            name=self.tenant_name)
        self.assertEqual(tenant_info.status_code, 200,
                         msg="Response to get tenant by name is not 200.")

    @attr('regression', type='positive')
    def test_service_catalog_for_user_via_tenant(self):
        """
        Verifies that endpoint can be seen in user service catalog only
        once even if same tenant is attached to multiple roles and all roles
        are assigned to user
        """
        endpoint_template = self._create_endpoint_template()
        add_endpoint_to_tenant = self.admin_client.add_endpoint_to_tenant(
            id=endpoint_template.entity.id,
            tenant_id=self.tenant_id)
        self.assertEqual(add_endpoint_to_tenant.status_code, 200,
                         msg="Response for add endpoint to tenant is not 200.")
        user = self._create_user_for_test()
        role1 = self._create_role_for_test()
        role2 = self._create_role_for_test()
        add_role1_to_user_tenant = \
            self.admin_client.add_role_to_user_on_tenant(
                tenant_id=self.tenant_id,
                user_id=user.entity.id,
                role_id=role1.entity.id)
        self.assertEqual(add_role1_to_user_tenant.status_code, 200,
                         msg="Response for Add Role to User for Tenant is not "
                             "200.")
        add_role2_to_user_tenant = \
            self.admin_client.add_role_to_user_on_tenant(
                tenant_id=self.tenant_id,
                user_id=user.entity.id,
                role_id=role2.entity.id)
        self.assertEqual(add_role2_to_user_tenant.status_code, 200,
                         msg="Response for Add Role to User for Tenant is not "
                             "200.")
        user_admin_auth = self.admin_client.authenticate_user_password(
            username=user.entity.username,
            password=self.password)
        self.assertEqual(user_admin_auth.status_code, 200,
                         msg="Response for authenticate user with password is"
                             " not 200.")
        self.assertIsNotNone(user_admin_auth.entity.serviceCatalog,
                             msg="There is no endpoint for user.")
        tenant_found = False
        for service_catalog in user_admin_auth.entity.serviceCatalog:
            self._check_for_duplicate_endpoints(service_catalog)
            for endpoint in service_catalog.endpoints:
                if endpoint.tenantId is not None and \
                        endpoint.tenantId == self.tenant_id:
                    tenant_found = True
        self.assertTrue(tenant_found,
                        msg="Tenant ID '{0}' is not found in endpoints of "
                            "service catalog.".format(self.tenant_id))

    @attr('regression', type='positive')
    def test_service_catalog_for_user_via_multiple_tenant(self):
        """
        Verifies that endpoint can be seen in users service catalog for each
        tenant if there are multiple tenants and tenants have same endpoints
        """
        endpoint_template = self._create_endpoint_template()
        add_endpoint_to_tenant = self.admin_client.add_endpoint_to_tenant(
            id=endpoint_template.entity.id,
            tenant_id=self.tenant_id)
        self.assertEqual(add_endpoint_to_tenant.status_code, 200,
                         msg="Response for add endpoint to tenant is not 200.")
        user = self._create_user_for_test()
        another_tenant = self.created_tenant = self.admin_client.add_tenant(
            name=rand_name("cctenant"),
            description="Tenant for testing",
            enabled=True)
        self.assertEqual(another_tenant.status_code, 201,
                         msg="Response for add tenant is not 201.")
        self.addCleanup(self.admin_client.delete_tenant,
                        tenant_id=another_tenant.entity.id)
        add_endpoint_to_tenant = self.admin_client.add_endpoint_to_tenant(
            id=endpoint_template.entity.id,
            tenant_id=another_tenant.entity.id)
        self.assertEqual(add_endpoint_to_tenant.status_code, 200,
                         msg="Response for add endpoint to tenant is not 200.")
        role1 = self._create_role_for_test()
        role2 = self._create_role_for_test()
        add_role1_to_user_tenant = \
            self.admin_client.add_role_to_user_on_tenant(
                tenant_id=self.tenant_id,
                user_id=user.entity.id,
                role_id=role1.entity.id)
        self.assertEqual(add_role1_to_user_tenant.status_code, 200,
                         msg="Response for Add Role to User for Tenant is not "
                             "200.")
        add_role2_to_user_tenant2 = \
            self.admin_client.add_role_to_user_on_tenant(
                tenant_id=another_tenant.entity.id,
                user_id=user.entity.id,
                role_id=role2.entity.id)
        self.assertEqual(add_role2_to_user_tenant2.status_code, 200,
                         msg="Response for Add Role to User for Tenant is not "
                             "200.")
        user_admin_auth = self.admin_client.authenticate_user_password(
            username=user.entity.username,
            password=self.password)
        self.assertEqual(user_admin_auth.status_code, 200,
                         msg="Response for authenticate user with password is"
                             " not 200.")
        self.assertIsNotNone(user_admin_auth.entity.serviceCatalog,
                             msg="There is no endpoint for user.")
        tenants_to_be_found = [self.tenant_id, another_tenant.entity.id]
        for service_catalog in user_admin_auth.entity.serviceCatalog:
            self._check_for_duplicate_endpoints(service_catalog)
            for endpoint in service_catalog.endpoints:
                if endpoint.tenantId is not None and \
                        endpoint.tenantId in tenants_to_be_found:
                    tenants_to_be_found.remove(endpoint.tenantId)
        self.assertEqual(len(tenants_to_be_found), 0,
                         msg="Tenant IDs {0} is not found in endpoints of "
                             "service catalog.".format(tenants_to_be_found))
