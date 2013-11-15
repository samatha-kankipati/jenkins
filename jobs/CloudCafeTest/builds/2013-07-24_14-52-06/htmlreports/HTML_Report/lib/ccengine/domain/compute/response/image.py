from ccengine.domain.base_domain import BaseMarshallingDomain
from ccengine.domain.compute.response.links import Links
import json
import xml.etree.ElementTree as ET
from ccengine.common.tools.equality_tools import EqualityTools
from ccengine.common.constants.compute_constants import Constants
from ccengine.domain.compute.metadata import Metadata


class Image(BaseMarshallingDomain):

    ROOT_TAG = 'image'

    def __init__(self, **kwargs):
        '''An object that represents an image response object.
        Keyword arguments:
        '''
        super(Image, self).__init__(**kwargs)
        for keys, values in kwargs.items():
            setattr(self, keys, values)

    def __eq__(self, other):
        """
        @summary: Overrides the default equals
        @param other: Image object to compare with
        @type other: Image
        @return: True if Image objects are equal, False otherwise
        @rtype: bool
        """
        return EqualityTools.are_objects_equal(self, other)

    def __ne__(self, other):
        """
        @summary: Overrides the default not-equals
        @param other: Image object to compare with
        @type other: Image
        @return: True if Image objects are not equal, False otherwise
        @rtype: bool
        """
        return not self == other

    def __repr__(self):
        values = []
        for prop in __dict__:
            values.append("%s: %s" % (prop, __dict__[prop]))
        return '[' + ', '.join(values) + ']'

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        if 'image' in json_dict.keys():
            image = cls._dict_to_obj(json_dict['image'])
            return image

        if 'images' in json_dict.keys():
            images = []
            for image_dict in json_dict['images']:
                images.append(cls._dict_to_obj(image_dict))
            return images

    @classmethod
    def _dict_to_obj(cls, json_dict):
        image = Image(**json_dict)
        if hasattr(image, 'links'):
            image.links = Links._dict_to_obj(image.links)
        if hasattr(image, 'metadata'):
            image.metadata = Metadata._dict_to_obj(image.metadata)
        if hasattr(image, 'server'):
            '''To prevent circular import issue import just in time'''
            from ccengine.domain.compute.response.server import ServerMin
            image.server = ServerMin._dict_to_obj(image.server)
        if hasattr(image, 'OS-DCF:diskConfig'):
            setattr(image, 'diskConfig' , getattr(image, 'OS-DCF:diskConfig'))
            
        return image

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        '''Returns an instance of a Image based on the xml serialized_str
        passed in.'''
        element = ET.fromstring(serialized_str)
        cls._remove_namespace(element, Constants.XML_API_NAMESPACE)
        cls._remove_namespace(element, Constants.XML_API_ATOM_NAMESPACE)
        cls._remove_namespace_from_attrb(element.attrib, Constants.XML_API_DISK_CONFIG_NAMESPACE)

        if element.tag == 'image':
            image = cls._xml_ele_to_obj(element)
            return image

        if element.tag == 'images':
            images = []
            for image in element.findall('image'):
                image = cls._xml_ele_to_obj(image)
                images.append(image)
            return images

    @classmethod
    def _xml_ele_to_obj(cls, element):
        image_dict = element.attrib
        if 'minDisk' in image_dict:
            image_dict['minDisk'] = image_dict.get('minDisk') and int(image_dict.get('minDisk'))
        if 'progress' in image_dict:
            image_dict['progress'] = image_dict.get('progress') and int(image_dict.get('progress'))
        if 'minRam' in image_dict:
            image_dict['minRam'] = image_dict.get('minRam') and int(image_dict.get('minRam'))
        image = Image(**image_dict)
        if element.find('link') is not None:
            image.links = Links._xml_ele_to_obj(element)
        if element.find('metadata') is not None:
            image.metadata = Metadata._xml_ele_to_obj(element)
        if element.find('server') is not None:
            '''To prevent circular import issue import just in time'''
            from ccengine.domain.compute.response.server import ServerMin
            image.server = ServerMin._xml_ele_to_obj(element)


        return image


class ImageMin(Image):
    """
    @summary: Represents minimum details of a image
    """
    def __init__(self, **kwargs):
        '''Image min should only have id, name and links '''
        for keys, values in kwargs.items():
            setattr(self, keys, values)

    def __eq__(self, other):
        """
        @summary: Overrides the default equals
        @param other: ImageMin object to compare with
        @type other: ImageMin
        @return: True if ImageMin objects are equal, False otherwise
        @rtype: bool
        """
        return EqualityTools.are_objects_equal(self, other)

    def __ne__(self, other):
        """
        @summary: Overrides the default not-equals
        @param other: ImageMin object to compare with
        @type other: ImageMin
        @return: True if ImageMin objects are not equal, False otherwise
        @rtype: bool
        """
        return not self == other

    @classmethod
    def _xml_ele_to_obj(cls, element):
        '''Helper method to turn ElementTree instance to Image instance.'''
        cls._remove_namespace(element, Constants.XML_API_NAMESPACE)
        image_dict = element.attrib
        image_min = ImageMin(**image_dict)
        image_min.links = Links._xml_ele_to_obj(element)
        return image_min

    @classmethod
    def _dict_to_obj(cls, json_dict):
        image_min = ImageMin(**json_dict)
        if hasattr(image_min, 'links'):
            image_min.links = Links(image_min.links)
        return image_min
