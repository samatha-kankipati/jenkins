import json
import xml.etree.ElementTree as ET

from ccengine.domain.base_domain import BaseMarshallingDomain


class CreateImage(BaseMarshallingDomain):
    '''
    Create Image Server Action Request Object
    '''
    ROOT_TAG = 'create_image'

    def __init__(self, name, server_id):
        super(CreateImage, self).__init__()
        self.name = name
        self.server_id = server_id

    def _obj_to_dict(self):
        """
        @summary: Convert send message object to JSON dictionary
        @return: Dictionary of image server action request object
        """
        return {'image':
                self._remove_empty_values(self._get_attribute_dictionary())}

    def _obj_to_xml(self):
        """
        @summary: Convert send message object to XML element
        @return: XML element of image server action request object
        """
        element = ET.Element(self.ROOT_TAG)
        e_attrs = self._get_attribute_dictionary()
        return self._set_xml_attrs(element, e_attrs)

    def _obj_to_json(self):
        ret = self._obj_to_dict()
        return json.dumps(ret)

    def _get_attribute_dictionary(self):
        attrs = dict()
        attrs["name"] = self.name
        attrs["serverId"] = self.server_id
        return attrs
