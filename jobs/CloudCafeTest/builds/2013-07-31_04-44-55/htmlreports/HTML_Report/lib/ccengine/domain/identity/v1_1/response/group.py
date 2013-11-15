from xml.etree import ElementTree
import json
from ccengine.domain.base_domain \
    import BaseMarshallingDomain, BaseMarshallingDomainList
from ccengine.common.constants.identity import V1_1Constants


class Groups(BaseMarshallingDomainList):

    ROOT_TAG = 'groups'

    def __init__(self, groups=None):
        super(Groups, self).__init__()
        self.extend(groups)

    @classmethod
    def _json_to_obj(cls, serialized_str):
        ret = json.loads(serialized_str)
        return cls._list_to_obj(ret.get(cls.ROOT_TAG).get('values'))

    @classmethod
    def _list_to_obj(cls, list_):
        kwargs = {cls.ROOT_TAG: [Group(**group) for group in list_]}
        return Groups(**kwargs)

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        element = ElementTree.fromstring(serialized_str)
        cls._remove_namespace(element, V1_1Constants.XML_NS)
        if element.tag != cls.ROOT_TAG:
            return None
        return cls._xml_ele_to_obj(element)

    @classmethod
    def _xml_ele_to_obj(cls, xml_ele):
        xml_groups = xml_ele.findall(Group.ROOT_TAG)
        groups = [Group._xml_ele_to_obj(xml_group) for xml_group in xml_groups]
        kwargs = {cls.ROOT_TAG: groups}
        return Groups(**kwargs)


class Group(BaseMarshallingDomain):

    ROOT_TAG = 'group'

    def __init__(self, id=None, description=None):
        super(Group, self).__init__()
        self.id = id
        self.description = description

    @classmethod
    def _json_to_obj(cls, serialized_str):
        ret = json.loads(serialized_str)
        return Group(**ret.get(cls.ROOT_TAG))

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        element = ElementTree.fromstring(serialized_str)
        cls._remove_namespace(element, V1_1Constants.XML_NS)
        if element.tag != cls.ROOT_TAG:
            return None
        return cls._xml_ele_to_obj(element)

    @classmethod
    def _xml_ele_to_obj(cls, xml_ele):
        kwargs = {'id': xml_ele.get('id')}
        description = xml_ele.find('description')
        if description is not None:
            kwargs['description'] = description.text
        return Group(**kwargs)
