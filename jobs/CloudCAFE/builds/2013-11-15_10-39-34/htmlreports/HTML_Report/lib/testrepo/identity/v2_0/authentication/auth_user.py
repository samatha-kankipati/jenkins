from ccengine.common.dataset_generators import DatasetList
from ccengine.common.decorators import (
    attr, DataDrivenFixture, data_driven_test)
from ccengine.common.tools.datagen import random_int, rand_name

from ccengine.providers.identity.v2_0.identity_api \
    import IdentityAPIProvider
from testrepo.common.testfixtures.identity.v2_0.identity \
    import BaseIdentityFixture


@DataDrivenFixture
class AuthenticationTest(BaseIdentityFixture):
    """
    @summary: Functional tests to verify roles listed in auth response

    Data set list for the test cases.  Based on these data set list
    test cases get replicated.

    Test data generated below is of type string, but it represents the type
    of data set combination that will be tested.
    Test data is a set of user type.  Exact test data will assigned inside the
    setUpClass where we get the created test users.

    """
    expected_resp_normal = [200]
    # Type of users to be tested
    user_types = ["IDENTITY_USER", "USER_ADMIN_USER", "SUB_USER"]

    # Generating test data to verify role listed after authentication
    user_dataset_list = DatasetList()
    for user_type in user_types:
        suffix_test_name = user_type.lower()
        data_type_for_test = {'user_type': user_type}
        user_dataset_list.append_new_dataset(
            suffix_test_name, data_type_for_test)

    @classmethod
    def setUpClass(cls):
        """
        Function to create test bed for all the test. Execute once at the
        beginning of class
        @param cls: instance of class

        """
        super(AuthenticationTest, cls).setUpClass()
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

        cls.create_iden_adm_resp = cls.get_test_user_v2_0(
            client=cls.service_client, username=cls.identity_admin_name,
            password=cls.password, domain_id=None, enabled=True)

        cls.create_usr_adm_resp = cls.get_test_user_v2_0(
            client=cls.admin_client, username=cls.user_admin_name,
            password=cls.password, domain_id=cls.domain_id, enabled=True)

        cls.create_sub_usr_resp = cls.get_test_user_v2_0(
            client=cls.public_admin_client, username=cls.sub_user_name,
            password=cls.password, domain_id=None, enabled=True)

        cls.role_resp_list = []
        cls.num_of_test_role = 5
        cls.roleid = 3
        for _ in range(cls.num_of_test_role):
            create_role_resp = cls.get_test_role(
                client=cls.admin_client, propagate=True)
            cls.roleid = create_role_resp.entity.id
            cls.role_resp_list.append(create_role_resp)

        # Data set list gets executed before setUpClass, here we are setting
        # up the exact user set list, which will be fetched from the test case
        cls.user_list = {"IDENTITY_USER": cls.create_iden_adm_resp,
                         "USER_ADMIN_USER": cls.create_usr_adm_resp,
                         "SUB_USER": cls.create_sub_usr_resp}

        # Default role id for the users
        cls.default_user_role_id_mapping = {
            "IDENTITY_USER":
            cls.config.default_role_id.identity_user_default_role_id,
            "USER_ADMIN_USER":
            cls.config.default_role_id.user_admin_default_role_id,
            "SUB_USER":
            cls.config.default_role_id.sub_user_default_role_id}

    @classmethod
    def tearDownClass(cls):
        """
        Function to clean up the data after execution of all the tests
        completed. Execute once at the end of all the tests.
        @param cls: instance of class

        """

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
        for role_resp in cls.role_resp_list:
            cls.admin_client.delete_role(role_id=role_resp.entity.id)

    @data_driven_test(user_dataset_list)
    @attr('regression')
    def ddtest_auth_resp_role_listing_for(self, user_type):
        """
        Test to verify the user roles in the auth response

        """
        user_id = self.user_list[user_type].entity.id
        username = self.user_list[user_type].entity.username
        # Roles to be verified in the auth response
        roles_to_verify = [role.entity.id for role in self.role_resp_list]
        roles_to_verify.append(self.default_user_role_id_mapping[user_type])

        normal_response_codes = [200, 201]
        # Adding test roles to the user to validate
        for role_resp in self.role_resp_list:
            add_role_to_user = self.service_client.add_role_to_user(
                user_id=user_id,
                role_id=role_resp.entity.id)
            self.assertIn(
                add_role_to_user.status_code,
                normal_response_codes,
                msg='Add role to user response expected {0} received {1}'.
                format(normal_response_codes, add_role_to_user.status_code))
        auth_resp = self.public_client.authenticate_user_password(
            username=username,
            password=self.password)
        user_roles = [user_role.id for user_role in
                      auth_resp.entity.user.roles]

        # verifying test roles added and the roles listed in auth response
        roles_not_in_auth_resp = list(set(roles_to_verify) - set(user_roles))
        self.assertEqual(
            [], roles_not_in_auth_resp,
            msg=('Roles with id {0} not present in auth resp'.format(
                roles_not_in_auth_resp)))

        for role_resp in self.role_resp_list:
            delete_role_from_user = self.service_client.delete_role_from_user(
                user_id=user_id,
                role_id=role_resp.entity.id)
            self.assertEqual(
                delete_role_from_user.status_code, 204,
                msg=("Delete role from user response is {0}".format(
                    delete_role_from_user.status_code)))
