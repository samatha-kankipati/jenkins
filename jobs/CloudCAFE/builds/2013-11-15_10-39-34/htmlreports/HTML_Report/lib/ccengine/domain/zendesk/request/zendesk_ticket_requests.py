import json

from ccengine.domain.base_domain import BaseMarshallingDomain


class CreateTicketRequest(BaseMarshallingDomain):

    def __init__(self, group_id, subject, comment_body,
                 priority=None, tags=None, assignee_id=None, status=None):

        super(CreateTicketRequest, self).__init__()
        self.group_id = group_id
        self.subject = subject.encode('utf8')
        self.assignee_id = assignee_id
        self.comment_body = comment_body.encode('utf8')
        self.priority = priority
        self.status = status
        self.tags = tags

    def _obj_to_json(self):
        final_dict = {}
        ret = self._obj_to_dict()
        final_dict["ticket"] = ret
        return json.dumps(final_dict)

    def _obj_to_dict(self):
        self.comment = Comment(self.comment_body.encode('utf8')).\
            _obj_to_json()
        del self.comment_body
        ret = self._auto_to_dict()
        final_dict = self._remove_empty_values(ret)
        return final_dict


class Comment(BaseMarshallingDomain):

    def __init__(self, body):
        self.body = body

    def _obj_to_json(self):
        ret = {}
        ret['body'] = self.body
        return ret


class UpdateTicketRequest(BaseMarshallingDomain):

    def __init__(self, status=None, priority=None,
                 assignee_id=None, tags=None):

        super(UpdateTicketRequest, self).__init__()
        self.status = status
        self.priority = priority
        self.assignee_id = assignee_id
        self.tags = tags

    def _obj_to_json(self):
        ret = {}
        final_dict = {}
        if self.status is not None:
            ret["status"] = self.status
        if self.assignee_id is not None:
            ret["assignee_id"] = self.assignee_id
        if self.priority is not None:
            ret["priority"] = self.priority
        if self.tags is not None:
            ret["tags"] = self.tags

        final_dict["ticket"] = ret
        return json.dumps(final_dict)
