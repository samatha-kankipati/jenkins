from xml.etree import ElementTree
import json
from ccengine.domain.base_domain import BaseMarshallingDomain
from ccengine.common.constants.identity import V1_1Constants
from ccengine.domain.identity.v1_1.response.base_url import BaseURLRefs


class User(BaseMarshallingDomain):

    ROOT_TAG = 'user'

    def __init__(self, id=None, key=None, mossoId=None, nastId=None,
                 enabled=None, baseURLRefs=None, created=None, updated=None):
        super(User, self).__init__()
        self.id = id
        self.key = key
        self.mossoId = mossoId
        self.nastId = nastId
        self.enabled = enabled
        self.baseURLRefs = baseURLRefs
        self.created = created
        self.updated = updated

    @classmethod
    def _json_to_obj(cls, serialized_str):
        ret = json.loads(serialized_str)
        return cls._dict_to_obj(ret.get(cls.ROOT_TAG))

    @classmethod
    def _dict_to_obj(cls, dic):
        if BaseURLRefs.ROOT_TAG in dic:
            dic[BaseURLRefs.ROOT_TAG] = BaseURLRefs.\
                _list_to_obj(dic.get(BaseURLRefs.ROOT_TAG))
        return User(**dic)

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        element = ElementTree.fromstring(serialized_str)
        cls._remove_namespace(element, V1_1Constants.XML_NS)
        if element.tag != cls.ROOT_TAG:
            return None
        return cls._xml_ele_to_obj(element)

    @classmethod
    def _xml_ele_to_obj(cls, xml_ele):
        kwargs = {'id': xml_ele.get('id'),
                  'nastId': xml_ele.get('nastId'), 'key': xml_ele.get('key'),
                  'created': xml_ele.get('created'),
                  'updated': xml_ele.get('updated')}
        try:
            kwargs['mossoId'] = int(xml_ele.get('mossoId'))
        except (ValueError, TypeError):
            kwargs['mossoId'] = xml_ele.get('mossoId')
        if xml_ele.get('enabled') is not None:
            kwargs['enabled'] = json.loads(xml_ele.get('enabled').lower())
        base_url_refs = xml_ele.find(BaseURLRefs.ROOT_TAG)
        if base_url_refs is not None:
            kwargs[BaseURLRefs.ROOT_TAG] = BaseURLRefs._xml_ele_to_obj(
                    base_url_refs)
        return User(**kwargs)
