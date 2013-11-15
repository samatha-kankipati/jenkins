from ccengine.domain.base_domain import BaseMarshallingDomain
import json
import xml.etree.ElementTree as ET
from ccengine.common.tools.equality_tools import EqualityTools
from ccengine.common.constants.compute_constants import Constants


class AutoStatuses(BaseMarshallingDomain):

    def __init__(self, automation_status, cloud_server_id, api_server_id,
                 cloud_version):
        '''An object that represents configurations.

        Keyword arguments:
        '''
        super(AutoStatuses, self).__init__()
        self.automation_status = automation_status
        self.cloud_server_id = cloud_server_id
        self.api_server_id = api_server_id
        self.cloud_version = cloud_version

    @classmethod
    def _json_to_obj(cls, serialized_str):
        '''Returns an instance of a configurations, json serialized_str
        passed in.'''
        json_dict = json.loads(serialized_str)
        configurations = []
        for conf_dict in json_dict:
            conf = cls._dict_to_obj(conf_dict)
            configurations.append(conf)
        return configurations

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        '''Returns an instance of a configurations, xml serialized_str
        passed in.'''
        raise NotImplemented
    
    @classmethod
    def _dict_to_obj(cls, conf_dict):
        '''Helper method to turn dictionary into Server instance.'''
        config = AutoStatuses(
            automation_status=conf_dict.get('automation_status'),
            cloud_server_id=conf_dict.get('cloud_server_id'),
            api_server_id=conf_dict.get('api_server_id'),
            cloud_version=conf_dict.get('cloud_version'))
        return config

