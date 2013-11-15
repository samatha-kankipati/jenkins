from ccengine.domain.base_domain import BaseMarshallingDomain
import json


class JobStatus(BaseMarshallingDomain):

    ROOT_TAG = 'status'

    def __init__(self, status=None, timeout=None, error_message=None):

        super(JobStatus, self).__init__()
        self.status = status
        self.timeout = timeout
        self.error_message = error_message

    def _obj_to_json(self):

        ret = self._obj_to_dict()

        return json.dumps({self.ROOT_TAG: ret})

    def _obj_to_xml(self):

        pass

    def _obj_to_dict(self):

        ret = {}

        if self.status is not None:
            ret['status'] = self.status

        if self.timeout is not None:
            ret['timeout'] = self.timeout

        if self.error_message is not None:
            ret['error_message'] = self.error_message

        return ret
