from ccengine.clients.core.core_api import CoreAPIClient


class QueueAPIClient(CoreAPIClient):
    '''
    Client for ticket related queries in CTK API
    '''
    def __init__(self, url, auth_token, serialize_format=None,
                 deserialize_format=None):
        super(QueueAPIClient, self).__init__(url, auth_token,
                                             serialize_format,
                                             deserialize_format)

    def list_subcategories_by_queue_query(self, queue_id):
        '''
        @param queue: Queue on which ticket is to be created
        @type queue: String
        @param result_map: Results Map
        @type: Array of Name Value pairs
        '''
        class_name = "Ticket.Queue"
        method = "getSubcategories"
        load_arg = queue_id
        response = self.query(load_arg=load_arg,
                              class_name=class_name,
                              method=method)
        return response

    def get_queue_attributes(self, queue_id, attributes=None):
        '''
        @param queue_id: Queue details to be verified
        @type queue_id: integer
        '''
        class_name = "Ticket.Queue"
        load_arg = queue_id
        attributes = ["id", "name", "all_categories", "all_statuses",
                      "categories", "default_category", "description",
                      "displayable_categories", "email", "groups",
                      "inactive_categories", "inactive_statuses",
                      "priorities", "roles", "sources", "statuses",
                      "transfer_queues", "work_types"]
        response = self.query(load_arg=load_arg,
                              class_name=class_name,
                              attributes=attributes)
        return response

    def get_queue_attributes_using_queuewhere(self, where_conditions,
                                              attribute=None, limit=None,
                                              offset=None):
        '''
        @summary: Get Attributes of an Queue
        @param where_conditions: Values of where conditions
        @type where_conditions: Array of CTK API objects
        @param attributes: Attributes of CTK Objects
        @type attributes: List or dictionary of attribute name-value pairs
        @param limit: Effective limit on returned query
        @type limit: integer
        @param offset: Effective offset of returned query
        @type offset: integer
        '''
        if attribute is None:
            attribute = ["id"]
        class_name = "Ticket.Queue"
        response = self.list(class_name=class_name,
                             where_class="Ticket.QueueWhere",
                             where_conditions=where_conditions,
                             attributes=attribute,
                             limit=limit, offset=offset)
        return response

    def get_queue_attribute(self, load_value, attribute=None):
        '''
        @summary: Get Attribute value of an Queue class
        @param attribute: Attributes of Ticket.Queue
        @type attribute: String
        @param load_value: Queue id
        @type load_value: Integer
        '''
        if attribute is None:
            attribute = ["id"]
        response = self.get_attribute(class_name="Ticket.Queue",
                                      load_value=load_value,
                                      attribute=attribute)
        return response
