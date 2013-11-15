from ccengine.clients.base_client import BaseMarshallingClient
from ccengine.domain.quantum.request.network import Network as RequestNetwork
from ccengine.domain.quantum.response.network import Network as ResponseNetwork
from ccengine.domain.quantum.request.subnet import Subnet as RequestSubnet
from ccengine.domain.quantum.response.subnet import Subnet as ResponseSubnet


class QuantumClient(BaseMarshallingClient):

    _networks_suffix = '/networks'
    _subnets_suffix = '/subnets'
    _ports_suffix = '/ports'

    def __init__(self, url, auth_token, serialize_format,
                 deserialize_format=None):
        super(QuantumClient, self).__init__(serialize_format,
                                            deserialize_format)
        self.networks_url = '{0}{1}'.format(url, self._networks_suffix)
        self.subnets_url = '{0}{1}'.format(url, self._subnets_suffix)
        self.ports_url = '{0}{1}'.format(url, self._ports_suffix)
        self.auth_token = auth_token
        self.default_headers['X-Auth-Token'] = auth_token
        ct = 'application/{0}'.format(self.serialize_format)
        accept = 'application/{0}'.format(self.deserialize_format)
        self.default_headers['Content-Type'] = ct
        self.default_headers['Accept'] = accept

    def list_networks(self, requestslib_kwargs=None):
        return self.request('GET', self.networks_url,
                            response_entity_type=ResponseNetwork,
                            requestslib_kwargs=requestslib_kwargs)

    def create_network(self, name, admin_state_up=None, shared=None,
                       tenant_id=None, requestslib_kwargs=None):
        network = RequestNetwork(name=name, admin_state_up=admin_state_up,
                                 shared=shared, tenant_id=tenant_id)
        return self.request('POST', self.networks_url,
                            response_entity_type=ResponseNetwork,
                            request_entity=network,
                            requestslib_kwargs=requestslib_kwargs)

    def delete_network(self, network_id, requestslib_kwargs=None):
        full_url = '{0}/{1}'.format(self.networks_url, str(network_id))
        return self.request('DELETE', full_url,
                            response_entity_type=None,
                            requestslib_kwargs=requestslib_kwargs)

    def show_network(self, network_id, requestslib_kwargs=None):
        full_url = '{0}/{1}'.format(self.networks_url, str(network_id))
        return self.request('GET', full_url,
                            response_entity_type=ResponseNetwork,
                            requestslib_kwargs=requestslib_kwargs)

    def update_network(self, network_id, name=None, admin_state_up=None,
                       shared=None, tenant_id=None, status=None, new_id=None,
                       requestslib_kwargs=None):
        network = RequestNetwork(name=name, admin_state_up=admin_state_up,
                                 shared=shared, tenant_id=tenant_id,
                                 status=status, id=new_id)
        full_url = '{0}/{1}'.format(self.networks_url, str(network_id))
        return self.request('PUT', full_url,
                            request_entity=network,
                            response_entity_type=ResponseNetwork,
                            requestslib_kwargs=requestslib_kwargs)

    def list_subnets(self, requestslib_kwargs=None):
        return self.request('GET', self.subnets_url,
                            response_entity_type=ResponseSubnet,
                            requestslib_kwargs=requestslib_kwargs)

    def show_subnet(self, subnet_id, requestslib_kwargs=None):
        full_url = '{0}/{1}'.format(self.subnets_url, str(subnet_id))
        return self.request('GET', full_url,
                            response_entity_type=ResponseSubnet,
                            requestslib_kwargs=requestslib_kwargs)

    def create_subnet(self, network_id, cidr, ip_version, name=None,
                      gateway_ip=None, allocation_pools=None, enable_dhcp=None,
                      host_routes=None, dns_nameservers=None,
                      requestslib_kwargs=None):

        subnet = RequestSubnet(network_id=network_id, cidr=cidr,
                               ip_version=ip_version, name=name,
                               gateway_ip=gateway_ip,
                               allocation_pools=allocation_pools,
                               enable_dhcp=enable_dhcp)
        return self.request('POST', self.subnets_url,
                            response_entity_type=ResponseSubnet,
                            request_entity=subnet,
                            requestslib_kwargs=requestslib_kwargs)

    def update_subnet(self, subnet_id, name=None, gateway_ip=None,
                      dns_nameservers=None, host_routes=None, enable_dhcp=None,
                      tenant_id=None, network_id=None, cidr=None,
                      ip_version=None, allocation_pools=None, new_id=None,
                      requestslib_kwargs=None):

        # network_id, cidr, ip_version and allocation_pools to be used for
        # negative testing, if part of an update call an error is expected
        subnet = RequestSubnet(name=name, gateway_ip=gateway_ip,
                      dns_nameservers=dns_nameservers, host_routes=host_routes,
                      enable_dhcp=enable_dhcp, tenant_id=tenant_id,
                      network_id=network_id, cidr=cidr, ip_version=ip_version,
                      allocation_pools=allocation_pools, id=new_id)
        full_url = '{0}/{1}'.format(self.subnets_url, str(subnet_id))
        return self.request('PUT', full_url,
                            request_entity=subnet,
                            response_entity_type=ResponseSubnet,
                            requestslib_kwargs=requestslib_kwargs)

    def delete_subnet(self, subnet_id, requestslib_kwargs=None):
        full_url = '{0}/{1}'.format(self.subnets_url, str(subnet_id))
        return self.request('DELETE', full_url,
                            response_entity_type=None,
                            requestslib_kwargs=requestslib_kwargs)
