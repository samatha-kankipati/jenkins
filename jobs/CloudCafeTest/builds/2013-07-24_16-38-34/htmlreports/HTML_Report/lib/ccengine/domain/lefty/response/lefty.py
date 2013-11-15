import json
import re

from ccengine.common.tools.equality_tools import EqualityTools
from ccengine.domain.base_domain import BaseDomain
from ccengine.domain.base_domain import BaseMarshallingDomain


class Ticket(BaseMarshallingDomain):

    def __init__(self, **kwargs):
        super(Ticket, self).__init__(**kwargs)
        for keys, values in kwargs.iteritems():
            setattr(self, keys, values)

    @classmethod
    def _json_to_obj(cls, serialized_str):
        ret = None
        json_dict = json.loads(serialized_str)
        if 'ticket' in json_dict.keys():
            ret = cls._dict_to_obj(json_dict.get('ticket'))
        if 'tickets' in json_dict.keys():
            ret = []
            for ticket in json_dict.get('tickets'):
                s = cls._dict_to_obj(ticket)
                ret.append(s)
        return ret

    @classmethod
    def _dict_to_obj(cls, ticket_dict):
        ticket = Ticket(**ticket_dict)
        if hasattr(ticket, 'events'):
            new_serialized_dict = {}
            new_serialized_dict['events'] = ticket.events
            new_serialized_dict = json.dumps(new_serialized_dict)
            ticket.events = Events._json_to_obj(new_serialized_dict)

        return ticket


class Category(BaseMarshallingDomain):

    def __init__(self, **kwargs):
        super(Category, self).__init__(**kwargs)
        for keys, values in kwargs.iteritems():
            setattr(self, keys, values)

    @classmethod
    def _json_to_obj(cls, serialized_str):
        ret = None
        json_dict = json.loads(serialized_str)
        if 'category' in json_dict.keys():
            ret = cls._dict_to_obj(json_dict.get('category'))
        if 'categories' in json_dict.keys():
            ret = []
            for category in json_dict.get('categories'):
                category_obj = cls._dict_to_obj(category)
                ret.append(category_obj)
        return ret

    @classmethod
    def _dict_to_obj(cls, category_dict):
        category = Category(**category_dict)
        return category


class Subcategory(BaseMarshallingDomain):

    def __init__(self, **kwargs):
        super(Subcategory, self).__init__(**kwargs)
        for keys, values in kwargs.iteritems():
            setattr(self, keys, values)

    @classmethod
    def _json_to_obj(cls, serialized_str):
        ret = None
        json_dict = json.loads(serialized_str)
        if 'sub_category' in json_dict.keys():
            ret = cls._dict_to_obj(json_dict.get('sub_category'))
        if 'sub_categories' in json_dict.keys():
            ret = []
            for sub_category in json_dict.get('sub_categories'):
                sub_category_obj = cls._dict_to_obj(sub_category)
                ret.append(sub_category_obj)
        return ret

    @classmethod
    def _dict_to_obj(cls, sub_category_dict):
        sub_category = Subcategory(**sub_category_dict)
        return sub_category


class Queue(BaseMarshallingDomain):

    def __init__(self, **kwargs):
        super(Queue, self).__init__(**kwargs)
        for keys, values in kwargs.iteritems():
            setattr(self, keys, values)

    @classmethod
    def _json_to_obj(cls, serialized_str):
        ret = None
        json_dict = json.loads(serialized_str)
        if 'queue' in json_dict.keys():
            ret = cls._dict_to_obj(json_dict.get('queue'))
        if 'queues' in json_dict.keys():
            ret = []
            for queue in json_dict.get('queues'):
                queue_obj = cls._dict_to_obj(queue_obj)
                ret.append(s)
        return ret

    @classmethod
    def _dict_to_obj(cls, queue_dict):
        queue = Queue(**queue_dict)
        if hasattr(queue, 'query'):
            queue.query = QueueQuery._json_to_obj(queue.query)
        if hasattr(queue, 'sort'):
            queue.sort = QueueSort._json_to_obj(queue.sort)
        if hasattr(queue, 'tickets'):
            new_serialized_dict = {}
            new_serialized_dict['tickets'] = queue.tickets
            new_serialized_dict = json.dumps(new_serialized_dict)
            queue.tickets = Ticket._json_to_obj(new_serialized_dict)
        return queue


class QueueQuery(BaseMarshallingDomain):

    def __init__(self, **kwargs):
        super(QueueQuery, self).__init__(**kwargs)
        for keys, values in kwargs.iteritems():
            setattr(self, keys, values)

    @classmethod
    def _json_to_obj(cls, serialized_str):
        ret = None
        for query_details in serialized_str:
            ret = cls._dict_to_obj(query_details)
        return ret

    @classmethod
    def _dict_to_obj(cls, query_details):
        queue_det = QueueQuery(**query_details)
        return queue_det


class QueueSort(BaseMarshallingDomain):

    def __init__(self, **kwargs):
        super(QueueSort, self).__init__(**kwargs)
        for keys, values in kwargs.iteritems():
            setattr(self, keys, values)

    @classmethod
    def _json_to_obj(cls, serialized_str):
        ret = None
        for sort_details in serialized_str:
            ret = cls._dict_to_obj(sort_details)
        return ret

    @classmethod
    def _dict_to_obj(cls, sort_details):
        sort_det = QueueQuery(**sort_details)
        return sort_det


class Statuses(BaseMarshallingDomain):

    def __init__(self, **kwargs):
        super(Statuses, self).__init__(**kwargs)
        for keys, values in kwargs.iteritems():
            setattr(self, keys, values)

    @classmethod
    def _json_to_obj(cls, serialized_str):
        ret = None
        json_dict = json.loads(serialized_str)
        ret = cls._dict_to_obj(json_dict)

        return ret

    @classmethod
    def _dict_to_obj(cls, status_dict):
        statuses = Statuses(**status_dict)
        return statuses


class Events(BaseMarshallingDomain):

    def __init__(self, **kwargs):
        super(Events, self).__init__(**kwargs)
        for keys, values in kwargs.iteritems():
            setattr(self, keys, values)

    @classmethod
    def _json_to_obj(cls, serialized_str):
        ret = None
        json_dict = json.loads(serialized_str)
        ret = []
        ret = [cls._dict_to_obj(feed) for feed in json_dict.get('events')]
        return ret

    @classmethod
    def _dict_to_obj(cls, event_feed):
        event = Events(**event_feed)
        return event


class PubSub(BaseMarshallingDomain):

    def __init__(self, **kwargs):
        super(PubSub, self).__init__(**kwargs)
        for keys, values in kwargs.iteritems():
            setattr(self, keys, values)

    @classmethod
    def _json_to_obj(cls, serialized_str):
        ret = None
        json_dict = json.loads(serialized_str)
        ret = []

        ret = [cls._dict_to_obj(event) for event in json_dict.get('events')]
        return ret

    @classmethod
    def _dict_to_obj(cls, event_feed):
        event = PubSub(**event_feed)
        if hasattr(event, "data"):
            setattr(event, "ticket",
                    Ticket._dict_to_obj(event.data.get("ticket")))
            setattr(event, "update",
                    Events._dict_to_obj(event.data.get("update")))
            del event.data
        return event
