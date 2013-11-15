'''
@summary: Classes and Utilities that provide low level connectivity to the
          Rest Client
@note: Should be consumed/exposed by a a L{ccengine.providers} class and
       rarely be used directly by any other object or process
@copyright: Copyright (c) 2012 Rackspace US, Inc.
'''
from ccengine.clients.base_client import BaseMarshallingClient
from ccengine.domain.compute.response.flavor import Flavor, FlavorMin
from urlparse import urlparse


class FlavorsApiClient(BaseMarshallingClient):

    def __init__(self, url, auth_token, serialize_format=None,
                 deserialize_format=None):
        '''
        @param logger: PBLogger instance to use, Generates private logger if
                       None
        @type logger: L{PBLogger}
        '''
        super(FlavorsApiClient, self).__init__(serialize_format,
                                               deserialize_format)
        self.auth_token = auth_token
        self.default_headers['X-Auth-Token'] = auth_token
        ct = ''.join(['application/', self.serialize_format])
        accept = ''.join(['application/', self.deserialize_format])
        self.default_headers['Content-Type'] = ct
        self.default_headers['Accept'] = accept
        self.url = url

    def list_flavors(self, min_disk=None, min_ram=None, marker=None,
                     limit=None, requestslib_kwargs=None):
        '''
        @summary: Returns a list of flavors
        @param min_disk: min Disk in GB, to filter by minimum Disk size in MB
        @type min_disk:int
        @param min_ram: min ram in GB, to filter by minimum RAM size in MB
        @type min_Disk:int
        @param marker: ID of last item in previous list (paginated collections)
        @type marker:C{str}
        @param limit: Sets page size
        @type limit: int
        @return: List of flavors filtered by params on success
        @rtype: C{list}
        '''

        '''
            GET
            v2/{tenant_id}/flavors
        '''
        url = '%s/flavors' % self.url

        params = {'minDisk': min_disk, 'minRam': min_ram, 'marker': marker,
                  'limit': limit}
        flavor_response = self.request('GET', url, params=params,
                                       response_entity_type=FlavorMin,
                                       requestslib_kwargs=requestslib_kwargs)
        return flavor_response

    def list_flavors_with_detail(self, min_disk=None, min_ram=None, marker=None,
                                 limit=None, requestslib_kwargs=None):
        '''
        @summary: Returns details from a list of flavors
        @param min_disk: min Disk in GB, to filter by minimum Disk size in MB
        @type min_disk:int
        @param min_ram: min ram in GB, to filter by minimum RAM size in MB
        @type min_Disk:int
        @param marker: ID of last item in previous list (paginated collections)
        @type marker:C{str}
        @param limit: Sets page size
        @type limit: int
        @return: Detail List of flavors filtered by params on success
        @rtype: C{list}
        '''
        '''
        GET
        v2/tenant_id/flavors/detail
        '''
        url = '%s/flavors/detail' % self.url

        params = {'minDisk': min_disk, 'minRam': min_ram, 'marker': marker,
                  'limit': limit}
        flavor_response = self.request('GET', url, params=params,
                                       response_entity_type=Flavor,
                                       requestslib_kwargs=requestslib_kwargs)
        return flavor_response

    def get_flavor_details(self, flavor_id, requestslib_kwargs=None):
        '''
        @summary: Returns a dict of details for given filter
        @param flavor_id: if of flavor for which details are required
        @type flavor_id:C{str}
        @return: Details of filter with filter id in the param on success
        @rtype: C{dict}
        '''
        '''
        GET
        v2/tenant_id/flavors/id
        '''
        url_new = str(flavor_id)
        url_scheme = urlparse(url_new).scheme
        url = url_new if url_scheme \
        else '%s/flavors/%s' % (self.url, flavor_id)

        flavor_response = self.request('GET', url, requestslib_kwargs,
                                       response_entity_type=Flavor,
                                       requestslib_kwargs=requestslib_kwargs)
        return flavor_response
