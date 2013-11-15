from ccengine.domain.base_domain import BaseMarshallingDomain, \
    BaseMarshallingDomainList
import xml.etree.ElementTree as ET
import json


class HealthCheckList(BaseMarshallingDomainList):

    ROOT_TAG = 'healthChecks'

    def __init__(self, healthChecks=None):
        '''A management virtual ip list object

        '''
        for healthCheck in healthChecks:
            self.append(healthCheck)

    def _obj_to_json(self):
        ret = self._auto_to_dict()
        return json.dumps(ret[self.ROOT_TAG])

    def _obj_to_xml(self):
        ret = self._auto_to_xml()
        return ET.tostring(ret)

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        return cls._dict_to_obj(json_dict.get(cls.ROOT_TAG))

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        pass

    @classmethod
    def _dict_to_obj(cls, dic):
        kwargs = {cls.ROOT_TAG: [HealthCheck._dict_to_obj(check)
                                 for check in dic]}
        return HealthCheckList(**kwargs)


class HealthCheck(BaseMarshallingDomain):

    ROOT_TAG = 'healthCheck'

    def __init__(self, type=None, status=None, time=None):
        '''A management virtual ip object

        '''
        self.type = type
        self.status = status
        self.time = time

    def _obj_to_json(self):
        ret = self._auto_to_dict()
        return json.dumps(ret[self.ROOT_TAG])

    def _obj_to_xml(self):
        ret = self._auto_to_xml()
        return ET.tostring(ret)

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        return cls._dict_to_obj(json_dict)

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        pass

    @classmethod
    def _dict_to_obj(cls, dic):
        return HealthCheck(**dic)
