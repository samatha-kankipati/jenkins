from ccengine.domain.base_domain import BaseMarshallingDomain
import json
import xml.etree.ElementTree as ET
from ccengine.common.tools.equality_tools import EqualityTools
from ccengine.common.constants.compute_constants import Constants


class Launch(BaseMarshallingDomain):

    def __init__(self, **kwargs):
        '''An object that represents a launch.

        Keyword arguments:
        '''
        super(Launch, self).__init__(**kwargs)
        for keys, values in kwargs.items():
            setattr(self, keys, values)

    def __repr__(self):
        values = []
        for prop in self.__dict__:
            values.append("%s: %s" % (prop, self.__dict__[prop]))
        return '[' + ', '.join(values) + ']'

    @classmethod
    def _json_to_obj(cls, serialized_str):
        '''Returns an instance of a Launch based on the json serialized_str
        passed in.'''
        json_dict = json.loads(serialized_str)
        ''' One or more launches will be a list'''
        if 'launches' in json_dict.keys():
            launches = []
            for launch_dict in json_dict['launches']:
                launch = cls._dict_to_obj(launch_dict)
                launches.append(launch)
            return launches

    @classmethod
    def _dict_to_obj(cls, launch_dict):
        '''Helper method to turn dictionary into Launch instance.'''
        launch = Launch(**launch_dict)
        return launch

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        '''Returns an instance of a Launch based on the xml serialized_str
        passed in.'''
        element = ET.fromstring(serialized_str)
        cls._remove_namespace(element, Constants.XML_API_NAMESPACE)
        cls._remove_namespace(element, Constants.XML_API_ATOM_NAMESPACE)

        if element.tag == 'launches':
            launches = []
            for launch in element.findall('launch'):
                launch = cls._xml_ele_to_obj(launch)
                launches.append(launch)
            return launches

    @classmethod
    def _xml_ele_to_obj(cls, element):
        '''Helper method to turn ElementTree instance to Launch instance.'''
        launch_dict = element.attrib
        if 'id' in launch_dict:
            launch_dict['id'] = launch_dict.get('id')
        if 'instance' in launch_dict:
            launch_dict['instance'] = launch_dict.get('instance')
        if 'instance_type_id' in launch_dict:
            launch_dict['instance_type_id'] = launch_dict.get('instance_type_id')
        if 'launched_at' in launch_dict:
            launch_dict['launched_at'] = launch_dict.get('launched_at')
        if 'request_id' in launch_dict:
            launch_dict['swap'] = launch_dict.get('request_id')
        launch = Launch(**launch_dict)
        return launch

    def __eq__(self, other):
        """
        @summary: Overrides the default equals
        @param other: Launch object to compare with
        @type other: Launch
        @return: True if Launch objects are equal, False otherwise
        @rtype: bool
        """
        return EqualityTools.are_objects_equal(self, other)

    def __ne__(self, other):
        """
        @summary: Overrides the default not-equals
        @param other: Launch object to compare with
        @type other: Launch
        @return: True if Launch objects are not equal, False otherwise
        @rtype: bool
        """
        return not self == other

class Delete(BaseMarshallingDomain):

    def __init__(self, **kwargs):
        '''An object that represents a delete.

        Keyword arguments:
        '''
        super(Delete, self).__init__(**kwargs)
        for keys, values in kwargs.items():
            setattr(self, keys, values)

    def __repr__(self):
        values = []
        for prop in self.__dict__:
            values.append("%s: %s" % (prop, self.__dict__[prop]))
        return '[' + ', '.join(values) + ']'

    @classmethod
    def _json_to_obj(cls, serialized_str):
        '''Returns an instance of a Delete based on the json serialized_str
        passed in.'''
        json_dict = json.loads(serialized_str)
        ''' One or more deletes will be a list'''
        if 'deletes' in json_dict.keys():
            deletes = []
            for delete_dict in json_dict['deletes']:
                delete = cls._dict_to_obj(delete_dict)
                deletes.append(delete)
            return deletes

    @classmethod
    def _dict_to_obj(cls, delete_dict):
        '''Helper method to turn dictionary into Delete instance.'''
        delete = Delete(**delete_dict)
        return delete

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        '''Returns an instance of a Delete based on the xml serialized_str
        passed in.'''
        element = ET.fromstring(serialized_str)
        cls._remove_namespace(element, Constants.XML_API_NAMESPACE)
        cls._remove_namespace(element, Constants.XML_API_ATOM_NAMESPACE)

        if element.tag == 'deletes':
            deletes = []
            for delete in element.findall('delete'):
                delete = cls._xml_ele_to_obj(delete)
                deletes.append(delete)
            return deletes

    @classmethod
    def _xml_ele_to_obj(cls, element):
        '''Helper method to turn ElementTree instance to Delete instance.'''
        delete_dict = element.attrib
        if 'deleted_at' in delete_dict:
            delete_dict['deleted_at'] = delete_dict.get('deleted_at')
        if 'id' in delete_dict:
            delete_dict['id'] = delete_dict.get('id')
        if 'instance' in delete_dict:
            delete_dict['instance'] = delete_dict.get('instance')
        if 'launched_at' in delete_dict:
            delete_dict['launched_at'] = delete_dict.get('launched_at')
        if 'raw' in delete_dict:
            delete_dict['raw'] = delete_dict.get('raw')
        delete = Delete(**delete_dict)
        return delete

    def __eq__(self, other):
        """
        @summary: Overrides the default equals
        @param other: Delete object to compare with
        @type other: Delete
        @return: True if Delete objects are equal, False otherwise
        @rtype: bool
        """
        return EqualityTools.are_objects_equal(self, other)

    def __ne__(self, other):
        """
        @summary: Overrides the default not-equals
        @param other: Delete object to compare with
        @type other: Delete
        @return: True if Delete objects are not equal, False otherwise
        @rtype: bool
        """
        return not self == other

class Exist(BaseMarshallingDomain):

    def __init__(self, **kwargs):
        '''An object that represents an exist.

        Keyword arguments:
        '''
        super(Exist, self).__init__(**kwargs)
        for keys, values in kwargs.items():
            setattr(self, keys, values)

    def __repr__(self):
        values = []
        for prop in self.__dict__:
            values.append("%s: %s" % (prop, self.__dict__[prop]))
        return '[' + ', '.join(values) + ']'

    @classmethod
    def _json_to_obj(cls, serialized_str):
        '''Returns an instance of an Exist based on the json serialized_str
        passed in.'''
        json_dict = json.loads(serialized_str)
        ''' One or more exists will be a list'''
        if 'exists' in json_dict.keys():
            exists = []
            for exist_dict in json_dict['exists']:
                exist = cls._dict_to_obj(exist_dict)
                exists.append(exist)
            return exists

    @classmethod
    def _dict_to_obj(cls, exist_dict):
        '''Helper method to turn dictionary into Exist instance.'''
        exist = Exist(**exist_dict)
        return exist

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        '''Returns an instance of a Exist based on the xml serialized_str
        passed in.'''
        element = ET.fromstring(serialized_str)
        cls._remove_namespace(element, Constants.XML_API_NAMESPACE)
        cls._remove_namespace(element, Constants.XML_API_ATOM_NAMESPACE)

        if element.tag == 'exists':
            exists = []
            for exist in element.findall('exist'):
                exist = cls._xml_ele_to_obj(exist)
                exists.append(exist)
            return exists

    @classmethod
    def _xml_ele_to_obj(cls, element):
        '''Helper method to turn ElementTree instance to Exist instance.'''
        exist_dict = element.attrib
        if 'delete' in exist_dict:
            exist_dict['delete'] = exist_dict.get('delete')
        if 'deleted_at' in exist_dict:
            exist_dict['deleted_at'] = exist_dict.get('deleted_at')
        if 'id' in exist_dict:
            exist_dict['id'] = exist_dict.get('id')
        if 'instance' in exist_dict:
            exist_dict['instance'] = exist_dict.get('instance')
        if 'instance_type_id' in exist_dict:
            exist_dict['instance_type_id'] = exist_dict.get('instance_type_id')
        if 'launched_at' in exist_dict:
            exist_dict['launched_at'] = exist_dict.get('launched_at')
        if 'message_id' in exist_dict:
            exist_dict['message_id'] = exist_dict.get('message_id')
        if 'raw' in exist_dict:
            exist_dict['raw'] = exist_dict.get('raw')
        if 'status' in exist_dict:
            exist_dict['status'] = exist_dict.get('status')
        if 'usage' in exist_dict:
            exist_dict['usage'] = exist_dict.get('usage')
        exist = Exist(**exist_dict)
        return exist

    def __eq__(self, other):
        """
        @summary: Overrides the default equals
        @param other: Exist object to compare with
        @type other: Exist
        @return: True if Exist objects are equal, False otherwise
        @rtype: bool
        """
        return EqualityTools.are_objects_equal(self, other)

    def __ne__(self, other):
        """
        @summary: Overrides the default not-equals
        @param other: Exist object to compare with
        @type other: Exist
        @return: True if Exist objects are not equal, False otherwise
        @rtype: bool
        """
        return not self == other
