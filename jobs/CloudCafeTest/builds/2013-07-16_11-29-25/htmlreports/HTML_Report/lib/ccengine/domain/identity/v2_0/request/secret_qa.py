import json
from xml.etree import ElementTree
from ccengine.domain.identity.v2_0.base_identity_domain \
    import BaseIdentityDomain
from ccengine.common.constants.identity import V2_0Constants


class SecretQA(BaseIdentityDomain):

    ROOT_TAG = 'secretqa'
    JSON_ROOT_TAG = 'RAX-AUTH:{0}'.format(ROOT_TAG)

    def __init__(self, id=None, question=None, answer=None):
        super(SecretQA, self).__init__()
        self.question = question
        self.id = id
        self.answer = answer

    def _obj_to_json(self):
        ret = {}
        if self.question is not None:
            ret['question'] = self.question
        if self.answer is not None:
            ret['answer'] = self.answer
        if self.id is not None:
            ret['id'] = self.id
        ret = {self.JSON_ROOT_TAG: ret}
        return json.dumps(ret)

    def _obj_to_xml(self):
        element = ElementTree.Element(self.ROOT_TAG)
        element.set('xmlns', V2_0Constants.XML_NS_RAX_AUTH)
        element.set('xmlns:identity', V2_0Constants.XML_NS)
        if self.id is not None:
            element.set('id', str(self.id))
        if self.answer is not None:
            element.set('answer', str(self.answer))
        if self.question is not None:
            element.set('question', str(self.question))
        return ElementTree.tostring(element)


#Need this because of the discrepancy between json root tags when creating
#and updating.  Also xml namespaces are different.  This should be logged
#as a bug because this is pretty lame.
class UpdateSecretQA(BaseIdentityDomain):

    ROOT_TAG = 'secretQA'
    JSON_ROOT_TAG = 'RAX-KSQA:{0}'.format(ROOT_TAG)

    def __init__(self, id=None, question=None, answer=None):
        super(UpdateSecretQA, self).__init__()
        self.question = question
        self.id = id
        self.answer = answer

    def _obj_to_json(self):
        ret = {}
        if self.question is not None:
            ret['question'] = self.question
        if self.answer is not None:
            ret['answer'] = self.answer
        if self.id is not None:
            ret['id'] = self.id
        ret = {self.JSON_ROOT_TAG: ret}
        return json.dumps(ret)

    def _obj_to_xml(self):
        element = ElementTree.Element(self.ROOT_TAG)
        element.set('xmlns', V2_0Constants.XML_NS_RAX_KSQA)
        if self.id is not None:
            element.set('id', str(self.id))
        if self.answer is not None:
            element.set('answer', str(self.answer))
        if self.answer is not None:
            element.set('question', str(self.question))
        return ElementTree.tostring(element)
