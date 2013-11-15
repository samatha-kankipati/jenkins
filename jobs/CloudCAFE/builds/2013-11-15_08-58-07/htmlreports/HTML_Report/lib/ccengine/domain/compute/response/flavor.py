from ccengine.domain.base_domain import BaseMarshallingDomain
import json
import xml.etree.ElementTree as ET
from links import Links
from ccengine.common.tools.equality_tools import EqualityTools
from ccengine.common.constants.compute_constants import Constants


class Flavor(BaseMarshallingDomain):

    def __init__(self, **kwargs):
        '''An object that represents a flavor.

        Keyword arguments:
        '''
        super(Flavor, self).__init__(**kwargs)
        for keys, values in kwargs.items():
            setattr(self, keys, values)

    def __repr__(self):
        values = []
        for prop in self.__dict__:
            values.append("%s: %s" % (prop, self.__dict__[prop]))
        return '[' + ', '.join(values) + ']'

    @classmethod
    def _json_to_obj(cls, serialized_str):
        '''Returns an instance of a Flavor based on the json serialized_str
        passed in.'''
        json_dict = json.loads(serialized_str)
        ''' We may get a single flavor or a list of flavors'''
        if 'flavor' in json_dict.keys():
            flavor = cls._dict_to_obj(json_dict['flavor'])
            return flavor

        if 'flavors' in json_dict.keys():
            flavors = []
            for flavor_dict in json_dict['flavors']:
                flavor = cls._dict_to_obj(flavor_dict)
                flavors.append(flavor)
            return flavors

    @classmethod
    def _dict_to_obj(cls, flavor_dict):
        '''Helper method to turn dictionary into Server instance.'''
        flavor = Flavor(**flavor_dict)
        if hasattr(flavor, 'links'):
            flavor.links = Links._dict_to_obj(flavor.links)
        if hasattr(flavor, 'OS-FLV-EXT-DATA:ephemeral'):
            setattr(flavor, 'ephemeral',
                    getattr(flavor, 'OS-FLV-EXT-DATA:ephemeral'))
        return flavor

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        '''Returns an instance of a Flavor based on the xml serialized_str
        passed in.'''
        element = ET.fromstring(serialized_str)
        cls._remove_namespace(element, Constants.XML_API_NAMESPACE)
        cls._remove_namespace(element, Constants.XML_API_ATOM_NAMESPACE)

        if element.tag == 'flavor':
            flavor = cls._xml_ele_to_obj(element)
            return flavor

        if element.tag == 'flavors':
            flavors = []
            for flavor in element.findall('flavor'):
                flavor = cls._xml_ele_to_obj(flavor)
                flavors.append(flavor)
            return flavors

    @classmethod
    def _xml_ele_to_obj(cls, element):
        '''Helper method to turn ElementTree instance to Flavor instance.'''
        flavor_dict = element.attrib
        if 'vcpus' in flavor_dict:
            flavor_dict['vcpus'] = flavor_dict.get('vcpus') and int(flavor_dict.get('vcpus'))
        if 'disk' in flavor_dict:
            flavor_dict['disk'] = flavor_dict.get('disk') and int(flavor_dict.get('disk'))
        if 'rxtx_factor' in flavor_dict:
            flavor_dict['rxtx_factor'] = flavor_dict.get('rxtx_factor') \
            and float(flavor_dict.get('rxtx_factor'))
        if 'ram' in flavor_dict:
            flavor_dict['ram'] = flavor_dict.get('ram') and int(flavor_dict.get('ram'))
        if 'swap' in flavor_dict:
            flavor_dict['swap'] = flavor_dict.get('swap') and int(flavor_dict.get('swap'))
        if 'id' in flavor_dict:
            flavor_dict['id'] = flavor_dict.get('id')
        if 'name' in flavor_dict:
            flavor_dict['name'] = flavor_dict.get('name')
        if 'swap' in flavor_dict:
            flavor_dict['ephemeral'] = \
                flavor_dict.get('OS-FLV-EXT-DATA:ephemeral') and \
                int(flavor_dict.get('OS-FLV-EXT-DATA:ephemeral'))
        flavor = Flavor(**flavor_dict)
        flavor.links = Links._xml_ele_to_obj(element)
        return flavor

    def __eq__(self, other):
        """
        @summary: Overrides the default equals
        @param other: Flavor object to compare with
        @type other: Flavor
        @return: True if Flavor objects are equal, False otherwise
        @rtype: bool
        """
        return EqualityTools.are_objects_equal(self, other, ['links'])

    def __ne__(self, other):
        """
        @summary: Overrides the default not-equals
        @param other: Flavor object to compare with
        @type other: Flavor
        @return: True if Flavor objects are not equal, False otherwise
        @rtype: bool
        """
        return not self == other


class FlavorMin(Flavor):
    """
    @summary: Represents minimum details of a flavor
    """
    def __init__(self, **kwargs):
        '''Flavor Min has only id, name and links '''
        for keys, values in kwargs.items():
            setattr(self, keys, values)

    def __eq__(self, other):
        """
        @summary: Overrides the default equals
        @param other: FlavorMin object to compare with
        @type other: FlavorMin
        @return: True if FlavorMin objects are equal, False otherwise
        @rtype: bool
        """
        return EqualityTools.are_objects_equal(self, other, ['links'])

    def __ne__(self, other):
        """
        @summary: Overrides the default not-equals
        @param other: FlavorMin object to compare with
        @type other: FlavorMin
        @return: True if FlavorMin objects are not equal, False otherwise
        @rtype: bool
        """
        return not self == other

    @classmethod
    def _xml_ele_to_obj(cls, element):
        '''Helper method to turn ElementTree instance to Server instance.'''
        flavor_dict = element.attrib
        flavor_min = FlavorMin(**flavor_dict)
        if hasattr(flavor_min, 'links'):
            flavor_min.links = Links._xml_ele_to_obj(element)
        return flavor_min

    @classmethod
    def _dict_to_obj(cls, flavor_dict):
        '''Helper method to turn dictionary into Server instance.'''
        flavor_min = FlavorMin(**flavor_dict)
        if hasattr(flavor_min, 'links'):
            flavor_min.links = Links._dict_to_obj(flavor_min.links)
        return flavor_min
