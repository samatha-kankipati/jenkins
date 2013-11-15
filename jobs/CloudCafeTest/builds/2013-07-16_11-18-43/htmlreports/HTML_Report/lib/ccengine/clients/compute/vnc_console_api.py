from ccengine.clients.base_client import BaseMarshallingClient
from ccengine.domain.compute.request.server_requests import GetConsole
from ccengine.domain.compute.response.vnc_console import VncConsole


class VncConsoleClient(BaseMarshallingClient):

    def __init__(self, url, auth_token, serialize_format=None,
                 deserialize_format=None):
        super(VncConsoleClient, self).__init__(serialize_format,
                                               deserialize_format)
        self.auth_token = auth_token
        self.default_headers['X-Auth-Token'] = auth_token
        ct = ''.join(['application/', self.serialize_format])
        accept = ''.join(['application/', self.deserialize_format])
        self.default_headers['Content-Type'] = ct
        self.default_headers['Accept'] = accept
        self.url = url

    def get_vnc_console(self, server_id, vnc_type, tenant_id=None,
                        requestslib_kwargs=None):
        request = GetConsole(vnc_type=vnc_type, tenant_id=tenant_id)

        url = '{base_url}/servers/{server_id}/action'.format(
            base_url=self.url, server_id=server_id)
        resp = self.request('POST', url,
                            response_entity_type=VncConsole,
                            request_entity=request,
                            requestslib_kwargs=requestslib_kwargs)
        return resp
