from ccengine.common.dataset_generators import DatasetList
from ccengine.common.decorators import (
    attr, DataDrivenFixture, data_driven_test)
from ccengine.common.tools.datagen import rand_name, random_int
from testrepo.common.testfixtures.identity.v2_0.identity \
    import IdentityAdminFixture


@DataDrivenFixture
class RolesTests(IdentityAdminFixture):
    """
    This class executes all the combinations for add/delete role to/from user.
    Also, add/delete role to/from user on tenants.
    """
    USER_TYPE, ADD_ROLE, DELETE_ROLE = (0, 1, 2)
    IDENTITY_ADMIN, USER_ADMIN, DEFAULT_USER = (
        "IDENTITY_ADMIN", "USER_ADMIN", "DEFAULT_USER")

    USER_ADMIN_DIFF_DOMAIN, DEFAULT_USER_DIFF_DOMAIN, USER_MANAGER = (
        "USER_ADMIN_DIFF_DOMAIN", "DEFAULT_USER_DIFF_DOMAIN", "USER_MANAGER")

    SERVICE_ADMIN_CLIENT, IDENTITY_ADMIN_CLIENT, USER_ADMIN_CLIENT = (
        "SERVICE_ADMIN_CLIENT", "IDENTITY_ADMIN_CLIENT", "USER_ADMIN_CLIENT")

    USER_MANAGER_CLIENT, DEFAULT_USER_CLIENT = (
        "USER_MANAGER_CLIENT", "DEFAULT_USER_CLIENT")
    # Mapped Not Applicable to a negative integer value to make it consistent
    # with status code type
    NA = -1
    # TEST_DATA contains response codes for client, user and weight
    # combination. In the list first element is USER_TYPE, Second value is
    # response for ADD_ROLE and third value is for DELETE_ROLE
    # e.g. [USER_TYPE, ADD_ROLE_RESP, DELETE_ROLE_RESP]
    # Note:
    # Role with weight 900 can not be added to Tenant. All the response will
    # be 403, which is handled in datalist creation.
    TEST_DATA = {
        SERVICE_ADMIN_CLIENT: {
            100: [[IDENTITY_ADMIN, 200, 204],
                  [USER_ADMIN, 200, 204],
                  [DEFAULT_USER, 200, 204],
                  [USER_MANAGER, 200, 204]],
            500: [[IDENTITY_ADMIN, 200, 204],
                  [USER_ADMIN, 200, 204],
                  [DEFAULT_USER, 200, 204],
                  [USER_MANAGER, 200, 204]],
            900: [[IDENTITY_ADMIN, 400, NA],
                  [USER_ADMIN, 400, NA],
                  [DEFAULT_USER, 200, 204],
                  [USER_MANAGER, 200, 204]],
            1000: [[IDENTITY_ADMIN, 200, 204],
                   [USER_ADMIN, 200, 204],
                   [DEFAULT_USER, 200, 204],
                   [USER_MANAGER, 200, 204]],
            2000: [[IDENTITY_ADMIN, 200, 204],
                   [USER_ADMIN, 200, 204],
                   [DEFAULT_USER, 200, 204],
                   [USER_MANAGER, 200, 204]]},
        IDENTITY_ADMIN_CLIENT: {
            100: [[IDENTITY_ADMIN, 403, 403],
                  [USER_ADMIN, 403, 403],
                  [DEFAULT_USER, 403, 403],
                  [USER_MANAGER, 403, 403]],
            500: [[IDENTITY_ADMIN, 403, 403],
                  [USER_ADMIN, 200, 204],
                  [DEFAULT_USER, 200, 204],
                  [USER_MANAGER, 200, 204]],
            900: [[IDENTITY_ADMIN, 403, NA],
                  [USER_ADMIN, 400, NA],
                  [DEFAULT_USER, 200, 204],
                  [USER_MANAGER, 200, 204]],
            1000: [[IDENTITY_ADMIN, 403, 403],
                   [USER_ADMIN, 200, 204],
                   [DEFAULT_USER, 200, 204],
                   [USER_MANAGER, 200, 204]],
            2000: [[IDENTITY_ADMIN, 403, 403],
                   [USER_ADMIN, 200, 204],
                   [DEFAULT_USER, 200, 204],
                   [USER_MANAGER, 200, 204]]},
        USER_ADMIN_CLIENT: {
            100: [[IDENTITY_ADMIN, 403, 403],
                  [USER_ADMIN, 403, 403],
                  [DEFAULT_USER, 403, 403],
                  [USER_ADMIN_DIFF_DOMAIN, 403, 403],
                  [DEFAULT_USER_DIFF_DOMAIN, 403, 403],
                  [USER_MANAGER, 403, 403]],
            500: [[IDENTITY_ADMIN, 403, 403],
                  [USER_ADMIN, 403, 403],
                  [DEFAULT_USER, 403, 403],
                  [USER_ADMIN_DIFF_DOMAIN, 403, 403],
                  [DEFAULT_USER_DIFF_DOMAIN, 403, 403],
                  [USER_MANAGER, 403, 403]],
            900: [[IDENTITY_ADMIN, 403, NA],
                  [USER_ADMIN, 403, NA],
                  [DEFAULT_USER, 200, 204],
                  [USER_ADMIN_DIFF_DOMAIN, 403, NA],
                  [DEFAULT_USER_DIFF_DOMAIN, 403, 403],
                  [USER_MANAGER, 200, 204]],
            1000: [[IDENTITY_ADMIN, 403, 403],
                   [USER_ADMIN, 403, 403],
                   [DEFAULT_USER, 200, 204],
                   [USER_ADMIN_DIFF_DOMAIN, 403, 403],
                   [DEFAULT_USER_DIFF_DOMAIN, 403, 403],
                   [USER_MANAGER, 200, 204]],
            2000: [[IDENTITY_ADMIN, 403, 403],
                   [USER_ADMIN, 403, 403],
                   [DEFAULT_USER, 200, 204],
                   [USER_ADMIN_DIFF_DOMAIN, 403, 403],
                   [DEFAULT_USER_DIFF_DOMAIN, 403, 403],
                   [USER_MANAGER, 200, 204]]},
        USER_MANAGER_CLIENT: {
            100: [[IDENTITY_ADMIN, 403, 403],
                  [USER_ADMIN, 403, 403],
                  [DEFAULT_USER, 403, 403],
                  [USER_MANAGER, 403, 403],
                  [USER_ADMIN_DIFF_DOMAIN, 403, 403],
                  [DEFAULT_USER_DIFF_DOMAIN, 403, 403]],
            500: [[IDENTITY_ADMIN, 403, 403],
                  [USER_ADMIN, 403, 403],
                  [DEFAULT_USER, 403, 403],
                  [USER_ADMIN_DIFF_DOMAIN, 403, 403],
                  [DEFAULT_USER_DIFF_DOMAIN, 403, 403],
                  [USER_MANAGER, 403, 403]],
            900: [[IDENTITY_ADMIN, 403, NA],
                  [USER_ADMIN, 403, NA],
                  [DEFAULT_USER, 403, 403],
                  [USER_ADMIN_DIFF_DOMAIN, 403, NA],
                  [DEFAULT_USER_DIFF_DOMAIN, 403, 403],
                  [USER_MANAGER, 403, 403]],
            1000: [[IDENTITY_ADMIN, 403, 403],
                   [USER_ADMIN, 403, 403],
                   [DEFAULT_USER, 200, 204],
                   [USER_ADMIN_DIFF_DOMAIN, 403, 403],
                   [DEFAULT_USER_DIFF_DOMAIN, 403, 403],
                   [USER_MANAGER, 403, 403]],
            2000: [[IDENTITY_ADMIN, 403, 403],
                   [USER_ADMIN, 403, 403],
                   [DEFAULT_USER, 200, 204],
                   [USER_ADMIN_DIFF_DOMAIN, 403, 403],
                   [DEFAULT_USER_DIFF_DOMAIN, 403, 403],
                   [USER_MANAGER, 403, 403]]},
        DEFAULT_USER_CLIENT: {
            100: [[IDENTITY_ADMIN, 403, 403],
                  [USER_ADMIN, 403, 403],
                  [DEFAULT_USER, 403, 403],
                  [USER_ADMIN_DIFF_DOMAIN, 403, 403],
                  [DEFAULT_USER_DIFF_DOMAIN, 403, 403],
                  [USER_MANAGER, 403, 403]],
            500: [[IDENTITY_ADMIN, 403, 403],
                  [USER_ADMIN, 403, 403],
                  [DEFAULT_USER, 403, 403],
                  [USER_ADMIN_DIFF_DOMAIN, 403, 403],
                  [DEFAULT_USER_DIFF_DOMAIN, 403, 403],
                  [USER_MANAGER, 403, 403]],
            900: [[IDENTITY_ADMIN, 403, NA],
                  [USER_ADMIN, 403, NA],
                  [DEFAULT_USER, 403, 403],
                  [USER_ADMIN_DIFF_DOMAIN, 403, NA],
                  [DEFAULT_USER_DIFF_DOMAIN, 403, 403],
                  [USER_MANAGER, 403, 403]],
            1000: [[IDENTITY_ADMIN, 403, 403],
                   [USER_ADMIN, 403, 403],
                   [DEFAULT_USER, 403, 403],
                   [USER_ADMIN_DIFF_DOMAIN, 403, 403],
                   [DEFAULT_USER_DIFF_DOMAIN, 403, 403],
                   [USER_MANAGER, 403, 403]],
            2000: [[IDENTITY_ADMIN, 403, 403],
                   [USER_ADMIN, 403, 403],
                   [DEFAULT_USER, 403, 403],
                   [USER_ADMIN_DIFF_DOMAIN, 403, 403],
                   [DEFAULT_USER_DIFF_DOMAIN, 403, 403],
                   [USER_MANAGER, 403, 403]]}}

    # Data list for different type of tests
    add_role_test_dataset_list = DatasetList()
    add_role_on_tenant_test_dataset_list = DatasetList()
    delete_role_test_dataset_list = DatasetList()
    delete_role_from_tenant_test_dataset_list = DatasetList()

    # Creating data list for testing
    for client, weight_and_user_dict in TEST_DATA.iteritems():
        for role_weight, user_resp_lists in weight_and_user_dict.iteritems():
            for user_resp_list in user_resp_lists:
                resp_delete_role = user_resp_list[DELETE_ROLE]
                user_type = user_resp_list[USER_TYPE]
                data_for_add_role = {
                    "client": client,
                    "role": role_weight,
                    "user": user_type,
                    "expected_response": user_resp_list[ADD_ROLE]}
                add_role_test_dataset_list.append_new_dataset(
                    "with_weight_{0}_to_{1}_using_{2}".format(
                        role_weight, user_type, client), data_for_add_role)

                data_for_add_role_on_tenant = {
                    "client": client,
                    "role": role_weight,
                    "user": user_type,
                    "expected_response": user_resp_list[ADD_ROLE]}
                # Role with weight 900 is a special role which can not be
                # added to use on tenant
                if role_weight == 900:
                    data_for_add_role_on_tenant["expected_response"] = 403
                add_role_on_tenant_test_dataset_list.append_new_dataset(
                    "with_weight_{0}_to_{1}_using_{2}"
                    .format(role_weight, user_type, client),
                    data_for_add_role_on_tenant)
                # Role with weight 900 can not be added to certain users
                # hence delete role is Not Applicable (NA) for those user
                if resp_delete_role != NA:
                    data_for_delete_role = {
                        "client": client,
                        "role": role_weight,
                        "user": user_type,
                        "expected_response": resp_delete_role}
                    delete_role_test_dataset_list.append_new_dataset(
                        "with_weight_{0}_from_{1}_using_{2}"
                        .format(role_weight, user_type, client),
                        data_for_delete_role)
                    if role_weight != 900:
                        delete_role_from_tenant_test_dataset_list \
                            .append_new_dataset(
                                "with_weight_{0}_from_{1}_using_{2}"
                                .format(role_weight, user_type, client),
                                data_for_delete_role)

    @classmethod
    def setUpClass(cls):
        """
        Function to create test bed for all the test. Execute once at the
        beginning of class
        @param cls: class
        """
        super(RolesTests, cls).setUpClass()
        cls.domain_1_id = random_int(10000, 900000)
        cls.domain_2_id = random_int(10000, 900000)
        password = cls.config.identity_api.password
        cls.user_manage_role_id = cls.config.identity_api.user_manage_role_id
        cls.identity_admin_1 = cls.get_test_user_v2_0(
            client=cls.service_client,
            username=rand_name("ccidentityadmin"),
            password=password)
        cls.identity_admin_2 = cls.get_test_user_v2_0(
            client=cls.service_client,
            username=rand_name("ccidentityadmin"),
            password=password)
        cls.identity_admin_1_client = cls.provider.get_client(
            username=cls.identity_admin_1.entity.username, password=password)

        cls.user_admin_1 = cls.get_test_user_v2_0(
            client=cls.identity_admin_1_client,
            username=rand_name("ccuseradmin"),
            password=password,
            domain_id=cls.domain_1_id)
        cls.user_admin_2 = cls.get_test_user_v2_0(
            client=cls.identity_admin_1_client,
            username=rand_name("ccuseradmin"),
            password=password,
            domain_id=cls.domain_1_id)
        cls.user_admin_1_client = cls.provider.get_client(
            username=cls.user_admin_1.entity.username, password=password)

        cls.default_user_1 = cls.get_test_user_v2_0(
            client=cls.user_admin_1_client,
            username=rand_name("ccdefaultuser"),
            password=password)
        cls.default_user_1_client = cls.provider.get_client(
            username=cls.default_user_1.entity.username, password=password)
        cls.default_user_2 = cls.get_test_user_v2_0(
            client=cls.user_admin_1_client,
            username=rand_name("ccdefaultuser"),
            password=password)

        cls.user_manager_1 = cls.get_test_user_v2_0(
            client=cls.user_admin_1_client,
            username=rand_name("ccdefaultuser"),
            password=password)
        add_role = cls.service_client.add_role_to_user(
            user_id=cls.user_manager_1.entity.id,
            role_id=cls.user_manage_role_id)
        assert add_role.status_code == 200, \
            "Response for add user manage role to default user is not 200."
        cls.user_manager_1_client = cls.provider.get_client(
            username=cls.user_manager_1.entity.username, password=password)

        cls.add_role_user_manager2 = True
        cls.user_manager_2 = cls.get_test_user_v2_0(
            client=cls.user_admin_1_client,
            username=rand_name("ccdefaultuser"),
            password=password)

        cls.user_admin_domain_2 = cls.get_test_user_v2_0(
            client=cls.identity_admin_1_client,
            username=rand_name("ccuseradmin"),
            password=password,
            domain_id=cls.domain_2_id)
        cls.user_admin_domain_2_client = cls.provider.get_client(
            username=cls.user_admin_domain_2.entity.username,
            password=password)

        cls.default_user_domain_2 = cls.get_test_user_v2_0(
            client=cls.user_admin_domain_2_client,
            username=rand_name("ccdefaultuser"),
            password=password)

        cls.tenant = cls.admin_client.add_tenant(
            name=rand_name("cctenant"),
            description="Tenant for testing")

        cls.role_list = {
            900: cls.user_manage_role_id,
            100: cls.config.default_role_id.role_with_weight_100_id,
            500: cls.config.default_role_id.role_with_weight_500_id,
            1000: cls.config.default_role_id.role_with_weight_1000_id,
            2000: cls.config.default_role_id.role_with_weight_2000_id}

        # Adding role to user on Tenant
        cls.service_client.add_role_to_user_on_tenant(
            tenant_id=cls.tenant.entity.id,
            user_id=cls.user_admin_1.entity.id,
            role_id=cls.role_list[1000])
        cls.service_client.add_role_to_user_on_tenant(
            tenant_id=cls.tenant.entity.id,
            user_id=cls.user_manager_1.entity.id,
            role_id=cls.role_list[1000])
        cls.service_client.add_role_to_user_on_tenant(
            tenant_id=cls.tenant.entity.id,
            user_id=cls.default_user_1.entity.id,
            role_id=cls.role_list[2000])

        cls.user_list = {
            cls.IDENTITY_ADMIN: cls.identity_admin_2,
            cls.USER_ADMIN: cls.user_admin_2,
            cls.DEFAULT_USER: cls.default_user_2,
            cls.USER_ADMIN_DIFF_DOMAIN: cls.user_admin_domain_2,
            cls.DEFAULT_USER_DIFF_DOMAIN: cls.default_user_domain_2,
            cls.USER_MANAGER: cls.user_manager_2}

        cls.client_list = {
            cls.SERVICE_ADMIN_CLIENT: cls.service_client,
            cls.IDENTITY_ADMIN_CLIENT: cls.identity_admin_1_client,
            cls.USER_ADMIN_CLIENT: cls.user_admin_1_client,
            cls.USER_MANAGER_CLIENT: cls.user_manager_1_client,
            cls.DEFAULT_USER_CLIENT: cls.default_user_1_client}

    @classmethod
    def tearDownClass(cls):
        """
        Function to clean up the data after execution of all the tests
        completed. Execute once at the end of all the tests.
        @param cls: class
        """
        cls.delete_user_permanently(
            user_id=cls.default_user_1.entity.id,
            client=cls.user_admin_1_client)
        cls.delete_user_permanently(
            user_id=cls.default_user_2.entity.id,
            client=cls.user_admin_1_client)
        cls.delete_user_permanently(
            user_id=cls.default_user_domain_2.entity.id,
            client=cls.user_admin_domain_2_client)

        cls.delete_user_permanently(
            user_id=cls.user_manager_1.entity.id,
            client=cls.user_admin_1_client)
        cls.delete_user_permanently(
            user_id=cls.user_manager_2.entity.id,
            client=cls.user_admin_1_client)

        cls.delete_user_permanently(
            user_id=cls.user_admin_1.entity.id,
            client=cls.identity_admin_1_client)
        cls.delete_user_permanently(
            user_id=cls.user_admin_2.entity.id,
            client=cls.identity_admin_1_client)
        cls.delete_user_permanently(
            user_id=cls.user_admin_domain_2.entity.id,
            client=cls.identity_admin_1_client)

        cls.delete_user_permanently(
            user_id=cls.identity_admin_1.entity.id,
            client=cls.service_client)
        cls.delete_user_permanently(
            user_id=cls.identity_admin_2.entity.id,
            client=cls.service_client)

        cls.service_client.delete_tenant(tenant_id=cls.tenant.entity.id)
        cls.service_client.delete_domain(domain_id=cls.domain_1_id)
        cls.service_client.delete_domain(domain_id=cls.domain_2_id)

    def setUp(self):
        """
        Function to create test bed for all the test. Execute at the
        beginning of every test
        @param self: instance of class
        """
        if self.add_role_user_manager2:
            add_role = self.service_client.add_role_to_user(
                user_id=self.user_manager_2.entity.id,
                role_id=self.user_manage_role_id)
            assert add_role.status_code == 200, \
                "Response for add user manage role to default user is not 200."
            self.add_role_user_manager2 = False

    @data_driven_test(add_role_test_dataset_list)
    @attr('regression', type='positive')
    def ddtest_add_role(self, client, role, user, expected_response):
        """
        Verifies that user can/cannot add roles to other users
        """
        add_role = self.client_list[client].add_role_to_user(
            user_id=self.user_list[user].entity.id,
            role_id=self.role_list[role])
        if add_role.status_code == 200:
            if user.upper() == self.USER_MANAGER and role == 900:
                self.add_role_user_manager2 = True
            self.addCleanup(self.service_client.delete_role_from_user,
                            user_id=self.user_list[user].entity.id,
                            role_id=self.role_list[role])
        self.assertEqual(
            add_role.status_code, expected_response,
            msg="Response for add role to user is not {0}.".format(
                expected_response))
    
    @data_driven_test(delete_role_test_dataset_list)
    @attr('regression', type='positive')
    def ddtest_delete_role(self, client, role, user, expected_response):
        """
        Verifies that user can/cannot delete roles from other users
        """
        add_role = self.service_client.add_role_to_user(
            user_id=self.user_list[user].entity.id,
            role_id=self.role_list[role])
        self.assertEqual(add_role.status_code, 200,
                         msg="Response for add role to user using service "
                             "admin is not 200.")
        delete_role = self.client_list[client].delete_role_from_user(
            user_id=self.user_list[user].entity.id,
            role_id=self.role_list[role])
        if user.upper() == self.USER_MANAGER and role == 900:
            self.add_role_user_manager2 = True
        if delete_role.status_code != 204:
            self.addCleanup(self.service_client.delete_role_from_user,
                            user_id=self.user_list[user].entity.id,
                            role_id=self.role_list[role])
        self.assertEqual(delete_role.status_code, expected_response,
                         msg="Response for delete role from user is not {0}."
                         .format(expected_response))

    @data_driven_test(add_role_on_tenant_test_dataset_list)
    @attr('regression', type='positive')
    def ddtest_add_role_to_user_on_tenant(
            self, client, role, user, expected_response):
        """
        Verifies that user can/cannot add roles to other users on tenant
        """
        add_role = self.client_list[client].add_role_to_user_on_tenant(
            tenant_id=self.tenant.entity.id,
            user_id=self.user_list[user].entity.id,
            role_id=self.role_list[role])
        if add_role.status_code == 200:
            self.addCleanup(
                self.service_client.delete_role_to_user_on_tenant,
                tenant_id=self.tenant.entity.id,
                user_id=self.user_list[user].entity.id,
                role_id=self.role_list[role])
        self.assertEqual(
            add_role.status_code, expected_response,
            msg="Response for add role to user on tenant is not {0}.".format(
                expected_response))

    @data_driven_test(delete_role_from_tenant_test_dataset_list)
    @attr('regression', type='positive')
    def ddtest_delete_role_from_user_on_tenant(
            self, client, role, user, expected_response):
        """
        Verifies that user can/cannot delete roles from other users on tenant
        """
        add_role = self.service_client.add_role_to_user_on_tenant(
            tenant_id=self.tenant.entity.id,
            user_id=self.user_list[user].entity.id,
            role_id=self.role_list[role])
        self.assertEqual(
            add_role.status_code, 200,
            msg="Response for add role to user on tenant using service admin "
                "is not 200.")
        delete_role = self.client_list[client].delete_role_to_user_on_tenant(
            tenant_id=self.tenant.entity.id,
            user_id=self.user_list[user].entity.id,
            role_id=self.role_list[role])
        if delete_role.status_code != 204:
            self.addCleanup(
                self.service_client.delete_role_to_user_on_tenant,
                tenant_id=self.tenant.entity.id,
                user_id=self.user_list[user].entity.id,
                role_id=self.role_list[role])
        self.assertEqual(delete_role.status_code, expected_response,
                         msg="Response for delete role from user on tenanat "
                             "is not {0}.".format(expected_response))
