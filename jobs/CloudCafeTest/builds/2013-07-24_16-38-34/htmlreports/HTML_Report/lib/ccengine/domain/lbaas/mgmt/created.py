from ccengine.domain.base_domain import BaseMarshallingDomain
import xml.etree.ElementTree as ET
import json


class Created(BaseMarshallingDomain):

    ROOT_TAG = 'created'

    def __init__(self, time=None):
        '''An object describing when a load balancer is created

        '''
        self.time = time

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
        return Created(**dic)
