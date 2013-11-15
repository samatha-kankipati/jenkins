from ccengine.clients.base_client import BaseMarshallingClient
from ccengine.domain.compute.response.admin import Hosts

class HypervisorsAPIClient(BaseMarshallingClient):

    def __init__(self, url, auth_token, serialize_format=None,
                 deserialize_format=None):
        '''
        @param logger: PBLogger instance to use,
         Generates private logger if None
        @type logger: L{PBLogger}
        '''
        super(HypervisorsAPIClient, self).__init__(serialize_format,
                                                   deserialize_format)
        self.auth_token = auth_token
        self.default_headers['X-Auth-Token'] = auth_token
        ct = ''.join(['application/', self.serialize_format])
        accept = ''.join(['application/', self.deserialize_format])
        self.default_headers['Content-Type'] = ct
        self.default_headers['Accept'] = accept
        self.url = url

    def list_hypervisors(self, requestslib_kwargs=None):
        url = '%s/os-hypervisors' % self.url
        hypervisors = self.request('GET', url,
                                       response_entity_type=Hosts,
                                       requestslib_kwargs=requestslib_kwargs)
        return hypervisors

