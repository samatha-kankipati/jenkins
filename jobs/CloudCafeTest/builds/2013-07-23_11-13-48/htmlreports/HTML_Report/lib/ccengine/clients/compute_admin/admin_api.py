from ccengine.clients.base_client import BaseMarshallingClient
from ccengine.domain.compute_admin.request.fixed_ip import \
    AddFixedIp, RemoveFixedIp
from ccengine.domain.compute.request.server_requests import \
    MigrateServer, LiveMigrateServer, Lock, Unlock, \
    Start, Stop, Suspend, Resume, Pause, Unpause, \
    ResetState, ResetNetwork, CreateBackup, Evacuate


class AdminAPIClient(BaseMarshallingClient):

    _admin_prefix = '/servers'
    _admin_suffix = '/action'

    def __init__(self, url, auth_token, serialize_format,
                 deserialize_format=None):
        super(AdminAPIClient, self).__init__(serialize_format,
                                             deserialize_format)
        self.url = '{0}{1}'.format(url, self._admin_prefix)
        self.auth_token = auth_token
        self.default_headers['X-Auth-Token'] = auth_token
        ct = 'application/{0}'.format(self.serialize_format)
        accept = 'application/{0}'.format(self.deserialize_format)
        self.default_headers['Content-Type'] = ct
        self.default_headers['Accept'] = accept

    def add_fixed_ip(self, server_id, network_id, requestslib_kwargs=None):
        '''
        @summary: Adds a fixed IP to a server.
        @param server_id: The id of an existing server.
        @type server_id: String
        @param network_id: A unique network id.
        @type network_id: String
        @return: Base Response object
        @rtype: Response object
        '''
        req_body = AddFixedIp(network_id=network_id)
        full_url = '{0}/{1}{2}'.format(self.url, server_id, self._admin_suffix)
        return self.request('POST', full_url,
                            response_entity_type=None,
                            request_entity=req_body,
                            requestslib_kwargs=requestslib_kwargs)

    def remove_fixed_ip(self, server_id, address, requestslib_kwargs=None):
        '''
        @summary: Removes a fixed IP to a server.
        @param server_id: The id of an existing server.
        @type server_id: String
        @param address: IP address to be removed.
        @type address: String
        @return: Base Response object
        @rtype: Response object
        '''
        req_body = RemoveFixedIp(address=address)
        full_url = '{0}/{1}{2}'.format(self.url, server_id, self._admin_suffix)
        return self.request('POST', full_url,
                            response_entity_type=None,
                            request_entity=req_body,
                            requestslib_kwargs=requestslib_kwargs)

    def lock_server(self, server_id, requestslib_kwargs=None):
        '''
        @summary: Locks a server
        @param server_id: The id of an existing server.
        @type server_id: String
        @return: Base Response object
        @rtype: Response object
        '''
        url = '{0}/servers/{1}/action'.format(self.url, server_id)
        resp = self.request('POST', url,
                            request_entity=Lock(),
                            requestslib_kwargs=requestslib_kwargs)
        return resp

    def unlock_server(self, server_id, requestslib_kwargs=None):
        '''
        @summary: Unlocks a server
        @param server_id: The id of an existing server.
        @type server_id: String
        @return: Base Response object
        @rtype: Response object
        '''
        url = '{0}/servers/{1}/action'.format(self.url, server_id)
        resp = self.request('POST', url,
                            request_entity=Unlock(),
                            requestslib_kwargs=requestslib_kwargs)
        return resp

    def stop_server(self, server_id, requestslib_kwargs=None):
        '''
        @summary: Stops a server, changes status to STOPPED
        @param server_id: The id of an existing server.
        @type server_id: String
        @return: Base Response object
        @rtype: Response object
        @todo: check if this is only exclusive to admin api
        '''
        url = '{0}/servers/{1}/action'.format(self.url, server_id)
        resp = self.request('POST', url,
                            request_entity=Stop(),
                            requestslib_kwargs=requestslib_kwargs)
        return resp

    def start_server(self, server_id, requestslib_kwargs=None):
        '''
        @summary: Starts a STOPPED server, changes status to ACTIVE
        @param server_id: The id of an existing server.
        @type server_id: String
        @return: Base Response object
        @rtype: Response object
        @todo: check if this is only exclusive to admin api
        '''
        url = '{0}/servers/{1}/action'.format(self.url, server_id)
        resp = self.request('POST', url,
                            request_entity=Start(),
                            requestslib_kwargs=requestslib_kwargs)
        return resp

    def suspend_server(self, server_id, requestslib_kwargs=None):
        '''
        @summary: Suspends a server, changes status to SUSPENDED
        @param server_id: The id of an existing server.
        @type server_id: String
        @return: Base Response object
        @rtype: Response object
        '''
        url = '{0}/servers/{1}/action'.format(self.url, server_id)
        resp = self.request('POST', url,
                            request_entity=Suspend(),
                            requestslib_kwargs=requestslib_kwargs)
        return resp

    def resume_server(self, server_id, requestslib_kwargs=None):
        '''
        @summary: Resumes a SUSPENDED server, changes status to ACTIVE
        @param server_id: The id of an existing server.
        @type server_id: String
        @return: Base Response object
        @rtype: Response object
        '''
        url = '{0}/servers/{1}/action'.format(self.url, server_id)
        resp = self.request('POST', url,
                            request_entity=Resume(),
                            requestslib_kwargs=requestslib_kwargs)
        return resp

    def pause_server(self, server_id, requestslib_kwargs=None):
        '''
        @summary: Pauses a server, changes status to PAUSED
        @param server_id: The id of an existing server.
        @type server_id: String
        @return: Base Response object
        @rtype: Response object
        '''
        url = '{0}/servers/{1}/action'.format(self.url, server_id)
        resp = self.request('POST', url,
                            request_entity=Pause(),
                            requestslib_kwargs=requestslib_kwargs)
        return resp

    def unpause_server(self, server_id, requestslib_kwargs=None):
        '''
        @summary: Unpauses a server, changes status to ACTIVE
        @param server_id: The id of an existing server.
        @type server_id: String
        @return: Base Response object
        @rtype: Response object
        '''
        url = '{0}/servers/{1}/action'.format(self.url, server_id)
        resp = self.request('POST', url,
                            request_entity=Unpause(),
                            requestslib_kwargs=requestslib_kwargs)
        return resp

    def reset_state(self, server_id, reset_state='ERROR',
                    requestslib_kwargs=None):
        '''
        @summary: Resets state of server to specified state.
        @param server_id: The id of an existing server.
        @type server_id: String
        @param state: The desired state of a server
        @type state: String
        @return: Base Response object
        @rtype: Response object
        '''
        url = '{0}/servers/{1}/action'.format(self.url, server_id)
        resp = self.request('POST', url,
                            request_entity=ResetState(),
                            requestslib_kwargs=requestslib_kwargs)
        return resp

    def reset_network(self, server_id, requestslib_kwargs=None):
        '''
        @summary: Resets networking on server.
        @param server_id: The id of an existing server.
        @type server_id: String
        @return: Base Response object
        @rtype: Response object
        '''
        url = '{0}/servers/{1}/action'.format(self.url, server_id)
        resp = self.request('POST', url,
                            request_entity=ResetNetwork(),
                            requestslib_kwargs=requestslib_kwargs)
        return resp

    def inject_network_info(self, server_id, requestslib_kwargs=None):
        '''
        @summary: Injects network info into server.
        @param server_id: The id of an existing server.
        @type server_id: String
        @return: Base Response object
        @rtype: Response object
        '''
        url = '{0}/servers/{1}/action'.format(self.url, server_id)
        resp = self.request('POST', url,
                            request_entity=ResetNetwork(),
                            requestslib_kwargs=requestslib_kwargs)
        return resp

    def create_backup(self, server_id, name, backup_type="daily",
                      rotation=5, requestslib_kwargs=None):
        '''
        @summary: Backs up a server instance.
        @param server_id: The id of an existing server.
        @type server_id: String
        @param name: The name of backup image.
        @type name: String
        @param backup_type: Backup type; either 'daily' or 'weekly'.
        @type backup_type: String
        @param rotation: Number of backups to maintain.
        @type rotation: String
        @return: Base Response object
        @rtype: Response object
        '''
        req_body = CreateBackup(name=name,
                                backup_type=backup_type,
                                rotation=rotation)
        url = '{0}/servers/{1}/action'.format(self.url, server_id)
        resp = self.request('POST', url,
                            request_entity=req_body,
                            requestslib_kwargs=requestslib_kwargs)
        return resp

    def evacuate(self, server_id, host, onSharedStorage,
                      adminPass, requestslib_kwargs=None):
        '''
        @summary: Evacuates server from failed host.
        @param server_id: The id of an existing server.
        @type server_id: String
        @param host: The name or ID of host where to server is evacuated to.
        @type host: String
        @param onSharedStorage: Required if server is on shared storage.
        @type onSharedStorage: Boolean
        @param adminPass: Not Specified with onSharedStorage;
            New password for the evacuated instance.
        @type adminPass: String
        @return: Base Response object
        @rtype: Response object
        '''
        req_body = Evacuate(host=host,
                            onSharedStorage=onSharedStorage,
                            adminPass=adminPass)
        url = '{0}/servers/{1}/action'.format(self.url, server_id)
        resp = self.request('POST', url,
                            request_entity=req_body,
                            requestslib_kwargs=requestslib_kwargs)
        return resp
