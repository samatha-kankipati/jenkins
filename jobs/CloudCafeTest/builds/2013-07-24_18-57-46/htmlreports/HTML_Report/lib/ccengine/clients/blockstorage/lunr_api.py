'''
@summary: Client to make rest calls to the Lunr API
@copyright: Copyright (c) 2012 Rackspace US, Inc.
'''

from ccengine.clients.base_client import BaseRESTClient


class LunrAPIClient(object):

    def __init__(self, is_ssl, host, port, version='v1.0',
                 account_name='admin', account_id='admin'):
        '''@TODO: Move the individual client instantiation to the provider!'''

        self.host = host
        self.port = port
        self.version = version
        self.is_ssl = is_ssl
        self.account_name = account_name
        self.account_id = account_id

        client_args = [is_ssl, host, port, version, account_name, account_id]

        self.Volumes = Volumes(*client_args)
        self.Backups = Backups(*client_args)
        self.VolumesAdmin = VolumesAdmin(*client_args)
        self.BackupsAdmin = BackupsAdmin(*client_args)
        self.Nodes = Nodes(*client_args)
        self.Accounts = Accounts(*client_args)
        self.VolumeTypes = VolumeTypes(*client_args)

    def __repr__(self):
        r_str = ''
        r_str = r_str + str(self.host)
        r_str = r_str + str(self.port)
        r_str = r_str + str(self.version)
        r_str = r_str + str(self.account_name)
        r_str = r_str + str(self.account_id)
        return r_str


class _BaseLunrClient(BaseRESTClient):
    def __init__(self, is_ssl, host, port, version, account_name, account_id):
        super(_BaseLunrClient, self).__init__()
        self.host = host
        self.port = port
        self.version = version
        self.is_ssl = is_ssl
        self.account_name = account_name
        self.account_id = account_id
        self._suffix = None

        http_prefix = 'http://'
        if self.is_ssl == True:
            http_prefix = 'https://'
        self._base_url = '{0}{1}:{2}'.format(http_prefix, self.host, self.port)

        if self.version:
            self._base_url = '{0}/{1}'.format(self._base_url, self.version)


class Volumes(_BaseLunrClient):
    def __init__(self, is_ssl, host, port, version, account_name, account_id):
        super(Volumes, self).__init__(is_ssl, host, port, version,
                                       account_name, account_id)
        self._base_url = '{0}/{1}/volumes'.format(self._base_url,
                                                  self.account_id)

    def list(self, headers=None, params=None, requestslib_kwargs=None):
        '''
            GET {account_name}/volumes
            List volumes for an account
        '''
        return self.request('GET', self._base_url, headers=headers,
                params=params, requestslib_kwargs=requestslib_kwargs)

    def create(self, volume_id, size, volume_type_name,
               headers=None, params=None, requestslib_kwargs=None):
        '''
            PUT {account_name}/volumes
            Create a volume
        '''
        url = '{0}/{1}'.format(self._base_url, volume_id)
        required_params = {'size': size, 'volume_type_name': volume_type_name}
        params = dict(required_params, **(params or {}))
        return self.request('PUT', url, params=params, headers=headers,
                            requestslib_kwargs=requestslib_kwargs)

    def get_info(self, volume_id, headers=None, params=None,
                 requestslib_kwargs=None):
        '''
            GET {account_name}/volumes/{volume_id}
            Get information about a volume
        '''
        url = '{0}/{1}'.format(self._base_url, volume_id)
        return self.request('GET', url, headers=headers, params=params,
                            requestslib_kwargs=requestslib_kwargs)

    def update(self, volume_id, headers=None, params=None,
               requestslib_kwargs=None):
        '''
            POST {account_name}/volumes/{volume_id}
            Update information about a volume
        '''
        url = '{0}/{1}'.format(self._base_url, volume_id)
        return self.request('POST', url, headers=headers, params=params,
                            requestslib_kwargs=requestslib_kwargs)

    def delete(self, volume_id, headers=None, params=None,
               requestslib_kwargs=None):
        '''
            @TODO: Rename to 'delete_volume' so as not to overload base delete
                   method
            DELETE {account_name}/volumes/{volume_id}
            Delete a volume
        '''
        url = '{0}/{1}'.format(self._base_url, volume_id)
        return self.request('DELETE', url, headers=headers, params=params,
                            requestslib_kwargs=requestslib_kwargs)


class Backups(_BaseLunrClient):

    def __init__(self, is_ssl, host, port, version, account_name, account_id):
        super(Backups, self).__init__(is_ssl, host, port, version,
                                       account_name, account_id)
        self._base_url = '{0}/{1}/backups'.format(self._base_url,
                                                  self.account_id)

    def list(self, headers=None, params=None, requestslib_kwargs=None):
        '''
            GET {account_name}/backups
            List backups for an account
        '''
        return self.request('GET', self._base_url, headers=headers,
                params=params, requestslib_kwargs=requestslib_kwargs)

    def create(self, backup_id, headers=None, params=None,
               requestslib_kwargs=None):
        '''
            PUT {account_name}/backups
            Create backup
        '''
        url = '{0}/{1}'.format(self._base_url, backup_id)
        return self.request('PUT', url, headers=headers, params=params,
                            requestslib_kwargs=requestslib_kwargs)

    def get_info(self, backup_id, headers=None, params=None,
                 requestslib_kwargs=None):
        '''
            GET {account_name}/backups/{backup_id}
            Get information about a backup
        '''
        url = '{0}/{1}'.format(self._base_url, backup_id)
        return self.request('GET', url, headers=headers, params=params,
                            requestslib_kwargs=requestslib_kwargs)

    def update(self, backup_id, headers=None, params=None,
               requestslib_kwargs=None):
        '''
            POST {account_name}/backups/{backup_id}
            Update information about a backup
        '''
        url = '{0}/{1}'.format(self._base_url, backup_id)
        return self.request('POST', url, headers=headers, params=params,
                            requestslib_kwargs=requestslib_kwargs)

    def delete(self, backup_id, headers=None, params=None,
               requestslib_kwargs=None):
        '''
        DELETE {account_name}/backups/{backup_id}
        Delete a backup
        '''
        url = '{0}/{1}'.format(self._base_url, backup_id)
        return self.request('DELETE', url, headers=headers, params=params,
                            requestslib_kwargs=requestslib_kwargs)


class _AdminTemplate(_BaseLunrClient):
    def __init__(self, is_ssl, host, port, version, account_name, account_id):
        super(_AdminTemplate, self).__init__(is_ssl, host, port, version,
                                             account_name, account_id)

        self._base_url = '{0}/admin'.format(self._base_url)

    def create(self, headers=None, params=None,
               requestslib_kwargs=None):
        '''POST'''
        return self.request('POST', self._base_url, headers=headers,
                params=params, requestslib_kwargs=requestslib_kwargs)

    def put_create(self, headers=None, params=None, requestslib_kwargs=None):
        '''PUT'''
        return self.request('PUT', self._base_url, headers=headers,
                params=params, requestslib_kwargs=requestslib_kwargs)

    def list(self, headers=None, params=None, requestslib_kwargs=None):
        '''GET'''
        return self.request('GET', self._base_url, headers=headers,
                params=params, requestslib_kwargs=requestslib_kwargs)


class VolumesAdmin(_AdminTemplate):

    def __init__(self, is_ssl, host, port, version, account_name, account_id):
        super(VolumesAdmin, self).__init__(is_ssl, host, port, version,
                                            account_name, account_id)
        self._base_url = '{0}/volumes'.format(self._base_url)

    def update(self, volume_id, headers=None, params=None,
               requestslib_kwargs=None):
        '''POST'''
        url = '{0}/{1}'.format(self._base_url, volume_id)
        return self.request('POST', url, headers=headers, params=params,
                            requestslib_kwargs=requestslib_kwargs)

    def get_info(self, volume_id, headers=None, params=None,
                 requestslib_kwargs=None):
        '''GET'''
        url = '{0}/{1}'.format(self._base_url, volume_id)
        return self.request('GET', url, headers=headers, params=params,
                            requestslib_kwargs=requestslib_kwargs)

    def delete(self, volume_id, headers=None, params=None,
               requestslib_kwargs=None):
        '''DELETE'''
        url = '{0}/{1}'.format(self._base_url, volume_id)
        return self.request('DELETE', url,
                            headers=headers, params=params,
                            requestslib_kwargs=requestslib_kwargs)


class BackupsAdmin(_AdminTemplate):

    def __init__(self, is_ssl, host, port, version, account_name, account_id):
        super(BackupsAdmin, self).__init__(is_ssl, host, port, version,
                                            account_name, account_id)
        self._base_url = '{0}/backups'.format(self._base_url)

    def update(self, backup_id, headers=None, params=None,
               requestslib_kwargs=None):
        '''POST'''
        url = '{0}/{1}'.format(self._base_url, backup_id)
        return self.request('POST', url, headers=headers, params=params,
                            requestslib_kwargs=requestslib_kwargs)

    def get_info(self, backup_id, headers=None, params=None,
                 requestslib_kwargs=None):
        '''GET'''
        url = '{0}/{1}'.format(self._base_url, backup_id)
        return self.request('GET', url, headers=headers, params=params,
                            requestslib_kwargs=requestslib_kwargs)

    def delete(self, backup_id, headers=None, params=None,
               requestslib_kwargs=None):
        '''DELETE'''
        url = '{0}/{1}'.format(self._base_url, backup_id)
        return self.request('DELETE', url, headers=headers, params=params,
                            requestslib_kwargs=requestslib_kwargs)


class Nodes(_AdminTemplate):

    def __init__(self, is_ssl, host, port, version, account_name, account_id):
        super(Nodes, self).__init__(is_ssl, host, port, version,
                                     account_name, account_id)
        self._base_url = '{0}/nodes'.format(self._base_url)

    def update(self, node_id, headers=None, params=None,
               requestslib_kwargs=None):
        '''POST'''
        url = '{0}/{1}'.format(self._base_url, node_id)
        return self.request('POST', url, headers=headers, params=params,
                            requestslib_kwargs=requestslib_kwargs)

    def get_info(self, node_id, headers=None, params=None,
                 requestslib_kwargs=None):
        '''GET'''
        url = '{0}/{1}'.format(self._base_url, node_id)
        return self.request('GET', url, headers=headers, params=params,
                            requestslib_kwargs=requestslib_kwargs)

    def delete(self, node_id, headers=None, params=None,
               requestslib_kwargs=None):
        '''DELETE'''
        url = '{0}/{1}'.format(self._base_url, node_id)
        return self.request('DELETE', url, headers=headers, params=params,
                            requestslib_kwargs=requestslib_kwargs)


class Accounts(_AdminTemplate):

    def __init__(self, is_ssl, host, port, version, account_name, account_id):
        super(Accounts, self).__init__(is_ssl, host, port, version,
                                        account_name, account_id)
        self._base_url = '{0}/accounts'.format(self._base_url)

    def update(self, account_id, headers=None, params=None,
               requestslib_kwargs=None):
        '''POST'''
        url = '{0}/{1}'.format(self._base_url, account_id)
        return self.request('POST', url, headers=headers, params=params,
                            requestslib_kwargs=requestslib_kwargs)

    def get_info(self, account_id, headers=None, params=None,
                 requestslib_kwargs=None):
        '''GET'''
        url = '{0}/{1}'.format(self._base_url, account_id)
        return self.request('GET', url, headers=headers, params=params,
                            requestslib_kwargs=requestslib_kwargs)

    def delete(self, account_id, headers=None, params=None,
               requestslib_kwargs=None):
        '''DELETE'''
        url = '{0}/{1}'.format(self._base_url, account_id)
        return self.request('DELETE', url, headers=headers, params=params,
                            requestslib_kwargs=requestslib_kwargs)


class VolumeTypes(_AdminTemplate):

    def __init__(self, is_ssl, host, port, version, account_name, account_id):
        super(VolumeTypes, self).__init__(is_ssl, host, port, version,
                                           account_name, account_id)
        self._base_url = '{0}/volume_types'.format(self._base_url)

    def get_info(self, volume_type_id, headers=None, params=None,
                 requestslib_kwargs=None):
        '''GET'''
        url = '{0}/{1}'.format(self._base_url, volume_type_id)
        return self.request('GET', url, headers=headers, params=params,
                            requestslib_kwargs=requestslib_kwargs)

    def delete(self, volume_type_id, headers=None, params=None,
               requestslib_kwargs=None):
        '''DELETE'''
        url = '{0}/{1}'.format(self._base_url, volume_type_id)
        return self.request('DELETE', url, headers=headers, params=params,
                            requestslib_kwargs=requestslib_kwargs)
