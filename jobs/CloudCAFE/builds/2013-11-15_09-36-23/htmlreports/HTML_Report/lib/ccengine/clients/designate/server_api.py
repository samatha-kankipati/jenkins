from ccengine.clients.base_client import BaseMarshallingClient
from ccengine.domain.designate.request.server import Server
from ccengine.domain.designate.response.server import ServerResponse
from ccengine.domain.designate.response.server import ServerList


class ServerApiClient(BaseMarshallingClient):

    def __init__(self, url, serialize_format=None, deserialize_format=None):
        super(ServerApiClient, self).__init__(serialize_format,
                                              deserialize_format)
        self.url = url
        self.default_headers['Content-Type'] = 'application/{0}'.format(
            self.serialize_format)
        self.default_headers['Accept'] = 'application/{0}'.format(
            self.serialize_format)

    def create_server(self, name=None, requestslib_kwargs=None):
        """
        Create a Server
        CREATE
        v1/servers
        """
        server = Server(name=name)
        url = "{0}/servers".format(self.url)
        return self.request('POST', url, response_entity_type=ServerResponse,
                            request_entity=server,
                            requestslib_kwargs=requestslib_kwargs)

    def update_server(self, server_id, name, requestslib_kwargs=None):
        """
        Update a Server
        UPDATE
        v1/servers/{serversId}
        """
        server = Server(name=name)
        url = "{0}/servers/{1}".format(self.url, server_id)
        return self.request('PUT', url, response_entity_type=ServerResponse,
                            request_entity=server,
                            requestslib_kwargs=requestslib_kwargs)

    def list_servers(self, requestslib_kwargs=None):
        """
        List Servers
        GET
        v1/servers
        """
        url = "{0}/servers".format(self.url)
        return self.request('GET', url, response_entity_type=ServerList,
                            requestslib_kwargs=requestslib_kwargs)

    def get_server(self, server_id, requestslib_kwargs=None):
        """
        Get a  Servers
        GET
        v1/servers/{serversId}
        """
        url = "{0}/servers/{1}".format(self.url,
                                       server_id)
        return self.request('GET', url, response_entity_type=ServerResponse,
                            requestslib_kwargs=requestslib_kwargs)

    def delete_server(self, server_id, requestslib_kwargs=None):
        """
        Delete a  Servers
        DELETE
        v1/servers/{serversId}
        """
        url = "{0}/servers/{1}".format(self.url, server_id)
        return self.request('DELETE', url,
                            requestslib_kwargs=requestslib_kwargs)
