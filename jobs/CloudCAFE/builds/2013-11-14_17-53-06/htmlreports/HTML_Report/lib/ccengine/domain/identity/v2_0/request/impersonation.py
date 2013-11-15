import json
from xml.etree import ElementTree
from ccengine.domain.identity.v2_0.base_identity_domain \
    import BaseIdentityDomain, BaseIdentityDomainList
from ccengine.common.constants.identity import V2_0Constants


class Impersonation(BaseIdentityDomain):

    ROOT_TAG = 'impersonation'
    JSON_ROOT_TAG = 'RAX-AUTH:{0}'.format(ROOT_TAG)

    def __init__(self, username=None, expire_in_seconds=None):
        '''An object that represents an impersonation request object.
        '''
        super(Impersonation, self).__init__()
        self.username = username
        self.expire_in_seconds = expire_in_seconds

    def _obj_to_json(self):
        ret = {}
        if self.expire_in_seconds is not None:
            ret['expire-in-seconds'] = self.expire_in_seconds
        if self.username is not None:
            ret['user'] = {'username': self.username}
        ret = {self.JSON_ROOT_TAG: ret}
        return json.dumps(ret)

    def _obj_to_xml(self):
        element = ElementTree.Element(self.ROOT_TAG)
        element.set('xmlns:rax-auth', V2_0Constants.XML_NS_RAX_AUTH)
        element.set('xmlns:ns', V2_0Constants.XML_NS)
        if self.username is not None:
            user = ElementTree.Element('rax-auth:user')
            user.set('username', str(self.username))
            element.append(user)
        if self.expire_in_seconds is not None:
            eis = ElementTree.Element('expire-in-seconds')
            eis.text = str(self.expire_in_seconds)
            element.append(eis)
        return ElementTree.tostring(element)
