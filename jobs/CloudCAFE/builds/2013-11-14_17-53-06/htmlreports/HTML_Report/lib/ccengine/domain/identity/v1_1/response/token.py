from xml.etree import ElementTree
import json
from ccengine.domain.base_domain import BaseMarshallingDomain
from ccengine.common.constants.identity import V1_1Constants


class Token(BaseMarshallingDomain):

    ROOT_TAG = 'token'
    XMLNS = 'http://docs.rackspacecloud.com/auth/api/v1.1'

    def __init__(self, id=None, userId=None, userURL=None, created=None,
                 expires=None):
        super(Token, self).__init__()
        self.id = id
        self.userId = userId
        self.userURL = userURL
        self.created = created
        self.expires = expires

    @classmethod
    def _json_to_obj(cls, serialized_str):
        ret = json.loads(serialized_str)
        return Token(**ret.get(cls.ROOT_TAG))

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        element = ElementTree.fromstring(serialized_str)
        cls._remove_namespace(element, V1_1Constants.XML_NS)
        if element.tag != cls.ROOT_TAG:
            return None
        return cls._xml_ele_to_obj(element)

    @classmethod
    def _xml_ele_to_obj(cls, xml_ele):
        kwargs = {'id': xml_ele.get('id'), 'userId': xml_ele.get('userId'),
                  'userURL': xml_ele.get('userURL'),
                  'created': xml_ele.get('created'),
                  'expires': xml_ele.get('expires')}
        return Token(**kwargs)
