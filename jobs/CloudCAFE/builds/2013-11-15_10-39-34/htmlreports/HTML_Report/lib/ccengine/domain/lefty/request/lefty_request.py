import json

from ccengine.common.constants.isl_constants import Constants
from ccengine.domain.base_domain import BaseMarshallingDomain


class CreateTicketRequest(BaseMarshallingDomain):

    def __init__(self, subject, description, category_id, sub_category_id,
                 comment=None):

        super(CreateTicketRequest, self).__init__()
        self.subject = subject
        self.description = description
        self.category_id = category_id
        self.sub_category_id = sub_category_id
        self.comment = comment

    def _obj_to_json(self):
        ret = self._auto_to_dict()
        return json.dumps(ret)


class UpdateTicketRequest(BaseMarshallingDomain):

    def __init__(self, priority=None, assignee=None, rating=None,
                 tags=None, products=[], recipients=[], status=None,
                 comment=None, category_id=None, sub_category_id=None,
                 subject=None, description=None, group=None,
                 difficulty=None, severity=None):

        super(UpdateTicketRequest, self).__init__()
        self.priority = priority
        self.assignee = assignee
        self.rating = rating
        self.tags = tags
        self.products = products
        self.recipients = recipients
        self.status = status
        self.comment = comment
        self.category_id = category_id
        self.sub_category_id = sub_category_id
        self.subject = subject
        self.description = description
        self.group = group
        self.difficulty = difficulty
        self.severity = severity

    def _obj_to_json(self):
        ret = self._auto_to_dict()
        return json.dumps(ret)


class CreateCategorySubCategoryRequest(BaseMarshallingDomain):

    def __init__(self, name):

        super(CreateCategorySubCategoryRequest, self).__init__()
        self.name = name

    def _obj_to_json(self):
        ret = self._auto_to_dict()
        return json.dumps(ret)


class CreateQueueRequest(BaseMarshallingDomain):

    def __init__(self, name, query, sort, description):

        super(CreateQueueRequest, self).__init__()
        self.name = name
        self.query = query
        self.sort = sort
        self.description = description

    def _obj_to_json(self):
        ret = self._auto_to_dict()
        return json.dumps(ret)


class QueueQuery(BaseMarshallingDomain):

    def __init__(self, occurrence, q_property, values):

        super(QueueQuery, self).__init__()
        self.property = q_property
        self.values = values
        self.occurrence = occurrence

    def _obj_to_json(self):
        ret = self._auto_to_dict()
        return [eval(json.dumps(ret))]


class QueueSort(BaseMarshallingDomain):

    def __init__(self, sort_property, order):

        super(QueueSort, self).__init__()
        self.property = sort_property
        self.order = order

    def _obj_to_json(self):
        ret = self._auto_to_dict()
        return [eval(json.dumps(ret))]
