from ccengine.common.decorators import attr
from ccengine.common.tools.datagen import random_int, rand_name
from ccengine.providers.identity.v2_0.identity_api \
    import IdentityClientTypes
from testrepo.common.testfixtures.identity.v2_0.identity \
    import BaseIdentityFixture


class ListUsersTenant(BaseIdentityFixture):
    """
    @summary: Test to verify that all users are listed for a tenant
    """
    @classmethod
    def setUpClass(cls):
        """
        Function to create test bed for all the tests. Execute once at the
        beginning of class
        @param cls: instance of class

        """
        super(ListUsersTenant, cls).setUpClass()
        cls.password = "CCPassword1"
        cls.cloudfiles_role_id = cls.config.identity_api.cloudfiles_role_id
        cls.iden_admin_name = cls.config.identity_api.admin_username
        cls.iden_admin_password = cls.config.identity_api.admin_password

        iden_admin_client = cls.set_client(
            username=cls.iden_admin_name, password=cls.iden_admin_password,
            user_type=IdentityClientTypes.ADMIN)
        cls.admin_client.token = iden_admin_client.token

    @attr('regression', type='positive')
    def test_list_users_tenant_propagate(self):
        """
        @summary: Verify list users for specified tenant returns user admin
         and sub user for the tenant
        """
        self.user_admin_name_v1_1 = rand_name("ccuseradmin11")
        self.sub_user_name = rand_name("ccsubuser")
        self.key = 'asdasdasd-adsasdads-asdasdasd-adsadsasd'
        self.mosso_id = random_int(1000000, 9000000)

        self.create_usr_adm_resp_v1_1 = self.get_test_user_v1_1(
            client=self.admin_client, user_id=self.user_admin_name_v1_1,
            api_key=self.key, mosso_id=self.mosso_id, enabled=True)
        self.get_user_id = self.admin_client.get_user_by_name(
            name=self.user_admin_name_v1_1)
        self.addCleanup(self.delete_user_permanently,
                        user_id=self.get_user_id.entity.id,
                        client=self.service_client)
        self.list_credentials = self.service_client.list_credentials(
            self.get_user_id.entity.id)
        self.password_11 = (self.list_credentials.entity.passwordCredentials
            .password)
        assert (self.create_usr_adm_resp_v1_1.status_code in [201])
        usernames = [self.user_admin_name_v1_1]
        self._test_list_user_tenant(
            self.service_client, self.mosso_id, 1, usernames)
        self._test_list_user_tenant(
            self.admin_client, self.mosso_id, 1, usernames)

        user_admin_client = self.set_client(
            username=self.user_admin_name_v1_1, password=self.password_11,
            user_type=IdentityClientTypes.DEFAULT)
        self.public_client.token = user_admin_client.token
        self.create_sub_usr_resp = self.get_test_user_v2_0(
            client=self.public_client, username=self.sub_user_name,
            password=self.password, domain_id=None, enabled=True)
        self.addCleanup(self.delete_user_permanently,
                        user_id=self.create_sub_usr_resp.entity.id,
                        client=self.service_client)
        assert (self.create_sub_usr_resp.status_code in [201])

        usernames = [self.user_admin_name_v1_1, self.sub_user_name]
        self._test_list_user_tenant(
            self.service_client, self.mosso_id, 2, usernames)
        self._test_list_user_tenant(
            self.admin_client, self.mosso_id, 2, usernames)

    @attr('regression', type='positive')
    def test_list_users_tenant_non_propagate(self):
        """
        @summary: Verify list users for specified tenant returns user admin
        and after the role is added to user admin it returns user admin and
        sub user
        """
        user_admin_name_v2_0 = rand_name("ccuseradmin")
        sub_user1_name = rand_name("ccsubuser")
        domain_id = random_int(1000000, 9000000)
        tenant_name = random_int(10000, 1000000000)
        create_tenant_resp = self.get_test_tenant(
            client=self.admin_client, name=tenant_name, enabled=True)
        create_usr_adm_resp = self.get_test_user_v2_0(
            client=self.admin_client, username=user_admin_name_v2_0,
            password=self.password, domain_id=domain_id, enabled=True)
        self.addCleanup(self.delete_user_permanently,
                        user_id=create_usr_adm_resp.entity.id,
                        client=self.service_client)
        usernames = []
        self._test_list_user_tenant(
            self.service_client, create_tenant_resp.entity.id, 0, usernames)
        self._test_list_user_tenant(
            self.admin_client, create_tenant_resp.entity.id, 0, usernames)
        self._test_add_role_user_tenant(create_tenant_resp.entity.id,
                                        create_usr_adm_resp.entity.id,
                                        self.cloudfiles_role_id)

        usernames = [user_admin_name_v2_0]
        self._test_list_user_tenant(
            self.service_client, create_tenant_resp.entity.id, 1, usernames)
        self._test_list_user_tenant(
            self.admin_client, create_tenant_resp.entity.id, 1, usernames)

        user_admin_client = self.set_client(
            username=user_admin_name_v2_0, password=self.password,
            user_type=IdentityClientTypes.DEFAULT)
        self.public_client.token = user_admin_client.token
        create_sub_sec_usr_resp = self.get_test_user_v2_0(
            client=self.public_client, username=sub_user1_name,
            password=self.password, domain_id=None, enabled=True)
        self.addCleanup(self.delete_user_permanently,
                        user_id=create_sub_sec_usr_resp.entity.id,
                        client=self.service_client)

        usernames = [user_admin_name_v2_0, sub_user1_name]
        self._test_list_user_tenant(
            self.service_client, create_tenant_resp.entity.id, 2, usernames)
        self._test_list_user_tenant(
            self.admin_client, create_tenant_resp.entity.id, 2, usernames)
        self.admin_client.delete_tenant(create_tenant_resp.entity.id)
        self.admin_client.delete_domain(domain_id=domain_id)

    @attr('regression', type='positive')
    def test_list_users_tenant_after_subusers_created(self):
        """
        @summary: User admin creates two sub users and after adding the tenant
        role to the sub users the list user for tenant returns all the users
        for that tenant
        """
        user_admin_name_v2_0 = rand_name("ccuseradmin")
        sub_user1_name = rand_name("ccsubuser")
        sub_user2_name = rand_name("ccsubuser")
        domain_id = random_int(1000000, 9000000)
        tenant_name = random_int(10000, 1000000000)
        create_tenant_resp = self.get_test_tenant(
            client=self.admin_client, name=tenant_name, enabled=True)
        self.addCleanup(self.delete_tenant,
                        tenant_id=create_tenant_resp.entity.id,
                        client=self.admin_client)
        create_usr_adm_resp = self.get_test_user_v2_0(
            client=self.admin_client, username=user_admin_name_v2_0,
            password=self.password, domain_id=domain_id, enabled=True)
        self.addCleanup(self.delete_domain,
                        domain_id=domain_id,
                        client=self.admin_client)
        self.addCleanup(self.delete_user_permanently,
                        user_id=create_usr_adm_resp.entity.id,
                        client=self.service_client)

        user_admin_client = self.set_client(
            username=user_admin_name_v2_0, password=self.password,
            user_type=IdentityClientTypes.DEFAULT)
        self.public_client.token = user_admin_client.token
        create_sub_usr1_resp = self.get_test_user_v2_0(
            client=self.public_client, username=sub_user1_name,
            password=self.password, domain_id=None, enabled=True)
        self.addCleanup(self.delete_user_permanently,
                        user_id=create_sub_usr1_resp.entity.id,
                        client=self.service_client)
        create_sub_usr2_resp = self.get_test_user_v2_0(
            client=self.public_client, username=sub_user2_name,
            password=self.password, domain_id=None, enabled=True)
        self.addCleanup(self.delete_user_permanently,
                        user_id=create_sub_usr2_resp.entity.id,
                        client=self.service_client)

        self._test_add_role_user_tenant(create_tenant_resp.entity.id,
                                        create_sub_usr1_resp.entity.id,
                                        self.cloudfiles_role_id)

        usernames = [sub_user1_name]
        self._test_list_user_tenant(
            self.service_client, create_tenant_resp.entity.id, 1, usernames)
        self._test_list_user_tenant(
            self.admin_client, create_tenant_resp.entity.id, 1, usernames)

        self._test_add_role_user_tenant(create_tenant_resp.entity.id,
                                        create_sub_usr2_resp.entity.id,
                                        self.cloudfiles_role_id)

        usernames = [sub_user1_name, sub_user2_name]
        self._test_list_user_tenant(
            self.service_client, create_tenant_resp.entity.id, 2, usernames)
        self._test_list_user_tenant(
            self.admin_client, create_tenant_resp.entity.id, 2, usernames)

    def _test_list_user_tenant(self, client, tenant_id, expected_users_count,
                               usernames):
        """
        @summary:Test to verify the users returned for the specified tenant
        """
        resp = client.list_users_for_tenant(tenant_id)
        self.assertEqual(resp.status_code, 200,
                         msg="Response status code is not 200")
        self.assertEqual(len(resp.entity), expected_users_count,
                         msg="More then one user is returned")
        for user in resp.entity:
            if user.username not in usernames:
                fail_msg = ('username {0} not in expected list: {1}'
                            .format(user.username, usernames))
                self.fail(fail_msg)

    def _test_add_role_user_tenant(self, tenant_id, user_id, role_id):
        """
        @summary:Test to verify the user is added with the specified tenant
        role
        """
        normal_response_codes = [200]
        add_role_user_tenant = self.admin_client.add_role_to_user_on_tenant(
            tenant_id, user_id, role_id)
        self.assertIn(add_role_user_tenant.status_code,
                      normal_response_codes,
                      msg="Response for Add role to user on tenant is not as "
                          "expected.")
