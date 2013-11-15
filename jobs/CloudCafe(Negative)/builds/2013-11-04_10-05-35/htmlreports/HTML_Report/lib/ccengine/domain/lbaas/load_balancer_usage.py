from ccengine.domain.base_domain import BaseMarshallingDomain
from ccengine.domain.lbaas.load_balancer_usage_record import \
    LoadBalancerUsageRecord
import json
import xml.etree.ElementTree as ET


class LoadBalancerUsage(BaseMarshallingDomain):

    ROOT_TAG = 'loadBalancerUsage'

    def __init__(self, loadBalancerId=None, loadBalancerName=None,
                 loadBalancerUsageRecords=None, links=None):
        self.loadBalancerId = loadBalancerId
        self.loadBalancerName = loadBalancerName
        self.loadBalancerUsageRecords = loadBalancerUsageRecords
        self.links = links

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        ret = cls._dict_to_obj(json_dict)
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
        lbur_list = []
        for lbur in dic.get(''.join([LoadBalancerUsageRecord.ROOT_TAG, 's'])):
            lbur_list.append(LoadBalancerUsageRecord._dict_to_obj(lbur))
        kwargs = {'loadBalancerId': dic.get('loadBalancerId'),
                  'loadBalancerName': dic.get('loadBalancerName'),
                  'loadBalancerUsageRecords': lbur_list,
                  'links': dic.get('links')}
        return LoadBalancerUsage(**kwargs)
