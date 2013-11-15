'''
@summary: Domain Object Class for Quantum Subnets responses
@copyright: Copyright (c) 2013 Rackspace US, Inc.
@author: leon0944
'''
import json
from ccengine.domain.base_domain import BaseMarshallingDomain


class Subnet(BaseMarshallingDomain):

    ROOT_TAG = 'subnet'

    def __init__(self, ip_version=None, enable_dhcp=None, network_id=None,
                 dns_nameservers=None, tenant_id=None, gateway_ip=None,
                 id=None, cidr=None, host_routes=None, name=None,
                 allocation_pools=None):
        super(Subnet, self).__init__()
        self.ip_version = ip_version
        self.enable_dhcp = enable_dhcp
        self.network_id = network_id
        self.dns_nameservers = dns_nameservers
        self.tenant_id = tenant_id
        self.gateway_ip = gateway_ip
        self.id = id
        self.cidr = cidr
        self.host_routes = host_routes
        self.name = name
        self.allocation_pools = allocation_pools

    @classmethod
    def _json_to_obj(cls, serialized_str):
        ret = None
        json_resp = json.loads(serialized_str)

        if 'subnets' in json_resp:
            ret = []
            for subnet in json_resp.get('subnets'):
                ret.append(Subnet(**subnet))

        elif 'subnet' in json_resp:
            subnet_dict = json_resp.get('subnet')
            ret = Subnet(**subnet_dict)

        return ret

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        """Not implemented in Quantum v2.0"""
        pass
