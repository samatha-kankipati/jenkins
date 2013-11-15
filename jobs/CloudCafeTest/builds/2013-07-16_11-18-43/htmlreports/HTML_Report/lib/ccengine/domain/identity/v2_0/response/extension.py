from xml.etree import ElementTree
import json
from ccengine.domain.identity.v2_0.base_identity_domain \
    import BaseIdentityDomain, BaseIdentityDomainList


class Extensions(BaseIdentityDomainList):

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
        cls._remove_identity_xml_namespaces(element)
        if element.tag != cls.ROOT_TAG:
            return None
        return cls._xml_list_to_obj(element.findall(Extension.ROOT_TAG))

    @classmethod
    def _xml_list_to_obj(cls, xml_list):
        kwargs = {cls.ROOT_TAG: [Extension._xml_ele_to_obj(ele)
                                 for ele in xml_list]}
        return Extensions(**kwargs)


class Extension(BaseIdentityDomain):

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
    def _json_to_obj(cls, serialized_str):
        ret = json.loads(serialized_str)
        return cls._dict_to_obj(ret.get(cls.ROOT_TAG))

    @classmethod
    def _dict_to_obj(cls, dic):
        if Links.ROOT_TAG in dic:
            dic[Links.ROOT_TAG] = Links._list_to_obj(dic.get(Links.ROOT_TAG))
        return Extension(**dic)

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        element = ElementTree.fromstring(serialized_str)
        cls._remove_identity_xml_namespaces(element)
        if element.tag != cls.ROOT_TAG:
            return None
        return cls._xml_ele_to_obj(element)

    @classmethod
    def _xml_ele_to_obj(cls, xml_ele):
        kwargs = {'name': xml_ele.get('name'),
                  'namespace': xml_ele.get('namespace'),
                  'alias': xml_ele.get('alias'),
                  'updated': xml_ele.get('updated')}
        description = xml_ele.find('description')
        if description is not None:
            kwargs['description'] = description.text
        links = xml_ele.findall('link')
        kwargs['links'] = Links._xml_list_to_obj(links)
        return Extension(**kwargs)


class Links(BaseIdentityDomainList):

    ROOT_TAG = 'links'

    def __init__(self, links=None):
        super(Links, self).__init__()
        self.extend(links)

    @classmethod
    def _list_to_obj(cls, list_):
        kwargs = {cls.ROOT_TAG: [Link(**link) for link in list_]}
        return Links(**kwargs)

    @classmethod
    def _xml_list_to_obj(cls, xml_list):
        kwargs = {cls.ROOT_TAG: [Link._xml_ele_to_obj(link)
                                 for link in xml_list]}
        return Links(**kwargs)


class Link(BaseIdentityDomain):

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