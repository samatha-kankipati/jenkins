'''
@summary: Domain Object Class for Quantum Subnets requests
@copyright: Copyright (c) 2013 Rackspace US, Inc.
@author: leon0944
'''
from ccengine.domain.base_domain import BaseMarshallingDomain
import json


class Subnet(BaseMarshallingDomain):

    ROOT_TAG = 'subnet'

    def __init__(self, network_id, cidr, ip_version, name=None,
                 gateway_ip=None, allocation_pools=None, enable_dhcp=None,
                 dns_nameservers=None, host_routes=None, tenant_id=None,
                 id=None):
        super(Subnet, self).__init__()
        self.network_id = network_id
        self.cidr = cidr
        self.name = name
        self.ip_version = ip_version
        self.gateway_ip = gateway_ip
        self.allocation_pools = allocation_pools
        self.enable_dhcp = enable_dhcp
        self.dns_nameservers = dns_nameservers
        self.host_routes = host_routes
        self.tenant_id = tenant_id
        self.id = id

    def _obj_to_json(self):
        ret = self._auto_to_dict()
        return json.dumps(ret)

    def _obj_to_xml(self):
        """Not implemented in Quantum v2.0"""
        pass
