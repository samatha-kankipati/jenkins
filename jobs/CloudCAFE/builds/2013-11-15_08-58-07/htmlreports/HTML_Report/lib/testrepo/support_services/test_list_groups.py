from ccengine.common.decorators import attr
from ccengine.common.tools.datagen import random_string
from testrepo.common.testfixtures.support_service import SupportServicesFixture


class ListGroupsTest(SupportServicesFixture):

    @attr(type='groups')
    def test_attributes_in_response_of_list_groups(self):
        """
        @summary: Verifies if a list group resp has the expected attributes.
        """
        groups = self.support_services_groups_provider.\
            support_services_groups_client.list_groups().entity
        self.assertNotEqual(len(groups), 0, msg="The group list is empty")
        for group in groups:
            self.assertIsNotNone(group.group_id, msg="Group Id is not getting"
                                 " assigned.")
            self.assertIsNotNone(group.group_name, msg="Group Name is not "
                                 "getting assigned.")

    @attr(type='groups')
    def test_attributes_in_response_of_group_detail(self):
        """
        @summary: Verifies if a group details resp has the expected attributes.
        """
        groups = self.support_services_groups_provider.\
            support_services_groups_client.list_groups().entity
        self.assertNotEqual(len(groups), 0, msg="The group list is empty")

        group = self.support_services_groups_provider.\
            support_services_groups_client.get_group(groups[0].group_id).entity

        self.assertIsNotNone(group[0].group_id, msg="Group Id is not getting"
                             " assigned.")
        self.assertIsNotNone(group[0].group_name, msg="Group Name is not "
                             "getting assigned.")
        self.assertIsNotNone(group[0].group_users, msg="Group Users are not "
                             "getting assigned.")

    @attr(type='groups')
    def test_fetch_groups_by_unknown_group_id(self):
        """
        @summary: Verifies group details call with unknown group id returns
        404 response.
        """
        unknown_group_id = 9999
        group = self.support_services_groups_provider.\
            support_services_groups_client.get_group(unknown_group_id)
        self.assertEqual(group.status_code, self.NOT_FOUND,
                         msg="The actual status code: {0} does not match "
                             "the expected code: {1}".format(
                                 group.status_code, self.NOT_FOUND))

    @attr(type='groups')
    def test_fetch_groups_by_invalid_group_id(self):
        """
        @summary: Verifies group details call with invalid group id returns
        400 response.
        """
        invalid_group_id = "abcd"
        group = self.support_services_groups_provider.\
            support_services_groups_client.get_group(invalid_group_id)
        self.assertEqual(group.status_code, self.BAD_REQ_CODE,
                         msg="The actual status code: {0} does not match "
                             "the expected code: {1}".format(
                                 group.status_code, self.BAD_REQ_CODE))

    @attr(type='groups')
    def test_list_groups_by_name(self):
        """
        @summary: Verifies a user is able to fetch the list of groups by
        group name.
        """
        name_exp = "rackspace"
        groups = self.support_services_groups_provider.\
            support_services_groups_client.list_groups(name=name_exp).entity

        self.assertNotEqual(len(groups), 0, msg="The group list is empty")

        for group in groups:
            self.assertNotEqual(group.group_name.lower().find(name_exp), -1,
                                msg="The group with id: {0} should not belong "
                                    " to the list as search criteria not met".
                                    format(group.group_id))

    @attr(type='groups')
    def test_fetch_list_of_groups_with_invalid_x_auth(self):
        """
        @summary: Verifies list group call with invalid X-Auth returns
        401 response.
        """
        self.auth_token = {"headers": {'X-Auth-Token': 'dasdasdasdsadas'}}
        groups = self.support_services_groups_provider.\
            support_services_groups_client.list_groups(
                requestslib_kwargs=self.auth_token
            )
        self.assertEqual(groups.status_code, self.UNAUTHORIZED_CODE,
                         msg="The actual status code: {0} does not match "
                             "the expected code: {1}".format(
                                 groups.status_code,
                                 self.UNAUTHORIZED_CODE))

    @attr(type='groups')
    def test_fetch_a_group_with_invalid_x_auth(self):
        """
        @summary: Verifies group details  call with invalid X-Auth returns
        401 response.
        """
        self.auth_token = {"headers": {'X-Auth-Token': 'asdsdasdasda'}}

        groups = self.support_services_groups_provider.\
            support_services_groups_client.list_groups().entity
        self.assertNotEqual(len(groups), 0, msg="The group list is empty")

        group = self.support_services_groups_provider.\
            support_services_groups_client.get_group(
                groups[0].group_id,
                requestslib_kwargs=self.auth_token
            )

        self.assertEqual(group.status_code, self.UNAUTHORIZED_CODE,
                         msg="The actual status code: {0} does not match "
                             "the expected code: {1}".format(
                                 group.status_code, self.UNAUTHORIZED_CODE))

    @attr(type='groups')
    def test_fetch_list_of_groups_with_no_x_auth_header(self):
        """
        @summary: Verifies list group call with no X-Auth returns
        401 response.
        """
        self.auth_token = {"headers": {}}
        groups = self.support_services_groups_provider.\
            support_services_groups_client.list_groups(
                requestslib_kwargs=self.auth_token
            )
        self.assertEqual(groups.status_code, self.UNAUTHORIZED_CODE,
                         msg="The actual status code: {0} does not match "
                             "the expected code: {1}".format(
                                 groups.status_code,
                                 self.UNAUTHORIZED_CODE))

    @attr(type='groups')
    def test_fetch_a_group_with_no_x_auth_header(self):
        """
        @summary: Verifies list group call with no X-Auth returns
        401 response.
        """
        self.auth_token = {"headers": {}}
        groups = self.support_services_groups_provider.\
            support_services_groups_client.list_groups().entity
        self.assertNotEqual(len(groups), 0, msg="The group list is empty")

        group = self.support_services_groups_provider.\
            support_services_groups_client.get_group(
                groups[0].group_id,
                requestslib_kwargs=self.auth_token
            )

        self.assertEqual(group.status_code, self.UNAUTHORIZED_CODE,
                         msg="The actual status code: {0} does not match "
                             "the expected code: {1}".format(
                                 group.status_code, self.UNAUTHORIZED_CODE))

    @attr(type='groups')
    def test_user_attributes_in_group_details(self):
        """
        @summary: Verifies group details call with for a group with assigned
        users, has the expected attributes.
        """
        group = self.support_services_groups_provider.\
            support_services_groups_client.get_group(
                self.group_with_users).entity

        self.assertIsNotNone(group[0].group_users, msg="Groups users are "
                             "not getting populated")

        for user in group[0].group_users:
            self.assertIsNotNone(user.user_id, msg="User ID is not "
                                 "getting populated.")
            self.assertIsNotNone(user.user_sso, msg="User SSO is not "
                                 "getting populated.")
            self.assertIsNotNone(user.user_email, msg="User Email is not "
                                 "getting populated.")
            self.assertIsNotNone(user.user_name, msg="User Name is not "
                                 "getting populated.")
            self.assertIsNotNone(user.user_tags, msg="User Tags is not "
                                 "getting populated.")

    @attr(type='groups')
    def test_user_badges_in_user_attributes_in_group_details(self):
        """
        @summary: Verifies group details call with for a group with assigned
        users, has the expected user badges attributes.
        """
        group = self.support_services_groups_provider.\
            support_services_groups_client.get_group(
                self.group_with_users).entity

        self.assertEqual(len(group[0].group_users), 0, msg="The user list "
                            "is not empty")

    @attr(type='groups')
    def test_list_groups_by_non_existing_name(self):
        """
        @summary: Verifies if a user is trying to fetch the list of groups
        by name with a non-existing name, empty list is returned.
        """
        name_exp = "THIS_GROUP_SHOULD_BE_PRESENT"
        groups = self.support_services_groups_provider.\
            support_services_groups_client.list_groups(name=name_exp).entity

        self.assertEqual(len(groups), 0, msg="The group list is not empty")

    @attr(type='groups')
    def test_user_values_in_group_details(self):
        """
        @summary: Verifies group details call for a group with assigned
        users, has the expected values.
        """
        group = self.support_services_groups_provider.\
            support_services_groups_client.get_group(
                self.group_with_users).entity

        self.assertEqual(group[0].group_users[0].user_id, self.user_id,
                         msg="The user id does not match")

        self.assertEqual(group[0].group_users[0].user_email, self.user_email,
                         msg="The user email does not match")

        self.assertEqual(group[0].group_users[0].user_name, self.user_name,
                         msg="The user name does not match")

        self.assertIsNotNone(group[0].group_users[0].user_tags,
                             msg="The user tags are not getting assigned")

        self.assertEqual(group[0].group_users[0].user_sso, self.user_sso,
                         msg="The user sso does not match")
