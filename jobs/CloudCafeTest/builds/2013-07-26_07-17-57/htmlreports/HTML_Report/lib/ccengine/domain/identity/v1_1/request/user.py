from xml.etree import ElementTree
import json
from ccengine.domain.base_domain import BaseMarshallingDomain
from ccengine.common.constants.identity import V1_1Constants


class User(BaseMarshallingDomain):

    ROOT_TAG = 'user'

    def __init__(self, id=None, key=None, mossoId=None, nastId=None,
                 enabled=None):
        self.id = id
        self.key = key
        self.mossoId = mossoId
        self.nastId = nastId
        self.enabled = enabled

    def _obj_to_json(self):
        ret = {'id': self.id, 'key': self.key, 'mossoId': self.mossoId,
               'nastId': self.nastId, 'enabled': self.enabled}
        return json.dumps({self.ROOT_TAG: ret})

    def _obj_to_xml(self):
        element = ElementTree.Element(self.ROOT_TAG)
        element.set('xmlns', V1_1Constants.XML_NS)
        if self.id is not None:
            element.set('id', str(self.id))
        if self.key is not None:
            element.set('key', str(self.key))
        if self.mossoId is not None:
            element.set('mossoId', str(self.mossoId))
        if self.nastId is not None:
            element.set('nastId', str(self.nastId))
        if self.enabled is not None:
            element.set('enabled', str(self.enabled).lower())
        return ElementTree.tostring(element)
