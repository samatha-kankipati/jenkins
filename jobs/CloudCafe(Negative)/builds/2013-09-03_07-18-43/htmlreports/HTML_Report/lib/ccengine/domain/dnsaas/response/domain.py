from ccengine.domain.base_domain import BaseMarshallingDomain
from ccengine.domain.base_domain import BaseDomain
import xml.etree.ElementTree as ET
import json


class Domain(BaseMarshallingDomain):

    def __init__(self, name=None,  emailAddress=None, ttl=None,
                 comment=None, id=None, updated=None,
                  created=None, accountId=None):

        #Common Attributes
        self.name = name
        self.id = id
        self.comment = comment
        self.ttl = ttl
        self.emailAddress = emailAddress
        self.updated = updated
        self.created = created
        self.accountId = accountId

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        ret = None
        if 'domains' in json_dict:
            ret = []
            for domain in json_dict['domains']:
                ret.append(cls._dict_to_obj(domain))
        else:
            ret = cls._dict_to_obj(json_dict)
        return ret

    @classmethod
    def _dict_to_obj(cls, json_dict):
        return Domain(**json_dict)

