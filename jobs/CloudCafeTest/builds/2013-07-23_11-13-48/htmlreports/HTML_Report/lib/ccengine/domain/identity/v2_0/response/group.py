import json
from xml.etree import ElementTree
from ccengine.domain.identity.v2_0.base_identity_domain \
    import BaseIdentityDomain, BaseIdentityDomainList


class Groups(BaseIdentityDomainList):

    ROOT_TAG = 'groups'
    JSON_ROOT_TAG = 'RAX-KSGRP:{0}'.format(ROOT_TAG)

    def __init__(self, groups=None):
        '''An object that represents an groups response object.
        '''
        super(Groups, self).__init__()
        self.extend(groups)

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        return cls._list_to_obj(json_dict.get(cls.JSON_ROOT_TAG))

    @classmethod
    def _list_to_obj(cls, list_):
        ret = {cls.ROOT_TAG: [Group(**group) for group in list_]}
        return Groups(**ret)

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        element = ElementTree.fromstring(serialized_str)
        cls._remove_identity_xml_namespaces(element)
        if element.tag != cls.ROOT_TAG:
            return None
        return cls._xml_list_to_obj(element.findall(Group.ROOT_TAG))

    @classmethod
    def _xml_list_to_obj(cls, xml_list):
        kwargs = {cls.ROOT_TAG: [Group._xml_ele_to_obj(ele)
                                 for ele in xml_list]}
        return Groups(**kwargs)


class Group(BaseIdentityDomain):

    ROOT_TAG = 'group'
    JSON_ROOT_TAG = 'RAX-KSGRP:{0}'.format(ROOT_TAG)

    def __init__(self, id=None, name=None, description=None):
        '''An object that represents an groups response object.
        '''
        super(Group, self).__init__()
        self.id = id
        self.name = name
        self.description = description

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        return Group(**json_dict.get(cls.JSON_ROOT_TAG))

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        element = ElementTree.fromstring(serialized_str)
        cls._remove_identity_xml_namespaces(element)
        if element.tag != cls.ROOT_TAG:
            return None
        return cls._xml_ele_to_obj(element)

    @classmethod
    def _xml_ele_to_obj(cls, xml_ele):
        kwargs = {'name': xml_ele.get('name')}
        description = xml_ele.find('description')
        if description is not None:
            kwargs['description'] = description.text
        try:
            kwargs['id'] = int(xml_ele.get('id'))
        except (ValueError, TypeError):
            kwargs['id'] = xml_ele.get('id')
        return Group(**kwargs)
