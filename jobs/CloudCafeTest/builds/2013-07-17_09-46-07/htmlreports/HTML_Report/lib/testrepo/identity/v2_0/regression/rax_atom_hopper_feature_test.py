from ccengine.common.tools.datagen import rand_name
from ccengine.common.tools.datagen import random_int
from ccengine.common.decorators import attr
from ccengine.providers.atomhopper import AtomHopperProvider
from ccengine.providers.identity.v2_0.identity_api \
    import IdentityAPIProvider
from testrepo.common.testfixtures.identity.v2_0.identity \
    import BaseIdentityFixture


class RaxAtomHopperFeedTest(BaseIdentityFixture):

    @classmethod
    def setUpClass(cls):
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
                domainId=domain_id,
                password=cls.password)
        cls.auth_usr_adm_resp = cls.public_client.authenticate_user_password(
                cls.useradminname,
                cls.password)
        cls.public_client.token = cls.auth_usr_adm_resp.entity.token.id

        cls.atomhp = AtomHopperProvider(
                cls.config.identity_api.atom_hopper_url,
                cls.config)
        cls.provider = IdentityAPIProvider(cls.config)

    @classmethod
    def tearDownClass(cls):
        del cls.admin_client.token
        del cls.public_client.token
        cls.admin_client.delete_user(
                userId=cls.user_adm_resp.entity.id)
        cls.service_client.delete_user_hard(
                userId=cls.user_adm_resp.entity.id)

    def delete_user(self, user_info):
        delete_user_soft = self.admin_client.delete_user(
                userId=user_info.entity.id)
        if delete_user_soft.status_code == 204:
            delete_user_hard = self.service_client.delete_user_hard(
                userId=user_info.entity.id)
            return delete_user_hard.status_code
        return delete_user_soft.status_code

    @attr('regression', type='positive')
    def test_39383_verify_atom_hopper_add_role_to_user(self):
        test_values = {self.service_client: rand_name("ccidentityadmin"),
                       self.admin_client: rand_name("ccuseradmin"),
                       self.public_client: rand_name("ccsubuser")}
        client_keys = test_values.keys()
        for client in client_keys:
            name = rand_name("Guest:Role")
            description = rand_name("Guest description ")
            propagation_flag = False
            username = test_values.get(client)
            email = '{0}@{1}'.format("testbox", "mailtrust.com")
            domain_id = random_int(10000, 1000000000)
            if client == self.service_client:
                create_user_resp = client.add_user(
                        username=username,
                        email=email,
                        enabled=True,
                        password=self.password)
            else:
                create_user_resp = client.add_user(
                        username=username,
                        email=email,
                        enabled=True,
                        domainId=domain_id,
                        password=self.password)
            self.assertEqual(
                    create_user_resp.status_code,
                    201,
                    msg='Add user expected response 201 received {0}'.
                    format(create_user_resp.status_code))

            add_role = self.admin_client.add_role(
                    name=name,
                    description=description,
                    propagate=propagation_flag)
            self.assertEqual(
                    add_role.status_code,
                    201,
                    msg="Response is not 201")

            add_role_to_user = client.add_role_to_user(
                    userId=create_user_resp.entity.id,
                    roleId=add_role.entity.id)
            normal_response_codes = 200
            self.assertEqual(
                    add_role_to_user.status_code,
                    normal_response_codes,
                    msg='Add role to user response expected {0} received {1}'.
                    format(normal_response_codes,
                           add_role_to_user.status_code))

            user_roles = self.admin_client.list_user_global_roles(
                    userId=create_user_resp.entity.id)
            test_flag = False
            for userrole in user_roles.entity:
                if userrole.name == add_role.entity.name:
                    test_flag = True
            self.assertTrue(test_flag, msg="Role not added to user")

            search_attrib = 'resourceName'
            search_regex = username
            results = self.atomhp.search_past_events_by_attribute(
                    attribute=search_attrib,
                    attribute_regex=search_regex)
            self.assertIsNotNone(
                results,
                msg='No Feed found in the Atom Hopper for the attributes')
            user_roles = results.product.roles.split()
            feed_role_flag = False
            for role in user_roles:
                if role == name:
                    feed_role_flag = True
            self.assertTrue(feed_role_flag, msg="Role not found in feed")

            del_role_resp = self.service_client.delete_role(
                    roleId=add_role.entity.id)
            self.assertEqual(
                    del_role_resp.status_code,
                    204,
                    msg="Delete role response is not 204")
            del_user_resp = self.delete_user(create_user_resp)
            self.assertEqual(
                    del_user_resp,
                    204,
                    msg="Delete user expected response 204 received {0}".
                    format(del_user_resp))

    @attr('regression', type='positive')
    def test_39382_verify_atom_hopper_add_role_to_user_propagation(self):
        create_user_list = []
        username = rand_name("ccuseradmin")
        propagation_flag = True
        email = '{0}@{1}'.format("testbox", "mailtrust.com")
        domain_id = random_int(10000, 1000000000)
        sub_user = rand_name("ccsubuser")
        create_user_resp = self.admin_client.add_user(
                username=username,
                email=email,
                enabled=True,
                domainId=domain_id,
                password=self.password)
        auth_user_adm = self.public_client.authenticate_user_password(
                username,
                self.password)
        public_admin_client = self.provider.get_client()
        public_admin_client.token = auth_user_adm.entity.token.id

        create_sub_user_resp = public_admin_client.add_user(
                username=sub_user,
                email=email,
                enabled=True,
                domainId=domain_id,
                password=self.password)
        self.assertEqual(
                create_sub_user_resp.status_code,
                201,
                msg='Add user expected response 201 received {0}'.
                format(create_sub_user_resp.status_code))

        create_user_list.append(create_sub_user_resp)
        self.assertEqual(
                create_user_resp.status_code,
                201,
                msg='Add user expected response 201 received {0}'.
                format(create_user_resp.status_code))
        create_user_list.append(create_user_resp)

        name = rand_name("ccRole")
        description = 'static descr'
        add_role = self.admin_client.add_role(
                name=name,
                description=description,
                propagate=propagation_flag)
        self.assertEqual(
                add_role.status_code,
                201,
                msg="Response is not 201")

        add_role_to_user = self.admin_client.add_role_to_user(
                userId=create_user_resp.entity.id,
                roleId=add_role.entity.id)
        normal_response_codes = 200
        self.assertEqual(
                add_role_to_user.status_code,
                normal_response_codes,
                msg='Add role to user response expected {0} received {1}'.
                format(normal_response_codes,
                       add_role_to_user.status_code))

        for user_info in create_user_list:
            user_roles = self.admin_client.list_user_global_roles(
                    userId=user_info.entity.id)
            test_flag = False
            for userrole in user_roles.entity:
                if userrole.name == add_role.entity.name:
                    test_flag = True
            self.assertTrue(test_flag, msg="Role not added to user")

            search_attrib = 'resourceName'
            search_regex = user_info.entity.username
            results = self.atomhp.search_past_events_by_attribute(
                    attribute=search_attrib,
                    attribute_regex=search_regex)
            user_roles = results.product.roles.split()
            feed_role_flag = False
            for role in user_roles:
                if role == name:
                    feed_role_flag = True
            self.assertTrue(feed_role_flag, msg="Role not found in feed")

        del_role_resp = self.service_client.delete_role(
                roleId=add_role.entity.id)
        self.assertEqual(
                del_role_resp.status_code,
                204,
                msg="Delete role response is not 204")

        for userinfo in create_user_list:
            del_user_resp = self.delete_user(userinfo)
            self.assertEqual(
                    del_user_resp,
                    204,
                    msg="Delete user expected response 204 received {0}".
                    format(del_user_resp))

    @attr('regression', type='positive')
    def test_39382_verify_atom_hopper_delete_role_to_user_propagation(self):
        create_user_list = []
        username = rand_name("ccuseradmin")
        propagation_flag = True
        email = '{0}@{1}'.format("testbox", "mailtrust.com")
        domain_id = random_int(10000, 1000000000)
        sub_user = rand_name("ccsubuser")
        create_user_resp = self.admin_client.add_user(
                username=username,
                email=email,
                enabled=True,
                domainId=domain_id,
                password=self.password)
        auth_user_adm = self.public_client.authenticate_user_password(
                username,
                self.password)
        public_admin_client = self.provider.get_client()
        public_admin_client.token = auth_user_adm.entity.token.id

        create_sub_user_resp = public_admin_client.add_user(
                username=sub_user,
                email=email,
                enabled=True,
                domainId=domain_id,
                password=self.password)
        self.assertEqual(
                create_sub_user_resp.status_code,
                201,
                msg='Add user expected response 201 received {0}'.
                format(create_sub_user_resp.status_code))

        create_user_list.append(create_sub_user_resp)
        self.assertEqual(
                create_user_resp.status_code,
                201,
                msg='Add user expected response 201 received {0}'.
                format(create_user_resp.status_code))
        create_user_list.append(create_user_resp)

        name = rand_name("ccRole")
        description = 'static descr'
        add_role = self.admin_client.add_role(
                name=name,
                description=description,
                propagate=propagation_flag)
        self.assertEqual(
                add_role.status_code,
                201,
                msg="Response is not 201")

        add_role_to_user = self.admin_client.add_role_to_user(
                userId=create_user_resp.entity.id,
                roleId=add_role.entity.id)
        normal_response_codes = 200
        self.assertEqual(
                add_role_to_user.status_code,
                normal_response_codes,
                msg='Add role to user response expected {0} received {1}'.
                format(normal_response_codes,
                       add_role_to_user.status_code))

        for user_info in create_user_list:
            user_roles = self.admin_client.list_user_global_roles(
                    userId=user_info.entity.id)
            test_flag = False
            for userrole in user_roles.entity:
                if userrole.name == add_role.entity.name:
                    test_flag = True
            self.assertTrue(test_flag, msg="Role not added to user")

        delete_role_from_user = self.admin_client.delete_role_from_user(
                userId=create_user_resp.entity.id,
                roleId=add_role.entity.id)
        self.assertEqual(
                delete_role_from_user.status_code,
                204,
                msg="Response is not 204")

        for user_info in create_user_list:
            user_roles = self.admin_client.list_user_global_roles(
                    userId=user_info.entity.id)
            test_flag = True
            for userrole in user_roles.entity:
                if userrole.name == name:
                    test_flag = False
            self.assertTrue(test_flag, msg="Role deletion from user failed")

            search_attrib = 'resourceName'
            search_regex = user_info.entity.username
            results = self.atomhp.search_past_events_by_attribute(
                    search_attrib,
                    search_regex)
            user_roles = results.product.roles.split()
            feed_role_flag = False
            for role in user_roles:
                if role == name:
                    feed_role_flag = True
            self.assertFalse(feed_role_flag, msg="Role found in feed")

        del_role_resp = self.service_client.delete_role(
                roleId=add_role.entity.id)
        self.assertEqual(
                del_role_resp.status_code,
                204,
                msg="Delete role response is not 204")

        for userinfo in create_user_list:
            del_user_resp = self.delete_user(userinfo)
            self.assertEqual(
                    del_user_resp,
                    204,
                    msg="Delete user expected response 204 received {0}".
                    format(del_user_resp))

    @attr('regression', type='positive')
    def test_39383_verify_atom_hopper_delete_role_to_user(self):
        test_values = {self.service_client: rand_name("ccidentityadmin"),
                       self.admin_client: rand_name("ccuseradmin"),
                       self.public_client: rand_name("ccsubuser")}
        client_keys = test_values.keys()
        for client in client_keys:
            name = rand_name("Guest:Role")
            description = rand_name("Guest description ")
            propagation_flag = False
            username = test_values.get(client)
            email = '{0}@{1}'.format("testbox", "mailtrust.com")
            domain_id = random_int(10000, 1000000000)
            if client == self.service_client:
                create_user_resp = client.add_user(
                        username=username,
                        email=email,
                        enabled=True,
                        password=self.password)
            else:
                create_user_resp = client.add_user(
                        username=username,
                        email=email,
                        enabled=True,
                        domainId=domain_id,
                        password=self.password)

            add_role = self.admin_client.add_role(
                    name=name,
                    description=description,
                    propagate=propagation_flag)
            self.assertEqual(
                    add_role.status_code,
                    201,
                    msg="Response is not 201")

            add_role_to_user = self.admin_client.add_role_to_user(
                    userId=create_user_resp.entity.id,
                    roleId=add_role.entity.id)

            user_roles = self.admin_client.list_user_global_roles(
                    userId=create_user_resp.entity.id)
            test_flag = False
            for userrole in user_roles.entity:
                if userrole.name == add_role.entity.name:
                    test_flag = True

            #In api docs the add role to user response is 201 - pravin
            normal_response_codes = 200
            self.assertEqual(
                    add_role_to_user.status_code,
                    normal_response_codes,
                    msg='Add role to user response expected {0} received {1}'.
                    format(normal_response_codes,
                           add_role_to_user.status_code))

            delete_role_from_user = self.admin_client.delete_role_from_user(
                userId=create_user_resp.entity.id,
                roleId=add_role.entity.id)
            self.assertEqual(
                    delete_role_from_user.status_code,
                    204,
                    msg="Response is not 204")

            user_roles = client.list_user_global_roles(
                    userId=create_user_resp.entity.id)
            test_flag = True
            for userrole in user_roles.entity:
                if userrole.name == name:
                    test_flag = False
            self.assertTrue(test_flag, msg="Role deletion from user failed")

            search_attrib = 'resourceName'
            search_regex = username
            results = self.atomhp.search_past_events_by_attribute(
                    search_attrib,
                    search_regex)
            user_roles = results.product.roles.split()
            feed_role_flag = False
            for role in user_roles:
                if role == name:
                    feed_role_flag = True
            self.assertFalse(feed_role_flag, msg="Role found in feed")

            del_role_resp = self.service_client.delete_role(
                    roleId=add_role.entity.id)
            self.assertEqual(
                    del_role_resp.status_code,
                    204,
                    msg="Delete role response is not 204")
            del_user_resp = self.delete_user(create_user_resp)
            self.assertEqual(
                    del_user_resp,
                    204,
                    msg="Delete user expected response 204 received {0}".
                    format(del_user_resp))

    @attr('regression', type='positive')
    def test_39382_verify_atom_hopper_add_group(self):
        test_values = {self.service_client: rand_name("ccidentityadmin"),
                       self.admin_client: rand_name("ccuseradmin")}
        client_keys = test_values.keys()
        for client in client_keys:
            username_list = []
            create_user_list = []
            username = test_values.get(client)
            email = '{0}@{1}'.format("testbox", "mailtrust.com")
            domain_id = random_int(10000, 1000000000)
            if client == self.service_client:
                create_user_resp = client.add_user(
                        username=username,
                        email=email,
                        enabled=True,
                        password=self.password)
            else:
                sub_user = rand_name("ccsubuser")
                create_user_resp = client.add_user(
                        username=username,
                        email=email,
                        enabled=True,
                        domainId=domain_id,
                        password=self.password)
                auth_user_adm = self.public_client.authenticate_user_password(
                        username,
                        self.password)
                public_admin_client = self.provider.get_client()
                public_admin_client.token = auth_user_adm.entity.token.id

                create_sub_user_resp = public_admin_client.add_user(
                        username=sub_user,
                        email=email,
                        enabled=True,
                        domainId=domain_id,
                        password=self.password)
                self.assertEqual(
                        create_sub_user_resp.status_code,
                        201,
                        msg='Add user expected response 201 received {0}'.
                        format(create_sub_user_resp.status_code))
                username_list.append(sub_user)
                create_user_list.append(create_sub_user_resp)
            self.assertEqual(
                    create_user_resp.status_code,
                    201,
                    msg='Add user expected response 201 received {0}'.
                    format(create_user_resp.status_code))
            username_list.append(username)
            create_user_list.append(create_user_resp)

            name_group = rand_name("ccgroupname")
            description = 'static descr'
            add_group = self.admin_client.add_group(
                    name=name_group,
                    description=description)
            self.assertEqual(
                    add_group.status_code,
                    201,
                    msg="Response is not 201")

            user_addgroup = self.service_client.add_user_to_group(
                    userId=create_user_resp.entity.id,
                    groupId=add_group.entity.id)
            self.assertEqual(
                    user_addgroup.status_code,
                    204,
                    msg="Response is not 204")

            search_attrib = 'resourceName'
            for search_regex in username_list:
                results = self.atomhp.search_past_events_by_attribute(
                        attribute=search_attrib,
                        attribute_regex=search_regex)
                user_groups = results.product.groups.split()
                feed_group_flag = False
                for group in user_groups:
                    if group == name_group:
                        feed_group_flag = True
                self.assertTrue(feed_group_flag, msg="Group not found in feed")

                user_groups = self.service_client.list_groups_for_user(
                        userId=create_user_resp.entity.id)
                self.assertEqual(
                        user_groups.status_code,
                        200,
                        msg="Response is not 200")

                test_flag_bfrem = False
                for group in user_groups.entity:
                    if group.name == name_group:
                        test_flag_bfrem = True
                self.assertTrue(test_flag_bfrem, msg="Group wasn't founded")

            user_removegroup = self.admin_client.remove_user_from_group(
                        userId=create_user_resp.entity.id,
                        groupId=add_group.entity.id)
            self.assertEqual(
                    user_removegroup.status_code,
                    204,
                    msg="Response is not 204")

            delete_group = self.admin_client.delete_group(
                    groupId=add_group.entity.id)
            self.assertEqual(
                    delete_group.status_code,
                    204,
                    msg="Response is not 204")

            for userinfo in create_user_list:
                del_user_resp = self.delete_user(userinfo)
                self.assertEqual(
                        del_user_resp,
                        204,
                        msg="Delete user expected response 204 received {0}".
                        format(del_user_resp))

    @attr('regression', type='positive')
    def test_39382_verify_atom_hopper_delete_group(self):
        test_values = {self.service_client: rand_name("ccidentityadmin"),
                       self.admin_client: rand_name("ccuseradmin")}
        client_keys = test_values.keys()
        for client in client_keys:
            username_list = []
            create_user_list = []
            username = test_values.get(client)
            email = '{0}@{1}'.format("testbox", "mailtrust.com")
            domain_id = random_int(10000, 1000000000)
            if client == self.service_client:
                create_user_resp = client.add_user(
                        username=username,
                        email=email,
                        enabled=True,
                        password=self.password)
            else:
                sub_user = rand_name("ccsubuser")
                create_user_resp = client.add_user(
                        username=username,
                        email=email,
                        enabled=True,
                        domainId=domain_id,
                        password=self.password)

                auth_user_adm = self.public_client.authenticate_user_password(
                        username,
                        self.password)
                public_admin_client = self.provider.get_client()
                public_admin_client.token = auth_user_adm.entity.token.id

                create_sub_user_resp = public_admin_client.add_user(
                        username=sub_user,
                        email=email,
                        enabled=True,
                        domainId=domain_id,
                        password=self.password)
                self.assertEqual(
                        create_sub_user_resp.status_code,
                        201,
                        msg='Add user expected response 201 received {0}'.
                        format(create_sub_user_resp.status_code))
                username_list.append(sub_user)
                create_user_list.append(create_sub_user_resp)

            self.assertEqual(
                    create_user_resp.status_code,
                    201,
                    msg='Add user expected response 201 received {0}'.
                    format(create_user_resp.status_code))
            username_list.append(username)
            create_user_list.append(create_user_resp)

            name_group = rand_name("ccgroupname")
            description = 'static descr'
            add_group = self.admin_client.add_group(
                    name=name_group,
                    description=description)
            self.assertEqual(
                    add_group.status_code,
                    201,
                    msg="Response is not 201")

            user_addgroup = self.service_client.add_user_to_group(
                    userId=create_user_resp.entity.id,
                    groupId=add_group.entity.id)
            self.assertEqual(
                    user_addgroup.status_code,
                    204,
                    msg="Response is not 204")

            user_removegroup = self.admin_client.remove_user_from_group(
                    userId=create_user_resp.entity.id,
                    groupId=add_group.entity.id)
            self.assertEqual(
                    user_removegroup.status_code,
                    204,
                    msg="Response is not 204")

            search_attrib = 'resourceName'
            for search_regex in username_list:
                results = self.atomhp.search_past_events_by_attribute(
                        attribute=search_attrib,
                        attribute_regex=search_regex)
                if results.product.groups is None:
                    pass
                else:
                    user_groups = results.product.groups.split()
                    feed_group_flag = True
                    for group in user_groups:
                        if group == name_group:
                            feed_group_flag = False
                    self.assertTrue(feed_group_flag,
                                    msg="Group delete feed not found")

                    user_groups = self.service_client.list_groups_for_user(
                            userId=create_user_resp.entity.id)
                    self.assertEqual(
                            user_groups.status_code,
                            200,
                            msg="Response is not 200")

                    test_flag_bfrem = True
                    for group in user_groups.entity:
                        if group.name == name_group:
                            test_flag_bfrem = False
                    self.assertTrue(test_flag_bfrem, msg="Group founded")

            delete_group = self.admin_client.delete_group(
                    groupId=add_group.entity.id)
            self.assertEqual(
                    delete_group.status_code,
                    204,
                    msg="Response is not 204")

            for userinfo in create_user_list:
                del_user_resp = self.delete_user(userinfo)
                self.assertEqual(
                        del_user_resp,
                        204,
                        msg="Delete user expected response 204 received {0}".
                        format(del_user_resp))

    @attr('regression', type='positive')
    def test_39769_verify_atom_hopper_revoke_token_update_password(self):
        email = '{0}@{1}'.format("testbox", "mailtrust.com")
        password = "Gsubusrpass8"
        mod_password = 'ModGadmpass8'
        domain_id = random_int(10000, 1000000000)

        username_map = {self.service_client: rand_name("ccidenadmin"),
                        self.admin_client: rand_name("ccuseradmin"),
                        self.public_client: rand_name("ccsubuser")}
        client_keys = username_map.keys()
        for client in client_keys:
            username = username_map[client]
            if client == self.service_client:
                user_add_resp = client.add_user(
                        username=username,
                        email=email,
                        enabled=True,
                        password=password)
            else:
                user_add_resp = client.add_user(
                        username=username,
                        email=email,
                        enabled=True,
                        domainId=domain_id,
                        password=password)
            auth_resp = self.admin_client.authenticate_user_password(
                    username,
                    password)
            normal_response_codes = [200, 203]
            self.assertIn(
                    auth_resp.status_code,
                    normal_response_codes,
                    msg="Expected response {0} received response {1}".
                    format(normal_response_codes, auth_resp.status_code))

            user_client = self.provider.get_client()
            user_client.token = auth_resp.entity.token.id
            search_attrib = 'resourceName'
            search_regex = username
            user_create_feed = self.atomhp.search_past_events_by_attribute(
                    attribute=search_attrib,
                    attribute_regex=search_regex)
            self.assertIsNotNone(
                user_create_feed,
                msg='No Feed found in the Atom Hopper for the attributes')

            update_user_password = self.admin_client.update_user(
                    userId=user_add_resp.entity.id,
                    password=mod_password)
            self.assertEqual(
                    update_user_password.status_code,
                    200,
                    msg="Update user password should return {0} but "
                    "received {1}".format(200,
                                          update_user_password.status_code))

            search_attrib = 'resourceId'
            search_regex = user_client.token
            results = self.atomhp.search_past_events_by_attribute(
                    attribute=search_attrib,
                    attribute_regex=search_regex)
            self.assertEqual(
                    results.resourceId,
                    user_client.token,
                    msg='Revoke Token Feed not found in the Atom Hopper')
            self.assertEqual(
                    results.type,
                    'DELETE',
                    msg='Revoke Token Feed found was not of type Delete')

            del user_client.token
            del_user_resp = self.delete_user(user_add_resp)
            self.assertEqual(
                    del_user_resp,
                    204,
                    msg="Delete user expected response 204 received {0}".
                    format(del_user_resp))

    @attr('regression', type='positive')
    def test_39769_verify_atom_hopper_revoke_token_update_status(self):
        email = '{0}@{1}'.format("testbox", "mailtrust.com")
        password = "Gsubusrpass8"
        domain_id = random_int(10000, 1000000000)
        username_map = {self.service_client: rand_name("ccidenadmin"),
                        self.admin_client: rand_name("ccuseradmin"),
                        self.public_client: rand_name("ccsubuser")}
        client_keys = username_map.keys()

        for client in client_keys:
            username = username_map[client]
            if client == self.service_client:
                user_add_resp = client.add_user(
                        username=username,
                        email=email,
                        enabled=True,
                        password=password)
            else:
                user_add_resp = client.add_user(
                        username=username,
                        email=email,
                        enabled=True,
                        domainId=domain_id,
                        password=password)

            auth_resp = self.admin_client.authenticate_user_password(
                    username,
                    password)
            normal_response_codes = [200, 203]
            self.assertIn(
                    auth_resp.status_code,
                    normal_response_codes,
                    msg="Expected response {0} received response {1}".
                    format(normal_response_codes, auth_resp.status_code))

            user_client = self.provider.get_client()
            user_client.token = auth_resp.entity.token.id
            search_attrib = 'resourceName'
            search_regex = username
            user_create_feed = self.atomhp.search_past_events_by_attribute(
                    attribute=search_attrib,
                    attribute_regex=search_regex)
            self.assertIsNotNone(
                user_create_feed,
                msg='No Feed found in the Atom Hopper for the attributes')

            update_user_status = self.admin_client.update_user(
                userId=user_add_resp.entity.id,
                enabled=False)
            self.assertEqual(
                    update_user_status.status_code,
                    200,
                    msg="Update user status should return {0} but "
                    "received {1}".format(200, update_user_status.status_code))

            search_attrib = 'resourceId'
            search_regex = user_client.token
            results = self.atomhp.search_past_events_by_attribute(
                    attribute=search_attrib,
                    attribute_regex=search_regex)
            self.assertEqual(
                    results.resourceId,
                    user_client.token,
                    msg='Revoke Token Feed not found in the Atom Hopper')
            self.assertEqual(
                    results.type,
                    'DELETE',
                    msg='Revoke Token Feed found was not of type Delete')

            del user_client.token
            del_user_resp = self.delete_user(user_add_resp)
            self.assertEqual(
                    del_user_resp,
                    204,
                    msg="Delete user expected response 204 received {0}".
                    format(del_user_resp))

    @attr('regression', type='positive')
    def test_39769_verify_atom_hopper_revoke_token(self):
        email = '{0}@{1}'.format("testbox", "mailtrust.com")
        password = "Gsubusrpass8"
        domain_id = random_int(10000, 1000000000)
        username_map = {self.service_client: rand_name("ccidenadmin"),
                        self.admin_client: rand_name("ccuseradmin"),
                        self.public_client: rand_name("ccsubuser")}
        client_keys = username_map.keys()
        for client in client_keys:
            username = username_map[client]
            if client == self.service_client:
                user_add_resp = client.add_user(
                        username=username,
                        email=email,
                        enabled=True,
                        password=password)
            else:
                user_add_resp = client.add_user(
                        username=username,
                        email=email,
                        enabled=True,
                        domainId=domain_id,
                        password=password)

            auth_resp = self.admin_client.authenticate_user_password(
                    username,
                    password)
            normal_response_codes = [200, 203]
            self.assertIn(
                    auth_resp.status_code,
                    normal_response_codes,
                    msg="Expected response {0} received response {1}".
                    format(normal_response_codes, auth_resp.status_code))

            user_client = self.provider.get_client()
            user_client.token = auth_resp.entity.token.id
            search_attrib = 'resourceName'
            search_regex = username
            user_create_feed = self.atomhp.search_past_events_by_attribute(
                    attribute=search_attrib,
                    attribute_regex=search_regex)
            self.assertIsNotNone(
                user_create_feed,
                msg='No Feed found in the Atom Hopper for the attributes')
            self.admin_client.revoke_token(user_client.token)

            search_attrib = 'resourceId'
            search_regex = user_client.token
            results = self.atomhp.search_past_events_by_attribute(
                    attribute=search_attrib,
                    attribute_regex=search_regex)
            self.assertEqual(
                    results.resourceId,
                    user_client.token,
                    msg='Revoke Token Feed not found in the Atom Hopper')
            self.assertEqual(
                    results.type,
                    'DELETE',
                    msg='Revoke Token Feed found was not of type Delete')
            del_user_resp = self.delete_user(user_add_resp)
            self.assertEqual(
                    del_user_resp,
                    204,
                    msg="Delete user expected response 204 received {0}".
                    format(del_user_resp))
