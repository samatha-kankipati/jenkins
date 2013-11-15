from ccengine.domain.base_domain import BaseMarshallingDomain, \
    BaseMarshallingDomainList
from ccengine.domain.lbaas.mgmt.ticket import Ticket
import xml.etree.ElementTree as ET
import json


class VirtualIpBlockList(BaseMarshallingDomainList):

    ROOT_TAG = 'virtualIpBlocks'

    def __init__(self, type=None, virtualIpBlocks=None):
        '''A management virtual ip block list object

        '''
        self.type = type
        for vipBlock in virtualIpBlocks:
            self.append(vipBlock)

    def _obj_to_json(self):
        ret = self._auto_to_dict()
        return json.dumps(ret[self.ROOT_TAG])

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
        kwargs = {cls.ROOT_TAG: [VirtualIpBlock._dict_to_obj(vipBlock)
                                 for vipBlock in dic]}
        return VirtualIpBlockList(**kwargs)


class VirtualIpBlock(BaseMarshallingDomain):

    ROOT_TAG = 'virtualIpBlock'

    def __init__(self, firstIp=None, lastIp=None):
        '''A management virtual ip block object

        '''
        self.firstIp = firstIp
        self.lastIp = lastIp

    def _obj_to_json(self):
        ret = self._auto_to_dict()
        return json.dumps(ret[self.ROOT_TAG])

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
        return VirtualIp(**dic)
