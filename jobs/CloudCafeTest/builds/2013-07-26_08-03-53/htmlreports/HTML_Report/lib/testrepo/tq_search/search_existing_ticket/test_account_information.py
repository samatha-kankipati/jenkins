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
        account_info_from_acc_svs = \
            cls.account_services_provider.account_client.\
            search_for_specific_account_in_account_services(
                account_number=cls.account_number_3,
                account_type=cls.account_type_2
            ).entity
        cls.initial_team_name = account_info_from_acc_svs.team

    @classmethod
    def tearDownClass(cls):
        super(TestAccountInformation, cls).tearDownClass()
        cls.account_services_provider.account_client.\
            update_team_of_specific_account_in_account_services(
                account_number=cls.account_number_3,
                account_type=cls.account_type_2,
                team=cls.initial_team_name
            ).entity

    @attr(type='positive11', module='accountsvs', suite='smoke')
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

    @attr(type='positive11', module='accountsvs', suite='smoke')
    def test_update_ticket_attributes_and_verify_the_account_data(self):
        '''
        @summary: Update ticket attribute and verify account data
        '''

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
        time.sleep(5)
        results = \
            self.gate_provider.search_client.search_ticket_in_core(
                hardcoded_parameters=params).entity
        self.assertEquals(results.tickets[0].account,
                          get_account_info_from_acc_svs)

    @attr(type='positive11', module='accountsvs', suite='smoke')
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
