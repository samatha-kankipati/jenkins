from ccengine.common.tools.datagen import rand_name
from testrepo.common.testfixtures.identity.v2_0.identity \
    import IdentityAdminFixture
from ccengine.clients.identity.v2_0.rax_auth_api import IdentityClient
from ccengine.common.decorators import attr
from ccengine.domain.identity.v2_0.response.role import Role, Roles


class AdminRolesTest(IdentityAdminFixture):
    @classmethod
    def setUpClass(cls):
        super(AdminRolesTest, cls).setUpClass()
        cls.base_authentication = cls.public_client.authenticate_user_apikey(
            cls.config.identity_api.username,
            cls.config.identity_api.api_key)
        cls.user_admin_client = IdentityClient(
            url=cls.config.identity_api.authentication_endpoint,
            serialize_format=cls.config.misc.serializer,
            deserialize_format=cls.config.misc.deserializer,
            auth_token=cls.base_authentication.entity.token.id)

    @classmethod
    def tearDownClass(cls):
        pass

    @attr('regression', type='positive')
    def test_identity_admin_list_roles(self):
        """
        NOTE:>>> tenantId in the response is not in the docs.
        """
        roles_list = self.admin_client.list_roles()
        # serviceId, tenantId, and description may or may not be in the
        # response
        self.assertIsInstance(roles_list.entity,
                              Roles,
                              msg='Admin list roles expected a Roles obj '
                                  'received {0}'.format(
                                  type(roles_list.entity)))

        try:
            for role in roles_list.entity:
                self.assertIsInstance(role, Role,
                                      msg='Admin list roles expected a Role '
                                          'obj received {0}'.format(type(
                                          role)))

                self.assertIsNotNone(role.id,
                                     msg='Role obj expected a role ID '
                                         'received {0}'.format(role.id))

                self.assertIsNotNone(role.name,
                                     msg='Role obj expected a name received '
                                         '{0}'.format(role.name))
        except TypeError:
            self.assertIsNotNone(roles_list.entity,
                                 msg='roles list expected roles objects '
                                     'received {0}'.format(type(roles_list
                                 .entity)))

    @attr('regression', type='positive')
    def test_identity_admin_list_roles_limit(self):
        """
        NOTE:>>> tenantId in the response is not in the docs.
        """
        roles_list = self.admin_client.list_roles(limit=5)
        # serviceId, tenantId, and description may or may not be in the
        # response
        self.assertEqual(len(roles_list.entity), 5)

        try:
            for role in roles_list.entity:
                self.assertIsInstance(
                    role,
                    Role,
                    msg='Admin list user roles expected a Role obj '
                        'received {0}'.format(type(role)))

                self.assertIsNotNone(
                    role.id,
                    msg='Role obj expected a role ID received '
                        '{0}'.format(role.id))

                self.assertIsNotNone(
                    role.name,
                    msg='Role obj expected a name received {0}'.
                    format(role.name))
        except TypeError:
            self.assertIsNotNone(
                roles_list.entity,
                msg='roles list with limit expected roles objects '
                    'received {0}'.format(type(roles_list.entity)))

    @attr('regression', type='positive')
    def test_identity_admin_list_roles_marker(self):
        """
        NOTE:>>> tenantId in the response is not in the docs.
        """
        roles_list = self.admin_client.list_roles(marker=5)
        # serviceId, tenantId, and description may or may not be in the
        # response
        try:
            for role in roles_list.entity:
                self.assertIsInstance(
                    role,
                    Role,
                    msg='Admin list user roles expected a Role obj '
                        'received {0}'.format(type(role)))

                self.assertIsNotNone(
                    role.id,
                    msg='Role obj expected a role ID received '
                        '{0}'.format(role.id))

                self.assertIsNotNone(
                    role.name,
                    msg='Role obj expected a name received '
                        '{0}'.format(role.name))
        except TypeError:
            self.assertIsNotNone(
                roles_list.entity,
                msg='roles list with marker expected roles objects '
                    'received {0}'.format(type(roles_list.entity)))

    @attr('regression', type='positive')
    def test_identity_admin_list_roles_service_id(self):
        """
        NOTE:>>> tenantId in the response is not in the docs.
        """
        roles_list = self.admin_client.list_roles(service_id='a')
        # serviceId, tenantId, and description may or may not be in the
        # response
        try:
            for role in roles_list.entity:
                self.assertIsInstance(
                    role,
                    Role,
                    msg='Admin list user roles expected a Role obj '
                        'received {0}'.format(type(role)))

                self.assertIsNotNone(
                    role.id,
                    msg='Role obj expected a role ID received '
                        '{0}'.format(role.id))

                self.assertIsNotNone(
                    role.name,
                    msg='Role obj expected a name received '
                        '{0}'.format(role.name))
        except TypeError:
            self.assertIsNotNone(
                roles_list.entity,
                msg='roles list with service ID expected roles objects '
                    'received {0}'.format(type(roles_list.entity)))

    @attr('regression', type='positive')
    def test_identity_admin_list_roles_limit_marker(self):
        """
        NOTE:>>> tenantId in the response is not in the docs.
        """
        roles_list = self.admin_client.list_roles(limit=5, marker=5)
        # serviceId, tenantId, and description may or may not be in the
        # response
        try:
            for role in roles_list.entity:
                self.assertIsInstance(
                    role,
                    Role,
                    msg='Admin list user roles expected a Role obj '
                        'received {0}'.format(type(role)))

                self.assertIsNotNone(
                    role.id,
                    msg='Role obj expected a role ID received '
                        '{0}'.format(role.id))

                self.assertIsNotNone(
                    role.name,
                    msg='Role obj expected a name received '
                        '{0}'.format(role.name))
        except TypeError:
            self.assertIsNotNone(
                roles_list.entity,
                msg='roles list with limit and marker expected roles '
                    'objects received {0}'.format(type(roles_list.entity)))

    @attr('regression', type='positive')
    def test_identity_admin_list_roles_limit_marker_service_id(self):
        """
        NOTE:>>> tenantId in the response is not in the docs.
        """
        roles_list = self.admin_client.list_roles(
            limit=5,
            marker=5,
            service_id='a')
        # serviceId, tenantId, and description may or may not be in the
        # response
        try:
            for role in roles_list.entity:
                self.assertIsInstance(
                    role,
                    Role,
                    msg='Admin list user roles expected a Role obj '
                        'received {0}'.format(type(role)))

                self.assertIsNotNone(
                    role.id,
                    msg='Role obj expected a role ID received '
                        '{0}'.format(role.id))

                self.assertIsNotNone(
                    role.name,
                    msg='Role obj expected a name received '
                        '{0}'.format(role.name))
        except TypeError:
            self.assertIsNotNone(
                roles_list.entity,
                msg='roles list with limit, marker, and service id '
                    'expected roles objects received {0}'.
                format(type(roles_list.entity)))

    @attr('regression', type='positive')
    def test_identity_admin_add_role(self):
        name = rand_name("Guest:Role")
        description = rand_name("Guest description ")
        add_role = self.admin_client.add_role(
            name=name,
            description=description)
        # Delete role after test completion, even if any verification fails
        self.addCleanup(self.admin_client.delete_role,
                        roleId=add_role.entity.id)

        self.assertIsInstance(
            add_role.entity,
            Role,
            msg='Admin add role expected a Role obj received {0}'.
            format(type(add_role.entity)))

        self.assertIsNotNone(
            add_role.entity.id,
            msg='Role response obj expected an ID received {0}'.
            format(type(add_role.entity.id)))

        self.assertIsNotNone(
            add_role.entity.name,
            msg='Role response obj expected a name received {0}'.
            format(type(add_role.entity.name)))

        self.assertIsNotNone(
            add_role.entity.description,
            msg='Role response obj expected a description received {0}'.
            format(type(add_role.entity.description)))

        self.assertEqual(
            add_role.entity.name,
            name,
            msg='Role response obj expected name {0} received {1}'.
            format(name, add_role.entity.name))

        self.assertEqual(
            add_role.entity.description,
            description,
            msg='Role response obj expected name {0} received {1}'.
            format(name, add_role.entity.name))

        get_role = self.admin_client.get_role(
            roleId=add_role.entity.id)

        # possibly the try except in this test to this?
        # try: self.assertEqual(car.make, make)
        # except AssertionError, e: self.verificationErrors.append(str(e))

        try:
            self.assertEqual(
                add_role.entity.id,
                get_role.entity.id,
                msg='id of added role:{0} received role id {0}'.
                format(add_role.entity.id, get_role.entity.id))
        except TypeError:
            self.assertIsNotNone(
                get_role.entity,
                msg='get role with id of added role returned {0}'.
                format(type(get_role.entity)))

    @attr('regression', type='positive')
    def test_identity_admin_delete_role(self):
        name = rand_name("Guest:Role")
        description = rand_name("Guest description ")
        add_role = self.admin_client.add_role(
            name=name,
            description=description)

        self.assertIsInstance(
            add_role.entity,
            Role,
            msg='Admin add role expected a Role obj received {0}'.
            format(type(add_role.entity)))

        self.admin_client.delete_role(roleId=add_role.entity.id)

        get_role = self.admin_client.get_role(
            roleId=add_role.entity.id)

        self.assertIsNone(
            get_role.entity,
            msg='Admin get role on deleted role expected None received '
                '{0}'.format(type(add_role.entity)))

    @attr('regression', type='positive')
    def test_identity_admin_get_role(self):
        name = rand_name("Guest:Role")
        description = rand_name("Guest description ")
        list_roles = self.admin_client.add_role(
            name=name,
            description=description)
        get_role = self.admin_client.get_role(roleId=list_roles.entity.id)

        self.assertIsInstance(
            get_role.entity,
            Role,
            msg='Admin get role expected a Role obj received {0}'.
            format(type(get_role.entity)))

        self.assertIsNotNone(get_role.entity.id)

    @attr('regression', type='positive')
    def test_identity_admin_add_global_role_to_user(self):
        name = rand_name("Guest:Role")
        description = rand_name("Guest description ")
        add_role = self.admin_client.add_role(
            name=name,
            description=description)
        # Delete role after test completion, even if any verification fails
        self.addCleanup(self.admin_client.delete_role,
                        roleId=add_role.entity.id)
        self.assertIsInstance(
            add_role.entity,
            Role,
            msg='Admin add role expected a Role obj received {0}'.
            format(type(add_role.entity)))

        list_users = self.user_admin_client.list_users()
        username = list_users.entity[-1].username
        get_user = self.user_admin_client.get_user_by_name(name=username)
        user_id = get_user.entity.id
        self.admin_client.add_role_to_user(
            userId=user_id,
            roleId=add_role.entity.id)
        # Delete role from user after test completion, even if any
        # verification fails
        self.addCleanup(self.admin_client.delete_role_from_user,
                        userId=user_id,
                        roleId=add_role.entity.id)
        list_user_roles = self.admin_client.list_user_global_roles(
            userId=user_id)

        id_list = []
        id_list[:-1] = [role.id for role in list_user_roles.entity]

        self.assertIn(
            add_role.entity.id,
            id_list,
            msg='Global role {0} was not found in the users roles'.
            format(add_role.entity.id))

    @attr('regression', type='positive')
    def test_identity_admin_list_user_global_roles(self):
        list_users = self.user_admin_client.list_users()
        username = list_users.entity[-1].username
        get_user = self.user_admin_client.get_user_by_name(name=username)
        user_id = get_user.entity.id
        user_roles = self.admin_client.list_user_global_roles(userId=user_id)

        self.assertIsInstance(
            user_roles.entity,
            Roles,
            msg='Admin list user global roles expected a Roles obj '
                'received {0}'.format(type(user_roles.entity)))

        try:
            for role in user_roles.entity:
                self.assertIsInstance(
                    role,
                    Role,
                    msg='Admin list user global roles expected a Role obj '
                        'received {0}'.format(type(role)))

                self.assertIsNotNone(
                    role.id,
                    msg='Role obj expected a role ID received '
                        '{0}'.format(role.id))

                self.assertIsNotNone(
                    role.name,
                    msg='Role obj expected a name received '
                        '{0}'.format(role.name))
        except TypeError:
            self.assertIsNotNone(
                user_roles.entity,
                msg='user roles list expected roles objects received {0}'.
                format(type(user_roles.entity)))

    @attr('regression', type='positive')
    def test_identity_admin_delete_global_role_from_user(self):
        name = rand_name("Guest:Role")
        description = rand_name("Guest description ")
        add_role = self.admin_client.add_role(
            name=name,
            description=description)
        # Delete role after test completion, even if any verification fails
        self.addCleanup(self.admin_client.delete_role,
                        roleId=add_role.entity.id)
        self.assertIsInstance(
            add_role.entity,
            Role,
            msg='Admin add role expected a Role obj received {0}'.
            format(type(add_role.entity)))

        list_users = self.user_admin_client.list_users()
        username = list_users.entity[-1].username
        get_user = self.user_admin_client.get_user_by_name(name=username)
        user_id = get_user.entity.id
        self.admin_client.add_role_to_user(
            userId=user_id,
            roleId=add_role.entity.id)
        # Delete role from user after test completion, even if any
        # verification fails
        self.addCleanup(self.admin_client.delete_role_from_user,
                        userId=user_id,
                        roleId=add_role.entity.id)
        list_user_roles = self.admin_client.list_user_global_roles(
            userId=user_id)

        id_list = []
        name_list = []
        id_list[:-1] = [role.id for role in list_user_roles.entity]
        name_list[:-1] = [role.name for role in list_user_roles.entity]
        self.assertIn(add_role.entity.id,
                      id_list,
                      msg='Global role id {0} was not found in the users '
                          'roles'.format(add_role.entity.id))
        self.assertIn(add_role.entity.name,
                      name_list,
                      msg='Global role name {0} was not found in the users '
                          'roles'.format(add_role.entity.name))
        self.admin_client.delete_role_from_user(userId=user_id,
                                                roleId=add_role.entity.id)

        list_user_roles = self.admin_client.list_user_global_roles(
            userId=user_id)
        id_list = []
        name_list = []
        id_list[:-1] = [role.id for role in list_user_roles.entity]
        name_list[:-1] = [role.name for role in list_user_roles.entity]
        self.assertNotIn(add_role.entity.id,
                         id_list,
                         msg='Global role id {0} was found in the users '
                             'roles after delete'.format(add_role.entity.id))
        self.assertNotIn(add_role.entity.name,
                         name_list,
                         msg='Global role name {0} was found in the users '
                             'roles after delete'.format(add_role.entity.name))