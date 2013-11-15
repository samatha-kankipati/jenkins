from ccengine.domain.base_domain import BaseMarshallingDomain
from ccengine.domain.base_domain import BaseMarshallingDomainList
import xml.etree.ElementTree as ET
from ccengine.domain.lbaas.mgmt.ticket import Ticket
from ccengine.domain.lbaas.mgmt.ticket import TicketList
import json


class AbsoluteLimits(BaseMarshallingDomain):

    ROOT_TAG = 'allAbsoluteLimits'

    def __init__(self, customLimits=None, defaultLimits=None):
        '''An object to describe the non-standard rate limit of requests on a
                load balancer
        '''
        self.customLimits = customLimits
        self.defaultLimits = defaultLimits

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
        ### Handling nested objects; in this case, Ticket is an object of
        ###     Rate Limit
        if CustomLimitList.ROOT_TAG in dic:
            dic[CustomLimitList.ROOT_TAG] = \
                CustomLimitList._dict_to_obj(dic.get(CustomLimitList.ROOT_TAG))
        if DefaultLimitList.ROOT_TAG in dic:
            dic[DefaultLimitList.ROOT_TAG] = \
                DefaultLimitList._dict_to_obj(
                    dic.get(DefaultLimitList.ROOT_TAG))
        return AbsoluteLimits(**dic)


class CustomLimitList(BaseMarshallingDomainList):

    ROOT_TAG = 'customLimits'

    def __init__(self, customLimits=None):
        '''An object providing a list of allowed domains

        '''
        for limit in customLimits:
            self.append(limit)

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
        kwargs = {cls.ROOT_TAG: [Limit._dict_to_obj(limit) for limit in dic]}
        return CustomLimitList(**kwargs)


class DefaultLimitList(BaseMarshallingDomainList):

    ROOT_TAG = 'defaultLimits'

    def __init__(self, defaultLimits=None):
        '''An object providing a list of allowed domains

        '''
        for limit in defaultLimits:
            self.append(limit)

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
        kwargs = {cls.ROOT_TAG: [Limit._dict_to_obj(limit) for limit in dic]}
        return DefaultLimitList(**kwargs)


class Limit(BaseMarshallingDomain):

    ROOT_TAG = 'limit'

    def __init__(self, name=None, value=None, id=None):
        '''An object to describe an allowed domain

        '''
        self.value = value
        self.name = name
        self.id = id

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
        return Limit(**dic)
