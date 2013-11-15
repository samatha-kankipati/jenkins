import json
from xml.etree import ElementTree

from ccengine.common.constants.identity import V2_0Constants as v2_0_constants
from ccengine.domain.base_domain \
    import BaseMarshallingDomain, BaseMarshallingDomainList


class EndpointTemplates(BaseMarshallingDomainList):

    ROOT_TAG = 'OS-KSCATALOG:endpointTemplate'

    def __init__(self, base_urls=None):
        super(EndpointTemplates, self).__init__()
        self.extend(base_urls)

    @classmethod
    def _json_to_obj(cls, serialized_str):
        ret = json.loads(serialized_str)
        return cls._list_to_obj(ret.get(cls.ROOT_TAG))

    @classmethod
    def _list_to_obj(cls, list_):
        kwargs = {cls.ROOT_TAG: [EndpointTemplate(**group) for group in list_]}
        return EndpointTemplates(**kwargs)

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        element = ElementTree.fromstring(serialized_str)
        cls._remove_namespace(element, v2_0_constants.XML_NS)
        if element.tag != cls.ROOT_TAG:
            return None
        return cls._xml_ele_to_obj(element)

    @classmethod
    def _xml_ele_to_obj(cls, xml_ele):
        xml_base_urls = xml_ele.findall(EndpointTemplate.ROOT_TAG)
        base_urls = [EndpointTemplate._xml_ele_to_obj(xml_base_url)
                     for xml_base_url in xml_base_urls]
        kwargs = {cls.ROOT_TAG: base_urls}
        return EndpointTemplates(**kwargs)


class EndpointTemplate(BaseMarshallingDomain):

    ROOT_TAG = 'OS-KSCATALOG:endpointTemplate'
    endpoint_global = 'global'
    global_enabled = 'false'

    def __init__(self, id=None, name=None, type=None, region=None,
                 publicURL=None, internalURL=None,
                 adminURL=None, enabled=None):
        super(EndpointTemplate, self).__init__()
        self.id = id
        self.name = name
        self.type = type
        self.region = region
        self.public_url = publicURL
        self.internal_url = internalURL
        self.admin_url = adminURL
        self.enabled = enabled

    @classmethod
    def _json_to_obj(cls, serialized_str):
        ret = json.loads(serialized_str)
        retValue = ret.get(cls.ROOT_TAG)
        if retValue[cls.endpoint_global] is not None:
            cls.global_enabled = retValue.get(cls.endpoint_global)
            del retValue[cls.endpoint_global]
        ret[cls.ROOT_TAG] = retValue
        return EndpointTemplate(**ret.get(cls.ROOT_TAG))

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        element = ElementTree.fromstring(serialized_str)
        cls._remove_namespace(element, v2_0_constants.XML_NS)
        if element.tag != cls.ROOT_TAG:
            return None
        return cls._xml_ele_to_obj(element)

    @classmethod
    def _xml_ele_to_obj(cls, xml_ele):
        kwargs = {'id': xml_ele.get('id'),
                  'name': xml_ele.get('name'),
                  'type': xml_ele.get('type'),
                  'region': xml_ele.get('region'),
                  'adminURL': xml_ele.get('admin_url'),
                  'publicURL': xml_ele.get('public_url'),
                  'internalURL': xml_ele.get('internal_url')
                  }

        if xml_ele.get('enabled') is not None:
            kwargs['enabled'] = json.loads(xml_ele.get('enabled').lower())
        if xml_ele.get('global') is not None:
            kwargs['global'] = json.loads(xml_ele.get('global').lower())
        return EndpointTemplate(**kwargs)
