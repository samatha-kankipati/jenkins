from urlparse import urlparse

from ccengine.clients.base_client import BaseMarshallingClient
from ccengine.common.tools.datagen import rand_name
from ccengine.common.tools.datatools import nested_getattr
from ccengine.domain.lefty.request.lefty_request import CreateTicketRequest,\
    UpdateTicketRequest, CreateCategorySubCategoryRequest,\
    QueueQuery, QueueSort, CreateQueueRequest
from ccengine.domain.lefty.response.lefty import Ticket, Category,\
    Subcategory, Queue, Statuses, PubSub


class LeftyAPITicketClient(BaseMarshallingClient):

    def __init__(self, url, auth_token, serialize_format=None,
                 deserialize_format=None):

        super(LeftyAPITicketClient, self).__init__(serialize_format,
                                                   deserialize_format)
        self.auth_token = auth_token
        self.default_headers['X-Auth-Token'] = auth_token
        ct = ''.join(['application/', self.serialize_format])
        accept = ''.join(['application/', self.deserialize_format])
        self.default_headers['Content-Type'] = ct
        self.default_headers['Accept'] = accept
        self.url = url

    def list_tickets(self, account_id):
        '''
            @summary: Returns a list of tickets for the Account.
            @return type: List
            @param: account_id
            @param desc: Account id for which the tickets needs to be fetched.
            @param type: String
        '''
        url = '{0}/accounts/{1}/tickets'.format(self.url, account_id)

        lefty_response = self.request('GET', url,
                                      response_entity_type=Ticket)
        return lefty_response

    def create_ticket(self, account_id, subject, description, category_id,
                      sub_category_id, comment=None):
        '''
            @summary: Creates a ticket for the Account.
            @return type: Response Object
            @param: account_id
            @param desc: Account id for which the ticket needs to be created.
            @param type: String
            @param: subject
            @param desc: Subject for the ticket.
            @param type: String
            @param: description
            @param desc: Description for the ticket.
            @param type: String
            @param: category_id
            @param desc: ID of the Category for the ticket.
            @param type: Integer
            @param: sub_category_id
            @param desc: ID of the SubCategory for the ticket.
            @param type: Integer
            @param: comments
            @param desc: Public/Private comments for the ticket.
            @param type: String
        '''

        url = '{0}/accounts/{1}/tickets'.format(self.url, account_id)

        create_ticket_request_obj =\
            CreateTicketRequest(subject=subject, description=description,
                                category_id=category_id,
                                sub_category_id=sub_category_id,
                                comment=comment)

        lefty_response = self.request('POST', url, request_entity=
                                      create_ticket_request_obj,
                                      response_entity_type=Ticket)
        return lefty_response

    def update_ticket(self, account_id, ticket_id, priority=None,
                      assignee=None, rating=None, tags=None, products=None,
                      recipients=None, status=None, comment=None,
                      is_comment_public=False, category_id=None,
                      sub_category_id=None, subject=None,
                      description=None, group=None, difficulty=None,
                      severity=None):
        '''
            @summary: Updates a ticket for the Account.
            @return type: Response Object
            @param: ticket_id
            @param desc: ID of the ticket that needs to be updated.
            @param type: String
            @param: account_id
            @param desc: Account id for which the ticket needs to be created.
            @param type: String
            @param: subject
            @param desc: Subject for the ticket.
            @param type: String
            @param: priority
            @param desc: Priority for the ticket.
            @param type: String
            @param: assignee
            @param desc: Assignee for the ticket.
            @param type: String
            @param: recipients
            @param desc: Recipients for the ticket.
            @param type: String
            @param: rating
            @param desc: Rating for the ticket.
            @param type: String
            @param: tags
            @param desc: Tags for the ticket.
            @param type: String
            @param: products
            @param desc: Products for the ticket.
            @param type: String
            @param: is_comment_public
            @param desc: Boolean to mark public comment for the ticket.
            @param type: Boolean
            @param: status
            @param desc: Status for the ticket.
            @param type: String
            @param: description
            @param desc: Description for the ticket.
            @param type: String
            @param: category_id
            @param desc: ID of the Category for the ticket.
            @param type: Integer
            @param: sub_category_id
            @param desc: ID of the SubCategory for the ticket.
            @param type: Integer
            @param: comments
            @param desc: Public/Private comments for the ticket.
            @param type: String
            @param: subject
            @param desc: Subject for the ticket.
            @param type: String
            @param: description
            @param desc: Description for the ticket.
            @param type: String
            @param: group
            @param desc: Group for the ticket.
            @param type: String
            @param: difficulty
            @param desc: Difficulty for the ticket.
            @param type: String
        '''

        new_recipient_list = None
        if comment is not None:
            comment = {"text": comment, "is_public": is_comment_public}
        if assignee is not None:
            assignee = {"type": "racker", "value": assignee}
        if recipients is not None:
            new_recipient_list = []
            for recipient in recipients:
                new_recipient_list.append(
                    {"type": "racker", "value": recipient}
                )

        url = '{0}/accounts/{1}/tickets/{2}'.format(self.url, account_id,
                                                    ticket_id)

        update_ticket_request_obj = \
            UpdateTicketRequest(
                priority=priority,
                assignee=assignee,
                rating=rating,
                tags=tags,
                products=products,
                recipients=new_recipient_list,
                status=status,
                comment=comment,
                category_id=category_id,
                sub_category_id=sub_category_id,
                subject=subject,
                description=description,
                group=group,
                difficulty=difficulty,
                severity=severity)

        lefty_response = self.request('PUT', url, request_entity=
                                      update_ticket_request_obj,
                                      response_entity_type=Ticket)
        return lefty_response

    def get_ticket(self, account_id, ticket_id):
        '''
            @summary: Retrieves the details of a ticket for an Account.
            @return type: Response Object
            @param: ticket_id
            @param desc: ID of the ticket that needs to be fetched.
            @param type: String
            @param: account_id
            @param desc: Account id for which the ticket needs to be created.
            @param type: String
        '''
        url = '{0}/accounts/{1}/tickets/{2}'.format(self.url,
                                                    account_id,
                                                    ticket_id)

        lefty_response = self.request('GET', url,
                                      response_entity_type=Ticket)
        return lefty_response

    def search_events_by_attribute(self, event_list, attribute, attribute_val):
        '''
            @summary: Searches an event by the attribute provided.
            @return type: List of Found Events
            @param: event_list
            @param desc: List of all the events.
            @param type: List
            @param: attribute
            @param desc: Search attibute for events.
            @param type: String
            @param: attribute_val
            @param desc: Value for the Search attibute provided for events.
            @param type: String
        '''
        found_events = []
        found_events = [event for event in event_list
                        if (hasattr(event, attribute) and
                            getattr(event, attribute) == attribute_val)]
        return found_events


class LeftyAPICategrySubCategoryClient(BaseMarshallingClient):

    def __init__(self, url, auth_token, serialize_format=None,
                 deserialize_format=None):

        super(LeftyAPICategrySubCategoryClient, self).\
            __init__(serialize_format, deserialize_format)

        self.auth_token = auth_token
        self.default_headers['X-Auth-Token'] = auth_token
        ct = ''.join(['application/', self.serialize_format])
        accept = ''.join(['application/', self.deserialize_format])
        self.default_headers['Content-Type'] = ct
        self.default_headers['Accept'] = accept
        self.url = url

    def list_categories(self):
        '''
            @summary: Lists all the categories available
            @return type: Response Object
        '''

        url = '{0}/categories'.format(self.url)

        lefty_response = self.request('GET', url,
                                      response_entity_type=Category)
        return lefty_response

    def create_category(self, name):
        '''
            @summary: Creates a new category.
            @return type: Response Object
            @param: name
            @param desc: Name for the new category to be created.
            @param type: String
        '''

        url = '{0}/categories'.format(self.url)

        create_category_req = CreateCategorySubCategoryRequest(name=name)

        lefty_response = self.request('POST', url,
                                      request_entity=create_category_req,
                                      response_entity_type=Category)
        return lefty_response

    def get_category(self, category_id):
        '''
            @summary: Fetches the details of a specific category.
            @return type: Response Object
            @param: category_id
            @param desc: ID of the category to be fecthed
            @param type: String
        '''

        url = '{0}/categories/{1}'.format(self.url, category_id)

        lefty_response = self.request('GET', url,
                                      response_entity_type=Category)
        return lefty_response

    def list_sub_categories(self, category_id):
        '''
            @summary: Fetches the list of Subcategories for a category.
            @return type: Response Object
            @param: category_id
            @param desc: ID of the category for which the Subcategories to be
                         listed.
            @param type: String
        '''

        url = '{0}/categories/{1}/sub_categories'.format(self.url, category_id)

        lefty_response = self.request('GET', url,
                                      response_entity_type=Subcategory)
        return lefty_response

    def create_sub_category(self, category_id, name):
        '''
            @summary: Creates a new Subcategory for a category.
            @return type: Response Object
            @param: category_id
            @param desc: ID of the category for which the Subcategory to be
                         created.
            @param type: String
            @param: name
            @param desc: Name for the new Subcategory
            @param type: String
        '''

        url = '{0}/categories/{1}/sub_categories'.format(self.url, category_id)

        create_sub_category_req = CreateCategorySubCategoryRequest(name=name)

        lefty_response = self.request('POST', url,
                                      request_entity=create_sub_category_req,
                                      response_entity_type=Subcategory)
        return lefty_response

    def get_sub_category(self, category_id, sub_category_id):
        '''
            @summary: Fetches the details of a Subcategory for a category.
            @return type: Response Object
            @param: category_id
            @param desc: ID of the category for which the Subcategories to be
                         listed.
            @param type: String
            @param: sub_category_id
            @param desc: ID of the Subcategory.
            @param type: String
        '''

        url = '{0}/categories/{1}/sub_categories/{2}'.format(self.url,
                                                             category_id,
                                                             sub_category_id)

        lefty_response = self.request('GET', url,
                                      response_entity_type=Subcategory)
        return lefty_response

    def delete_category(self, category_id):
        '''
            @summary: Deletes a category.
            @return type: Response Object
            @param: category_id
            @param desc: ID of the category to be deleted.
            @param type: String
        '''
        url = '{0}/categories/{1}'.format(self.url, category_id)

        lefty_response = self.request('DELETE', url,
                                      response_entity_type=Category)
        return lefty_response

    def delete_sub_category(self, category_id, sub_category_id):
        '''
            @summary: Deletes a Subcategory.
            @return type: Response Object
            @param: category_id
            @param desc: ID of the category the sub category belongs to.
            @param type: String
            @param: sub_category_id
            @param desc: ID of the Subcategory to be deleted.
            @param type: String
        '''

        url = '{0}/categories/{1}/sub_categories/{2}'.format(self.url,
                                                             category_id,
                                                             sub_category_id)

        lefty_response = self.request('DELETE', url,
                                      response_entity_type=Category)
        return lefty_response


class LeftyAPIQueueClient(BaseMarshallingClient):

    def __init__(self, url, auth_token, serialize_format=None,
                 deserialize_format=None):

        super(LeftyAPIQueueClient, self).__init__(serialize_format,
                                                  deserialize_format)
        self.auth_token = auth_token
        self.default_headers['X-Auth-Token'] = auth_token
        ct = ''.join(['application/', self.serialize_format])
        accept = ''.join(['application/', self.deserialize_format])
        self.default_headers['Content-Type'] = ct
        self.default_headers['Accept'] = accept
        self.url = url

    def create_queue(self, name, description, query_occurrence, query_type,
                     query_property, query_text, sort_property, sort_order):
        '''
            @summary: Creates a new Queue.
            @return: Response Object
            @param: name
            @param desc: Name of the Queue
            @param type: String
            @param: query_occurrence
            @param desc: Query Occurance for the new Queue
            @param type: String
            @param: query_type
            @param desc: Queue Type for the Queue
            @param type: String
            @param: query_property
            @param desc: Query property for the Queue
            @param type: String
            @param: query_text
            @param desc: Query Text for the Queue
            @param type: String
            @param: sort_property
            @param desc: Sort property for the Queue
            @param type: String
            @param: sort_order
            @param desc: Sort order of tickets for the Queue
            @param type: String
        '''
        url = '{0}/queues'.format(self.url)

        queue_query_request = QueueQuery(query_occurrence, query_type,
                                         query_property, query_text)

        queue_sort_request = QueueSort(sort_property, sort_order)

        create_queue_request = CreateQueueRequest(name, queue_query_request,
                                                  queue_sort_request,
                                                  description)

        lefty_response = self.request('POST', url, request_entity=
                                      create_queue_request,
                                      response_entity_type=Queue)
        return lefty_response

    def get_queue(self, queue_id):
        '''
            @summary: Retrieves the details of a Queue.
            @param: queue_id
            @param desc: ID of the Queue to be fetched
            @param type: String
        '''
        url = '{0}/queues/{1}'.format(self.url, queue_id)

        lefty_response = self.request('GET', url, response_entity_type=Queue)

        return lefty_response

    def get_tickets_for_a_queue(self, queue_id):
        '''
            @summary: Retrieves the list of Tickets for a Queue.
            @param: queue_id
            @param desc: ID of the Queue for which the tickets to be fetched
            @param type: String
        '''

        url = '{0}/queues/{1}/tickets'.format(self.url, queue_id)

        lefty_response = self.request('GET', url, response_entity_type=Queue)

        return lefty_response


class LeftyAPIStatusesClient(BaseMarshallingClient):

    def __init__(self, url, auth_token, serialize_format=None,
                 deserialize_format=None):

        super(LeftyAPIStatusesClient, self).__init__(serialize_format,
                                                     deserialize_format)
        self.auth_token = auth_token
        self.default_headers['X-Auth-Token'] = auth_token
        ct = ''.join(['application/', self.serialize_format])
        accept = ''.join(['application/', self.deserialize_format])
        self.default_headers['Content-Type'] = ct
        self.default_headers['Accept'] = accept
        self.url = url

    def get_statuses(self):
        '''
            @summary: Retrives the list of available Statues.
        '''
        url = '{0}/statuses'.format(self.url)

        lefty_response = self.request('GET', url,
                                      response_entity_type=Statuses)

        return lefty_response


class PubSubClient(BaseMarshallingClient):

    def __init__(self, url, auth_token, serialize_format=None,
                 deserialize_format=None):

        super(PubSubClient, self).__init__(serialize_format,
                                           deserialize_format)
        self.auth_token = auth_token
        self.default_headers['X-Auth-Token'] = auth_token
        ct = ''.join(['application/', self.serialize_format])
        accept = ''.join(['application/', self.deserialize_format])
        self.default_headers['Content-Type'] = ct
        self.default_headers['Accept'] = accept
        self.url = url

    def search_events_by_attribute(self, attribute, attr_value, since_value):
        '''
            @summary: Retrives the list of events based on search params.
            @param: attribute.
            @param type: String.
            @param desc: Search attribute name.
            @param: attr_value.
            @param type: String.
            @param desc: Search attribute value.
            @param: since.
            @param type: String.
            @param desc: Time since when all the events should be retrieved.
        '''
        found_events = []
        all_events = self.get_all_events_by_since(since_value).entity
        for event in all_events:
            if nested_getattr(event, attribute) == attr_value:
                found_events.append(event)
        return found_events

    def get_all_events_by_since(self, since_value):
        '''
            @summary: Retrives the list of events based on since param.
            @param: since.
            @param type: String.
            @param desc: Time since when all the events should be retrieved.
        '''
        url = '{0}/subscribe'.format(self.url)
        params = {"since": since_value}
        events = self.request('GET', url, params=params,
                              response_entity_type=PubSub)

        return events
