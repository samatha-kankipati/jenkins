from ccengine.domain.base_domain import BaseMarshallingDomain, \
    BaseMarshallingDomainList
from ccengine.domain.lbaas.mgmt.link import Link
import xml.etree.ElementTree as ET
import json


class AccountBillingList(BaseMarshallingDomainList):

    ROOT_TAG = 'accountBillings'

    def __init__(self, accountBillings=None):
        ''' An object to describe billing necessary info on an account'''
        for billing in accountBillings:
            self.append(billing)

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
        kwargs = {cls.ROOT_TAG: [AccountBilling._dict_to_obj(billing)
                                 for billing in dic]}
        return AccountBillingList(**kwargs)


class AccountBilling(BaseMarshallingDomain):

    ROOT_TAG = 'accountBilling'

    def __init__(self, accountId=None, accountUsage=None,
                 loadBalancerUsages=None):
        ''' An object to describe billing necessary info on an account'''
        self.accountId = accountId
        self.accountUsage = accountUsage
        self.loadBalancerUsages = loadBalancerUsages

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
        if AccountUsage.ROOT_TAG in dic:
            dic[AccountUsage.ROOT_TAG] = \
                AccountUsage._dict_to_obj(
                    dic.get(AccountUsage.ROOT_TAG))
        if LoadBalancerUsageList.ROOT_TAG in dic:
            dic[LoadBalancerUsageList.ROOT_TAG] = \
                LoadBalancerUsageList._dict_to_obj(
                    dic.get(LoadBalancerUsageList.ROOT_TAG))
        return AccountBilling(**dic)


class AccountUsage(BaseMarshallingDomain):

    ROOT_TAG = 'accountUsage'

    def __init__(self, accountUsageRecords=None, links=None):
        '''A management load balancer list object

        '''
        self.accountUsageRecords = accountUsageRecords
        self.links = links

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
        if AccountUsageRecordList.ROOT_TAG in dic:
            dic[AccountUsageRecordList.ROOT_TAG] = \
                AccountUsageRecordList._dict_to_obj(dic.get(
                    AccountUsageRecordList.ROOT_TAG))
        if Link.ROOT_TAG in dic:
            dic[Link.ROOT_TAG] = Link._dict_to_obj(dic.get(Link.ROOT_TAG))
        return AccountUsage(**dic)


class AccountUsageRecordList(BaseMarshallingDomainList):

    ROOT_TAG = 'accountUsageRecords'

    def __init__(self, accountUsageRecords=None):
        ''' An object to describe billing necessary info on an account'''
        for record in accountUsageRecords:
            self.append(record)

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
        kwargs = {cls.ROOT_TAG: [AccountUsageRecord._dict_to_obj(record)
                                 for record in dic]}
        return AccountUsageRecordList(**kwargs)


class AccountUsageRecord(BaseMarshallingDomain):

    ROOT_TAG = 'accountUsageRecord'

    def __init__(self, numLoadBalancers=None, numPublicVips=None,
                 numServicenetVips=None, startTime=None, accountId=None):
        '''An object providing information on usage stats for a load balancer.

        '''
        self.accountId = accountId
        self.numLoadBalancers = numLoadBalancers
        self.numPublicVips = numPublicVips
        self.numServicenetVips = numServicenetVips
        self.startTime = startTime

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
        return AccountUsageRecord(**dic)


class LoadBalancerUsageList(BaseMarshallingDomainList):

    ROOT_TAG = 'loadBalancerUsageRecords'

    def __init__(self, loadBalancerUsageRecords=None):
        '''A management load balancer list object

        '''
        for record in loadBalancerUsageRecords:
            self.append(record)

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
        kwargs = {cls.ROOT_TAG: [LoadBalancerUsage._dict_to_obj(usage)
                                 for usage in dic]}
        return LoadBalancerUsageList(**kwargs)


class LoadBalancerUsage(BaseMarshallingDomain):

    ROOT_TAG = 'loadBalancerUsageRecord'

    def __init__(self, id=None, accountId=None, loadBalancerId=None,
                 averageNumConnections=None, incomingTransfer=None,
                 outgoingTransfer=None, averageNumConnectionsSsl=None,
                 incomingTransferSsl=None, outgoingTransferSsl=None,
                 numVips=None, numPolls=None, startTime=None, endTime=None,
                 vipType=None, sslMode=None, eventType=None):
        '''An object providing information on usage stats for a load balancer.

        '''
        self.accountId = accountId
        self.id = id
        self.loadBalancerId = loadBalancerId
        self.averageNumConnections = averageNumConnections
        self.incomingTransfer = incomingTransfer
        self.outgoingTransfer = outgoingTransfer
        self.averageNumConnections = averageNumConnections
        self.averageNumConnectionsSsl = averageNumConnectionsSsl
        self.outgoingTransferSsl = outgoingTransferSsl
        self.incomingTransferSsl = incomingTransferSsl
        self.numVips = numVips
        self.numPolls = numPolls
        self.startTime = startTime
        self.endTime = endTime
        self.vipType = vipType
        self.sslMode = sslMode
        self.eventType = eventType

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
        if Link.ROOT_TAG in dic:
            dic[Link.ROOT_TAG] = Link._dict_to_obj(dic.get(Link.ROOT_TAG))
        return LoadBalancerUsage(**dic)
