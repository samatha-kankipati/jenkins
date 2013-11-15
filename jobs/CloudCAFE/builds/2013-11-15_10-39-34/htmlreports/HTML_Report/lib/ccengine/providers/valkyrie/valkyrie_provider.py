from ccengine.clients.valkyrie.valkyrie_api import ValkyrieAPIClient
from ccengine.common.tools.datagen import rand_name
from ccengine.providers.base_provider import BaseProvider


class ValkyrieProvider(BaseProvider):

    def __init__(self, config, logger=None):
        super(ValkyrieProvider, self).__init__()
        self.config = config
        self.auth_token = self.config.valkyrie.valkyrie_auth_token
        self.dedicated_account = self.config.valkyrie.\
            valkyrie_dedicated_account
        self.cloud_account = self.config.valkyrie.valkyrie_cloud_account
        self.valkyrie_base_url = self.config.valkyrie.valkyrie_base_url
        self.valkyrie_test_ticket = self.config.valkyrie.valkyrie_test_ticket
        self.valkyrie_client = ValkyrieAPIClient(self.valkyrie_base_url,
                                                 self.auth_token,
                                                 self.config.misc.serializer,
                                                 self.config.misc.deserializer)
