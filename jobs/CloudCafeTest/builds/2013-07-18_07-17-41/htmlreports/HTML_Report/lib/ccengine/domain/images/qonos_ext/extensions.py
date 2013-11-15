import json
from ccengine.domain.base_domain import BaseMarshallingDomain
import xml.etree.ElementTree as ET
from ccengine.common.constants.images_constants import Constants
from ccengine.domain.compute.response.links import Links
import re


class Extensions(BaseMarshallingDomain):

    ROOT_TAG = 'extension'

    def __init__(self, updated=None, name=None, links=None, namespace=None,
                 alias=None, description=None):

        super(Extensions, self).__init__()
        self.updated = updated
        self.name = name
        self.links = links
        self.namespace = namespace
        self.alias = alias
        self.description = description

    @classmethod
    def _json_to_obj(cls, serialized_str):

        ret = None

        json_dict = json.loads(serialized_str)

        if json_dict.get(cls.ROOT_TAG) is not None:
            ret = cls._dict_to_obj(json_dict.get(cls.ROOT_TAG))

        if json_dict.get("{0}{1}".format(cls.ROOT_TAG, 's')) is not None:
            ret = []
            for item in json_dict.get("{0}{1}".format(cls.ROOT_TAG, 's')):
                ret.append(cls._dict_to_obj(item))

        return ret

    @classmethod
    def _dict_to_obj(cls, dic):

        kwargs = {'updated': dic.get('updated'), 'name': dic.get('name'),
                  'links': dic.get('links'), 'namespace': dic.get('namespace'),
                  'alias': dic.get('alias'),
                  'description': dic.get('description')}

        return Extensions(**kwargs)

    @classmethod
    def _xml_to_obj(cls, serialized_str):

        element = ET.fromstring(serialized_str)
        cls._remove_namespace(element, Constants.XML_API_NAMESPACE)
        cls._remove_namespace(element, Constants.XML_API_ATOM_NAMESPACE)

        if element.tag == 'extension':
            ret = cls._xml_ele_to_obj(element)
        if element.tag == 'extensions':
            ret = []
            for ext in element.findall('extension'):
                s = cls._xml_ele_to_obj(ext)
                ret.append(s)

        return ret

    @classmethod
    def _xml_ele_to_obj(cls, element):

        ext_dict = element.attrib

        if 'updated' in ext_dict:
            ext_dict['updated'] = ext_dict.get('updated')
        if 'name' in ext_dict:
            ext_dict['name'] = ext_dict.get('name')
        if 'namespace' in ext_dict:
            ext_dict['namespace'] = ext_dict.get('namespace')
        if 'alias' in ext_dict:
            ext_dict['alias'] = ext_dict.get('alias')
        for child in element:
            if child.tag == 'description':
                ext_dict['description'] = child.text

        ext = Extensions(**ext_dict)
        ext.links = Links._xml_ele_to_obj(element)

        for each in ext_dict:
            if each.startswith("{"):
                newkey = re.split("}", each)[1]
                if ext_dict[each] == "None":
                    setattr(ext, newkey, None)
                else:
                    setattr(ext, newkey, ext_dict.get(each))

        return ext
