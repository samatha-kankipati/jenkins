from ccengine.domain.base_domain import BaseMarshallingDomain
import json
from ccengine.domain.images.response.metadata import Metadata


class Schedule(BaseMarshallingDomain):

    ROOT_TAG = 'schedule'

    def __init__(self, id=None, created_at=None, updated_at=None, tenant=None,
                  action=None, minute=None, hour=None, day_of_month=None,
                  month=None, day_of_week=None, last_scheduled=None,
                  next_run=None, metadata=None):

        super(Schedule, self).__init__()
        self.id = id
        self.created_at = created_at
        self.updated_at = updated_at
        self.tenant = tenant
        self.action = action
        self.minute = minute
        self.hour = hour
        self.day_of_month = day_of_month
        self.month = month
        self.day_of_week = day_of_week
        self.last_scheduled = last_scheduled
        self.next_run = next_run
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

        kwargs = {'id': dic.get('id'), 'created_at': dic.get('created_at'),
                  'updated_at': dic.get('updated_at'),
                  'tenant': dic.get('tenant'),
                  'action': dic.get('action'), 'minute': dic.get('minute'),
                  'hour': dic.get('hour'),
                  'day_of_month': dic.get('day_of_month'),
                  'month': dic.get('month'),
                  'day_of_week': dic.get('day_of_week'),
                  'last_scheduled': dic.get('last_scheduled'),
                  'next_run': dic.get('next_run'),
                  'metadata': dic.get('metadata')}

        return Schedule(**kwargs)
