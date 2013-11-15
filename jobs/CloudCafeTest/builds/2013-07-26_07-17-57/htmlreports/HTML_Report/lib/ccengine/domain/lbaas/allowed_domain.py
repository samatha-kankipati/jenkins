from ccengine.domain.base_domain import BaseMarshallingDomain, \
    BaseMarshallingDomainList
import json
import xml.etree.ElementTree as ET


class AllowedDomainList(BaseMarshallingDomainList):

    ROOT_TAG = 'allowedDomains'

    def __init__(self, allowedDomains=[]):
        super(AllowedDomainList, self).__init__()
        for allowedDomain in allowedDomains:
            self.append(allowedDomain)

    def _obj_to_json(self):
        ret = self._auto_to_dict()
        return json.dumps(ret[self.ROOT_TAG])

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
    def _dict_to_obj(cls, node_dict):
        kwargs = {cls.ROOT_TAG: [AllowedDomain._dict_to_obj(node)
                                 for node in node_dict]}
        return AllowedDomainList(**kwargs)


class AllowedDomain(BaseMarshallingDomain):

    ROOT_TAG = 'allowedDomain'

    def __init__(self, name=None):
        self.name = name

    def _obj_to_json(self):
        ret = self._auto_to_dict()
        return json.dumps(ret[self.ROOT_TAG])

    @classmethod
    def _json_to_obj(cls, serialized_str):
        ret = None
        json_dict = json.loads(serialized_str)
        if json_dict.get(cls.ROOT_TAG) is not None:
            ret = cls._dict_to_obj(json_dict.get(cls.ROOT_TAG))
        return ret

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        pass

    @classmethod
    def _dict_to_obj(cls, dic):
        if cls.ROOT_TAG in dic:
            dic = dic[cls.ROOT_TAG]
        return AllowedDomain(**dic)
