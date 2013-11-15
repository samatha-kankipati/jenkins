from ccengine.domain.base_domain import BaseMarshallingDomain
import json
import xml.etree.ElementTree as ET


class ErrorPage(BaseMarshallingDomain):

    ROOT_TAG = 'errorpage'

    def __init__(self, content=None):
        self.content = content

    def _obj_to_json(self):
        ret = self._auto_to_dict()
        return json.dumps(ret)

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
        return ErrorPage(**dic)
