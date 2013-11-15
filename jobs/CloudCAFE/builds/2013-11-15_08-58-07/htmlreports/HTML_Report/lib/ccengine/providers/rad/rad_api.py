from ccengine.providers.base_provider import BaseProvider
from ccengine.clients.rad.flavors_api import FlavorsClient


class RADAPIProvider(BaseProvider):

    """Provider Class for RAD API."""

    def __init__(self, config, logger=None):
        super(RADAPIProvider, self).__init__()
        if config is None:
            self.provider_log.warning('empty (=None) config recieved in init')
        self.config = config
        self.base_url = self.config.rad.base_url
        self.rad_client = FlavorsClient(self.base_url,
                                        self.config.misc.serializer,
                                        self.config.misc.deserializer)
