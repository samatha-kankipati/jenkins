from ccengine.common.decorators import attr
from testrepo.common.testfixtures.support_service import SupportServicesFixture


class ListSupportAccountRackerTest(SupportServicesFixture):

    @attr(type='support_accounts_racker')
    def test_list_support_account_has_expected_account_badges_attributes(self):
        """
        @summary: Verify that support account has account_bages attribute and
        account badges has expected badges attributes.
        """
        support_account = self.support_services_groups_provider.\
            support_contact_client.list_support_account_details(
                self.account_number).entity
        self.assertTrue(hasattr(support_account, "account_badges"),
                        msg="Support Accoount does not contain"
                            " account badges")
        for account_badge in support_account.account_badges:
            self.assertIsNotNone(account_badge.badge_name,
                                 msg="The badge name value is not getting "
                                     "assigned.")
            self.assertIsNotNone(account_badge.badge_description,
                                 msg="The badge description value is not "
                                     "getting assigned.")
            self.assertIsNotNone(account_badge.badge_url,
                                 msg="The badge url value is not getting "
                                     "assigned.")

    @attr(type='support_accounts_racker')
    def test_list_support_account_has_expected_service_level_attribute(self):
        """
        @summary: Verify that support account has expected service level
        attribute.
        """
        support_account = self.support_services_groups_provider.\
            support_contact_client.list_support_account_details(
                self.account_number).entity
        self.assertEqual(support_account.account_service_level,
                         self.service_level,
                         msg="Support Accoount does not contain"
                             " expected service level: {0}".
                         format(self.service_level))

    @attr(type='support_accounts_racker')
    def test_list_support_account_has_expected_role_attributes(self):
        """
        @summary: Verify that support account has expected roles attributes.
        """
        support_account = self.support_services_groups_provider.\
            support_contact_client.list_support_account_details(
                self.account_number).entity
        self.assertTrue(hasattr(support_account, "account_roles"),
                        msg="Support Accoount does not contain Roles details.")

        for role in support_account.account_roles:
            self.assertIsNotNone(role.role,
                                 msg="The Role value is not getting assigned.")
            self.assertIsNotNone(role.user_id,
                                 msg="The User ID value is not getting "
                                     "assigned.")
            self.assertIsNotNone(role.user_sso,
                                 msg="The User SSO is not getting assigned.")
            self.assertIsNotNone(role.user_name,
                                 msg="The User Name is not getting assigned.")
            self.assertIsNotNone(role.user_email,
                                 msg="The User Email is not getting "
                                     "assigned.")

    @attr(type='support_accounts_racker')
    def test_list_support_account_has_expected_support_teams_attributes(self):
        """
        @summary: Verify that the support account has a team attribute, which
        itself has a support team with expected attributes.
        """
        support_account = self.support_services_groups_provider.\
            support_contact_client.list_support_account_details(
                self.account_number).entity
        self.assertTrue(hasattr(support_account, "account_teams"),
                        msg="Support Accoount does not contain Teams details.")

        for team in support_account.account_teams:
            if team.team_type == "support":
                self.assertIsNotNone(team.team_id,
                                     msg="Team ID is not getting assigned")
                self.assertIsNotNone(team.team_name,
                                     msg="Team Name is not getting assigned")
                self.assertIsNotNone(team.team_flags,
                                     msg="Team flags are not getting assigned")
                self.assertIsNotNone(team.team_description,
                                     msg="Team description are not getting "
                                         "assigned")

    @attr(type='support_accounts_racker')
    def test_list_support_account_has_expected_revenue_teams_attributes(self):
        """
        @summary: Verify that the support account has a team attribute, which
        itself has a revenue team with expected attributes.
        """
        revenue_account = self.support_services_groups_provider.\
            support_contact_client.list_support_account_details(
                self.account_number).entity

        for team in revenue_account.account_teams:
            if team.team_type == "revenue":
                self.assertIsNotNone(team.team_id,
                                     msg="Team ID is not getting assigned")
                self.assertIsNotNone(team.team_name,
                                     msg="Team Name is not getting assigned")
                self.assertIsNotNone(team.team_business_unit,
                                     msg="Team business unit is not assigned")
                self.assertIsNotNone(team.team_segment,
                                     msg="Team segment is not getting "
                                         "assigned")
                self.assertIsNotNone(team.team_description,
                                     msg="Team description are not getting "
                                         "assigned")

    @attr(type='support_accounts_racker')
    def test_racker_invalid_x_auth_header_gives_401(self):
        """
        @summary: Verify that racker gets a 401 response from the API, if the
        request is made with invalid X-Auth-Token.
        """
        self.auth_token = {"headers": {"X-Auth-Token": "abcd"}}
        support_account = self.support_services_groups_provider.\
            support_contact_client.list_support_account_details(
                self.account_number, requestslib_kwargs=self.auth_token)

        self.assertEqual(support_account.status_code,
                         self.UNAUTHORIZED_CODE,
                         msg="The actual status code: {0} does not match "
                             "the expected code: {1}".format(
                         support_account.status_code,
                         self.UNAUTHORIZED_CODE))

    @attr(type='support_accounts_racker')
    def test_racker_without_x_auth_header_gives_401(self):
        """
        @summary: Verify that racker gets a 401 response from the API, if the
        request is made with no X-Auth-Token.
        """
        self.auth_token = {"headers": {}}
        support_account = self.support_services_groups_provider.\
            support_contact_client.list_support_account_details(
                self.account_number, requestslib_kwargs=self.auth_token)

        self.assertEqual(support_account.status_code,
                         self.UNAUTHORIZED_CODE,
                         msg="The actual status code: {0} does not match "
                             "the expected code: {1}".format(
                         support_account.status_code,
                         self.UNAUTHORIZED_CODE))

    @attr(type='support_accounts_racker')
    def test_racker_list_support_account_for_invalid_account_gives_400(self):
        """
        @summary: Verify that racker gets a 400 response from the API, if the
        request is made with invalid account ID.
        """
        unknown_account = "abcd"
        support_account = self.support_services_groups_provider.\
            support_contact_client.list_support_account_details(
                unknown_account)

        self.assertEqual(support_account.status_code, self.BAD_REQ_CODE,
                         msg="The actual status code: {0} does not match "
                             "the expected code: {1}".format(
                         support_account.status_code, self.BAD_REQ_CODE))

    @attr(type='support_accounts_racker')
    def test_racker_list_support_accounts_for_unknown_account_gives_404(self):
        """
        @summary: Verify that racker gets a 401 response from the API, if the
        request is made with unknown account ID.
        """
        unknown_account = "999999999"
        support_contact = self.support_services_groups_provider.\
            support_contact_client.list_support_account_details(
                unknown_account)

        self.assertEqual(support_contact.status_code, self.NOT_FOUND,
                         msg="The actual status code: {0} does not match "
                             "the expected code: {1}".format(
                         support_contact.status_code, self.NOT_FOUND))

    @attr(type='support_accounts_racker')
    def test_get_roles_for_an_account(self):
        """
        @summary: Verify that racker is able to fetch all the roles for an
        account.
        """
        support_account_roles = self.support_services_groups_provider.\
            support_contact_client.get_roles_for_an_account(
                self.account_number).entity

        for role in support_account_roles:
            self.assertIsNotNone(role.role,
                                 msg="The Role value is not getting assigned.")
            self.assertIsNotNone(role.user_id,
                                 msg="The User ID value is not getting "
                                     "assigned.")
            self.assertIsNotNone(role.user_sso,
                                 msg="The User SSO is not getting assigned.")
            self.assertIsNotNone(role.user_name,
                                 msg="The User Name is not getting assigned.")

    @attr(type='support_accounts_racker')
    def test_racker_can_get_linked_account_id_from_account_details(self):
        """
        @summary: Verify that racker is able to get the linked account ID from
        account details call.
        """
        support_account = self.support_services_groups_provider.\
            support_contact_client.list_support_account_details(
                self.account_number).entity

        self.assertEquals(support_account.account_linked_account,
                          self.linked_account,
                          msg="The linked account is not correctly populated")

    @attr(type='support_accounts_racker')
    def test_racker_can_get_account_name_from_account_details(self):
        """
        @summary: Verify that racker is able to get the account name from
        account details call.
        """
        support_account = self.support_services_groups_provider.\
            support_contact_client.list_support_account_details(
                self.account_number).entity

        self.assertEquals(support_account.account_name, self.account_name,
                          msg="The account name is not correctly populated")

    @attr(type='support_accounts_racker')
    def test_racker_can_get_account_tags_from_account_details(self):
        """
        @summary: Verify that racker is able to get the account tags from
        account details call.
        """
        support_account = self.support_services_groups_provider.\
            support_contact_client.list_support_account_details(
                self.account_number).entity

        self.assertIsNotNone(support_account.account_tags,
                             msg="The account_tags are not showing up.")

    @attr(type='support_accounts_racker')
    def test_racker_can_get_support_team_flags_from_account_details(self):
        """
        @summary: Verify that racker is able to get the support team flags from
        account details call.
        """
        support_account = self.support_services_groups_provider.\
            support_contact_client.list_support_account_details(
                self.account_number).entity

        for team in support_account.account_teams:
            if team.team_type == "support":
                self.assertIsNotNone(team.team_flags,
                                     msg="The team_flags are not showing up.")

    @attr(type='support_accounts_racker')
    def test_if_customer_tries_to_fetch_roles_for_an_account_he_gets_401(self):
        """
        @summary: Verify that if customer tries to fetch all the roles for an
        account, he gets a 403 - Forbidden.
        """
        support_account_roles = self.support_services_cutomer_provider.\
            support_contact_client.get_roles_for_an_account(
                self.account_number)

        self.assertEqual(support_account_roles.status_code,
                         self.FORBIDDEN,
                         msg="The actual status code: {0} does not match "
                             "the expected code: {1}".format(
                             support_account_roles.status_code,
                             self.FORBIDDEN))
