from ccengine.domain.base_domain import BaseMarshallingDomain
import json
import xml.etree.ElementTree as ET


class SSLTermination(BaseMarshallingDomain):

    ROOT_TAG = 'sslTermination'

    def __init__(self, certificate=None, enabled=None, secureTrafficOnly=None,
                 privatekey=None, intermediateCertificate=None,
                 securePort=None):
        '''An object that represents the data of Load Balancer SSL Termination.
        '''
        self.certificate = certificate
        self.enabled = enabled
        self.secureTrafficOnly = secureTrafficOnly
        self.privatekey = privatekey
        self.intermediateCertificate = intermediateCertificate
        self.securePort = securePort

    def _obj_to_json(self):
        ret = self._auto_to_dict()
        return json.dumps(ret)

    def _obj_to_xml(self):
#        element = ET.Element('network')
#        id_ele = ET.Element('id')
#        cidr_ele = ET.Element('cidr')
#        label_ele = ET.Element('label')
#        if self.id is not None:
#            id_ele.text = self.id
#        cidr_ele.text = self.cidr
#        label_ele.text = self.label
#        element.append(id_ele)
#        element.append(cidr_ele)
#        element.append(label_ele)
#        ret = ET.tostring(element)
#        return ret
        pass

    @classmethod
    def _json_to_obj(cls, serialized_str):
        ret = None
        json_dict = json.loads(serialized_str)
        if json_dict.get(cls.ROOT_TAG) is not None:
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
        return SSLTermination(**dic)
