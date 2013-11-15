from ccengine.domain.base_domain import BaseMarshallingDomain, \
    BaseMarshallingDomainList
import xml.etree.ElementTree as ET
import json


class Blacklist(BaseMarshallingDomainList):

    ROOT_TAG = 'blacklistItems'

    def __init__(self, blacklistItems=None):
        '''An object that holds information about the number of accounts in a
                host
        '''
        for item in blacklistItems:
            self.append(item)

    def _obj_to_json(self):
        ret = {self.ROOT_TAG: [item._obj_to_dict() for item in self]}
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
        kwargs = {cls.ROOT_TAG: [BlacklistItem._dict_to_obj(item)
                                 for item in dic]}
        return Blacklist(**kwargs)


class BlacklistItem(BaseMarshallingDomain):

    ROOT_TAG = 'blacklistItem'

    def __init__(self, id=None, cidrBlock=None, ipVersion=None, type=None):
        '''An object to hold information about a single account on a host

        '''
        self.id = id
        self.cidrBlock = cidrBlock
        self.ipVersion = ipVersion
        self.type = type

    def _obj_to_json(self):
        ret = self._auto_to_dict()
        return json.dumps(ret[self.ROOT_TAG])

    def _obj_to_dict(self):
        dic = {}
        if self.id is not None:
            dic['id'] = self.id
        if self.cidrBlock is not None:
            dic['cidrBlock'] = self.cidrBlock
        if self.ipVersion is not None:
            dic['ipVersion'] = self.ipVersion
        if self.type is not None:
            dic['type'] = self.type
        return dic

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
        return BlacklistItem(**dic)
