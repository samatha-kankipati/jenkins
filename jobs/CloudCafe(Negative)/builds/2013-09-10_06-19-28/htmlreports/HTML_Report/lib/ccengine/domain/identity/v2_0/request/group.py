import json
from xml.etree import ElementTree
from ccengine.domain.identity.v2_0.base_identity_domain \
    import BaseIdentityDomain
from ccengine.common.constants.identity import V2_0Constants


class Group(BaseIdentityDomain):

    ROOT_TAG = 'group'
    JSON_ROOT_TAG = 'RAX-KSGRP:{0}'.format(ROOT_TAG)

    def __init__(self, description=None, name=None):
        super(Group, self).__init__()
        self.description = description
        self.name = name

    def _obj_to_json(self):
        ret = {}
        if self.description is not None:
            ret['description'] = self.description
        if self.name is not None:
            ret['name'] = self.name
        ret = {self.JSON_ROOT_TAG: ret}
        return json.dumps(ret)

    def _obj_to_xml(self):
        element = ElementTree.Element(self.ROOT_TAG)
        element.set('xmlns', V2_0Constants.XML_NS_RAX_KSGRP)
        if self.description is not None:
            description = ElementTree.Element('description')
            description.text = str(self.description)
            element.append(description)
        if self.name is not None:
            element.set('name', str(self.name))
        return ElementTree.tostring(element)
