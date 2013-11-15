from ccengine.domain.base_domain import BaseMarshallingDomain
from ccengine.domain.base_domain import BaseDomain
import xml.etree.ElementTree as ET
import json


class Domain(BaseMarshallingDomain):
    '''
    @summary: Create Domain Request Object
    '''
    def __init__(self, name=None, domain_id=None, comment=None,
                  emailAddress=None, subdomains=None,
                   recordsList=None, ttl=None):

        #Common Attributes
        self.name = name
        self.comment = comment
        self.emailAddress = emailAddress
        self.ttl = ttl
        self.subdomains = subdomains
        self.recordsList = recordsList
        self.id = domain_id

    #Request Generators
    def _obj_to_json(self):
        ret = self._obj_to_dict()
        return json.dumps(ret)

#    def _obj_to_dict(self):
#        ret = {'domains': [{'name': self.name,
#               'comment': self.comment,
#               'emailAddress': self.emailAddress,
#               'ttl': self.ttl,
#               'subdomains': self.subdomains._obj_to_dict(),
#               'recordsList': self.recordsList._obj_to_dict()}]}
#        return ret

    def _obj_to_dict(self):

        domains = []
        ret = {}
        if self.name:
            ret["name"] = self.name
        if self.comment:
            ret['comment'] = self.comment
        if self.emailAddress:
            ret["emailAddress"] = self.emailAddress
        if self.id:
            ret['id'] = self.id
        if self.ttl:
            ret['ttl'] = self.ttl
        if self.subdomains:
            ret['subdomains'] = self.subdomains._obj_to_dict()
        if self.recordsList:
            ret['recordsList'] = self.recordsList._obj_to_dict()

        if type(ret) is dict:
                domains.append(ret)
        return {'domains': domains}


class ImportDomain(BaseMarshallingDomain):
    '''
    @summary: Import Domain Request Object
    '''

    def __init__(self, import_name=None):
        self.import_name = import_name

    #Request Generators
    def _obj_to_json(self):
        ret = self._obj_to_dict()
        return json.dumps(ret)

    def _obj_to_dict(self):
        d_imp = ('{x}.com. IN SOA ns.rackspace.com. hostmonster.rackspace.com.'
                 '(1304406823 7000 7000 1814400 301)\n'
                 '{x}.com. 7000 IN A 72.77.26.210\n'
                 '{x}.com. 7000 IN AAAA 2001:db8:10::2\n'
                 '{x}.com. 9000 IN NS ns.rackspace.com.\n'
                 'www.{x}.com. 86400 IN CNAME {x}.com.\n'
                 'pub.{x}.com. 86400 IN DNAME {x}.com.\n'
                 '{x}.com. 7000 IN MX 2 mail.{x}.com.\n'
                 '{x}.com. 7000 IN TXT example.com.\n'
                 '_sip._tcp.{x}.com. 7000 IN SRV 1 5 5540 sipserver.{x}.com.\n'
                 '{x}.com. 7000 IN TXT p='
                 'MIGfKh1FCMIGfKh1FCMIGfKh1FCMIGfKh1FCMIGfKh1FCMI.')
        contents = d_imp.format(x=self.import_name)
        body = {'domains':[{'contents': contents}]}
        return body

#class SubDomains(BaseMarshallingDomain):
#
#    def __init__(self, domains=None):
#
#        #Common Attributes
#        self.domains = domains
#
#    #Request Generators
#    def _obj_to_json(self):
#        ret = self._obj_to_dict()
#        return json.dumps(ret)
#
#    def _obj_to_dict(self):
#        ret = []
#        for domain in self.domains:
#            ret.append(domain._obj_to_dict())
#        ret = {'domains': ret}
#        return ret
