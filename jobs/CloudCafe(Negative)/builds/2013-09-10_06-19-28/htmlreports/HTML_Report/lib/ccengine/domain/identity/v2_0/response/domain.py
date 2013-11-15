import json
from xml.etree import ElementTree
from ccengine.domain.identity.v2_0.base_identity_domain \
    import BaseIdentityDomain, BaseIdentityDomainList


class Domains(BaseIdentityDomainList):

    ROOT_TAG = 'domains'
    JSON_ROOT_TAG = 'RAX-AUTH:{0}'.format(ROOT_TAG)

    def __init__(self, domains=None):
        super(Domains, self).__init__()
        self.extend(domains)

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        return cls._list_to_obj(json_dict.get(cls.JSON_ROOT_TAG))

    @classmethod
    def _list_to_obj(cls, list_):
        ret = {cls.ROOT_TAG: [Domain(**domain) for domain in list_]}
        return Domains(**ret)

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        element = ElementTree.fromstring(serialized_str)
        cls._remove_identity_xml_namespaces(element)
        if element.tag != cls.ROOT_TAG:
            return None
        return cls._xml_list_to_obj(element.findall(Domain.ROOT_TAG))

    @classmethod
    def _xml_list_to_obj(cls, xml_list):
        kwargs = {cls.ROOT_TAG: [Domain._xml_ele_to_obj(ele)
                                for ele in xml_list]}
        return Domains(**kwargs)


class Domain(BaseIdentityDomain):

    ROOT_TAG = 'domain'
    JSON_ROOT_TAG = 'RAX-AUTH:{0}'.format(ROOT_TAG)

    def __init__(self, id=None, enabled=None, description=None, name=None):
        '''An object that represents an imperson response object.
        '''
        super(Domain, self).__init__()
        self.id = id
        self.enabled = enabled
        self.description = description
        self.name = name

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        return Domain(**json_dict.get(cls.JSON_ROOT_TAG))

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        element = ElementTree.fromstring(serialized_str)
        cls._remove_identity_xml_namespaces(element)
        if element.tag != cls.ROOT_TAG:
            return None
        return cls._xml_ele_to_obj(element)

    @classmethod
    def _xml_ele_to_obj(cls, xml_ele):
        #not converting id as an int because json returns it as a string
        kwargs = {'name': xml_ele.get('name'), 'id': xml_ele.get('id')}
        description = xml_ele.find('description')
        if description is not None:
            kwargs['description'] = description.text
        if xml_ele.get('enabled') is not None:
            kwargs['enabled'] = json.loads(xml_ele.get('enabled').lower())
        return Domain(**kwargs)
