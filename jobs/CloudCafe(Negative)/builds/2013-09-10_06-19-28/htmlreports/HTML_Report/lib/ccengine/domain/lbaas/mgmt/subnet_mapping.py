from ccengine.domain.base_domain import BaseMarshallingDomain, \
    BaseMarshallingDomainList
import xml.etree.ElementTree as ET
import json


class HostSubnetList(BaseMarshallingDomainList):

    ROOT_TAG = 'hostsubnets'

    def __init__(self, hostsubnets=None):
        '''An object that data concerning tickets on a load balancer.

        '''
        for subnet in hostsubnets:
            self.append(subnet)

    def _obj_to_json(self):
        ret = {self.ROOT_TAG: [hostsubnet._obj_to_dict()
                               for hostsubnet in self]}
        return json.dumps(ret)

    def _obj_to_xml(self):
        ret = self._auto_to_xml()
        return ET.tostring(ret)

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        return cls._dict_to_obj(json_dict.get(cls.ROOT_TAG))

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        pass

    @classmethod
    def _dict_to_obj(cls, dic):
        kwargs = {cls.ROOT_TAG: [HostSubnet._dict_to_obj(hostSubnet)
                                 for hostSubnet in dic]}
        return HostSubnetList(**kwargs)


class HostSubnet(BaseMarshallingDomain):

    ROOT_TAG = 'hostsubnet'

    def __init__(self, name=None, netInterfaces=None):
        '''An object that data concerning tickets on a load balancer.

        '''
        self.name = name
        self.netInterfaces = netInterfaces

    def _obj_to_json(self):
        ret = self._obj_to_dict()
        return json.dumps(ret[self.ROOT_TAG])

    def _obj_to_dict(self):
        ret = {}
        if self.name is not None:
            ret['name'] = self.name
        ret['netInterfaces'] = [netInterface._obj_to_dict()
                                for netInterface in self.netInterfaces]
        return ret

    def _obj_to_xml(self):
        ret = self._auto_to_xml()
        return ET.tostring(ret)

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        return cls._dict_to_obj(json_dict)

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        pass

    @classmethod
    def _dict_to_obj(cls, dic):
        if NetInterfaceList.ROOT_TAG in dic:
            dic[NetInterfaceList.ROOT_TAG] = NetInterfaceList._dict_to_obj(
                dic.get(NetInterfaceList.ROOT_TAG))
        return HostSubnet(**dic)


class NetInterfaceList(BaseMarshallingDomainList):

    ROOT_TAG = 'netInterfaces'

    def __init__(self, netInterfaces=None):
        '''An object that data concerning tickets on a load balancer.

        '''
        for netInterface in netInterfaces:
            self.append(netInterface)

    def _obj_to_json(self):
        ret = {self.ROOT_TAG: self._obj_to_dict()}
        return json.dumps(ret)

    def _obj_to_dict(self):
        ret = [netInterface._obj_to_dict() for netInterface in self]
        return ret

    def _obj_to_xml(self):
        ret = self._auto_to_xml()
        return ET.tostring(ret)

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        return cls._dict_to_obj(json_dict.get(cls.ROOT_TAG))

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        pass

    @classmethod
    def _dict_to_obj(cls, dic):
        kwargs = {cls.ROOT_TAG: [NetInterface._dict_to_obj(netInterface)
                                 for netInterface in dic]}
        return NetInterfaceList(**kwargs)


class NetInterface(BaseMarshallingDomain):

    ROOT_TAG = 'netInterface'

    def __init__(self, cidrs=None, name=None):
        '''An object that data concerning tickets on a load balancer.

        '''
        self.name = name
        self.cidrs = cidrs

    def _obj_to_json(self):
        ret = self._obj_to_dict()
        return json.dumps(ret[self.ROOT_TAG])

    def _obj_to_dict(self):
        ret = {}
        if self.name is not None:
            ret['name'] = self.name
        ret['cidrs'] = [cidr._obj_to_dict() for cidr in self.cidrs]
        return ret

    def _obj_to_xml(self):
        ret = self._auto_to_xml()
        return ET.tostring(ret)

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        return cls._dict_to_obj(json_dict)

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        pass

    @classmethod
    def _dict_to_obj(cls, dic):
        if CidrList.ROOT_TAG in dic:
            dic[CidrList.ROOT_TAG] = CidrList._dict_to_obj(
                dic.get(CidrList.ROOT_TAG))
        return NetInterface(**dic)


class CidrList(BaseMarshallingDomainList):

    ROOT_TAG = 'cidrs'

    def __init__(self, cidrs=None):
        '''An object that data concerning tickets on a load balancer.

        '''
        for cidr in cidrs:
            self.append(cidr)

    def _obj_to_json(self):
        ret = {self.ROOT_TAG: self._obj_to_dict()}
        return json.dumps(ret)

    def _obj_to_dict(self):
        ret = [cidr._obj_to_dict() for cidr in self]
        return ret

    def _obj_to_xml(self):
        ret = self._auto_to_xml()
        return ET.tostring(ret)

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        return cls._dict_to_obj(json_dict.get(cls.ROOT_TAG))

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        pass

    @classmethod
    def _dict_to_obj(cls, dic):
        kwargs = {cls.ROOT_TAG: [Cidr._dict_to_obj(cidr)
                                 for cidr in dic]}
        return CidrList(**kwargs)


class Cidr(BaseMarshallingDomain):

    ROOT_TAG = 'cidr'

    def __init__(self, block=None):
        '''An object that data concerning tickets on a load balancer.

        '''
        self.block = block

    def _obj_to_json(self):
        ret = self._obj_to_dict()
        return json.dumps(ret[self.ROOT_TAG])

    def _obj_to_dict(self):
        ret = {}
        if self.block is not None:
            ret['block'] = self.block
        return ret

    def _obj_to_xml(self):
        ret = self._auto_to_xml()
        return ET.tostring(ret)

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        return cls._dict_to_obj(json_dict)

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        pass

    @classmethod
    def _dict_to_obj(cls, dic):
        return Cidr(**dic)
