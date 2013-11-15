from ccengine.domain.base_domain import BaseMarshallingDomain
from ccengine.domain.base_domain import BaseDomain
import xml.etree.ElementTree as ET
import json


class SubDomainsList(BaseMarshallingDomain):

    def __init__(self, subdomains=None):
        self.subdomains = subdomains

    def _obj_to_json(self):
        return json.dumps(self._obj_to_dict())

    def _obj_to_dict(self):
        subdomains = []
        for subdomain in self.subdomains:
            if type(subdomain) is SubDomain:
                subdomains.append(subdomain._obj_to_dict())
            if type(subdomain) is dict:
                subdomains.append(subdomain)
        return {'domains': subdomains}


class SubDomain(BaseMarshallingDomain):

    def __init__(self, name=None, comment=None,
        emailAddress=None, ttl=None):

        #Common Attributes

        self.name = name
        self.comment = comment
        self.emailAddress = emailAddress
        self.ttl = ttl

    #Request Generators
    def _obj_to_json(self):
        ret = self._obj_to_dict()
        return json.dumps(ret)

    def _obj_to_dict(self):
        ret = {'name': self.name,
               'comment': self.comment,
               'emailAddress': self.emailAddress}

        return ret


