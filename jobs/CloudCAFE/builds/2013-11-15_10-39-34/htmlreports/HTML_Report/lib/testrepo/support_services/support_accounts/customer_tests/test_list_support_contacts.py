from ccengine.common.decorators import attr
from testrepo.common.testfixtures.support_service import SupportServicesFixture


class ListSupportContactsTest(SupportServicesFixture):

    @attr(type='support_accounts')
    def test_list_support_account_has_expected_chat_team_attributes(self):
        """
        @summary: Verify that list support team has expected chat teams
        attribute.
        """
        support_contact = self.support_services_cutomer_provider.\
            support_contact_client.list_support_account_details(
                self.account_number).entity
        for chat_team in support_contact.chat_teams:
            self.assertIsNotNone(chat_team.team_id, msg="Team ID is not "
                                 "getting assigned.")
            self.assertIsNotNone(chat_team.team_name, msg="Team Name is not "
                                 "getting assigned.")
            self.assertIsNotNone(chat_team.team_flags, msg="Team Flags not "
                                 "getting assigned.")
            self.assertIsNotNone(chat_team.chat_team_name, msg="ChatTeam Name "
                                 "is not getting assigned.")
            self.assertIsNotNone(chat_team.chat_team_html, msg="ChatTeam HTML "
                                 "is not getting assigned.")
            self.assertIsNotNone(chat_team.chat_team_url, msg="ChatTeam URL "
                                 "is not getting assigned.")

    @attr(type='support_accounts')
    def test_list_support_account_has_expected_phone_team_attributes(self):
        """
        @summary: Verify that list support team has expected phone team
        attribute.
        """
        support_contact = self.support_services_cutomer_provider.\
            support_contact_client.list_support_account_details(
                self.account_number).entity

        for phone_team in support_contact.phone_teams:
            self.assertIsNotNone(phone_team.team_id, msg="Team ID is not "
                                 "getting assigned.")
            self.assertIsNotNone(phone_team.team_name, msg="TeamName is not "
                                 "getting assigned.")
            self.assertIsNotNone(phone_team.team_flags, msg="Team Flags not "
                                 "getting assigned.")
            self.assertIsNotNone(phone_team.phone_team_name,
                                 msg="PhoneTeam Name is not "
                                 "getting assigned.")
            self.assertIsNotNone(phone_team.phone_numbers, msg="PhoneNumber "
                                 "is not getting assigned.")

    @attr(type='support_accounts1')
    def test_list_support_account_has_expected_phone_number_attributes(self):
        """
        @summary: Verify that list support team has expected phone number
        attributes inside phone team.
        """
        support_contact = self.support_services_cutomer_provider.\
            support_contact_client.list_support_account_details(
                self.account_number).entity
        for phone_number in support_contact.phone_teams[0].phone_numbers:
            self.assertIsNotNone(phone_number.country_code, msg="Country code "
                                 "is not getting assigned.")
            self.assertIsNotNone(phone_number.phone_number, msg="Phone number "
                                 "is not getting assigned.")
            self.assertIsNotNone(phone_number.phone_number_flags,
                                 msg="Phonenumber flags not getting assigned.")

    @attr(type='support_accounts')
    def test_chat_teams_shows_up_in_list_support_accounts(self):
        """
        @summary: Verify that chat teams details shows up in list support
        team
        """
        support_contact = self.support_services_cutomer_provider.\
            support_contact_client.list_support_account_details(
                self.account_number).entity
        self.assertNotEqual(len(support_contact.chat_teams), 0,
                            msg="The chat teams are not showing up for the "
                                "account: {0}".format(self.account_number))

    @attr(type='wait_till_db_access')
    def test_phone_numbers_shows_up_in_list_support_accounts(self):
        """
        @summary: Verify that phone number details shows up in list support
        team
        """
        support_contact = self.support_services_cutomer_provider.\
            support_contact_client.list_support_account_details(
                self.account_number).entity
        self.assertNotEqual(len(support_contact.phone_teams), 0,
                            msg="The phone teams are not showing up for the "
                                "account: {0}".format(self.account_number))

    @attr(type='support_accounts')
    def test_list_support_accounts_for_unknown_account_gives_403(self):
        """
        @summary: Verify that list support account with unknown account ID
        gives 404 Not Found
        """
        unknown_account = "999999999"
        support_contact = self.support_services_cutomer_provider.\
            support_contact_client.list_support_account_details(
                unknown_account)

        self.assertEqual(support_contact.status_code, self.FORBIDDEN,
                         msg="The actual status code: {0} does not match "
                             "the expected code: {1}".format(
                         support_contact.status_code, self.FORBIDDEN))

    @attr(type='support_accounts')
    def test_list_support_account_for_invalid_account_gives_403(self):
        """
        @summary: Verify that list support account with invalid account ID
        gives 400 Bad Request
        """
        invalid_account = "abcd"
        support_contact = self.support_services_cutomer_provider.\
            support_contact_client.list_support_account_details(
                invalid_account)

        self.assertEqual(support_contact.status_code, self.FORBIDDEN,
                         msg="The actual status code: {0} does not match "
                             "the expected code: {1}".format(
                         support_contact.status_code, self.FORBIDDEN))

    @attr(type='support_accounts')
    def test_list_support_account_without_x_auth_header_gives_401(self):
        """
        @summary: Verify that list support account without the authentiication
        header gives 401 Unauthorized.
        """
        self.auth_token = {"headers": {}}
        support_account = self.support_services_cutomer_provider.\
            support_contact_client.list_support_account_details(
                self.account_number, requestslib_kwargs=self.auth_token)

        self.assertEqual(support_account.status_code,
                         self.UNAUTHORIZED_CODE,
                         msg="The actual status code: {0} does not match "
                             "the expected code: {1}".format(
                         support_account.status_code,
                         self.UNAUTHORIZED_CODE))

    @attr(type='support_accounts')
    def test_list_support_account_invalid_x_auth_header_gives_401(self):
        """
        @summary: Verify that list support account with invalid authentiication
        header gives 401 Unauthorized.
        """
        self.auth_token = {"headers": {"X-Auth-Token": "abcd"}}
        support_account = self.support_services_cutomer_provider.\
            support_contact_client.list_support_account_details(
                self.account_number, requestslib_kwargs=self.auth_token)

        self.assertEqual(support_account.status_code,
                         self.UNAUTHORIZED_CODE,
                         msg="The actual status code: {0} does not match "
                             "the expected code: {1}".format(
                         support_account.status_code,
                         self.UNAUTHORIZED_CODE))

    @attr(type='support_accounts')
    def test_list_support_account_has_valid_service_level_details(self):
        """
        @summary: Verify that user is able to fetch service level value with
        list support account call.
        """
        support_account = self.support_services_cutomer_provider.\
            support_contact_client.list_support_account_details(
                self.account_number).entity

        self.assertEqual(support_account.account_service_level,
                         self.service_level,
                         msg="The actual service level: {0} does not match "
                             "the expected service level: {1}".format(
                         support_account.account_service_level,
                         self.service_level))
