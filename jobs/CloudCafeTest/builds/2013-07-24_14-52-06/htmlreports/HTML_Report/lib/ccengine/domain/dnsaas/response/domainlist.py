from ccengine.domain.base_domain import BaseMarshallingDomain,\
                                        BaseMarshallingDomainList
from ccengine.domain.base_domain import BaseDomain
import xml.etree.ElementTree as ET
import json


class DomainList(BaseMarshallingDomainList):

    ROOT_TAG = 'domains'

    def __init__(self, domains=[], totalEntries=None):
        super(DomainList, self).__init__()
        self.totalEntries = totalEntries
        for domain in domains:
            self.append(domain)

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        return cls._dict_to_obj(json_dict)

    @classmethod
    def _dict_to_obj(cls, domain_dict):
        kwargs = {cls.ROOT_TAG: [Domains._dict_to_obj(domain)
                                 for domain in domain_dict.get(cls.ROOT_TAG)]}
        kwargs['totalEntries'] = domain_dict.get('totalEntries')
        return DomainList(**kwargs)


class Domains(BaseMarshallingDomain):
    ROOT_TAG = 'domains'

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
        if cls.ROOT_TAG not in json_dict:
            return None
        return cls._dict_to_obj(json_dict.get(cls.ROOT_TAG))

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        pass

    @classmethod
    def _dict_to_obj(cls, dic):
        return Domains(**dic)
