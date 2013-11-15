'''
@summary: Provider Module for the AUTH API
@note: Should be the primary interface to a test case or external tool.
@copyright: Copyright (c) 2012 Rackspace US, Inc.
'''

from ccengine.providers.base_provider import BaseProvider
from ccengine.clients.auth.auth_client import AuthClient as _AuthClient
from ccengine.clients.auth.keystone_client import KeystoneClient as _KeystoneClient
from ccengine.domain.auth import Auth_2_0 as _Auth_2_0_DomainObject
from ccengine.domain.auth import Auth_1_1 as _Auth_1_1_DomainObject
import json


class AuthProvider(BaseProvider):
    '''
    @summary: Provides an interface to Auth providers
    '''

    def __init__(self, config):
        super(AuthProvider, self).__init__()
        self.config = config
        self.client = _AuthClient(self.config.auth.base_url,
                                  self.config.auth.version,
                                  self.config.auth.username,
                                  self.config.auth.api_key,
                                  self.config.auth.password)
        self.keystone_client = _KeystoneClient(self.config.auth.base_url)

    def authenticate(self):
        '''
            Automatically authenticates with the correct version of auth given
            the information in the configuration file
        '''
        try:
            if self.config.auth.version == 'keystone':
                r = self.keystone_client.authenticate(self.config.auth.username,
                                                      self.config.auth.password,
                                                      self.config.auth.tenant_name)
                if not r.ok:
                    self.provider_log.error('Failed to authenticate using Keystone')
                ResponseDict = json.loads(r.content)
                return _Auth_2_0_DomainObject(ResponseDict)
            elif self.config.auth.version == '2.0':
                r = self.client.auth_2_0()
                if not r.ok:
                    self.provider_log.error('Quick Auth 2.0 recieved a negative response from auth')
                ResponseDict = json.loads(r.content)
                return _Auth_2_0_DomainObject(ResponseDict)

            elif self.config.auth.version == '1.1':
                r = self.client.auth_1_1()
                if not r.ok:
                    self.provider_log.error('Quick Auth 1.1 recieved a negative response from auth')
                ResponseDict = json.loads(r.content)
                return _Auth_1_1_DomainObject(ResponseDict)
            elif self.config.auth.version == 'core':
                token = self.client.auth_core()
                if not token.ok:
                    self.provider_log.error('recieved a negative response from Core auth')
                return token.content
            elif self.config.auth.version == '2.0_internal':
                r = self.client.auth_2_0_internal()
                if not r.ok:
                    self.provider_log.error('Quick Auth 2.0 recieved a negative response from auth')
                ResponseDict = json.loads(r.content)
                return _Auth_2_0_DomainObject(ResponseDict)

        except ValueError as e:
            msg = 'authenticate in the auth_api provider failed due to a non-json response: \n%s' % (str(e))
            self.provider_log.exception(msg)
            raise ValueError(msg)
        except Exception as e:
            msg = 'authenticate in the auth_api provider failed due to unexpected exception: \n%s' % (str(e))
            self.provider_log.exception(msg)
