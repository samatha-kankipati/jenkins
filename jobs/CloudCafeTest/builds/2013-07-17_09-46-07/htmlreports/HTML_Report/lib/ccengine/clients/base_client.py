'''  All CloudCAFE clients should inherit from BaseClient '''
from os import putenv as os_putenv, unsetenv as os_unsetenv
from ccengine.common.tools import logging_tools
from ccengine.common.connectors.soap import SoapConnector
from ccengine.common.connectors.rest import RestConnector
from ccengine.common.connectors.commandline import CommandLineConnector


class BaseClient(object):
    '''
        Sets up logging for all inheriting clients.
    '''
    def __init__(self):
        super(BaseClient)
        self.client_log = logging_tools.getLogger(
                            logging_tools.get_object_namespace(self.__class__))


class BaseOpenstackCLIClient(BaseClient, CommandLineConnector):
    '''
    @summary: Allows client-wrappers for Openstack CLI Tools to set OS
              environment variables up for themselves
    @ivar ClientLogger: This Client's logger instance.
    @type ClientLogger: L{PBLogger}
    @note: This class is dependent on a local installation of the Nova client
           process.
    '''
    def __init__(self, os_env_dict):
        super(BaseOpenstackCLIClient, self).__init__()
        self.base_command = None
        self.client_log = logging_tools.getLogger(
                            logging_tools.get_object_namespace(self.__class__))
        #Set up OS Environment by exporting all env vars passed to client
        self.os_env_dict = os_env_dict
        for key, value in os_env_dict.items():
            self.client_log.debug('setting {0}={1}'.format(key, value))
            os_putenv(str(key), str(value))

    def set_os_env_vars(self):
        '''
            Sets all os environment variables provided in os_env_dict
        '''
        for key, value in self.os_env_dict.items():
            self.client_log.debug('setting {0}={1}'.format(key, value))
            os_putenv(str(key), str(value))

    def unset_os_env_vars(self):
        '''
            Sets all os environment variables provided in os_env_dict
        '''
        for key, value in self.os_env_dict.items():
            self.client_log.debug('setting {0}={1}'.format(key, value))
            os_unsetenv(str(key), str(value))


class BaseRESTClient(BaseClient, RestConnector):
    '''
        Allows clients to inherit all requests-defined RESTfull verbs.
        This version inherits from both the client and the connector, but acts
        like a Client first in the mro

        requests documentation:
        http://docs.python-requests.org/en/latest/api/#configurations
    '''

    def __init__(self):
        super(BaseRESTClient, self).__init__()
        self.default_headers = {}

    def request(self, method, url, auth=None, headers=None, params=None, data=None,
                      requestslib_kwargs=None):

        #set requestslib_kwargs to an empty dict if None
        requestslib_kwargs = requestslib_kwargs if\
                                     requestslib_kwargs is not None else {}

        #Set defaults
        params = params if params is not None else {}
        headers = dict(self.default_headers, **(headers or {}))
        verify = False

        #Override url and method if present in requestslib_kwargs
        if 'url' in requestslib_kwargs.keys():
            url = requestslib_kwargs.get('url', None) or url
            del requestslib_kwargs['url']

        if 'method' in requestslib_kwargs.keys():
            method = requestslib_kwargs.get('method', None) or method
            del requestslib_kwargs['method']

        #Delete key:value pairs from requestslib_kwargs if the value=None
        for key, _ in requestslib_kwargs.items():
            if requestslib_kwargs[key] is None:
                del requestslib_kwargs[key]

        #Assign final values to requestslib_kwargs, but prevent this method's
        #kwarg's values from overwriting requestslib_kwargs values.
        requestslib_kwargs = dict({'headers': headers,
                                   'params': params,
                                   'verify': verify,
                                   'data': data},
                                   **requestslib_kwargs)

        #Return final requests response object
        return super(BaseRESTClient, self).request(method, url, auth=auth,
                                                          **requestslib_kwargs)


class BaseSOAPClient(BaseClient, SoapConnector):

    def __init__(self, wsdl, endpoint=None, username=None, password=None):
        BaseClient.__init__(self)
        SoapConnector.__init__(self, wsdl, endpoint, username, password)


class BaseMarshallingClient(BaseRESTClient):
    def __init__(self, serialize_format=None, deserialize_format=None):
        super(BaseMarshallingClient, self).__init__()
        self.serialize_format = serialize_format or 'json'
        self.deserialize_format = deserialize_format or self.serialize_format

    def request(self, method, url, headers=None, params=None, data=None, auth=None,
                      response_entity_type=None, request_entity=None,
                      requestslib_kwargs=None):
        #defaults requestslib_kwargs to a dictionary if it's None
        requestslib_kwargs = requestslib_kwargs if\
                                         requestslib_kwargs is not None else {}

        #set the 'data' paramater of the request to either what's already in
        #requestslib_kwargs, or the deserialized output of the request_entity
        if request_entity is not None:
            requestslib_kwargs = dict({'data': request_entity.serialize(
                                 self.serialize_format)}, **requestslib_kwargs)

        #Make the actual request
        response = super(BaseMarshallingClient, self).request(method, url, auth=auth,
                                    headers=headers, params=params, data=data,
                                    requestslib_kwargs=requestslib_kwargs)
        #Append the de/serialized data object to the response
        response.request.__dict__['entity'] = None
        response.__dict__['entity'] = None

        if response.request is not None:
            response.request.__dict__['entity'] = request_entity

        if response_entity_type is not None:
            response.__dict__['entity'] = \
                    response_entity_type.deserialize(response.content,
                                                     self.deserialize_format)
        return response
