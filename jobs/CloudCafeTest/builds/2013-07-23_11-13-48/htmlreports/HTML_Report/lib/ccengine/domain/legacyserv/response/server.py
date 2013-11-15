from ccengine.domain.base_domain import BaseMarshallingDomain
from ccengine.domain.base_domain import BaseDomain
import xml.etree.ElementTree as ET
import json


class ServerResponse(BaseMarshallingDomain):
    ROOT_TAG = 'server'

    def __init__(self, progress=None, id=None, imageId=None, flavorId=None,
                  status=None, adminPass=None, name=None, hostId=None,
                 addresses=None, public=None, private=None, metadata=None):

        #Common Attributes
        self.progress = progress
        self.imageId = imageId
        self.flavorId = flavorId
        self.status = status
        self.id = id
        self.adminPass = adminPass
        self.name = name
        self.hostId = hostId
        self.addresses = addresses
        self.public = public
        self.private = private
        self.metadata = metadata

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        if cls.ROOT_TAG not in json_dict:
            return None
        ret = cls._dict_to_obj(json_dict.get(cls.ROOT_TAG))
        return ret

    @classmethod
    def _dict_to_obj(cls, dic):
        if Address.ROOT_TAG in dic:
            address = dic.get(Address.ROOT_TAG)
            dic[Address.ROOT_TAG] = Address._dict_to_obj(address)
        return ServerResponse(**dic)


class Address(BaseMarshallingDomain):

    ROOT_TAG = 'addresses'

    def __init__(self, public=None, private=None):
        self.public = public
        self.private = private

    @classmethod
    def _dict_to_obj(self, dic):
        return Address(**dic)
