import datetime
from datetime import timedelta
import time

from ccengine.common.decorators import attr
from ccengine.common.tools.datatools import string_to_datetime, \
    convert_date_from_cst_to_utc_date
from ccengine.domain.core.request.core_request import Where, WhereSet, \
    WhereCondition, WhereOperators, WhereEquals, WhereGreaterOrEquals, \
    WhereLessOrEquals, LoadArgs, CoreQuery, WhereIn, WhereNotEquals, \
    WhereNotIn, WhereLess, WhereGreater
from ccengine.domain.tq_search.request.account_services_request import \
    AccountServicesRequest
from ccengine.domain.tq_search.response.account_services import AccountServices
from ccengine.domain.tq_search.response.tq_search import TicketDetails
from ccengine.domain.tq_search.response.elastic_search import ElasticSearch
from testrepo.common.testfixtures.tq_search import TQSearchFixture


class TestAccountInformation(TQSearchFixture):

    @attr(type='positive', module='accountsvs', suite='smoke')
    def test_list_tickets_and_verify_the_account_data(self):
        """
        @summary:B-48389 Compare the account information of the ticket\
         after fetching data from account services
        """
        account_info_from_acc_svs = \
            self.account_services_provider.account_client.\
            search_for_specific_account_in_account_services(
                account_number=self.account_number_2,
                account_type=self.account_type_2
            ).entity
        params = \
            {'account.id': '{0}{1}'.format(self.account_type_2,
                                           self.account_number_2)}
        results = \
            self.gate_provider.search_client.\
            search_ticket_in_core(hardcoded_parameters=params).entity
        self.assertEquals(results.tickets[0].account,
                          account_info_from_acc_svs)
        team_segment = \
            self.core_provider.account_client.get_account_attribute(
                load_value=account_info_from_acc_svs.number,
                attribute="segment"
            ).entity
        team_segment_name = team_segment.get("name")
        self.assertEquals(results.tickets[0].account.team_segment,
                          team_segment_name)
        team_information = \
            self.core_provider.account_client.get_account_attribute(
                load_value=account_info_from_acc_svs.number,
                attribute="highprofiles.id"
            ).entity
        high_profile_value = self.account_services_provider.\
            account_client.is_high_profile(team_info=team_information)
        self.assertEquals(results.tickets[0].account.high_profile,
                          high_profile_value)
        team_information_one = \
            self.core_provider.account_client.get_account_attribute(
                load_value=account_info_from_acc_svs.number,
                attribute="support_team"
            ).entity
        support_team_information = \
            self.core_provider.account_client.get_account_team_attribute(
                load_value=team_information_one.get("load_value"),
                attribute="name"
            ).entity
        self.assertEquals(
            results.tickets[0].account.team, support_team_information,
            "Failed:actual{0} expected{1}".format(
                results.tickets[0].account.team, support_team_information))

    @attr(type='positive', module='accountsvs', suite='smoke')
    def test_updating_ctkapi_team_attribute_sync_in_tq_search(self):
        """
        @summary: Compare the account information of the ticket\
         after updating team data from ctkapi
        """
        params = \
            {'account.id': '{0}{1}'.format(self.account_type_2,
                                           self.account_number_3)}
        team_information_two = \
            self.core_provider.account_client.get_account_attribute(
                load_value=self.account_number_3,
                attribute="support_team"
            ).entity
        initial_team_info = team_information_two
        updated_value = \
            self.core_provider.account_client.update_account_team(
                account_number=self.account_number_3,
                attribute_name="support_team",
                attribute_value=self.team_number
            ).entity
        # The sleep of 30 seconds is required as this is the time where the
        # updated team info will flow in the tq_search API
        time.sleep(float(self.sleep_30_sec))
        updated_results = \
            self.gate_provider.search_client.search_ticket_in_core(
                hardcoded_parameters=params
            ).entity
        team_information_one = \
            self.core_provider.account_client.get_account_attribute(
                load_value=self.account_number_3,
                attribute="support_team"
            ).entity
        support_team_information = \
            self.core_provider.account_client.\
            get_account_team_attribute(
                load_value=team_information_one.get("load_value"),
                attribute="name"
            ).entity
        self.assertEquals(
            updated_results.tickets[0].account.team, support_team_information,
            "Failed:actual{0} expected{1}".format(
                updated_results.tickets[0].account.team,
                support_team_information))
        updated_value = \
            self.core_provider.account_client.update_account_team(
                account_number=self.account_number_3,
                attribute_name="support_team",
                attribute_value=initial_team_info.get("load_value")
            ).entity
        # The sleep is given here so that after the test completes the
        # field is set back to the original value
        time.sleep(float(self.sleep_30_sec))
        team_information_three = \
            self.core_provider.account_client.get_account_attribute(
                load_value=self.account_number_3,
                attribute="support_team"
            ).entity

    @attr(type='positive', module='accountsvs', suite='smoke')
    def test_updating_acc_svs_team_attribute_not_syncing_in_tq_search(self):
        """
        @summary: Update team attribute of ticket from account services
        and verify that the data does not get synced to tq_search
        """
        get_account_info_from_acc_svs = \
            self.account_services_provider.account_client.\
            search_for_specific_account_in_account_services(
                account_number=self.account_number_3,
                account_type=self.account_type_2
            ).entity
        initial_team_name = get_account_info_from_acc_svs.team
        account_info_from_acc_svs = \
            self.account_services_provider.account_client.\
            update_team_of_specific_account_in_account_services(
                account_number=self.account_number_3,
                account_type=self.account_type_2,
                team=self.team_name
            ).entity
        get_account_info_from_acc_svs = \
            self.account_services_provider.account_client.\
            search_for_specific_account_in_account_services(
                account_number=self.account_number_3,
                account_type=self.account_type_2
            ).entity
        params = \
            {'account.id': '{0}{1}'.format(self.account_type_2,
                                           self.account_number_3)}
        # The sleep is given here so that after the test completes the
        # field is set back to the original value
        time.sleep(float(self.sleep_30_sec))
        results = \
            self.gate_provider.search_client.search_ticket_in_core(
                hardcoded_parameters=params
            ).entity
        self.assertTrue(
            results.tickets[0].account.team !=
            get_account_info_from_acc_svs.team,
            "Failed {0}!={1}".format(results.tickets[0].account.team,
                                     get_account_info_from_acc_svs.team))
        account_info_from_acc_svs = \
            self.account_services_provider.account_client.\
            update_team_of_specific_account_in_account_services(
                account_number=self.account_number_3,
                account_type=self.account_type_2,
                team=initial_team_name
            ).entity

    @attr(type='regression', module='accountsvs', suite='smoke')
    def test_same_number_of_accounts_in_account_svs_and_elastic_search(self):
        """
        @summary: Verify that same number of account is present in elastic
        search and tq search
        """
        number_of_accounts_in_acc_svs = \
            self.account_services_provider.account_client.\
            get_number_of_accounts_in_account_services().entity

        number_of_accounts_in_elastic_search = \
            self.elastic_search_provider.elastic_client.\
            total_number_of_accounts().entity
        self.assertEquals(
            number_of_accounts_in_acc_svs.total,
            str(number_of_accounts_in_elastic_search.total),
            "The number of accounts are not same{0}{1}".format(
                number_of_accounts_in_acc_svs.total,
                str(number_of_accounts_in_elastic_search.total)))
