from ccengine.domain.base_domain import BaseDomain
from ccengine.domain.base_domain import BaseMarshallingDomain
import json
from ccengine.domain.core.response.core import Core
from ccengine.common.tools.equality_tools import EqualityTools
from ccengine.common.tools.datatools import string_to_datetime, \
    convert_date_from_cst_to_utc_date
from ccengine.domain.tq_search.response.account_services import AccountServices
from datetime import datetime
import time
import os


class Gate(BaseMarshallingDomain):

    def __init__(self, **kwargs):
        super(Gate, self).__init__(**kwargs)
        for keys, values in kwargs.items():
            setattr(self, keys, values)

    @classmethod
    def _json_to_obj(cls, serialized_str):
        ret = None
        json_dict = json.loads(serialized_str)
        if json_dict.get("Ticket Search API") is not None:
            ret = cls._dict_to_obj(json_dict.get("Ticket Search API"))
        else:
            ret = cls._dict_to_obj(json_dict)
        return ret

    @classmethod
    def _dict_to_obj(cls, result_dict):
        for key, value in result_dict.items():
            new_key = key.replace("-", "_")
            del result_dict[key]
            result_dict[new_key] = value

        gate = Gate(**result_dict)
        return gate


class Search(BaseMarshallingDomain):

    def __init__(self):
        self.total = None
        self.tickets = []
        self.ticket = None
        self.first = None
        self.last = None
        self.previous = None
        self.next = None
        self.offset = None
        self.limit = None

    @classmethod
    def _json_to_obj(cls, serialized_str):
        ret = Search()
        json_dict = json.loads(serialized_str)
        response = json_dict.get("response")
        if response is not None:
            ret.total = response.get("total")
            ret.limit = response.get("limit")
            ret.offset = response.get("offset")
            for link in response.get("links"):
                rel = None
                href = None
                for key, value in link.iteritems():
                    if key == 'rel':
                        rel = value
                    if key == 'href':
                        href = value
                    if (rel is not None) and (href is not None):
                        setattr(ret, rel, href)

            for ticket in response.get("tickets"):
                ticket = TicketDetails(ticket)
                if (hasattr(ticket, "account")) and (ticket.account
                                                     is not None):
                    ticket.account = AccountServices._dict_to_obj(
                        ticket.account)
                if (hasattr(ticket, "queue")) and (ticket.queue
                                                   is not None):
                    ticket.queue = Queue(name=ticket.queue.get("name"),
                                         id=ticket.queue.get("id"))
                if (hasattr(ticket, "assignee")) and (ticket.assignee
                                                      is not None):
                    ticket.assignee =\
                        Assignee(
                            name=ticket.assignee.get("name"),
                            sso=ticket.assignee.get("sso"))
                ret.tickets.append(ticket)
        else:
            response = json_dict.get("ticket")
            ret.ticket = TicketDetails(response)
            if (hasattr(response, "account")) and\
               (response.account is not None):
                response.account = AccountServices.\
                    _dict_to_obj(response.account)
                if (hasattr(ticket, "queue")) and (ticket.queue
                                                   is not None):
                    ticket.queue = Queue(name=ticket.queue.get("name"),
                                         id=ticket.queue.get("id"))
                if (hasattr(ticket, "assignee")) and (ticket.assignee
                                                      is not None):
                    ticket.assignee = Assignee(
                        name=ticket.assignee.get("name"),
                        sso=ticket.assignee.get("sso"))
        return ret


class TicketDetails(BaseMarshallingDomain):

    def __init__(self, ticket):
        if not "source_system" in ticket:
            if 'category.name' in ticket:
                setattr(self, "category", ticket.get("category.name"))
                ticket.pop('category.name')
            if 'subcategory.name' in ticket:
                setattr(self, "subCategory", ticket.get("subcategory.name"))
                ticket.pop('subcategory.name')
            if "status.name" in ticket:
                setattr(self, "status", ticket.get("status.name"))
                ticket.pop('status.name')
            if "status.types.name" in ticket:
                setattr(self, "statusTypes", ticket.get("status.types.name"))
                ticket.pop('status.types.name')
            if "priority.name" in ticket:
                setattr(self, "priority", ticket.get("priority.name"))
                ticket.pop('priority.name')
            if "created" in ticket:
                setattr(self, "createdAt",
                        self._convert_core_date_to_elastic_date(
                        ticket.get("created")))
                ticket.pop('created')
            if "account.number" in ticket:
                setattr(self, "account.id", ticket.get("account.number"))
                ticket.pop('account.number')
            if "modified" in ticket:
                setattr(self, "updatedAt",
                        self._convert_core_date_to_elastic_date(
                        ticket.get("modified")))
                ticket.pop('modified')
            if "has_linux_servers" in ticket:
                setattr(self, "hasLinuxServers",
                        ticket.get("has_linux_servers"))
            if "has_windows_servers" in ticket:
                setattr(self, "hasWindowsServers",
                        ticket.get("has_windows_servers"))
                ticket.pop('has_windows_servers')
            if "severity.name" in ticket:
                setattr(self, "severityName",
                        ticket.get("severity.name"))
                ticket.pop("severity.name")
            if "subcategory.name" in ticket:
                setattr(self, "subCategory",
                        ticket.get("subcategory.name"))
                ticket.pop("subcategory.name")
            if "last_public_response_date" in ticket:
                last_public_response_date = \
                    self._convert_core_date_to_elastic_date(
                        ticket.get("last_public_response_date"))
                ticket.pop("last_public_response_date")
                setattr(self, "lastPublicCommentDate",
                        last_public_response_date)
            if "account.service_level_name" in ticket:
                setattr(self, "accountServiceLevel",
                        ticket.get("account.service_level_name"))
                ticket.pop("account.service_level_name")
            if "account.support_team.support_territory.code" in ticket:
                setattr(self, "accountTeamTerritoryCode",
                        ticket.
                        get("account.support_team.support_territory.code"))
                ticket.pop("account.support_team.support_territory.code")
            if "assignee.name" in ticket and "assignee.employee_userid"\
                    in ticket:
                setattr(self, "assignee",
                        Assignee(ticket.get("assignee.name"),
                                 ticket.get("assignee.employee_userid")))
                ticket.pop("assignee.name")
                ticket.pop("assignee.employee_userid")
            if "queue.name" in ticket and "queue.id" in ticket:
                setattr(self, "queue", Queue(ticket.get("queue.name"),
                                             ticket.get("queue.id")))
                ticket.pop("queue.id")
                ticket.pop("queue.name")

            setattr(self, "sourceSystem", "CORE")

        for key, value in ticket.items():
            setattr(self, key, value)

    def __eq__(self, other):
        other = TicketDetails(vars(other))
        self.difficulty = int(self.difficulty)
        self.statusTypes.sort()
        other.statusTypes.sort()
        # since the are_object_equal  method does not take care of the
        # comparison of the object in an object so for comparing those fields
        # like queue and assignee we are having condition_1 and condition_2
        if self.queue is not None:
            condition_1 = EqualityTools.are_objects_equal(self.queue,
                                                          other.queue)
        else:
            condition_1 = False
        if self.assignee is not None:
            condition_2 = EqualityTools.are_objects_equal(self.assignee,
                                                          other.assignee)
        else:
            condition_2 = True
        condition = EqualityTools.\
            are_objects_equal(self, other,
                              keys_to_exclude=["link",
                                               "severityName",
                                               "account",
                                               "queue",
                                               "assignee",
                                               "documentLastUpdatedTimestamp",
                                               "updateEventDate"])
        return condition and condition_1 and condition_2

    def _convert_core_date_to_elastic_date(self, datetime_str):
        if datetime_str is not None:
            return convert_date_from_cst_to_utc_date(datetime_str) + \
                ".000+0000"
        else:
            return datetime_str


class Queue(BaseMarshallingDomain):

    def __init__(self, name=None, id=None):
        '''An object that represents an account services response object.
        Keyword arguments:
        '''
        self.name = name
        self.id = unicode(id)


class Assignee(BaseMarshallingDomain):

    def __init__(self, name=None, sso=None):
        '''An object that represents an account services response object.
        Keyword arguments:
        '''
        self.name = name
        self.sso = sso
