from ccengine.clients.base_client import BaseMarshallingClient
from ccengine.common.tools.datagen import rand_name
from ccengine.domain.legacyserv.request.image import CreateImage
from ccengine.domain.legacyserv.request.server import Server
from ccengine.domain.legacyserv.response.image import ImageResponse
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

    def create_next_gen_image(self, server_id, name,
                              requestslib_kwargs=None):
        """
        @summary: Creates next gen snapshot of the server
        @param server_id: The id of an existing server.
        @type server_id: String
        @param: name: The name you want to assign to the image
        @type name: String
        @return: Response Object
        @rtype: Response Object

            POST
            v1.1/{tenant_id}/next_gen_image_requests
        """
        # RM2172: stupid hack to replace v1.0 to v1.1 in url
        url_split = self.url.split('/')
        url_split[3] = 'v1.1'
        self.url = '/'.join(url_split)
        url = '{0}/next_gen_image_requests'.format(self.url)
        create_image_request_object = CreateImage(name, server_id)
        image_action_response = self.request(
            'POST', url,
            request_entity=create_image_request_object,
            response_entity_type=ImageResponse,
            requestslib_kwargs=requestslib_kwargs)
        return image_action_response
