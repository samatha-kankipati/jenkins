from ccengine.domain.networks.isolated_network import IsolatedNetwork
from ccengine.domain.networks.request.virtual_interface import \
                                VirtualInterface as RequestVirtualInterface
from ccengine.domain.networks.response.virtual_interface import \
                                VirtualInterface as ResponseVirtualInterface
from ccengine.clients.base_client import BaseMarshallingClient


class IsolatedNetworksClient(BaseMarshallingClient):

    _suffix = '/os-networksv2'
    _vi_prefix = '/servers'
    _vi_suffix = '/os-virtual-interfacesv2'

    def __init__(self, url, auth_token, serialize_format,
                 deserialize_format=None):
        super(IsolatedNetworksClient, self).__init__(serialize_format,
                                                     deserialize_format)
        self.url = ''.join([url, self._suffix])
        self.vi_url = '/'.join([url, self._vi_prefix])
        self.auth_token = auth_token
        self.default_headers['X-Auth-Token'] = auth_token
        ct = ''.join(['application/', self.serialize_format])
        accept = ''.join(['application/', self.deserialize_format])
        self.default_headers['Content-Type'] = ct
        self.default_headers['Accept'] = accept

    def list_networks(self, requestslib_kwargs=None):
        return self.request('GET', self.url,
                                  response_entity_type=IsolatedNetwork,
                                  requestslib_kwargs=requestslib_kwargs)

    def get_network(self, network_id, requestslib_kwargs=None):
        full_url = ''.join([self.url, '/', str(network_id)])
        return self.request('GET', full_url,
                                  response_entity_type=IsolatedNetwork,
                                  requestslib_kwargs=requestslib_kwargs)

    def delete_network(self, network_id, requestslib_kwargs=None):
        full_url = ''.join([self.url, '/', str(network_id)])
        return self.request('DELETE', full_url,
                                  response_entity_type=None,
                                  requestslib_kwargs=requestslib_kwargs)

    def create_network(self, cidr=None, label=None, requestslib_kwargs=None):
        n = IsolatedNetwork(cidr=cidr, label=label)
        return self.request('POST', self.url,
                                  response_entity_type=IsolatedNetwork,
                                  request_entity=n,
                                  requestslib_kwargs=requestslib_kwargs)

    def list_virtual_interfaces(self, server_id, requestslib_kwargs=None):
        url = '/'.join([self.vi_url, str(server_id), self._vi_suffix])
        return self.request('GET', url,
                                response_entity_type=ResponseVirtualInterface,
                                  requestslib_kwargs=requestslib_kwargs)

    def create_virtual_interface(self, server_id, network_id,
                                 requestslib_kwargs=None):
        vi = RequestVirtualInterface(network_id=network_id)
        url = '/'.join([self.vi_url, str(server_id), self._vi_suffix])
        return self.request('POST', url,
                              response_entity_type=ResponseVirtualInterface,
                              request_entity=vi,
                              requestslib_kwargs=requestslib_kwargs)

    def delete_virtual_interface(self, server_id, virtual_interface_id,
                                 requestslib_kwargs=None):
        url = '/'.join([self.vi_url, str(server_id), self._vi_suffix,
                        str(virtual_interface_id)])
        return self.request('DELETE', url,
                                  response_entity_type=None,
                                  requestslib_kwargs=requestslib_kwargs)
