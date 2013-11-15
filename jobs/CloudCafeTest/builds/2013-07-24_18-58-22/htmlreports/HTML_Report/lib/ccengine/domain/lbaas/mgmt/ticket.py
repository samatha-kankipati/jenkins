from ccengine.domain.base_domain import BaseMarshallingDomain, \
    BaseMarshallingDomainList
import xml.etree.ElementTree as ET
import json


class TicketList(BaseMarshallingDomainList):

    ROOT_TAG = 'tickets'

    def __init__(self, tickets=None):
        '''An object that data concerning tickets on a load balancer.

        '''
        for ticket in tickets:
            self.append(ticket)

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
        kwargs = {cls.ROOT_TAG: [Ticket._dict_to_obj(ticket)
                                 for ticket in dic]}
        return TicketList(**kwargs)


class Ticket(BaseMarshallingDomain):

    ROOT_TAG = 'ticket'

    def __init__(self, comment=None, id=None, ticketId=None):
        '''An object that data concerning tickets on a load balancer.

        '''
        self.comment = comment
        self.id = id
        self.ticketId = ticketId

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
        return Ticket(**dic)
