'''
@summary: Provider Module for Big Data Lava API
@copyright: Copyright (c) 2012 Rackspace US, Inc.
'''
import time
import json
from dateutil import parser
from datetime import datetime

from ccengine.providers.base_provider import BaseProvider, ProviderActionResult
from ccengine.providers.auth.auth_api import AuthProvider as _AuthProvider
from ccengine.clients.auth.auth_client import AuthClient as _AuthClient
from ccengine.clients.identity.v2_0.rax_auth_admin_api import IdentityAdminClient
from ccengine.clients.bigdata.lava_api_client import LavaAPIClient as\
    _LavaAPIClient
from ccengine.domain.bigdata.lava import Cluster as _Cluster, Node as _Node,\
    Type as _Type, Flavor as _Flavor
from ccengine.domain.types import LavaClusterStatusTypes as\
    _LavaClusterStatusTypes
from ccengine.domain.auth import Auth_2_0 as _Auth_2_0_DomainObject
from ccengine.domain.bigdata.lava import CloudCredentials, SSHKey
from ccengine.common.connectors.ssh import SSHConnector

class LavaAPIProvider(BaseProvider):

    '''
    @summary: Provides helper methods for Lava API functionality
    '''
    def __init__(self, config):
        super(LavaAPIProvider, self).__init__()
        self.config = config
        
        #Auth based on time to live
        auth_provider = _AuthProvider(config)
        auth_data = auth_provider.authenticate()
        expires_in = parser.parse(auth_data.token.expires).replace(tzinfo=None)
        current_time = datetime.now().replace(tzinfo=None)
        time_delta = expires_in - current_time
        ttl_hours = time_delta.total_seconds()/3600
        if ttl_hours < 2:
            identity_admin_client = IdentityAdminClient(
                url=config.auth.base_url,
                serialize_format='json',
                auth_token="my-simple-demo-token"
            )
            resp = identity_admin_client.revoke_token(auth_data.token.id)
            auth_data = auth_provider.authenticate()
        
        # Create a lava client
        base_url = config.lava_api.BASE_URL + config.auth.tenant_id + "/"
        self.lava_client = _LavaAPIClient(base_url,
                                          auth_data.token.id)

    def create_profile(self, username, password, ssh_keys, cloud_credentials):
        provider_action_result = ProviderActionResult()
        api_response = self.lava_client.Profiles.create(username,
                                                        password,
                                                        ssh_keys,
                                                        cloud_credentials)
        provider_action_result.response = api_response
        return provider_action_result

    def delete_profile(self,
                       username,
                       password,
                       api_key,
                       user_id,
                       tenant_id):
        auth_client = _AuthClient(self.config.auth.base_url,
                                  self.config.auth.version,
                                  username,
                                  password,
                                  api_key)
        response = auth_client.auth_2_0()
        ResponseDict = json.loads(response.content)
        auth_data = _Auth_2_0_DomainObject(ResponseDict)
        base_url = "{0}{1}/".format(
            self.config.lava_api.BASE_URL,
            self.config.auth.alt_tenant_id)
        lava_client = _LavaAPIClient(base_url,
                                     auth_data.token.id)
        api_response = lava_client.Profiles.get()
        if api_response.status_code != 404:
            api_response = lava_client.Clusters.list()
            clusters = api_response.entity
            for cluster in clusters:
                if not self.delete_cluster(
                    cluster.id,
                        timeout=self.config.lava_api.DELETE_CLUSTER_TIMEOUT):
                    return False
            lava_client.Profiles.delete(user_id=user_id)
            return True
        else:
            return True

    def get_flavor_id(self, flavor_name):
        flavors = self.lava_client.Flavors.list().entity
        for flavor in flavors:
            if flavor.name.lower().find(flavor_name) != -1:
                return flavor.id

    def create_cluster(self, name, count, type, flavor_name, timeout=500):
        '''
        @summary: Create a cluster and wait for it to have active status
        @param name: Name of cluster
        @type name: C{str}
        @param count: Number of nodes in cluster
        @type count: C{int}
        @param type: Type of cluster to create
        @type type: C{str}
        @param flavor_id: ID of flavor to assign cluster
        @type flavor_id: C{int}
        @return: The cluster is stored in the entity field.
        Whether a successful creation with active status was achieved is
        stored in the ok field.
        The last response from any LavaAPICall is stored in
        the response field.
        @rtype: L{ProviderActionResult}
        '''
        active_status = _LavaClusterStatusTypes.ACTIVE
        provider_action_result = ProviderActionResult()
        #flavor_type_compatible = self.check_type_flavor_combo(type, flavor_id)
        # if flavor_type_compatible:
        flavor_id = self.get_flavor_id(flavor_name)
        api_response = self.lava_client.Clusters.create(name, count, type,
                                                        flavor_id)
        provider_action_result.response = api_response
        if not api_response.ok:
            self.provider_log.warning("Create returned with an"
                                      " error for '%s'" % name)
            return provider_action_result
        created_cluster = provider_action_result.response.entity
        self.provider_log.info("Created Cluster: %s" % created_cluster)
        wait_response, msg = self.wait_for_cluster_status(
            created_cluster.id, active_status, timeout=timeout)
        return wait_response, msg

    def get_cluster(self, name):
        api_response = self.lava_client.Clusters.list()
        clusters = api_response.entity
        for cluster in clusters:
            if cluster is not None and cluster.name == name:
                return cluster

    def concurrent_cluster_create(self, flavor_id):
        cluster_count = 1
        cluster_type_list = []
        cluster_list = []
        flavors_class = self.lava_client.Flavors
        supported_types = flavors_class.list_supported_types(flavor_id)
        supported_types_json = json.loads(supported_types.content)
        cluster_types = supported_types_json['flavors']['types']
        for type in cluster_types:
            cluster_type_list.append(type['id'])

        for cluster_type in cluster_type_list:
            STAMP = datetime.now().microsecond
            cluster_name = "%s_%s_%d" % (flavor_id, cluster_type, STAMP)
            created_cluster = self.lava_client.Clusters.create(cluster_name,
                                                               cluster_count,
                                                               cluster_type,
                                                               flavor_id)
            created_cluster = json.loads(created_cluster.content)
            cluster_list.append(created_cluster)
        cluster_domain_objects = []
        for cluster in cluster_list:
            temp_clus_id = cluster['cluster'][0]['id']
            status_active = _LavaClusterStatusTypes.ACTIVE
            wait_result = self.wait_for_cluster_status(temp_clus_id,
                                                       status_active)
            cluster_domain_objects.append(wait_result.entity)
        return cluster_domain_objects

    def create_cluster_of_all_types(self, flavor_id):
        '''
        @summary: Creates clusters for all types of clusters that are
        compatible with the given flavor
        @param flavor_id: ID of flavor to create clusters with
        @type flavor_id: C{int}
        @return: List of created clusters
        @rtype: C{list}
        '''
        cluster_count = 1
        cluster_type_list = []
        cluster_list = []
        flavors_class = self.lava_client.Flavors
        supported_types = flavors_class.list_supported_types(flavor_id)
        supported_types_json = json.loads(supported_types.content)
        cluster_types = supported_types_json['flavors']['types']

        for type in cluster_types:
            cluster_type_list.append(type['id'])

        for cluster_type in cluster_type_list:
            STAMP = datetime.now().microsecond
            cluster_name = "%s_%s_%d" % (flavor_id, cluster_type, STAMP)
            create_result = self.create_cluster(cluster_name, cluster_count,
                                                cluster_type, flavor_id)
            if not create_result.ok:
                self.provider_log.warning("Cluster '%s' failed to create."
                                          % cluster_name)
            else:
                self.provider_log.info("Cluster '%s' created!" % cluster_name)
            cluster_list.append(create_result.entity)
        return cluster_list

    def check_flavor_exists(self, flavor_id):
        '''
        @summary: Check if flavors exist in the system
        @param flavor_id: ID of flavor that we are checking exists
        @type flavor_id: C{int}
        @return: If flavor exists
        @rtype: C{bool}
        '''
        api_response = self.lava_client.Flavors.list()
        if api_response.ok:
            api_response_json = json.loads(api_response.content)
            flavor_list = api_response_json['choices']
            self.provider_log.info('Available flavors: %s' % flavor_list)
            if flavor_list == []:
                self.provider_log.warning("There are no available flavors")
                return False

            for flavor in flavor_list:
                if str(flavor_id) == flavor['id']:
                    self.provider_log.info("Flavor '%s' is in the Flavor list"
                                           % (flavor_id))
                    return True
            self.provider_log.warning("Flavor '%s' is NOT in the Flavor list"
                                      % flavor_id)
            return False

        else:
            self.provider_log.warning("Lava list supported cluster Flavors "
                                      "API call failed with error:"
                                      " '#{0}' and status code '#{1}':"
                                      "\n '#{2}'".
                                      format(api_response.reason,
                                             api_response.status_code,
                                             json.loads(api_response.content)))
            return False

    def check_type_exists(self, type_id):
        '''
        @summary: Checks if the given type exists in the environment
        @param type_id: ID of type that we are checking exists
        @type type_id: C{str}
        @return: If type exists
        @rtype: C{bool}
        '''
        api_response = self.lava_client.Types.list()
        if api_response.ok:
            api_response_json = json.loads(api_response.content)
            type_list = api_response_json['types']
            if type_list == []:
                self.provider_log.warning("There are no available types.")
                return False

            for type in type_list:
                if type_id == type['id']:
                    self.provider_log.info("Type '%s' is in the Type list"
                                           % type_id)
                    return True
            self.provider_log.warning("Type '%s' is NOT in the Type list"
                                      % type_id)
            return False

        else:
            self.provider_log.warning("Lava list supported cluster Types API"
                                      " call failed with error: '%s' and"
                                      " status code '%s': \n '%s'"
                                      % (api_response.reason,
                                         api_response.status_code,
                                         json.loads(api_response.content)))
            return False

    def check_type_flavor_combo(self, type_id, flavor_id):
        '''
        @summary: Takes a list of supported types for the specified
                  flavor and checks if specified type is in the returned list
        @param type_id: Type ID to check for
        @type type_id: C{str}
        @param flavor_id: Flavor ID to check for supported types
        @type flavor_id: C{int}
        @return: True if type/flavor combo is compatible
        @rtype: C{bool}
        '''
        flavor_exists = self.check_flavor_exists(flavor_id)
        type_exists = self.check_type_exists(type_id)

        if flavor_exists and type_exists:
            flavors_class = self.lava_client.Flavors
            api_response = flavors_class.list_supported_types(flavor_id)
            api_response_json = json.loads(api_response.content)
            supported_types = api_response_json['flavors']['types']
            types_domain_object_list = self.convert_json_to_domain_object_list(
                supported_types, _Type)
            for type in types_domain_object_list:
                if type_id == type.id:
                    self.provider_log.info("Flavor '%s' and Type '%s' "
                                           "are compatible."
                                           % (flavor_id, type_id))
                    return True
            self.provider_log.warning("Flavor '%s' and Type '%s'"
                                      " are NOT compatible."
                                      % (flavor_id, type_id))
            return False
        self.provider_log.warning("Flavor '%s' or Type '%s' does NOT exist."
                                  % (flavor_id, type_id))
        return False

    def wait_for_cluster_status(self, cluster_id, expected_status,
                                timeout=500):
        '''
        @summary: Gets info on the given cluster waiting until it
                  reaches the timeout
        @param cluster_id: Cluster waiting for status
        @type cluster_id: C{str}
        @param expected_status: Status for cluster to reach
        @type expected_status: C{str}
        @param timeout: Maximum seconds to wait for cluster to reach status
        @type timeout: C{int}
        @return: The cluster is stored in the entity field.
        Whether the cluster reached the expected status was achieved is stored
        in the ok field.
        The last response from any LavaAPICall is stored in the response field.
        @rtype: L{ProviderActionResult}
        '''
        status = ['ERROR', 'BUILD', 'CONFIGURING', 'CONFIGURED', 'ACTIVE']
        self.provider_log.info(("Waiting for cluster id: {0} to reach"
                                " status {1} in {2} seconds").format(
                               cluster_id, expected_status, timeout))
        max_time = time.time() + timeout
        provider_action_result = ProviderActionResult()
        current_status = ""
        prev_status = ""
        number_of_errors = 0
        node_count = self.lava_client.Clusters.list_nodes(
            cluster_id).entity.count
        while (number_of_errors < node_count) and (time.time() < max_time):
            try:
                api_response = self.lava_client.Clusters.get_info(cluster_id)
                provider_action_result.response = api_response
                prev_status = current_status
                current_status = api_response.entity.status
                progress = api_response.entity.progress
            except Exception, wait_exception:
                exception_message = ("Exception waiting for cluster #{0}"
                                     ": status #{1}: #{2}").format(
                                         cluster_id, expected_status,
                                         wait_exception)
                self.provider_log.warning(exception_message)
                return provider_action_result, exception_message

            self.provider_log.debug(
                ("Waiting for cluster #{0} Status #{1}, current Status"
                 " is #{2}, Seconds remaining: #{3} . .").format(
                     cluster_id, expected_status, current_status,
                     max_time - time.time()))
            if current_status == expected_status:
                self.provider_log.info(
                    "Cluster {0} returned status {1}".format(cluster_id,
                                                             expected_status))
                provider_action_result.ok = True
                return provider_action_result, ""
            elif current_status == _LavaClusterStatusTypes.ERROR:
                if prev_status != "ERROR":
                    number_of_errors = number_of_errors + 1
                    max_time = time.time() + timeout
                    self.provider_log.warning(
                        "Error status: timeout reset to {0}".format(
                            max_time - time.time()))
                else:
                    continue
            else:
                if current_status != '' and prev_status != '' and \
                        status.index(current_status) < status.index(
                            prev_status):
                    status_sequence_message = (
                        "Improper status sequence: "
                        "Current Status: #{0},Previous Status: #{1}").format(
                            current_status, prev_status)
                    self.provider_log.error(status_sequence_message)
                    return provider_action_result, status_sequence_message
                if progress is None:
                    progress_message = "Progress not returned"
                    self.provider_log.error(progress_message)
                    return provider_action_result, progress_message
                '''
                Commented because of a communicated bug decided to be of
                low priority for Preview.
                '''
                # if progress < 0 or progress > 100:
                #    self.provider_log.error("Invalid progress: %s"
                #                            %(api_response.entity.progress))
                #    break
                time.sleep(
                    int(
                        self.config.lava_api.CLUSTER_SLEEP_INTERVAL))

        if number_of_errors == node_count:
            timeout_message = ("Unable to reach status: {0} Last Status {1}"
                               " because of max retries").format(
                                   expected_status, current_status)
            self.provider_log.info(timeout_message)
            return provider_action_result, timeout_message
        else:
            timeout_message = ("Unable to reach status: {0} Last Status {1}"
                               " because of timeout and no stat chan").format(
                                   expected_status, current_status)
            self.provider_log.info(timeout_message)
            return provider_action_result, timeout_message

    def delete_cluster(self, cluster_id, timeout=300):
        '''
        @summary: Make an API call to delete a cluster and
                  wait until it is deleted
        @param cluster_id: ID of cluster to be deleted
        @type cluster_id: C{int}
        @param timeout: Maximum seconds to wait for cluster to be deleted
        @type timeout: C{int}
        @return: Whether the cluster was successfully deleted
        @rtype: C{bool}
        '''
        api_response = self.lava_client.Clusters.delete(cluster_id)
        if not api_response.ok:
            self.provider_log.warning("Lava API call to delete cluster %s"
                                      "failed" % (cluster_id))
            return False
        max_time = time.time() + timeout
        while time.time() < max_time:
            api_response = self.lava_client.Clusters.get_info(cluster_id)
            if api_response.status_code == 404:
                self.provider_log.info("Cluster: %s deleted" % (cluster_id))
                return True
            time.sleep(3)
        self.provider_log.info("Cluster %s timed out on delete with status: %s"
                               % (cluster_id, api_response.entity.status))
        return api_response.ok

    def get_node_with_role(self, cluster, role):
        '''
        @summary: Iterated through cluster's nodes and returns its master node
        @param cluster: Cluster whose master node will be returned
        @type cluster: L{Cluster}
        @return: master node
        @rtype: L{Node}
        '''
        cluster_nodes = self.get_cluster_nodes(cluster)
        for node in cluster_nodes:
            if node.role == role:
                self.provider_log.info(
                    "node %s for cluster %s with role %s found" %
                    (node.private_ip, cluster.name, role))
                return node

    def get_cluster_nodes(self, cluster):
        '''
        @summary: Return all nodes in the cluster
        @param cluster: Cluster whose nodes will be returned
        @type cluster: L{Cluster}
        @return: List of node domain objects
        @rtype: C{list}
        '''
        api_response = self.lava_client.Clusters.list_nodes(cluster.id)
        return api_response.entity

    def create_ssh_connector(self, node, port=22):
        '''
        @summary: Creates an SSH connection, checks the connection
                  then returns ssh client
        @param node: Node to create the ssh session with
        @type node: L{Node}
        @return: Provides methods to execute commands via ssh
        @rtype: L{SSHConnector}
        '''
        username = self.config.lava_api.USER_NAME
        password = self.config.lava_api.PASSWORD

        self.provider_log.info('Creating SSH Session to test server')
        ssh_connector = SSHConnector(node.ip, username, password, 360, port)
        if ssh_connector.test_connection_auth():
            return ssh_connector

    def delete_active_clusters(self, client, clusters_to_delete):
        '''
        @summary: Iterate through list of clusters and delete any
                  with status "active"
        @param client: LavaAPIClient used to delete the clusters
        @type client: L{LavaAPIClient}
        @param clusters_to_delete: List of Clusters to delete
        @type clusters_to_delete: C{list}
        @return: None
        @rtype: None
        '''
        for cluster in clusters_to_delete:
            if cluster.status == _LavaClusterStatusTypes.ACTIVE:
                self.provider_log.info("Tear Down: Deleting cluster '%s'"
                                       % cluster.id)
                client.Clusters.delete(cluster.id)
