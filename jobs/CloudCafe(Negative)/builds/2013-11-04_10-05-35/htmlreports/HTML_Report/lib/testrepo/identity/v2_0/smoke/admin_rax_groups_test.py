from ccengine.common.tools.datagen import rand_name
from testrepo.common.testfixtures.identity.v2_0.identity \
    import IdentityAdminFixture
from ccengine.common.decorators import attr


class AdminGroupsTest(IdentityAdminFixture):
    @classmethod
    def setUpClass(cls):
        """
        Set up test bed for all the test in AdminGroupsTest
        """
        super(AdminGroupsTest, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        """
        Clean up test bed
        """
        pass

    @attr('smoke', type='positive')
    def test_get_groups(self):
        get_groups = self.admin_client.get_groups()
        self.assertEqual(get_groups.status_code, 200,
                         msg="Response is not 200")
        self.assertTrue(get_groups.entity[0].id is not None,
                        msg="ID is present")
        self.assertGreaterEqual(len(get_groups.entity), 0,
                                msg="There is at least one child tenant")

    @attr('smoke', type='positive')
    def test_get_groups_parameters(self):
        get_groups = self.admin_client.get_groups(marker=2, limit=5)
        self.assertEqual(get_groups.status_code, 200,
                         msg="Response is not 200")
        self.assertTrue(get_groups.entity[0].id is not None,
                        msg="ID is present")
        self.assertGreaterEqual(len(get_groups.entity), 0,
                                msg="There is at least one child tenant")

    @attr('smoke', type='positive')
    def test_get_group_details(self):
        get_groups = self.admin_client.get_groups()
        self.assertEqual(get_groups.status_code, 200,
                         msg="Response is not 200")
        get_group = self.admin_client.get_group(get_groups.entity[0].id)
        self.assertEqual(get_group.status_code, 200, msg="Response is not 200")
        self.assertEqual(get_group.entity.id, get_groups.entity[0].id,
                         msg="Expected id is %s but received %s" %
                             (get_groups.entity[0].id, get_group.entity.id))
        self.assertTrue(get_group.entity.name is not None,
                        msg="Name is present")

    @attr('smoke', type='positive')
    def test_add_group(self):
        name = rand_name("ccgroupname")
        description = 'static descr'
        add_group = self.admin_client.add_group(name=name,
                                                description=description)
        self.assertEqual(add_group.status_code, 201, msg="Response is not 201")
        # Delete Group after test completion
        self.addCleanup(self.admin_client.delete_group,
                        groupId=add_group.entity.id)
        self.assertEqual(add_group.entity.name, name,
                         msg="Expected username is %s but received %s" %
                             (name, add_group.entity.name))
        self.assertEqual(add_group.entity.description, description,
                         msg="Expected password is %s but received %s" %
                             (description, add_group.entity.description))

    @attr('smoke', type='positive')
    def test_delete_group(self):
        name = rand_name("ccgroupname")
        description = 'static descr'
        add_group = self.admin_client.add_group(name=name,
                                                description=description)
        self.assertEqual(add_group.status_code, 201,
                         msg="Response is not 201")
        delete_group = self.admin_client.delete_group(
            groupId=add_group.entity.id)
        self.assertEqual(delete_group.status_code, 204,
                         msg="Response is not 204")
        get_group = self.admin_client.get_group(add_group.entity.id)
        self.assertEqual(get_group.status_code, 404,
                         msg="Response is not 404")
        self.assertTrue("not found" in get_group.content,
                        msg="Expecting 'Fault state- Should be no group' "
                            "received %s" % get_group.content)

    @attr('smoke', type='positive')
    def test_update_group(self):
        name = rand_name("ccgroupname")
        description = 'static descr'
        update_descr = 'updated descr'
        add_group = self.admin_client.add_group(name=name,
                                                description=description)
        self.assertEqual(add_group.status_code, 201,
                         msg="Response is not 201")
        # Delete Group after test completion
        self.addCleanup(self.admin_client.delete_group,
                        groupId=add_group.entity.id)
        update_group = self.admin_client.update_group(
            groupId=add_group.entity.id,
            name=name,
            description=update_descr)
        self.assertEqual(update_group.status_code, 200,
                         msg="Response is not 200")
        self.assertEqual(update_group.entity.description, update_descr,
                         msg="Expected password is %s but received %s" %
                             (update_descr, update_group.entity.description))

    @attr('smoke', type='positive')
    def test_list_group_for_user(self):
        list_users = self.public_client.list_users()
        user_id = list_users.entity[0].id
        user_groups = self.admin_client.list_groups_for_user(userId=user_id)
        self.assertEqual(user_groups.status_code, 200,
                         msg="Response is not 200")
        self.assertTrue(user_groups.entity[0].id is not None,
                        msg="Enabled field present")
        self.assertTrue(user_groups.entity[0].description is not None,
                        msg="Enabled field present")

    @attr('smoke', type='positive')
    def test_add_user_to_group(self):
        list_users = self.public_client.list_users()
        user_id = list_users.entity[0].id
        name = rand_name("ccgroupname")
        description = 'static descr'
        add_group = self.admin_client.add_group(name=name,
                                                description=description)
        self.assertEqual(add_group.status_code, 201,
                         msg="Response is not 201")
        # Delete Group after test completion
        self.addCleanup(self.admin_client.delete_group,
                        groupId=add_group.entity.id)
        user_addgroup = self.admin_client.add_user_to_group(
            userId=user_id,
            groupId=add_group.entity.id)
        self.assertEqual(user_addgroup.status_code, 204,
                         msg="Response is not 204")
        # Remove user from Group after test completion
        self.addCleanup(self.admin_client.remove_user_from_group,
                        userId=user_id,
                        groupId=add_group.entity.id)

    @attr('smoke', type='positive')
    def test_get_user_for_group(self):
        normal_response_codes = [200, 203]
        list_users = self.public_client.list_users()
        user_id = list_users.entity[0].id
        get_user = self.public_client.get_user_by_id(userId=user_id)
        self.assertIn(get_user.status_code, normal_response_codes,
                      msg='Admin get user by id expected %s recieved %s' %
                          (normal_response_codes, get_user.status_code))
        name = rand_name("ccgroupname")
        description = 'static descr'
        add_group = self.admin_client.add_group(name=name,
                                                description=description)
        self.assertEqual(add_group.status_code, 201,
                         msg="Response is not 201")
        # Delete Group after test completion
        self.addCleanup(self.admin_client.delete_group,
                        groupId=add_group.entity.id)

        user_addgroup = self.admin_client.add_user_to_group(
            userId=user_id,
            groupId=add_group.entity.id)
        self.assertEqual(user_addgroup.status_code, 204,
                         msg="Response is not 204")
        # Remove user from Group after test completion
        self.addCleanup(self.admin_client.remove_user_from_group,
                        userId=user_id,
                        groupId=add_group.entity.id)

        group_getusers = self.admin_client.get_users_for_group(
            groupId=add_group.entity.id)
        self.assertEqual(group_getusers.status_code, 200,
                         msg="Response is not 200")
        usernames = [user.username for user in group_getusers.entity]
        self.assertIn(get_user.entity.username, usernames,
                      msg="Expected username %s in list but received %s" %
                          (name, usernames))

    @attr('smoke', type='positive')
    def test_get_user_for_group_limit(self):
        normal_response_codes = [200, 203]
        list_users = self.public_client.list_users()
        user_id = list_users.entity[0].id
        get_user = self.public_client.get_user_by_id(userId=user_id)
        self.assertIn(get_user.status_code, normal_response_codes,
                      msg='Admin get user by id expected %s recieved %s' %
                          (normal_response_codes, get_user.status_code))
        name = rand_name("ccgroupname")
        description = 'static descr'
        add_group = self.admin_client.add_group(name=name,
                                                description=description)
        self.assertEqual(add_group.status_code, 201,
                         msg="Response is not 201")
        # Delete Group after test completion
        self.addCleanup(self.admin_client.delete_group,
                        groupId=add_group.entity.id)

        user_addgroup = self.admin_client.add_user_to_group(
            userId=user_id,
            groupId=add_group.entity.id)
        self.assertEqual(user_addgroup.status_code, 204,
                         msg="Response is not 204")
        # Remove user from Group after test completion
        self.addCleanup(self.admin_client.remove_user_from_group,
                        userId=user_id,
                        groupId=add_group.entity.id)

        group_getusers = self.admin_client.get_users_for_group(
            groupId=add_group.entity.id,
            limit=10)
        self.assertEqual(group_getusers.status_code, 200,
                         msg="Response is not 200")

    @attr('smoke', type='positive')
    def test_get_user_for_group_marker(self):
        normal_response_codes = [200, 203]
        list_users = self.public_client.list_users()
        user_id = list_users.entity[0].id
        get_user = self.public_client.get_user_by_id(userId=user_id)
        self.assertIn(get_user.status_code, normal_response_codes,
                      msg='Admin get user by id expected %s recieved %s' %
                          (normal_response_codes, get_user.status_code))
        name = rand_name("ccgroupname")
        description = 'static descr'
        add_group = self.admin_client.add_group(name=name,
                                                description=description)
        self.assertEqual(add_group.status_code, 201,
                         msg="Response is not 201")
        # Delete Group after test completion
        self.addCleanup(self.admin_client.delete_group,
                        groupId=add_group.entity.id)

        user_addgroup = self.admin_client.add_user_to_group(
            userId=user_id,
            groupId=add_group.entity.id)
        self.assertEqual(user_addgroup.status_code, 204,
                         msg="Response is not 204")
        # Remove user from Group after test completion
        self.addCleanup(self.admin_client.remove_user_from_group,
                        userId=user_id,
                        groupId=add_group.entity.id)

        group_getusers = self.admin_client.get_users_for_group(
            groupId=add_group.entity.id,
            marker=2)
        self.assertEqual(group_getusers.status_code, 200,
                         msg="Response is not 200")

    @attr('smoke', type='positive')
    def test_get_user_for_group_limit_marker(self):
        normal_response_codes = [200, 203]
        list_users = self.public_client.list_users()
        user_id = list_users.entity[0].id
        get_user = self.public_client.get_user_by_id(userId=user_id)
        self.assertIn(get_user.status_code, normal_response_codes,
                      msg='Admin get user by id expected %s recieved %s' %
                          (normal_response_codes, get_user.status_code))
        name = rand_name("ccgroupname")
        description = 'static descr'
        add_group = self.admin_client.add_group(name=name,
                                                description=description)
        self.assertEqual(add_group.status_code, 201,
                         msg="Response is not 201")
        # Delete Group after test completion
        self.addCleanup(self.admin_client.delete_group,
                        groupId=add_group.entity.id)

        user_addgroup = self.admin_client.add_user_to_group(
            userId=user_id,
            groupId=add_group.entity.id)
        self.assertEqual(user_addgroup.status_code, 204,
                         msg="Response is not 204")
        # Remove user from Group after test completion
        self.addCleanup(self.admin_client.remove_user_from_group,
                        userId=user_id,
                        groupId=add_group.entity.id)

        group_getusers = self.admin_client.get_users_for_group(
            groupId=add_group.entity.id,
            limit=10,
            marker=2)
        self.assertEqual(group_getusers.status_code, 200,
                         msg="Response is not 200")
