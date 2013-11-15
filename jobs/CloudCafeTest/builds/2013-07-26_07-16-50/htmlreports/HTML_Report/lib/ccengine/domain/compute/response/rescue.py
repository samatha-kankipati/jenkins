from ccengine.domain.base_domain import BaseMarshallingDomain
import json
import xml.etree.ElementTree as ET
from ccengine.common.constants.compute_constants import Constants


class Rescue(BaseMarshallingDomain):

    def __init__(self, **kwargs):
        '''An object that represents any response returned by Compute API.

        Keyword arguments:
        '''
        for keys, values in kwargs.items():
            setattr(self, keys, values)

    def __repr__(self):
        values = []
        for prop in self.__dict__:
            values.append("%s: %s" % (prop, self.__dict__[prop]))
        return '[' + ', '.join(values) + ']'

    @classmethod
    def _json_to_obj(cls, serialized_str):
        '''Returns an instance of a Compute Base response based on the
        json serialized_str passed in.'''
        response_dict = json.loads(serialized_str)
        response = Rescue(**response_dict)
        return response

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        '''Returns an instance of a Compute Base response based on the xml
         serialized_str passed in.'''
        element = ET.fromstring(serialized_str)
        cls._remove_namespace(element, Constants.XML_API_NAMESPACE)
        cls._remove_namespace(element, Constants.XML_API_ATOM_NAMESPACE)
        response_dict = {}
        if element.tag == 'adminPass':
            response_dict['adminPass'] = element.text

        response = Rescue(**response_dict)
        return response
