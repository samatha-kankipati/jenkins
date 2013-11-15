import json
from xml.etree import ElementTree
from ccengine.domain.identity.v2_0.base_identity_domain \
    import BaseIdentityDomain
from ccengine.common.constants.identity import V2_0Constants


class User(BaseIdentityDomain):

    ROOT_TAG = 'user'

    def __init__(self, username=None, email=None, id=None, defaultRegion=None,
                 domainId=None, enabled=None, password=None):

        super(User, self).__init__()
        self.username = username
        self.email = email
        self.enabled = enabled
        self.password = password
        self.id = id
        self.defaultRegion = defaultRegion
        self.domainId = domainId

    def _obj_to_json(self):
        ret = {}
        if self.username is not None:
            ret['username'] = self.username
        if self.email is not None:
            ret['email'] = self.email
        if self.enabled is not None:
            ret['enabled'] = self.enabled
        if self.password is not None:
            ret['OS-KSADM:password'] = self.password
        if self.id is not None:
            ret['id'] = self.id
        if self.defaultRegion is not None:
            ret['RAX-AUTH:defaultRegion'] = self.defaultRegion
        if self.domainId is not None:
            ret['RAX-AUTH:domainId'] = self.domainId
        return json.dumps({self.ROOT_TAG: ret})

    def _obj_to_xml(self):
        element = ElementTree.Element(self.ROOT_TAG)
        element.set('xmlns', V2_0Constants.XML_NS)
        element.set('xmlns:ns1', V2_0Constants.XML_NS_OS_KSADM)
        element.set('xmlns:rax-auth', V2_0Constants.XML_NS_RAX_AUTH)
        if self.id is not None:
            element.set('id', str(self.id))
        if self.username is not None:
            element.set('username', str(self.username))
        if self.email is not None:
            element.set('email', str(self.email))
        if self.enabled is not None:
            element.set('enabled', str(self.enabled).lower())
        if self.password is not None:
            element.set('ns1:password', str(self.password))
        if self.defaultRegion is not None:
            element.set('rax-auth:defaultRegion', str(self.defaultRegion))
        if self.domainId is not None:
            element.set('rax-auth:domainId', str(self.domainId))
        return ElementTree.tostring(element)
