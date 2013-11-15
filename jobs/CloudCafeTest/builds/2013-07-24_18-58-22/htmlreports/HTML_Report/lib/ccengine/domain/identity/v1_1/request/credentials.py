from xml.etree import ElementTree
import json
from ccengine.domain.base_domain import BaseMarshallingDomain
from ccengine.common.constants.identity import V1_1Constants


class Credentials(BaseMarshallingDomain):

    ROOT_TAG = 'credentials'

    def __init__(self, username=None, key=None):
        self.username = username
        self.key = key

    def _obj_to_json(self):
        ret = {self.ROOT_TAG: self._obj_to_dict()}
        return json.dumps(ret)

    def _obj_to_dict(self):
        return {'username': self.username, 'key': self.key}

    def _obj_to_xml(self):
        ret = self._obj_to_xml_ele()
        ret.set('xmlns', V1_1Constants.XML_NS)
        return ElementTree.tostring(ret)

    def _obj_to_xml_ele(self):
        element = ElementTree.Element(self.ROOT_TAG)
        if self.username is not None:
            element.set('username', str(self.username))
        if self.key is not None:
            element.set('key', str(self.key))
        return element


class MossoCredentials(BaseMarshallingDomain):

    ROOT_TAG = 'mossoCredentials'

    def __init__(self, mossoId=None, key=None):
        self.mossoId = mossoId
        self.key = key

    def _obj_to_json(self):
        ret = {self.ROOT_TAG: self._obj_to_dict()}
        return json.dumps(ret)

    def _obj_to_dict(self):
        return {'mossoId': str(self.mossoId), 'key': self.key}

    def _obj_to_xml(self):
        ret = self._obj_to_xml_ele()
        ret.set('xmlns', V1_1Constants.XML_NS)
        return ElementTree.tostring(ret)

    def _obj_to_xml_ele(self):
        element = ElementTree.Element(self.ROOT_TAG)
        if self.mossoId is not None:
            element.set('mossoId', str(self.mossoId))
        if self.key is not None:
            element.set('key', str(self.key))
        return element


class NastCredentials(BaseMarshallingDomain):

    ROOT_TAG = 'nastCredentials'

    def __init__(self, nastId=None, key=None):
        self.nastId = nastId
        self.key = key

    def _obj_to_json(self):
        ret = {self.ROOT_TAG: self._obj_to_dict()}
        return json.dumps(ret)

    def _obj_to_dict(self):
        return {'nastId': str(self.nastId), 'key': str(self.key)}

    def _obj_to_xml(self):
        ret = self._obj_to_xml_ele()
        ret.set('xmlns', V1_1Constants.XML_NS)
        return ElementTree.tostring(ret)

    def _obj_to_xml_ele(self):
        element = ElementTree.Element(self.ROOT_TAG)
        if self.nastId is not None:
            element.set('nastId', str(self.nastId))
        if self.key is not None:
            element.set('key', str(self.key))
        return element


class PasswordCredentials(BaseMarshallingDomain):

    ROOT_TAG = 'passwordCredentials'

    def __init__(self, username=None, password=None):
        self.username = username
        self.password = password

    def _obj_to_json(self):
        ret = {self.ROOT_TAG: self._obj_to_dict()}
        return json.dumps(ret)

    def _obj_to_dict(self):
        return {'username': str(self.username), 'password': str(self.password)}

    def _obj_to_xml(self):
        ret = self._obj_to_xml_ele()
        ret.set('xmlns', V1_1Constants.XML_NS)
        return ElementTree.tostring(ret)

    def _obj_to_xml_ele(self):
        element = ElementTree.Element(self.ROOT_TAG)
        if self.username is not None:
            element.set('username', str(self.username))
        if self.password is not None:
            element.set('password', str(self.password))
        return element
