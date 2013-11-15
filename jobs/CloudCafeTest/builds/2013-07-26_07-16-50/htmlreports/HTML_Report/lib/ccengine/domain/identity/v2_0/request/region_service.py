import json
from xml.etree import ElementTree
from ccengine.domain.identity.v2_0.base_identity_domain \
    import BaseIdentityDomainList
from ccengine.common.constants.identity import V2_0Constants


class DefaultRegionServices(BaseIdentityDomainList):

    ROOT_TAG = 'defaultregionServices'
    JSON_ROOT_TAG = 'RAX-AUTH:{0}'.format(ROOT_TAG)

    def __init__(self, defaultRegionServices=None):
        super(DefaultRegionServices, self).__init__()
        self.extend(defaultRegionServices)

    def _obj_to_json(self):
        ret = {self.JSON_ROOT_TAG: self}
        return json.dumps(ret)

    def _obj_to_xml(self):
        element = ElementTree.Element(self.ROOT_TAG)
        element.set('xmlns', V2_0Constants.XML_NS_RAX_AUTH)
        element.set('xmlns:identity', V2_0Constants.XML_NS)
        for service in self:
            if service is None:
                continue
            service_element = ElementTree.Element('serviceName')
            service_element.text = str(service)
            element.append(service_element)
        return ElementTree.tostring(element)
