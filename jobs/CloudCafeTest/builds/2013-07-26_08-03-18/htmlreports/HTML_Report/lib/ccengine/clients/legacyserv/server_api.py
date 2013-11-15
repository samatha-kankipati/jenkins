from ccengine.clients.base_client import BaseMarshallingClient
from ccengine.domain.legacyserv.request.server import Server
from ccengine.domain.legacyserv.response.server import ServerResponse


class LegacyServClient(BaseMarshallingClient):

    def __init__(self, url, auth_token, serialize_format=None,
                 deserialize_format=None):
        super(LegacyServClient, self).__init__(serialize_format,
                                               deserialize_format)

        self.url = url
        self.auth_token = auth_token
        self.default_headers['X-Auth-Token'] = auth_token
        self.default_headers['Content-Type'] = 'application/%s' % \
         self.serialize_format
        self.default_headers['Accept'] = 'application/%s' % \
         self.deserialize_format

    # Create Server(Create a Server)
    def create_server(self, name=None, image_id=None, flavor_id=None,
                            requestslib_kwargs=None):

        s = Server(name=name, image_id=image_id, flavor_id=flavor_id)

        url = '%s/servers' % (self.url)
        return self.request('POST', url,
                                  response_entity_type=ServerResponse,
                                  request_entity=s,
                                  requestslib_kwargs=requestslib_kwargs)

    #list server
    def list_server(self, requestslib_kwargs=None):

        url = '%s/servers' % (self.url)
        return self.request('GET', url,
                                  response_entity_type=ServerResponse,
                                  requestslib_kwargs=requestslib_kwargs)

    #list server
    def list_server_id(self, server_id, requestslib_kwargs=None):

        url = '%s/servers/%s' % (self.url, server_id)
        return self.request('GET', url,
                                  response_entity_type=ServerResponse,
                                  requestslib_kwargs=requestslib_kwargs)

    #Delete Server
    def delete_server(self, server_id, requestslib_kwargs=None):
        url = '%s/servers/%s' % (self.url, server_id)
        return self.request('DELETE', url,
                                  requestslib_kwargs=requestslib_kwargs)

