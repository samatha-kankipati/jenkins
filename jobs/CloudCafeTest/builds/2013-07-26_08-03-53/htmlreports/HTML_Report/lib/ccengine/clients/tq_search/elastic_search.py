from ccengine.clients.base_client import BaseMarshallingClient
from ccengine.domain.tq_search.response.tq_search import Gate, Search, \
    TicketDetails
from ccengine.domain.tq_search.response.elastic_search import ElasticSearch
from ccengine.common.tools.datatools import string_to_datetime
import datetime
from urlparse import urlparse


class ElasticSearchClient(BaseMarshallingClient):

    def __init__(self, url, serialize_format=None,
                 deserialize_format=None):
        super(ElasticSearchClient, self).__init__()
        self.url = url

    def total_number_of_accounts(self):

        url = '{0}account/_search'.format(self.url)
        gate_response = self.request('GET', url,
                                     response_entity_type=ElasticSearch)
        return gate_response
