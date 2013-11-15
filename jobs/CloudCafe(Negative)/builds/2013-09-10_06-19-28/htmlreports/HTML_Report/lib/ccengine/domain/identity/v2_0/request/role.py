import json
from xml.etree import ElementTree
from ccengine.domain.identity.v2_0.base_identity_domain \
    import BaseIdentityDomain
from ccengine.common.constants.identity import V2_0Constants


class Role(BaseIdentityDomain):

    ROOT_TAG = 'role'

    def __init__(self, name=None, description=None, id=None,
                 weight=None, propagate=None):

        super(Role, self).__init__()
        self.name = name
        self.description = description
        self.id = id
        self.propagate = propagate
        self.weight = weight

    def _obj_to_json(self):
        ret = self._auto_to_dict()
        if self.propagate is not None:
            ret['role']['RAX-AUTH:propagate'] = self.propagate
            del(ret['role']['propagate'])
        if self.weight is not None:
            ret['role']['RAX-AUTH:Weight'] = self.weight
            del(ret['role']['weight'])
        return json.dumps(ret)

    def _obj_to_xml(self):
        element = ElementTree.Element(self.ROOT_TAG)
        element.set('xmlns', V2_0Constants.XML_NS)
        if self.id is not None:
            element.set('id', str(self.id))
        if self.name is not None:
            element.set('name', str(self.name))
        if self.description is not None:
            element.set('description', str(self.description))
        return ElementTree.tostring(element)
