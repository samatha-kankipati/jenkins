import json
from xml.etree import ElementTree
from ccengine.domain.identity.v2_0.base_identity_domain \
    import BaseIdentityDomain, BaseIdentityDomainList
from ccengine.common.constants.identity import V2_0Constants


class Capabilities(BaseIdentityDomainList):

    ROOT_TAG = 'capabilities'
    JSON_ROOT_TAG = 'RAX-AUTH:{0}'.format(ROOT_TAG)

    def __init__(self, capabilities=None):
        super(Capabilities, self).__init__()
        self.extend(capabilities)

    def _obj_to_json(self):
        ret = {self.JSON_ROOT_TAG: [cap._dict_to_json()
                                    for cap in self]}
        return json.dumps(ret)

    def _obj_to_xml(self):
        element = ElementTree.Element(self.ROOT_TAG)
        element.set('xmlns', V2_0Constants.XML_NS_RAX_AUTH)
        element.set('xmlns:identity', V2_0Constants.XML_NS)
        for capability in self:
            element.append(capability._obj_to_xml_ele())
        return ElementTree.tostring(element)


class Capability(BaseIdentityDomain):

    ROOT_TAG = 'capability'
    JSON_ROOT_TAG = 'RAX-AUTH:{0}'.format(ROOT_TAG)

    def __init__(self, id=None, name=None, action=None, url=None):
        super(Capability, self).__init__()
        self.id = id
        self.name = name
        self.action = action
        self.url = url

    def _dict_to_json(self):
        ret = {}
        if self.id is not None:
            ret['id'] = self.id
        if self.name is not None:
            ret['name'] = self.name
        if self.action is not None:
            ret['action'] = self.action
        if self.url is not None:
            ret['url'] = self.url
        return ret

    def _obj_to_xml(self):
        element = self._obj_to_xml_ele()
        element.set('xmlns', V2_0Constants.XML_NS_RAX_AUTH)
        element.set('xmlns:identity', V2_0Constants.XML_NS)
        return ElementTree.tostring(element)

    def _obj_to_xml_ele(self):
        element = ElementTree.Element(self.ROOT_TAG)
        if self.id is not None:
            element.set('id', str(self.id))
        if self.name is not None:
            element.set('name', str(self.name))
        if self.action is not None:
            element.set('action', str(self.action))
        if self.url is not None:
            element.set('url', str(self.url))
        return element

