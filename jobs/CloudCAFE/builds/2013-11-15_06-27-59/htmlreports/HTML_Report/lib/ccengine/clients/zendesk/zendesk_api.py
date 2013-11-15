from ccengine.clients.base_client import BaseMarshallingClient
from ccengine.domain.zendesk.request.zendesk_ticket_requests import \
    CreateTicketRequest, UpdateTicketRequest
from ccengine.domain.zendesk.response.zendesk_ticket_response import \
    ZendeskTicketResponse


class ZendeskTicketClient(BaseMarshallingClient):

    def __init__(self, url, basic_auth, serialize_format=None,
                 deserialize_format=None):
        super(ZendeskTicketClient, self).__init__(serialize_format,
                                                  deserialize_format)
        self.url = url
        ct = "application/{0}".format(self.serialize_format)
        accept = "application/{0}".format(self.deserialize_format)
        self.default_headers['Content-Type'] = ct
        self.default_headers['Accept'] = accept
        self.url = url
        self.auth = basic_auth

    def create_ticket(self, group_id, subject, comment_body, status=None,
                      assignee_id=None, priority=None, tags=None):

        url = '{0}tickets.json'.format(self.url)
        create_tkt_request = CreateTicketRequest(
            group_id=group_id, subject=subject, comment_body=comment_body,
            assignee_id=assignee_id, priority=priority,
            status=status, tags=tags)

        all_tkt_resp = self.request(
            'POST', url, request_entity=create_tkt_request,
            response_entity_type=ZendeskTicketResponse,
            requestslib_kwargs={'auth': self.auth})
        return all_tkt_resp

    def update_ticket(self, ticket_number, status=None, priority=None,
                      assignee_id=None, tags=None):
        url = '{0}tickets/{1}.json'.format(self.url, ticket_number)
        update_ticket_request = UpdateTicketRequest(
            status=status, tags=tags, priority=priority,
            assignee_id=assignee_id)
        update_tkt_resp = self.request(
            'PUT', url, request_entity=update_ticket_request,
            requestslib_kwargs={'auth': self.auth})
        return update_tkt_resp
