from ccengine.domain.base_domain import BaseMarshallingDomain, \
    BaseMarshallingDomainList
import xml.etree.ElementTree as ET
import json


class HostUsageList(BaseMarshallingDomain):

    ROOT_TAG = 'hostUsageList'

    def __init__(self, hostUsageList=None):
        '''An object that data concerning tickets on a load balancer.

        '''
        self.hostUsageList = hostUsageList

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
        if HostUsageRecords.ROOT_TAG in dic:
            dic[HostUsageRecords.ROOT_TAG] = \
                HostUsageRecords._dict_to_obj(dic.get(
                    HostUsageRecords.ROOT_TAG))
        return HostUsageList(**dic)


class HostUsageRecords(BaseMarshallingDomainList):

    ROOT_TAG = 'hostUsageRecords'

    def __init__(self, hostUsageRecords=None):
        '''An object that data concerning tickets on a load balancer.

        '''
        for record in hostUsageRecords:
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
        kwargs = {cls.ROOT_TAG: [HostUsageRecord._dict_to_obj(record)
                                 for record in dic]}
        return HostUsageRecords(**kwargs)


class HostUsageRecord(BaseMarshallingDomain):

    ROOT_TAG = 'hostUsageRecord'

    def __init__(self, hostId=None, hostUsages=None):
        '''An object that data concerning tickets on a load balancer.

        '''
        self.hostId = hostId
        self.hostUsages = hostUsages

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
        if HostUsages.ROOT_TAG in dic:
            dic[HostUsages.ROOT_TAG] = \
                HostUsages._dict_to_obj(dic.get(HostUsages.ROOT_TAG))
        return HostUsageRecord(**dic)


class HostUsages(BaseMarshallingDomainList):

    ROOT_TAG = 'hostUsages'

    def __init__(self, hostUsages=None):
        '''An object that data concerning tickets on a load balancer.

        '''
        for usage in hostUsages:
            self.append(usage)

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
        kwargs = {cls.ROOT_TAG: [HostUsage._dict_to_obj(usage)
                                 for usage in dic]}
        return HostUsages(**kwargs)


class HostUsage(BaseMarshallingDomain):

    ROOT_TAG = 'hostUsage'

    def __init__(self, day=None, bandwidthIn=None, bandwidthOut=None):
        '''An object that data concerning tickets on a load balancer.

        '''
        self.day = day
        self.bandwidthIn = bandwidthIn
        self.bandwidthOut = bandwidthOut

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
        return HostUsage(**dic)
