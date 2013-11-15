from ccengine.domain.base_domain import BaseDomain

class Volume(BaseDomain):
    '''
        @summary: Represents a Storage Node API Volume
    '''
    __attrs__ = ['origin',
                 'realpath',
                 'origin',
                 'realpath',
                 'device_number',
                 'volume',
                 'export',
                 'msg',
                 'path',
                 'id',
                 'size']

class Backup(BaseDomain):
    '''
        @summary: Represents a Storage Node API Backup
    '''
    __attrs__ = ['origin',
                'status',
                'backup_id',
                'realpath',
                'timestamp',
                'device_number',
                'path',
                'id',
                'size']