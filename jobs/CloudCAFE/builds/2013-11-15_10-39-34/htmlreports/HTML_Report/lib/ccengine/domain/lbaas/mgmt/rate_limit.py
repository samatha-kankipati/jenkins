from ccengine.domain.base_domain import BaseMarshallingDomain
import xml.etree.ElementTree as ET
from ccengine.domain.lbaas.mgmt.ticket import Ticket
from ccengine.domain.lbaas.mgmt.ticket import TicketList
import json


class RateLimit(BaseMarshallingDomain):

    ROOT_TAG = 'rateLimit'

    def __init__(self, expirationTime=None, maxRequestsPerSecond=None,
                 ticket=None):
        '''An object to describe the non-standard rate limit of requests on a
                load balancer
        '''
        self.expirationTime = expirationTime
        self.maxRequestsPerSecond = maxRequestsPerSecond
        self.ticket = ticket

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
        if Ticket.ROOT_TAG in dic:
            dic[Ticket.ROOT_TAG] = Ticket._dict_to_obj(
                dic.get(Ticket.ROOT_TAG))
        if TicketList.ROOT_TAG in dic:
            dic[TicketList.ROOT_TAG] = \
                TicketList._dict_to_obj(dic.get(TicketList.ROOT_TAG))
        return RateLimit(**dic)


class GroupList(BaseMarshallingDomain):

    ROOT_TAG = 'groups'

    def __init__(self, groups):
        '''An object providing a list of allowed domains

        '''
        self.groups = groups

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
        if Group.ROOT_TAG in dic:
            dic[Group.ROOT_TAG] = Group._dict_to_obj(dic.get(Group.ROOT_TAG))
        return GroupList(**dic)


class Group(BaseMarshallingDomain):

    ROOT_TAG = 'group'

    def __init__(self, name, default=None, id=None):
        '''An object to describe an allowed domain

        '''
        self.name = name
        self.default = default
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
        return Group(**dic)
