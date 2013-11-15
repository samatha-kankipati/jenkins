import datetime
from urlparse import urlparse

from ccengine.clients.base_client import BaseMarshallingClient
from ccengine.common.tools.datatools import string_to_datetime
from ccengine.domain.tq_search.response.tq_search import Gate, Search, \
    TicketDetails


class GateAPIClient(BaseMarshallingClient):

    def __init__(self, url, serialize_format=None,
                 deserialize_format=None):
        super(GateAPIClient, self).__init__(serialize_format,
                                            deserialize_format)
        self.url = url

    def health_check(self):
        url = '{0}healthStatus'.format(self.url)
        gate_response = self.request('GET', url, response_entity_type=Gate)
        return gate_response

    def info_check(self):
        url = '{0}info'.format(self.url)
        get_response = self.request('GET', url, response_entity_type=Gate)
        return get_response


class SearchApiClient(BaseMarshallingClient):

    def __init__(self, url, serialize_format=None,
                 deserialize_format=None):
        super(SearchApiClient, self).__init__(serialize_format,
                                              deserialize_format)
        self.url = url

    def search_ticket_in_core(self, status=None, queue=None, category=None,
                              priority=None, subject=None, number=None,
                              created_at=None, created_at_range=None,
                              limit=100, offset=0, url=None,
                              hardcoded_parameters={}, sort=None):

        params = {'status': status, 'queue': queue, 'category': category,
                  'priority': priority, 'subject': subject, 'number': number,
                  'createdAt': created_at,
                  'createdAt_range': created_at_range,
                  'limit': limit, 'offset': offset, 'sort': sort}

        params = dict(params.items() + hardcoded_parameters.items())

        if url is None:
            url = '{0}tickets'.format(self.url)
        else:
            url = url
        search_response = self.request('GET', url, response_entity_type=Search,
                                       params=params)

        return search_response

    def get_specific_ticket_from_core(self, number, url=None):

        if url is None:
            url = '{0}tickets/{1}'.format(self.url, number)
        else:
            url = url
        search_response = self.request('GET', url, response_entity_type=Search)

        return search_response

    def get_facets(self, fields, url=None):

        if url is None:
            url = '{0}tickets/{1}'.format(self.url, fields)
        else:
            url = url
        search_response = self.request('GET', url, response_entity_type=Search)

        return search_response


class ComplexQueryClient(BaseMarshallingClient):

    def __init__(self, url, serialize_format=None,
                 deserialize_format=None):
        super(ComplexQueryClient, self).__init__()
        self.url = url

    def filter_tickets(self, payload, requestslib_kwargs=None):
        url = '{}tickets'.format(self.url)
        if requestslib_kwargs is None:
            search_response = self.request('POST', url,
                                           response_entity_type=Search,
                                           data=payload._obj_to_json())
        else:
            search_response = self.request('POST', url,
                                           response_entity_type=Search,
                                           data=payload._obj_to_json(),
                                           params=requestslib_kwargs['params'])
        return search_response
