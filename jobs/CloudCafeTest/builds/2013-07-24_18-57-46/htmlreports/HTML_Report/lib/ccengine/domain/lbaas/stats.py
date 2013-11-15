from ccengine.domain.base_domain import BaseMarshallingDomain
import json
import xml.etree.ElementTree as ET


class Stats(BaseMarshallingDomain):

    ROOT_TAG = 'stats'

    def __init__(self, connectTimeOut=None, connectError=None,
                 connectFailure=None, dataTimedOut=None,
                 keepAliveTimedOut=None, maxConn=None):
        self.connectTimeOut = connectTimeOut
        self.connectError = connectError
        self.connectFailure = connectFailure
        self.dataTimedOut = dataTimedOut
        self.keepAliveTimedOut = keepAliveTimedOut
        self.maxConn = maxConn

    @classmethod
    def _json_to_obj(cls, serialized_str):
        ret = None
        json_dict = json.loads(serialized_str)
        ret = cls._dict_to_obj(json_dict)
        return ret

    @classmethod
    def _xml_to_obj(cls, serialized_str):
        pass

    @classmethod
    def _dict_to_obj(cls, dic):
        return Stats(**dic)
