'''
@summary: Tests Lava (Big Data) REST API
@copyright: Copyright (c) 2012 Rackspace US, Inc.
'''

from ccengine.common.connectors import rest
from testrepo.common.testfixtures.fixtures import BaseParameterizedTestFixture
from ccengine.providers.bigdata.hadoop_provider import HadoopProvider
from ccengine.domain.bigdata.lava import Node as _Node, Flavor as _Flavor, \
    Type as _Type, CloudCredentials as _CloudCredentials, SSHKey as _SSHKey
from ccengine.domain.types import LavaClusterStatusTypes
from ccengine.common.connectors.ping import PingClient
from testrepo.bigdata.functional.lava_base_fixture import LavaBaseFixture
from ccengine.clients.remote_instance.linux.linux_instance_client \
    import LinuxClient
from ccengine.clients.bigdata.socksproxy import SocksProxyClient
from ccengine.common.tools.sshtools import generate_ssh_keys,\
    add_public_key_to_authorized_keys
from ccengine.common.connectors.ssh import SSHConnector

import json
import random
import time


class LavaAPITest(LavaBaseFixture):

    '''
    @summary: Basic smoke test for Big Data REST API
    '''

    def test_list_flavors(self):
        api_response = self.lava_client.Flavors.list()
        returned_flavor_list = api_response.entity
        self.assertTrue(api_response.ok,
                        "Lava list supported cluster Flavors API call failed"
                        "with error: '%s' and status code '%s'"
                        % (api_response.reason,
                           api_response.status_code))
        flavor_list = api_response.entity
        flavor_list_json = json.dumps(self.valid_flavors)
        expected_flavor_list = _Flavor.deserialize(flavor_list_json,
                                                   "json")
        self.assertEquals(expected_flavor_list, flavor_list)

    def test_list_types(self):
        api_response = self.lava_client.Types.list()
        returned_types_list = api_response.entity
        self.assertTrue(api_response.ok,
                        "Lava list supported cluster Types API call failed"
                        "with error: '%s' and status code '%s'"
                        % (api_response.reason,
                           api_response.status_code))
        types_list = api_response.entity
        expected_types_list = _Type.deserialize(json.dumps(self.valid_types),
                                                "json")
        self.assertEquals(types_list, expected_types_list)

    def test_type_list_for_flavor(self):
        for flavor_id in self.valid_types_for_flavor.keys():
            api_response = \
                self.lava_client.Flavors.list_supported_types(
                    flavor_id)
            self.assertTrue(api_response.ok,
                            "Lava API call to list supported cluster"
                            " Types for Flavor"
                            " '%s' failed with error: '%s', status code '%s'"
                            % (flavor_id,
                               api_response.reason,
                               api_response.status_code))
            type_list = api_response.entity
            valid_type_dict = self.valid_types_for_flavor[flavor_id]
            valid_type_list_json = json.dumps(valid_type_dict)
            valid_type_list = _Type.deserialize(valid_type_list_json, "json")
            self.assertEquals(type_list, valid_type_list)

    def test_flavor_list_for_type(self):
        for type_id in self.valid_flavors_for_type.keys():
            api_response = \
                self.lava_client.Types.list_supported_flavors(type_id)
            self.assertTrue(api_response.ok,
                            "Lava API call to list supported cluster"
                            " Flavors for Type"
                            " '%s' failed with error: '%s', status code '%s'"
                            % (type_id,
                               api_response.reason,
                               api_response.status_code))
            flavors_list = api_response.entity
            valid_flavors_dict = self.valid_flavors_for_type[type_id]
            valid_flavors_list_json = json.dumps(valid_flavors_dict)
            valid_flavor_list = _Flavor.deserialize(valid_flavors_list_json,
                                                    "json")
            self.assertEquals(flavors_list, valid_flavor_list)

    def test_add_cluster(self):
        limits_prev = self.lava_client.Limits.get().entity
        pac, message = self.lava_provider.create_cluster(
            self.cluster_name, self.cluster_size,
            self.cluster_type, self.cluster_flavor,
            int(self.config.lava_api.CLUSTER_CREATE_TIMEOUT))
        self.assertTrue(pac.ok,
                        "Lava API Create Cluster failed: \n{0} \n{1}".format(
                            pac.response.content,
                            message))
        self.cluster = pac.response.entity
        self.fixture_log.info("Added cluster: %s" % self.cluster.id)
        self.assertEqual(self.cluster.status,
                         LavaClusterStatusTypes.ACTIVE,
                         "Cluster '%s' created return status %s. Cluster: %s"
                         % (self.cluster_name,
                            self.cluster.status,
                            self.cluster))
        self.assertEqual(self.cluster.name,
                         self.cluster_name,
                         "Cluster '%s' created with incorrect name"
                         % (self.cluster_name))
        self.assertEqual(self.cluster.type,
                         self.cluster_type,
                         "Cluster '%s' created with incorrect type"
                         % (self.cluster_name))
        self.assertEqual(self.cluster.count,
                         self.cluster_size,
                         "Cluster '%s' created with incorrect count"
                         % (self.cluster_name))
        self.assertEqual(self.cluster.flavor,
                         self.lava_provider.get_flavor_id(self.cluster_flavor),
                         "Cluster '%s' created with incorrect flavor"
                         % (self.cluster_name))
        tenant_id = self.config.auth.tenant_id
        expected_self_link = self.config.lava_api.BASE_URL + \
            tenant_id + "/" + "clusters/" +\
            self.cluster.id
        expected_bookmark_link = self.config.lava_api.VERSIONLESS_LINK + \
            tenant_id + \
            "/" + "clusters/" + self.cluster.id
        self.assertEqual(self.cluster.sel, expected_self_link,
                         "Expected: %s, Recieved: %s"
                         % (expected_self_link, self.cluster.sel))
        self.assertEqual(self.cluster.bookmark, expected_bookmark_link,
                         "Expected: %s, Recieved: %s"
                         % (expected_bookmark_link, self.cluster.bookmark))
        limits_new = self.lava_client.Limits.get().entity

        nodes = self.lava_provider.get_cluster_nodes(self.cluster)
        for node in nodes:
            self.assertEqual(node.status,
                             LavaClusterStatusTypes.ACTIVE,
                             "Node {0} status {1}".format(
                                 node.ip, node.status))

        # node count
        limits_update = limits_prev.nodeCount.remaining -\
            limits_new.nodeCount.remaining
        self.assertTrue(limits_update == self.cluster.count,
                        "Previous: %s, Now :%s"
                        % (limits_prev.nodeCount.remaining,
                           limits_new.nodeCount.remaining))
        # vcpus
        vcpus_update = limits_prev.vcpus.remaining -\
            limits_new.vcpus.remaining
        flavor_info = self.lava_client.Flavors.get_flavor_info(
            self.cluster.flavor).entity
        vcpu_for_cluster = flavor_info.vcpus * self.cluster.count
        self.assertTrue(vcpu_for_cluster == vcpus_update,
                        "Previous: %s, Now :%s"
                        % (limits_prev.vcpus.remaining,
                           limits_new.vcpus.remaining))
        # ram
        # disk space

    def test_cluster_nodes(self):
        hadoop_provider = HadoopProvider(self.config, self.cluster)
        self.assertTrue(hadoop_provider.verify_data_nodes_dfsadmin(
            self.cluster_flavor),
            "Data nodes invalid for this cluster")
        nodes = self.lava_provider.get_cluster_nodes(self.cluster)
        for i in xrange(len(nodes)):
            # Check ssh keys
            key_filenames = []
            key_filenames.append(
                "/tmp/" + self.config.lava_api.PROFILE_KEY_FILE_NAME)
            key_ssh_connector = SSHConnector(nodes[i].ip,
                                             self.config.lava_api.USER_NAME,
                                             key_filenames=key_filenames
                                             )
            self.assertTrue(
                key_ssh_connector.test_connection_auth(),
                "{0} nodes cannot be ssh'd into using key".format(
                    nodes[i].ip))
            for j in xrange(len(nodes)):
                ssh_client = self.lava_provider.create_ssh_connector(nodes[i])
                response = (PingClient.ping_using_remote_machine(ssh_client,
                    nodes[j].ip) != 100)
                self.assertTrue(response,
                                "%s cannot ping %s"
                                % (nodes[i].ip, nodes[j].ip))
        gateway_node_count = 0
        master_node_count = 0
        for node in nodes:
            if node.role == "NAMENODE":
                master_node_count = master_node_count + 1
            if node.role == "GATEWAY":
                gateway_node_count = gateway_node_count + 1
        self.assertTrue(gateway_node_count == 1,
                        "Gateway node absent")
        self.assertTrue(master_node_count == 1,
                        "Master node absent")
        self.assertTrue(len(nodes) == self.cluster.count + 2,
                        "Node count invalid: Got %s Expected: %s"
                        % (len(nodes), self.cluster.count + 2))

    def test_node_web_pages(self):
        hadoop_provider = HadoopProvider(self.config, self.cluster)
        gateway_node = self.lava_provider.get_node_with_role(self.cluster,
                                                             "GATEWAY")
        socks_port = int(self.config.lava_api.SOCKS_PROXY_PORT)
        socks_client = SocksProxyClient(
            proxy_host=gateway_node.ip,
            username=self.config.lava_api.USER_NAME,
            id_file="/tmp/"+self.config.lava_api.PROFILE_KEY_FILE_NAME,
            proxy_port=socks_port)
        # Socks proxy doesnt return an acknowldgement, so hard coded timeout
        self.assertTrue(
            socks_client.start_socks_proxy(),
            "\nStandard output: {0} \n Standard error: {1}".format(
                socks_client.os_response.StandardOut,
                socks_client.os_response.StandardError))
        # Socks proxy doesnt return an acknowldgement, so hard coded timeout
        time.sleep(4)
        name_node_dfs_hc = hadoop_provider.verify_master_dfs_health_check(
            proxy_url="127.0.0.1",
            proxy_port=socks_port,
            timeout=int(self.config.lava_api.HADOOP_WEB_PAGE_TIMEOUT)
        )
        name_node_jbt = hadoop_provider.verify_job_tracker_page(
            proxy_url="127.0.0.1",
            proxy_port=int(self.config.lava_api.SOCKS_PROXY_PORT),
            timeout=int(self.config.lava_api.HADOOP_WEB_PAGE_TIMEOUT))
        task_tracker_pages = {}
        for node in self.lava_provider.get_cluster_nodes(self.cluster):
            if str(node.role) != "NAMENODE" and \
                    str(node.role) != "GATEWAY":
                task_tracker_pages[node.private_ip] = \
                    hadoop_provider.\
                    verify_task_tracker(node,
                                        proxy_url="127.0.0.1",
                                        proxy_port=socks_port,
                                        timeout=int(
                                        self.config.lava_api.
                                        HADOOP_WEB_PAGE_TIMEOUT))
        tt_urls_on_pages, tt_urls_on_error = hadoop_provider.\
            verify_task_tracker_urls_on_pages(
                proxy_url="127.0.0.1",
                proxy_port=socks_port
            )
        socks_client.end_socks_proxy()
        self.assertTrue(name_node_dfs_hc,
                        "DFS Health page failed to launch")
        self.assertTrue(name_node_jbt,
                        "Job Tracker page failed to launch.")
        for node in self.lava_provider.get_cluster_nodes(self.cluster):
            if str(node.role) != "NAMENODE" and \
                    str(node.role) != "GATEWAY":
                self.assertTrue(task_tracker_pages[node.private_ip],
                                "{0} failed task tracker".format(
                                    node.private_ip)
                                )
        self.assertTrue(tt_urls_on_pages, "{0}".format(tt_urls_on_error))

    def test_get_node(self):
        for node in self.lava_provider.get_cluster_nodes(self.cluster):
            api_response = self.lava_client.Clusters.get_node(self.cluster.id,
                                                              node.id)
            self.assertTrue(api_response.ok, "%s not OK" % api_response)
            cur_node = api_response.entity
            self.assertEqual(cur_node.id, node.id,
                             "%s not found" % node.id)
            tenant_id = self.config.auth.tenant_id
            expected_self_link = self.config.lava_api.BASE_URL + \
                tenant_id + "/clusters/" + self.cluster.id
            expected_bookmark_link = self.config.lava_api.VERSIONLESS_LINK +\
                tenant_id + "/clusters/" + \
                self.cluster.id
            self.assertEqual(self.cluster.sel, expected_self_link,
                             "Expected: %s, Recieved: %s"
                             % (expected_self_link, self.cluster.sel))
            self.assertEqual(self.cluster.bookmark, expected_bookmark_link,
                             "Expected: %s, Recieved: %s"
                             % (expected_bookmark_link, self.cluster.bookmark))

    def test_manual_ssh_key_addition(self):
        man_keyfile_name = self.config.lava_api.MANUAL_KEY_FILE_NAME
        keyfilepath = "/tmp"
        result, error = generate_ssh_keys(
            keyfilename=man_keyfile_name,
            keyfilepath=keyfilepath)
        self.assertTrue(result,
                        "SSH Key error: {0}".format(error))
        nodes = self.lava_provider.get_cluster_nodes(self.cluster)
        public_key = open("{0}/{1}.pub".format(keyfilepath,
                                               man_keyfile_name)).read()
        for node in nodes:
            add_key_result = add_public_key_to_authorized_keys(
                public_key,
                node.ip,
                self.config.lava_api.USER_NAME,
                self.config.lava_api.PASSWORD)
            self.assertTrue(
                add_key_result,
                "SSH Key wasn't appended for node: {0}".format(
                    node.ip))
            
            # Check ssh keys
            key_filenames = []
            key_filenames.append(
                "/tmp/{0}".format(self.config.lava_api.MANUAL_KEY_FILE_NAME))
            key_ssh_connector = SSHConnector(node.ip,
                                             self.config.lava_api.USER_NAME,
                                             key_filenames=key_filenames
                                             )
            self.assertTrue(
                key_ssh_connector.test_connection_auth(),
                "{0} nodes cannot be ssh'd into using key".format(
                    node.ip))

    def test_update_profile(self):
        ccs = _CloudCredentials(self.config.auth.username,
                                self.config.auth.api_key)
        profiles_client = self.lava_client.Profiles
        prof_keyfile_name = self.config.lava_api.PROFILE_KEY_FILE_NAME
        result, error = generate_ssh_keys(
            keyfilename=prof_keyfile_name,
            keyfilepath="/tmp")
        self.assertTrue(result,
                        "SSH Key error: {0}".format(error))
        ssh_key_obj = _SSHKey(prof_keyfile_name,
                              open(
                                "/tmp/" + prof_keyfile_name + ".pub").read())
        ssh_keys = []
        ssh_keys.append(ssh_key_obj)
        api_response = profiles_client.edit(username=
                                            self.config.lava_api.USER_NAME,
                                            password=
                                            self.config.lava_api.PASSWORD,
                                            cloud_credentials=ccs,
                                            ssh_keys=ssh_keys)
        self.assertTrue(api_response.status_code == 200,
                        "Profile create failed with %s"
                        % (api_response.content))
        profile_created = api_response.entity
        self.assertTrue(profile_created, "Erronoeus profile response: %s"
                        % (api_response.content))
        self.assertEqual(profile_created.username,
                         self.config.lava_api.USER_NAME)
        self.assertEqual(profile_created.cloud_credentials.username,
                         ccs.username)
        if len(profile_created.ssh_keys) > 1:
            for ssh_key in profile_created.ssh_keys:
                if ssh_key['name'] == \
                self.config.lava_api.PROFILE_KEY_FILE_NAME:
                    break
            else:
                self.assertTrue(
                    False,
                    "{0} key not found in the profile".format(
                        self.config.lava_api.PROFILE_KEY_FILE_NAME))
        else:
            self.assertEquals(
                profile_created.ssh_keys[0].name,
                self.config.lava_api.PROFILE_KEY_FILE_NAME)

    def test_list_clusters(self):
        api_response = self.lava_client.Clusters.list()
        api_response_json = json.loads(api_response.content)
        self.assertTrue(api_response.ok,
                        "Lava List Clusters API Call failed with error:"
                        " '%s' and status code '%s': \n '%s'"
                        % (api_response.reason,
                           api_response.status_code,
                           api_response_json))
        cluster_list = api_response.entity
        self.assertNotEqual(cluster_list, [], "Returned Empty List")
        self.assertIn(self.cluster,
                      cluster_list,
                      "Cluster %s not in list"
                      % self.cluster_name)

    def test_get_cluster_info(self):
        api_response = self.lava_client.Clusters.get_info(self.cluster.id)
        api_response_json = json.loads(api_response.content)
        self.assertTrue(api_response.ok,
                        "Lava Get Cluster Info API Call failed"
                        " with error: '%s' and status code '%s': \n '%s'"
                        % (api_response.reason,
                           api_response.status_code,
                           api_response_json))
        self.assertEqual(api_response.entity, self.cluster,
                         "Clusters do not match")

    def test_delete_cluster(self):
        limits_prev = self.lava_client.Limits.get().entity
        if self.cluster.status != LavaClusterStatusTypes.ERROR:
            self.fixture_log.info("Deleting cluster: %s" % self.cluster)
            is_cluster_deleted = self.lava_provider.delete_cluster(
                self.cluster.id)
            self.assertTrue(is_cluster_deleted,
                            "Lava delete cluster failed")
            limits_new = self.lava_client.Limits.get().entity
            # node count
            limits_update = limits_new.nodeCount.remaining -\
                limits_prev.nodeCount.remaining
            self.assertTrue(limits_update == self.cluster.count,
                            "Previous: %s, Now :%s"
                            % (limits_prev.nodeCount.remaining,
                               limits_new.nodeCount.remaining))
            # vcpus
            vcpus_update = limits_new.vcpus.remaining -\
                limits_prev.vcpus.remaining
            flavor_info = self.lava_client.Flavors.get_flavor_info(
                self.cluster.flavor).entity
            vcpu_for_cluster = flavor_info.vcpus * self.cluster.count
            self.assertTrue(vcpu_for_cluster == vcpus_update,
                            "Previous: %s, Now :%s"
                            % (limits_prev.vcpus.remaining,
                               limits_new.vcpus.remaining))

    def test_resize_cluster(self):
        cluster_size = self.cluster.count
        cluster_new_size = random.randint(cluster_size + 1,
                                          cluster_size + 5)
        response = self.lava_provider.lava_client.Clusters.resize(
            self.cluster.id,
            cluster_new_size)
        self.assertTrue(response.ok, "API call to resize"
                        " Cluster: %s to new size: %s failed. Response: %s"
                        % (self.cluster,
                           cluster_new_size,
                           response.content))
        wait_result, msg = self.lava_provider.wait_for_cluster_build(
            self.cluster.id, resize=True)
        resized_cluster = wait_result.response.entity
        self.assertTrue(
            wait_result.ok,
            "Cluster {0} failed to reach status {1} due to msg {2}".format(
                resized_cluster, LavaClusterStatusTypes.ACTIVE, msg))
        self.assertEqual(resized_cluster.count,
                         cluster_new_size,
                         "Nodecount is not as expected")
        nodes = self.lava_provider.get_cluster_nodes(self.cluster)
        for node in nodes:
            self.assertEqual(node.status,
                             LavaClusterStatusTypes.ACTIVE,
                             "Node {0} status {1}".format(
                                 node.ip, node.status))

    def test_restart_all_nodes(self):
        nodes = self.lava_provider.get_cluster_nodes(self.cluster)
        for node in nodes:
            linux_client = LinuxClient(node.ip,
                                       "",
                                       "",
                                       self.config.lava_api.USER_NAME,
                                       self.config.lava_api.PASSWORD)
            self.assertTrue(linux_client.reboot(
                timeout=int(
                    self.config.lava_api.NODE_REBOOT_TIMEOUT)),
                "%s did not reboot" % (node.ip))
        time.sleep(30)
