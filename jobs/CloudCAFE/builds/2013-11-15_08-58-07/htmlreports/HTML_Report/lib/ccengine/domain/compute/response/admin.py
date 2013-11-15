from ccengine.domain.base_domain import BaseMarshallingDomain
import xml.etree.ElementTree as ET
import json
from ccengine.common.constants.compute_constants import Constants
from ccengine.domain.compute.metadata import Metadata


class Hosts(BaseMarshallingDomain):
    """
    @summary: Represents Host domain object
    """
    ROOT_TAG = 'hosts'

    def __init__(self, str_hosts):
        if str_hosts is not None:
            for key, value in str_hosts.items():
                setattr(self, key, value)

    @classmethod
    def _str_to_dict(cls, str_xenmeta):
        '''Returns dict of all xenstore metadata
        passed in.'''
    
    
    @classmethod
    def _dict_to_obj(cls, dict_hosts):
        '''Helper method to turn dictionary into Xenmeta instance.'''
        lst_objhost = []
        for dict_host in dict_hosts:
            lst_objhost.append(Hosts(dict_host))
            
        return lst_objhost
    
    @classmethod
    def _json_to_obj(cls, serialized_str):
        '''Returns an instance of a Server based on the json serialized_str
        passed in.'''
        ret = None
        json_dict = json.loads(serialized_str)
        if 'hosts' in json_dict.keys():
            ret = cls._dict_to_obj(json_dict['hosts'])
        if 'host' in json_dict.keys():
            ret = cls._dict_to_obj(json_dict['host'])
        return ret