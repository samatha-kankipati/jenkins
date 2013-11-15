'''
@summary: Classes and Utilities that provide low level connectivity to the
          Rest Client
@note: Should be consumed/exposed by a a L{ccengine.providers} class and
       rarely be used directly by any other object or process
@copyright: Copyright (c) 2012 Rackspace US, Inc.
'''
from ccengine.clients.base_client import BaseMarshallingClient
from ccengine.domain.rackconnect.configurations import Configurations
from ccengine.domain.rackconnect.autostatus import AutoStatuses
from urlparse import urlparse


class RackConnectApiClient(BaseMarshallingClient):

    def __init__(self, url, username, password, serialize_format=None,
                 deserialize_format=None):
        '''
        @param url: Rackconnect url
        @type url: string
        @param username: Rackconnect username
        @type username: string
        @param password: Rackconnect password
        @type password: string
        '''
        super(RackConnectApiClient, self).__init__(serialize_format,
                                               deserialize_format)
        self.default_headers['X-Auth-User'] = username
        self.default_headers['X-Auth-Key'] = password
        ct = ''.join(['application/', self.serialize_format])
        accept = ''.join(['application/', self.deserialize_format])
        self.default_headers['Content-Type'] = ct
        self.default_headers['Accept'] = accept
        self.url = url

    def get_core_account_configurations(self, account_number,
                                        requestslib_kwargs=None):
        '''
        @summary: Returns configurations of an account
        @param account_number: account id
        @type account_number:string
        @return: Object
        @rtype: C{configurations}
        '''

        
        #    GET
        #    v2/{core_account_number}/configurations
        
        url = '{0}/{1}/configurations'.format(self.url, account_number)
        config_response = self.request('GET', url,
                                       response_entity_type=Configurations,
                                       requestslib_kwargs=requestslib_kwargs)
        return config_response
    
    def get_tenant_automation_status(self, account_number, tenant_id,
                                     requestslib_kwargs=None):
        '''
        @summary: Returns configurations of an account
        @param account_number: account id
        @type account_number:string
        @param tenant_id: tenant id of the account
        @type tenant_id:string
        @return: Object
        @rtype: C{configurations}
        '''

        
        #    GET
        #    v2/{core_account_number}/configurations/cloud_accounts/{tenant_id}
        #    /cloud_servers/automation_statuses
        
        url = '{0}/{1}/configurations/cloud_accounts/{2}/cloud_servers/automation_statuses'.format(self.url, account_number, tenant_id)
        config_response = self.request('GET', url,
                                       response_entity_type=AutoStatuses,
                                       requestslib_kwargs=requestslib_kwargs)
        return config_response

