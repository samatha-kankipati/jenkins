from ccengine.domain.base_domain import BaseMarshallingDomain, \
    BaseMarshallingDomainList
import json
import xml.etree.ElementTree as ET


class Metadata(BaseMarshallingDomainList):

    ROOT_TAG = 'metadata'

    def __init__(self, metadata=[]):
        super(Metadata, self).__init__()
        for meta in metadata:
            self.append(meta)

    def get_meta(self, key, default=None):
        for meta in self:
            if meta.key == key:
                return meta
        return default

    def get(self, key, default=None):
        for meta in self:
            if meta.key == key:
                return meta.value
        return default

    def _obj_to_json(self):
        return json.dumps({self.ROOT_TAG: self._obj_to_dict()})

    def _obj_to_dict(self):
        return [meta._obj_to_dict() for meta in self]

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        if cls.ROOT_TAG not in json_dict:
            return None
        return cls._dict_to_obj(json_dict.get(cls.ROOT_TAG))

    @classmethod
    def _dict_to_obj(cls, meta_dict):
        kwargs = {cls.ROOT_TAG: [Meta._dict_to_obj(meta)
                                 for meta in meta_dict]}
        return Metadata(**kwargs)

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        pass


class Meta(BaseMarshallingDomain):

    ROOT_TAG = 'meta'

    def __init__(self, id=None, key=None, value=None):
        self.id = id
        self.key = key
        self.value = value

    def _obj_to_json(self):
        return json.dumps({self.ROOT_TAG: self._obj_to_dict()})

    def _obj_to_dict(self):
        ret = {}
        if self.id is not None:
            ret['id'] = self.id
        if self.key is not None:
            ret['key'] = self.key
        if self.value is not None:
            ret['value'] = self.value
        return ret

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
        return Meta(**dic)
