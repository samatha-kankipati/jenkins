from ccengine.domain.base_domain import BaseMarshallingDomain
import json
import xml.etree.ElementTree as ET


class ConnectionLogging(BaseMarshallingDomain):

    ROOT_TAG = 'connectionLogging'

    def __init__(self, enabled=None):
        self.enabled = enabled

    def _obj_to_json(self):
        return json.dumps({self.ROOT_TAG: self._obj_to_dict()})

    def _obj_to_dict(self):
        return {'enabled': self.enabled}

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        if cls.ROOT_TAG not in json_dict:
            return None
        return cls._dict_to_obj(json_dict.get(cls.ROOT_TAG))

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        pass

    @classmethod
    def _dict_to_obj(cls, dic):
        if ConnectionLogging.ROOT_TAG in dic:
            dic = dic.get(ConnectionLogging.ROOT_TAG)
        return ConnectionLogging(**dic)
