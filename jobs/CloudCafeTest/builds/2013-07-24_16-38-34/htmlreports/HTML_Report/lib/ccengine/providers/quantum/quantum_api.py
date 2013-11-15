'''
@summary: Provider Module for Quantum Networks
@copyright: Copyright (c) 2012 Rackspace US, Inc.
'''
import json
import inspect
import ccengine.common.tools.datagen as datagen
from ccengine.domain.quantum.response.network import Network
from ccengine.providers.base_provider import BaseProvider
from ccengine.clients.quantum.quantum_api import QuantumClient
from ccengine.providers.auth.auth_api import AuthProvider as _AuthProvider
from ccengine.common.constants.networks_constants import QuantumResponseCodes


class QuantumProvider(BaseProvider):

    def __init__(self, config, logger):
        '''Initializes the Quantum Provider with config data'''
        super(QuantumProvider, self).__init__()
        self.config = config
        self.auth_provider = _AuthProvider(self.config)
        auth_data = self.auth_provider.authenticate()
        url = config.quantum_api.endpoint
        self.client = QuantumClient(url, auth_data.token.id,
                                            config.misc.serializer,
                                            config.misc.deserializer)
        self.network_args = inspect.getargspec(Network.__init__).args

    def get_network_by_kwarg(self, key, value, starts_with=None,
                             networks=None):
        """List Networks that match a Key Value"""
        if key not in self.network_args:
            return None

        # If the user does not provide a network list
        if networks is None:
            resp = self.client.list_networks()
            assert resp.status_code == QuantumResponseCodes.LIST_NETWORKS, \
                       'List Networks API call failed {0}'.format(resp.content)
            net_list = resp.entity
        # If the user provides the network list
        else:
            net_list = networks
        kw_list = []
        for net in net_list:
            net_value = getattr(net, key)
            if net_value == value:
                kw_list.append(net)
            # allows a starts with search
            elif starts_with:
                # to enable boolean values
                net_value_str = str(net_value)
                if net_value_str.startswith(str(value)):
                    kw_list.append(net)
        # return the network object list of the key value match
        return kw_list

    def get_attr_list(self, obj_list, attr):
        """Get an attribute list from an object list"""
        attr_list = []
        for obj in obj_list:
            value = getattr(obj, attr)
            attr_list.append(value)
        return attr_list

    def delete_network_list(self, id_list):
        """Deletes a list of networks without ports given an id list"""
        not_deleted = []
        for net_id in id_list:
            resp = self.client.delete_network(net_id)
            if resp.status_code != QuantumResponseCodes.DELETE_NETWORK:
                error_data = json.loads(resp.content)
                error_data.update(dict(id=net_id))
                not_deleted.append(error_data)
        # dict list of undeleted networks with id and reason
        return not_deleted

    def delete_networks_by_kwargs(self, key, value):
        """Deletes networks without ports by key values"""
        networks = self.get_network_by_kwarg(key, value, True)
        net_list = self.get_attr_list(networks, 'id')
        not_deleted = self.delete_network_list(net_list)
        resul = dict(to_delete=len(net_list), deleted=len(net_list) - \
                      len(not_deleted), not_deleted=not_deleted)
        # dict with to delete and deleted counts and not deleted network ids
        return resul

    def create_n_networks(self, n, name_startswith='q_network'):
        """Creates n quantum networks"""
        net_list = []
        error_list = []
        for _ in range(n):
            name = datagen.rand_name(name_startswith)
            resp = self.client.create_network(name=name)
            if resp.status_code == QuantumResponseCodes.CREATE_NETWORK:
                net_list.append(resp.entity)
            else:
                error = dict(status=resp.status_code, reason=resp.reason, 
                             content=resp.content)
                error_list.append(error)
        resul = dict(count=len(net_list), networks=net_list, errors=error_list)
        # dict with created networks count and obj list
        return resul
