from ccengine.domain.base_domain import BaseMarshallingDomain
import json
import xml.etree.ElementTree as ET


class LoadBalancerUsageRecord(BaseMarshallingDomain):

    ROOT_TAG = 'loadBalancerUsageRecord'

    def __init__(self, id=None, startTime=None, endTime=None, eventType=None,
                 numVips=None, incomingTransfer=None, outgoingTransfer=None,
                 incomingTransferSsl=None, outgoingTransferSsl=None,
                 vipType=None, averageNumConnections=None,
                 averageNumConnectionsSsl=None, numPolls=None, sslMode=None):
        '''An object that represents the data of a Load Balancer usage
           record.
        '''
        self.id = id
        self.startTime = startTime
        self.endTime = endTime
        self.eventType = eventType
        self.numVips = numVips
        self.incomingTransfer = incomingTransfer
        self.outgoingTransfer = outgoingTransfer
        self.incomingTransferSsl = incomingTransferSsl
        self.outgoingTransferSsl = outgoingTransferSsl
        self.vipType = vipType
        self.averageNumConnections = averageNumConnections
        self.averageNumConnectionsSsl = averageNumConnectionsSsl
        self.numPolls = numPolls
        self.sslMode = sslMode

    @classmethod
    def _json_to_obj(cls, serialized_str):
        ret = None
        json_dict = json.loads(serialized_str)
        if cls.ROOT_TAG in json_dict:
            ret = cls._dict_to_obj(json_dict.get(cls.ROOT_TAG))
        if ''.join([cls.ROOT_TAG, 's']) in json_dict:
            ret = []
            for item in json_dict.get(''.join([cls.ROOT_TAG, 's'])):
                ret.append(cls._dict_to_obj(item))
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
        return LoadBalancerUsageRecord(**dic)
