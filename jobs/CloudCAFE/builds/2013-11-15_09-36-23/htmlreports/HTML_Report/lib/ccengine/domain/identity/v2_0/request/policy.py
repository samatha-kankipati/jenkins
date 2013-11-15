import json
from xml.etree import ElementTree
from ccengine.domain.identity.v2_0.base_identity_domain \
    import BaseIdentityDomain
from ccengine.common.constants.identity import V2_0Constants


class Policy(BaseIdentityDomain):

    ROOT_TAG = 'policy'
    JSON_ROOT_TAG = 'RAX-AUTH:{0}'.format(ROOT_TAG)

    def __init__(self, enabled=None, description=None, blob=None, global_=None,
                 type=None, name=None):
        super(Policy, self).__init__()
        self.enabled = enabled
        self.description = description
        self.blob = blob
        self.global_ = global_
        self.type = type
        self.name = name

    def _obj_to_json(self):
        ret = {}
        if self.enabled is not None:
            ret['enabled'] = self.enabled
        if self.description is not None:
            ret['description'] = self.description
        if self.blob is not None:
            ret['blob'] = self.blob
        if self.global_ is not None:
            ret['global'] = self.global_
        if self.type is not None:
            ret['type'] = self.type
        if self.name is not None:
            ret['name'] = self.name
        ret = {self.JSON_ROOT_TAG: ret}
        return json.dumps(ret)

    def _obj_to_xml(self):
        element = ElementTree.Element(self.ROOT_TAG)
        element.set('xmlns', V2_0Constants.XML_NS_RAX_AUTH)
        element.set('xmlns:identity', V2_0Constants.XML_NS)
        if self.blob is not None:
            element.set('blob', str(self.blob))
        if self.enabled is not None:
            element.set('enabled', str(self.enabled).lower())
        if self.description is not None:
            description = ElementTree.Element('description')
            description.text = str(self.description)
            element.append(description)
        if self.name is not None:
            element.set('name', str(self.name))
        if self.type is not None:
            element.set('type', str(self.type))
        if self.global_ is not None:
            element.set('global', str(self.global_).lower())
        return ElementTree.tostring(element)
