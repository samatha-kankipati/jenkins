from ccengine.providers.base_provider import BaseProvider
from ccengine.clients.core.core_api import CoreAPIClient
from ccengine.providers.auth.auth_api import AuthProvider as _AuthProvider
from ccengine.clients.core.ticket_api import TicketAPIClient
from ccengine.clients.core.queue_api import QueueAPIClient
from ccengine.clients.core.contact_api import ContactAPIClient
from ccengine.clients.core.account_api import AccountAPIClient
from ccengine.clients.core.contract_api import ContractAPIClient
from ccengine.clients.core.computer_api import ComputerAPIClient


class CoreAPIProvider(BaseProvider):

    def __init__(self, config, logger=None):
        super(CoreAPIProvider, self).__init__()
        if config is None:
            self.client_log.warning('empty (=None) config recieved in init')
            ''' Load configuration from default.conf '''
            self.config = _AuthProvider
        else:
            self.config = config

        '''Get Auth Info '''
        self.auth_provider = _AuthProvider(self.config)

        '''Get Auth Token'''
        self.auth_token = self.auth_provider.authenticate()

        '''setup url'''
        self.base_request_url = self.config.auth.base_url

        '''initialize core api clients'''
        self.core_client = CoreAPIClient(self.base_request_url,
                                         self.auth_token,
                                         self.config.misc.serializer,
                                         self.config.misc.deserializer)

        self.ticket_client = TicketAPIClient(self.base_request_url,
                                             self.auth_token,
                                             self.config.misc.serializer,
                                             self.config.misc.deserializer)

        self.queue_client = QueueAPIClient(self.base_request_url,
                                           self.auth_token,
                                           self.config.misc.serializer,
                                           self.config.misc.deserializer)

        self.account_client = AccountAPIClient(self.base_request_url,
                                               self.auth_token,
                                               self.config.misc.serializer,
                                               self.config.misc.deserializer)

        self.contract_client = ContractAPIClient(self.base_request_url,
                                                 self.auth_token,
                                                 self.config.misc.serializer,
                                                 self.config.misc.deserializer)

        self.contact_client = ContactAPIClient(self.base_request_url,
                                               self.auth_token,
                                               self.config.misc.serializer,
                                               self.config.misc.deserializer)
        self.computer_client = ComputerAPIClient(self.base_request_url,
                                                 self.auth_token,
                                                 self.config.misc.serializer,
                                                 self.config.misc.deserializer)
