from ccengine.domain.base_domain import BaseMarshallingDomain
from ccengine.domain.dnsaas.response.record import RecordsList, Link
import xml.etree.ElementTree as ET
import json


class RDNS(BaseMarshallingDomain):

    def __init__(self, recordsList=None, link=None):
        self.recordsList = recordsList
        self.link = link

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        return cls._dict_to_obj(json_dict)

    @classmethod
    def _dict_to_obj(cls, json_dict):
        rl = RecordsList._dict_to_obj(json_dict.get('recordsList'))
        link = Link._dict_to_obj(json_dict.get('link'))
        return RDNS(recordsList=rl, link=link)
