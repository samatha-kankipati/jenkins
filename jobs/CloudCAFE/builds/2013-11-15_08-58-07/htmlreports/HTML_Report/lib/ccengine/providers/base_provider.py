'''
@summary: Base Class for Providers
@copyright: Copyright (c) 2012 Rackspace US, Inc.
'''
from ccengine.common.tools import logging_tools


class BaseProvider(object):
    '''
    @summary: Interface for all Providers in CloudCAFE.
    @cvar provider_log: Python logger instance
    @type provider_log: C{Logger}
    '''
    def __init__(self):
        self.provider_log = logging_tools.getLogger(
                            logging_tools.get_object_namespace(self.__class__))


class ProviderActionResult(object):
    '''
        @summary: An object to represent the result of a provider method.
        @ivar response: Last response returned from a client or connector call in the provider method
        @ivar ok: Represents the success of the provider method
        @type ok:C{bool}
        @ivar entity: Domain object in use by provider method
    '''
    def __init__(self):
        self.response = None
        self.ok = False
        self.entity = None
