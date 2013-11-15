import json

from ccengine.domain.base_domain import BaseMarshallingDomain


class Schedule(BaseMarshallingDomain):

    ROOT_TAG = 'schedule'

    def __init__(self, tenant=None, action=None, minute=None, hour=None,
                 day_of_month=None, month=None, day_of_week=None,
                 metadata=None, next_run=None, last_scheduled=None,
                 updated_at=None, created_at=None):

        super(Schedule, self).__init__()
        self.tenant = tenant
        self.action = action
        self.minute = minute
        self.hour = hour
        self.day_of_month = day_of_month
        self.month = month
        self.day_of_week = day_of_week
        self.next_run = next_run
        self.metadata = metadata
        self.last_scheduled = last_scheduled
        self.updated_at = updated_at
        self.created_at = created_at

    def _obj_to_json(self):

        ret = self._obj_to_dict()

        return json.dumps({self.ROOT_TAG: ret})

    def _obj_to_dict(self):

        ret = {}

        if self.tenant is not None:
            ret['tenant'] = self.tenant

        if self.action is not None:
            ret['action'] = self.action

        if self.minute is not None:
            ret['minute'] = self.minute

        if self.hour is not None:
            ret['hour'] = self.hour

        if self.day_of_month is not None:
            ret['day_of_month'] = self.day_of_month

        if self.month is not None:
            ret['month'] = self.month

        if self.day_of_week is not None:
            ret['day_of_week'] = self.day_of_week

        if self.next_run is not None:
            ret['next_run'] = self.next_run

        if self.metadata is not None:
            ret['metadata'] = self.metadata

        if self.last_scheduled is not None:
            ret['last_scheduled'] = self.last_scheduled

        if self.updated_at is not None:
            ret['updated_at'] = self.updated_at

        if self.created_at is not None:
            ret['created_at'] = self.created_at

        return ret

    def _obj_to_xml(self):

        pass
