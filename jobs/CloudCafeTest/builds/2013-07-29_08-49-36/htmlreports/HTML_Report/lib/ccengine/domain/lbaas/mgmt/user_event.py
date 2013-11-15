from ccengine.domain.base_domain import BaseMarshallingDomain
import xml.etree.ElementTree as ET
import json


class UserEvent(BaseMarshallingDomain):

    ROOT_TAG = 'loadBalancerServiceEvent'

    def __init__(self, id=None, loadbalancerId=None, accountId=None,
                 title=None, author=None, description=None, type=None,
                 category=None, severity=None, relativeUri=None, created=None):
        '''An object that data concerning tickets on a load balancer.

        '''
        self.id = id
        self.loadbalancerId = loadbalancerId
        self.accountId = accountId
        self.title = title
        self.author = author
        self.description = description
        self.type = type
        self.category = category
        self.severity = severity
        self.relativeUri = relativeUri
        self.created = created

    def _obj_to_json(self):
        ret = self._auto_to_dict()
        return json.dumps(ret[self.ROOT_TAG])

    def _obj_to_xml(self):
        ret = self._auto_to_xml()
        return ET.tostring(ret)

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        return cls._dict_to_obj(json_dict)

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        pass

    @classmethod
    def _dict_to_obj(cls, dic):
        return UserEvent(**dic)
