import json

from ccengine.domain.base_domain import BaseMarshallingDomain


class Job(BaseMarshallingDomain):

    ROOT_TAG = 'job'

    def __init__(self, schedule_id=None):

        super(Job, self).__init__()
        self.schedule_id = schedule_id

    def _obj_to_json(self):

        ret = self._obj_to_dict()

        return json.dumps({self.ROOT_TAG: ret})

    def _obj_to_dict(self):

        ret = {}

        if self.schedule_id is not None:
            ret['schedule_id'] = self.schedule_id

        return ret

    def _obj_to_xml(self):

        pass
