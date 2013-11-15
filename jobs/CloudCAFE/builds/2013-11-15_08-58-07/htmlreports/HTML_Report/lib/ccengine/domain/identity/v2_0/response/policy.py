import json
from xml.etree import ElementTree
from ccengine.domain.identity.v2_0.base_identity_domain \
    import BaseIdentityDomain, BaseIdentityDomainList


class Policies(BaseIdentityDomainList):

    ROOT_TAG = 'policies'
    JSON_ROOT_TAG = 'RAX-AUTH:{0}'.format(ROOT_TAG)

    def __init__(self, policies=None):
        super(Policies, self).__init__()
        self.extend(policies)

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        return cls._list_to_obj(json_dict.get(cls.JSON_ROOT_TAG))

    @classmethod
    def _list_to_obj(cls, list_):
        if Policy.JSON_ROOT_TAG in list_:
            list_ = list_[Policy.JSON_ROOT_TAG]
        ret = {cls.ROOT_TAG: [Policy._dict_to_obj(policy)
                              for policy in list_]}
        return Policies(**ret)

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        element = ElementTree.fromstring(serialized_str)
        cls._remove_identity_xml_namespaces(element)
        if element.tag != cls.ROOT_TAG:
            return None
        return cls._xml_list_to_obj(element.findall(Policy.ROOT_TAG))

    @classmethod
    def _xml_list_to_obj(cls, xml_list):
        kwargs = {cls.ROOT_TAG: [Policy._xml_ele_to_obj(ele)
                                 for ele in xml_list]}
        return Policies(**kwargs)


class Policy(BaseIdentityDomain):

    ROOT_TAG = 'policy'
    JSON_ROOT_TAG = 'RAX-AUTH:{0}'.format(ROOT_TAG)

    def __init__(self, id=None, enabled=None, description=None, blob=None,
                 type=None, name=None, global_=None):
        super(Policy, self).__init__()
        self.id = id
        self.enabled = enabled
        self.description = description
        self.blob = blob
        self.global_ = global_
        self.type = type
        self.name = name

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        return cls._dict_to_obj(json_dict.get(cls.JSON_ROOT_TAG))

    @classmethod
    def _dict_to_obj(cls, dic):
        if 'global' in dic:
            dic['global_'] = dic['global']
            del dic['global']
        return Policy(**dic)

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
                  'description': xml_ele.get('description'),
                  'blob': xml_ele.get('blob'),
                  'type': xml_ele.get('type')}
        try:
            kwargs['id'] = int(xml_ele.get('id'))
        except (ValueError, TypeError):
            kwargs['id'] = xml_ele.get('id')
        if xml_ele.get('enabled') is not None:
            kwargs['enabled'] = json.loads(xml_ele.get('enabled').lower())
        if xml_ele.get('global') is not None:
            kwargs['global_'] = json.loads(xml_ele.get('global').lower())
        return Policy(**kwargs)
