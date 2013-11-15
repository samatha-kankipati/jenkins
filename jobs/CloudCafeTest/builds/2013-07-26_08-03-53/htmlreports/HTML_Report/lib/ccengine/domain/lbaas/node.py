from ccengine.domain.base_domain import BaseMarshallingDomain, \
    BaseMarshallingDomainList
import json
import xml.etree.ElementTree as ET
from ccengine.domain.lbaas.metadata import Metadata


class NodeList(BaseMarshallingDomainList):

    ROOT_TAG = 'nodes'

    def __init__(self, nodes=[]):
        super(NodeList, self).__init__()
        for node in nodes:
            self.append(node)

    def get_by_type(self, type):
        for node in self:
            if node.type == type:
                return node

    def get_by_id(self, id):
        for node in self:
            if node.id == id:
                return node

    def get_by_address(self, address):
        for node in self:
            if node.address == address:
                return node

    def _obj_to_json(self):
        return json.dumps({self.ROOT_TAG: self._obj_to_dict()})

    def _obj_to_dict(self):
        return [node._obj_to_dict() for node in self]

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        return cls._dict_to_obj(json_dict.get(cls.ROOT_TAG))

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        pass

    @classmethod
    def _dict_to_obj(cls, node_dict):
        kwargs = {cls.ROOT_TAG: [Node._dict_to_obj(node)
                                 for node in node_dict]}
        return NodeList(**kwargs)


class Node(BaseMarshallingDomain):

    ROOT_TAG = 'node'

    def __init__(self, id=None, address=None, port=None, condition=None,
                 status=None, weight=None, type=None, metadata=None):
        '''An object that represents the data of a Load Balancer Node.
        '''
        self.id = id
        self.address = address
        self.port = port
        self.condition = condition
        self.status = status
        self.weight = weight
        self.type = type
        self.metadata = metadata

    def _obj_to_json(self):
        return json.dumps({self.ROOT_TAG: self._obj_to_dict()})

    def _obj_to_dict(self):
        ret = {}
        if self.id is not None:
            ret['id'] = self.id
        if self.address is not None:
            ret['address'] = self.address
        if self.type is not None:
            ret['type'] = self.type
        if self.port is not None:
            ret['port'] = self.port
        if self.condition is not None:
            ret['condition'] = self.condition
        if self.status is not None:
            ret['status'] = self.status
        if self.weight is not None:
            ret['weight'] = self.weight
        if self.metadata is not None:
            ret['metadata'] = Metadata._obj_to_dict(self)
            pass
        return ret

    def _obj_to_xml(self):
        ret = self._auto_to_xml()
        for meta in ret.iter('metadat'):
            meta.tag = 'meta'
        return ET.tostring(ret)

    @classmethod
    def _json_to_obj(cls, serialized_str):
        ret = None
        json_dict = json.loads(serialized_str)
        if json_dict.get(cls.ROOT_TAG) is not None:
            ret = cls._dict_to_obj(json_dict.get(cls.ROOT_TAG))
        return ret

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        pass

    @classmethod
    def _dict_to_obj(cls, dic):
        if Node.ROOT_TAG in dic:
            dic = dic.get(Node.ROOT_TAG)
        if Metadata.ROOT_TAG in dic:
            dic[Metadata.ROOT_TAG] = \
                Metadata._dict_to_obj(dic.get(Metadata.ROOT_TAG))
        return Node(**dic)


class NodeServiceEventList(BaseMarshallingDomainList):

    ROOT_TAG = 'nodeServiceEvents'

    def __init__(self, nodeServiceEvents=[]):
        super(NodeServiceEventList, self).__init__()
        for nse in nodeServiceEvents:
            self.append(nse)

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        if cls.ROOT_TAG not in json_dict:
            return None
        return cls._dict_to_obj(json_dict.get(cls.ROOT_TAG))

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        pass

    @classmethod
    def _dict_to_obj(cls, nse_dict):
        kwargs = {cls.ROOT_TAG: [NodeServiceEvent._dict_to_obj(event)
                                 for event in nse_dict]}
        return NodeServiceEventList(**kwargs)


class NodeServiceEvent(BaseMarshallingDomain):

    ROOT_TAG = 'nodeServiceEvent'

    def __init__(self, nodeId=None, detailedMessage=None, id=None,
                 loadbalancerId=None, accountId=None, author=None,
                 title=None, description=None, type=None, category=None,
                 severity=None, relativeUri=None, created=None):
        self.nodeId = nodeId
        self.detailedMessage = detailedMessage
        self.id = id
        self.loadbalancerId = loadbalancerId
        self.accountId = accountId
        self.author = author
        self.title = title
        self.description = description
        self.type = type
        self.category = category
        self.severity = severity
        self.relativeUri = relativeUri
        self.created = created

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        if cls.ROOT_TAG not in json_dict:
            return None
        return cls._dict_to_obj(json_dict.get(cls.ROOT_TAG))

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        pass

    @classmethod
    def _dict_to_obj(cls, dic):
        return NodeServiceEvent(**dic)
