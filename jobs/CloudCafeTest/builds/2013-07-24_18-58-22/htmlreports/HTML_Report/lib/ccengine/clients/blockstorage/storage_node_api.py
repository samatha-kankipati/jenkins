from ccengine.clients.base_client import BaseRESTClient


class StorageNodeAPIClient(object):
    def __init__(self, is_ssl, host, port, name=None):
        '''
            @TODO: Move this init functionality into the provider.  The client
                   Shouldn't be collecting sub clients.
            @summary: Collection of REST clients the Lunr Storage Node API
                      This will create a Volumes, Backup, and Status
                      Storage Node API Client.
            @param is_ssl: Whether or not to use http or https for the url
            @type is_ssl: Boolean
            @param host: Location of storage node (usually IPv4 address)
            @type host: String
            @param port: Port to use to connect to storage node
            @keyword name: Name of the storage node as reported by the LunrAPI
            @type Volumes: Storage Node Volumes API Client instance
            @type Backups: Storage Node Backups API Client instance
            @type Status: Storage Node Status API Client instance
        '''

        client_args = [host, port, is_ssl]
        self.Volumes = Volumes(*client_args)
        self.Backups = Backups(*client_args)
        self.Status = Status(*client_args)

        self.host = host
        self.port = port
        self.is_ssl = is_ssl
        self.name = name

    def __repr__(self):
        r_str = ''
        r_str = r_str + str(self.host)
        r_str = r_str + str(self.port)
        r_str = r_str + str(self.is_ssl)
        return r_str


class _BaseStorageNodeClient(BaseRESTClient):
    def __init__(self, host, port, is_ssl):
        '''
            @summary: Base client from which all other StorageNode clients
                      inherit.
            @param is_ssl: Whether or not to use http or https for the url
            @type is_ssl: Boolean
            @param host: Location of storage node (usually IPv4 address)
            @param type: String
            @param port: Port to use to connect to storage node
        '''
        super(_BaseStorageNodeClient, self).__init__()
        self.is_ssl = is_ssl
        self.host = str(host)
        self.port = str(port)

        self.name = None
        self.volume_type_name = None

        http_prefix = 'https://' if self.is_ssl else 'http://'
        self._base_url = '{0}{1}:{2}'.format(http_prefix, self.host, self.port)


class Volumes(_BaseStorageNodeClient):
    def __init__(self, host, port, is_ssl):
        super(Volumes, self).__init__(host, port, is_ssl)
        self._base_url = "{0}/volumes".format(self._base_url)

    def delete(self, volume_id, headers=None, params=None,
               requestslib_kwargs=None):
        """Perform a DELETE on http(s)://host/volumes/{volume_id}"""
        url = '{0}/{1}'.format(self._base_url, volume_id)
        return self.request('DELETE', url, headers=headers, params=params,
                            requestslib_kwargs=requestslib_kwargs)

    def list(self, headers=None, params=None, requestslib_kwargs=None):
        """ Perform a GET on http(s)://host/volumes"""
        url = self._base_url
        return self.request('GET', url, headers=headers, params=params,
                            requestslib_kwargs=requestslib_kwargs)

    def get_info(self, volume_id=None, headers=None, params=None,
                 requestslib_kwargs=None):
        """ Perform a GET on http(s)://host/volumes/{volume_id}"""
        url = '{0}/{1}'.format(self._base_url, volume_id)
        return self.request('GET', url, headers=headers, params=params,
                            requestslib_kwargs=requestslib_kwargs)

    def create(self, volume_id=None, headers=None, params=None,
               requestslib_kwargs=None):
        """ Perform a PUT on http(s)://host/volumes/{volume_id}
            Optional params:
                size = positive integer
                source_volume_id = string
                backup_id = string
        """
        url = '{0}/{1}'.format(self._base_url, volume_id)
        return self.request('PUT', url, headers=headers, params=params,
                            requestslib_kwargs=requestslib_kwargs)

    def create_from_snapshot(self, source_volume_id=None, backup_id=None,
                             size=None, headers=None, params=None,
                             requestslib_kwargs=None):
        """ Perform a PUT on http(s)://host/volumes/{volume_id}
            Required params:
                size = positive integer
                source_volume_id = string
                backup_id = string
            (Note: Passing required params in invocation inserts them
                  automatically into the params dict.)
        """
        url = '{0}/{1}'.format(self._base_url, source_volume_id)
        required = {'size': size, 'source_volume_id': source_volume_id,
                       'backup_id': backup_id}
        params = dict(required, **params)
        return self.request('PUT', url, headers=headers, params=params,
                            requestslib_kwargs=requestslib_kwargs)


class Status(_BaseStorageNodeClient):
    def __init__(self, host, port, is_ssl):
        super(Status, self).__init__(host, port, is_ssl)
        self._base_url = "{0}/status".format(self._base_url)

    def all(self, headers=None, params=None, requestslib_kwargs=None):
        """ Perform a GET on http(s)://host/status """
        url = self._base_url
        return self.request('GET', url, headers=headers, params=params,
                            requestslib_kwargs=requestslib_kwargs)

    def api(self, headers=None, params=None, requestslib_kwargs=None):
        """ Perform a GET on http(s)://host/status/api """
        url = '{0}/api'.format(self._base_url)
        return self.request('GET', url, headers=headers, params=params,
                            requestslib_kwargs=requestslib_kwargs)

    def volumes(self, headers=None, params=None, requestslib_kwargs=None):
        """ Perform a GET on http(s)://host/status/volumes """
        url = '{0}/volumes'.format(self._base_url)
        return self.request('GET', url, headers=headers, params=params,
                            requestslib_kwargs=requestslib_kwargs)

    def exports(self, headers=None, params=None, requestslib_kwargs=None):
        """ Perform a GET on http(s)://host/status/exports """
        url = '{0}/exports'.format(self._base_url)
        return self.request('GET', url, headers=headers, params=params,
                            requestslib_kwargs=requestslib_kwargs)

    def backups(self, headers=None, params=None, requestslib_kwargs=None):
        """ Perform a GET on http(s)://host/status/backups """
        url = '{0}/backups'.format(self._base_url)
        return self.request('GET', url, headers=headers, params=params,
                            requestslib_kwargs=requestslib_kwargs)


class Backups(_BaseStorageNodeClient):
    def __init__(self, host, port, is_ssl):
        super(Backups, self).__init__(host, port, is_ssl)
        self._base_url = "{0}/volumes".format(self._base_url)

    def list(self, volume_id, headers=None, params=None,
             requestslib_kwargs=None):
        ''' GET /volumes/{volume_id}/backups - List backups for a volume '''
        url = '{0}/{1}/backups'.format(self._base_url, volume_id)
        return self.request('GET', url, headers=headers, params=params,
                            requestslib_kwargs=requestslib_kwargs)

    def get_info(self, volume_id, backup_id, headers=None, params=None,
                 requestslib_kwargs=None):
        '''
            GET /volumes/{volume_id}/backups/{id}
            Get information about a running backup
        '''
        url = '{0}/{1}/backups/{2}'.format(self._base_url, volume_id,
                                           backup_id)
        return self.request('GET', url, headers=headers, params=params,
                            requestslib_kwargs=requestslib_kwargs)

    def create(self, volume_id, backup_id, timestamp, headers=None,
               params=None, requestslib_kwargs=None):
        """ @summary: PUT /volumes/{volume_id}/backups/{id}
                      Create a new backup
            @param timestamp: Timestamp to use for new backup
            @type timestamp: integer
        """
        url = '{0}/{1}/backups/{2}'.format(self._base_url, volume_id,
                                           backup_id)

        required = {'timestamp': timestamp}
        params = dict(required, **(params or {}))
        return self.request('PUT', url, headers=headers, params=params,
                            requestslib_kwargs=requestslib_kwargs)

    def delete(self, volume_id, backup_id, headers=None, params=None,
               requestslib_kwargs=None):
        '''
            DELETE /volumes/{volume_id}/backups/{id}
            Delete an existing backup
        '''
        url = '{0}/{1}/backups/{2}'.format(self._base_url, volume_id,
                                           backup_id)
        return self.request('DELETE', url, headers=headers, params=params,
                            requestslib_kwargs=requestslib_kwargs)


class Exports(_BaseStorageNodeClient):
    def __init__(self, host, port, is_ssl):
        super(Exports, self).__init__(host, port, is_ssl)
        self._base_url = "{0}/volumes".format(self._base_url)

    def create(self, volume_id, requestslib_kwargs=None):
        '''
            PUT /volumes/{id}/export
            Create export
        '''
        url = '{0}/export'.format(self._base_url, volume_id)
        self.request('PUT', url, requestslib_kwargs=requestslib_kwargs)
        pass

    def get_info(self, volume_id, requestslib_kwargs=None):
        '''
            GET /volumes/{id}/export
            Get export information
        '''
        url = '{0}/export'.format(self._base_url, volume_id)
        self.request('GET', url, requestslib_kwargs=requestslib_kwargs)
        pass

    def remove(self, volume_id, requestslib_kwargs=None):
        ''' DELETE /volumes/{id}/export
            Remove export
        '''
        url = '{0}/export'.format(self._base_url, volume_id)
        self.request('DELETE', url, requestslib_kwargs=requestslib_kwargs)
        pass
