import json

from ccengine.domain.base_domain import BaseMarshallingDomain


class JobStatus(BaseMarshallingDomain):

    ROOT_TAG = 'status'

    def __init__(self, status=None, timeout=None, error_message=None):

        super(JobStatus, self).__init__()
        self.status = status
        self.timeout = timeout
        self.error_message = error_message

    @classmethod
    def _json_to_obj(cls, serialized_str):

        ret = None

        json_dict = json.loads(serialized_str)

        if json_dict.get(cls.ROOT_TAG) is not None:
            ret = cls._dict_to_obj(json_dict.get(cls.ROOT_TAG))

        return ret

    @classmethod
    def _dict_to_obj(cls, dic):

        return JobStatus(**dic)
