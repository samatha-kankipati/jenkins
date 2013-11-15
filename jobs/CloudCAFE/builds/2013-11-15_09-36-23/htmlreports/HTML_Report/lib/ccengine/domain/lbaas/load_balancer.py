from ccengine.domain.base_domain import BaseMarshallingDomain, \
    BaseMarshallingDomainList
from ccengine.domain.lbaas.node import NodeList
from ccengine.domain.lbaas.virtual_ip import VirtualIpList
from ccengine.domain.lbaas.connection_logging import ConnectionLogging
from ccengine.domain.lbaas.content_caching import ContentCaching
from ccengine.domain.lbaas.session_persistence import SessionPersistence
from ccengine.domain.lbaas.access_list import AccessList
from ccengine.domain.lbaas.connection_throttle import ConnectionThrottle
from ccengine.domain.lbaas.health_monitor import HealthMonitor
from ccengine.domain.lbaas.metadata import Metadata
from ccengine.domain.lbaas.ssl_termination import SSLTermination
import json
import xml.etree.ElementTree as ET


class LoadBalancerList(BaseMarshallingDomainList):

    ROOT_TAG = 'loadBalancers'

    def __init__(self, loadBalancers=[]):
        super(LoadBalancerList, self).__init__()
        for lb in loadBalancers:
            self.append(lb)

    def get_by_id(self, id):
        for lb in self:
            if lb.id == id:
                return lb

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        if cls.ROOT_TAG not in json_dict:
            return None
        json_dict[cls.ROOT_TAG] = [LoadBalancer._dict_to_obj(lb)
                                   for lb in json_dict.get(cls.ROOT_TAG)]
        return LoadBalancerList(**json_dict)

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        pass


class LoadBalancer(BaseMarshallingDomain):

    ROOT_TAG = 'loadBalancer'

    def __init__(self, name=None, nodes=None, protocol=None, virtualIps=None,
                 accessList=None, algorithm=None, connectionLogging=None,
                 connectionThrottle=None, healthMonitor=None, metadata=None,
                 port=None, sessionPersistence=None, id=None, status=None,
                 nodeCount=None, created=None, updated=None,
                 contentCaching=None, halfClosed=None, timeout=None,
                 cluster=None, sourceAddresses=None, sslTermination=None,
                 httpsRedirect=None):
        '''An object that represents the data of a Load Balancer.'''
        self.name = name
        self.nodes = nodes
        self.protocol = protocol
        self.virtualIps = virtualIps
        self.accessList = accessList
        self.algorithm = algorithm
        self.connectionLogging = connectionLogging
        self.connectionThrottle = connectionThrottle
        self.healthMonitor = healthMonitor
        self.metadata = metadata
        self.port = port
        self.sessionPersistence = sessionPersistence
        self.id = id
        self.status = status
        self.nodeCount = nodeCount
        self.created = created
        self.updated = updated
        self.contentCaching = contentCaching
        self.halfClosed = halfClosed
        self.timeout = timeout
        self.cluster = cluster
        self.sourceAddresses = sourceAddresses
        self.sslTermination = sslTermination
        self.httpsRedirect = httpsRedirect

    def get_public_ipv4_vip(self):
        for vip in self.virtualIps:
            if vip.ipVersion == 'IPV4' and vip.type == 'PUBLIC':
                return vip

    def get_public_ipv6_vip(self):
        for vip in self.virtualIps:
            if vip.ipVersion == 'IPV6' and vip.type == 'PUBLIC':
                return vip

    def get_servicenet_ipv4_vip(self):
        for vip in self.virtualIps:
            if vip.ipVersion == 'IPV4' and vip.type == 'SERVICENET':
                return vip

    def _obj_to_json(self):
        ret = self._auto_to_dict()
        return json.dumps(ret)

    def _obj_to_dict(self):
        ret = {}
        for attr in vars(self).keys():
            value = vars(self).get(attr)
            #quick and dirty fix for _log getting added in
            #ideally _log should be __log, talk to Jose about this.
            if value is not None and attr != '_log':
                ret[attr] = self._auto_value_to_dict(value)

        if hasattr(self, 'ROOT_TAG'):
            return {self.ROOT_TAG: ret}
        else:
            return ret

    def _auto_value_to_dict(self, value):
        ret = None
        if isinstance(value, (int, str, unicode, bool)):
            ret = value
        elif isinstance(value, list):
            ret = []
            for item in value:
                ret.append(self._auto_value_to_dict(item))
        elif isinstance(value, dict):
            ret = {}
            for key in value.keys():
                ret[key] = self._auto_value_to_dict(value[key])
        elif isinstance(value, BaseMarshallingDomain):
            ret = value._obj_to_dict()
        return ret

    def _obj_to_xml(self):
        ret = self._auto_to_xml()
        for meta in ret.iter('metadat'):
            meta.tag = 'meta'
        return ET.tostring(ret)

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        if cls.ROOT_TAG not in json_dict:
            return None
        ret = cls._dict_to_obj(json_dict.get(cls.ROOT_TAG))
        return ret

    @classmethod
    def _xml_to_obj(cls, serialized_str):
#        element = ET.fromstring(serialized_str)
#        ret = None
#        if element.tag == 'network':
#            cidr = None
#            if element.find('cidr') is not None:
#                cidr = element.find('cidr').text
#            ret = IsolatedNetwork(cidr = cidr,
#                                  label = element.find('label').text,
#                                  id = element.find('id').text)
#        if element.tag == 'networks':
#            ret = []
#            network_ele_list = element.findall('network')
#            for element in network_ele_list:
#                cidr = None
#                if element.find('cidr') is not None:
#                    cidr = element.find('cidr').text
#                ret.append(IsolatedNetwork(cidr = cidr,
#                                           label = element.find('label').text,
#                                           id = element.find('id').text))
#        return ret
        pass

    @classmethod
    def _dict_to_obj(cls, dic):
        if NodeList.ROOT_TAG in dic:
            node_list = dic.get(NodeList.ROOT_TAG)
            dic[NodeList.ROOT_TAG] = NodeList._dict_to_obj(node_list)
        if VirtualIpList.ROOT_TAG in dic:
            vip_list = dic.get(VirtualIpList.ROOT_TAG)
            dic[VirtualIpList.ROOT_TAG] = \
                VirtualIpList._dict_to_obj(vip_list)
        if Created.ROOT_TAG in dic:
            created = dic.get(Created.ROOT_TAG)
            dic[Created.ROOT_TAG] = Created._dict_to_obj(created)
        if Updated.ROOT_TAG in dic:
            updated = dic.get(Updated.ROOT_TAG)
            dic[Updated.ROOT_TAG] = Updated._dict_to_obj(updated)
        if SourceAddresses.ROOT_TAG in dic:
            s_addrs = dic.get(SourceAddresses.ROOT_TAG)
            dic[SourceAddresses.ROOT_TAG] = \
                SourceAddresses._dict_to_obj(s_addrs)
        if Cluster.ROOT_TAG in dic:
            cluster = dic.get(Cluster.ROOT_TAG)
            dic[Cluster.ROOT_TAG] = Cluster._dict_to_obj(cluster)
        if ContentCaching.ROOT_TAG in dic:
            cc = dic.get(ContentCaching.ROOT_TAG)
            dic[ContentCaching.ROOT_TAG] = ContentCaching._dict_to_obj(cc)
        if ConnectionLogging.ROOT_TAG in dic:
            cl = dic.get(ConnectionLogging.ROOT_TAG)
            dic[ConnectionLogging.ROOT_TAG] = \
                ConnectionLogging._dict_to_obj(cl)
        if SessionPersistence.ROOT_TAG in dic:
            sp = dic.get(SessionPersistence.ROOT_TAG)
            dic[SessionPersistence.ROOT_TAG] = \
                SessionPersistence._dict_to_obj(sp)
        if AccessList.ROOT_TAG in dic:
            al = dic.get(AccessList.ROOT_TAG)
            dic[AccessList.ROOT_TAG] = AccessList._dict_to_obj(al)
        if ConnectionThrottle.ROOT_TAG in dic:
            ct = dic.get(ConnectionThrottle.ROOT_TAG)
            dic[ConnectionThrottle.ROOT_TAG] = \
                ConnectionThrottle._dict_to_obj(ct)
        if HealthMonitor.ROOT_TAG in dic:
            hm = dic.get(HealthMonitor.ROOT_TAG)
            dic[HealthMonitor.ROOT_TAG] = HealthMonitor._dict_to_obj(hm)
        if Metadata.ROOT_TAG in dic:
            md = dic.get(Metadata.ROOT_TAG)
            dic[Metadata.ROOT_TAG] = Metadata._dict_to_obj(md)
        if SSLTermination.ROOT_TAG in dic:
            ssl = dic.get(SSLTermination.ROOT_TAG)
            dic[SSLTermination.ROOT_TAG] = SSLTermination._dict_to_obj(ssl)
        return LoadBalancer(**dic)

    @classmethod
    def xml_ele_to_obj(cls, ele):
        pass


class Created(BaseMarshallingDomain):

    ROOT_TAG = 'created'

    def __init__(self, time=None):
        self.time = time

    @classmethod
    def _dict_to_obj(cls, dic):
        return Created(**dic)


class Updated(BaseMarshallingDomain):

    ROOT_TAG = 'updated'

    def __init__(self, time=None):
        self.time = time

    @classmethod
    def _dict_to_obj(cls, dic):
        return Updated(**dic)


class SourceAddresses(object):

    ROOT_TAG = 'sourceAddresses'

    def __init__(self, ipv4Public=None, ipv4Servicenet=None, ipv6Public=None,
                 ipv6Servicenet=None):
        self.ipv4Public = ipv4Public
        self.ipv4Servicenet = ipv4Servicenet
        self.ipv6Public = ipv6Public
        self.ipv6Servicenet = ipv6Servicenet

    @classmethod
    def _dict_to_obj(self, dic):
        return SourceAddresses(**dic)


class Cluster(BaseMarshallingDomain):

    ROOT_TAG = 'cluster'

    def __init__(self, name=None):
        self.name = name

    @classmethod
    def _dict_to_obj(self, dic):
        return Cluster(**dic)
