from ccengine.domain.base_domain import BaseMarshallingDomain
from ccengine.domain.lbaas.mgmt.ticket import Ticket
import xml.etree.ElementTree as ET
import json


class Suspension(BaseMarshallingDomain):

    ROOT_TAG = 'suspension'

    def __init__(self, reason=None, user=None, ticket=None, id=None):
        '''An object used to provide information about a load balancer's
           suspensions.
        '''
        self.reason = reason
        self.user = user
        self.ticket = ticket
        self.id = id

    def _obj_to_json(self):
        ret = self._auto_to_dict()
        return json.dumps(ret[self.ROOT_TAG])

    def _obj_to_xml(self):
        ret = self._auto_to_xml()
#        for meta in ret.iter('metadata'):
#            meta.tag = 'meta'
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
        if Ticket.ROOT_TAG in dic:
            dic[Ticket.ROOT_TAG] = Ticket._dict_to_obj(dic.get(
                Ticket.ROOT_TAG))
        return Suspension(**dic)
