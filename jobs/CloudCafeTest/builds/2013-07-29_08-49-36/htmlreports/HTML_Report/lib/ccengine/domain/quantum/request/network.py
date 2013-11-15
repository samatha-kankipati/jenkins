from ccengine.domain.base_domain import BaseMarshallingDomain
import json


class Network(BaseMarshallingDomain):

    ROOT_TAG = 'network'

    def __init__(self, name, admin_state_up=None, shared=None, tenant_id=None,
                 status=None, id=None):
        super(Network, self).__init__()
        self.name = name
        self.admin_state_up = admin_state_up
        # For negative testing
        self.shared = shared
        self.tenant_id = tenant_id
        self.id = id
        self.status = status

    def _obj_to_json(self):
        ret = self._auto_to_dict()
        return json.dumps(ret)

    def _obj_to_xml(self):
        ret = self._mini_auto_to_xml(format_type='attr', header=1)
        return ret
