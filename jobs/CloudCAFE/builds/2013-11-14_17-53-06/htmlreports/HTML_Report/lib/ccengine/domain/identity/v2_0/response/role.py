import json
from xml.etree import ElementTree
from ccengine.domain.identity.v2_0.base_identity_domain \
    import BaseIdentityDomain, BaseIdentityDomainList


class Roles(BaseIdentityDomainList):

    ROOT_TAG = 'roles'

    def __init__(self, roles=None):
        '''An object that represents an users response object.
        Keyword arguments:
        '''
        super(Roles, self).__init__()
        self.extend(roles)

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        return cls._list_to_obj(json_dict.get(cls.ROOT_TAG))

    @classmethod
    def _list_to_obj(cls, list_):
        ret = {cls.ROOT_TAG: [Role._dict_to_obj(role) for role in list_]}
        return Roles(**ret)

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        element = ElementTree.fromstring(serialized_str)
        cls._remove_identity_xml_namespaces(element)
        if element.tag != cls.ROOT_TAG:
            return None
        return cls._xml_list_to_obj(element.findall(Role.ROOT_TAG))

    @classmethod
    def _xml_list_to_obj(cls, xml_list):
        kwargs = {cls.ROOT_TAG: [Role._xml_ele_to_obj(role)
                                 for role in xml_list]}
        return Roles(**kwargs)


class Role(BaseIdentityDomain):

    ROOT_TAG = 'role'

    def __init__(self, id=None, name=None, description=None, serviceId=None,
                 tenantId=None, propagate = None, weight = None):
        super(Role, self).__init__()
        self.id = id
        self.name = name
        self.description = description
        self.serviceId = serviceId
        self.tenantId = tenantId
        self.weight = weight
        self.propagate = propagate

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        return cls._dict_to_obj(json_dict.get(cls.ROOT_TAG))

    @classmethod
    def _dict_to_obj(cls, dic):
        if 'RAX-AUTH:propagate' in dic:
            dic['propagate'] = \
                dic['RAX-AUTH:propagate']
            del dic['RAX-AUTH:propagate']
        if 'RAX-AUTH:weight' in dic:
            dic['weight'] = dic['RAX-AUTH:weight']
            del dic['RAX-AUTH:weight']
        return Role(**dic)

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
                  'serviceId': xml_ele.get('serviceId'),
                  'tenantId': xml_ele.get('tenantId')}
        try:
            kwargs['id'] = int(xml_ele.get('id'))
        except (ValueError, TypeError):
            kwargs['id'] = xml_ele.get('id')
        return Role(**kwargs)
