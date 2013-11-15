import json
from xml.etree import ElementTree
from ccengine.domain.identity.v2_0.base_identity_domain \
    import BaseIdentityDomain
from ccengine.domain.identity.v2_0.request.credentials \
    import PasswordCredentials, ApiKeyCredentials
from ccengine.common.constants.identity import V2_0Constants


class Auth(BaseIdentityDomain):

    ROOT_TAG = 'auth'

    def __init__(self, passwordCredentials=None, apiKeyCredentials=None,
                 tenantName=None, tenantId=None, token=None):
        self.passwordCredentials = passwordCredentials
        self.apiKeyCredentials = apiKeyCredentials
        self.token = token
        self.tenantName = tenantName
        self.tenantId = tenantId

    def _obj_to_json(self):
        ret = {}
        if self.passwordCredentials is not None:
            ret[PasswordCredentials.ROOT_TAG] = \
                self.passwordCredentials._obj_to_dict()
        if self.apiKeyCredentials is not None:
            ret[ApiKeyCredentials.JSON_ROOT_TAG] = \
                self.apiKeyCredentials._obj_to_dict()
        if self.token is not None:
            ret[Token.ROOT_TAG] = self.token._obj_to_dict()
        if self.tenantId is not None:
            ret['tenantId'] = self.tenantId
        if self.tenantName is not None:
            ret['tenantName'] = self.tenantName
        ret = {self.ROOT_TAG: ret}
        return json.dumps(ret)

    def _obj_to_xml(self):
        ele = self._obj_to_xml_ele()
        if self.apiKeyCredentials is not None:
            ele.find(ApiKeyCredentials.ROOT_TAG).set(
                    'xmlns',
                    V2_0Constants.XML_NS_RAX_KSKEY)
        else:
            ele.set('xmlns:xsi', V2_0Constants.XML_NS_XSI)
            ele.set('xmlns', V2_0Constants.XML_NS)
        return ElementTree.tostring(ele)

    def _obj_to_xml_ele(self):
        element = ElementTree.Element(self.ROOT_TAG)
        if self.passwordCredentials is not None:
            element.append(self.passwordCredentials._obj_to_xml_ele())
        if self.apiKeyCredentials is not None:
            element.append(self.apiKeyCredentials._obj_to_xml_ele())
        if self.token is not None:
            element.append(self.token._obj_to_xml_ele())
        if self.tenantName is not None:
            element.set('tenantName', self.tenantName)
        if self.tenantId is not None:
            element.set('tenantId', self.tenantId)
        return element


class Token(BaseIdentityDomain):

    ROOT_TAG = 'token'

    def __init__(self, id=None):
        super(Token, self).__init__()
        self.id = id

    def _obj_to_dict(self):
        ret = {}
        if self.id is not None:
            ret['id'] = self.id
        return ret

    def _obj_to_xml(self):
        return ElementTree.dump(self._obj_to_xml_ele())

    def _obj_to_xml_ele(self):
        element = ElementTree.Element(self.ROOT_TAG)
        if self.id is not None:
            element.set('id', self.id)
        return element
