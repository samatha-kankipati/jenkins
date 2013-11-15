from ccengine.domain.base_domain import BaseMarshallingDomain
import xml.etree.ElementTree as ET
import json


class Link(BaseMarshallingDomain):

    ROOT_TAG = 'link'

    def __init__(self, href=None, rel=None, otherAttributes=None):
        ''' An object specific to usage records to represent pagination links

        '''
        self.otherAttributes = None
        self.href = href
        self.rel = rel

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
        return Link(**dic)
