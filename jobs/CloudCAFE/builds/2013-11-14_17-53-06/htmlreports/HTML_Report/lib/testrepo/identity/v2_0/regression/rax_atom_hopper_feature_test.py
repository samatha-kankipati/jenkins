from ccengine.common.tools.datagen import rand_name
from ccengine.common.tools.datagen import random_int
from ccengine.common.decorators import attr
from ccengine.providers.atomhopper import AtomHopperProvider
from testrepo.common.testfixtures.identity.v2_0.identity \
    import BaseIdentityFixture


class RaxAtomHopperFeedTest(BaseIdentityFixture):
    """
    Atom Hopper feed related tests
    """

    @classmethod
    def setUpClass(cls):
        """
        Function to create test bed for all the test. Execute once at the
        beginning of class
        @param cls: instance of class
        """
        super(RaxAtomHopperFeedTest, cls).setUpClass()
        cls.useradminname = rand_name("ccuseradmin")
        cls.email = '{0}@{1}'.format("testbox", "mailtrust.com")
        domain_id = random_int(10000, 1000000000)
        cls.password = "Gsubusrpass8"

        cls.auth_iden_adm_resp = cls.service_client.authenticate_user_password(
            cls.config.identity_api.admin_username,
            cls.config.identity_api.admin_password)
        cls.admin_client.token = cls.auth_iden_adm_resp.entity.token.id

        cls.servadminname = cls.config.identity_api.service_username
        cls.idenadminname = cls.config.identity_api.admin_username

        cls.user_adm_resp = cls.admin_client.add_user(
            username=cls.useradminname,
            email=cls.email,
            enabled=True,
            domain_id=domain_id,
            password=cls.password)
        cls.public_client.token = cls.provider.get_token(
            username=cls.useradminname,
            password=cls.password)

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
        cls.delete_user_permanently(user_id=cls.user_adm_resp.entity.id,
                                    client=cls.admin_client)

    def create_user_and_check_feed_for(self, client, username, domain_id):
        """
        Function to create a user and check the atom feed for the same.
        @param client: Client to create user with different token
        @param username: Username of the user type string
        @param domain_id: None or Integer value of domain
        @return user_client with created user token
        @return Response object of create user
        """
        user_add_resp = client.add_user(username=username,
                                        email=self.email,
                                        enabled=True,
                                        domain_id=domain_id,
                                        password=self.password)
        self.assertEqual(user_add_resp.status_code,
                         201, msg="Add user response is not 201")
        # delete user after test completion
        self.addCleanup(self.delete_user_permanently,
                        user_id=user_add_resp.entity.id,
                        client=client)
        user_client = self.provider.get_client()
        user_client.token = self.provider.get_token(username=username,
                                                    password=self.password)
        search_attrib = 'resourceName'
        search_regex = username
        user_create_feed = self.atomhp.search_past_events_by_attribute(
            attribute=search_attrib,
            attribute_regex=search_regex)
        self.assertIsNotNone(
            user_create_feed,
            msg='No Feed found in the Atom Hopper for the attributes')
        return user_client, user_add_resp

    @attr('regression', type='positive')
    def test_39383_verify_atom_hopper_add_delete_role_from_user(self):
        """
        Verifies atom hopper feed for adding and deleting role to/from user
        """
        test_values = {self.service_client: rand_name("ccidentityadmin"),
                       self.admin_client: rand_name("ccuseradmin"),
                       self.public_client: rand_name("ccsubuser")}
        for client, username in test_values.iteritems():
            role_name = rand_name("Guest:Role")
            description = rand_name("Guest description ")
            propagation_flag = False
            domain_id = random_int(10000, 1000000000)
            if client == self.service_client:
                domain_id = None
            create_user_resp = client.add_user(username=username,
                                               email=self.email,
                                               enabled=True,
                                               domain_id=domain_id,
                                               password=self.password)
            self.assertEqual(create_user_resp.status_code,
                             201,
                             msg='Add user expected response 201 received '
                                 '{0}'.format(create_user_resp.status_code))
            # delete user after test completion
            self.addCleanup(self.delete_user_permanently,
                            user_id=create_user_resp.entity.id,
                            client=client)

            add_role = self.admin_client.add_role(name=role_name,
                                                  description=description,
                                                  propagate=propagation_flag)
            self.assertEqual(add_role.status_code,
                             201,
                             msg="Response is not 201")
            # delete role after test completion
            self.addCleanup(self.admin_client.delete_role,
                            role_id=add_role.entity.id)

            add_role_to_user = client.add_role_to_user(
                user_id=create_user_resp.entity.id,
                role_id=add_role.entity.id)
            normal_response_codes = 200
            self.assertEqual(
                add_role_to_user.status_code,
                normal_response_codes,
                msg='Add role to user response expected {0} received {1}'
                .format(normal_response_codes, add_role_to_user.status_code))

            user_roles = self.admin_client.list_user_global_roles(
                user_id=create_user_resp.entity.id)
            role_added_to_user = False
            for user_role in user_roles.entity:
                if user_role.name == add_role.entity.name:
                    role_added_to_user = True
            self.assertTrue(role_added_to_user,
                            msg="Role is not added to user.")

            search_attrib = 'resourceName'
            search_regex = username
            results = self.atomhp.search_past_events_by_attribute(
                attribute=search_attrib,
                attribute_regex=search_regex)
            self.assertIsNotNone(
                results,
                msg='No Feed found in the Atom Hopper for the attributes')
            user_roles = results.product.roles.split()
            self.assertIn(role_name, user_roles, msg="Role not found in feed")

            delete_role_from_user = client.delete_role_from_user(
                user_id=create_user_resp.entity.id,
                role_id=add_role.entity.id)
            self.assertEqual(delete_role_from_user.status_code,
                             204,
                             msg="Response is not 204")

            user_roles = client.list_user_global_roles(
                user_id=create_user_resp.entity.id)
            for userrole in user_roles.entity:
                self.assertNotEqual(userrole.name, role_name,
                                    msg="Role deletion from user failed")

            search_attrib = 'resourceName'
            search_regex = username
            results = self.atomhp.search_past_events_by_attribute(
                search_attrib,
                search_regex)
            user_roles = results.product.roles.split()
            self.assertNotIn(role_name, user_roles, msg="Role found in feed")

    @attr('regression', type='positive')
    def test_39382_atom_hopper_add_delete_role_from_user_propagation(self):
        """
        Verifies role propagation and atom feeds for the same
        """
        create_user_list = []
        username = rand_name("ccuseradmin")
        propagation_flag = True
        email = '{0}@{1}'.format("testbox", "mailtrust.com")
        domain_id = random_int(10000, 1000000000)
        sub_user = rand_name("ccsubuser")
        create_user_resp = self.admin_client.add_user(username=username,
                                                      email=email,
                                                      enabled=True,
                                                      domain_id=domain_id,
                                                      password=self.password)
        self.assertEqual(create_user_resp.status_code,
                         201,
                         msg='Add user response is not 201.')
        # delete user after test completion
        self.addCleanup(self.delete_user_permanently,
                        user_id=create_user_resp.entity.id,
                        client=self.admin_client)

        auth_user_adm = self.public_client.authenticate_user_password(
            username,
            self.password)
        public_admin_client = self.provider.get_client()
        public_admin_client.token = auth_user_adm.entity.token.id

        create_sub_user_resp = public_admin_client.add_user(
            username=sub_user,
            email=email,
            enabled=True,
            domain_id=domain_id,
            password=self.password)
        self.assertEqual(create_sub_user_resp.status_code,
                         201,
                         msg='Add user response is not 201.')
        # delete sub-user after test completion
        self.addCleanup(self.delete_user_permanently,
                        user_id=create_sub_user_resp.entity.id,
                        client=public_admin_client)

        create_user_list.append(create_sub_user_resp)
        create_user_list.append(create_user_resp)

        role_name = rand_name("ccRole")
        description = "role for testing"
        add_role = self.admin_client.add_role(name=role_name,
                                              description=description,
                                              propagate=propagation_flag)
        self.assertEqual(add_role.status_code,
                         201,
                         msg="Add role response is not 201.")
        # delete role after test completion
        self.addCleanup(self.admin_client.delete_role,
                        role_id=add_role.entity.id)

        add_role_to_user = self.admin_client.add_role_to_user(
            user_id=create_user_resp.entity.id,
            role_id=add_role.entity.id)
        self.assertEqual(add_role_to_user.status_code,
                         200,
                         msg="Add role to user response is not 200.")

        for user_info in create_user_list:
            user_roles = self.admin_client.list_user_global_roles(
                user_id=user_info.entity.id)
            role_added_to_user = False
            for userrole in user_roles.entity:
                if userrole.name == add_role.entity.name:
                    role_added_to_user = True
            self.assertTrue(role_added_to_user, msg="Role not added to user")

            search_attrib = 'resourceName'
            search_regex = user_info.entity.username
            results = self.atomhp.search_past_events_by_attribute(
                attribute=search_attrib,
                attribute_regex=search_regex)
            user_roles = results.product.roles.split()
            self.assertIn(role_name, user_roles, msg="Role not found in feed")

        delete_role_from_user = self.admin_client.delete_role_from_user(
            user_id=create_user_resp.entity.id,
            role_id=add_role.entity.id)
        self.assertEqual(delete_role_from_user.status_code,
                         204,
                         msg="Response is not 204")

        for user_info in create_user_list:
            user_roles = self.admin_client.list_user_global_roles(
                user_id=user_info.entity.id)
            for userrole in user_roles.entity:
                self.assertNotEqual(userrole.name, role_name,
                                    msg="Role deletion from user failed")

            search_attrib = 'resourceName'
            search_regex = user_info.entity.username
            results = self.atomhp.search_past_events_by_attribute(
                search_attrib,
                search_regex)
            user_roles = results.product.roles.split()
            self.assertNotIn(role_name, user_roles, msg="Role found in feed")

    @attr('regression', type='positive')
    def test_39382_verify_atom_hopper_add_and_delete_group(self):
        """
        Verifies atom hopper feed for add and delete group from user
        """
        test_values = {self.service_client: rand_name("ccidentityadmin"),
                       self.admin_client: rand_name("ccuseradmin")}
        for client, username in test_values.iteritems():
            create_user_list = []
            email = '{0}@{1}'.format("testbox", "mailtrust.com")
            domain_id = random_int(10000, 1000000000)
            if client == self.service_client:
                create_user_resp = client.add_user(username=username,
                                                   email=email,
                                                   enabled=True,
                                                   password=self.password)
                self.assertEqual(create_user_resp.status_code,
                                 201,
                                 msg='Add user response is not 201')
                # delete user after test completion
                self.addCleanup(self.delete_user_permanently,
                                user_id=create_user_resp.entity.id,
                                client=client)
            else:
                create_user_resp = client.add_user(username=username,
                                                   email=email,
                                                   enabled=True,
                                                   domain_id=domain_id,
                                                   password=self.password)
                self.assertEqual(create_user_resp.status_code,
                                 201,
                                 msg='Add user response is not 201')
                # delete user after test completion
                self.addCleanup(self.delete_user_permanently,
                                user_id=create_user_resp,
                                client=client)
                public_admin_client = self.provider.get_client()
                public_admin_client.token = self.provider.get_token(
                    username=username, password=self.password)

                sub_user = rand_name("ccsubuser")
                create_sub_user_resp = public_admin_client.add_user(
                    username=sub_user,
                    email=email,
                    enabled=True,
                    domain_id=domain_id,
                    password=self.password)
                self.assertEqual(create_sub_user_resp.status_code,
                                 201,
                                 msg='Add user response is not 201')
                # delete sub-user after test completion
                self.addCleanup(self.delete_user_permanently,
                                user_id=create_sub_user_resp.entity.id,
                                client=public_admin_client)
                create_user_list.append(create_sub_user_resp)

            create_user_list.append(create_user_resp)
            name_group = rand_name("cc group name")
            description = "Group for testing"
            add_group = self.admin_client.add_group(name=name_group,
                                                    description=description)
            self.assertEqual(add_group.status_code,
                             201,
                             msg="Response is not 201")
            # Delete group after test completion
            self.addCleanup(self.admin_client.delete_group,
                            group_id=add_group.entity.id)

            user_addgroup = self.service_client.add_user_to_group(
                user_id=create_user_resp.entity.id,
                group_id=add_group.entity.id)
            self.assertEqual(user_addgroup.status_code,
                             204,
                             msg="Add user to group response is not 204.")
            # Remove user from group after test completion
            self.addCleanup(self.service_client.remove_user_from_group,
                            user_id=create_user_resp.entity.id,
                            group_id=add_group.entity.id)

            search_attrib = 'resourceName'
            for user in create_user_list:
                user_groups = self.service_client.list_groups_for_user(
                    user_id=user.entity.id)
                self.assertEqual(user_groups.status_code,
                                 200,
                                 msg="Response is not 200")
                group_added_to_user = False
                for group in user_groups.entity:
                    if group.id == add_group.entity.id:
                        group_added_to_user = True
                self.assertTrue(group_added_to_user,
                                msg="Group is not added to user.")

                results = self.atomhp.search_past_events_by_attribute(
                    attribute=search_attrib,
                    attribute_regex=user.entity.username)
                user_groups = results.product.groups.split()
                self.assertIn(add_group.entity.id, user_groups,
                              msg="Group ID is not found in feed.")

            user_removegroup = self.admin_client.remove_user_from_group(
                user_id=create_user_resp.entity.id,
                group_id=add_group.entity.id)
            self.assertEqual(user_removegroup.status_code,
                             204,
                             msg="Remove user from group Response is not 204.")

            search_attrib = 'resourceName'
            for user in create_user_list:
                user_groups = self.service_client.list_groups_for_user(
                    user_id=user.entity.id)
                self.assertEqual(user_groups.status_code,
                                 200,
                                 msg="Get global role for user response is "
                                     "not 200.")
                for group in user_groups.entity:
                    self.assertNotEqual(group.id,
                                        add_group.entity.id,
                                        msg="Group is not removed from user.")

                results = self.atomhp.search_past_events_by_attribute(
                    attribute=search_attrib,
                    attribute_regex=user.entity.username)
                if results.product.groups is not None:
                    user_groups = results.product.groups.split()
                    self.assertNotIn(add_group.entity.id,
                                     user_groups,
                                     msg="Group feed found for removed group.")

    @attr('regression', type='positive')
    def test_39769_verify_atom_hopper_update_user_password(self):
        """
        Verifies atom hopper feed for update user's password
        """
        mod_password = 'ModGadmpass8'
        username_map = {self.service_client: rand_name("ccidenadmin"),
                        self.admin_client: rand_name("ccuseradmin"),
                        self.public_client: rand_name("ccsubuser")}
        for client, username in username_map.iteritems():
            domain_id = None
            if client == self.admin_client:
                domain_id = random_int(10000, 1000000000)
            user_client, user_add_resp = self.create_user_and_check_feed_for(
                client=client,
                username=username,
                domain_id=domain_id)

            update_user_password = self.admin_client.update_user(
                user_id=user_add_resp.entity.id,
                password=mod_password)
            self.assertEqual(update_user_password.status_code,
                             200,
                             msg="Update user response is not 200.")

            search_attrib = 'resourceId'
            results = self.atomhp.search_past_events_by_attribute(
                attribute=search_attrib,
                attribute_regex=user_client.token)
            self.assertEqual(results.resourceId,
                             user_client.token,
                             msg='Revoke Token Feed not found in the AH.')
            self.assertEqual(results.type,
                             'DELETE',
                             msg='Revoke Token Feed found was not'
                                 ' type of Delete')
            del user_client.token

    @attr('regression', type='positive')
    def test_39769_verify_atom_hopper_update_user_status(self):
        """
        Verifies atom hopper feed for update user's status
        """
        username_map = {self.service_client: rand_name("ccidenadmin"),
                        self.admin_client: rand_name("ccuseradmin"),
                        self.public_client: rand_name("ccsubuser")}
        for client, username in username_map.iteritems():
            domain_id = None
            if client == self.admin_client:
                domain_id = random_int(10000, 1000000000)
            user_client, user_add_resp = self.create_user_and_check_feed_for(
                client=client,
                username=username,
                domain_id=domain_id)

            update_user_status = self.admin_client.update_user(
                user_id=user_add_resp.entity.id,
                enabled=False)
            self.assertEqual(update_user_status.status_code,
                             200,
                             msg="Update user response is not 200.")

            search_attrib = 'resourceId'
            results = self.atomhp.search_past_events_by_attribute(
                attribute=search_attrib,
                attribute_regex=user_client.token)
            self.assertEqual(results.resourceId,
                             user_client.token,
                             msg='Revoke Token Feed not found in Atom Hopper.')
            self.assertEqual(results.type,
                             'DELETE',
                             msg="Revoke Token Feed was not type of Delete.")
            del user_client.token

    @attr('regression', type='positive')
    def test_39769_verify_atom_hopper_revoke_token(self):
        """
        Verifies atom hopper feed for revoke user's token
        """
        username_map = {self.service_client: rand_name("ccidenadmin"),
                        self.admin_client: rand_name("ccuseradmin"),
                        self.public_client: rand_name("ccsubuser")}
        for client, username in username_map.iteritems():
            domain_id = None
            if client == self.admin_client:
                domain_id = random_int(10000, 1000000000)
                # Ignoring second return value as not required in this test
            user_client, _ = self.create_user_and_check_feed_for(
                client=client,
                username=username,
                domain_id=domain_id)

            self.service_client.revoke_token(user_client.token)
            search_attrib = 'resourceId'
            search_regex = user_client.token
            results = self.atomhp.search_past_events_by_attribute(
                attribute=search_attrib,
                attribute_regex=search_regex)
            self.assertEqual(results.resourceId,
                             user_client.token,
                             msg='Revoke Token Feed not found in Atom Hopper')
            self.assertEqual(results.type,
                             'DELETE',
                             msg='Revoke Token Feed was not type of Delete')
