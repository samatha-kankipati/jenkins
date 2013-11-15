import json
from xml.etree import ElementTree
from ccengine.domain.identity.v2_0.base_identity_domain \
    import BaseIdentityDomain, BaseIdentityDomainList


class SecretQAs(BaseIdentityDomainList):

    ROOT_TAG = 'secretqas'
    JSON_ROOT_TAG = 'RAX-AUTH:{0}'.format(ROOT_TAG)

    def __init__(self, secretqas=None):
        '''An object that represents an secrets response object.
        '''
        super(SecretQAs, self).__init__()
        self.extend(secretqas)

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        return cls._list_to_obj(json_dict.get(cls.JSON_ROOT_TAG))

    @classmethod
    def _list_to_obj(cls, list_):
        ret = {cls.ROOT_TAG: [SecretQA(**secretqa) for secretqa in list_]}
        return SecretQAs(**ret)

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        element = ElementTree.fromstring(serialized_str)
        cls._remove_identity_xml_namespaces(element)
        if element.tag != cls.ROOT_TAG:
            return None
        return cls._xml_list_to_obj(element.findall(SecretQA.ROOT_TAG))

    @classmethod
    def _xml_list_to_obj(cls, xml_list):
        kwargs = {cls.ROOT_TAG: [SecretQA._xml_ele_to_obj(ele)
                                 for ele in xml_list]}
        return SecretQAs(**kwargs)


class SecretQA(BaseIdentityDomain):

    ROOT_TAG = 'secretqa'
    JSON_ROOT_TAG = 'RAX-KSQA:secretQA'

    def __init__(self, id=None, question=None, answer=None):
        '''An object that represents an secrets response object.
        '''
        super(SecretQA, self).__init__()
        self.id = id
        self.question = question
        self.answer = answer

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        return SecretQA(**json_dict.get(cls.JSON_ROOT_TAG))

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        element = ElementTree.fromstring(serialized_str)
        cls._remove_identity_xml_namespaces(element)
        if element.tag.lower() != cls.ROOT_TAG.lower():
            return None
        return cls._xml_ele_to_obj(element)

    @classmethod
    def _xml_ele_to_obj(cls, xml_ele):
        kwargs = {'question': xml_ele.get('question'),
                  'answer': xml_ele.get('answer')}
        try:
            kwargs['id'] = int(xml_ele.get('id'))
        except (ValueError, TypeError):
            kwargs['id'] = xml_ele.get('id')
        return SecretQA(**kwargs)
