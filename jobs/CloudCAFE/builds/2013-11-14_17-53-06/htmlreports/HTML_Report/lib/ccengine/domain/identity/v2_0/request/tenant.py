import json
from xml.etree import ElementTree

from ccengine.common.constants.identity import V2_0Constants
from ccengine.domain.identity.v2_0.base_identity_domain \
    import BaseIdentityDomain


class Tenant(BaseIdentityDomain):

    ROOT_TAG = 'tenant'

    def __init__(self, name, description=None, enabled=None):

        super(Tenant, self).__init__()
        self.name = name
        self.description = description
        self.enabled = enabled

    def _obj_to_json(self):
        ret = self._auto_to_dict()
        return json.dumps(ret)

    def _obj_to_xml(self):
        element = ElementTree.Element(self.ROOT_TAG)
        element.set('xmlns', V2_0Constants.XML_NS)
        if self.name is not None:
            element.set('name', str(self.name))
        if self.description is not None:
            element.set('description', str(self.description))
        if self.enabled is not None:
            element.set('enabled', str(self.enabled))
        return ElementTree.tostring(element)
