from testrepo.common.testfixtures.tq_search import TQSearchFixture
from ccengine.common.decorators import attr
import time
import datetime
from datetime import timedelta
from ccengine.common.tools.datatools import string_to_datetime, \
    convert_date_from_cst_to_utc_date
from ccengine.domain.tq_search.response.tq_search import TicketDetails
from ccengine.domain.tq_search.response.account_services import AccountServices
from ccengine.domain.tq_search.request.account_services_request import \
    AccountServicesRequest
from ccengine.domain.tq_search.response.tq_search import TicketDetails
from ccengine.domain.tq_search.response.elastic_search import ElasticSearch
from ccengine.domain.core.request.core_request import Where, WhereSet, \
    WhereCondition, WhereOperators, WhereEquals, WhereGreaterOrEquals, \
    WhereLessOrEquals, LoadArgs, CoreQuery, WhereIn, WhereNotEquals, \
    WhereNotIn, WhereLess, WhereGreater


class TestAccountInformation(TQSearchFixture):

    @classmethod
    def setUpClass(cls):
        super(TestAccountInformation, cls).setUpClass()
        print "NOW 1:"
        account_info_from_acc_svs = \
            cls.account_services_provider.account_client.\
            search_for_specific_account_in_account_services(
                account_number=cls.account_number_3,
                account_type=cls.account_type_2
            ).entity

    @classmethod
    def tearDownClass(cls):
        super(TestAccountInformation, cls).tearDownClass()
        #cls.account_services_provider.account_client.\
        #    update_team_of_specific_account_in_account_services(
        #        account_number=cls.account_number_3,
        #        account_type=cls.account_type_2,
        #        team=cls.initial_team_name
        #    ).entity

    @attr(type='positive109', module='accountsvs', suite='smoke')
    def test_list_tickets_and_verify_the_account_data(self):
        '''
        @summary:B-48389 Compare the account information of the ticket\
         after fetching data from account services
        '''
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
        team_information = \
            self.core_provider.account_client.get_account_attribute(
                load_value=account_info_from_acc_svs.number,
                attribute="highprofiles.id").entity
        high_profile_value = self.account_services_provider.\
            account_client.is_high_profile(team_info = team_information)
        self.assertEquals(results.tickets[0].account.highProfile,
                          high_profile_value)
        team_information_one = \
            self.core_provider.account_client.get_account_attribute(
                load_value=account_info_from_acc_svs.number,
                attribute="support_team").entity
        support_team_information = \
            self.core_provider.account_client.\
            get_account_team_attribute(load_value=
                                       team_information_one.get("load_value"),
                                       attribute="name").entity
        
        self.assertEquals(results.tickets[0].account.team,
                          support_team_information)

    @attr(type='positive10900', module='accountsvs', suite='smoke')
    def test_two_new_update_ticket_attributes_and_verify_the_account_data(self):
        params = \
            {'account.id': '{0}{1}'.format(self.account_type_2,
                                           self.account_number_3)}
        print "ACCOUNT NUMBER"
        print self.account_number_3
        team_information_two = \
            self.core_provider.account_client.get_account_attribute(
                load_value=self.account_number_3,
                attribute="support_team").entity
        initial_team_info = team_information_two
        print "INITIAL TEAM INFORMATION:"
        print initial_team_info.get("load_value")
        updated_value = \
            self.core_provider.account_client.update_account_team(
                account_number=self.account_number_3,
                attribute_name="support_team",
                attribute_value=79).entity
        # The sleep of 30 seconds is required as this is the time where the
        # updated team info will flow in the tq_search API
        time.sleep(30)
        updated_results = \
            self.gate_provider.search_client.search_ticket_in_core(
                hardcoded_parameters=params).entity
        team_information_one = \
            self.core_provider.account_client.get_account_attribute(
                load_value=self.account_number_3,
                attribute="support_team").entity
        support_team_information = \
            self.core_provider.account_client.\
            get_account_team_attribute(load_value=
                                       team_information_one.get("load_value"),
                                       attribute="name").entity
        print "UPDATED VALUE CORE"
        print support_team_information
        print "UPDATED VALUE TQ_SEARCH"
        print updated_results.tickets[0].account.team
        self.assertEquals(updated_results.tickets[0].account.team,
                          support_team_information)
        updated_value = \
            self.core_provider.account_client.update_account_team(
                account_number=self.account_number_3,
                attribute_name="support_team",
                attribute_value=initial_team_info.get("load_value")).entity
        time.sleep(30)
        team_information_three = \
            self.core_provider.account_client.get_account_attribute(
                load_value=self.account_number_3,
                attribute="support_team").entity
        print "TEARDOWN"
        print team_information_three.get("load_value")


    #@attr(type='positive109', module='accountsvs', suite='smoke')
    #def test_new_update_ticket_attributes_and_verify_the_account_data(self):
    #    '''
    #    @summary: Update ticket attribute and verify account data
    #    '''
    #    params = \
    #        {'account.id': '{0}{1}'.format(self.account_type_2,
    #                                       self.account_number_3)}
    #    results = \
    #        self.gate_provider.search_client.search_ticket_in_core(
    #            hardcoded_parameters=params).entity
    #    account_info_from_acc_svs = results.tickets[0].account
    #    print "ACCOUNT INFO FROM TQ_SEARCH"
    #    print account_info_from_acc_svs
    #    team_information_one = \
    #        self.core_provider.account_client.get_account_attribute(
    #            load_value=account_info_from_acc_svs.number,
    #            attribute="segment_team").entity
    #    updated_value = \
    #        self.core_provider.account_client.set_attribute(
    #            class_name="Account.Account",
    #            load_arg=account_info_from_acc_svs.number,
    #            attribute_name="support_team", attribute_value="80").entity
    #    print "UPDATES VALUE"
    #    print updated_value
    #    support_team_name = \
    #        self.core_provider.account_client.get_account_team_attribute(
    #            load_value=updated_value, attribute="name").entity
    #    print "UPDATED TEAM NAME"
    #    print support_team_name
    #    # The sleep here ensures that we need to wait 10 seconds before
    #    # we check the value in the search API
    #    time.sleep(10)
    #    results = \
    #        self.gate_provider.search_client.search_ticket_in_core(
    #            hardcoded_parameters=params).entity
    #    self.assertEquals(results.tickets[0].account.team,
    #                      support_team_name)
    #    print "UDATED_NAME IN TQ_SEARCH"
    #    print results.tickets[0].account.team
    #    updated_value = \
    #        self.core_provider.account_client.set_attribute(
    #            class_name="Account.Account",
    #            load_arg=account_info_from_acc_svs.number,
    #            attribute_name="segment_team",
    #            attribute_value=team_information_one)

    @attr(type='positive109', module='accountsvs', suite='smoke')
    def test_updating_team_attribute_from_account_services_doesnt_showup_in_tq_search(self):
        '''
        @summary: Update ticket attribute and verify account data
        '''
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
        # field is set back to the original value so that the update test
        # can go on
        time.sleep(30)
        results = \
            self.gate_provider.search_client.search_ticket_in_core(
                hardcoded_parameters=params).entity
        self.assertTrue(results.tickets[0].account.team <>
                          get_account_info_from_acc_svs.team)
        account_info_from_acc_svs = \
            self.account_services_provider.account_client.\
            update_team_of_specific_account_in_account_services(
                account_number=self.account_number_3,
                account_type=self.account_type_2,
                team=initial_team_name
            ).entity

    @attr(type='positive109', module='accountsvs', suite='smoke')
    def test_same_number_of_accounts_in_account_svs_and_elastic_search(self):
        '''
        @summary: Verify that same number of account is present in elastic
        search and tq search
        '''
        number_of_accounts_in_acc_svs = \
            self.account_services_provider.account_client.\
            get_number_of_accounts_in_account_services().entity
        print number_of_accounts_in_acc_svs.total
    
        number_of_accounts_in_elastic_search = \
            self.elastic_search_provider.elastic_client.\
            total_number_of_accounts().entity
        print number_of_accounts_in_elastic_search.total
        self.assertEquals(number_of_accounts_in_acc_svs.total,
                          str(number_of_accounts_in_elastic_search.total),
                          "The number of accounts are not same in elastic \
                          search and account services")
