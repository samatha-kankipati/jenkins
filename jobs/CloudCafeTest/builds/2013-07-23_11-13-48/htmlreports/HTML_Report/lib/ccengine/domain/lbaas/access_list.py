from ccengine.domain.base_domain import BaseMarshallingDomain, \
    BaseMarshallingDomainList
import json


class AccessList(BaseMarshallingDomainList):

    ROOT_TAG = 'accessList'

    def __init__(self, accessList=[]):
        super(AccessList, self).__init__()
        for item in accessList:
            self.append(item)

    def get_by_id(self, id):
        for item in self:
            if item.id == id:
                return item

    def get_by_address(self, address):
        for item in self:
            if item.address == address:
                return item

    def _obj_to_json(self):
        ret_list = self._obj_to_dict()
        return json.dumps({self.ROOT_TAG: ret_list})

    def _obj_to_dict(self):
        ret_list = [item._obj_to_dict() for item in self]
        return ret_list

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        if cls.ROOT_TAG not in json_dict:
            return None
        json_dict[cls.ROOT_TAG] = cls._dict_to_obj(json_dict.get(cls.ROOT_TAG))
        return AccessList(**json_dict)

    @classmethod
    def _dict_to_obj(cls, dic):
        dic = {cls.ROOT_TAG: [NetworkItem._dict_to_obj(item)
                              for item in dic]}
        return AccessList(**dic)

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        pass


class NetworkItem(BaseMarshallingDomain):

    ROOT_TAG = 'networkItem'

    def __init__(self, address=None, id=None, type=None):
        self.address = address
        self.id = id
        self.type = type

    def _obj_to_json(self):
        pass

    def _obj_to_dict(self):
        ret = {}
        if self.address is not None:
            ret['address'] = self.address
        if self.id is not None:
            ret['id'] = self.id
        if self.type is not None:
            ret['type'] = self.type
        return ret

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        if cls.ROOT_TAG not in json_dict:
            return None
        return NetworkItem._dict_to_obj(json_dict.get(cls.ROOT_TAG))

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        pass

    @classmethod
    def _dict_to_obj(cls, dic):
        return NetworkItem(**dic)
