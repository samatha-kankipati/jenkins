from ccengine.domain.base_domain import BaseMarshallingDomain, \
    BaseMarshallingDomainList
import xml.etree.ElementTree as ET
import json


class AccountEventList(BaseMarshallingDomain):

    ROOT_TAG = 'accountLoadBalancerServiceEvents'

    def __init__(self, loadBalancerServiceEvents=None, accountId=None):
        '''An object that data concerning tickets on a load balancer.

        '''
        self.accountId = accountId
        self.loadBalancerServiceEvents = loadBalancerServiceEvents

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
        if AccountLoadBalancerEventList.ROOT_TAG in dic:
            dic[AccountLoadBalancerEventList.ROOT_TAG] = \
                AccountLoadBalancerEventList._dict_to_obj(dic.get(
                    AccountLoadBalancerEventList.ROOT_TAG))
        return AccountEventList(**dic)


class AccountLoadBalancerEventList(BaseMarshallingDomainList):

    ROOT_TAG = 'loadBalancerServiceEvents'

    def __init__(self, loadBalancerServiceEvents=None):
        '''An object that data concerning tickets on a load balancer.

        '''
        for loadBalancerServiceEvent in loadBalancerServiceEvents:
            self.append(loadBalancerServiceEvent)

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
        kwargs = {cls.ROOT_TAG: [LoadBalancerEventList._dict_to_obj(lbe)
                                 for lbe in dic]}
        return AccountLoadBalancerEventList(**kwargs)


class LoadBalancerEventList(BaseMarshallingDomain):

    ROOT_TAG = 'loadBalancerServiceEvents'

    def __init__(self, loadBalancerServiceEvents=None, loadbalancerId=None):
        '''An object that data concerning tickets on a load balancer.

        '''
        self.loadbalancerId = loadbalancerId
        self.loadBalancerServiceEvents = loadBalancerServiceEvents

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
        if LoadBalancerEvents.ROOT_TAG in dic:
            dic[LoadBalancerEvents.ROOT_TAG] = \
                LoadBalancerEvents._dict_to_obj(dic.get(
                    LoadBalancerEvents.ROOT_TAG))
        return LoadBalancerEventList(**dic)


class LoadBalancerEvents(BaseMarshallingDomainList):

    ROOT_TAG = 'loadBalancerServiceEvents'

    def __init__(self, loadBalancerServiceEvents=None):
        '''An object that data concerning tickets on a load balancer.

        '''
        for loadBalancerServiceEvent in loadBalancerServiceEvents:
            self.append(loadBalancerServiceEvent)

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
        kwargs = {cls.ROOT_TAG: [LoadBalancerEvent._dict_to_obj(lbe)
                                 for lbe in dic]}
        return AccountLoadBalancerEventList(**kwargs)


class LoadBalancerEvent(BaseMarshallingDomain):

    ROOT_TAG = 'loadBalancerServiceEvent'

    def __init__(self, author=None, description=None, category=None,
                 severity=None, created=None):
        '''An object that data concerning tickets on a load balancer.

        '''
        self.author = author
        self.description = description
        self.category = category
        self.severity = severity
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
        return LoadBalancerEvent(**dic)
