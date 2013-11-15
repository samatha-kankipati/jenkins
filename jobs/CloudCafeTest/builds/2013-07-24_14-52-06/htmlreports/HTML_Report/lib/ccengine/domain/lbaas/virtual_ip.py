from ccengine.domain.base_domain import BaseMarshallingDomain, \
    BaseMarshallingDomainList
from ccengine.domain.types import LoadBalancerVirtualIpVersions as LBVIP
import json
import xml.etree.ElementTree as ET


class VirtualIpList(BaseMarshallingDomainList):

    ROOT_TAG = 'virtualIps'

    def __init__(self, virtualIps=[]):
        super(VirtualIpList, self).__init__()
        for vip in virtualIps:
            self.append(vip)

    def get_ipv4_vips(self):
        return [vip for vip in self if vip.ipVersion == LBVIP.IPV4]

    def get_ipv6_vips(self):
        return [vip for vip in self if vip.ipVersion == LBVIP.IPV6]

    def _obj_to_json(self):
        return json.dumps(self._obj_to_dict())

    def _obj_to_dict(self):
        return [vip._obj_to_dict() for vip in self]

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        if cls.ROOT_TAG not in json_dict:
            return None
        return cls._dict_to_obj(json_dict.get(cls.ROOT_TAG))

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        pass

    @classmethod
    def _dict_to_obj(cls, vip_dict):
        kwargs = {cls.ROOT_TAG: [VirtualIp._dict_to_obj(vip)
                                 for vip in vip_dict]}
        return VirtualIpList(**kwargs)

    def _auto_value_to_dict(self, value):
        ret = None
        if isinstance(value, (int, str, unicode)):
            ret = value
        elif isinstance(value, list):
            ret = []
            for item in value:
                ret.append(self._auto_value_to_dict(item))
        elif isinstance(value, dict):
            ret = {}
            for key in value.keys():
                ret[key] = self._auto_value_to_dict(value[key])
        elif isinstance(value, BaseMarshallingDomain):
            ret = value._obj_to_dict()
        return ret


class VirtualIp(BaseMarshallingDomain):

    ROOT_TAG = 'virtualIp'

    def __init__(self, id=None, address=None, type=None, ipVersion=None):
        '''An object that represents the data of a Load Balancer Virtual IP.
        '''
        self.id = id
        self.address = address
        self.type = type
        self.ipVersion = ipVersion

    def _obj_to_json(self):
        return json.dumps(self._obj_to_dict())

    def _obj_to_dict(self):
        ret = {}
        if self.id is not None:
            ret['id'] = self.id
        if self.address is not None:
            ret['address'] = self.address
        if self.type is not None:
            ret['type'] = self.type
        if self.ipVersion is not None:
            ret['ipVersion'] = self.ipVersion
        return ret

    def _obj_to_xml(self):
        pass

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        return cls._dict_to_obj(json_dict)

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        pass

    @classmethod
    def _dict_to_obj(cls, dic):
        return VirtualIp(**dic)
