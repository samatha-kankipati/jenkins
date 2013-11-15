from ccengine.domain.base_domain import BaseMarshallingDomain, \
    BaseMarshallingDomainList
import xml.etree.ElementTree as ET
import json


class VirtualIpAvailabilityReportList(BaseMarshallingDomainList):

    ROOT_TAG = 'virtualIpAvailabilityReports'

    def __init__(self, virtualIpAvailabilityReports=None):
        '''A management host list object

        '''
        for report in virtualIpAvailabilityReports:
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
        kwargs = {cls.ROOT_TAG: [VirtualIpAvailabilityReport.
                                 _dict_to_obj(report) for report in dic]}
        return VirtualIpAvailabilityReportList(**kwargs)


class VirtualIpAvailabilityReport(BaseMarshallingDomain):

    ROOT_TAG = 'virtualIpAvailabilityReport'

    def __init__(self, allocatedPublicIpAddressesInLastSevenDays=None,
                 freeAndClearPublicIpAddresses=None, clusterId=None,
                 allocatedServiceNetIpAddressesInLastSevenDays=None,
                 clusterName=None, publicIpAddressesInHolding=None,
                 totalServiceNetAddresses=None, totalPublicIpAddresses=None,
                 freeAndClearServiceNetIpAddresses=None,
                 serviceNetIpAddressesInHolding=None,
                 publicIpAddressesAllocatedToday=None,
                 serviceNetIpAddressesAllocatedToday=None,
                 remainingDaysOfPublicIpAddresses=None,
                 remainingDaysOfServiceNetIpAddresses=None):
        '''An object describing the availability of vips on each cluster'''
        self.allocatedPublicIpAddressesInLastSevenDays = \
            allocatedPublicIpAddressesInLastSevenDays
        self.freeAndClearPublicIpAddresses = freeAndClearPublicIpAddresses
        self.clusterId = clusterId
        self.allocatedServiceNetIpAddressesInLastSevenDays = \
            allocatedServiceNetIpAddressesInLastSevenDays
        self.clusterName = clusterName
        self.publicIpAddressesInHolding = publicIpAddressesInHolding
        self.totalServiceNetAddresses = totalServiceNetAddresses
        self.totalPublicIpAddresses = totalPublicIpAddresses
        self.freeAndClearServiceNetIpAddresses = \
            freeAndClearServiceNetIpAddresses
        self.serviceNetIpAddressesInHolding = serviceNetIpAddressesInHolding
        self.publicIpAddressesAllocatedToday = publicIpAddressesAllocatedToday
        self.serviceNetIpAddressesAllocatedToday = \
            serviceNetIpAddressesAllocatedToday
        self.remainingDaysOfPublicIpAddresses = \
            remainingDaysOfPublicIpAddresses
        self.remainingDaysOfServiceNetIpAddresses = \
            remainingDaysOfServiceNetIpAddresses

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
        return VirtualIpAvailabilityReport(**dic)
