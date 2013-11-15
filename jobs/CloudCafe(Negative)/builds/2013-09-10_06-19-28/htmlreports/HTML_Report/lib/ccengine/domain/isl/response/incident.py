from ccengine.domain.base_domain import BaseDomain
from ccengine.domain.base_domain import BaseMarshallingDomain
import json
import xml.etree.ElementTree as ET
from ccengine.common.tools.equality_tools import EqualityTools
from ccengine.common.constants.isl_constants import Constants
import re

class Incident(BaseMarshallingDomain):

    ROOT_TAG = 'incidents'

    def __init__(self, **kwargs):
        super(Incident, self).__init__(**kwargs)
        for keys, values in kwargs.items():
            setattr(self, keys, values)

    @classmethod
    def _json_to_obj(cls, serialized_str):
        '''Returns an instance of an Incident based on the json serialized_str
        passed in.'''
        ret = None
        json_dict = json.loads(serialized_str)
        if 'incident' in json_dict.keys():
            ret = cls._dict_to_obj(json_dict['incident'])
        if 'incidents' in json_dict.keys():
            ret = []
            for incident in json_dict['incidents']['incident']:
                s = cls._dict_to_obj(incident)
                ret.append(s)
        return ret

    @classmethod
    def _dict_to_obj(cls, incident_dict):
        '''Helper method to turn dictionary into Server instance.'''
        for key, value in incident_dict.items():
            new_key = key.replace("-", "_")
            del incident_dict[key]
            incident_dict[new_key] = value

        incident = Incident(**incident_dict)
        return incident


    @classmethod
    def _xml_to_obj(cls, serialized_str):
        '''Returns an instance of a Incident based on the xml serialized_str
        passed in.'''
        element = ET.fromstring(serialized_str)
        cls._remove_namespace(element, Constants.XML_API_NAMESPACE)
        cls._remove_namespace(element, Constants.XML_API_SCHEMA_NAMESPACE)
        cls._remove_namespace(element, Constants.XML_API_SCHEMA_LOCATION_NAMESPACE)
        cls._remove_namespace(element, Constants.XML_API_ATOM_NAMESPACE)
        if element.tag == 'incident':
            ret = cls._xml_ele_to_obj(element)
        if element.tag == 'incidents':
            ret = []
            for incident in element.findall('incident'):
                s = cls._xml_ele_to_obj(incident)
                ret.append(s)
        return ret

    @classmethod
    def _xml_ele_to_obj(cls, element):
        '''Helper method to turn ElementTree instance to Incident instance.'''
        incident_dict = element.attrib
        if element.find('incident-id') is not None:
            incident_dict['incident_id'] = element.find('incident-id').text
        if element.find('subject') is not None:
            incident_dict['subject'] = element.find('subject').text
        if element.find('incident_status') is not None:
            incident_dict['incident_status'] = element.find('incident-status').text
        if element.find('request-received-at') is not None:
            incident_dict['request_received_at'] = element.find('request-received-at').text
        incident = Incident(**incident_dict)
        return incident

