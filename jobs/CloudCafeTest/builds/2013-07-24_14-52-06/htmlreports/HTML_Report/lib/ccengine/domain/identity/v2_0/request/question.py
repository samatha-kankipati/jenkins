import json
from xml.etree import ElementTree
from ccengine.domain.identity.v2_0.base_identity_domain \
    import BaseIdentityDomain
from ccengine.common.constants.identity import V2_0Constants


class Question(BaseIdentityDomain):

    ROOT_TAG = 'question'
    JSON_ROOT_TAG = 'RAX-AUTH:{0}'.format(ROOT_TAG)

    def __init__(self, question=None, questionId=None, answer=None):
        super(Question, self).__init__()
        self.question = question

    def _obj_to_json(self):
        ret = {}
        if self.question is not None:
            ret['question'] = self.question
        ret = {self.JSON_ROOT_TAG: ret}
        return json.dumps(ret)

    def _obj_to_xml(self):
        element = ElementTree.Element(self.ROOT_TAG)
        element.set('xmlns', V2_0Constants.XML_NS_RAX_AUTH)
        element.set('xmlns:identity', V2_0Constants.XML_NS)
        if self.question is not None:
            element.set('question', str(self.question))
        return ElementTree.tostring(element)
