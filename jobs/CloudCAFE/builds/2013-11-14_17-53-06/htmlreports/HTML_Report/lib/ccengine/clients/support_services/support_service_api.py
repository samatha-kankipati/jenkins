import time
from urlparse import urlparse

from ccengine.clients.base_client import BaseMarshallingClient
from ccengine.domain.support_services.response.support_service import Groups,\
    SupportAccounts, Roles
from ccengine.domain.support_services.response.team import SupportTeam


class SupportServicesAPIGroupsClient(BaseMarshallingClient):

    def __init__(self, url, auth_token, serialize_format=None,
                 deserialize_format=None):

        super(SupportServicesAPIGroupsClient, self).\
            __init__(serialize_format, deserialize_format)
        self.auth_token = auth_token
        self.default_headers['X-Auth-Token'] = auth_token
        ct = ''.join(['application/', self.serialize_format])
        accept = ''.join(['application/', self.deserialize_format])
        self.default_headers['Content-Type'] = ct
        self.default_headers['Accept'] = accept
        self.url = url

    def list_groups(self, name=None, requestslib_kwargs=None):
        """
        @summary: Returns a list of all the available groups.
        @param name: Name of the group to filter the list.
        @type name: String
        @param requestslib_kwargs: pass if you want to add new headers or
        modify existing
        headers.
        @type requestslib_kwargs: dict
        """
        url = '{0}/groups'.format(self.url)
        params = {"name": name}
        groups_response = self.request('GET', url, params=params,
                                       response_entity_type=Groups,
                                       requestslib_kwargs=requestslib_kwargs)
        return groups_response

    def get_group(self, group_id, requestslib_kwargs=None):
        """
        @summary: Returns the details of the group.
        @param group_id: ID of the group whose details are needed.
        @type group_id: Integer
        @param requestslib_kwargs: pass if you want to add new headers or
        modify existing
        headers.
        @type requestslib_kwargs: dict
        """
        url = '{0}/groups/{1}'.format(self.url, group_id)
        group_response = self.request('GET', url,
                                      response_entity_type=Groups,
                                      requestslib_kwargs=requestslib_kwargs)
        return group_response


class SupportContactClient(BaseMarshallingClient):

    def __init__(self, url, auth_token, serialize_format=None,
                 deserialize_format=None):

        super(SupportContactClient, self).\
            __init__(serialize_format, deserialize_format)
        self.auth_token = auth_token
        self.default_headers['X-Auth-Token'] = auth_token
        ct = ''.join(['application/', self.serialize_format])
        accept = ''.join(['application/', self.deserialize_format])
        self.default_headers['Content-Type'] = ct
        self.default_headers['Accept'] = accept
        self.url = url

    def list_support_account_details(self, account_number,
                                     requestslib_kwargs=None):
        """
        @summary: Returns the details of the group.
        @param account_number: ID of the account whose details are needed.
        @type account_number: Integer
        @param requestslib_kwargs: pass if you want to add new headers or
        modify existing
        headers.
        @type requestslib_kwargs: dict
        """
        url = '{0}/support-accounts/{1}'.format(self.url, account_number)
        account_response = self.request('GET', url,
                                        response_entity_type=SupportAccounts,
                                        requestslib_kwargs=requestslib_kwargs)
        return account_response

    def get_roles_for_an_account(self, account_number):
        """
        @summary: Returns the details of the group.
        @param account_number: ID of the account whose details are needed.
        @type account_number: Integer
        """
        url = '{0}/support-accounts/{1}/roles'.format(self.url, account_number)
        account_response = self.request('GET', url,
                                        response_entity_type=Roles)
        return account_response


class SupportTeamsClient(BaseMarshallingClient):

    def __init__(self, url, auth_token, serialize_format=None,
                 deserialize_format=None):

        super(SupportTeamsClient, self).\
            __init__(serialize_format, deserialize_format)
        self.auth_token = auth_token
        self.default_headers['X-Auth-Token'] = auth_token
        ct = ''.join(['application/', self.serialize_format])
        accept = ''.join(['application/', self.deserialize_format])
        self.default_headers['Content-Type'] = ct
        self.default_headers['Accept'] = accept
        self.url = url

    def list_support_teams(self, name=None, requestslib_kwargs=None):
        """
        @summary: Returns the details of the teams.
        @param requestslib_kwargs: pass if you want to add new headers or
        modify existing headers.
        @type requestslib_kwargs: dict
        """
        url = '{0}/teams'.format(self.url)
        params = {'name': name}
        support_teams_response = self.request(
            'GET', url, params=params,
            response_entity_type=SupportTeam,
            requestslib_kwargs=requestslib_kwargs)
        return support_teams_response

    def get_support_teams_details(self, team_id, requestslib_kwargs=None):
        """
        @summary: Returns the details of the teams.
        @param team_id: ID of the team
        @type team_id: integer
        @param requestslib_kwargs: pass if you want to add new headers or
        modify existing headers.
        @type requestslib_kwargs: dict
        """
        url = '{0}/teams/{1}'.format(self.url, team_id)
        support_teams_response = self.request(
            'GET', url,
            response_entity_type=SupportTeam,
            requestslib_kwargs=requestslib_kwargs)
        return support_teams_response
