from ccengine.domain.base_domain import BaseMarshallingDomain
from ccengine.domain.dnsaas.response.record import RecordsList, Link
from ccengine.domain.dnsaas.response.rdns import RDNS as rdns
import xml.etree.ElementTree as ET
import json


class AsyncResponse(BaseMarshallingDomain):

    def __init__(self, jobId=None, callbackUrl=None, status=None,
                 requestUrl=None, verb=None, request=None, response=None):
        self.jobId = jobId
        self.callbackUrl = callbackUrl
        self.status = status
        self.requestUrl = requestUrl
        self.verb = verb
        self.request = request
        self.response = response

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        return cls._dict_to_obj(json_dict)

    @classmethod
    def _dict_to_obj(cls, json_dict):
#        json_dict['request'] = None
        return AsyncResponse(**json_dict)
