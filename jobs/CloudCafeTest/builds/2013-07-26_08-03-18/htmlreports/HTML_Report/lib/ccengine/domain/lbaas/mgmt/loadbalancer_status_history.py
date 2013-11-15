from ccengine.domain.base_domain import BaseMarshallingDomain, \
    BaseMarshallingDomainList
import xml.etree.ElementTree as ET
import json


class LoadBalancerStatusHistoryList(BaseMarshallingDomainList):

    ROOT_TAG = 'loadBalancerStatusHistories'

    def __init__(self, loadBalancerStatusHistories=None):
        '''An object to detail all the alerts for a system

        '''
        for history in loadBalancerStatusHistories:
            self.append(history)

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
        kwargs = {cls.ROOT_TAG: [LoadBalancerStatusHistory._dict_to_obj(entry)
                                 for entry in dic]}
        return LoadBalancerStatusHistoryList(**kwargs)


class LoadBalancerStatusHistory(BaseMarshallingDomain):

    ROOT_TAG = 'loadBalancerStatusHistory'

    def __init__(self, accountId=None, status=None, loadBalancerId=None,
                 created=None):
        '''An object that represents the status history of a load balancer.

        '''
        self.accountId = accountId
        self.status = status
        self.loadBalancerId = loadBalancerId
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
        return LoadBalancerStatusHistory(**dic)
