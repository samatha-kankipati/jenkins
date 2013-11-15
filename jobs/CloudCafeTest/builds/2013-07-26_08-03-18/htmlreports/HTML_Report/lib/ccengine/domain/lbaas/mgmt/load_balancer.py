from ccengine.domain.base_domain import BaseMarshallingDomain, \
    BaseMarshallingDomainList
from ccengine.domain.lbaas.mgmt.cluster import Cluster
from ccengine.domain.lbaas.connection_logging import ConnectionLogging
from ccengine.domain.lbaas.mgmt.created import Created
from ccengine.domain.lbaas.mgmt.updated import Updated
from ccengine.domain.lbaas.virtual_ip import VirtualIpList
from ccengine.domain.lbaas.mgmt.ticket import TicketList
import xml.etree.ElementTree as ET
import json


class LoadBalancerList(BaseMarshallingDomainList):

    ROOT_TAG = 'loadBalancers'

    def __init__(self, loadBalancers=None):
        '''A management load balancer list object

        '''
        for lb in loadBalancers:
            self.append(lb)

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
        kwargs = {cls.ROOT_TAG: [LoadBalancer._dict_to_obj(lb) for lb in dic]}
        return LoadBalancerList(**kwargs)


class LoadBalancer(BaseMarshallingDomain):

    ROOT_TAG = 'loadBalancer'

    def __init__(self, virtualIps=None, cluster=None, created=None, name=None,
                 updated=None, connectionLogging=None, tickets=None, id=None,
                 status=None, protocol=None, algorithm=None, isSticky=None,
                 accountId=None):
        '''An object detailing specific fields of a load balancer

        '''
        self.accountId = accountId
        self.virtualIps = virtualIps
        self.cluster = cluster
        self.created = created
        self.updated = updated
        self.connectionLogging = connectionLogging
        self.tickets = tickets
        self.status = status
        self.name = name
        self.id = id
        self.protocol = protocol
        self.algorithm = algorithm
        self.isSticky = isSticky

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
        if VirtualIpList.ROOT_TAG in dic:
            dic[VirtualIpList.ROOT_TAG] = \
                VirtualIpList._dict_to_obj(dic.get(VirtualIpList.ROOT_TAG))
        if Cluster.ROOT_TAG in dic:
            dic[Cluster.ROOT_TAG] = \
                Cluster._dict_to_obj(dic.get(Cluster.ROOT_TAG))
        if TicketList.ROOT_TAG in dic:
            dic[TicketList.ROOT_TAG] = \
                TicketList._dict_to_obj(dic.get(TicketList.ROOT_TAG))
        if ConnectionLogging.ROOT_TAG in dic:
            dic[ConnectionLogging.ROOT_TAG] = \
                ConnectionLogging._dict_to_obj(dic.get(
                    ConnectionLogging.ROOT_TAG).get(
                        ConnectionLogging.ROOT_TAG))
        if Created.ROOT_TAG in dic:
            dic[Created.ROOT_TAG] = \
                Created._dict_to_obj(dic.get(Created.ROOT_TAG))
        if Updated.ROOT_TAG in dic:
            dic[Updated.ROOT_TAG] = \
                Updated._dict_to_obj(dic.get(Updated.ROOT_TAG))
        return LoadBalancer(**dic)


class AccountLoadBalancerList(BaseMarshallingDomain):

    ROOT_TAG = 'accountLoadBalancers'

    def __init__(self, accountId=None, accountLoadBalancers=None):
        '''A management load balancer list object

        '''
        self.accountId = accountId
        self.accountLoadBalancers = accountLoadBalancers

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
        if AccountLoadBalancer.ROOT_TAG in dic:
            dic[AccountLoadBalancer.ROOT_TAG] = \
                AccountLoadBalancer._dict_to_obj(
                    dic.get(AccountLoadBalancer.ROOT_TAG))
        return AccountLoadBalancerList(**dic)


class AccountLoadBalancer(BaseMarshallingDomain):

    ROOT_TAG = 'accountLoadBalancer'

    def __init__(self, protocol=None, status=None, loadBalancerId=None,
                 loadBalancerName=None, clusterId=None, clusterName=None):
        '''An object detailing specific fields of a load balancer

        '''
        self.protocol = protocol
        self.status = status
        self.loadBalancerId = loadBalancerId
        self.loadBalancerName = loadBalancerName
        self.clusterId = clusterId
        self.clusterName = clusterName

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
        return AccountLoadBalancer(**dic)


class ExtendedAccountLoadBalancerList(BaseMarshallingDomainList):

    ROOT_TAG = 'extendedAccountLoadbalancers'

    def __init__(self, accountId=None, extendedAccountLoadbalancers=None):
        '''A management load balancer list object

        '''
        self.accountId = accountId
        for lb in extendedAccountLoadbalancers:
            self.append(lb)

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
        kwargs = {cls.ROOT_TAG: [ExtendedAccountLoadBalancer._dict_to_obj(lb)
                                 for lb in dic]}
        return ExtendedAccountLoadBalancerList(**kwargs)


class ExtendedAccountLoadBalancer(BaseMarshallingDomain):

    ROOT_TAG = 'extendedAccountLoadBalancer'

    def __init__(self, protocol=None, status=None, loadBalancerId=None,
                 loadBalancerName=None, clusterId=None, clusterName=None,
                 region=None, virtualIps=None):
        '''An object detailing specific fields of a load balancer

        '''
        self.protocol = protocol
        self.status = status
        self.loadBalancerId = loadBalancerId
        self.loadBalancerName = loadBalancerName
        self.clusterId = clusterId
        self.clusterName = clusterName
        self.region = region
        self.virtualIps = virtualIps

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
        if VirtualIpList.ROOT_TAG in dic:
            dic[VirtualIpList.ROOT_TAG] = \
                VirtualIpList._dict_to_obj(dic.get(VirtualIpList.ROOT_TAG))
        return ExtendedAccountLoadBalancer(**dic)
