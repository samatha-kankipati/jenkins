from ccengine.providers.base_provider import BaseProvider
from ccengine.clients.tq_search.gate_api import GateAPIClient, SearchApiClient
from ccengine.providers.auth.auth_api import AuthProvider as _AuthProvider
from ccengine.clients.tq_search.account_api import AccountServicesClient
from ccengine.clients.tq_search.elastic_search import ElasticSearchClient


class GateAPIProvider(BaseProvider):

    def __init__(self, config, logger=None):
        super(GateAPIProvider, self).__init__()
        if config is None:
            self.client_log.warning('empty (=None) config recieved in init')
            ''' Load configuration from default.conf '''
            self.config = _AuthProvider
        else:
            self.config = config

        self.base_request_url = self.config.tq_search.base_url

        '''initialize tq api clients'''
        self.gate_client = GateAPIClient(self.base_request_url,
                                         self.config.misc.serializer,
                                         self.config.misc.deserializer)

        self.search_client = SearchApiClient(self.base_request_url,
                                             self.config.misc.serializer,
                                             self.config.misc.deserializer)


class AccountServicesProvider(BaseProvider):

    def __init__(self, config, logger=None):
        super(AccountServicesProvider, self).__init__()

        if config is None:
            self.client_log.warning('empty (=None) config recieved in init')
            ''' Load configuration from default.conf '''
            self.config = _AuthProvider
        else:
            self.config = config
        self.base_request_url_account = \
            self.config.auth.account_services_url
        '''Initilize Account services client'''

        self.account_client =\
            AccountServicesClient(self.base_request_url_account,
                                  self.config.misc.serializer,
                                  self.config.misc.deserializer,
                                  config=self.config)


class EasticSearchProvider(BaseProvider):

    def __init__(self, config, logger=None):
        super(EasticSearchProvider, self).__init__()
        if config is None:
            self.client_log.warning('empty (=None) config recieved in init')
            ''' Load configuration from default.conf '''
            self.config = _AuthProvider
        else:
            self.config = config
        self.elastic_search_url = \
            self.config.tq_search.elastic_search_url
        '''Initilize Account services client'''
        self.elastic_client =\
            ElasticSearchClient(self.elastic_search_url,
                                self.config.misc.serializer,
                                self.config.misc.deserializer)
