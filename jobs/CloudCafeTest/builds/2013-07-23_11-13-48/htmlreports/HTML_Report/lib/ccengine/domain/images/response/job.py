from ccengine.domain.base_domain import BaseMarshallingDomain
from ccengine.domain.images.response.metadata import Metadata
import json


class Job(BaseMarshallingDomain):

    ROOT_TAG = 'job'

    def __init__(self, status=None, hard_timeout=None, tenant=None,
                  created_at=None, updated_at=None, retry_count=None,
                  schedule_id=None, worker_id=None, timeout=None, action=None,
                  id=None, metadata=None):

        super(Job, self).__init__()
        self.status = status
        self.hard_timeout = hard_timeout
        self.tenant = tenant
        self.created_at = created_at
        self.updated_at = updated_at
        self.retry_count = retry_count
        self.schedule_id = schedule_id
        self.worker_id = worker_id
        self.timeout = timeout
        self.action = action
        self.id = id
        self.metadata = metadata

    @classmethod
    def _json_to_obj(cls, serialized_str):

        ret = None

        json_dict = json.loads(serialized_str)

        if json_dict.get(cls.ROOT_TAG) is not None:
            ret = cls._dict_to_obj(json_dict.get(cls.ROOT_TAG))

        if json_dict.get("{0}{1}".format(cls.ROOT_TAG, 's')) is not None:
            ret = []
            for item in json_dict.get("{0}{1}".format(cls.ROOT_TAG, 's')):
                ret.append(cls._dict_to_obj(item))

        return ret

    @classmethod
    def _dict_to_obj(cls, dic):

        kwargs = {'status': dic.get('status'),
                  'hard_timeout': dic.get('hard_timeout'),
                  'tenant': dic.get('tenant'),
                  'created_at': dic.get('created_at'),
                  'updated_at': dic.get('updated_at'),
                  'retry_count': dic.get('retry_count'),
                  'schedule_id': dic.get('schedule_id'),
                  'worker_id': dic.get('worker_id'),
                  'timeout': dic.get('timeout'),
                  'action': dic.get('action'), 'id': dic.get('id'),
                  'metadata': Metadata._dict_to_obj(dic.get('metadata'))}

        return Job(**kwargs)
