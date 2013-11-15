from urlparse import urljoin
from ccengine.clients.base_client import BaseMarshallingClient


class ImagesAPIClient(BaseMarshallingClient):

    '''
    Client for Image API
    '''

    def __init__(self, url, auth_token,
                 serialize_format=None, deserialize_format=None):
        super(ImagesAPIClient, self).__init__(serialize_format,
                                              deserialize_format)
        self.auth_token = auth_token
        self.default_headers['X-Auth-Token'] = auth_token
        self.default_headers['Content-Type'] = 'application/{0}'.format(
            self.serialize_format)
        self.default_headers['Accept'] = 'application/{0}'.format(
            self.deserialize_format)
        # Url needs a trailing '/' for urljoin to work
        self.url = "{0}/".format(url)

    def list_images(self):
        '''
        @summary: List all the available legacy images.
        '''

        '''
        GET
        /images
        '''
        url = urljoin(self.url, "images")
        server_response = self.request("GET", url=url)
        return server_response
