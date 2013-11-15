from ccengine.domain.base_domain import BaseMarshallingDomain
import json


class AddFixedIp(BaseMarshallingDomain):

    ROOT_TAG = 'addFixedIp'

    def __init__(self, network_id):
        self.networkId = network_id

    def _obj_to_json(self):
        ret = self._auto_to_dict()
        return json.dumps(ret)

    def _obj_to_xml(self):
        ret = self._mini_auto_to_xml(format_type='attr')
        return ret


class RemoveFixedIp(BaseMarshallingDomain):

    ROOT_TAG = 'removeFixedIp'

    def __init__(self, address):
        self.address = address

    def _obj_to_json(self):
        ret = self._auto_to_dict()
        return json.dumps(ret)

    def _obj_to_xml(self):
        ret = self._mini_auto_to_xml(format_type='attr')
        return ret
