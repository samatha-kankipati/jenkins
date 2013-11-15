from ccengine.domain.base_domain import BaseMarshallingDomain
from ccengine.domain.lbaas.account_usage import AccountUsage
from ccengine.domain.lbaas.load_balancer_usage import LoadBalancerUsage
import json
import xml.etree.ElementTree as ET


class AccountBilling(BaseMarshallingDomain):

    ROOT_TAG = 'accountBilling'

    def __init__(self, accountId=None, accountUsage=None,
                 loadBalancerUsages=None):
        self.accountId = accountId
        self.accountUsage = accountUsage
        self.loadBalancerUsages = loadBalancerUsages

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
        au = AccountUsage._dict_to_obj(dic.get(AccountUsage.ROOT_TAG))
        lbu_list = []
        for lbu in dic.get(''.join([LoadBalancerUsage.ROOT_TAG, 's'])):
            lbu_list.append(LoadBalancerUsage._dict_to_obj(lbu))
        kwargs = {'accountId': dic.get('accountId'), 'accountUsage': au,
                  'loadBalancerUsages': lbu_list}
        return AccountBilling(**kwargs)
