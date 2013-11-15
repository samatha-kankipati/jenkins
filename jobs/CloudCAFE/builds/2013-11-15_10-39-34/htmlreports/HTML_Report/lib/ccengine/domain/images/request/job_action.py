import json

from ccengine.domain.base_domain import BaseMarshallingDomain


class JobAction(BaseMarshallingDomain):

    def __init__(self, action=None):

        super(JobAction, self).__init__()
        self.action = action

    def _obj_to_json(self):

        ret = self._obj_to_dict()

        return json.dumps(ret)

    def _obj_to_dict(self):

        ret = {}

        if self.action is not None:
            ret['action'] = self.action

        return ret

    def _obj_to_xml(self):

        pass
