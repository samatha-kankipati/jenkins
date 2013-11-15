from ccengine.clients.base_client import BaseMarshallingClient
from ccengine.domain.flow.request.flow_request import TicketRequest
from ccengine.domain.flow.response.queues import AllQueueViews
from ccengine.domain.flow.response.ticket import AllTicketsresponse


class FlowAPIClient(BaseMarshallingClient):
    """
    Client for Flow API
    """
    def __init__(self, url, auth_token, serialize_format=None,
                 deserialize_format=None):

        super(FlowAPIClient, self).__init__(serialize_format,
                                            deserialize_format)
        self.auth_token = auth_token
        self.default_headers['RX-AUTH-TOKEN'] = self.auth_token
        self.url = url

    def get_tickets(self, core_view_id=None,
                    zendesk_view_id=None, cloud_view_id=None):
        """
        @summary: Returns a list of tickets for the queue views.
        @returntype: List
        @param core_view_id: view id for core queues .
        @type core_view_id:List
        @param zendesk_view_id: view id for zendesk groups
        @type zendesk_view_id: List
        @param cloud_view_id: View id for cloud queue
        @type: Integer
        """
        url = "{0}/allthetickets.json".format(self.url)
        get_ticket_request = TicketRequest(
            queue=core_view_id, group=zendesk_view_id,
            cloud_queue=cloud_view_id)
        response = self.request('POST', url,
                                response_entity_type=AllTicketsresponse,
                                request_entity=get_ticket_request)
        return response

    def get_queue_views(self):
        """
        @summary: Returns a list of all types of queue views
        @returntype: List
        """
        url = "{0}/awesomeSauce.json".format(self.url)
        response = self.request('GET', url, response_entity_type=AllQueueViews)
        return response
