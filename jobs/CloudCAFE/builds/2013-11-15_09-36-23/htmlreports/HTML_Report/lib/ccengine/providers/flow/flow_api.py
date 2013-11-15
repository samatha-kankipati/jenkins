from ccengine.providers.auth.auth_api import AuthProvider as _AuthProvider
from ccengine.providers.base_provider import BaseProvider
from ccengine.clients.flow.flow_api import FlowAPIClient


class FlowAPIProvider(BaseProvider):

    def __init__(self, config):
        super(FlowAPIProvider, self).__init__()
        if config is None:
            self.client_log.warning('empty (=None) config recieved in init')
            # Load configuration from default.conf
            self.config = _AuthProvider
        else:
            self.config = config
        # Get Auth Info
        self.auth_provider = _AuthProvider(self.config)

        # GET Auth Token
        self.auth_token = self.auth_provider.authenticate()
        self.url = self.config.auth.base_url
        self.flow_client = FlowAPIClient(self.url, self.auth_token,
                                         self.config.misc.serializer,
                                         self.config.misc.deserializer)

    def search_tickets_in_queue_views(self, ticket_number, core_view_id=None,
                                      zendesk_view_id=None,
                                      cloud_view_id=None):
        """
        @summary: Searches the ticket by ticket number provided
        @returntype: Ticket object
        @param core_view_id: view id for core queues .
        @type core_view_id:List
        @param zendesk_view_id: view id for zendesk groups
        @type zendesk_view_id: List
        @param cloud_view_id: View id for cloud queue
        @type cloud_view_id:List
        @param ticket_number: Ticket number to be searched
        @type ticket_number: String or Integer
        """
        tickets_list = self.flow_client.get_tickets(
            core_view_id, zendesk_view_id, cloud_view_id).entity
        for ticket in tickets_list.list:
            if str(ticket.number).lower() == str(ticket_number).lower():
                return ticket

    def search_in_my_tickets(self, ticket_number):
        """
        @summary: searches ticket in My Ticket list
        @returntype: Ticket object
        @param ticket_number: ticket number to be searched
        @type ticket_number: String or Integer
        """
        tickets_list = self.flow_client.get_tickets().entity
        for ticket in tickets_list.my_tickets:
            if str(ticket.number).lower() == str(ticket_number).lower():
                return ticket
