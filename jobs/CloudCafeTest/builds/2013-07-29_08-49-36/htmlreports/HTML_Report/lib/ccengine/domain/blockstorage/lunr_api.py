import json
from ccengine.domain.base_domain import BaseDomain, BaseMarshallingDomain


class AccountResponse(BaseMarshallingDomain):
    def __init__(self, status=None, created_at=None, last_modified=None,
                 id_=None, name=None):
        '''
        @summary: Represents a Lunr API "Create account" response.
        '''
        self.status = status
        self.created_at = created_at
        self.last_modified = last_modified
        self.id = id_
        self.name = name

    @classmethod
    def _json_to_obj(cls, serialized_str):
        body = json.loads(serialized_str)
        return AccountResponse(
                status=body.get('status'),
                created_at=body.get('created_at'),
                last_modified=body.get('last_modified'),
                id_=body.get('id'),
                name=body.get('name'))


class StorageNode(BaseDomain):
    '''
        @summary: Represents a Lunr API Storage Node
    '''
    __attrs__ = ['status',
                 'volume_type_name',
                 'name',
                 'created_at',
                 'hostname',
                 'port',
                 'meta',
                 'storage_hostname',
                 'last_modified',
                 'storage_port',
                 'id',
                 'size']


class Account(BaseDomain):
    '''
        @summary: Represents a Lunr API User
    '''
    __attrs__ = ['status',
                 'created_at',
                 'last_modified',
                 'id',
                 'name']


class Volume(BaseDomain):
    '''
        @summary: Represents a Lunr API Volume
    '''
    __attrs__ = ['status',
                'volume_type_name',
                'account_id',
                'target_name',
                'created_at',
                'node_id',
                'target_portal',
                'last_modified',
                'id',
                'size']


class Backup(BaseDomain):
    __attrs__ = ['status',
                 'account_id',
                 'created_at',
                 'last_modified',
                 'volume_id',
                 'id',
                 'size']


class VolumeType(BaseDomain):
    __attrs__ = ['status',
                 'name',
                 'created_at',
                 'min_size',
                 'last_modified',
                 'read_iops',
                 'write_iops',
                 'max_size']
