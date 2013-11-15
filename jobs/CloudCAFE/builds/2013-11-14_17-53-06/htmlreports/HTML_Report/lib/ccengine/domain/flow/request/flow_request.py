import json
from datetime import datetime

from ccengine.domain.base_domain import BaseMarshallingDomain


class TicketRequest(BaseMarshallingDomain):

    def __init__(self, queue=None, group=None,
                 cloud_queue=None, lastActivity=None):
        super(TicketRequest, self).__init__()
        self.queue = queue
        self.group = group
        self.cloud_queue = cloud_queue
        self.lastActivity = lastActivity

    def last_activity(self):
        last_activity_time = datetime.utcnow()
        return last_activity_time.strftime('%a, %d %b %Y %H:%M:%S GMT')

    def _obj_to_json(self):
        final_dict = {}
        view_list = ListObject(self.queue, self.group,
                               self.cloud_queue)._obj_to_dict()
        final_dict['list'] = view_list
        if self.lastActivity is None:
            final_dict['lastActivity'] = self.last_activity()
        return json.dumps(final_dict)


class ListObject(BaseMarshallingDomain):

    def __init__(self, queue=None, group=None,
                 cloud_queue=None):
        super(ListObject, self).__init__()
        self.queue = queue
        self.group = group
        self.cloud_queue = cloud_queue

    def _obj_to_dict(self):
        ret = self._auto_to_dict()
        final_dict = self._remove_empty_values(ret)
        return final_dict
