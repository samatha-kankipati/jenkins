from xml.etree import ElementTree
import json
from ccengine.domain.base_domain import BaseMarshallingDomain, \
    BaseMarshallingDomainList
from ccengine.common.constants.identity import V1_1Constants


class Extensions(BaseMarshallingDomainList):

    ROOT_TAG = 'extensions'

    def __init__(self, extensions=None):
        super(Extensions, self).__init__()
        self.extend(extensions)

    @classmethod
    def _json_to_obj(cls, serialized_str):
        ret = json.loads(serialized_str)
        return cls._list_to_obj(ret.get(cls.ROOT_TAG))

    @classmethod
    def _list_to_obj(cls, list_):
        kwargs = {cls.ROOT_TAG: [Extension._dict_to_obj(extension)
                                 for extension in list_]}
        return Extensions(**kwargs)

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        element = ElementTree.fromstring(serialized_str)
        cls._remove_namespace(element, V1_1Constants.XML_NS_OPENSTACK)
        if element.tag != cls.ROOT_TAG:
            return None
        return cls._xml_ele_to_obj(element)

    @classmethod
    def _xml_ele_to_obj(cls, xml_ele):
        xml_extensions = xml_ele.findall('extension')
        extensions = [Extensions._xml_ele_to_obj(xml_extension)
                      for xml_extension in xml_extensions]
        kwargs = {cls.ROOT_TAG: extensions}
        return Extensions(**kwargs)


class Extension(BaseMarshallingDomain):

    ROOT_TAG = 'extension'

    def __init__(self, name=None, namespace=None, alias=None, updated=None,
                 description=None, links=None):
        super(Extension, self).__init__()
        self.name = name
        self.namespace = namespace
        self.alias = alias
        self.updated = updated
        self.description = description
        self.links = links

    @classmethod
    def _dict_to_obj(cls, dic):
        if Links.ROOT_TAG in dic:
            dic[Links.ROOT_TAG] = Links._list_to_obj(dic.get(Links.ROOT_TAG))
        return Extension(**dic)

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        element = ElementTree.fromstring(serialized_str)
        cls._remove_namespace(element, V1_1Constants.XML_NS)
        if element.tag != cls.ROOT_TAG:
            return None
        return cls._xml_ele_to_obj(element)

    @classmethod
    def _xml_ele_to_obj(cls, xml_ele):
        kwargs = {'name': xml_ele.get('name'),
                  'namespace': xml_ele.get('namespace'),
                  'alias': xml_ele.get('alias'),
                  'updated': xml_ele.get('updated'),
                  'description': xml_ele.get('description')}
        links = xml_ele.findall('atom:link')
        kwargs['links'] = Links._xml_ele_to_obj(links)
        return Extension(**kwargs)


class Links(BaseMarshallingDomainList):

    ROOT_TAG = 'links'

    def __init__(self, links=None):
        super(Links, self).__init__()
        self.extend(links)

    @classmethod
    def _list_to_obj(cls, list_):
        kwargs = {cls.ROOT_TAG: [Link(**link) for link in list_]}
        return Links(**kwargs)

    @classmethod
    def _xml_ele_to_obj(cls, list_):
        links = [Link._xml_ele_to_obj(xml_link) for xml_link in list_]
        kwargs = {cls.ROOT_TAG: links}
        return Links(**kwargs)


class Link(BaseMarshallingDomain):

    ROOT_TAG = 'link'

    def __init__(self, rel=None, type=None, href=None):
        super(Link, self).__init__()
        self.rel = rel
        self.type = type
        self.href = href

    @classmethod
    def _xml_ele_to_obj(cls, xml_ele):
        kwargs = {'rel': xml_ele.get('rel'), 'type': xml_ele.get('type'),
                  'href': xml_ele.get('href')}
        return Link(**kwargs)
