import json

from ccengine.domain.base_domain import BaseMarshallingDomain


class AllTicketsresponse(BaseMarshallingDomain):
    def __init__(self, list, my, statistics, visited):
        """ An object that represent all ticket response
        of flow API"""
        super(AllTicketsresponse, self).__init__()
        self.list = list
        self.my_tickets = my
        self.statistics = statistics
        self.visited = visited

    @classmethod
    def _json_to_obj(cls, serialized_str):
        json_dict = json.loads(serialized_str)
        ret = cls._dict_to_obj(json_dict)
        return ret

    @classmethod
    def _dict_to_obj(self, all_response_dict):
        obj_all_ticket = AllTicketsresponse(**all_response_dict)
        my_tickets_list = []
        tickets_list = []
        if len(obj_all_ticket.list) != 0:
            for ticket in obj_all_ticket.list:
                tickets_list.append(Ticket._dict_to_obj(ticket))
            obj_all_ticket.list = tickets_list

        if len(obj_all_ticket.list) != 0:
            for ticket in obj_all_ticket.my_tickets:
                my_tickets_list.append(Ticket._dict_to_obj(ticket))
            obj_all_ticket.my_tickets = my_tickets_list
        return obj_all_ticket


class Ticket(BaseMarshallingDomain):

    def __init__(self, account=None, account_link=None, age=None,
                 assigned=None, category=None, difficulty=None,
                 has_linux_servers=None, has_windows_servers=None,
                 high_profile=None, os_sort=None, queueview=None,
                 account_number=None, service_level=None, state=None,
                 idle=None, severity=None, severity_display=None, queue=None,
                 ref_no=None, state_id=None, status=None, subject=None,
                 system=None, team=None, ticket_link=None):
        """
        An object that represents an flow api ticket response object.
        Keyword arguments:
        """
        super(Ticket, self).__init__()
        self.account = account.encode('utf8')
        self.account_link = account_link
        self.account_number = account_number
        self.age = age
        self.assignee = assigned
        self.category = category.encode('utf8')
        self.difficulty = difficulty
        self.has_linux_servers = has_linux_servers
        self.has_windows_servers = has_windows_servers
        self.high_profile = high_profile
        self.os_sort = os_sort
        self.idle = idle
        self.queue = queue
        self.queueview = queueview
        self.number = ref_no
        self.severity = severity
        self.severity_display = severity_display
        self.service_level = service_level
        self.state = state
        self.state_id = state_id
        self.status = status
        self.subject = subject.encode('utf8')
        self.system = system
        self.team = team
        self.ticket_link = ticket_link

    @classmethod
    def _json_to_obj(cls, serialized_str):
        ticket_list = json.loads(serialized_str)
        ret = [cls._dict_to_obj(ticket) for ticket in ticket_list]
        return ret

    @classmethod
    def _dict_to_obj(cls, flow_dict):
        flow_obj = Ticket(**flow_dict)
        return flow_obj
