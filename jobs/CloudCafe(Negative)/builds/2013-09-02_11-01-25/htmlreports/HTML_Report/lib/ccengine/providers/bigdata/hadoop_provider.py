'''
@summary: Provider for Hadoop Commands
@copyright: Copyright (c) 2012 Rackspace US, Inc.
'''
from ccengine.providers.base_provider import BaseProvider
from ccengine.common.connectors.ssh import SSHConnector
from ccengine.common.connectors import rest
from ccengine.clients.bigdata.hadoop_client import HadoopClient
from ccengine.clients.bigdata.hadoop_client import _DfsAdmin
from ccengine.providers.bigdata.lava_api import LavaAPIProvider
from ccengine.clients.remote_instance.linux.linux_instance_client \
    import LinuxClient

import pycurl
import human_curl as hurl
from human_curl.exceptions import CurlError
import subprocess
from StringIO import StringIO
import math


class HadoopProvider(BaseProvider):
    def __init__(self, config, cluster):
        super(HadoopProvider, self).__init__()
        self.config = config
        self.lava_provider = LavaAPIProvider(self.config)
        self.cluster = cluster
        self.gateway_node = self.lava_provider.get_node_with_role(cluster,
                                                                  "GATEWAY")
        self.name_node = self.lava_provider.get_node_with_role(cluster,
                                                               "NAMENODE")
        self.ssh_connector = SSHConnector(self.gateway_node.ip,
                                          self.config.lava_api.USER_NAME,
                                          self.config.lava_api.PASSWORD)
        self.cluster_nodes = self.lava_provider.get_cluster_nodes(cluster)

    def verify_file_in_folder(self, filename, folder=''):
        '''
        @summary: Call hadoop filesystem to list contents in a folder.
        Return whether the response contains the substring matching
        the file name.
        @param filename: Name of file to verify is in folder
        @type filename: C{str}
        @param folder: Name of folder to search for file in. Defaults to
                       empty string (home directory)
        @type folder: C{str}
        @return: Whether the filename is found in the folder contents
        @rtype: C{bool}
        '''
        hadoop_client = HadoopClient(self.config.lava_api.USER_NAME,
                                     self.config.lava_api.PASSWORD,
                                     self.gateway_node.ip)
        response = hadoop_client.filesystem.list(folder)
        if response.find(filename) == -1:
            self.provider_log.warning("File: %s not found in Folder: %s"
                                      % (filename, folder))
            return False
        self.provider_log.info("File: %s found in Folder: %s"
                               % (filename, folder))
        return True

    def verify_data_nodes_dfsadmin(self, flavor_name):
        '''
        @summary: Uses dfsadmin -report to get a list of datanodes.
        Verifies that the datanode count is exactly one less than cluster
        node count.
        Verifies that each slave node in cluster_nodes is a datanode
        @param cluster_nodes: List of nodes in a cluster
        @type cluster_nodes: C{list} of C{Node Domain Object}
        @return: True if the cluster nodes meet the criteria for
        dfsadmin -report
        @rtype: C{bool}
        '''
        cluster_nodes = self.lava_provider.get_cluster_nodes(self.cluster)
        dfs_admin_client = _DfsAdmin(self.config.lava_api.USER_NAME,
                                     self.config.lava_api.PASSWORD,
                                     self.gateway_node.ip)
        output = dfs_admin_client.report()
        self.provider_log.info("Output from dfsadmin report"
                               ": %s\nLooking for data nodes:%s"
                               % (output, cluster_nodes))
        data_node_count = len(cluster_nodes) - 2
        result = output.find("Datanodes available: %s" % data_node_count) != -1
        if not result:
            self.provider_log.warning(
                "Expected data node count: {0} not found".format(
                    data_node_count))
            return False
        for datanode in cluster_nodes:
            if datanode.role == 'DATANODE':
                result = output.find(
                    "Name: {0}".format(datanode.private_ip)) != -1
                if not result:
                    self.provider_log.warning("Data node: %s not in %s"
                                              % datanode.private_ip, output)
                    return False
                else:
                    '''
                    verify disk space and ram if they stick to the flavor
                    '''
                    flavor_id = self.lava_provider.get_flavor_id(flavor_name)
                    flavor_response = self.lava_provider.\
                        lava_client.Flavors.get_flavor_info(
                            flavor_id)
                    flavor = flavor_response.entity
                    flavor_disk_space = int(flavor.disk)
                    linux_client = LinuxClient(datanode.ip,
                                               None,
                                               None,
                                               self.config.lava_api.USER_NAME,
                                               self.config.lava_api.PASSWORD)
                    data_node_size = linux_client.get_disk_size_in_gb(
                        self.config.lava_api.EPHEMERAL_DISK_PATH) + \
                        linux_client.get_disk_size_in_gb(
                            self.config.lava_api.PRIMARY_DISK_PATH)
                    delta = ((flavor_disk_space - data_node_size) * 100)\
                        / flavor_disk_space
                    if delta > 7:
                        self.provider_log.warning(
                            "Data node: #{0} disk size #{1}, not #{2}".format(
                                str(datanode.ip),
                                str(data_node_size),
                                str(flavor_disk_space)))
                        return False
        return True

    def make_request_with_proxy(self,
                                request_url,
                                proxy_url,
                                proxy_port,
                                timeout=10):
        self.provider_log.info("Pycurl request: {0}".format(request_url))
        self.provider_log.info("Pycurl proxy url: {0}".format(proxy_url))
        self.provider_log.info("Pycurl proxy port: {0}".format(
            str(proxy_port)))
        try:
            if proxy_url is not None and proxy_port is not None:
                r = hurl.get(request_url,
                             proxy=('socks5', (proxy_url, proxy_port)),
                             timeout=timeout)
            else:
                r = hurl.get(request_url,
                             timeout=timeout)
                self.provider_log.info(
                    "Pyccurl Response: {0}".format(
                        r.content
                    )
                )
        except CurlError, e:
            self.provider_log.info(
                    "Pyccurl Exception: {0}".format(
                        e.message
                    )
                )
            return e.message
        return r.content

    def verify_hadoop_home_web(self,
                               proxy_url,
                               proxy_port,
                               timeout=10):
        hadoop_web = "http://" + self.gateway_node.ip
        response = self.make_request_with_proxy(
            hadoop_web,
            proxy_url,
            proxy_port,
            timeout)
        jobt_string = "Hadoop Cluster Status"
        return response.find(jobt_string) != -1

    def verify_task_tracker_urls_on_pages(self,
                                          proxy_url,
                                          proxy_port,
                                          timeout=10):
        hadoop_pages = ["http://0.0.0.0/",
                        "http://{0}:50030/machines.jsp?type=active".format(
                            self.name_node.private_ip)]
        for page in hadoop_pages:
            response = self.make_request_with_proxy(page,
                                                    proxy_url,
                                                    proxy_port,
                                                    timeout)
            for node in self.cluster_nodes:
                tt_url_ip = "http://{0}:50060/".format(node.private_ip)
                tt_url_name = "http://{0}:50060/".format(node.name)
                if node.role == "DATANODE":
                    res = response.find(tt_url_ip) == -1 or \
                        response.find(tt_url_name) == -1
                    if not res:
                        return False,
                        "{0} does not have task tracker url {1} or {2}".format(
                            page,
                            tt_url_ip,
                            tt_url_name
                        )
        return True, ""

    def verify_job_tracker_page(self,
                                proxy_url,
                                proxy_port,
                                timeout=10):
        jbt_url = "http://{0}:50030/jobtracker.jsp".format(
            self.name_node.private_ip)
        response = self.make_request_with_proxy(
            jbt_url,
            proxy_url,
            proxy_port,
            timeout)
        jobt_string = "Hadoop Map/Reduce Administration"
        return response.find(jobt_string) != -1

    def verify_master_dfs_health_check(self,
                                       proxy_url,
                                       proxy_port,
                                       timeout=10):
        dfs_url = "http://{0}:50070/dfshealth.jsp".format(
            self.name_node.private_ip)
        response = self.make_request_with_proxy(
            dfs_url,
            proxy_url,
            proxy_port,
            timeout=20)
        return response.find("Cluster Summary") != -1

    def verify_task_tracker(self,
                            slave,
                            proxy_url,
                            proxy_port,
                            timeout=10):
        slave_name = ""
        i = 0
        for node in self.cluster_nodes:
            if node.role == "slave":
                i = i + 1
                if(node.id == slave.id):
                    slave_name = "slave-%s" % i
        tt_url = "http://{0}:50060/tasktracker.jsp".format(
            slave.private_ip)
        response = self.make_request_with_proxy(
            tt_url,
            proxy_url,
            proxy_port,
            timeout)
        result = response.find("Running tasks") != -1
        return result

    def get_max_hdfs(self):
        flavor_id = self.cluster.flavor
        flavor = self.lava_provider.lava_client.Flavors.get_flavor_info(
            flavor_id).entity
        size = flavor.disk * 1073741824 * self.cluster.count
        size = size - 0.15 * (size)
        # replication factor
        size = size / int(self.config.lava_api.HADOOP_REPLICATION_COUNT)
        return size

    def run_max_tera_sort(self):
        # Get available hdfs before trying to build some
        sort_size = self.get_max_hdfs()
        sort_size = 0.25 * (sort_size)
        sort_size = math.trunc(sort_size / 100)
        data_gen_path = "/user/{0}/terasort-input".format(
            self.config.lava_api.USER_NAME)
        tera_sort_output_path = "/user/{0}/terasort-output".format(
            self.config.lava_api.USER_NAME)
        tera_sort_validate_path = "/user/{0}/terasort-validate".format(
            self.config.lava_api.USER_NAME)

        # Free the space if the folders already exist
        hadoop_client = HadoopClient(self.config.lava_api.USER_NAME,
                                     self.config.lava_api.PASSWORD,
                                     self.gateway_node.ip)
        hadoop_client.filesystem.rmr(data_gen_path,
                                     skip_trash=True)
        hadoop_client.filesystem.rmr(tera_sort_output_path,
                                     skip_trash=True)
        hadoop_client.filesystem.rmr(tera_sort_validate_path,
                                     skip_trash=True)

        self.ssh_connector.exec_shell_command("cd /usr/lib/hadoop")

        # Run and test the success of all the 3 steps in the job
        output, prompt = self.ssh_connector.exec_shell_command_wait_for_prompt(
            "hadoop jar hadoop-examples.jar teragen {0} {1}".format(
                str(sort_size),
                data_gen_path),
            "lavaqe@GATEWAY",
            timeout=int(self.config.lava_api.TERA_SORT_TIMEOUT))
        if output.find("Job complete") == -1:
            return False, "TeraGen failed with output: {0}".format(
                output
            )
        output, prompt = self.ssh_connector.exec_shell_command_wait_for_prompt(
            "hadoop jar hadoop-examples.jar terasort {0} {1}".format(
                data_gen_path,
                tera_sort_output_path),
            "lavaqe@GATEWAY",
            timeout=int(self.config.lava_api.TERA_SORT_TIMEOUT))
        if output.find("INFO terasort.TeraSort: done") == -1:
            return False, "TeraSort failed with output: {0}".format(
                output
            )
        output, prompt = self.ssh_connector.exec_shell_command_wait_for_prompt(
            "hadoop jar hadoop-examples.jar teravalidate {0} {1}".format(
                tera_sort_output_path,
                tera_sort_validate_path),
            "lavaqe@GATEWAY",
            timeout=int(self.config.lava_api.TERA_SORT_TIMEOUT))
        if output.find("Job complete") == -1:
            return False, "TeraValidate failed with output: {0}".format(
                output
            )
        return True, ""
