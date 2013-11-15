from ccengine.clients.base_client import BaseMarshallingClient
from ccengine.domain.compute.response.server import Server
from ccengine.domain.compute.response.admin import Hosts
from ccengine.domain.compute.request.server_requests import Rebuild, \
            CreateImage, RevertResize, CreateServer, RescueMode, \
            ExitRescueMode, AddFixedIP, RemoveFixedIP
from ccengine.domain.compute.request.server_requests import ChangePassword, \
                                                ConfirmResize, Resize, Reboot
from ccengine.domain.compute.metadata import MetadataItem, Metadata
from ccengine.common.tools.datagen import rand_name
from ccengine.domain.compute.response.rescue import Rescue
from urlparse import urlparse


class HostsAPIClient(BaseMarshallingClient):

    def __init__(self, url, auth_token, serialize_format=None,
                 deserialize_format=None):
        '''
        @param logger: PBLogger instance to use,
         Generates private logger if None
        @type logger: L{PBLogger}
        '''
        super(HostsAPIClient, self).__init__(serialize_format,
                                             deserialize_format)
        self.auth_token = auth_token
        self.default_headers['X-Auth-Token'] = auth_token
        ct = ''.join(['application/', self.serialize_format])
        accept = ''.join(['application/', self.deserialize_format])
        self.default_headers['Content-Type'] = ct
        self.default_headers['Accept'] = accept
        self.url = url

    def list_hosts(self, requestslib_kwargs=None):
        """
        @summary: Lists all hosts by service.
        @return: Response code and hosts by service
        @rtype: Integer(Response code) and List(hosts)
        """
        '''
            GET
            v2/{tenant_id}/servers?{params}
        '''
        url = '%s/os-hosts' % self.url
        server_response = self.request('GET', url,
                                       response_entity_type=Hosts,
                                       requestslib_kwargs=requestslib_kwargs)
        return server_response

    def describe_host(self, hostname, requestslib_kwargs=None):
        """
        @summary: Lists all hosts by service.
        @return: Response code and hosts by service
        @rtype: Integer(Response code) and List(hosts)
        """
        '''
            GET
            v2/{tenant_id}/servers?{params}
        '''
        url = '%s/os-hosts/%s' % (self.url, hostname)
        server_response = self.request('GET', url,
                                       response_entity_type=Hosts,
                                       requestslib_kwargs=requestslib_kwargs)
        return server_response
