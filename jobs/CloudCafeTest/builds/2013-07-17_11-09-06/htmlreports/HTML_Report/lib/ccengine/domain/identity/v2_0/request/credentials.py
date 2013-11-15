import json
from xml.etree import ElementTree
from ccengine.domain.identity.v2_0.base_identity_domain \
    import BaseIdentityDomain
from ccengine.common.constants.identity import V2_0Constants


class PasswordCredentials(BaseIdentityDomain):

    ROOT_TAG = 'passwordCredentials'

    def __init__(self, username=None, password=None):

        super(PasswordCredentials, self).__init__()
        self.username = username
        self.password = password

    def _obj_to_json(self):
        ret = {self.ROOT_TAG: self._obj_to_dict()}
        return json.dumps(ret)

    def _obj_to_dict(self):
        ret = {}
        if self.username is not None:
            ret['username'] = self.username
        if self.password is not None:
            ret['password'] = self.password
        return ret

    def _obj_to_xml(self):
        element = self._obj_to_xml_ele()
        element.set('xmlns', V2_0Constants.XML_NS)
        element.set('xmlns:xsi', V2_0Constants.XML_NS_XSI)
        return ElementTree.tostring(element)

    def _obj_to_xml_ele(self):
        element = ElementTree.Element(self.ROOT_TAG)
        if self.username is not None:
            element.set('username', self.username)
        if self.password is not None:
            element.set('password', self.password)
        return element


class ApiKeyCredentials(BaseIdentityDomain):

    ROOT_TAG = 'apiKeyCredentials'
    JSON_ROOT_TAG = 'RAX-KSKEY:{0}'.format(ROOT_TAG)

    def __init__(self, username=None, apiKey=None):
        super(ApiKeyCredentials, self).__init__()
        self.username = username
        self.apiKey = apiKey

    def _obj_to_json(self):
        ret = {self.JSON_ROOT_TAG: self._obj_to_dict()}
        return json.dumps(ret)

    def _obj_to_dict(self):
        ret = {}
        if self.username is not None:
            ret['username'] = self.username
        if self.apiKey is not None:
            ret['apiKey'] = self.apiKey
        return ret

    def _obj_to_xml(self):
        element = self._obj_to_xml_ele()
        element.set('xmlns', V2_0Constants.XML_NS_RAX_KSKEY)
        return ElementTree.tostring(element)

    def _obj_to_xml_ele(self):
        element = ElementTree.Element(self.ROOT_TAG)
        if self.username is not None:
            element.set('username', self.username)
        if self.apiKey is not None:
            element.set('apiKey', self.apiKey)
        return element
