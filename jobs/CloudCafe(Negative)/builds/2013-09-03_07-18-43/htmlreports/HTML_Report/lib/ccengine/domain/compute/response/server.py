from ccengine.domain.base_domain import BaseDomain
from ccengine.domain.base_domain import BaseMarshallingDomain
import json
import xml.etree.ElementTree as ET
from ccengine.domain.compute.response.links import Links
from ccengine.domain.compute.response.flavor import Flavor, FlavorMin
from ccengine.domain.compute.response.image import Image, ImageMin
from ccengine.domain.images.qonos_ext.response.scheduled_images import ScheduledImages
from ccengine.common.tools.equality_tools import EqualityTools
from ccengine.common.constants.compute_constants import Constants
from ccengine.domain.compute.metadata import Metadata
import re


class Server(BaseMarshallingDomain):

    ROOT_TAG = 'server'

    def __init__(self, **kwargs):
        super(Server, self).__init__(**kwargs)
        for keys, values in kwargs.items():
            setattr(self, keys, values)

    @classmethod
    def _json_to_obj(cls, serialized_str):
        '''Returns an instance of a Server based on the json serialized_str
        passed in.'''
        ret = None
        json_dict = json.loads(serialized_str)
        if 'server' in json_dict.keys():
            ret = cls._dict_to_obj(json_dict['server'])
        if 'servers' in json_dict.keys():
            ret = []
            for server in json_dict['servers']:
                s = cls._dict_to_obj(server)
                ret.append(s)
        return ret

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        '''Returns an instance of a Server based on the xml serialized_str
        passed in.'''
        element = ET.fromstring(serialized_str)
        cls._remove_namespace(element, Constants.XML_API_NAMESPACE)
        cls._remove_namespace(element, Constants.XML_API_EXTENDED_STATUS_NAMESPACE)
        cls._remove_namespace(element, Constants.XML_API_DISK_CONFIG_NAMESPACE)
        cls._remove_namespace(element, Constants.XML_API_ATOM_NAMESPACE)
        cls._remove_namespace(element, Constants.XML_API_SCH_IMG_NAMESPACE)
        if element.tag == 'server':
            ret = cls._xml_ele_to_obj(element)
        if element.tag == 'servers':
            ret = []
            for server in element.findall('server'):
                s = cls._xml_ele_to_obj(server)
                ret.append(s)
        return ret

    @classmethod
    def _xml_ele_to_obj(cls, element):
        '''Helper method to turn ElementTree instance to Server instance.'''
        server_dict = element.attrib
        if 'progress' in server_dict:
            server_dict['progress'] = server_dict.get('progress') \
            and int(server_dict.get('progress'))
        if 'tenantId' in server_dict:
            server_dict['tenant_id'] = server_dict.get('tenantId')
        if 'userId' in server_dict:
            server_dict['user_id'] = server_dict.get('userId')
        server = Server(**server_dict)
        if element.find('addresses') is not None:
            server.addresses = Addresses._xml_ele_to_obj(element.find('addresses'))
        server.links = Links._xml_ele_to_obj(element)
        if element.find('flavor') is not None:
            server.flavor = Flavor._xml_ele_to_obj(element.find('flavor'))
        if element.find('image') is not None:
            server.image = Image._xml_ele_to_obj(element.find('image'))
        if element.find('metadata') is not None:
            server.metadata = Metadata._xml_ele_to_obj(element)
        for child in element:
            if child.tag == 'image_schedule':
                server.image_schedule = ScheduledImages._xml_ele_to_obj(child)
        '''Parse for those keys which have the namespace prefixed, strip the namespace out
        and take only the actual values such as diskConfig, power_state and assign to server obj'''
        for each in server_dict:
            if each.startswith("{"):
                newkey = re.split("}", each)[1]
                if server_dict[each] == "None":
                    setattr(server, newkey, None)
                else:
                    setattr(server, newkey, server_dict.get(each))
        if hasattr(server, 'power_state'):
            setattr(server, 'power_state', int(getattr(server, 'power_state')))
        return server

    @classmethod
    def _dict_to_obj(cls, server_dict):
        '''Helper method to turn dictionary into Server instance.'''
        server = Server(**server_dict)
        if hasattr(server, 'links'):
            server.links = Links._dict_to_obj(server.links)
        if hasattr(server, 'addresses'):
            server.addresses = Addresses._dict_to_obj(server.addresses)
        if hasattr(server, 'flavor'):
            server.flavor = FlavorMin._dict_to_obj(server.flavor)
        if hasattr(server, 'image'):
            server.image = ImageMin._dict_to_obj(server.image)
        if hasattr(server, 'metadata'):
            server.metadata = Metadata._dict_to_obj(server.metadata)
        if hasattr(server, 'OS-EXT-STS:power_state'):
            setattr(server, 'power_state' , getattr(server, 'OS-EXT-STS:power_state'))
        if hasattr(server, 'OS-DCF:diskConfig'):
            setattr(server, 'diskConfig' , getattr(server, 'OS-DCF:diskConfig'))
        if hasattr(server, 'OS-EXT-STS:task_state'):
            setattr(server, 'task_state', getattr(server, 'OS-EXT-STS:task_state'))
        if hasattr(server, 'OS-EXT-STS:vm_state'):
            setattr(server, 'vm_state', getattr(server, 'OS-EXT-STS:vm_state'))
        '''Parse for those keys which have the namespace prefixed, strip the namespace out
        and take only the actual values such as diskConfig, power_state and assign to server obj'''
        for each in server_dict:
            if each.startswith("{"):
                newkey = re.split("}", each)[1]
                setattr(server, newkey, server_dict[each])
        return server

    def __eq__(self, other):
        """
        @summary: Overrides the default equals
        @param other: Server object to compare with
        @type other: Server
        @return: True if Server objects are equal, False otherwise
        @rtype: bool
        """
        return EqualityTools.are_objects_equal(self, other, ['adminPass', 'updated', 'progress'])

    def __ne__(self, other):
        """
        @summary: Overrides the default not-equals
        @param other: Server object to compare with
        @type other: Server
        @return: True if Server objects are not equal, False otherwise
        @rtype: bool
        """
        return not self == other

    def min_details(self):
        """
        @summary: Get the Minimum details of server
        @return: Minimum details of server
        @rtype: ServerMin
        """
        return ServerMin(name=self.name, id=self.id, links=self.links)


class ServerMin(Server):
    """
    @summary: Represents minimum details of a server
    """
    def __init__(self, **kwargs):
        for keys, values in kwargs.items():
            setattr(self, keys, values)

    def __eq__(self, other):
        """
        @summary: Overrides the default equals
        @param other: ServerMin object to compare with
        @type other: ServerMin
        @return: True if ServerMin objects are equal, False otherwise
        @rtype: bool
        """
        return EqualityTools.are_objects_equal(self, other)

    def __ne__(self, other):
        """
        @summary: Overrides the default equals
        @param other: ServerMin object to compare with
        @type other: ServerMin
        @return: True if ServerMin objects are not equal, False otherwise
        @rtype: bool
        """
        return not self == other

    @classmethod
    def _xml_ele_to_obj(cls, element):
        '''Helper method to turn ElementTree instance to Server instance.'''
        if element.find('server') is not None:
            element = element.find('server')
            server_dict = element.attrib
            servermin = ServerMin(**server_dict)
            servermin.links = Links._xml_ele_to_obj(element)
        return servermin

    @classmethod
    def _dict_to_obj(cls, server_dict):
        '''Helper method to turn dictionary into Server instance.'''
        servermin = ServerMin(**server_dict)
        if hasattr(servermin, 'links'):
            servermin.links = Links._dict_to_obj(servermin.links)
        '''Parse for those keys which have the namespace prefixed, strip the namespace out
        and take only the actual values such as diskConfig, power_state and assign to server obj'''
        for each in server_dict:
            if each.startswith("{"):
                newkey = re.split("}", each)[1]
                setattr(servermin, newkey, server_dict[each])

        return servermin


#New Version
class Addresses(BaseMarshallingDomain):
    ROOT_TAG = 'addresses'

    class _NetworkAddressesList(BaseDomain):

        def __init__(self):
            super(Addresses._NetworkAddressesList, self).__init__()
            self.addresses = []

        def __repr__(self):
            ret = ''
            for a in self.addresses:
                ret = ret + 'Address:\n\t%s' % str(a)
            return ret

        def append(self, addr_obj):
            self.addresses.append(addr_obj)

        @property
        def ipv4(self):
            for addr in self.addresses:
                if str(addr.version) == '4':
                    return str(addr.addr)
            return None

        @property
        def ipv6(self):
            for addr in self.addresses:
                if str(addr.version) == '6':
                    return str(addr.addr)
            return None

        @property
        def count(self):
            return len(self.addresses)

    class _AddrObj(BaseDomain):

        def __init__(self, version=None, addr=None):
            super(Addresses._AddrObj, self).__init__()
            self.version = version
            self.addr = addr

        def __repr__(self):
            ret = ''
            ret = ret + 'version: %s' % str(self.version)
            ret = ret + 'addr: %s' % str(self.addr)
            return ret

    def __init__(self, addr_dict):
        super(Addresses, self).__init__()

        #Preset properties that should be expected, if not always populated
        self.public = None
        self.private = None

        if len(addr_dict) > 1:
            ''' adddress_type is PUBLIC/PRIVATE '''
            for address_type in addr_dict:
                ''' address_list is list of address dictionaries'''
                address_list = addr_dict[address_type]
                ''' init a network object with empty addresses list '''
                network = self._NetworkAddressesList()
                for address in address_list:
                    addrobj = self._AddrObj(version=int(address.get('version')),
                                            addr=address.get('addr'))
                    network.addresses.append(addrobj)
                setattr(self, address_type, network)
        # Validation in case we have nested addresses in addresses
        else:
            big_addr_dict = addr_dict
            if big_addr_dict.get('addresses') is not None:
                addr_dict = big_addr_dict.get('addresses')
            for address_type in addr_dict:
                ''' address_list is list of address dictionaries'''
                address_list = addr_dict[address_type]
                ''' init a network object with empty addresses list '''
                network = self._NetworkAddressesList()
                for address in address_list:
                    addrobj = self._AddrObj(version=address.get('version'),
                                            addr=address.get('addr'))
                    network.addresses.append(addrobj)
                setattr(self, address_type, network)

    def get_by_name(self, label):
        try:
            ret = getattr(self, label)
        except AttributeError:
            ret = None
        return ret

    def __repr__(self):
        ret = '\n'
        ret = ret + '\npublic:\n\t\t%s' % str(self.public)
        ret = ret + '\nprivate:\n\t\t%s' % str(self.private)
        return ret

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        return Addresses(json_dict)

    @classmethod
    def _dict_to_obj(cls, serialized_str):
        return Addresses(serialized_str)

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        element = ET.fromstring(serialized_str)
        cls._remove_namespace(element, Constants.XML_API_NAMESPACE)
        return cls._xml_ele_to_obj(element)

    @classmethod
    def _xml_ele_to_obj(cls, element):
        addresses = {}
        if element.tag != 'network':
            networks = element.findall('network')
            for network in networks:
                network_id = network.attrib.get('id')
                addresses[network_id] = []
                for ip in network:
                    addresses[network_id].append(ip.attrib)
        else:
            networks = element
            network_id = networks.attrib.get('id')
            addresses[network_id] = []
            for ip in networks:
                addresses[network_id].append(ip.attrib)

        return Addresses(addresses)
