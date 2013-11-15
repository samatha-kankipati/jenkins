from xml.etree import ElementTree
import json
from ccengine.domain.base_domain \
    import BaseMarshallingDomain, BaseMarshallingDomainList
from ccengine.common.constants.identity import V1_1Constants


class BaseURLs(BaseMarshallingDomainList):

    ROOT_TAG = 'baseURLs'

    def __init__(self, baseURLs=None):
        super(BaseURLs, self).__init__()
        self.extend(baseURLs)

    @classmethod
    def _json_to_obj(cls, serialized_str):
        ret = json.loads(serialized_str)
        return cls._list_to_obj(ret.get(cls.ROOT_TAG))

    @classmethod
    def _list_to_obj(cls, list_):
        kwargs = {cls.ROOT_TAG: [BaseURL(**group) for group in list_]}
        return BaseURLs(**kwargs)

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        element = ElementTree.fromstring(serialized_str)
        cls._remove_namespace(element, V1_1Constants.XML_NS)
        if element.tag != cls.ROOT_TAG:
            return None
        return cls._xml_ele_to_obj(element)

    @classmethod
    def _xml_ele_to_obj(cls, xml_ele):
        xml_base_urls = xml_ele.findall(BaseURL.ROOT_TAG)
        base_urls = [BaseURL._xml_ele_to_obj(xml_base_url)
                     for xml_base_url in xml_base_urls]
        kwargs = {cls.ROOT_TAG: base_urls}
        return BaseURLs(**kwargs)


class BaseURL(BaseMarshallingDomain):

    ROOT_TAG = 'baseURL'

    def __init__(self, id=None, userType=None, region=None, default=None,
                 serviceName=None, publicURL=None, internalURL=None,
                 enabled=None):
        super(BaseURL, self).__init__()
        self.id = id
        self.userType = userType
        self.region = region
        self.default = default
        self.serviceName = serviceName
        self.publicURL = publicURL
        self.internalURL = internalURL
        self.enabled = enabled

    @classmethod
    def _json_to_obj(cls, serialized_str):
        ret = json.loads(serialized_str)
        return BaseURL(**ret.get(cls.ROOT_TAG))

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        element = ElementTree.fromstring(serialized_str)
        cls._remove_namespace(element, V1_1Constants.XML_NS)
        if element.tag != cls.ROOT_TAG:
            return None
        return cls._xml_ele_to_obj(element)

    @classmethod
    def _xml_ele_to_obj(cls, xml_ele):
        kwargs = {'userType': xml_ele.get('userType'),
                  'region': xml_ele.get('region'),
                  'serviceName': xml_ele.get('serviceName'),
                  'publicURL': xml_ele.get('publicURL'),
                  'internalURL': xml_ele.get('internalURL')}
        try:
            kwargs['id'] = int(xml_ele.get('id'))
        except (ValueError, TypeError):
            kwargs['id'] = xml_ele.get('id')
        if xml_ele.get('default') is not None:
            kwargs['default'] = json.loads(xml_ele.get('default').lower())
        if xml_ele.get('enabled') is not None:
            kwargs['enabled'] = json.loads(xml_ele.get('enabled').lower())
        return BaseURL(**kwargs)


class BaseURLRefs(BaseMarshallingDomainList):

    ROOT_TAG = 'baseURLRefs'

    def __init__(self, baseURLRefs=None):
        super(BaseURLRefs, self).__init__()
        self.extend(baseURLRefs)

    @classmethod
    def _json_to_obj(cls, serialized_str):
        ret = json.loads(serialized_str)
        return cls._list_to_obj(ret.get(cls.ROOT_TAG))

    @classmethod
    def _list_to_obj(cls, list_):
        #This is to account for when getting userId/enabled
        if BaseURLRef.ROOT_TAG in list_:
            list_ = list_.get(BaseURLRef.ROOT_TAG)
        kwargs = {cls.ROOT_TAG: [BaseURLRef(**ref) for ref in list_]}
        return BaseURLRefs(**kwargs)

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        element = ElementTree.fromstring(serialized_str)
        cls._remove_namespace(element, V1_1Constants.XML_NS)
        if element.tag != cls.ROOT_TAG:
            return None
        return cls._xml_ele_to_obj(element)

    @classmethod
    def _xml_ele_to_obj(cls, xml_ele):
        xml_base_url_refs = xml_ele.findall(BaseURLRef.ROOT_TAG)
        base_url_refs = [BaseURLRef._xml_ele_to_obj(xml_base_url_ref)
                         for xml_base_url_ref in xml_base_url_refs]
        kwargs = {cls.ROOT_TAG: base_url_refs}
        return BaseURLRefs(**kwargs)


class BaseURLRef(BaseMarshallingDomain):

    ROOT_TAG = 'baseURLRef'

    def __init__(self, id=None, href=None, v1Default=None):
        super(BaseURLRef, self).__init__()
        self.id = id
        self.href = href
        self.v1Default = v1Default

    @classmethod
    def _json_to_obj(cls, serialized_str):
        ret = json.loads(serialized_str)
        return BaseURLRef(**ret.get(cls.ROOT_TAG))

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        element = ElementTree.fromstring(serialized_str)
        cls._remove_namespace(element, V1_1Constants.XML_NS)
        if element.tag != cls.ROOT_TAG:
            return None
        return cls._xml_ele_to_obj(element)

    @classmethod
    def _xml_ele_to_obj(cls, xml_ele):
        kwargs = {'href': xml_ele.get('href')}
        if xml_ele.get('v1Default') is not None:
            kwargs['v1Default'] = json.loads(xml_ele.get('v1Default').lower())
        try:
            kwargs['id'] = int(xml_ele.get('id'))
        except (ValueError, TypeError):
            kwargs['id'] = xml_ele.get('id')
        return BaseURLRef(**kwargs)
