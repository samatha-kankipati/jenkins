import json
import xml.etree.ElementTree as ET
from ccengine.common.tools import datatools
from ccengine.domain.base_domain import BaseMarshallingDomain


class Network(BaseMarshallingDomain):

    ROOT_TAG = 'network'

    def __init__(self, name=None, admin_state_up=None, id=None, status=None,
                 shared=None, subnets=None, tenant_id=None,
                 port_security_enabled=None, router_external=None):
        super(Network, self).__init__()
        self.name = name
        self.admin_state_up = admin_state_up
        self.id = id
        self.status = status
        self.shared = shared
        self.subnets = subnets
        self.tenant_id = tenant_id
        self.port_security_enabled = port_security_enabled
        self.router_external = router_external

    @classmethod
    def _json_to_obj(cls, serialized_str):
        ret = None
        json_resp = json.loads(serialized_str)

        # Replacing response variable names that can not be mapped to Python
        json_dict = datatools.replace_response_key(json_resp,
                                                             'router:external',
                                                             'router_external')

        if 'networks' in json_dict:
            ret = []
            for network in json_dict.get('networks'):
                ret.append(Network(**network))

        elif 'network' in json_dict:
            network_dict = json_dict.get('network')
            ret = Network(**network_dict)

        return ret

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        """Creates Python Object from XML data, may be updated once
        the Quantum Networks XML response format is given"""
        ret = cls._xml_ele_to_obj(serialized_str)

        #to use in case the values come as attributes
        #ret = cls._xml_ele_to_obj(serialized_str, 'attr')

        return ret

    @classmethod
    def _xml_ele_to_obj(cls, serialized_str, format_type='text'):
        """Simple XML-Python object converter that expects values as text
        node values or as node attribute values (format type attr)"""
        element = ET.fromstring(serialized_str)
        ret = []
        if element.tag == 'networks':
            element_list = element.findall('network')
        #if there is no networks tag and we only have one network
        else:
            element_list = [element]
        for ele in element_list:
            #doing a copy so there are no issues with other inherited attrs
            network_dict = dict(vars(cls))
            if format_type == 'attr':
                attr_dict = ele.attrib
                network_dict.update(attr_dict)
                #expecting the subnets as subnet child nodes
                subnets = ele.find('subnets')
                if subnets is not None:
                    subnet_list = subnets.findall('subnet')
                    network_subnets = []
                    for sub in subnet_list:
                        #this may be different once it comes out
                        sub_id = sub.get('id')
                        if sub_id is not None:
                            network_subnets.append(sub_id)
                    if len(network_subnets) != 0:
                        network_dict['subnets'] = network_subnets
            else:
                status = ele.find('status')
                if status is not None:
                    network_dict['status'] = status.text
                name = ele.find('name')
                if name is not None:
                    network_dict['name'] = name.text
                admin_state_up = ele.find('admin_state_up')
                if admin_state_up is not None:
                    network_dict['admin_state_up'] = admin_state_up.text
                tenant_id = ele.find('tenant_id')
                if tenant_id is not None:
                    network_dict['tenant_id'] = tenant_id.text
                net_id = ele.find('id')
                if net_id is not None:
                    network_dict['id'] = net_id.text
                shared = ele.find('shared')
                if shared is not None:
                    network_dict['shared'] = shared.text
                #expecting the subnets as subnet child nodes
                subnets = ele.find('subnets')
                if subnets is not None:
                    subnet_list = subnets.findall('subnet')
                    network_subnets = []
                    for sub in subnet_list:
                        #this may be different once it comes out
                        if sub.text is not None:
                            network_subnets.append(sub.text)
                    if len(network_subnets) != 0:
                        network_dict['subnets'] = network_subnets
            #log is not defined in this network class it will be inherited
            if '_log' in network_dict:
                del network_dict['_log']
            ret.append(Network(**network_dict))
        #if there is only 1 network only the network object is returned
        if len(ret) == 1:
            return ret[0]
        else:
            return ret
