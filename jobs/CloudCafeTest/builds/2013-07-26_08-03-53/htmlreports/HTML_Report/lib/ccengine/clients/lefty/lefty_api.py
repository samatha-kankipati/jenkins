import time
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
        """
            @summary: Returns a list of tickets for the Account.
            @returntype: List
            @param account_id: Account id for which the tickets needs
                               to be fetched.
            @type account_id: String
        """
        url = '{0}/accounts/{1}/tickets'.format(self.url, account_id)

        lefty_response = self.request('GET', url,
                                      response_entity_type=Ticket)
        return lefty_response

    def create_ticket(self, account_id, subject, description, category_id,
                      sub_category_id, comment=None):
        """
            @summary: Creates a ticket for the Account.
            @returntype: Response Object
            @param account_id:Account id for which the ticket needs
                              to be created.
            @type account_id: String
            @param subject: Subject for the ticket.
            @type subject: String
            @param description: Description for the ticket.
            @type description: String
            @param category_id: ID of the Category for the ticket.
            @type category_id: Integer
            @param sub_category_id: ID of the SubCategory for the ticket.
            @type sub_category_id: Integer
            @param comments: Public/Private comments for the ticket.
            @type comments: String
        """

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
        """
            @summary: Updates a ticket for the Account.
            @returntype: Response Object
            @param ticket_id: ID of the ticket that needs to be updated.
            @type ticket_id: String
            @param account_id: Account id for which the ticket
                               needs to be created.
            @type account_id: String
            @param subject: Subject for the ticket.
            @type subject: String
            @param priority: Priority for the ticket.
            @type priority: String
            @param assignee: Assignee for the ticket.
            @type assignee: String
            @param recipients: Recipients for the ticket.
            @type recipients: String
            @param rating: Rating for the ticket.
            @type rating: String
            @param tags: Tags for the ticket.
            @type tags: String
            @param products: Products for the ticket.
            @type products: String
            @param is_comment_public: Boolean to mark public comment for the ticket.
            @type is_comment_public: Boolean
            @param status: Status for the ticket.
            @type status: String
            @param description: Description for the ticket.
            @type description: String
            @param category_id: ID of the Category for the ticket.
            @type category_id: Integer
            @param sub_category_id: ID of the SubCategory for the ticket.
            @type sub_category_id: Integer
            @param comments: Public/Private comments for the ticket.
            @type comments: String
            @param subject: Subject for the ticket.
            @type subject: String
            @param description: Description for the ticket.
            @type description: String
            @param group: Group for the ticket.
            @type group: String
            @param difficulty: Difficulty for the ticket.
            @type difficulty: String
        """

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

    def get_ticket(self, account_id, ticket_id, data_centre_url=None):
        """
            @summary: Retrieves the details of a ticket for an Account.
            @returntype: Response Object
            @param ticket_id: ID of the ticket that needs to be fetched.
            @type ticket_id: String
            @param account_id: Account id for which the ticket needs to be created.
            @type account_id: String
        """
        base_url = data_centre_url or self.url
        url = '{0}/accounts/{1}/tickets/{2}'.format(base_url, account_id,
                                                    ticket_id)

        lefty_response = self.request('GET', url,
                                      response_entity_type=Ticket)
        return lefty_response

    def search_events_by_attribute(self, event_list, attribute, attribute_val):
        """
            @summary: Searches an event by the attribute provided.
            @returntype: List of Found Events
            @param event_list: List of all the events.
            @type event_list: List
            @param attribute: Search attibute for events.
            @type attribute: String
            @param attribute_val: Value for the Search attibute provided for events.
            @type attribute_val: String
        """
        found_events = []
        found_events = [event for event in event_list
                        if (hasattr(event, attribute) and
                            getattr(event, attribute) == attribute_val)]
        return found_events

    def wait_for_ticket_to_sync_in_data_centre(self, data_centre_url,
                                               last_updated, account_id=None,
                                               ticket_id=None):
        """
            @summary: Waits for ticket to be synced
            @returntype: None
            @param data_centre_url: URL of the data centre where data should be synced.
            @type data_centre_url: String
            @param last_updated: last_updated time of the ticket.
            @type last_updated: String
            @param account_id: account_id to which the ticket belongs.
            @type account_id: String
            @param ticket_id: ID of the created/updated ticket.
            @type ticket_id: String            
        """
        time_to_wait = time.time() + 60*1
        current_time = time.time()
        while current_time < time_to_wait:
            wait_response = self.get_ticket(account_id, ticket_id,
                                            data_centre_url)
            if wait_response.status_code == 200 and \
                    wait_response.entity.last_updated == last_updated:
                break
            else:
                current_time = time.time()
        else:
            raise Exception("The ticket did not get sync across data centres")


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
        """
            @summary: Lists all the categories available
            @returntype: Response Object
        """

        url = '{0}/categories'.format(self.url)

        lefty_response = self.request('GET', url,
                                      response_entity_type=Category)
        return lefty_response

    def create_category(self, name):
        """
            @summary: Creates a new category.
            @returntype: Response Object
            @param name: Name for the new category to be created.
            @type name: String
        """

        url = '{0}/categories'.format(self.url)

        create_category_req = CreateCategorySubCategoryRequest(name=name)

        lefty_response = self.request('POST', url,
                                      request_entity=create_category_req,
                                      response_entity_type=Category)
        return lefty_response

    def get_category(self, category_id, data_centre_url=None):
        """
            @summary: Fetches the details of a specific category.
            @returntype: Response Object
            @param category_id: ID of the category to be fecthed
            @type category_id: String
            @param data_centre_url: end point for the data center where
                                    the category belongs
            @type data_centre_url: String
        """
        base_url = data_centre_url or self.url
        url = '{0}/categories/{1}'.format(base_url, category_id)

        lefty_response = self.request('GET', url,
                                      response_entity_type=Category)
        return lefty_response

    def list_sub_categories(self, category_id):
        """
            @summary: Fetches the list of Subcategories for a category.
            @returntype: Response Object
            @param category_id: ID of the category for which the Subcategories to be
                         listed.
            @type category_id: String
        """

        url = '{0}/categories/{1}/sub_categories'.format(self.url, category_id)

        lefty_response = self.request('GET', url,
                                      response_entity_type=Subcategory)
        return lefty_response

    def create_sub_category(self, category_id, name):
        """
            @summary: Creates a new Subcategory for a category.
            @returntype: Response Object
            @param category_id: ID of the category for which the Subcategory
                                to be created.
            @type category_id: String
            @param name: Name for the new Subcategory
            @type name: String
        """

        url = '{0}/categories/{1}/sub_categories'.format(self.url, category_id)

        create_sub_category_req = CreateCategorySubCategoryRequest(name=name)

        lefty_response = self.request('POST', url,
                                      request_entity=create_sub_category_req,
                                      response_entity_type=Subcategory)
        return lefty_response

    def get_sub_category(self, category_id, sub_category_id,
                         data_centre_url=None):
        """
            @summary: Fetches the details of a Subcategory for a category.
            @returntype: Response Object
            @param category_id: ID of the category for which the
                                Subcategories to be listed.
            @type category_id: String
            @param sub_category_id: ID of the Subcategory.
            @type sub_category_id: String
        """

        base_url = data_centre_url or self.url
        url = '{0}/categories/{1}/sub_categories/{2}'.format(base_url,
                                                             category_id,
                                                             sub_category_id)

        lefty_response = self.request('GET', url,
                                      response_entity_type=Subcategory)
        return lefty_response

    def delete_category(self, category_id):
        """
            @summary: Deletes a category.
            @returntype: Response Object
            @param category_id: ID of the category to be deleted.
            @type category_id: String
        """
        url = '{0}/categories/{1}'.format(self.url, category_id)

        lefty_response = self.request('DELETE', url,
                                      response_entity_type=Category)
        return lefty_response

    def delete_sub_category(self, category_id, sub_category_id):
        """
            @summary: Deletes a Subcategory.
            @returntype: Response Object
            @param category_id: ID of the category the sub category belongs to.
            @type category_id: String
            @param sub_category_id: ID of the Subcategory to be deleted.
            @type sub_category_id: String
        """

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
        """
            @summary: Creates a new Queue.
            @returns: Response Object
            @param name: Name of the Queue
            @type name: String
            @param query_occurrence: Query Occurance for the new Queue
            @type query_occurrence: String
            @param query_type: Queue Type for the Queue
            @type query_type: String
            @param query_property: Query property for the Queue
            @type query_property: String
            @param query_text: Query Text for the Queue
            @type query_text: String
            @param sort_property: Sort property for the Queue
            @type sort_property: String
            @param sort_order: Sort order of tickets for the Queue
            @type sort_order: String
        """
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

    def get_queue(self, queue_id, data_centre_url=None):
        """
            @summary: Retrieves the details of a Queue.
            @returntype: Queue Object
            @param queue_id: ID of the Queue to be fetched
            @type queue_id: String
        """
        base_url = data_centre_url or self.url
        url = '{0}/queues/{1}'.format(base_url, queue_id)

        lefty_response = self.request('GET', url, response_entity_type=Queue)

        return lefty_response

    def get_tickets_for_a_queue(self, queue_id):
        """
            @summary: Retrieves the list of Tickets for a Queue.
            @returntype: List
            @param queue_id: ID of the Queue for which the tickets to be fetched
            @type queue_id: String
        """

        url = '{0}/queues/{1}/tickets'.format(self.url, queue_id)

        lefty_response = self.request('GET', url, response_entity_type=Queue)

        return lefty_response

    def delete_queue(self, queue_id):
        """
            @summary: Deletes a Queue.
            @returntype: Queue Object
            @param queue_id: ID of the Queue which is to be deleted
            @type queue_id: String
        """

        url = '{0}/queues/{1}'.format(self.url, queue_id)

        lefty_response = \
            self.request('DELETE', url, response_entity_type=Queue)

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
        """
            @summary: Retrives the list of available Statues.
            @returntype: Status Object
        """
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
        """
            @summary: Retrives the list of events based on search params.
            @returntype: List
            @type attribute: String.
            @param attribute: Search attribute name.
            @type attr_value: String.
            @param attr_value: Search attribute value.
            @type since: String.
            @param since: Time since when all the events should be retrieved.
        """
        found_events = []
        all_events = self.get_all_events_by_since(since_value).entity
        for event in all_events:
            if nested_getattr(event, attribute) == attr_value:
                found_events.append(event)
        return found_events

    def get_all_events_by_since(self, since_value):
        """
            @summary: Retrives the list of events based on since param.
            @returntype: List
            @type since: String.
            @param since: Time since when all the events should be retrieved.
        """
        url = '{0}/subscribe'.format(self.url)
        params = {"since": since_value}
        events = self.request('GET', url, params=params,
                              response_entity_type=PubSub)

        return events
