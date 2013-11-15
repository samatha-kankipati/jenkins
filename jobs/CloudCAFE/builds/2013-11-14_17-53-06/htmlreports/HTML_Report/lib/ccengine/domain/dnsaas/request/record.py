from ccengine.domain.base_domain import BaseMarshallingDomain
from ccengine.domain.base_domain import BaseDomain
import xml.etree.ElementTree as ET
import json


class RecordsList(BaseMarshallingDomain):

    def __init__(self, records=None):
        self.records = records

    def _obj_to_json(self):
        return json.dumps(self._obj_to_dict())

    def _obj_to_dict(self):
        records = []
        for record in self.records:
            if type(record) is Record:
                records.append(record._obj_to_dict())
            if type(record) is dict:
                records.append(record)
        return {'records': records}


class Record(BaseMarshallingDomain):

    def __init__(self, name=None, record_type=None, comment=None,
                 data=None, ttl=None, record_id=None, priority=None):

        #Common Attributes
        self.name = name
        self.type = record_type
        self.data = data
        self.ttl = ttl
        self.id = record_id
        self.priority = priority
        self.comment = comment

    #Request Generators
    def _obj_to_json(self):
        ret = self._obj_to_dict()
        return json.dumps(ret)

    def _obj_to_dict(self):
        ret = {}
        if self.name:
            ret["name"] = self.name
        if self.type:
            ret['type'] = self.type
        if self.id:
            ret["id"] = self.id
        if self.data:
            ret['data'] = self.data
        if self.ttl:
            ret['ttl'] = self.ttl
        if self.priority:
            ret['priority'] = self.priority
        if self.comment:
            ret['comment'] = self.comment
        return ret


class Link(BaseMarshallingDomain):

    def __init__(self, content=None, href=None, rel=None):
        self.content = content
        self.href = href
        self.rel = rel

    def _obj_to_json(self):
        return json.dumps(self._obj_to_dict())

    def _obj_to_dict(self):
        ret = {'content': self.content,
               'href': self.href,
               'rel': self.rel}
        return ret
#
#
#class RecordsListUp(BaseMarshallingDomain):
#
#    def __init__(self, records=None):
#        self.records = records
#
#    def _obj_to_json(self):
#        return json.dumps(self._obj_to_dict())
#
#    def _obj_to_dict(self):
#        records = []
#        for record in self.records:
#            if type(record) is RecordUpdate:
#                records.append(record._obj_to_dict())
#            if type(record) is dict:
#                records.append(record)
#        return {'records': records}
#
#
#class RecordUpdate(BaseMarshallingDomain):
#
#    def __init__(self, name=None, record_type=None, data=None, ttl=None,
#                  id=None):
#
#        #Common Attributes
#        self.name = name
#        self.type = record_type
#        self.data = data
#        self.ttl = ttl
#        self.id = id
#
#    #Request Generators
#    def _obj_to_json(self):
#        ret = self._obj_to_dict()
#        return json.dumps(ret)
#
#    def _obj_to_dict(self):
#        ret = {}
#        if self.name:
#            ret["name"] = self.name
#        if self.type:
#            ret['type'] = self.type
#        if self.id:
#            ret["id"] = self.id
#        if self.data:
#            ret['data'] = self.data
#        if self.ttl:
#            ret['ttl'] = self.ttl
#
#        ret = {'name': self.name,
#               'type': self.type,
#               'id': self.id,
#               'data': self.data,
#               'ttl': self.ttl}
#
#
#        return ret














