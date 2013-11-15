from ccengine.domain.base_domain import BaseMarshallingDomain, \
    BaseMarshallingDomainList
import xml.etree.ElementTree as ET
import json


class HostList(BaseMarshallingDomainList):

    ROOT_TAG = 'hosts'

    def __init__(self, hosts=None):
        '''A management host list object

        '''
        for host in hosts:
            self.append(host)

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
        kwargs = {cls.ROOT_TAG: [Host._dict_to_obj(host)
                                 for host in dic]}
        return HostList(**kwargs)


class Host(BaseMarshallingDomain):

    ROOT_TAG = 'host'

    def __init__(self, id=None, name=None, clusterId=None, coreDeviceId=None,
                 zone=None, status=None, type=None, utilization=None,
                 maxConcurrentConnections=None, managementIp=None,
                 managementSoapInterface=None, soapEndpointActive=None,
                 numberOfLoadBalancingConfigurations=None, ipv6Public=None,
                 ipv4Servicenet=None, uniqueCustomers=None, ipv4Public=None,
                 trafficManagerName=None, availableConcurrentConnections=None,
                 activeLBConfigurations=None, currentUtilization=None,
                 totalConcurrentConnections=None):
        '''An object that represents a host.

        '''
        self.id = id
        self.name = name
        self.clusterId = clusterId
        self.coreDeviceId = coreDeviceId
        self.zone = zone
        self.status = status
        self.type = type
        self.maxConcurrentConnections = maxConcurrentConnections
        self.managementIp = managementIp
        self.managementSoapInterface = managementSoapInterface
        self.utilization = utilization
        self.numberOfLoadBalancingConfigurations = \
            numberOfLoadBalancingConfigurations
        self.soapEndpointActive = soapEndpointActive
        self.uniqueCustomers = uniqueCustomers
        self.ipv6Public = ipv6Public
        self.ipv4Servicenet = ipv4Servicenet
        self.ipv4Public = ipv4Public
        self.trafficManagerName = trafficManagerName
        self.availableConcurrentConnections = availableConcurrentConnections
        self.activeLBConfigurations = activeLBConfigurations
        self.currentUtilization = currentUtilization
        self.totalConcurrentConnections = totalConcurrentConnections

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
        return Host(**dic)


class HostCapacityReportList(BaseMarshallingDomainList):

    ROOT_TAG = 'hostCapacityReports'

    def __init__(self, hostCapacityReports=None):
        '''A list object to provide capacity reports on all hosts'''
        for report in hostCapacityReports:
            self.append(report)

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
        kwargs = {cls.ROOT_TAG: [HostCapacityReport._dict_to_obj(report)
                                 for report in dic]}
        return HostCapacityReportList(**kwargs)


class HostCapacityReport(BaseMarshallingDomain):

    ROOT_TAG = 'hostCapacityReport'

    def __init__(self, hostId=None, hostName=None,
                 availableConcurrentConnections=None,
                 totalConcurrentConnectionCapacity=None,
                 allocatedConcurrentConnections=None,
                 allocatedConcurrentConnectionsToday=None,
                 allocatedConcurrentConnectionsInLastSevenDays=None,
                 remainingDaysOfCapacity=None):
        '''An object describing the capacity of a single host'''
        self.hostId = hostId
        self.hostName = hostName
        self.availableConcurrentConnections = availableConcurrentConnections
        self.totalConcurrentConnectionCapacity = \
            totalConcurrentConnectionCapacity
        self.allocatedConcurrentConnections = allocatedConcurrentConnections
        self.allocatedConcurrentConnectionsToday = \
            allocatedConcurrentConnectionsToday
        self.allocatedConcurrentConnectionsInLastSevenDays = \
            allocatedConcurrentConnectionsInLastSevenDays
        self.remainingDaysOfCapacity = remainingDaysOfCapacity

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
        return HostCapacityReport(**dic)
