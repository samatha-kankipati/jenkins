from ccengine.domain.base_domain import BaseMarshallingDomain, \
    BaseMarshallingDomainList
import xml.etree.ElementTree as ET
import json


class AlertList(BaseMarshallingDomainList):

    ROOT_TAG = 'alerts'

    def __init__(self, alerts=None):
        '''An object to detail all the alerts for a system

        '''
        for alert in alerts:
            self.append(alert)
        self.alerts = alerts

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
        kwargs = {cls.ROOT_TAG: [Alert._dict_to_obj(acc)
                                 for acc in dic]}
        return AlertList(**kwargs)


class Alert(BaseMarshallingDomain):

    ROOT_TAG = 'alert'

    def __init__(self, accountId=None, id=None, loadbalancerId=None,
                 status=None, created=None, messageName=None, message=None):
        '''An object to detail all the alerts for a system

        '''
        self.id = id
        self.accountId = accountId
        self.loadbalancerId = loadbalancerId
        self.messageName = messageName
        self.message = message
        self.status = status
        self.created = created

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
        return Alert(**dic)
