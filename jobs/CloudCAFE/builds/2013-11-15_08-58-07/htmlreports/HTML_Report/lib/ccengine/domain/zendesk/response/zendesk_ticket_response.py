import json

from ccengine.domain.base_domain import BaseMarshallingDomain


class ZendeskTicketResponse(BaseMarshallingDomain):

    def __init__(self, url=None, id=None, type=None, custom_fields=None,
                 group_id=None, subject=None, description=None,
                 updated_at=None, external_id=None, via=None,
                 priority=None, requester_id=None,
                 submitter_id=None, assignee_id=None, organization_id=None,
                 collaborator_ids=None, forum_topic_id=None,
                 problem_id=None, has_incidents=None, status=None,
                 due_at=None, tags=None, recipient=None, created_at=None,
                 satisfaction_rating=None, sharing_agreement_ids=None,
                 fields=None):

        self.url = url
        self.id = id
        self.external_id = external_id
        self.via = via
        self.created_at = created_at
        self.updated_at = updated_at
        self.type = type
        self.subject = subject
        self.description = description
        self.priority = priority
        self.requester_id = requester_id
        self.submitter_id = submitter_id
        self.assignee_id = assignee_id
        self.organization_id = organization_id
        self.group_id = group_id
        self.collaborator_ids = collaborator_ids
        self.forum_topic_id = forum_topic_id
        self.problem_id = problem_id
        self.has_incidents = has_incidents
        self.status = status
        self.due_at = due_at
        self.tags = tags
        self.custom_fields = custom_fields
        self.recipient = recipient
        self.satisfaction_rating = satisfaction_rating
        self.sharing_agreement_ids = sharing_agreement_ids
        self.fields = fields

    @classmethod
    def _json_to_obj(cls, serialized_str):
        ticket = json.loads(serialized_str)
        ret = cls._dict_to_obj(ticket.get('ticket'))
        return ret

    @classmethod
    def _dict_to_obj(cls, ticket_dict):
        ticket = ZendeskTicketResponse(**ticket_dict)
        if len(ticket.custom_fields) != 0:
            custom_field_obj = Fields._json_to_obj(ticket.custom_fields)
            ticket.custom_fields = custom_field_obj
        if len(ticket.fields) != 0:
            field_obj = Fields._json_to_obj(ticket.fields)
            ticket.fields = field_obj
        return ticket


class Fields(BaseMarshallingDomain):

    def __init__(self, field_id, value):
        self.field_id = field_id
        self.field_value = value

    @classmethod
    def _json_to_obj(cls, custom_fields):
        field_obj_list = []
        for field in custom_fields:
            obj = Fields(field['id'], field['value'])
            field_obj_list.append(obj)
        return field_obj_list
