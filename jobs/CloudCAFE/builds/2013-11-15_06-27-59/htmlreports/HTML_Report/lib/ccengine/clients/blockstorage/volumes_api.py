#from ccengine.common.connectors import rest
from ccengine.domain.blockstorage.volumes_api import Volume, Volumes,\
        VolumeType, VolumeTypes, VolumeSnapshot, VolumeSnapshots
from ccengine.clients.base_client import BaseMarshallingClient


class VolumesAPIClient(BaseMarshallingClient):
    def __init__(self, url, auth_token, tenant_id, serialize_format=None,
                 deserialize_format=None):
        super(VolumesAPIClient, self).__init__(serialize_format,
                                               deserialize_format)

        self.url = url
        self.auth_token = auth_token
        self.default_headers['X-Auth-Token'] = auth_token
        self.default_headers['Content-Type'] = 'application/%s' % \
                                               self.serialize_format
        self.default_headers['Accept'] = 'application/%s' % \
                                         self.deserialize_format

    def create_volume(self, display_name, size, volume_type,
                      availability_zone=None, metadata={},
                      display_description='', snapshot_id=None,
                      requestslib_kwargs=None):
        '''
            POST
            v1/{tenant_id}/volumes
        '''

        url = '%s/volumes' % (self.url)

        volume_request_entity = Volume(display_name=display_name,
                                       size=size,
                                       volume_type=volume_type,
                                       display_description=display_description,
                                       metadata=metadata,
                                       availability_zone=availability_zone,
                                       snapshot_id=snapshot_id)

        return self.request('POST', url,
                                  response_entity_type=Volume,
                                  request_entity=volume_request_entity,
                                  requestslib_kwargs=requestslib_kwargs)

    def create_volume_from_snapshot(self, snapshot_id, size, display_name='',
                                    volume_type=None, availability_zone=None,
                                    display_description='', metadata={},
                                    requestslib_kwargs=None):
        '''
            POST
            v1/{tenant_id}/volumes
        '''

        url = '%s/volumes' % (self.url)

        volume_request_entity = Volume(display_name=display_name,
                                       size=size,
                                       volume_type=volume_type,
                                       display_description=display_description,
                                       metadata=metadata,
                                       availability_zone=availability_zone,
                                       snapshot_id=snapshot_id)

        return self.request('POST', url,
                                  response_entity_type=Volume,
                                  request_entity=volume_request_entity,
                                  requestslib_kwargs=requestslib_kwargs)

    def list_all_volumes(self, requestslib_kwargs=None):
        '''
            GET
            v1/{tenant_id}/volumes
        '''
        url = '%s/volumes' % (self.url)
        return self.request('GET', url,
                                  response_entity_type=Volumes,
                                  requestslib_kwargs=requestslib_kwargs)

    def list_all_volumes_info(self, requestslib_kwargs=None):
        '''
            GET
            v1/{tenant_id}/volumes/detail
        '''
        url = '%s/volumes/detail' % (self.url)
        return self.request('GET', url,
                                  response_entity_type=Volumes,
                                  requestslib_kwargs=requestslib_kwargs)

    def get_volume_info(self, volume_id, requestslib_kwargs=None):
        '''
            GET
            v1/{tenant_id}/volumes/{volume_id}
        '''
        url = '%s/volumes/%s' % (self.url, volume_id)
        return self.request('GET', url,
                                  response_entity_type=Volume,
                                  requestslib_kwargs=requestslib_kwargs)

    def update_volume_info(
            self, volume_id, display_name=None, display_description=None,
            requestslib_kwargs=None):
        '''
            PUT
            v1/{tenant_id}/volumes/{volume_id}
        '''

        url = '{0}/volumes/{1}'.format(self.url, volume_id)

        volume_request_entity = Volume(
            display_name=display_name, display_description=display_description)

        return self.request(
            'PUT', url, response_entity_type=Volume,
            request_entity=volume_request_entity,
            requestslib_kwargs=requestslib_kwargs)

    def delete_volume(self, volume_id, requestslib_kwargs=None):
        '''
            DELETE
            v1/{tenant_id}/volumes/{volume_id}
        '''
        url = '%s/volumes/%s' % (self.url, volume_id)
        return self.request('DELETE', url,
                                  response_entity_type=Volume,
                                  requestslib_kwargs=requestslib_kwargs)

    def list_all_volume_types(self, requestslib_kwargs=None):
        '''
            GET
            v1/{tenant_id}/types
        '''
        url = '%s/types' % (self.url)
        return self.request('GET', url,
                                  response_entity_type=VolumeTypes,
                                  requestslib_kwargs=requestslib_kwargs)

    def get_volume_type_info(self, volume_type_id, requestslib_kwargs=None):
        '''
            GET
            v1/{tenant_id}/types/{volume_type_id}
        '''
        url = '%s/types/%s' % (self.url, volume_type_id)
        return self.request('GET', url,
                                  response_entity_type=VolumeType,
                                  requestslib_kwargs=requestslib_kwargs)

    def create_snapshot(self, volume_id, display_name=None,
                              display_description=None, force_create=False,
                              name=None, requestslib_kwargs=None):
        '''
            POST
            v1/{tenant_id}/snapshots
        '''
        url = '%s/snapshots' % (self.url)

        volume_snapshot_request_entity = VolumeSnapshot(volume_id,
                force=force_create, display_name=display_name, name=name,
                display_description=display_description)

        return self.request('POST', url,
                                response_entity_type=VolumeSnapshot,
                                request_entity=volume_snapshot_request_entity,
                                requestslib_kwargs=requestslib_kwargs)

    def update_snapshot_info(
            self, snapshot_id, display_name=None, display_description=None,
            requestslib_kwargs=None):
        '''
            PUT
            v1/{tenant_id}/snapshots/{snapshot_id}
        '''

        url = '{0}/snapshots/{1}'.format(self.url, snapshot_id)

        volume_snapshot_request_entity = VolumeSnapshot(
            display_name=display_name, display_description=display_description)

        return self.request(
            'PUT', url, response_entity_type=VolumeSnapshot,
            request_entity=volume_snapshot_request_entity,
            requestslib_kwargs=requestslib_kwargs)

    def list_all_snapshots(self, requestslib_kwargs=None):
        '''
            GET
            v1/{tenant_id}/snapshots
        '''
        url = '%s/snapshots' % (self.url)
        return self.request('GET', url,
                                response_entity_type=VolumeSnapshots,
                                requestslib_kwargs=requestslib_kwargs)

    def list_all_snapshots_info(self, requestslib_kwargs=None):
        '''
            GET
            v1/{tenant_id}/snapshots/detail
        '''
        url = '%s/snapshots/detail' % (self.url)
        return self.request('GET', url,
                                response_entity_type=VolumeSnapshots,
                                requestslib_kwargs=requestslib_kwargs)

    def get_snapshot_info(self, snapshot_id, requestslib_kwargs=None):
        '''
            GET
            v1/{tenant_id}/snapshots/{snapshot_id}
        '''
        url = '%s/snapshots/%s' % (self.url, snapshot_id)
        return self.request('GET', url,
                                response_entity_type=VolumeSnapshot,
                                requestslib_kwargs=requestslib_kwargs)

    def delete_snapshot(self, snapshot_id, requestslib_kwargs=None):
        '''
            DELETE
            v1/{tenant_id}/snapshots/{snapshot_id}
        '''
        url = '%s/snapshots/%s' % (self.url, snapshot_id)
        return self.request('DELETE', url,
                                response_entity_type=VolumeSnapshot,
                                requestslib_kwargs=requestslib_kwargs)
