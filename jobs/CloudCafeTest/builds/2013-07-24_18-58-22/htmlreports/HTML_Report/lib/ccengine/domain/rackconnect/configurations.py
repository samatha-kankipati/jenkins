from ccengine.domain.base_domain import BaseMarshallingDomain
import json
import xml.etree.ElementTree as ET
from ccengine.common.tools.equality_tools import EqualityTools
from ccengine.common.constants.compute_constants import Constants


class Configurations(BaseMarshallingDomain):

    def __init__(self, **kwargs):
        '''An object that represents configurations.

        Keyword arguments:
        '''
        super(Configurations, self).__init__(**kwargs)
        raise NotImplemented

    @classmethod
    def _json_to_obj(cls, serialized_str):
        '''Returns an instance of a configurations, json serialized_str
        passed in.'''
        raise NotImplemented

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        '''Returns an instance of a configurations, xml serialized_str
        passed in.'''
        raise NotImplemented
