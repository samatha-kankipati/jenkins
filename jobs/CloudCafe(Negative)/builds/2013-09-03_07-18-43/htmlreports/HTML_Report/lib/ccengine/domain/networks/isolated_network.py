from ccengine.domain.base_domain import BaseMarshallingDomain
import json
import xml.etree.ElementTree as ET


class IsolatedNetwork(BaseMarshallingDomain):

    def __init__(self, cidr, label, id=None):
        '''An object that represents the data of an Isolated Network.
        '''
        self.cidr = cidr
        self.label = label
        self.id = id

    def _obj_to_json(self):
        ret = {'network': {'id': self.id,
                           'cidr': self.cidr,
                           'label': self.label}}
        ret = json.dumps(ret)
        return ret

    def _obj_to_xml(self):
        element = ET.Element('network')
        id_ele = ET.Element('id')
        cidr_ele = ET.Element('cidr')
        label_ele = ET.Element('label')
        if self.id is not None:
            id_ele.text = self.id
        cidr_ele.text = self.cidr
        label_ele.text = self.label
        element.append(id_ele)
        element.append(cidr_ele)
        element.append(label_ele)
        ret = ET.tostring(element)
        return ret

    @classmethod
    def _json_to_obj(cls, serialized_str):
        ret = None
        json_dict = json.loads(serialized_str)
        if json_dict.get('network') is not None:
            json_dict = json_dict.get('network')
            ret = IsolatedNetwork(id=json_dict.get('id'),
                                  cidr=json_dict.get('cidr'),
                                  label=json_dict.get('label'))
        if json_dict.get('networks') is not None:
            ret = []
            for network_dict in json_dict.get('networks'):
                ret.append(IsolatedNetwork(id=network_dict.get('id'),
                                           cidr=network_dict.get('cidr'),
                                           label=network_dict.get('label')))
        return ret

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        element = ET.fromstring(serialized_str)
        ret = None
        if element.tag == 'network':
            cidr = None
            if element.find('cidr') is not None:
                cidr = element.find('cidr').text
            ret = IsolatedNetwork(cidr=cidr,
                                  label=element.find('label').text,
                                  id=element.find('id').text)
        if element.tag == 'networks':
            ret = []
            network_ele_list = element.findall('network')
            for element in network_ele_list:
                cidr = None
                if element.find('cidr') is not None:
                    cidr = element.find('cidr').text
                ret.append(IsolatedNetwork(cidr=cidr,
                                           label=element.find('label').text,
                                           id=element.find('id').text))
        return ret
