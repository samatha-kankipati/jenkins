import json
from xml.etree import ElementTree
from ccengine.domain.identity.v2_0.base_identity_domain \
    import BaseIdentityDomain, BaseIdentityDomainList


class ServiceAPIs(BaseIdentityDomainList):

    ROOT_TAG = 'serviceApis'
    JSON_ROOT_TAG = 'RAX-AUTH:{0}'.format(ROOT_TAG)

    def __init__(self, serviceApis=None):
        super(ServiceAPIs, self).__init__()
        self.extend(serviceApis)

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        return cls._list_to_obj(json_dict.get(cls.JSON_ROOT_TAG))

    @classmethod
    def _list_to_obj(cls, list_):
        ret = {cls.ROOT_TAG: [ServiceAPI(**s_api) for s_api in list_]}
        return ServiceAPIs(**ret)

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        element = ElementTree.fromstring(serialized_str)
        cls._remove_identity_xml_namespaces(element)
        if element.tag != cls.ROOT_TAG:
            return None
        return cls._xml_list_to_obj(element.findall(ServiceAPI.ROOT_TAG))

    @classmethod
    def _xml_list_to_obj(cls, xml_list):
        kwargs = {cls.ROOT_TAG: [ServiceAPI._xml_ele_to_obj(ele)
                                 for ele in xml_list]}
        return ServiceAPIs(**kwargs)


class ServiceAPI(BaseIdentityDomain):

    ROOT_TAG = 'serviceApi'
    JSON_ROOT_TAG = 'RAX-AUTH:{0}'.format(ROOT_TAG)

    def __init__(self, type=None, version=None):
        super(ServiceAPI, self).__init__()
        self.type = type
        self.version = version

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        return ServiceAPI(**json_dict.get(cls.JSON_ROOT_TAG))

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        element = ElementTree.fromstring(serialized_str)
        cls._remove_identity_xml_namespaces(element)
        if element.tag != cls.ROOT_TAG:
            return None
        return cls._xml_ele_to_obj(element)

    @classmethod
    def _xml_ele_to_obj(cls, xml_ele):
        kwargs = {'type': xml_ele.get('type'),
                  'version': xml_ele.get('version')}
        return ServiceAPI(**kwargs)
