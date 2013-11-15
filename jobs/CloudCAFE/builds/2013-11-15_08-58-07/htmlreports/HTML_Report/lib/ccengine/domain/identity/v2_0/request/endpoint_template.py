import json
from xml.etree import ElementTree

from ccengine.common.constants.identity import V2_0Constants as v2_0_constants
from ccengine.domain.base_domain import BaseMarshallingDomain


class EndpointTemplate(BaseMarshallingDomain):

    ROOT_TAG = 'OS-KSCATALOG:endpointTemplate'

    def __init__(self, id=None, name=None, type=None, region=None,
                 public_url=None, internal_url=None,
                 admin_url=None, enabled=None):
        super(EndpointTemplate, self).__init__()
        self.id = id
        self.name = name
        self.type = type
        self.region = region
        self.public_url = public_url
        self.internal_url = internal_url
        self.admin_url = admin_url
        self.enabled = enabled

    def _obj_to_json(self):
        ret = {'id': self.id,
               'type': self.type,
               'name': self.name,
               'region': self.region,
               'publicURL': self.public_url,
               'internalURL': self.internal_url,
               'adminURL': self.admin_url,
               'enabled': self.enabled}
        return json.dumps({self.ROOT_TAG: ret})

    def _obj_to_xml(self):
        ret = self._obj_to_xml_ele()
        ret.set('xmlns', v2_0_constants.XML_NS)
        return ElementTree.tostring(ret)

    def _obj_to_xml_ele(self):
        element = ElementTree.Element(self.ROOT_TAG)
        if self.id is not None:
            element.set('id', str(self.id))
        if self.name is not None:
            element.set('name', str(self.name))
        if self.type is not None:
            element.set('type', str(self.type))
        if self.region is not None:
            element.set('region', str(self.region))
        if self.publicURL is not None:
            element.set('publicURL', str(self.public_url))
        if self.internalURL is not None:
            element.set('internalURL', str(self.internal_url))
        if self.adminURL is not None:
            element.set('adminURL', str(self.admin_url))
        if self.enabled is not None:
            element.set('enabled', bool(self.enabled))

        return element
