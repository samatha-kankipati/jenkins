import json

from ccengine.domain.base_domain import BaseMarshallingDomain


class Worker(BaseMarshallingDomain):

    ROOT_TAG = 'worker'

    def __init__(self, host=None, process_id=None):

        super(Worker, self).__init__()
        self.host = host
        self.process_id = process_id

    def _obj_to_json(self):

        ret = self._obj_to_dict()

        return json.dumps({self.ROOT_TAG: ret})

    def _obj_to_dict(self):

        ret = {}

        if self.host is not None:
            ret['host'] = self.host

        if self.process_id is not None:
            ret['process_id'] = self.process_id

        return ret

    def _obj_to_xml(self):

        pass
