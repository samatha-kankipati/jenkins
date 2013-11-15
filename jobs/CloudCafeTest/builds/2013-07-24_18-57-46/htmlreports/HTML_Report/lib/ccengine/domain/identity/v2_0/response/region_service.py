import json
from xml.etree import ElementTree
from ccengine.domain.identity.v2_0.base_identity_domain \
    import BaseIdentityDomain, BaseIdentityDomainList


class DefaultRegionServices(BaseIdentityDomainList):

    ROOT_TAG = 'defaultRegionServices'
    JSON_ROOT_TAG = 'RAX-AUTH:{0}'.format(ROOT_TAG)

    def __init__(self, defaultRegionServices=None):
        '''An object that represents an imperson response object.
        '''
        super(DefaultRegionServices, self).__init__()
        self.extend(defaultRegionServices)

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        json_dict[cls.ROOT_TAG] = json_dict.get(cls.JSON_ROOT_TAG)
        del json_dict[cls.JSON_ROOT_TAG]
        return DefaultRegionServices(**json_dict)

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        element = ElementTree.fromstring(serialized_str)
        cls._remove_identity_xml_namespaces(element)
        if element.tag != cls.ROOT_TAG:
            return None
        return cls._xml_list_to_obj(element)

    @classmethod
    def _xml_list_to_obj(cls, xml_list):
        kwargs = {cls.ROOT_TAG: [ele.text for ele in xml_list]}
        return DefaultRegionServices(**kwargs)

