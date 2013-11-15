'''
@summary: Provider Module for Compute Isolated Networks
@note: Should be the primary interface to a test case or external tool.
@copyright: Copyright (c) 2012 Rackspace US, Inc.
'''
from ccengine.providers.base_provider import BaseProvider
from ccengine.clients.networks.isolated_networks import IsolatedNetworksClient
from ccengine.providers.auth.auth_api import AuthProvider as _AuthProvider
from ccengine.common.constants.networks_constants import Constants
from ccengine.common.constants.networks_constants import HTTPResponseCodes
from ccengine.common.tools import datagen


class IsolatedNetworksProvider(BaseProvider):

    def __init__(self, config, logger):
        '''
        Sets config, sets up client, sets deserializer and serializer based
        on format defined in the config.
        '''
        super(IsolatedNetworksProvider, self).__init__()
        self._public_network = None
        self._private_network = None
        self.config = config
        self.auth_provider = _AuthProvider(self.config)
        auth_data = self.auth_provider.authenticate()
        service_name = config.isolated_networks_api.identity_service_name
        region = config.isolated_networks_api.region
        service = auth_data.get_service(service_name)
        url = service.get_endpoint_by_region(region).publicURL
        self.client = IsolatedNetworksClient(url, auth_data.token.id,
                                             config.misc.serializer,
                                             config.misc.deserializer)

    def get_public_network(self):
        if self._public_network is None:
            r = self.client.list_networks()
            msg = 'Unable to list networks to get public: {0} {1} {2}'.format(
                r.status_code, r.reason, r.content)
            assert HTTPResponseCodes.LIST_NETWORKS == r.status_code, msg
            network_list = r.entity
            for network in network_list:
                if network.id == Constants.PUBLIC_NETWORK_ID:
                    self._public_network = network
        return self._public_network

    def get_private_network(self):
        if self._private_network is None:
            r = self.client.list_networks()
            msg = 'Unable to list networks to get private: {0} {1} {2}'.format(
                r.status_code, r.reason, r.content)
            assert HTTPResponseCodes.LIST_NETWORKS == r.status_code, msg
            network_list = r.entity
            for network in network_list:
                if network.id == Constants.PRIVATE_NETWORK_ID:
                    self._private_network = network
        return self._private_network

    def get_public_interface(self, server_id):
        ret = None
        resp = self.client.list_virtual_interfaces(server_id)
        msg = 'Unable to list virtual interfaces: {0} {1} {2}'.format(
            resp.status_code, resp.reason, resp.content)
        assert HTTPResponseCodes.LIST_INTERFACES == resp.status_code, msg
        interfaces = resp.entity
        if interfaces is not None:
            for interface in interfaces:
                #TODO: Change this to check for public id
                if interface.ip_addresses[0].network_label == 'public':
                    ret = interface
                    break
        return ret

    def get_private_interface(self, server_id):
        ret = None
        resp = self.client.list_virtual_interfaces(server_id)
        msg = 'Unable to list virtual interfaces: {0} {1} {2}'.format(
            resp.status_code, resp.reason, resp.content)
        assert HTTPResponseCodes.LIST_INTERFACES == resp.status_code, msg
        interfaces = resp.entity
        if interfaces is not None:
            for interface in interfaces:
                #TODO: Change this to check for private id
                if interface.ip_addresses[0].network_label == 'private':
                    ret = interface
                    break
        return ret

    def get_interface(self, server_id, network_id):
        ret = None
        resp = self.client.list_virtual_interfaces(server_id)
        msg = 'Unable to list virtual interfaces: {0} {1} {2}'.format(
            resp.status_code, resp.reason, resp.content)
        assert HTTPResponseCodes.LIST_INTERFACES == resp.status_code, msg
        interfaces = resp.entity
        if interfaces is not None:
            for interface in interfaces:
                if interface.ip_addresses[0].network_id == network_id:
                    ret = interface
                    break
        return ret

    def get_server_network_dd(self, network_list):
        """Converts simple networks id list to a list of uuids dictionaries
           as expected by the create server call"""
        if isinstance(network_list, str):
            network_list = [network_list]
        assert isinstance(network_list, list), 'List or Str type expected'
        data_dict_list = []
        for i in range(len(network_list)):
            temp_dict = {'uuid': network_list[i]}
            data_dict_list.append(temp_dict)
        return data_dict_list

    def get_new_ip(self, ip_list, new_ip_list):
        """Return the added IP in the new_ip_list"""
        new_ip = None
        for ip in new_ip_list:
            if ip not in ip_list:
                new_ip = ip
        return new_ip

    def create_ipv4_network(self, name_starts_with='test_net',
                            prefix='177.*.*.0', suffix='24'):
        """Creates an IPv4 isolated network"""
        kwargs = dict()
        if prefix is not None and suffix is not None:
            kwargs['ip_pattern'] = prefix
            kwargs['mask'] = suffix
        elif suffix is not None:
            kwargs['mask'] = suffix
        elif prefix is not None:
            kwargs['ip_pattern'] = prefix
        cidr = datagen.random_cidr(**kwargs)

        name = datagen.rand_name(name_starts_with)
        resp = self.client.create_network(cidr=cidr, label=name)
        assert resp.status_code == HTTPResponseCodes.CREATE_NETWORK, \
            'Test Network Create failed: {0} {1} {2}'.format(
                resp.status_code, resp.reason, resp.content)
        return resp.entity
