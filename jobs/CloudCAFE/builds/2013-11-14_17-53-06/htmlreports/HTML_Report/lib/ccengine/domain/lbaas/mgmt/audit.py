from ccengine.domain.base_domain import BaseMarshallingDomain, \
    BaseMarshallingDomainList
from ccengine.domain.lbaas.mgmt.alert import Alert
import xml.etree.ElementTree as ET
import json


class LoadBalancerAuditList(BaseMarshallingDomainList):

    ROOT_TAG = 'loadBalancerAudits'

    def __init__(self, loadBalancerAudits=None):
        '''A management host list object

        '''
        for audit in loadBalancerAudits:
            self.append(audit)

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
        kwargs = {cls.ROOT_TAG: [LoadBalancerAudit.
                                 _dict_to_obj(report) for report in dic]}
        return LoadBalancerAuditList(**kwargs)


class LoadBalancerAudit(BaseMarshallingDomain):

    ROOT_TAG = 'loadBalancerAudit'

    def __init__(self, id=None, status=None, created=None, updated=None,
                 alertAudits=None):
        '''An object describing the availability of vips on each cluster'''
        self.id = id
        self.status = status
        self.created = created
        self.updated = updated
        self.alertAudits = alertAudits

    def _obj_to_json(self):
        ret = self._auto_to_dict()
        return json.dumps(ret[self.ROOT_TAG])

    def _obj_to_xml(self):
        ret = self._auto_to_xml()
        return ET.tostring(ret)

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        if cls.ROOT_TAG in json_dict:
            return cls._dict_to_obj(json_dict.get(cls.ROOT_TAG))
        return cls._dict_to_obj(json_dict)

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        pass

    @classmethod
    def _dict_to_obj(cls, dic):
        return LoadBalancerAudit(**dic)


class AlertAuditList(BaseMarshallingDomainList):

    ROOT_TAG = 'alertAudits'

    def __init__(self, alertAudits=None):
        '''A management host list object

        '''
        for audit in alertAudits:
            self.append(audit)

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
        kwargs = {cls.ROOT_TAG: [Alert._dict_to_obj(alert) for alert in dic]}
        return AlertAuditList(**kwargs)
