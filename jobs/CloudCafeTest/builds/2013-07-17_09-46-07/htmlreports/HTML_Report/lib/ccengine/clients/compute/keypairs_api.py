from ccengine.clients.base_client import BaseMarshallingClient
from ccengine.domain.compute.request.keypair_requests import CreateKeypair
from ccengine.domain.compute.response.keypair import Keypair, Keypairs


class KeypairsClient(BaseMarshallingClient):

    def __init__(self, url, auth_token, serialize_format=None,
                 deserialize_format=None):
        """
        @param url: Base URL for the compute service
        @type url: String
        @param auth_token: Auth token to be used for all requests
        @type auth_token: String
        @param serialize_format: Format for serializing requests
        @type serialize_format: String
        @param deserialize_format: Format for de-serializing responses
        @type deserialize_format: String
        """
        super(KeypairsClient, self).__init__(serialize_format,
                                             deserialize_format)
        self.auth_token = auth_token
        self.default_headers['X-Auth-Token'] = auth_token
        ct = ''.join(['application/', self.serialize_format])
        accept = ''.join(['application/', self.deserialize_format])
        self.default_headers['Content-Type'] = ct
        self.default_headers['Accept'] = accept
        self.url = url

    def create_keypair(self, name, public_key=None, requestslib_kwargs=None):
        request = CreateKeypair(name=name, public_key=public_key)

        url = '{base_url}/os-keypairs'.format(base_url=self.url)
        resp = self.request('POST', url,
                            response_entity_type=Keypair,
                            request_entity=request,
                            requestslib_kwargs=requestslib_kwargs)
        return resp

    def get_keypair(self, keypair_name, requestslib_kwargs=None):

        url = '{base_url}/os-keypairs/{name}'.format(base_url=self.url,
                                                     name=keypair_name)
        resp = self.request('GET', url,
                            response_entity_type=Keypair,
                            requestslib_kwargs=requestslib_kwargs)
        return resp

    def list_keypairs(self, requestslib_kwargs=None):

        url = '{base_url}/os-keypairs'.format(base_url=self.url)
        resp = self.request('GET', url,
                            response_entity_type=Keypairs,
                            requestslib_kwargs=requestslib_kwargs)
        return resp

    def delete_keypair(self, keypair_name, requestslib_kwargs=None):
        url = '{base_url}/os-keypairs/{name}'.format(base_url=self.url,
                                                     name=keypair_name)
        resp = self.request('DELETE', url,
                            requestslib_kwargs=requestslib_kwargs)
        return resp