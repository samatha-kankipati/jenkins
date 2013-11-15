from ccengine.domain.base_domain import BaseMarshallingDomain
import json
import xml.etree.ElementTree as ET


class AssignVIP(BaseMarshallingDomain):

    ROOT_TAG = 'virtualIp'

    def __init__(self, type=None, ticket=None):
        '''An object that represents the data of a Load Balancer usage.

        '''
        self.type = type
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
        ret = cls._dict_to_obj(json_dict)
        return ret

    @classmethod
    def _dict_to_obj(cls, dic):
        return AssignVIP(**dic)
