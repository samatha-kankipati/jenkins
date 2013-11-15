from ccengine.domain.base_domain import BaseMarshallingDomain
from ccengine.domain.base_domain import BaseDomain
import xml.etree.ElementTree as ET
import json


class RecordsList(BaseMarshallingDomain):

    def __init__(self, records=None):
        self.records = records

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        return cls._dict_to_obj(json_dict)

    def _dict_to_obj(self, json_dict):
        records = []
        for record in json_dict.get('records'):
            records.append(Record._dict_to_obj(record))
        return RecordsList(records=records)


class Record(BaseMarshallingDomain):

    def __init__(self, name=None, type=None, data=None, ttl=None,
                 id=None, updated=None, created=None, comment=None,
                  priority=None):

        #Common Attributes
        self.name = name
        self.type = type
        self.data = data
        self.ttl = ttl
        self.id = id
        self.priority = priority
        self.comment = comment
        self.updated = updated
        self.created = created

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        ret = None
        if 'records' in json_dict:
            ret = []
            for record in json_dict['records']:
                ret.append(cls._dict_to_obj(record))
        else:
            ret = cls._dict_to_obj(json_dict)
        return ret

    @classmethod
    def _dict_to_obj(cls, json_dict):
        return Record(**json_dict)


class Link(BaseMarshallingDomain):

    def __init__(self, content=None, href=None, rel=None):
        self.content = content
        self.href = href
        self.rel = rel

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        return cls._dict_to_obj(json_dict)

    def _dict_to_obj(self, json_dict):
        return Link(**json_dict)


class Async(BaseMarshallingDomain):

    def __init__(self, jobid=None, callbackUrl=None, status=None, 
                 requestUrl=None, verb=None, request=None):
        self.jobid = jobid
        self.callbackUrl = callbackUrl
        self.status = status
        self.requestUrl = requestUrl
        self.verb = verb
        self.request = request

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        return cls._dict_to_obj(json_dict)

    def _dict_to_obj(self, json_dict):
        return Link(**json_dict)
