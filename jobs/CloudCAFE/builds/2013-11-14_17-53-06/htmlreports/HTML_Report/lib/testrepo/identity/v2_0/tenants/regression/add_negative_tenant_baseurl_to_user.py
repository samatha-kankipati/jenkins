from ccengine.common.dataset_generators import DatasetList
from ccengine.common.decorators import (
    attr, DataDrivenFixture, data_driven_test)
from ccengine.common.tools.datagen import random_int, rand_name
from ccengine.providers.atomhopper import AtomHopperProvider
from ccengine.providers.identity.v2_0.identity_api \
    import IdentityClientTypes, IdentityAPIProvider
from testrepo.common.testfixtures.identity.v2_0.identity \
    import BaseIdentityFixture


@DataDrivenFixture
class TenantBaseUrlAuthTest(BaseIdentityFixture):
    """
    @summary: Functional tests to allow negative tenant id

    Test data set list for the test cases.  Based on these data set list
    test cases get replicated.

    Test data generated below is of type string, but it represents the type
    of data set combination that will be tested.
    Test data is a set of client type, user type and the status of the user
    i.e. enabled or disabled.  Exact test data will assigned inside the
    setUpClass where we get the clients and creates users.

    """
    expected_resp_normal = [200]
    client_types = ["SERVICE_CLIENT", "ADMIN_CLIENT", "PUBLIC_CLIENT",
                    "DEFAULT_CLIENT"]
    user_types = ["IDENTITY_USER", "USER_ADMIN_USER", "SUB_USER"]
    statuses = ["ENABLED", "DISABLED"]
    expected_resp_neg = [403]
    client_user_test_dataset_list = DatasetList()
    for client_type in client_types:
        for user_type in user_types:
            for status in statuses:
                suffix_test_name = "{client}_{user}_{status}".format(
                    client=client_type.lower(),
                    user=user_type.lower(),
                    status=status.lower())
                expected_resp = []
                if client_type in ["PUBLIC_CLIENT", "DEFAULT_CLIENT"]:
                    expected_resp = expected_resp_neg
                elif client_type=="ADMIN_CLIENT" and \
                                user_type=="IDENTITY_USER":
                    expected_resp = expected_resp_neg
                else:
                    expected_resp = expected_resp_normal
                data_type_for_test = {'client_type': client_type,
                                      'user_type': user_type,
                                      'user_status': status,
                                      'expected_resp': expected_resp
                                      }
                client_user_test_dataset_list.append_new_dataset(
                    suffix_test_name, data_type_for_test)

    # Generating test data to verify role propagation related test scenarios
    user_test_role_prop_dataset_list = DatasetList()
    data_type_for_role_prop_test = {'user_one': "USER_ADMIN_USER",
                                    'user_two': "SUB_USER",
                                    'role_type': "ROLE_PROP_TRUE",
                                    'expected_resp': [409]
                                    }
    user_test_role_prop_dataset_list.append_new_dataset(
        "to_user_admin_and_sub_user_prop_true", data_type_for_role_prop_test)
    data_type_for_role_prop_test = {'user_one': "USER_ADMIN_USER",
                                    'user_two': "SUB_USER",
                                    'role_type': "ROLE_PROP_FALSE",
                                    'expected_resp': expected_resp_normal
                                    }
    user_test_role_prop_dataset_list.append_new_dataset(
        "to_user_admin_and_sub_user_prop_false", data_type_for_role_prop_test)
    data_type_for_role_prop_test = {'user_one': "SUB_USER",
                                    'user_two': "USER_ADMIN_USER",
                                    'role_type': "ROLE_PROP_TRUE",
                                    'expected_resp': expected_resp_normal
                                    }
    user_test_role_prop_dataset_list.append_new_dataset(
        "to_sub_user_and_user_admin_prop_true", data_type_for_role_prop_test)
    data_type_for_role_prop_test = {'user_one': "SUB_USER",
                                    'user_two': "USER_ADMIN_USER",
                                    'role_type': "ROLE_PROP_FALSE",
                                    'expected_resp': expected_resp_normal
                                    }
    user_test_role_prop_dataset_list.append_new_dataset(
        "to_sub_user_and_user_admin_prop_false", data_type_for_role_prop_test)

    # Generating test data to atom hopper feed for negative tenant to the user
    # atom hopper feed for negative tenant can be seen in the feed when the
    # tenant is added to the feed and revoked the token for that user
    ah_feed_test_user_list = DatasetList()
    for user_type in user_types:
        data_type_for_ah_feed_user_test = {'user_type': user_type}
        suffix_test_name = "{user}".format(user=user_type.lower())
        ah_feed_test_user_list.append_new_dataset(
            suffix_test_name, data_type_for_ah_feed_user_test)

    @classmethod
    def setUpClass(cls):
        """
        Function to create test bed for all the test. Execute once at the
        beginning of class
        @param cls: instance of class

        """
        super(TenantBaseUrlAuthTest, cls).setUpClass()
        cls.serv_admin_name = cls.config.identity_api.service_username
        cls.serv_admin_password = cls.config.identity_api.service_password

        cls.identity_admin_name = rand_name("ccidentityadmin")
        cls.user_admin_name = rand_name("ccuseradmin")
        cls.sub_user_name = rand_name("ccsubuser")
        cls.sub_user_name_for_client = rand_name("ccsubuserclient")
        cls.password = "CCPassword1"
        cls.domain_id = random_int(10000, 1000000000)

        cls.auth_iden_adm_resp = cls.service_client.authenticate_user_password(
            cls.config.identity_api.admin_username,
            cls.config.identity_api.admin_password)
        cls.admin_client.token = cls.auth_iden_adm_resp.entity.token.id

        cls.provider = IdentityAPIProvider(cls.config)
        cls.public_admin_client = cls.provider.get_client()
        cls.default_client = cls.provider.get_client()
        cls.auth_user_adm_resp = cls.service_client.authenticate_user_password(
            cls.config.identity_api.username,
            cls.config.identity_api.password)
        cls.public_admin_client.token = cls.auth_user_adm_resp.entity.token.id

        cls.create_sub_user_client_resp = cls.get_test_user_v2_0(
            client=cls.public_admin_client,
            username=cls.sub_user_name_for_client,
            password=cls.password)
        cls.sub_user_client_auth_resp = \
            cls.public_client.authenticate_user_password(
                cls.sub_user_name_for_client,
                cls.password)
        cls.default_client.token = \
            cls.sub_user_client_auth_resp.entity.token.id

        cls.get_service_user_to_test_resp = \
            cls.service_client.get_user_by_name(
                name=cls.config.identity_api.service_username_to_test)

        serv_admin_client = cls.set_client(
            username=cls.serv_admin_name, password=cls.serv_admin_password,
            user_type=IdentityClientTypes.SERVICE)
        cls.create_iden_adm_resp = cls.get_test_user_v2_0(
            client=serv_admin_client, username=cls.identity_admin_name,
            password=cls.password, domain_id=None, enabled=True)

        iden_admin_client = cls.set_client(
            username=cls.identity_admin_name, password=cls.password,
            user_type=IdentityClientTypes.ADMIN)
        cls.create_usr_adm_resp = cls.get_test_user_v2_0(
            client=iden_admin_client, username=cls.user_admin_name,
            password=cls.password, domain_id=cls.domain_id, enabled=True)

        user_admin_client = cls.set_client(
            username=cls.user_admin_name, password=cls.password,
            user_type=IdentityClientTypes.DEFAULT)
        cls.create_sub_usr_resp = cls.get_test_user_v2_0(
            client=user_admin_client, username=cls.sub_user_name,
            password=cls.password, domain_id=None, enabled=True)

        # creating enabled tenant for test
        cls.create_tenant_resp = cls.get_test_tenant(
            client=cls.admin_client, enabled=True)
        # creating roles with propation flag as True and False
        cls.create_role_resp = cls.get_test_role(
            client=cls.admin_client, propagate=True)
        cls.create_role_prop_false_resp = cls.get_test_role(
            client=cls.admin_client, propagate=False)

        # Data set list gets executed before setUpClass, here we are setting
        # up the exact client, user and role data set list, which will be
        # fetched from the test case
        cls.client_list = {"SERVICE_CLIENT": cls.service_client,
                           "ADMIN_CLIENT": cls.admin_client,
                           "PUBLIC_CLIENT": cls.public_admin_client,
                           "DEFAULT_CLIENT": cls.default_client}
        cls.user_list = {"SERVICE_USER": cls.get_service_user_to_test_resp,
                         "IDENTITY_USER": cls.create_iden_adm_resp,
                         "USER_ADMIN_USER": cls.create_usr_adm_resp,
                         "SUB_USER": cls.create_sub_usr_resp}
        cls.user_status_list = {"ENABLED": True, "DISABLED": False}
        cls.roles_list = {"ROLE_PROP_TRUE": cls.create_role_resp,
                          "ROLE_PROP_FALSE": cls.create_role_prop_false_resp}

        # creating endpoint template
        cls.create_endpoint_template_resp = (
            cls.get_test_endpoint_template(
                client=cls.admin_client,
                enabled=True))
        # creating disabled endpoint template
        cls.create_disabled_endpoint_template_resp = (
            cls.get_test_endpoint_template(
                client=cls.admin_client,
                enabled=False))

        # Adding enabled endpoint to the enabled tenant
        cls.admin_client.add_endpoint_to_tenant(
            id=cls.create_endpoint_template_resp.entity.id,
            tenant_id=cls.create_tenant_resp.entity.id)
        cls.admin_client.add_endpoint_to_tenant(
            id=cls.create_disabled_endpoint_template_resp.entity.id,
            tenant_id=cls.create_tenant_resp.entity.id)

        # creating disabled tenant for test
        cls.create_disabled_tenant_resp = cls.get_test_tenant(
            client=cls.admin_client, enabled=False)

        # Adding enabled endpoint to the disabled tenant
        cls.admin_client.add_endpoint_to_tenant(
            id=cls.create_endpoint_template_resp.entity.id,
            tenant_id=cls.create_disabled_tenant_resp.entity.id)
        cls.admin_client.add_endpoint_to_tenant(
            id=cls.create_disabled_endpoint_template_resp.entity.id,
            tenant_id=cls.create_disabled_tenant_resp.entity.id)

        cls.atomhp = AtomHopperProvider(
            url=cls.config.identity_api.atom_hopper_url,
            config=cls.config,
            auth_token=cls.admin_client.token)

    @classmethod
    def tearDownClass(cls):
        """
        Function to clean up the data after execution of all the tests
        completed. Execute once at the end of all the tests.
        @param cls: instance of class

        """
        cls.delete_user_permanently(
            user_id=cls.create_sub_user_client_resp.entity.id,
            client=cls.service_client)

        cls.delete_user_permanently(
            user_id=cls.create_sub_usr_resp.entity.id,
            client=cls.service_client)

        cls.delete_user_permanently(
            user_id=cls.create_usr_adm_resp.entity.id,
            client=cls.service_client)

        cls.delete_user_permanently(
            user_id=cls.create_iden_adm_resp.entity.id,
            client=cls.service_client)

        cls.admin_client.delete_domain(domain_id=cls.domain_id)
        cls.admin_client.delete_role(role_id=cls.create_role_resp.entity.id)
        cls.admin_client.delete_role(
            role_id=cls.create_role_prop_false_resp.entity.id)

        # Deleting endpoints from enabled tenant
        cls.admin_client.delete_endpoint_to_tenant(
            endpoint_id=cls.create_endpoint_template_resp.entity.id,
            tenant_id=cls.create_tenant_resp.entity.id)
        cls.admin_client.delete_endpoint_to_tenant(
            endpoint_id=cls.create_disabled_endpoint_template_resp.entity.id,
            tenant_id=cls.create_tenant_resp.entity.id)
        # Deleting enabled tenant
        cls.admin_client.delete_tenant(cls.create_tenant_resp.entity.id)

        # Deleting endpoints from disabled tenant
        cls.admin_client.delete_endpoint_to_tenant(
            endpoint_id=cls.create_endpoint_template_resp.entity.id,
            tenant_id=cls.create_disabled_tenant_resp.entity.id)
        cls.admin_client.delete_endpoint_to_tenant(
            endpoint_id=cls.create_disabled_endpoint_template_resp.entity.id,
            tenant_id=cls.create_disabled_tenant_resp.entity.id)
        # Deleting disabled tenant
        cls.admin_client.delete_tenant(
            cls.create_disabled_tenant_resp.entity.id)

        # Deleting endpoint templates
        cls.admin_client.delete_endpoint_template(
            endpoint_template_id=cls.create_endpoint_template_resp.entity.id)
        cls.admin_client.delete_endpoint_template(
            endpoint_template_id=
            cls.create_disabled_endpoint_template_resp.entity.id)

    def _set_user_enabled_state(self, enabled):
        """
        This method updates the user status for the test

        """
        updated_user = self.service_client.update_user(
            user_id=self.create_usr_adm_resp.entity.id,
            enabled=enabled)
        self.assertEqual(
            updated_user.entity.enabled, enabled,
            msg="Updated user is not in {0} state.".format(enabled))
        updated_user = self.service_client.update_user(
            user_id=self.create_sub_usr_resp.entity.id,
            enabled=enabled)
        self.assertEqual(
            updated_user.entity.enabled, enabled,
            msg="Updated user is not in {0} state.".format(enabled))
        updated_user = self.service_client.update_user(
            user_id=self.create_iden_adm_resp.entity.id,
            enabled=enabled)
        self.assertEqual(
            updated_user.entity.enabled, enabled,
            msg="Updated user is not in {0} state.".format(enabled))

    def _add_role_to_user_on_tenant(self, role_id, user_id, expected_resp,
                                    client=None):
        """
        Method to add role to the user on tenant

        """
        client = client or self.admin_client
        add_role_to_user_on_tenant_resp = (
            client.add_role_to_user_on_tenant(
                tenant_id=self.create_tenant_resp.entity.id,
                user_id=user_id,
                role_id=role_id))
        self.assertIn(
            add_role_to_user_on_tenant_resp.status_code,
            expected_resp,
            msg='Response for Add role to user on tenant is not in {0}'.format(
                expected_resp))
        self.addCleanup(
            self.service_client.delete_role_to_user_on_tenant,
            tenant_id=self.create_tenant_resp.entity.id,
            user_id=user_id,
            role_id=role_id)
        list_roles = client.list_roles_for_user_on_tenant(
                tenant_id=self.create_tenant_resp.entity.id,
                user_id=user_id)
        self.assertEqual(
            list_roles.entity[0].id,
            role_id,
            msg="Role not found for the user on tenant.")

    def _delete_role_to_user_on_tenant(self, role_id, user_id, expected_resp,
                                       client=None):
        """
        Method to delete role to the user on tenant

        """
        client = client or self.admin_client
        del_role = client.delete_role_to_user_on_tenant(
            tenant_id=self.create_tenant_resp.entity.id,
            user_id=user_id,
            role_id=role_id)
        self.assertIn(
            del_role.status_code,
            expected_resp,
            msg='Delete  expected {0} received {1}'.format(
                expected_resp,
                del_role.status_code))

    @data_driven_test(ah_feed_test_user_list)
    @attr('regression')
    def ddtest_atom_hopper_feed_test_for_user(self, user_type):
        """
        Data driven test to verify the tenant id in the Atom hopper feed for
        the user when the users token got revoked.

        """
        user_id = self.user_list[user_type].entity.id
        user_name = ""
        password = self.password
        self._set_user_enabled_state(enabled=True)
        normal_response_codes = self.expected_resp_normal
        role_id = self.create_role_resp.entity.id
        delete_role_from_user_resp_code = [204]
        if user_type is "IDENTITY_USER":
            client = self.client_list["SERVICE_CLIENT"]
            user_name = self.identity_admin_name
            password = self.password
        else:
            client = self.client_list["ADMIN_CLIENT"]
            user_name = self.user_list[user_type].entity.username

        auth_user_resp = client.authenticate_user_password(
            user_name,
            password)
        self.assertEqual(
            auth_user_resp.status_code, 200,
            msg=("Authentication Failed, response code received is {0}".format(
                auth_user_resp.status_code)))
        self._add_role_to_user_on_tenant(
            client=client,
            role_id=role_id,
            user_id=user_id,
            expected_resp=normal_response_codes)

        #revoke token
        revoke_resp = client.revoke_token(auth_user_resp.entity.token.id)
        self.assertEqual(
            revoke_resp.status_code, 204,
            msg=('Revoke token, Exepected response code {0} actual {1}'.format(
                204, revoke_resp.status_code)))

        # Searching the Atom hopper feed for the users revoked token and
        # assert the tenant id for that user in the event
        search_attrib = 'resourceId'
        results = self.atomhp.search_past_events_by_attribute(
            attribute=search_attrib,
            attribute_regex=auth_user_resp.entity.token.id)
        user_tenants = results.product.tenants.split()
        self.assertEqual(
            results.resourceId, auth_user_resp.entity.token.id,
            msg='Revoke Token Feed not found in the AH.')
        self.assertEqual(
            results.type, 'DELETE',
            msg='Revoke Token Feed found was not type of Delete')
        self.assertIn(
            self.create_tenant_resp.entity.id, user_tenants,
            msg="Tenant not found in AtomHopper feed when token revoked")

        self._delete_role_to_user_on_tenant(
            client=client,
            role_id=role_id,
            user_id=user_id,
            expected_resp=delete_role_from_user_resp_code)

    @data_driven_test(user_test_role_prop_dataset_list)
    @attr('regression')
    def ddtest_add_and_delete_role(self, user_one, user_two, role_type,
                                   expected_resp):
        """
        Data driven test to verify the role propagation between user admin
        and sub users for all different scenarios
        @param user_one : User to which the role is added first
        @param user_two : User to which the role is added second
        user_one and user_two could be either user admin or sub user users

        """
        user_one = self.user_list[user_one].entity.id
        user_two = self.user_list[user_two].entity.id
        role_id = self.roles_list[role_type].entity.id
        user_one_delete_role_resp_code = [204]

        # delete role respose from user one and two (i.e. either user admin
        # or sub user) are same usually.  But when role propagation flag is
        # set as True and when user one is User admin and user two is Sub user,
        # then the added role to user admin will be propagated to sub user
        # so when the same role is tried added to the sub user you can see a
        # conflict response.  Similarly for the same scenario, when the role
        # is removed from user admin (user one), the role is removed from the
        # sub user (user two) as well.  So when tried to remove the role
        # sub user (user two) we can see 404 response code.
        user_two_delete_role_resp_code = user_one_delete_role_resp_code
        if expected_resp == [409]:
            user_two_delete_role_resp_code = [404]

        self._set_user_enabled_state(enabled=True)
        self._add_role_to_user_on_tenant(
            role_id=role_id,
            user_id=user_one,
            expected_resp=self.expected_resp_normal)
        self._add_role_to_user_on_tenant(
            role_id=role_id,
            user_id=user_two,
            expected_resp=expected_resp)

        self._delete_role_to_user_on_tenant(
            role_id=role_id,
            user_id=user_one,
            expected_resp=user_one_delete_role_resp_code)
        self._delete_role_to_user_on_tenant(
            role_id=role_id,
            user_id=user_two,
            expected_resp=user_two_delete_role_resp_code)

    @data_driven_test(client_user_test_dataset_list)
    @attr('regression')
    def ddtest_add_role_to_user_on_tenant(self, client_type, user_type,
                                          user_status, expected_resp):
        """
        Test to verify the role added to users on tenant

        Propagation Flag is set as True for the role used in this test case,
        so when this test case gets executed for the user admin and if the
        propagation flag works as expected, then the role is propagated to the
        sub users and it will be removed from them at the end of the test.
        So when the same role is added to sub user there won't be any conflicts
        if the flag works fine.  Here we are not explicitly verifying
        propagation flag, but we are verifying in-directly.  There is another
        test which explicitly verifies propagation flag between user admin
        and sub users.

        """
        client = self.client_list[client_type]
        user_id = self.user_list[user_type].entity.id
        user_status = self.user_status_list[user_status]

        normal_response_codes = expected_resp
        delete_role_from_user_resp_code = [204]
        self._set_user_enabled_state(enabled=user_status)

        add_role_to_user_on_tenant_resp = (
            client.add_role_to_user_on_tenant(
                tenant_id=self.create_tenant_resp.entity.id,
                user_id=user_id,
                role_id=self.create_role_resp.entity.id))
        self.assertIn(
            add_role_to_user_on_tenant_resp.status_code,
            normal_response_codes,
            msg='Add base URLs expected {0} received {1}'.format(
                normal_response_codes,
                add_role_to_user_on_tenant_resp.status_code))
        self.addCleanup(
            self.service_client.delete_role_to_user_on_tenant,
            tenant_id=self.create_tenant_resp.entity.id,
            user_id=user_id,
            role_id=self.create_role_resp.entity.id)

        # Below test logic is valid only for positive test cases
        # i.e. where add_role_to_user_on_tenant_resp returns 200
        if (add_role_to_user_on_tenant_resp.status_code in
                self.expected_resp_normal):
            list_roles = client.list_roles_for_user_on_tenant(
                tenant_id=self.create_tenant_resp.entity.id,
                user_id=user_id)
            self.assertEqual(
                list_roles.entity[0].id,
                self.create_role_resp.entity.id,
                msg="Role not found for the user on tenant.")

            del_role = client.delete_role_to_user_on_tenant(
                tenant_id=self.create_tenant_resp.entity.id,
                user_id=user_id,
                role_id=self.create_role_resp.entity.id)
            self.assertIn(
                del_role.status_code,
                delete_role_from_user_resp_code,
                msg='Delete  expected {0} received {1}'.format(
                    delete_role_from_user_resp_code,
                    del_role.status_code))

    @data_driven_test(client_user_test_dataset_list)
    @attr('regression')
    def ddtest_add_role_to_user_on_disabled_tenant(
            self, client_type, user_type, user_status, expected_resp):
        """
        Test to verify the role added to diabled users on tenant

        Propagation Flag is set as True for the role used in this test case,
        so when this test case gets executed for the user admin and if the
        propagation flag works as expected, then the role is propagated to the
        sub users and it will be removed from them at the end of the test.
        So when the same role is added to sub user there won't be any conflicts
        if the flag works fine.  Here we are not explicitly verifying
        propagation flag, but we are verifying in-directly.  There is another
        test which explicitly verifies propagation flag between user admin
        and sub users.

        """
        client = self.client_list[client_type]
        user_id = self.user_list[user_type].entity.id
        user_status = self.user_status_list[user_status]

        normal_response_codes = expected_resp
        delete_role_from_user_resp_code = [204]
        self._set_user_enabled_state(enabled=user_status)

        add_role_to_user_on_tenant_resp = (
            client.add_role_to_user_on_tenant(
                tenant_id=self.create_disabled_tenant_resp.entity.id,
                user_id=user_id,
                role_id=self.create_role_resp.entity.id))
        self.assertIn(
            add_role_to_user_on_tenant_resp.status_code,
            normal_response_codes,
            msg='Add base URLs expected {0} received {1}'.format(
                normal_response_codes,
                add_role_to_user_on_tenant_resp.status_code))
        self.addCleanup(
            self.service_client.delete_role_to_user_on_tenant,
            tenant_id=self.create_tenant_resp.entity.id,
            user_id=user_id,
            role_id=self.create_role_resp.entity.id)

        # Below test logic is valid only for positive test cases
        # i.e. where add_role_to_user_on_tenant_resp returns 200
        if (add_role_to_user_on_tenant_resp.status_code in
                self.expected_resp_normal):
            list_roles = client.list_roles_for_user_on_tenant(
                tenant_id=self.create_disabled_tenant_resp.entity.id,
                user_id=user_id)
            self.assertEqual(
                list_roles.entity[0].id,
                self.create_role_resp.entity.id,
                msg="Role not found for the user on tenant.")

            del_role = client.delete_role_to_user_on_tenant(
                tenant_id=self.create_disabled_tenant_resp.entity.id,
                user_id=user_id,
                role_id=self.create_role_resp.entity.id)
            self.assertIn(
                del_role.status_code,
                delete_role_from_user_resp_code,
                msg='Delete  expected {0} received {1}'.format(
                    delete_role_from_user_resp_code,
                    del_role.status_code))
