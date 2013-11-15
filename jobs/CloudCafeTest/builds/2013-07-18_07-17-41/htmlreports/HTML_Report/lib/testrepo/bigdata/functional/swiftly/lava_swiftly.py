'''
@summary: Functional test for transferring files using Swiftly.
@copyright: Copyright (c) 2012 Rackspace US, Inc.
'''
from ccengine.providers.bigdata.lava_api import LavaAPIProvider as _LavaAPIProvider
from ccengine.providers.bigdata.swiftly_provider import SwiftlyProvider
from ccengine.clients.bigdata.hadoop_client import HadoopClient
from testrepo.common.testfixtures.fixtures import BaseParameterizedTestFixture
from testrepo.bigdata.functional.lava_base_fixture import LavaBaseFixture
import ccengine.common.tools.filetools as file_tools

class LavaSwiftlyTest(LavaBaseFixture):

    def test_swiftly_node_to_cloud_files(self):
        '''
        @summary: Parameterized Test uses SWIFTLY to UPLOAD a specified file 
                  from the node to Cloud Files.
        @ivar test_record['cluster_name']: The cluster that the node belongs to
        @ivar test_record['test_file']: The file to be copied.
        @ivar test_record['container_name']: Name of container 
                                            to to be created and used
        '''
        gateway_node = self.lava_provider.get_node_with_role(self.cluster,
                                                            "GATEWAY")
        swiftly_provider = SwiftlyProvider(self.config, gateway_node)
        container_name = 'test_container'
        test_file_path = file_tools.get_testfile(multiplier="kilo", 
                                           scalar_size = 1)
        test_file = test_file_path.split("/")[-1]
        ssh_connector = self.lava_provider.create_ssh_connector(gateway_node)
        self.assertTrue(ssh_connector.upload_a_file(test_file,test_file_path),
                        "%s not uploaded"%test_file)
        self.fixture_log.info("Creating container '%s' in Cloud Files "\
                              "using swiftly" % container_name)
        response = swiftly_provider.create_container(container_name)
        self.assertIsNotNone(response, "Returned None when "+
                             "running 'swiftly put'.")
        self.fixture_log.info("Putting an object '%s' into "\
                              "Cloud Files" % test_file)
        response = swiftly_provider.create_file(container_name, 
                                                test_file, 
                                                test_file)
        self.assertIsNotNone(response, "Returned None when"+
                             " running 'swiftly get'.")
        file_list = swiftly_provider.get_container_objects(container_name)
        self.assertIn(test_file, file_list, "File '%s' was not added on "\
                      "Cloud Files when using Swiftly." % test_file)
        swiftly_provider.delete_container(container_name)

    def test_swiftly_cloud_files_to_hdfs(self):
        '''
        @summary: Parameterized Test uses SWIFTLY to UPLOAD a the FIRST file in
                  the Cloud Files to the Hadoop File System.
        @ivar test_record['cluster_name']: The cluster that the node belongs to
        @ivar test_record['test_file']: The file to be copied.
        '''
        gateway_node = self.lava_provider.get_node_with_role(self.cluster,
                                                            "GATEWAY")

        swiftly_provider = SwiftlyProvider(self.config, gateway_node)
        swiftly_client = swiftly_provider.swiftly_client
        container_list = swiftly_provider.get_containers()
        self.assertNotEqual(container_list, [], "There are no files "+
                            "in Node Cloud Files.")
        path = "/%s" %container_list[0]
        file_list = swiftly_provider.get_container_objects(path)

        command = 'get'
        hadoop_client = HadoopClient(self.config.lava_api.USER_NAME,
                                     self.config.lava_api.PASSWORD,
                                     gateway_node.ip)
        path = "/%s/%s | hadoop fs -put - %s" % (container_list[0], 
                                                 file_list[0],
                                                 file_list[0])
        swiftly_client.run_command(command, post_variables=path)
        response = hadoop_client.filesystem.list()
        self.assertIn(file_list[0], response, "File '%s' was not found"\
                      " in HDFS" %file_list[0])

