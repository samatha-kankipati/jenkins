from xml.etree import ElementTree
import json
from ccengine.domain.base_domain import BaseMarshallingDomain
from ccengine.common.constants.identity import V1_1Constants


class BaseURLRef(BaseMarshallingDomain):

    ROOT_TAG = 'baseURLRef'

    def __init__(self, id=None, href=None, v1Default=None):
        super(BaseURLRef, self).__init__()
        self.id = id
        self.href = href
        self.v1Default = v1Default

    def _obj_to_json(self):
        ret = {'id': self.id, 'v1Default': self.v1Default}
        return json.dumps({self.ROOT_TAG: ret})

    def _obj_to_xml(self):
        ret = self._obj_to_xml_ele()
        ret.set('xmlns', V1_1Constants.XML_NS)
        return ElementTree.tostring(ret)

    def _obj_to_xml_ele(self):
        element = ElementTree.Element(self.ROOT_TAG)
        if self.id is not None:
            element.set('id', str(self.id))
        if self.href is not None:
            element.set('href', str(self.href))
        if self.v1Default is not None:
            element.set('v1Default', str(self.v1Default).lower())
        return element

class BaseURL(BaseMarshallingDomain):

    ROOT_TAG = 'baseURL'

    def __init__(self, id=None, userType=None, region=None,
            serviceName=None, publicURL=None, internalURL=None,
            adminURL=None, default=None, enabled=None):
        super(BaseURL, self).__init__()
        self.id = id
        self.userType = userType
        self.region = region
        self.serviceName = serviceName
        self.publicURL = publicURL
        self.internalURL = internalURL
        self.adminURL = adminURL
        self.default = default
        self.enabled = enabled

    def _obj_to_json(self):
        ret = {'id': self.id, 'userType': self.userType, 
                'region': self.region, 'serviceName': self.serviceName, 
                'publicURL': self.publicURL, 'internalURL': self.internalURL, 
                'adminURL': self.adminURL, 'default': self.default, 
                'enabled': self.enabled}
        return json.dumps({self.ROOT_TAG: ret})

    def _obj_to_xml(self):
        ret = self._obj_to_xml_ele()
        ret.set('xmlns', V1_1Constants.XML_NS)
        return ElementTree.tostring(ret)

    def _obj_to_xml_ele(self):
        element = ElementTree.Element(self.ROOT_TAG)
        if self.id is not None:
            element.set('id', str(self.id))
        if self.userType is not None:
            element.set('userType', str(self.userType))
        if self.region is not None:
            element.set('region', str(self.region))
        if self.serviceName is not None:
            element.set('serviceName', str(self.serviceName))
        if self.publicURL is not None:
            element.set('publicURL', str(self.publicURL))
        if self.internalURL is not None:
            element.set('internalURL', str(self.internalURL))
        if self.adminURL is not None:
            element.set('adminURL', str(self.adminURL))
        if self.default is not None:
            element.set('default', bool(self.default))
        if self.enabled is not None:
            element.set('enabled', bool(self.enabled))

        return element
