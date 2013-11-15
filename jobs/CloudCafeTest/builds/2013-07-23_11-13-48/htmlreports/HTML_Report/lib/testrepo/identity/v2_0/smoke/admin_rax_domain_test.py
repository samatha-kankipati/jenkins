from testrepo.common.testfixtures.identity.v2_0.identity \
        import IdentityAdminFixture
from ccengine.common.decorators import attr
from ccengine.common.tools.datagen import rand_name
from ccengine.common.tools.datagen import random_int


class AdminDomainTest(IdentityAdminFixture):

    @classmethod
    def setUpClass(cls):
        super(AdminDomainTest, cls).setUpClass()
        cls.dom_name = rand_name("ccdomname")
        cls.dom_id = random_int(1, 10000)
        cls.enabled = True
        cls.descr = 'static_descr'
        cls.upd_dom_name = rand_name("ccupdname")

    @classmethod
    def tearDownClass(cls):
        pass

    def tearDown(self):
        self.addCleanup(self.admin_client.delete_domain,
                domainId=self.dom_id)

    @attr('smoke', type='positive')
    def test_get_domains(self):
        get_domains = self.admin_client.get_domains()

        self.assertEqual(get_domains.status_code, 200,
                msg="Admin get domains expected response 200 received %s" %
                get_domains.status_code)

    @attr('smoke', type='positive')
    def test_create_domain(self):
        create_domain = self.admin_client.create_domain(name=self.dom_name,
                                                        id=self.dom_id,
                                                        enabled=self.enabled,
                                                        description=self.descr)

        self.assertEqual(create_domain.status_code, 201,
                msg="Admin create domain expected response 201 received %s" %
                create_domain.status_code)

        self.addCleanup(self.admin_client.delete_domain,
                        domainId=self.dom_id)

    @attr('smoke', type='positive')
    def test_get_domain(self):
        create_domain = self.admin_client.create_domain(name=self.dom_name,
                                                        id=self.dom_id,
                                                        enabled=self.enabled,
                                                        description=self.descr)

        self.assertEqual(create_domain.status_code, 201,
                msg="Admin create domain expected response 201 received %s" %
                create_domain.status_code)

        get_domain = self.admin_client.get_domain(
                domainId=create_domain.entity.id)

        self.assertEqual(get_domain.status_code, 200,
                msg="Admin get domain expected response 200 received %s" %
                get_domain.status_code)

        self.addCleanup(self.admin_client.delete_domain,
                        domainId=self.dom_id)

    @attr('smoke', type='positive')
    def test_update_domain(self):
        create_domain = self.admin_client.create_domain(name=self.dom_name,
                                                        id=self.dom_id,
                                                        enabled=self.enabled,
                                                        description=self.descr)

        self.assertEqual(create_domain.status_code, 201,
                msg="Admin create domain expected response 201 received %s" %
                create_domain.status_code)

        update_domain = self.admin_client.update_domain(
                name=self.upd_dom_name,
                id=self.dom_id,
                enabled=self.enabled,
                description=self.descr,
                domainId=create_domain.entity.id)

        self.assertEqual(update_domain.status_code, 200,
                msg="Admin update domain expected response 200 received %s" %
                update_domain.status_code)

        self.addCleanup(self.admin_client.delete_domain,
                        domainId=self.dom_id)

    @attr('smoke', type='positive')
    def test_delete_domain(self):
        create_domain = self.admin_client.create_domain(name=self.dom_name,
                                                        id=self.dom_id,
                                                        enabled=self.enabled,
                                                        description=self.descr)

        self.assertEqual(create_domain.status_code, 201,
                msg="Admin create domain expected response 201 received %s" %
                create_domain.status_code)

        delete_domain = self.admin_client.delete_domain(
                domainId=create_domain.entity.id)

        self.assertEqual(delete_domain.status_code, 204,
                msg="Admin delete domain expected response 204 received %s" %
                delete_domain.status_code)

        get_domain = self.admin_client.get_domain(
                domainId=create_domain.entity.id)

        self.assertEqual(get_domain.status_code, 404,
                msg="Admin delete non-existant domain expected response 404"
                " received %s" % get_domain.status_code)

    @attr('smoke', type='positive')
    def test_get_endpoints_for_domain(self):
        create_domain = self.admin_client.create_domain(name=self.dom_name,
                                                        id=self.dom_id,
                                                        enabled=self.enabled,
                                                        description=self.descr)

        self.assertEqual(create_domain.status_code, 201,
                msg="Admin create domain expected response 201 received %s" %
                create_domain.status_code)

        get_endpoints = self.admin_client.get_endpoints_for_domain(
                domainId=create_domain.entity.id)

        self.assertEqual(get_endpoints.status_code, 200,
                msg="Admin get endpoints expected response 200 received %s" %
                get_endpoints.status_code)

        self.addCleanup(self.admin_client.delete_domain,
                        domainId=self.dom_id)

    @attr('smoke', type='positive')
    def test_get_users_in_domain(self):
        create_domain = self.admin_client.create_domain(name=self.dom_name,
                                                        id=self.dom_id,
                                                        enabled=self.enabled,
                                                        description=self.descr)

        self.assertEqual(create_domain.status_code, 201,
                msg="Admin create domain expected response 201 received %s" %
                create_domain.status_code)

        get_user_dom = self.admin_client.get_users_in_domain(
                domainId=create_domain.entity.id)

        self.assertEqual(get_user_dom.status_code, 200,
                msg="expected response 200 received %s" %
                get_user_dom.status_code)

        self.addCleanup(self.admin_client.delete_domain,
                        domainId=self.dom_id)

    @attr('smoke', type='positive')
    def test_add_user_to_domain(self):
        username = rand_name("ccadminname")
        email = '{0}@{1}'.format(username, "supra.com")
        defaultRegion = "DFW"

        create_domain = self.admin_client.create_domain(name=self.dom_name,
                                                        id=self.dom_id,
                                                        enabled=self.enabled,
                                                        description=self.descr)

        self.assertEqual(create_domain.status_code, 201,
                msg="Admin create domain expected response 201 received %s" %
                create_domain.status_code)

        create_user = self.admin_client.add_user(
                username=username,
                email=email,
                enabled=True,
                defaultRegion=defaultRegion,
                domainId=create_domain.entity.id,
                password="Gadmpass8")

        self.assertEqual(create_user.status_code, 201,
                msg="Admin add user with passwd expected response 201"
                " received %s" % create_user.status_code)

        add_user_dom = self.admin_client.add_user_to_domain(
                userId=create_user.entity.id,
                domainId=create_domain.entity.id)

        self.assertEqual(add_user_dom.status_code, 204,
                msg="Admin add user to domain expected response 204"
                " received %s" % add_user_dom.status_code)

        self.addCleanup(self.admin_client.delete_domain,
                        domainId=self.dom_id)
        self.addCleanup(self.service_client.delete_user_hard,
                        userId=create_user.entity.id)
        self.addCleanup(self.public_client.delete_user,
                        userId=create_user.entity.id)

    @attr('smoke', type='positive')
    def test_get_tenants_in_domain(self):
        create_domain = self.admin_client.create_domain(name=self.dom_name,
                                                        id=self.dom_id,
                                                        enabled=self.enabled,
                                                        description=self.descr)

        self.assertEqual(create_domain.status_code, 201,
                msg="Admin create domain expected response 201 received %s" %
                create_domain.status_code)

        add_ten_dom = self.admin_client.add_tenant_to_domain(
                domainId=create_domain.entity.id,
                tenantId=self.config.identity_api.tenant_id)

        self.assertEqual(add_ten_dom.status_code, 204,
                msg="Admin add tenant to domain expected response 204"
                "received %s" % add_ten_dom.status_code)

        get_ten_dom = self.admin_client.get_tenants_in_domain(
                domainId=create_domain.entity.id)

        self.assertEqual(get_ten_dom.status_code, 200,
                msg="Admin get tenants in domain expected response 200"
                "received %s" % add_ten_dom.status_code)

        self.addCleanup(self.admin_client.delete_domain,
                        domainId=self.dom_id)

    @attr('smoke', type='positive')
    def test_add_tenant_to_domain(self):
        create_domain = self.admin_client.create_domain(name=self.dom_name,
                                                        id=self.dom_id,
                                                        enabled=self.enabled,
                                                        description=self.descr)

        self.assertEqual(create_domain.status_code, 201,
                msg="Admin create domain expected response 201 received %s" %
                create_domain.status_code)

        add_ten_dom = self.admin_client.add_tenant_to_domain(
                domainId=create_domain.entity.id,
                tenantId=self.config.identity_api.tenant_id)

        self.assertEqual(add_ten_dom.status_code, 204,
                msg="Admin add tenant to domain expected response 204"
                " received %s" % add_ten_dom.status_code)

        self.addCleanup(self.admin_client.delete_domain,
                        domainId=self.dom_id)
