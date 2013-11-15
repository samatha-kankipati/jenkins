from ccengine.clients.base_client import BaseMarshallingClient
from ccengine.domain.tq_search.response.tq_search import Gate, Search, \
    TicketDetails
from ccengine.domain.tq_search.response.account_services import AccountServices
from ccengine.domain.tq_search.request.account_services_request import\
    AccountServicesRequest
from ccengine.common.tools.datatools import string_to_datetime
import datetime
from urlparse import urlparse
from requests.auth import HTTPBasicAuth


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
        if url is None:
            url = '{0}accounts/{1}/{2}'.format(self.url, account_type,
                                               account_number)
        else:
            url = url
        auth_det = HTTPBasicAuth(self.config.auth.account_services_username,
                                 self.config.auth.account_services_password)
        account_services_response =\
            self.request('GET', url, auth=auth_det,
                         response_entity_type=AccountServices)
        return account_services_response

    def update_team_of_specific_account_in_account_services(self,
                                                            account_number,
                                                            account_type,
                                                            team,
                                                            url=None):
        if url is None:
            url = '{0}accounts/{1}/{2}'.format(self.url, account_type,
                                               account_number)

        else:
            url = url
        account_service_object = AccountServicesRequest(number=account_number,
                                                        type=account_type,
                                                        team=team)
        auth_det = HTTPBasicAuth(self.config.auth.account_services_username,
                                 self.config.auth.account_services_password)
        account_services_response =\
            self.request('PUT', url, auth=auth_det,
                         response_entity_type=AccountServices,
                         request_entity=account_service_object)

        return account_services_response

    def get_number_of_accounts_in_account_services(self, url=None):
        if url is None:
            url = '{0}accounts/'.format(self.url)
        else:
            url = url
        auth_det = HTTPBasicAuth(self.config.auth.account_services_username,
                                 self.config.auth.account_services_password)
        account_service_response =\
            self.request('GET', url, auth=auth_det,
                         response_entity_type=AccountServices)
        return account_service_response
