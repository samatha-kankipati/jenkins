#from ccengine.common.connectors import rest
from ccengine.domain.compute.volume_attachments import VolumeAttachment
from ccengine.clients.base_client import BaseMarshallingClient


class VolumeAttachmentsAPIClient(BaseMarshallingClient):

    def __init__(self, url, auth_token, tenant_id, serialize_format=None,
                 deserialize_format=None):
        super(VolumeAttachmentsAPIClient, self).__init__(serialize_format,
                                               deserialize_format)

        self.url = url
        self.auth_token = auth_token
        self.tenant_id = tenant_id
        self.default_headers['X-Auth-Token'] = auth_token
        self.default_headers['Content-Type'] = 'application/%s' % \
                                               self.serialize_format
        self.default_headers['Accept'] = 'application/%s' % \
                                         self.deserialize_format

    def attach_volume(self, server_id, volume_id, device=None,
                      requestslib_kwargs=None):
        '''
        POST
        v2/{tenant_id}/servers/{server_id}/os-volume_attachments
        '''

        url = '%s/servers/%s/os-volume_attachments' % (self.url, server_id)
        va = VolumeAttachment(volume_id, device)
        return self.request('POST', url,
                                  response_entity_type=VolumeAttachment,
                                  request_entity=va,
                                  requestslib_kwargs=requestslib_kwargs)

    def delete_volume_attachment(self, attachment_id, server_id,
                                 requestslib_kwargs=None):
        url = '%s/servers/%s/os-volume_attachments/%s' % (self.url, server_id,
                                                          attachment_id)

        params = {'tenant_id': self.tenant_id,
                  'server_id': server_id,
                  'attachment_id': attachment_id}

        return self.request('DELETE', url, params=params,
                                  requestslib_kwargs=requestslib_kwargs)

    def get_server_volume_attachments(self, server_id,
                                      requestslib_kwargs=None):
        url = '{0}/servers/{1}/os-volume_attachments'.format(
            self.url, server_id)

        params = {'tenant_id': self.tenant_id,
                  'server_id': server_id}

        return self.request(
            'GET', url, params=params, requestslib_kwargs=requestslib_kwargs)

    def get_volume_attachment_details(self, attachment_id, server_id,
                                      requestslib_kwargs=None):
        url = '{0}/servers/{1}/os-volume_attachments/{2}'.format(
            self.url, server_id, attachment_id)
        params = {'tenant_id': self.tenant_id,
                  'server_id': server_id,
                  'attachment_id': attachment_id}

        return self.request('GET', url, params=params,
                                  requestslib_kwargs=requestslib_kwargs)
