from ccengine.domain.base_domain import BaseMarshallingDomain, \
    BaseMarshallingDomainList
from ccengine.domain.lbaas.mgmt.host import Host
from ccengine.domain.lbaas.virtual_ip import VirtualIpList
from ccengine.domain.lbaas.node import NodeList
from ccengine.domain.lbaas.session_persistence import SessionPersistence
from ccengine.domain.lbaas.connection_logging import ConnectionLogging
from ccengine.domain.lbaas.mgmt.cluster import Cluster
from ccengine.domain.lbaas.mgmt.created import Created
from ccengine.domain.lbaas.mgmt.updated import Updated
from ccengine.domain.lbaas.mgmt.rate_limit import RateLimit
from ccengine.domain.lbaas.ssl_termination import SSLTermination
from ccengine.domain.lbaas.mgmt.events import AccountEventList
import xml.etree.ElementTree as ET
import json


class ExtendedLoadBalancerList(BaseMarshallingDomainList):

    ROOT_TAG = 'loadBalancers'

    def __init__(self, loadBalancers=None, accountId=None):
        '''A list of extended view load balancers'''
        for lb in loadBalancers:
            self.append(lb)
        self.accountId = accountId

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
        kwargs = {cls.ROOT_TAG: [ExtendedLoadBalancer._dict_to_obj(lb)
                                 for lb in dic]}
        return ExtendedLoadBalancerList(**kwargs)


class ExtendedLoadBalancer(BaseMarshallingDomain):

    ROOT_TAG = 'loadBalancer'

    def __init__(self, id=None, name=None, sticky=None, accountId=None,
                 protocol=None, port=None, algorithm=None, status=None,
                 timeout=None, totalActiveConnections=None, host=None,
                 ipv4Servicenet=None, ipv4Public=None, ipv6Public=None,
                 currentUsage=None, virtualIps=None, sessionPersistence=None,
                 connectionLimits=None, connectionLogging=None, cluster=None,
                 rateLimit=None, created=None, updated=None, nodes=None,
                 sslTermination=None, accountLoadBalancerServiceEvents=None):
        '''An object that holds information about the number of accounts in a
                cluster
        '''
        self.id = id
        self.name = name
        self.sticky = sticky
        self.accountId = accountId
        self.protocol = protocol
        self.port = port
        self.algorithm = algorithm
        self.status = status
        self.timeout = timeout
        self.totalActiveConnections = totalActiveConnections
        self.ipv4Servicenet = ipv4Servicenet
        self.ipv4Public = ipv4Public
        self.ipv6Public = ipv6Public
        self.host = host
        self.currentUsage = currentUsage
        self.virtualIps = virtualIps
        self.nodes = nodes
        self.sessionPersistence = sessionPersistence
        self.connectionLimits = connectionLimits
        self.connectionLogging = connectionLogging
        self.cluster = cluster
        self.rateLimit = rateLimit
        self.created = created
        self.updated = updated
        self.sslTermination = sslTermination
        self.accountLoadBalancerServiceEvents = \
            accountLoadBalancerServiceEvents

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
        if Host.ROOT_TAG in dic:
            dic[Host.ROOT_TAG] = Host._dict_to_obj(dic.get(Host.ROOT_TAG))
        if CurrentUsage.ROOT_TAG in dic:
            dic[CurrentUsage.ROOT_TAG] = \
                CurrentUsage._dict_to_obj(dic.get(CurrentUsage.ROOT_TAG))
        if VirtualIpList.ROOT_TAG in dic:
            dic[VirtualIpList.ROOT_TAG] = \
                VirtualIpList._dict_to_obj(dic.get(VirtualIpList.ROOT_TAG))
        if NodeList.ROOT_TAG in dic:
            dic[NodeList.ROOT_TAG] = \
                NodeList._dict_to_obj(dic.get(NodeList.ROOT_TAG))
        if SessionPersistence.ROOT_TAG in dic:
            dic[SessionPersistence.ROOT_TAG] = \
                SessionPersistence._dict_to_obj(
                    dic.get(SessionPersistence.ROOT_TAG))
        if ConnectionLogging.ROOT_TAG in dic:
            dic[ConnectionLogging.ROOT_TAG] = \
                ConnectionLogging._dict_to_obj(dic.get(
                    ConnectionLogging.ROOT_TAG))
        if ConnectionLimits.ROOT_TAG in dic:
            dic[ConnectionLimits.ROOT_TAG] = \
                ConnectionLimits._dict_to_obj(
                    dic.get(ConnectionLimits.ROOT_TAG))
        if Cluster.ROOT_TAG in dic:
            dic[Cluster.ROOT_TAG] = \
                Cluster._dict_to_obj(dic.get(Cluster.ROOT_TAG))
        if RateLimit.ROOT_TAG in dic:
            dic[RateLimit.ROOT_TAG] = \
                RateLimit._dict_to_obj(dic.get(RateLimit.ROOT_TAG))
        if Created.ROOT_TAG in dic:
            dic[Created.ROOT_TAG] = \
                Created._dict_to_obj(dic.get(Created.ROOT_TAG))
        if Updated.ROOT_TAG in dic:
            dic[Updated.ROOT_TAG] = \
                Updated._dict_to_obj(dic.get(Updated.ROOT_TAG))
        if SSLTermination.ROOT_TAG in dic:
            dic[SSLTermination.ROOT_TAG] = \
                SSLTermination._dict_to_obj(dic.get(SSLTermination.ROOT_TAG))
        if AccountEventList.ROOT_TAG in dic:
            dic[AccountEventList.ROOT_TAG] = \
                AccountEventList._dict_to_obj(
                    dic.get(AccountEventList.ROOT_TAG))
        return ExtendedLoadBalancer(**dic)


class CurrentUsage(BaseMarshallingDomain):

    ROOT_TAG = 'currentUsage'

    def __init__(self, incomingTransfer=None, outgoingTransfer=None):
        '''An object detailing current usage on a loadbalancer

        '''
        self.incomingTransfer = incomingTransfer
        self.outgoingTransfer = outgoingTransfer

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
        return CurrentUsage(**dic)


class ConnectionLimits(BaseMarshallingDomain):

    ROOT_TAG = 'connectionLimits'

    def __init__(self, minConnections=None, maxConnectionsFromIp=None,
                 maxConnectionRateFromIp=None, maxConnectionRateTimer=None):
        '''An object detailing current usage on a loadbalancer

        '''
        self.minConnections = minConnections
        self.maxConnectionsFromIp = maxConnectionsFromIp
        self.maxConnectionRateFromIp = maxConnectionRateFromIp
        self.maxConnectionRateTimer = maxConnectionRateTimer

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
        return ConnectionLimits(**dic)
