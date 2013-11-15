from ccengine.domain.base_domain import BaseMarshallingDomain
import json
import xml.etree.ElementTree as ET
from ccengine.common.constants.compute_constants import Constants


class VirtualInterface(BaseMarshallingDomain):

    def __init__(self, id=None, mac_address=None, ip_addresses=None):
        '''An object that represents the data of a Virtual Interface.
        '''
        super(VirtualInterface, self).__init__()
        self.id = id
        self.mac_address = mac_address
        self.ip_addresses = ip_addresses

    def get_ipv4_address(self, network_id):
        ret = None
        for ip_address in self.ip_addresses:
            if ip_address.network_id == network_id and\
                ip_address.address.find('.') > 0:
                ret = ip_address
                break
        return ret

    def get_ipv6_address(self, network_id):
        ret = None
        for ip_address in self.ip_addresses:
            if ip_address.network_id == network_id and\
                ip_address.address.find(':') > 0:
                ret = ip_address
                break
        return ret

    @property
    def network_label(self):
        for ip_address in self.ip_addresses:
            if ip_address.network_label is not None:
                return ip_address.network_label

    @property
    def network_id(self):
        for ip_address in self.ip_addresses:
            if ip_address.network_id is not None:
                return ip_address.network_id

    @classmethod
    def _json_to_obj(cls, serialized_str):
        ret = None
        json_dict = json.loads(serialized_str)
        if 'virtual_interface' in json_dict:
            interface_dict = json_dict.get('virtual_interface')
            ip_addrs = IPAddress._dict_to_obj(interface_dict)
            interface_dict['ip_addresses'] = ip_addrs
            ret = VirtualInterface(**interface_dict)
        if 'virtual_interfaces' in json_dict:
            ret = []
            for interface_dict in json_dict.get('virtual_interfaces'):
                ip_addrs = IPAddress._dict_to_obj(interface_dict)
                interface_dict['ip_addresses'] = ip_addrs
                ret.append(VirtualInterface(**interface_dict))
        return ret

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        element = ET.fromstring(serialized_str)
        cls._remove_namespace(element, Constants.XML_API_NAMESPACE)
        ret = None
        if element.tag == 'virtual_interfaces':
            ret = []
            ele_list = element.findall('virtual_interface')
            for ele in ele_list:
                ip_addrs = IPAddress._ele_to_obj(ele)
                ret.append(VirtualInterface(id=ele.get('id'),
                                            mac_address=ele.get('mac_address'),
                                            ip_addresses=ip_addrs))
        return ret


class IPAddress(BaseMarshallingDomain):

    def __init__(self, network_id=None, network_label=None, address=None):
        super(IPAddress, self).__init__()
        self.network_id = network_id
        self.network_label = network_label
        self.address = address

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        return cls._dict_to_obj(json_dict)

    @classmethod
    def _dict_to_obj(cls, json_dict):
        if 'ip_addresses' in json_dict:
            ret = []
            json_dict = json_dict.get('ip_addresses')
            for addr in json_dict:
                ret.append(IPAddress(**addr))
        return ret

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        element = ET.fromstring(serialized_str)
        return cls._ele_to_obj(element)

    @classmethod
    def _ele_to_obj(cls, element):
        if element is None:
            return None
        ret = []
        ele_list = element.findall('ip_address')
        for element in ele_list:
            ret.append(IPAddress(network_id=element.get('network_id'),
                                 network_label=element.get('network_label'),
                                 address=element.get('address')))
        return ret
