import json
import xml.etree.ElementTree as ET

from ccengine.common.constants.compute_constants import Constants
from ccengine.common.tools.equality_tools import EqualityTools
from ccengine.domain.base_domain import BaseMarshallingDomain


class ImageResponse(BaseMarshallingDomain):

    ROOT_TAG = 'image'

    def __init__(self, **kwargs):
        """An object that represents a legacy image response object.
        """
        super(ImageResponse, self).__init__(**kwargs)
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
        for prop, value in self.__dict__.items():
            values.append("{0}: {1}".format(prop, value))
        return "[{0}]".format(', '.join(values))

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
        image = ImageResponse(**json_dict)
        if hasattr(image, 'serverId'):
            setattr(image, 'server_id', getattr(image, 'serverId'))
        if hasattr(image, 'minRam'):
            setattr(image, 'min_ram', getattr(image, 'minRam'))
        if hasattr(image, 'nextGenUUID'):
            setattr(image, 'next_gen_uuid', getattr(image, 'nextGenUUID'))
        return image

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        """
        Returns an instance of a Image based on the xml serialized_str
        passed in.
        """
        element = ET.fromstring(serialized_str)
        cls._remove_namespace(element, Constants.XML_API_NAMESPACE)
        cls._remove_namespace(element, Constants.XML_API_ATOM_NAMESPACE)
        cls._remove_namespace_from_attrb(
            element.attrib, Constants.XML_API_DISK_CONFIG_NAMESPACE)

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
            image_dict['min_disk'] = \
            image_dict.get('minDisk') and int(image_dict.get('minDisk'))
        if 'progress' in image_dict:
            image_dict['progress'] = \
            image_dict.get('progress') and int(image_dict.get('progress'))
        if 'minRam' in image_dict:
            image_dict['min_ram'] = \
            image_dict.get('minRam') and int(image_dict.get('minRam'))
        image = ImageResponse(**image_dict)
        return image
