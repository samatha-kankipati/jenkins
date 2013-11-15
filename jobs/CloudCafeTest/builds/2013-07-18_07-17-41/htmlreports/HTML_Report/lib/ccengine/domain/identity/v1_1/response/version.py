from xml.etree import ElementTree
import json
from ccengine.domain.base_domain import BaseMarshallingDomain
from ccengine.common.constants.identity import V1_1Constants


class Version(BaseMarshallingDomain):

    ROOT_TAG = 'version'

    def __init__(self, id=None, status=None, updated=None, docURL=None,
                 wadl=None):
        super(Version, self).__init__()
        self.id = id
        self.status = status
        self.updated = updated
        self.docURL = docURL
        self.wadl = wadl

    @classmethod
    def _json_to_obj(cls, serialized_str):
        ret = json.loads(serialized_str)
        return cls._dict_to_obj(ret.get(cls.ROOT_TAG))

    @classmethod
    def _dict_to_obj(cls, dic):
        return Version(**dic)

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        element = ElementTree.fromstring(serialized_str)
        cls._remove_namespace(element, V1_1Constants.XML_NS)
        if element.tag != cls.ROOT_TAG:
            return None
        return cls._xml_ele_to_obj(element)

    @classmethod
    def _xml_ele_to_obj(cls, ele):
        kwargs = {'id': ele.get('id'), 'status': ele.get('status'),
                  'docURL': ele.get('docURL'), 'wadl': ele.get('wadl')}
        return Version(**kwargs)
