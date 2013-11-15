from ccengine.domain.base_domain import BaseMarshallingDomainList, \
    BaseMarshallingDomain
import xml.etree.ElementTree as ET
import json


class ClusterList(BaseMarshallingDomainList):

    ROOT_TAG = 'clusters'

    def __init__(self, clusters=None):
        '''A management load balancer list object

        '''
        for cluster in clusters:
            self.append(cluster)

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
        kwargs = {cls.ROOT_TAG: [Cluster._dict_to_obj(cluster)
                                 for cluster in dic]}
        return ClusterList(**kwargs)


class Cluster(BaseMarshallingDomain):

    ROOT_TAG = 'cluster'

    def __init__(self, id=None, name=None, description=None, dataCenter=None,
                 numberOfLoadBalancingConfigurations=None, status=None,
                 numberOfUniqueCustomers=None, utilization=None,
                 numberOfHostMachines=None, clusterIpv6Cidr=None):
        '''An object a cluster

        '''
        self.id = id
        self.name = name
        self.dataCenter = dataCenter
        self.numberOfLoadBalancingConfigurations = \
            numberOfLoadBalancingConfigurations
        self.numberOfUniqueCustomers = numberOfUniqueCustomers
        self.description = description
        self.utilization = utilization
        self.numberOfHostMachines = numberOfHostMachines
        self.status = status
        self.clusterIpv6Cidr = clusterIpv6Cidr

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
        return Cluster(**dic)
