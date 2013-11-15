import time

from ccengine.clients.lefty.lefty_api import LeftyAPITicketClient,\
    LeftyAPICategrySubCategoryClient, LeftyAPIQueueClient,\
    LeftyAPIStatusesClient, PubSubClient
from ccengine.common.tools.datagen import rand_name
from ccengine.providers.auth.auth_api import AuthProvider as _AuthProvider
from ccengine.providers.base_provider import BaseProvider


class LeftyAPIProvider(BaseProvider):

    def __init__(self, config, logger=None):
        super(LeftyAPIProvider, self).__init__()
        if config is None:
            self.client_log.warning('empty (=None) config recieved in init')
            ''' Load configuration from default.conf '''
            self.config = _AuthProvider
        else:
            self.config = config

        '''Get Auth Info '''
        self.auth_provider = _AuthProvider(self.config)

        self.auth_data = self.auth_provider.authenticate()
        '''Get Auth Token'''
        self.auth_token = self.auth_data.token.id
        '''setup url'''
        self.base_request_url = self.config.lefty.base_url
        self.data_centre = self.config.lefty.data_centre
        self.pubsub_url_dfw = self.config.lefty.pubsub_url_dfw
        self.pubsub_url_ord = self.config.lefty.pubsub_url_ord
        
        if self.data_centre == 'DFW':
            self.pubsub_url = self.pubsub_url_dfw
            self.pubsub_url_alt = self.pubsub_url_ord
        elif self.data_centre == 'ORD':
            self.pubsub_url = self.pubsub_url_ord
            self.pubsub_url_alt = self.pubsub_url_dfw

        '''initialize lefty api clients'''
        self.lefty_ticket_client =\
            LeftyAPITicketClient(self.base_request_url, self.auth_token,
                                 self.config.misc.serializer,
                                 self.config.misc.deserializer)

        self.lefty_category_sub_category_client =\
            LeftyAPICategrySubCategoryClient(self.base_request_url,
                                             self.auth_token,
                                             self.config.misc.serializer,
                                             self.config.misc.deserializer)

        self.lefty_queue_client =\
            LeftyAPIQueueClient(self.base_request_url, self.auth_token,
                                self.config.misc.serializer,
                                self.config.misc.deserializer)

        self.lefty_status_client =\
            LeftyAPIStatusesClient(self.base_request_url, self.auth_token,
                                   self.config.misc.serializer,
                                   self.config.misc.deserializer)

        self.pubsub_client =\
            PubSubClient(self.pubsub_url, self.auth_token,
                         self.config.misc.serializer,
                         self.config.misc.deserializer)

        self.pubsub_client_alt =\
            PubSubClient(self.pubsub_url_alt, self.auth_token,
                         self.config.misc.serializer,
                         self.config.misc.deserializer)
