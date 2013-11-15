import datetime
from requests.auth import HTTPBasicAuth
from urlparse import urlparse

from ccengine.clients.base_client import BaseMarshallingClient
from ccengine.common.tools.datatools import string_to_datetime
from ccengine.domain.tq_search.response.tq_search import Gate
from ccengine.domain.tq_search.response.tq_search import Search
from ccengine.domain.tq_search.response.tq_search import TicketDetails
from ccengine.domain.tq_search.response.account_services import AccountServices
from ccengine.domain.tq_search.request.account_services_request import\
    AccountServicesRequest


class AccountServicesClient(BaseMarshallingClient):

    def __init__(self, url, auth_token, serialize_format=None,
                 deserialize_format=None, config=None):
        super(AccountServicesClient, self).__init__(serialize_format,
                                                    deserialize_format)
        self.auth_token = auth_token
        self.url = url
        self.config = config
        ct = "application/{0}".format(self.serialize_format)
        accept = "application/{0}".format(self.deserialize_format)
        self.default_headers['Content-Type'] = ct
        self.default_headers['Accept'] = accept

    def search_for_specific_account_in_account_services(self,
                                                        account_number,
                                                        account_type,
                                                        url=None):
        '''
        @summary: Returns a specific account from account services
        @param account_number: which account to return
        @type account_number: int
        @param account_type: what is the type of the account getting returned
        @type account_type: string
        @param url: which returns the url
        @type account_number: string
        '''
        url = url or '{0}accounts/{1}/{2}'.format(self.url, account_type,
                                                  account_number)
        self.config.auth.account_services_username
        auth_det = HTTPBasicAuth(self.config.auth.account_services_username,
                                 self.config.auth.account_services_password)
        account_services_response =\
            self.request('GET', url, response_entity_type=AccountServices,
                         requestslib_kwargs={'auth': auth_det})
        return account_services_response

    def update_team_of_specific_account_in_account_services(self,
                                                            account_number,
                                                            account_type,
                                                            team,
                                                            url=None):
        '''
        @summary: Updated the team info of a specific account from
        account services
        @param account_number: which account to return
        @type account_number: int
        @param account_type: what is the type of the account getting returned
        @type account_type: string
        @param team: what is the team of the given account
        @type account_type: string
        @param url: which returns the url
        @type account_number: string
        '''
        url = url or '{0}accounts/{1}/{2}'.format(self.url, account_type,
                                                  account_number)
        account_service_object = AccountServicesRequest(number=account_number,
                                                        type=account_type,
                                                        team=team)
        auth_det = HTTPBasicAuth(self.config.auth.account_services_username,
                                 self.config.auth.account_services_password)
        account_services_response =\
            self.request('PUT', url,
                         response_entity_type=AccountServices,
                         request_entity=account_service_object,
                         requestslib_kwargs={'auth': auth_det})

        return account_services_response

    def get_number_of_accounts_in_account_services(self, url=None):
        '''
        @summary: gets the number of accounts in the account services.
        @param url: which returns the url
        @type account_number: string
        '''
        url = url or '{0}accounts/'.format(self.url)

        auth_det = HTTPBasicAuth(self.config.auth.account_services_username,
                                 self.config.auth.account_services_password)
        account_service_response =\
            self.request('GET', url,
                         response_entity_type=AccountServices,
                         requestslib_kwargs={'auth': auth_det})
        return account_service_response

    def is_high_profile(self, team_info=None):
        '''
        @summary: return the value for high profile
        @param team_info: accepts team_info
        @type team_info: list
        '''
        if team_info is None:
            team_info = list()
        value = False
        if len(team_info) is 0:
            value = False
        elif len(team_info) == 1 and team_info[0] == 1:
            value = True
        return value
