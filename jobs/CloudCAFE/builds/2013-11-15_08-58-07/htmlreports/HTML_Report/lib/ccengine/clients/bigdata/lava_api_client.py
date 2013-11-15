'''
@summary: Client to make rest calls to the Lava API
@copyright: Copyright (c) 2012 Rackspace US, Inc.
'''
from ccengine.clients.base_client import BaseClient, BaseMarshallingClient
from ccengine.domain.bigdata.lava import Cluster as _Cluster,\
    Node as _Node, Type as _Type, Flavor as _Flavor, Profile as _Profile,\
    Resize as _Resize, Limits as _Limit


class LavaAPIClient(BaseClient):
    def __init__(self, url, auth_token, tenant_id, serialize_format='json',
                 deserialize_format='json'):
        super(LavaAPIClient, self).__init__()
        self.Clusters = _Clusters(url,
                                  auth_token,
                                  tenant_id,
                                  serialize_format,
                                  deserialize_format)
        self.Flavors = _Flavors(url,
                                auth_token,
                                tenant_id,
                                serialize_format,
                                deserialize_format)
        self.Types = _Types(url,
                            auth_token,
                            tenant_id,
                            serialize_format,
                            deserialize_format)
        self.Profiles = _Profiles(url,
                                  auth_token,
                                  tenant_id,
                                  serialize_format,
                                  deserialize_format)
        self.Limits = _Limits(url,
                              auth_token,
                              tenant_id,
                              serialize_format,
                              deserialize_format)

class _BaseLavaAPIClient(BaseMarshallingClient):
    def __init__(self, url, auth_token, tenant_id,
                 serialize_format, deserialize_format):
        super(_BaseLavaAPIClient, self).__init__(serialize_format,
                                                 deserialize_format)

        self.base_url = "{0}{1}/".format(url,
                                         tenant_id)
        headers = {'X-Auth-Token': auth_token,
                   'Content-Type': 'application/%s' % serialize_format,
                   'Accept': 'application/%s' % deserialize_format}
        self.rest_parameters = {'headers': headers, 'verify': False}


class _Flavors(_BaseLavaAPIClient):
    def __init__(self, url, auth_token, tenant_id,
                 serialize_format, deserialize_format):
        super(_Flavors, self).__init__(url,
                                       auth_token,
                                       tenant_id,
                                       serialize_format,
                                       deserialize_format)
        self.url = "{0}flavors".format(self.base_url)

    def list(self):
        '''
        @summary: GET /flavors - List flavors
        '''
        return self.request("GET",
                            self.url,
                            response_entity_type=_Flavor,
                            requestslib_kwargs=self.rest_parameters)

    def get_flavor_info(self, flavor_id):
        '''
        @summary: GET /flavors - List flavors
        '''
        return self.request("GET",
                            "{0}/{1}".format(self.url, flavor_id),
                            response_entity_type=_Flavor,
                            requestslib_kwargs=self.rest_parameters)

    def list_supported_types(self, flavor_id):
        '''
        @summary: GET /flavors/<flavor_id>/types - List supported types for
        flavor
        '''
        url = "{0}/{1}/types".format(self.url, flavor_id)
        return self.request("GET",
                            url,
                            response_entity_type=_Type,
                            requestslib_kwargs=self.rest_parameters)


class _Types(_BaseLavaAPIClient):
    def __init__(self, url, auth_token, tenant_id,
                 serialize_format, deserialize_format):
        super(_Types, self).__init__(url,
                                     auth_token,
                                     tenant_id,
                                     serialize_format,
                                     deserialize_format)
        self.url = "{0}types".format(self.base_url)

    def list(self):
        '''
        @summary: GET /types - List types
        '''
        return self.request("GET",
                            self.url,
                            response_entity_type=_Type,
                            requestslib_kwargs=self.rest_parameters)

    def list_supported_flavors(self, type_id):
        '''
        @summary: GET /types/<type_name>/flavors - List supported flavor for
        types
        '''
        url = "{0}/{1}/flavors".format(self.url,
                                       type_id)
        return self.request("GET", url,
                            response_entity_type=_Flavor,
                            requestslib_kwargs=self.rest_parameters)


class _Clusters(_BaseLavaAPIClient):
    def __init__(self, url, auth_token, tenant_id,
                 serialize_format, deserialize_format):
        super(_Clusters, self).__init__(url,
                                        auth_token,
                                        tenant_id,
                                        serialize_format,
                                        deserialize_format)
        self.url = "{0}clusters".format(self.base_url)

    def list(self):
        '''
        @summary: GET /clusters - List clusters
        This is a special case with _json_to_obj, in that a list with
        length == 1 is returned as an object.
        '''
        response = self.request("GET", self.url,
                                response_entity_type=_Cluster,
                                requestslib_kwargs=self.rest_parameters)
        if type(response.entity) != list:
            response.entity = [response.entity]
        return response

    def get_info(self, cluster_id):
        '''GET /clusters - List clusters'''
        url = "{0}/{1}".format(self.url,
                               str(cluster_id))
        return self.request("GET", url,
                            response_entity_type=_Cluster,
                            requestslib_kwargs=self.rest_parameters)

    def get_node(self, cluster_id, node_id):
        '''
        GET /clusters/cluster_id/nodes/node_id
        '''
        url = "{0}/{1}/nodes/{2}".format(self.url,
                                         str(cluster_id),
                                         node_id)
        return self.request("GET",
                            url,
                            response_entity_type=_Node,
                            requestslib_kwargs=self.rest_parameters)

    def create(self, cluster_name, count, cluster_type, cluster_flavor):
        '''
        @summary: Create a cluster
        '''
        cluster = _Cluster(cluster_name, count, cluster_type,
                           cluster_flavor)
        if 'data' in self.rest_parameters:
            del self.rest_parameters['data']
        return self.request("POST", self.url,
                            response_entity_type=_Cluster,
                            request_entity=cluster,
                            requestslib_kwargs=self.rest_parameters)

    def delete(self, cluster_id):
        return self.request("DELETE", "%s/%s" % (self.url, cluster_id),
                            response_entity_type=_Cluster,
                            requestslib_kwargs=self.rest_parameters)

    def list_nodes(self, cluster_id):
        return self.request("GET", "%s/%s/nodes" % (self.url, cluster_id),
                            response_entity_type=_Node,
                            requestslib_kwargs=self.rest_parameters)

    def resize(self, cluster_id, new_size):
        resize = _Resize(new_size)
        if 'data' in self.rest_parameters:
            del self.rest_parameters['data']
        return self.request("POST", "%s/%s/action" % (self.url,
                                                      cluster_id),
                            request_entity=resize,
                            response_entity_type=_Cluster,
                            requestslib_kwargs=self.rest_parameters)


class _Profiles(_BaseLavaAPIClient):
    def __init__(self, url, auth_token, tenant_id,
                 serialize_format, deserialize_format):
        super(_Profiles, self).__init__(url,
                                        auth_token,
                                        tenant_id,
                                        serialize_format,
                                        deserialize_format)
        self.url = "{0}profile".format(self.base_url)

    def get(self):
        '''
        @summary: Delete a profile
        '''
        return self.request("GET", self.url,
                            response_entity_type=_Profile,
                            requestslib_kwargs=self.rest_parameters)

    def delete(self, user_id):
        '''
        @summary: Delete a profile
        '''
        return self.request("DELETE", self.url + "/" + user_id,
                            response_entity_type=_Profile,
                            requestslib_kwargs=self.rest_parameters)

    def edit(self, email=None, user_id=None, username=None, password=None,
             ssh_keys=None, cloud_credentials=None):
        '''
        @summary: Edit a profile
        '''
        profile = _Profile(email=email,
                           user_id=user_id,
                           username=username,
                           password=password,
                           ssh_keys=ssh_keys,
                           cloud_credentials=cloud_credentials)
        return self.request("POST", self.url,
                            response_entity_type=_Profile,
                            request_entity=profile,
                            requestslib_kwargs=self.rest_parameters)

class _Limits(_BaseLavaAPIClient):
    def __init__(self, url, auth_token, tenant_id,
                 serialize_format, deserialize_format):
        super(_Limits, self).__init__(url,
                                      auth_token,
                                      tenant_id,
                                      serialize_format,
                                      deserialize_format)
        self.url = "{0}limits".format(self.base_url)

    def get(self):
        '''
        @summary: limits response
        '''
        return self.request("GET", self.url,
                            response_entity_type=_Limit,
                            requestslib_kwargs=self.rest_parameters)
