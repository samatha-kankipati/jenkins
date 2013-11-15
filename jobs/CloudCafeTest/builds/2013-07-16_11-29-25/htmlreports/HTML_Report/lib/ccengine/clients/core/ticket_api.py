from ccengine.clients.core.core_api import CoreAPIClient
from ccengine.domain.core.request.core_request import CTKObject


class TicketAPIClient(CoreAPIClient):
    '''
    Client for ticket related queries in CTK API
    '''
    def __init__(self, url, auth_token, serialize_format=None,
                 deserialize_format=None):

        super(TicketAPIClient, self).__init__(url, auth_token,
                                              serialize_format,
                                              deserialize_format)

    def create_generic_ticket(self, account, queue, subcategory,
                              source, severity, subject,
                              text, result_map):
        '''
        @summary: Creates a Generic CORE ticket
        @param account: Account on which ticket is to be created
        @type account: String
        @param queue: Queue on which ticket is to be created
        @type queue: String
        @param subcategory: Subcategory of ticket
        @type subcategory: String
        @param source: Source of Ticket
        @type source: String
        @param severity: Severity of Ticket
        @type severity: String
        @param subject: Subject of Ticket
        @type subject: String
        @param text: Text of the Ticket
        @type Text: String
        @param result_map: Results Map
        @type: Array of Name Value pairs
        '''
        class_name = "Account.Account"
        method = "addTicket"
        load_arg = account
        args = [queue, subcategory, source, severity, subject, text]

        response = self.query(load_arg=load_arg,
                              class_name=class_name,
                              method=method, args=args,
                              result_map=result_map)
        return response

    def create_internal_ticket(self, queue, subcategory, source, severity,
                               subject, text, result_map):
        '''
        @summary: Create a Internal CORE ticket
        @param queue: Queue on which ticket is to be created
        @type queue: String
        @param subcategory: Subcategory of ticket
        @type subcategory: String
        @param source: Source of Ticket
        @type source: String
        @param severity: Severity of Ticket
        @type severity: String
        @param subject: Subject of Ticket
        @type subject: String
        @param text: Text of the Ticket
        @type Text: String
        @param result_map: Results Map
        @type: Array of Name Value pairs
        '''

        class_name = "Ticket.Queue"
        method = "addInternalTicket"
        load_arg = queue
        args = [subcategory, source, severity, subject, text]

        response = self.query(load_arg=load_arg,
                              class_name=class_name,
                              method=method,
                              args=args,
                              result_map=result_map)
        return response

    def create_customer_ticket(self, account, queue, subcategory, source,
                               severity, subject, text, result_map):
        '''
        @summary: Create a Customer CORE ticket
        @param account: Account on which ticket is to be created
        @type account: String
        @param queue: Queue on which ticket is to be created
        @type queue: String
        @param subcategory: Subcategory of ticket
        @type subcategory: String
        @param source: Source of Ticket
        @type source: String
        @param severity: Severity of Ticket
        @type severity: String
        @param subject: Subject of Ticket
        @type subject: String
        @param text: Text of the Ticket
        @type Text: String
        @param result_map: Results Map
        @type: Array of Name Value pairs
        '''
        class_name = "Ticket.Queue"
        method = "addCustomerTicket"
        load_arg = queue
        args = [subcategory, source, severity, subject, text, account]

        response = self.query(load_arg=load_arg,
                              class_name=class_name,
                              method=method, args=args,
                              result_map=result_map)
        return response

    def create_sub_ticket(self, ticket_number, subject, comment, result_map):
        '''
        @summary: Create a sub ticket for a given ticket
        @param ticket_number: Ticket Number for which subticket is created
        @type ticket_number: String
        @param subject: Subject of Ticket
        @type subject: String
        @param comment: Text of the Ticket
        @type comment: String
        @param result_map: Results Map
        @type result_map: Array of Name Value pairs
        '''
        load_arg = ticket_number
        class_name = "Ticket.Ticket"
        method = "addSubTicket"
        args = [subject, comment]

        response = self.query(load_arg=load_arg,
                              class_name=class_name,
                              method=method,
                              args=args,
                              result_map=result_map)
        return response

    def list_tickets_by_ticket_attributes(self, where_conditions,
                                          attributes=None, limit=None,
                                          offset=None):
        '''
        @summary: List Tickets by Ticket Attributes
        @param where_conditions:Values of where conditions
        @type where_conditions: Array of CTK API objects
        @param attributes: Attributes of CTK Objects
        @type attributes: List or dictionary of attribute name-value pairs
        @param limit: Effective limit on returned query
        @type limit: integer
        @param offset: Effective offset of returned query
        @type offset: integer
        '''
        if attributes is None:
            attributes = ["number"]
        response = self.list(class_name="Ticket.Ticket",
                             where_class="Ticket.TicketWhere",
                             where_conditions=where_conditions,
                             attributes=attributes,
                             limit=limit, offset=offset)
        return response

    def update_ticket(self, ticket_number, attribute_name, attribute_value):
        '''
        @summary: Update Ticket's Attributes
        @param attributeName: The name of the Attribute
        @type attributeName: string
        @param attributeValue: The value of the attribute to be set
        @type attributeValue: The type of the attribute as attributeName
        '''
        response = self.set_attribute(class_name="Ticket.Ticket",
                                      load_arg=ticket_number,
                                      attribute_name=attribute_name,
                                      attribute_value=attribute_value)
        return response

    def add_computer(self, ticket_number, computer):
        '''
        @summary: Add computer to Ticket
        @param ticket_number: Ticket Number
        @type ticket_number: String
        @param computer: Computer
        @type computer: String or CTK Object
        '''
        if isinstance(computer, basestring):
            computer = [computer]
        else:
            computer = CTKObject(computer)
        response = self.query(class_name="Ticket.Ticket",
                              load_arg=ticket_number,
                              method="addComputer",
                              args=computer)
        return response

    def add_message(self, ticket_number, text, source, private=False,
                    source_contact=None, send_message_text=False,
                    contact=None, send_email=True, message_time=None,
                    has_bbcode=False):
        '''
        @summary: Add message to Ticket
        @param ticket_number: Ticket Number
        @type ticket_number: String
        @param text: Message to be added.
        @param source: Where the message was added.
        @param private: Boolean determining if the Contact cannot see it.
        @param source_contact: Who created the message.
        @param send_message_text: Boolean if text should be in email
        @param has_bbcode: Boolean informing ticket renderer there is BBCode
        '''
        args = [text, source, private, source_contact, send_message_text,
                contact, send_email, message_time, has_bbcode]
        response = self.query(class_name="Ticket.Ticket",
                              load_arg=ticket_number,
                              method="addMessage",
                              args=args)
        return response

    def add_work(self, ticket_number, work_type, description, duration,
                 unit_count, fee_waived, contact=None):
        '''
        @summary: Add Work to Ticket
        @param work_type: install, upgrade, etc.
        @type work_type: (WorkType object)
        @param description: Description of work.
        @type description: (str)
        @param duration: The amount of time spent doing work, in minutes
        @type duration: (int)
        @param unit_count: Number of units of work to bill customer
        @type unit_count: (int)
        @param fee_waived: Whether fee should be waived
        @type fee_waived: (bool)
        @param contact: Contact for log - defaults to authenticated user
        '''
        args = [work_type, description, duration, unit_count, fee_waived,
                contact]
        response = self.query(class_name="Ticket.Ticket",
                              load_arg=ticket_number,
                              method="addWork",
                              args=args)
        return response

    def remove_computer(self, ticket_number, computer):
        '''
        @summary: Remove computer from Ticket
        @param ticket_number: Ticket Number
        @type ticket_number: String
        @param computer: Computer
        @type computer: String or CTK Object
        '''
        if isinstance(computer, basestring):
            computer = [computer]
        else:
            computer = CTKObject(computer)
        response = self.query(class_name="Ticket.Ticket",
                              load_arg=ticket_number,
                              method="removeComputer",
                              args=computer)
        return response

    def set_status_by_name(self, ticket_number, status_name):
        '''
        @summary: Set the appropriate status of this ticket based upon the
                    provided status name, if available.
        @param ticket_number: Ticket Number
        @param status_name: The name of the status the ticket should be changed
                    to. (Capitalization matters)
        @type status_name: String
        '''
        response = self.query(class_name="Ticket.Ticket",
                              load_arg=ticket_number,
                              method="setStatusByName",
                              args=[status_name])
        return response

    def get_ticket_details(self, ticket_number, attributes):
        '''
        @summary: Get Ticket Details
        @param ticket_number: Ticket Number
        @type ticket_number: String
        @param attributes: Attribute Details
        @type attributes: List or Dictionary
        '''
        response = self.query(class_name="Ticket.Ticket",
                              load_arg=ticket_number,
                              attributes=attributes)
        return response

    def close_ticket(self, ticket):
        '''
        @summary: Close Ticket
        @param ticket_number: Ticket Number
        @type ticket_number: String
        '''
        status = "Closed"
        ticket = ticket.number
        response = self.set_status_by_name(ticket,
                                           status)
        return response

    def get_ticket_count(self, queue_id, status_types, offset, limit,
                         attributes=None):
        '''
        @param queue_id: Queue id used for finding the ticket count
        @type queue_id: Integer
        @param status_types: status_types of the ticket
        @type status_types: a list
        @param offset: the number of record searching per query
        @type offset: Integer
        @param limit: the maximum number of record displayed per query
        @type limit: Integer
        '''
        load_method = "loadQueueView"
        load_arg = {"id": queue_id, "limit": limit, "offset": offset,
                    "status_types": status_types, "conditions": [
                                    ["has_linux_servers", "=", True]
                                ]}
        response = self.query(class_name="Ticket.Ticket",
                              load_method=load_method,
                              load_arg=load_arg,
                              attributes=attributes,
                              meta="count")
        return response
