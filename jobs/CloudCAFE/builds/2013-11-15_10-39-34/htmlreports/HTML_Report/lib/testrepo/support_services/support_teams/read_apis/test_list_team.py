from ccengine.common.decorators import attr
from testrepo.common.testfixtures.support_service import SupportServicesFixture


class ListTeamsTest(SupportServicesFixture):

    @attr(type='support_team')
    def test_verify_that_racker_can_retrieve_list_of_teams(self):
        """
        @summary: Verify that a racker can retrieve the list of all the teams.
        """
        support_teams = self.support_services_groups_provider.\
            support_team_client.list_support_teams()

        self.assertEqual(support_teams.status_code, self.OK_CODE,
                         msg="The team list is not retrieved successfully")

    @attr(type='support_team')
    def test_verify_list_team_with_invalid_x_auth_gives_401(self):
        """
        @summary: Verify if a racker tries to retrieve the list of all the
        teams with invalid x-auth token, he gets a 401.
        """
        self.auth_token = {"headers": {"X-Auth-Token": "abcd"}}
        support_teams = self.support_services_groups_provider.\
            support_team_client.list_support_teams(
                requestslib_kwargs=self.auth_token
            )

        self.assertEqual(support_teams.status_code,
                         self.UNAUTHORIZED_CODE,
                         msg="The actual status code: {0} does not match "
                             "the expected code: {1}".format(
                             support_teams.status_code,
                             self.UNAUTHORIZED_CODE))

    @attr(type='support_team')
    def test_verify_list_team_with_no_x_auth_gives_401(self):
        """
        @summary: Verify if a racker tries to retrieve the list of all the
        teams with no x-auth token, he gets a 401.
        """
        self.auth_token = {"headers": {}}
        support_teams = self.support_services_groups_provider.\
            support_team_client.list_support_teams(
                requestslib_kwargs=self.auth_token
            )

        self.assertEqual(support_teams.status_code,
                         self.UNAUTHORIZED_CODE,
                         msg="The actual status code: {0} does not match "
                             "the expected code: {1}".format(
                             support_teams.status_code,
                             self.UNAUTHORIZED_CODE))

    @attr(type='support_team')
    def test_verify_list_team_with_customer_auth_gives_403(self):
        """
        @summary: Verify if a customer tries to retrieve the list of all the
        teams, he gets a 403.
        """
        support_teams = self.support_services_cutomer_provider.\
            support_team_client.list_support_teams()

        self.assertEqual(support_teams.status_code,
                         self.FORBIDDEN,
                         msg="The actual status code: {0} does not match "
                             "the expected code: {1}".format(
                         support_teams.status_code,
                         self.FORBIDDEN))

    @attr(type='support_team')
    def test_verify_racker_can_retrieve_details_of_a_team(self):
        """
        @summary: Verify that a racker is able to retrieve the details of a
        team.
        """
        support_teams = self.support_services_groups_provider.\
            support_team_client.get_support_teams_details(
                self.team_id
            )

        self.assertEqual(support_teams.status_code, self.OK_CODE,
                         msg="The team details are not retrieved successfully")

    @attr(type='support_team')
    def test_verify_fetch_with_invalid_team_id_gives_400(self):
        """
        @summary: Verify that a racker tries to retrieve the details of a team
        with invalid team ID, the API returns a 400 BadRequest.
        """
        invalid_team_id = "abcd"
        support_teams = self.support_services_groups_provider.\
            support_team_client.get_support_teams_details(
                invalid_team_id
            )

        self.assertEqual(support_teams.status_code, self.BAD_REQ_CODE,
                         msg="The actual status code: {0} does not match "
                             "the expected code: {1}".format(
                             support_teams.status_code, self.BAD_REQ_CODE))

    @attr(type='support_team')
    def test_verify_fetch_with_unknown_team_id_gives_404(self):
        """
        @summary: Verify that a racker tries to retrieve the details of a team
        with unknown team ID, the API returns a 404 NotFound.
        """
        unknown_team_id = 9999999
        support_teams = self.support_services_groups_provider.\
            support_team_client.get_support_teams_details(
                unknown_team_id
            )

        self.assertEqual(support_teams.status_code, self.NOT_FOUND,
                         msg="The actual status code: {0} does not match "
                             "the expected code: {1}".format(
                             support_teams.status_code, self.NOT_FOUND))

    @attr(type='support_team')
    def test_verify_get_team_details_with_invalid_x_auth_gives_401(self):
        """
        @summary: Verify if a racker tries to retrieve the details of a
        team with invalid x-auth token, he gets a 401.
        """
        self.auth_token = {"headers": {"X-Auth-Token": "abcd"}}
        support_teams = self.support_services_groups_provider.\
            support_team_client.get_support_teams_details(
                self.team_id, requestslib_kwargs=self.auth_token
            )

        self.assertEqual(support_teams.status_code,
                         self.UNAUTHORIZED_CODE,
                         msg="The actual status code: {0} does not match "
                             "the expected code: {1}".format(
                             support_teams.status_code,
                             self.UNAUTHORIZED_CODE))

    @attr(type='support_team')
    def test_verify_get_team_details_with_no_x_auth_gives_401(self):
        """
        @summary: Verify if a racker tries to retrieve the details of a
        team with no x-auth token, he gets a 401.
        """
        self.auth_token = {"headers": {}}
        support_teams = self.support_services_groups_provider.\
            support_team_client.get_support_teams_details(
                self.team_id, requestslib_kwargs=self.auth_token
            )

        self.assertEqual(support_teams.status_code,
                         self.UNAUTHORIZED_CODE,
                         msg="The actual status code: {0} does not match "
                             "the expected code: {1}".format(
                             support_teams.status_code,
                             self.UNAUTHORIZED_CODE))

    @attr(type='support_team')
    def test_verify_get_team_details_with_customer_auth_gives_403(self):
        """
        @summary: Verify if a customer tries to retrieve the details of a
        team, he gets a 403.
        """
        self.auth_token = {"headers": {}}
        support_teams = self.support_services_cutomer_provider.\
            support_team_client.get_support_teams_details(
                self.team_id
            )

        self.assertEqual(support_teams.status_code,
                         self.FORBIDDEN,
                         msg="The actual status code: {0} does not match "
                             "the expected code: {1}".format(
                             support_teams.status_code,
                             self.FORBIDDEN))

    @attr(type='support_team')
    def test_verify_that_racker_can_retrieve_list_of_teams_by_name(self):
        """
        @summary: Verify that a racker can retrieve the list of all the teams
        filtered by name.
        """
        name_filter = "Rackspace"
        support_teams = self.support_services_groups_provider.\
            support_team_client.list_support_teams(name=name_filter)

        self.assertEqual(support_teams.status_code, self.OK_CODE,
                         msg="The expected code does not match the actual "
                             "code")

        for support_team in support_teams.entity:
            self.assertNotEqual(support_team.team_name.lower().
                                find(name_filter.lower()), -1,
                                msg="The support team with ID: {0}, should "
                                    "belong to the list".
                                    format(support_team.team_id))

    @attr(type='support_team')
    def test_verify_list_teams_by_name_returns_empty_list_when_not_found(self):
        """
        @summary: Verify that a racker gets an empty list back when he tries to
        filter with a team name that does not exist.
        """
        name_filter = "nothing"
        support_teams = self.support_services_groups_provider.\
            support_team_client.list_support_teams(name=name_filter).entity

        self.assertEqual(len(support_teams), 0, msg="The API does not return "
                         "an empty list")
