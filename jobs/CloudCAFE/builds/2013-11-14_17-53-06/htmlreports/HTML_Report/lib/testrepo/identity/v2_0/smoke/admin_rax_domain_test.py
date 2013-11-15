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
        cls.dom_id = random_int(10000, 90000)
        cls.enabled = True
        cls.descr = 'static_descr'
        cls.upd_dom_name = rand_name("ccupdname")
        cls.create_domain = cls.admin_client.create_domain(
            name=cls.dom_name,
            id=cls.dom_id,
            enabled=cls.enabled,
            description=cls.descr)

    @classmethod
    def tearDownClass(cls):
        cls.admin_client.delete_domain(domain_id=cls.dom_id)

    @attr('smoke', type='positive')
    def test_get_domains(self):
        """
        Test to verify get domains call

        """
        get_domains = self.admin_client.get_domains()
        self.assertEqual(
            get_domains.status_code, 200,
            msg=("Admin get domains expected response 200 received {0}"
                 .format(get_domains.status_code)))

    @attr('smoke', type='positive')
    def test_create_domain(self):
        """
        Test to verify create domain call

        """
        self.assertEqual(
            self.create_domain.status_code, 201,
            msg=("Admin create domain expected response 201 received {0}"
                 .format(self.create_domain.status_code)))

    @attr('smoke', type='positive')
    def test_get_domain(self):
        """
        Test to verify get domain call

        """
        self.assertEqual(
            self.create_domain.status_code, 201,
            msg=("Admin create domain expected response 201 received {0}"
                 .format(self.create_domain.status_code)))

        get_domain = self.admin_client.get_domain(
            domain_id=self.create_domain.entity.id)
        self.assertEqual(
            get_domain.status_code, 200,
            msg=("Admin get domain expected response 200 received {0}"
                 .format(get_domain.status_code)))

    @attr('smoke', type='positive')
    def test_update_domain(self):
        """
        Test to verify update domain call

        """
        self.assertEqual(
            self.create_domain.status_code, 201,
            msg=("Admin create domain expected response 201 received {0}"
                 .format(self.create_domain.status_code)))

        update_domain = self.admin_client.update_domain(
            name=self.upd_dom_name,
            id=self.dom_id,
            enabled=self.enabled,
            description=self.descr,
            domain_id=self.create_domain.entity.id)
        self.assertEqual(
            update_domain.status_code, 200,
            msg=("Admin update domain expected response 200 received {0}"
                 .format(update_domain.status_code)))

    @attr('smoke', type='positive')
    def test_delete_domain(self):
        """
        Test to verify delete domain call

        """
        dom_name = rand_name("ccdomname")
        dom_id = random_int(10000, 90000)
        enabled = True
        descr = 'static_descr'
        create_domain = self.admin_client.create_domain(
            name=dom_name,
            id=dom_id,
            enabled=enabled,
            description=descr)
        self.assertEqual(
            create_domain.status_code, 201,
            msg=("Admin create domain expected response 201 received {0}"
                 .format(create_domain.status_code)))

        delete_domain = self.admin_client.delete_domain(
            domain_id=create_domain.entity.id)
        self.assertEqual(
            delete_domain.status_code, 204,
            msg=("Admin delete domain expected response 204 received {0}"
                 .format(delete_domain.status_code)))

        get_domain = self.admin_client.get_domain(
            domain_id=create_domain.entity.id)
        self.assertEqual(
            get_domain.status_code, 404,
            msg=("Admin delete non-existant domain expected response 404"
                 " received {0}".format(get_domain.status_code)))

    @attr('smoke', type='positive')
    def test_get_endpoints_for_domain(self):
        """
        Test to verify get endpoints for domain call

        """
        self.assertEqual(
            self.create_domain.status_code, 201,
            msg=("Admin create domain expected response 201 received {0}"
                 .format(self.create_domain.status_code)))

        get_endpoints = self.admin_client.get_endpoints_for_domain(
            domain_id=self.create_domain.entity.id)
        self.assertEqual(
            get_endpoints.status_code, 200,
            msg=("Admin get endpoints expected response 200 received {0}"
                 .format(get_endpoints.status_code)))

    @attr('smoke', type='positive')
    def test_get_users_in_domain(self):
        """
        Test to verify get users in domain call

        """
        self.assertEqual(
            self.create_domain.status_code, 201,
            msg=("Admin create domain expected response 201 received {0}"
                 .format(self.create_domain.status_code)))

        get_user_dom = self.admin_client.get_users_in_domain(
            domain_id=self.create_domain.entity.id)
        self.assertEqual(
            get_user_dom.status_code, 200,
            msg=("Expected response 200 received {0}"
                 .format(get_user_dom.status_code)))

    @attr('smoke', type='positive')
    def test_add_user_to_domain(self):
        """
        Test to verify add user to domain call

        """
        username = rand_name("ccadminname")
        email = self.config.identity_api.default_email
        default_region = self.config.identity_api.default_region

        self.assertEqual(
            self.create_domain.status_code, 201,
            msg=("Admin create domain expected response 201 received {0}"
                 .format(self.create_domain.status_code)))

        create_user = self.admin_client.add_user(
            username=username,
            email=email,
            enabled=True,
            default_region=default_region,
            domain_id=self.create_domain.entity.id,
            password="Gadmpass8")
        self.assertEqual(
            create_user.status_code, 201,
            msg=("Admin add user with passwd expected response 201"
                 " received {0}".format(create_user.status_code)))
        self.assertIsNotNone(
            create_user.entity.id,
            msg='Create user returned id as None')
        # Delete user after test completion
        self.addCleanup(
            self.delete_user_permanently,
            user_id=create_user.entity.id,
            client=self.admin_client)

        add_user_dom = self.admin_client.add_user_to_domain(
            user_id=create_user.entity.id,
            domain_id=self.create_domain.entity.id)
        self.assertEqual(
            add_user_dom.status_code, 204,
            msg=("Admin add user to domain expected response 204"
                 " received {0}".format(add_user_dom.status_code)))

    @attr('smoke', type='positive')
    def test_get_tenants_in_domain(self):
        """
        Test to verify get tenants in domain call

        """
        add_ten_dom = self._add_tenant_to_domain()
        get_ten_dom = self.admin_client.get_tenants_in_domain(
            domain_id=self.create_domain.entity.id)
        self.assertEqual(
            get_ten_dom.status_code, 200,
            msg=("Admin get tenants in domain expected response 200"
                 "received {0}".format(add_ten_dom.status_code)))

    @attr('smoke', type='positive')
    def test_add_tenant_to_domain(self):
        """
        Test to verify add tenant to domain call

        """
        self._add_tenant_to_domain()

    def _add_tenant_to_domain(self):
        """
        method to add tenant to domain

        """
        self.assertEqual(
            self.create_domain.status_code, 201,
            msg=("Admin create domain expected response 201 received {0}"
                 .format(self.create_domain.status_code)))

        add_ten_dom = self.admin_client.add_tenant_to_domain(
            domain_id=self.create_domain.entity.id,
            tenant_id=self.config.identity_api.tenant_id)
        self.assertEqual(
            add_ten_dom.status_code, 204,
            msg=("Admin add tenant to domain expected response 204"
                 " received {0}".format(add_ten_dom.status_code)))
        return add_ten_dom
