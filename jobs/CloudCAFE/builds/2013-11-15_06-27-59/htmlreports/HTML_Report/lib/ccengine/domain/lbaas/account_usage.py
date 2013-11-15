from ccengine.domain.base_domain import BaseMarshallingDomain
from ccengine.domain.lbaas.account_usage_record import AccountUsageRecord
import json
import xml.etree.ElementTree as ET


class AccountUsage(BaseMarshallingDomain):

    ROOT_TAG = 'accountUsage'

    def __init__(self, accountUsageRecords=None, links=None):
        self.accountUsageRecords = accountUsageRecords
        self.links = links

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
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
        aur_list = []
        for aur in dic.get(''.join([AccountUsageRecord.ROOT_TAG, 's'])):
            aur_list.append(AccountUsageRecord._dict_to_obj(aur))
        kwargs = {'accountUsageRecords': aur_list, 'links': dic.get('links')}
        return AccountUsage(**kwargs)
