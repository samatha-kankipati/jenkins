from ccengine.domain.base_domain import BaseMarshallingDomain
import json
import xml.etree.ElementTree as ET


class HealthMonitor(BaseMarshallingDomain):

    ROOT_TAG = 'healthMonitor'

    def __init__(self, type=None, delay=None, timeout=None, path=None,
                 statusRegex=None, bodyRegex=None, hostHeader=None,
                 attemptsBeforeDeactivation=None):
        self.type = type
        self.delay = delay
        self.timeout = timeout
        self.attemptsBeforeDeactivation = attemptsBeforeDeactivation
        self.path = path
        self.statusRegex = statusRegex
        self.bodyRegex = bodyRegex
        self.hostHeader = hostHeader

    def _obj_to_json(self):
        return json.dumps(self._obj_to_dict())

    def _obj_to_dict(self):
        return self._auto_to_dict()[self.ROOT_TAG]

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
        return HealthMonitor(**dic)
